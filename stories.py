import instagrapi, os, urllib, json, datetime, pyotp

CONTENT_JPG = 1
CONTENT_MP4 = 2

if not os.path.exists("stories"):
	os.mkdir("stories")
	
if not os.path.exists("sessions"):
	os.mkdir("sessions")
	
	
tmp = open("userids.json", "r")
userids = list(json.load(tmp))
tmp.close()

tmp = open("settings.json", "r")
settings = list(json.load(tmp))
tmp.close()
	
grapi = instagrapi.Client()


def magic(st):
	st_ = ""
	for letter in st:
		if letter in "0123456789":
			st_ += letter
	return st_
	
	
today = "-" + magic(str(datetime.datetime.now(datetime.timezone.utc).date()))

yesterday = "-" + magic(str(datetime.datetime.now(datetime.timezone.utc).date() - datetime.timedelta(days = 1)))
tomorrow = "-" + magic(str(datetime.datetime.now(datetime.timezone.utc).date() + datetime.timedelta(days = 1)))


for story in os.listdir("stories"):
	if not today in story and not yesterday in story and not tomorrow in story:
		if os.path.exists("stories/" + story):
			os.remove("stories/" + story)


acc_1 = []
acc_2 = []
acc_3 = []

for index, account in enumerate(settings):
	acc_1.append(account["username"])
	acc_2.append(account["password"])
	acc_3.append(account["totp"])
	try:
		check = instagrapi.Client()
		
		check.login(acc_1[-1], acc_2[-1], verification_code=pyotp.TOTP(acc_3[-1]).now())
	except:
		acc_1.pop(-1)
		acc_2.pop(-1)
		acc_3.pop(-1)
		

for ids in [userids[i:i + 5] for i in range(0, len(userids), 5)]:
	try:
		grapi = instagrapi.Client()

		if not acc_1:
			break
			
		if not acc_2:
			break

		if not acc_3:
			break
				
		if os.path.exists("sessions/" + acc_1[0] + ".json"):
			grapi.load_settings("sessions/" + acc_1[0] + ".json")
		
		grapi.login(acc_1[0], acc_2[0], verification_code=pyotp.TOTP(acc_3[0]).now())
	except:
		pass
		
	try:
		grapi.get_timeline_feed()
	except:	
		try:
			grapi = instagrapi.Client()

			if not acc_1:
				break
				
			if not acc_2:
				break

			if not acc_3:
				break

			username = input("Username: ") 
			password = input("Passwd: ")
						
			acc_1[0] = acc_1[0] if username != "" else acc_1[0]
			acc_2[0] = acc_2[0] if password != "" else acc_2[0]
			
			grapi.login(acc_1[0], acc_2[0], verification_code=pyotp.TOTP(acc_3[0]).now())
		except:
			grapi = instagrapi.Client()

			if not acc_1:
				break
				
			if not acc_2:
				break
			
			if not acc_3:
				break
			
			acc_1.pop(0)
			acc_2.pop(0)
			acc_3.pop(0)
			
			if not acc_1:
				break
				
			if not acc_2:
				break

			if not acc_3:
				break
						
			grapi.login(acc_1[0], acc_2[0], verification_code=pyotp.TOTP(acc_3[0]).now())

	grapi.inject_sessionid_to_public()

	for userid in ids:
		try:
			for story in grapi.user_stories(str(userid)):
				if story.media_type == CONTENT_JPG:
					if not os.path.exists("stories/" + story.user.username + "-" + magic(str(story.taken_at)) + ".jpg"):
						urllib.request.urlretrieve("https://" + story.thumbnail_url.host + story.thumbnail_url.path + "?" + story.thumbnail_url.query, "stories/" + story.user.username + "-" + magic(str(story.taken_at)) + ".jpg")
					print(acc_1[0], story.user.username + "-" + magic(str(story.taken_at)) + ".jpg")
				if story.media_type == CONTENT_MP4:
					if not os.path.exists("stories/" + story.user.username + "-" + magic(str(story.taken_at)) + ".mp4"):
						urllib.request.urlretrieve("https://" + story.video_url.host + story.video_url.path + "?" + story.video_url.query, "stories/" + story.user.username + "-" + magic(str(story.taken_at)) + ".mp4")
					print(acc_1[0], story.user.username + "-" + magic(str(story.taken_at)) + ".mp4")
		except:
			pass
        
        
		doc_dates = []
		doc_names = []
		
		for doc in os.scandir("stories"):
			doc_dates.append(os.path.getctime("stories/" + doc.name))
			
		for doc in os.scandir("stories"):
			doc_names.append(os.path.abspath("stories/" + doc.name))

		for i in range(len(doc_dates)):
			for j in range(0, len(doc_dates) - i - 1):
				if doc_dates[j] > doc_dates[j + 1]:
					doc_dates[j], doc_dates[j + 1] = doc_dates[j + 1], doc_dates[j]
					doc_names[j], doc_names[j + 1] = doc_names[j + 1], doc_names[j]

		
		html = open("stories.html", "w")
		
		for doc_name in reversed(doc_names):
			if ".jpg" in doc_name:
				html.write('''<p style="text-align: center;">''' + doc_name + '''</p><object data="'''  + doc_name + '''" style="display: block; margin: 25px; margin-left: auto; margin-right: auto; border: 1px solid #000000;" width="270" height="480"></object>''')
			if ".mp4" in doc_name:
				html.write('''<p style="text-align: center;">''' + doc_name + '''</p><object data="'''  + doc_name + '''" style="display: block; margin: 25px; margin-left: auto; margin-right: auto; border: 1px solid #000000;" width="270" height="480"></object>''')
			
		html.close()
		
	grapi.dump_settings("sessions/" + acc_1[0] + ".json")
