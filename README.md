
## Steps to run the project

Create and active virtual environment using

```
python -m venv env
cd env
scripts\activate
```

Change the directory using

```
cd ..
cd searchProject
```

Now you need to install python packages to run the project

```
pip install -r requirements.txt
```

Run commands for migration and migrate

```
python manage.py makemigrations
python manage.py migrate
```

Create superuser

```
python manage.py createsuper
```

Run Django app

```
python manage.py runserver
```


# Endpoint 


```
http://127.0.0.1:8000/
```

