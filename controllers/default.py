#search by date 
#email sending(send a copy and for reminders)
#note downloading
#text editor(if possible)
#friend requests and privacy
import datetime
import os
import re
# -*- coding: utf-8 -*-
import time
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


import gluon.contrib.simplejson
@auth.requires_login()
def index():
    """
    example action using the internationalization operator t and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    """
    p='No tasks yet completed :('
    q='No pending tasks :)'
    a=db(db.auth_user.id==auth.user.id).select()
    b=a[0]['notes']
    c=db(db.task.authoris==auth.user.email).select()
    for i in range(0,len(c)):
	    if c[i]['done']:
	    	p='Completed Tasks :'
	    else:
	    	q='Pending Tasks :'
    response.flash ="Welcome to Notes!"
    return dict(b=b,a=[],c=c,p=p,q=q)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
@auth.requires_login()
def create():
	response.flash='Create Your Notes Here !'
	if session.msg=='NO':
		response.flash='Invalid Title!'
		session.msg='Yes'
	form=SQLFORM.factory(
		Field('title','string',label='Title'),
		Field('description','string',label="Short description",requires=IS_NOT_EMPTY()),
		Field('val','text',label='Note',requires=IS_NOT_EMPTY()),
		Field('tags','string',label="tag the table with word/s"))
	if form.process().accepted:
		a=db(db.auth_user.id==auth.user.id).select()
		if form.vars.title in a[0]['notes'].split('@'):
			session.msg='NO'
			redirect(URL('create'))
		b=a[0]['notes']+'@'+form.vars.title
		c=form.vars.tags.split(',')
		db(db.auth_user.id==auth.user.id).update(notes=b)
		session.title=form.vars.title
		db.note.insert(title=form.vars.title,cd=request.now,md=request.now,description=form.vars.description,val=form.vars.val,tags=form.vars.tags,authoris=auth.user.email)
		for i in range(len(c)):	
		 	db.tags.insert(word=c[i],title=form.vars.title,authoris=auth.user.email)	
		redirect(URL('cr'))
	return dict(form=form)

@auth.requires_login()
def cr():
	message='Want to add Attachments ?'
	return dict(message=message)

@auth.requires_login()
def cratt():
	if session.msg=='A':
		response.flash='Change File Name'
		session.msg='Y'
	title=session.title
	message='Hi'
	a=db((db.att.title==title)&(db.att.usr==auth.user.email)).select()
	form=SQLFORM(db.att,deletable=True,upload=os.path.join(request.folder,'/pic'))
	if request.vars.fil!=None:
		form.vars.nm=request.vars.fil.filename
	if form.process().accepted:
		a=db((db.att.nm==form.vars.nm)&(db.att.usr==auth.user.email)&(db.att.title==session.title)).select()
		if len(a)>0:
			session.msg='A'
			redirect(URL('cratt'))
		db(db.att.fil==form.vars.fil).update(usr=auth.user.email,title=title,nm=form.vars.nm)
		redirect(URL('cratt'))
	return dict(a=a,form=form)
@auth.requires_login()
def show():
	title=request.args(0,cast=str).strip()
	title=title.replace('_',' ')
	session.title=title
	a=db((db.note.title==title)& (auth.user.email==db.note.authoris)).select()
	tit=a[0]['title']
	val=a[0]['val']
	des=a[0]['description']
	tags=a[0]['tags']
	ct=a[0]['cd']
	mt=a[0]['md']
	l=db((db.att.title==title)&(db.att.usr==auth.user.email)).select()
	return dict(title=tit,val=val,des=des,tags=tags,ct=ct,mt=mt,a=a,l=l)
@auth.requires_login()
def edit():
	if session.message=='NOT':
		response.flash='Invalid Username'
		session.message='Yes'
	title=request.args(0,cast=str).replace('_',' ')
	title=title.replace('_',' ')
	c=db((db.note.title==title)&(db.note.authoris==auth.user.email)).select()
	form=SQLFORM.factory(
		Field('title','string',label='Title',default=c[0]['title']),
		Field('description','string',label='Description',default=c[0]['description']),
		Field('val','text',label='Note',default=c[0]['val'],requires=IS_NOT_EMPTY()),
		Field('tags','string',label='Tags',default=c[0]['tags']))
	if form.process().accepted:
		c=form.vars.tags.split(',')
		a=db(db.note.title==form.vars.title).select()
		if len(a)==1 and a[0]['title']!=title:
			session.message='NOT'
			redirect(URL('edit',args=title))
		db((db.tags.title==title)&(db.tags.authoris==auth.user.email)).delete()
		for i in range(len(c)):	
		 	db.tags.insert(word=c[i],title=form.vars.title,authoris=auth.user.email)	
		
		db((db.note.title==title)&(auth.user.email==db.note.authoris)).update(title=form.vars.title,md=request.now,description=form.vars.description,val=form.vars.val,tags=form.vars.tags)
		a=db(db.auth_user.id==auth.user.id).select()
		a=a[0]['notes']
		b=a.split('@')
		a=''
		for i in range(1,len(b)):
			if b[i].strip()==title.strip():
				b[i]=form.vars.title
			a+='@'+b[i]
		db(db.auth_user.id==auth.user.id).update(notes=a)
		redirect(URL('show',args=form.vars.title))
	return dict(form=form)
@auth.requires_login()
def edshow():
    a=db(db.auth_user.id==auth.user.id).select()
    b=a[0]['notes']
    response.flash = "You can edit notes here!"
    return dict(b=b,a=[])
@auth.requires_login()
def eddel():
    a=db(db.auth_user.id==auth.user.id).select()
    b=a[0]['notes']
    response.flash = "Are you sure ? :("
    return dict(b=b,a=[])
@auth.requires_login()
def shdel():
	title=request.args(0,cast=str).replace('_',' ')
	title=title.replace('_',' ')
	return dict(title=title)
@auth.requires_login()
def delet():
	title=request.args(0,cast=str).replace('_',' ')
	title=title.replace('_',' ')
	db((db.note.title==title)&(db.note.authoris==auth.user.email)).delete()
	db((db.tags.title==title)&(db.tags.authoris==auth.user.email)).delete()
	db((db.att.usr==auth.user.email)&(db.att.title==title)).delete()
	a=db(db.auth_user.id==auth.user.id).select()
	a=a[0]['notes']
	b=a.split('@')
	a=''
	for i in range(1,len(b)):
		if b[i].strip()==title.strip():
			continue
		a+='@'+b[i]
	db(db.auth_user.id==auth.user.id).update(notes=a)
	redirect(URL('index'))
	return dict(form=form)
@auth.requires_login()
def searchinp():
	form=SQLFORM.factory(Field('Name','string',requires=IS_NOT_EMPTY()),
			Field('Choice',requires=IS_IN_SET(['Title','Tags'])))
	if form.process().accepted:
		if form.vars.Choice=='Title':
			redirect(URL('searchtit',args=form.vars.Name))
		elif form.vars.Choice=='Tags':
			redirect(URL('searchtag',args=form.vars.Name))
	return dict(form=form)
@auth.requires_login()
def searchtag():
	a=request.args(0,cast=str).replace('_',' ')
	a=a.replace('_',' ')
        nam=[]
	tit=[]
        name=db(db.tags.id>0).select(db.tags.ALL)
	l=len(name)
	for i in range(len(name)):
		mat=re.search(a,name[i]['word'])
		if mat and name[i]['authoris']==auth.user.email:
			nam.append(name[i])
	return dict(nam=nam)
@auth.requires_login()
def litetag():
	tagname=[]
	notest=[]
	a=db(auth.user.email==db.tags.authoris).select(db.tags.ALL)
	for i in range(len(a)):#if len(a) is zero then tell that there is no tags attached
		if a[i]['word'] not in tagname:
			tagname.append(a[i]['word'])
			tmp=[];
			for j in range(len(a)):
				if a[i]['word']==a[j]['word']:
					tmp.append(a[j]['title'])
			notest.append(tmp)
	return dict(tagname=tagname,notest=notest)

@auth.requires_login()
def searchtit():
	a=request.args(0,cast=str).replace('_',' ')
	a=a.replace('_',' ')
        nam=[]
        name=db(db.note.title>0).select(db.note.ALL)
	l=len(name)
	for i in range(0,l):
		mat=re.search(a,name[i]['title'])
		if mat and name[i]['authoris']==auth.user.email:
			nam.append(name[i])
	return dict(nam=nam)
@auth.requires_login()
def crtask():
	a={}
	response.flash='Create Tasks Here'
	if session.msg=='N':
		response.flash='Invalid Title'
		session.msg='Y'
	elif session.msg=='T':
		response.flash='Invalid Date'
		session.msg='Y'
	form=SQLFORM.factory(
			Field('title','string',label='Title',requires=IS_NOT_EMPTY()),
			Field('des','string',label='Description'),
			Field('pen','date',label='Date'))
	if form.process().accepted:
		a=db((db.task.title==form.vars.title)&(db.task.authoris==db.auth_user.email)).select()
		if len(a)>0:
			session.msg='N'
			redirect(URL('crtask'))
		if form.vars.pen<datetime.date.today():
			session.msg='T'
			redirect(URL('crtask'))
		if len(a)==0:
			db.task.insert(title=form.vars.title,description=form.vars.des,pending=form.vars.pen,done=False,authoris=auth.user.email)
			redirect(URL('index'))
	return dict(form=form,a=a)
@auth.requires_login()
def shtask():
	title=request.args(0,cast=str).strip()
	title=title.replace('_',' ')
	a=db((db.task.title==title)& (auth.user.email==db.task.authoris)).select()
	tit=a[0]['title']
	des=a[0]['description']
	l=db(db.att.title==title).select()
	return dict(title=tit,description=des,a=a,pending=a[0]['pending'])
@auth.requires_login()
def taskde():
	response.flash='Are You Sure ??'
	title=request.args(0,cast=str).strip()
	title=title.replace('_',' ')
	return dict(title=title)
@auth.requires_login()
def taskdel():
	title=request.args(0,cast=str).strip()
	title=title.replace('_',' ')
	db((db.task.title==title)&(db.task.authoris==auth.user.email)).delete()
	message='Done'
	redirect(URL('index'))
	return (message)
@auth.requires_login()
def taskshdel():
	a=db(db.task.authoris==auth.user.email).select()
	return dict(a=a)

def help():
	response.flash='Hi'
	message='In case of doubts contact the developers'
	return dict(message=message)
@auth.requires_login()
def taskedit():
	if session.message=='NOT':
		response.flash='Invalid Username'
		session.message='Yes'
	title=request.args(0,cast=str).strip()
	title=title.replace('_',' ')
	c=db(db.task.title==title).select()
	form=SQLFORM.factory(
		Field('title','string',label='Title',default=c[0]['title']),
		Field('description','string',label='Description',default=c[0]['description']),
		Field('time','date',default=c[0]['pending']),
		Field('done','boolean',default=c[0]['done']))
	if form.process().accepted:
		a=db(db.task.title==form.vars.title).select()
		if len(a)==1 and a[0]['title']!=title:
			session.message='NOT'
			redirect(URL('taskedit',args=title))
		db((db.task.title==title)&(auth.user.email==db.task.authoris)).update(title=form.vars.title,description=form.vars.description,pending=form.vars.time,done=form.vars.done)
		redirect(URL('shtask',args=form.vars.title))
	return dict(form=form,title=title)
@auth.requires_login()
def taskedshow():
    a=db(db.task.authoris==auth.user.email).select()
    response.flash = "You can edit tasks here!"
    return dict(a=a)
@auth.requires_login()
def asearchtit():
	form=SQLFORM.factory(Field('Name','string',requires=IS_NOT_EMPTY()))
	if form.process().accepted:
		redirect(URL('searchtit',args=form.vars.Name))
	return dict(form=form)
@auth.requires_login()
def asearchtag():
	form=SQLFORM.factory(Field('Name','string',requires=IS_NOT_EMPTY()))
	if form.process().accepted:
		redirect(URL('searchtag',args=form.vars.Name))
	return dict(form=form)

@auth.requires_login()
def today():
	form=SQLFORM.factory(Field('Between','date'))
	a=db(db.task.authoris==auth.user.email).select()
	b=[]
	c=datetime.date.today()
	x='No'
	for i in range(0,len(a)):
		if a[i]['pending'].date()==c:
			b.append(a[i])
			x='Yes'
	return dict(x=x,b=b)
@auth.requires_login()
def attdel():
	title=request.args(0,cast=str).strip()
	title=title.replace('_',' ')
	db(db.att.fil==title).delete()
	redirect(URL('cratt'))
	return()
@auth.requires_login()
def attdel1():
	title=request.args(0,cast=str).strip()
	title=title.replace('_',' ')
	db(db.att.fil==title).delete()
	redirect(URL('show',args=session.title))
	return()
@auth.requires_login()
def asearchdate():
	form=SQLFORM.factory(Field('time','date',requires=IS_NOT_EMPTY()))
	if form.process().accepted:
		t=form.vars.time
		redirect(URL('sdate',args=form.vars.time))
	return dict(form=form)
@auth.requires_login()
def sdate():
	a=request.args(0,cast=str)
	nam=[]
	d=[]
	name=db(db.note.authoris==auth.user.email).select()
	l=len(name)
	for i in range(l):
		if str(name[i]['pending'].date())==a:
			nam.append(name[i])
	return dict(nam=nam,d=d)
@auth.requires_login()
def ma():
	mail.send('aniruddhkanojia94@gmail.com',subject='Hi Dude',message='Shikher is a bitch')
	redirect(URL('index'))
	return()
def aaa():
	a={}
	a=['shubham.rai@students.iiit.ac.in']
	db.scheduler_task.insert(
			application_name='notes/appadmin',
			task_name='Task 1',
			group_name='main',
			status='QUEUED',
			function_name='f',
			enabled=True,
			period=60,
			start_time=request.now,
			args=gluon.contrib.simplejson.dumps(a))
#a=db((db.note.title==title)& (auth.user.email==db.note.authoris[1:])).select()
