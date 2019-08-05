=====
tobmag1scrumy
=====

tobmag1scrumy is a simple Django app to conduct Web-based polls. For each
question, visitors can choose between a fixed number of answers.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "tobmag1scrumy" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'tobmag1scrumy',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('', include('tobmag1scrumy.urls')),

3. Run `python manage.py migrate` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/ to participate in the poll.