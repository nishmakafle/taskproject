from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not username:
            raise ValueError("Invalid")
        user = self.model(
            username=username,
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,

        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class NewUser(AbstractBaseUser):
    username = models.CharField(
        verbose_name="username", max_length=100, unique=True)
    email = models.EmailField(unique=True, max_length=30)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(
        verbose_name='last_login', auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    user_type = models.CharField(max_length=50, choices=(
        ('Admin', 'Admin'), ('Staff', 'Staff')))

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


TASK_STATUS = (
    ('Pending', 'Pending'),
    ('Processing', 'Processing'),
    ('Completed', 'Completed'),
)


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ForeignKey(
        NewUser, on_delete=models.CASCADE, related_name="totasks")
    assigned_by = models.ForeignKey(
        NewUser, on_delete=models.CASCADE, related_name="fromtasks")
    assigned_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField()
    status = models.CharField(
        max_length=50, choices=TASK_STATUS, default="Pending")

    def __str__(self):
        return self.title
