# Teachers Directory

Teachers Directory is a Django Application to create a directory of Teachers , View and Filter data, with a bulk data upload option. 

## Steps To Run the Project

1.Clone the git repo

2.Create a virtualenv and activate it

3.cd into the project directory

4.Install Requirements.txt - ```
pip install -r requirements.txt``` 

5.Make Migrations - ``` python manage.py makemigrations ``` 

 ``` python manage.py migrate``` 

6.Run the server - ``` python manage.py runserver``` 


## Routes
1. '' - Teachers directory 

2. '/add_teacher' - Create a new Teacher entry

3. 'bulk_upload' - Bulk Upload data through a csv (Sample csv in the 
    repo)

4.'/teacher-detail/<id>' - Get Details of a single Teacher

5. '/login_req'- Login
