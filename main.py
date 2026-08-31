# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import os
import sys
import subprocess
from pathlib import Path


welcome_message = """
 ____  _                       ____                  _
|  _ \(_)__ _ _ __   __ _  ___/ ___|  ___ _ ____   _| |_ ___  _ __
| | | | / _` | '_ \ / _` |/ _ \___ \ / _ \ '__\ \ / / __/ _ \| '__|
| |_| | | (_| | | | | (_| |  __/___) |  __/ |   \ V /| || (_) | |
|____/|_|\__, |_| |_|\__, |\___|____/ \___|_|    \_/  \__\___/|_|
          |___/        |___|
"""

def greeting_message():
    print(welcome_message)
    print('Hey Fellas!')
    x = input('Enter Your Django Project Name : ')
    y = input('Enter Your Django App Name : ')
    return x,y 

def creation():
    x, y = greeting_message() #unpacking deed
    subprocess.check_call([sys.executable,'-m', 'venv', 'myenv'])
    if os.name == 'nt':
        venv_pip = os.path.join('myenv', 'Scripts', 'pip.exe')
        venv_django_admin = os.path.join('myenv', "Scripts", "django-admin.exe")
    else:            
        venv_pip = os.path.join('myenv', 'bin', 'pip')
        venv_django_admin = os.path.join('myenv', "bin", "django-admin")
    
    subprocess.check_call([venv_pip, 'install', 'django'])
    subprocess.check_call([venv_pip,'install','python-dotenv'])

    
    subprocess.check_call([venv_django_admin, 'startproject', x])
    os.chdir(x)


    #to reate django app now
    if os.name == 'nt':
        venv_python = os.path.join('..','myenv','Scripts','python.exe')
    else:
        venv_python = os.path.join('..','myenv','bin','python')

    #writing the subprocess
    subprocess.check_call([venv_python, 'manage.py', 'startapp', y])
    

    files = [
        'templates/base.html',
        'templates/components/navbar.html',
        'templates/components/footer.html',
        f'templates/{y}/index.html',
        'static/css/style.css',
        'static/js/script.js',
        'static/image/n.jpeg',
        '.env',
        'README.md',
        'media/sample.jpeg'
    ]

    for file in files:
        path = Path(file)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()
    
    Path("templates/base.html").write_text("""
    {%load static%}
    <!DOCTYPE html>
    <html lang = 'en'>
    <head>
    <title>{% block title %} My Project {%endblock %}</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
    </head>
    <body>
    {%include 'components/navbar.html'%}
    {% block content %}
    {% endblock %}
    {%include 'components/footer.html'%}
    </body>
    </html>
    """)

    Path('templates/components/footer.html').write_text(
        """
        {% load static %} 
        <footer>
        </footer>
        """
    )
    Path('templates/components/navbar.html').write_text(
        """
        {% load static %} 
        <nav>
        </nav>
        """
    )

    Path(f'templates/{y}/index.html').write_text(
        """
        {% load static %}
        {% extends 'base.html' %}
        {%block title%}
        {%endblock %}
        {%block content%}
        {%endblock%}
        
        """
    )

    Path(f'{x}/settings.py').write_text(
        Path(f'{x}/settings.py').read_text().replace(
            "STATIC_URL = 'static/'",
            """
            STATIC_URL = 'static/'
            STATICFILES_DIRS = [BASE_DIR / 'static',]
            STATIC_ROOT = BASE_DIR / "staticfiles"
            MEDIA_ROOT = BASE_DIR / 'media'
            MEDIA_URL = '/media/'

            """
            ))
    
    Path(f'{x}/settings.py').write_text(
        Path(f'{x}/settings.py').read_text().replace(
        "'DIRS': [],",
        "'DIRS': [BASE_DIR / 'templates'],"
        )
    )

    Path(f'{x}/settings.py').write_text(
        Path(f'{x}/settings.py').read_text().replace(
        "'django.contrib.staticfiles',",
        f"'django.contrib.staticfiles',\n    '{y}',"
        )
    )
    
    subprocess.check_call([venv_python, 'manage.py', 'migrate'])



    print('[✓] Django Project Created!')
    print('[✓] Django App Created!')
    print('[✓] Boilerplate injected!')
    print('Settings file configured!')
    print('[✓] Good Luck with your project.')


if __name__ == '__main__':
    creation()