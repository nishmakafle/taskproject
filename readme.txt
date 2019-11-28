To use this app
1. Install requirements in the environments
	$ pip install -r requirements.txt
2. To use sqlite3 database, make USE_POSTGRESQL = False
	and to Use postgres database, make USE_POSTGRESQL = True
	also dont forget to change the database configuration

3. Make a superuser and login to django admin site after running 
	development server
	http://127.0.0.1:8000/django-admin

4. Make admin from there 
5. Now go to http://127.0.0.1:8000
6. Enter the required credentials and you will be sent to admin panel
7. Add multiple staffs from the admin panel.
8. In another browser, login as staff
9. Assign new tasks and go to staff panel and you will see the task assigned by
	the admins to the respective staffs. 
10. Staff can only see the tasks that are related to him/her. 
11. Staff can update the task status (Pending, Processing and Completed) 