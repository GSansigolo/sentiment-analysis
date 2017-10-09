'''
Created on Oct 05, 2017
@edited by: g_sansigolo
'''
import string
import pymongo
import codecs
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient
from pprint import pprint

'''
connect get words database
'''

ln = []
lp = []

lista_pos = open("sentiment-data/hu_liu_words/positive-words.txt", "r")

lista_pos = lista_pos.readlines()
for lines in lista_pos:
	lp.append(lines.replace("\n", ""))

lista_pos = lp

lista_neg = open("sentiment-data/hu_liu_words/negative-words.txt", "r")

lista_neg = lista_neg.readlines()
for lines in lista_neg:
	ln.append(lines.replace("\n", ""))

lista_neg = ln


'''
lista_pos = {'viva', 'liberte', 'legal'}
lista_neg = {'executa', 'mata', 'morte'}
'''

number_tweet_pos = 0
number_tweet_neg = 0

'''
connect mongodb database
'''
client = MongoClient()
db = client.tweet_db_1
tweet_collection = db.tweet_collection
tweet_collection.create_index([("id", pymongo.ASCENDING)],unique = True) # make sure the collected tweets are unique

'''
query collected data in MongoDB
'''

tweet_cursor = tweet_collection.find()
  
print (tweet_cursor.count())
  
user_cursor = tweet_collection.distinct("user.id")
 
print (len(user_cursor))

for document in tweet_cursor:
	
	#Variaveis
	number_words_pos = 0
	number_words_neg = 0

	#Tweets
	print ('----')
	print ('name:', document["user"]["name"])
	print ('text:', document["text"])

	#Função
	lista=document["text"].split(" ")
	for i in range(len(lista)):
		if lista[i] in lista_pos:
			number_words_pos = number_words_pos+1
		if lista[i] in lista_neg:
			number_words_neg = number_words_neg+1
	if 	(number_words_pos > number_words_neg):
		number_tweet_pos = number_tweet_pos+1
	if (number_words_pos < number_words_neg):
		number_tweet_neg = number_tweet_neg+1

print ('----')

print(number_tweet_pos, number_tweet_neg)


'''
colocar aqui o matplotlib
'''
