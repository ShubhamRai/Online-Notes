def ma(*a):
#	a=request.args(0,cast=str)
	import datetime
#	a=db(db.tasks.id>0).select()
#	db
#f=open('a')
	print a[0]
	mail.send(a[0],subject=a[1],message='You Have Tasks Pending')
#for i in range(len(a)):
#		if a[i]['pending']==datetime.date.today():
#			mail.send(a[i]['authoris'],subject='Pending Task',message='You have a task pending '+a[i]['title'])
	return
from gluon.scheduler import Scheduler
scheduler=Scheduler(db,dict(f=ma))
