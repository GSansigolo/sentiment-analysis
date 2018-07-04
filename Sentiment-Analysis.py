'''
Created on Oct 05, 2017
Author: @G_Sansigolo
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

number_tweet_pos = 0
number_tweet_neg = 0

'''
connect mongodb database
'''

client = MongoClient()
db = client.tweet_db_1
tweet_collection = db.tweet_collection
tweet_collection.create_index([("id", pymongo.ASCENDING)],unique = True) 

'''
query collected data in MongoDB
'''

tweet_cursor = tweet_collection.find()
  
print (tweet_cursor.count())
  
user_cursor = tweet_collection.distinct("user.id")
 
print (len(user_cursor))

for document in tweet_cursor:
	
	#Variables
	number_words_pos = 0
	number_words_neg = 0

	#Tweets
	print ('----')
	print ('name:', document["user"]["name"])
	print ('text:', document["text"])

	#Sentiment-Analysis
	lista=document["text"].split(" ")
	for i in range(len(lista)):
		if lista[i] in lista_pos:
			number_words_pos =+1
		if lista[i] in lista_neg:
			number_words_neg =+1
	if 	(number_words_pos > number_words_neg):
		number_tweet_pos =+1
	if (number_words_pos < number_words_neg):
		number_tweet_neg =+1

print ('----')

print(number_tweet_pos, number_tweet_neg)

'''
plot
'''

labels = 'Tweets Positivo','Tweets Negativo'

sizes = [number_tweet_pos, number_tweet_neg]

fig1, ax1 = plt.subplots()

ax1.set_title('Análise Sentimental dos Tweets')

ax1.pie(sizes, labels=labels, autopct='%1.2f%%',
        shadow=True, startangle=90, colors=['gold', 'lightskyblue'])

ax1.axis('equal')

plt.show()

