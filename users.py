import instagrapi, os, urllib, json, datetime, pyotp


if not os.path.exists("users"):
	os.mkdir("users")
	
if not os.path.exists("sessions"):
	os.mkdir("sessions")
	
	
tmp = open("userids.json", "r")
userids = list(json.load(tmp))
tmp.close()

tmp = open("settings.json", "r")
settings = list(json.load(tmp))
tmp.close()
	
grapi = instagrapi.Client()


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
			info = grapi.user_info(str(userid))
			
			urllib.request.urlretrieve(str(info.profile_pic_url_hd), "users/" + info.username + ".jpg")
			
			print(acc_1[0], info.username + ".jpg")
		except:
			pass
			
			
		doc_dates = []
		doc_names = []
		
		for doc in os.scandir("users"):
			doc_dates.append(os.path.getctime("users/" + doc.name))
			
		for doc in os.scandir("users"):
			doc_names.append(os.path.abspath("users/" + doc.name))

		for i in range(len(doc_dates)):
			for j in range(0, len(doc_dates) - i - 1):
				if doc_dates[j] > doc_dates[j + 1]:
					doc_dates[j], doc_dates[j + 1] = doc_dates[j + 1], doc_dates[j]
					doc_names[j], doc_names[j + 1] = doc_names[j + 1], doc_names[j]

		
		html = open("users.html", "w")
		
		for doc_name in reversed(doc_names):
			if ".jpg" in doc_name:
				html.write('''<p style="text-align: center;">''' + doc_name + '''</p><object data="'''  + doc_name + '''" style="display: block; margin: 25px; margin-left: auto; margin-right: auto; border: 1px solid #000000;" width="640" height="640"></object>''')
			if ".mp4" in doc_name:
				html.write('''<p style="text-align: center;">''' + doc_name + '''</p><object data="'''  + doc_name + '''" style="display: block; margin: 25px; margin-left: auto; margin-right: auto; border: 1px solid #000000;" width="640" height="640"></object>''')
			
		html.close()
		
	grapi.dump_settings("sessions/" + acc_1[0] + ".json")
