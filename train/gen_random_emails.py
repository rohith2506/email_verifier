'''
Generate Random emails
'''

import random

domains = ["gmail.com", "yahoo.com", "outlook.com", "mail.ru", "mail.kz", "bing.com"]
letters = "abcdefghijklmnopqrstuvwxyz"

def get_random_email():
	name = ''.join(random.choice(letters) for i in range(7))
	domain = random.choice(domains)
	return name + '@' + domain

if __name__ == "__main__":
	open("bad_emails.txt", "w").close()
	ofile = open("bad_emails.txt", "a")
	for i in range(100000):
		email = get_random_email()
		ofile.write(email+"\n")
	ofile.close()
