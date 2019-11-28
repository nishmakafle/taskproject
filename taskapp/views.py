from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.views.generic import *
from .forms import *
from .models import *


class LoginView(FormView):
    template_name = "stafftemplates/login.html"
    form_class = LoginForm

    def form_valid(self, form):
        self.username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        self.user = authenticate(username=self.username,
                                 password=password)
        if self.user is not None and self.user.is_superuser is False:
            login(self.request, self.user)

        elif self.user is not None and self.user.is_superuser is True:
            login(self.request, self.user)
        else:
            return render(self.request, self.template_name, {
                'form': form,
                'errors': "Please correct username or password"})

        return super().form_valid(form)

    def get_success_url(self):
        if self.request.user.user_type == "Staff":
            return reverse('taskapp:staffhome')
        elif self.request.user.user_type == "Admin":
            return reverse('taskapp:adminhome')
        else:
            return reverse('taskapp:login')


class LogoutView(View):
    login_url = reverse_lazy('taskapp:login')

    def get(self, request):
        logout(request)
        return redirect('taskapp:login')


# Staff Views


class StaffRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == "Staff":
            pass
        else:
            return redirect('/login/?next=' + request.path)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasklist'] = Task.objects.filter(
            assigned_to=self.request.user).order_by('-id')

        return context


class StaffHomeView(StaffRequiredMixin, TemplateView):
    template_name = 'stafftemplates/staffhome.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'status' in self.request.GET:
            status = self.request.GET['status']
            context['alltasks'] = Task.objects.filter(
                assigned_to=self.request.user, status=status).order_by('-id')
        else:
            context['alltasks'] = Task.objects.filter(
                assigned_to=self.request.user).order_by('-id')

        return context


class StaffTaskDetailView(StaffRequiredMixin, DetailView):
    template_name = 'stafftemplates/stafftaskdetail.html'
    model = Task
    context_object_name = 'task'


class StaffTaskUpdateView(StaffRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        task = Task.objects.get(id=self.kwargs['pk'])
        status = request.GET.get('status')
        task.status = status
        task.save()
        return JsonResponse({'message': 'Task status updated to ' + status})


# Admin  Views

class AdminRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == "Admin":
            pass
        else:
            return redirect('/login/?next=' + request.path)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['alltasks'] = Task.objects.all().order_by('-id')

        return context


class AdminHomeView(AdminRequiredMixin, TemplateView):
    template_name = 'admintemplates/adminhome.html'


class AdminStaffRegisterView(AdminRequiredMixin, FormView):
    template_name = 'admintemplates/staffregistration.html'
    form_class = RegForm
    success_url = '/'

    def form_valid(self, form):
        a = form.cleaned_data['username']
        b = form.cleaned_data.get('password')
        c = form.cleaned_data.get('first_name')
        d = form.cleaned_data.get('last_name')
        e = form.cleaned_data.get('email')
        f = NewUser.objects.create_user(e, a, b)
        f.user_type = "Staff"
        f.first_name = c
        f.last_name = d
        f.is_staff = True
        f.save()
        return super().form_valid(form)


class AdminTaskCreateView(AdminRequiredMixin, CreateView):
    template_name = 'admintemplates/admintaskcreate.html'
    form_class = TaskForm
    success_url = reverse_lazy('taskapp:adminhome')

    def form_valid(self, form):
        form.instance.assigned_by = self.request.user
        return super().form_valid(form)


class AdminTaskDetailView(AdminRequiredMixin, DetailView):
    template_name = 'admintemplates/admintaskdetail.html'
    model = Task
    context_object_name = 'tasks'


class AdminTaskUpdateView(AdminRequiredMixin, UpdateView):
    template_name = 'admintemplates/admintaskcreate.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('taskapp:adminhome')


class AdminTaskDeleteView(DeleteView):
    template_name = 'admintemplates/admintaskdelete.html'
    model = Task
    success_url = reverse_lazy('taskapp:adminhome')
