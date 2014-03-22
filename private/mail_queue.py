import time
while True:
	rows=db(db.queue.status=='pending').select()
	for i in len(rows):
		if rows[i]['dat']==datetime.date.today():
			mail.send(rows[i]['email'],subject='task',message='Your Task is approaching .. Stop fucking around')
	time.sleep(10)
				
