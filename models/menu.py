# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('Home !'),
                  _class="brand",_href=URL('default','index'))

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Notes'), False, URL('default', 'index'), [
     (T('Create'), False , URL('default', 'create')),
     (T('Edit'),False,URL('default','edshow')),
    (T('Delete'),False,URL('default','eddel'))]),
    (T('Tasks'),False,URL('default','index'),[
     (T('Create'),False,URL('default','crtask')),
     (T('Edit'),False,URL('default','taskedshow')),
     (T('Delete'),False,URL('default','taskshdel'))]),
    (T('Search'),False,URL('default','searchinp'),[
     (T('By Title'),False,URL('default','asearchtit')),
     (T('By Tags'),False,URL('default','asearchtag'))]),
    (T('View by Tags'),False,URL('default','litetag')),
    (T('Help'),False,URL('default','help'))
]


#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

