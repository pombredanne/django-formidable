# django-formidable

django-formidable is a full django application allows you to create, edit, delete and use forms.


## warning

Python Compatibility : python2.7 (tox said it's compliant until python3.2, but I don't)
Django compatibility : django1.8

It's not prod-ready for the moment, no version has been released on official Pypi.

## Licence

MIT Licence

## Quick-Start

### Install

No release is available, but we can install it from github.

    sudo pip install git+https://github.com/peopledoc/django-formidable.git


### Configure

#### Define Roles

django-formidable allows to access a single form with different role. The same
form can be rendered in different way. If you don't have to handle multiple roles
you have to define at least a default role.

Define a method which returns a list of formidable.accesses.AccessObject


    def get_roles(self):
        return [
            AccessObject(id='padawan', label='Padawan'),
            AccessObject(id='jedi', label='Jedi')
        ]


Fill the settings key

    FORMIDABLE_ACCESS_RIGHTS_LOADER = 'yourproject.access_rights.get_roles'


##### Get context

While accessing a form for a specific role, you need to provide a way in order
to get the which context to use.

`request` and `kwargs` are fetch from view (self.request, self.kwargs)

    def get_context(request, kwargs):
        return request.user.user_type


Next fill the setting key ``FORMIDABLE_CONTEXT_LOADER``

    FORMIDABLE_CONTEXT_LOADER = 'yourprojects.access_rights.get_context'

### Define URL's

URLs are defined in :mod:`formidable.urls`. You can load them with the
following line:

    url(r'^api/', include('formidable.urls', namespace='formidable'))
