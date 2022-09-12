# Assignment 

## Question 

```
Build custom filtering feature to support complex queries for Django.

The API filtering has to allow using parenthesis for defining operations precedence and use any combination of the available fields. The supported operations include or, and, eq (equals), ne (not equals), gt (greater than),
lt (lower than).

Example -> "(date eq 2016-05-01) AND ((distance gt 20) OR (distance lt 10))" Example 2 -> "distance lt 10"

Interface should look like this:

def parse_search_phrase(allowed_fields, phrase):
    ...
    return Q(...)
so I can use it like:

search_filter = parse_search_phrase(allowed_fields, search_phrase) 

queryset = MyModel.objects.filter(search_filter)
```

## To Run Program 

1. Create a virtual environment 
    ```
    python -m venv venv 
            or 
    python3 -m venv env
    ```

2. Activate Virtual Environment 
    ```
    source venv/bin/activate
    ```

3. Install packages 
    ```
    pip install -r requirements.txt
    ```

4. You don't have to run migrations as I am pushing a database too for testing purpose. 

5. If you want to enter data into Student model then create a superuser. 

    ```
    # In terminal 
    python manage.py createsuperuser

    ```

6. If you want to use already created admin account then 
    ```
    username = admin
    password = 1234
    ```

7. Run Project and goto admin panel 
    ```
    python manage.py runserver 

    url = 127.0.0.1:8000/admin/
    ```

## Constraint

```
string_query, each word or symbol should be seperated with space. 

```


## To check the function 

1. Open Terminal in main project folder 
2. run shell command
    ```
    python manage.py shell 
    ```

3. Import a function from app complex_search
    ```
    from complex_search.utils import parse_search_phrase
    from complex_search.models import Student 

    allowed_fields = ['name', 'dob', 'no_of_degree']

    search_phrase = "( name eq Yubraj ) AND ( ( dob gt 2020-01-01 ) OR ( no_of_degree lt 5 ) )"

    search_filter = parse_search_phrase(allowed_fields, search_phrase) 

    queryset = Student.objects.filter(search_filter)
    ```

4. You can check output from output folder where I have pushed my screenshot.



#### Please let me know for any explanation.