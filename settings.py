import instagrapi, os, urllib, json, datetime, pyotp


tmp = open("userids.json", "r")
userids = list(json.load(tmp))
tmp.close()

tmp = open("settings.json", "r")
settings = list(json.load(tmp))
tmp.close()
	

for index, account in enumerate(settings):
	acc_1 = account["username"]
	acc_2 = account["password"]
	acc_3 = account["totp"]
    
	try:
		check = instagrapi.Client()
		
		check.login(acc_1, acc_2, verification_code=pyotp.TOTP(acc_3).now())
	except:
		settings.pop(index)
		
	
for account in range(0, 10):
	acc_1 = input("Username: ")
	acc_2 = input("Passwd: ")
	acc_3 = input("TOTP: ")
	

	try:
		check = instagrapi.Client()
		
		check.login(acc_1, acc_2, verification_code=pyotp.TOTP(acc_3).now())
		
		check.dump_settings("sessions/" + acc_1 + ".json")
		
		for index, acc in enumerate(settings):
			if acc.get("username") == acc_1:
				settings.pop(index)

		settings.append({"username": acc_1, "password": acc_2, "totp": acc_3})
	except:
		pass

	
	tmp = open("settings.json", "w")
	json.dump(settings, tmp)
	tmp.close()
