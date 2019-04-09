patients = dict({'ujjwal' : 'ujjwal@123', 'daksh' : 'daksh@123', 'kushagra' : 'kushagra@123'})
doctors = dict({'basu' : 'basu@123', 'sandesh' : 'sandesh@123'})

def check_login(username, password):

	if username in patients:
		if(patients[username] == password):
			return 1

	if username in doctors:
		if(doctors[username] == password):
			return 2

	return 0