'''
A simple markhov model which takes list of emails and predicts the probability 
of each n-gram based on previous n-gram
Train with both good and bad emails

problems:
1) why can't i do it for character vs character instead of n-grams vs n-grams???

@Author: Rohith Uppala
'''

import re
import pdb
import operator
import math
from datetime import datetime, timedelta

class MarkhovModel(object):
	def __init__(self):
		self.n_grams_dict = {}
		self.n_grams_prob_dict = {}

	def refine_email(self, email):
		'''
		cut down the alpha numeric characters and domain name
		'''
		refined_email = ""
		try:
			email = email.strip().split("@")[0]
			refined_email = ''.join(re.findall('[a-zA-Z]', email))
		except Exception, e:
			print "Error in refining email: %s" %(str(e))
		return refined_email

	def generate_n_grams(self, email):
		'''
		generate n-grams of email (it's an iterator) (unigram)
		'''
		try:
			for length in range(1, 3):
				for pos in range(0, len(email) - length+1):
					yield email[pos:pos+length]
		except Exception, e:
			print "Error in generating n-grams of email: %s" %(str(e))

	def find_prob(self):
		try:
			n_grams_list = self.n_grams_dict.keys()
			for i in range(0, len(n_grams_list)):
				for j in range(i+1, len(n_grams_list)):
					e1, e2 = n_grams_list[i], n_grams_list[j]
					c1, c2 = self.n_grams_dict[e1], self.n_grams_dict[e2]
					p1, p2 = self.n_grams_dict.get(e1+e2, 0) * 1.0 / c1, self.n_grams_dict.get(e1+e2, 0) * 1.0 / c2
					if p1 != 0.0:
						self.n_grams_prob_dict[e1+e2] = p1
					if p2 != 0.0:
						self.n_grams_prob_dict[e2+e1] = p2
		except Exception, e:
			print "Error in running bayes algo: %s" %(str(e))

	def run_algo(self, email):
		try:
			refined_email = self.refine_email(email)
			n_grams_list = []
			for n_gram in self.generate_n_grams(refined_email):
					if n_gram not in self.n_grams_dict:
						self.n_grams_dict[n_gram] = 1
					self.n_grams_dict[n_gram] += 1
		except Exception, e:
			print "Error in running main algo: %s" %(str(e))

	def train(self):
		try:
			print "training good emails....."
			for email in open("good_emails.txt", "r"): m.run_algo(email)
			print "Done!!!"
			print "training bad emails......"
			for email in open("bad_emails.txt", "r"): m.run_algo(email)
			print "Done!!!"
			m.find_prob()
		except Exception, e:
			print "Error in training: %s" %(str(e))

	def test(self, email):
		total_cnt = 0.0
		try:
			email = self.refine_email(email)
			for i in range(0, len(email) - 1):
				total_cnt = total_cnt + self.n_grams_prob_dict.get(email[i] + email[i+1], 0.0)
		except Exception, e:
			print "Error in testing: %s" %(str(e))
		return total_cnt

if __name__ == "__main__":
	m = MarkhovModel()
	m.train()
	while True:
		print "Enter your email: "
		email = raw_input()
		print "email score: ", m.test(email)
