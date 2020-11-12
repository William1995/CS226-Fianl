#_*_coding:utf-8_*_
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import datetime
from collections import Counter

# collect data form DB
def connect_DB(city_list,start_time,end_time):

	json_dataset = []
	if len(city_list) >= 1:
		for city in city_list:
			
			MONGODB_HOST = 'localhost'
			MONGODB_PORT = 27017
			DBS_NAME = city
			COLLECTION_NAME = 'tweet'
			FIELDS = {"text": True, "datetime": {'$lte': end_time, '$gte': start_time}, "_id": False}

			connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
			collection = connection[DBS_NAME][COLLECTION_NAME]
			data = collection.find({"datetime": {'$gte': str(start_time),'$lte': str(end_time)}},{"text": 1, "datetime":1 ,"_id": 0})

			for rowdata in data:
				json_dataset.append(rowdata)

		json_dataset = json.dumps(json_dataset, default=json_util.default)
		json_dataset = json.loads(json_dataset)

		connection.close()

	return json_dataset

# create query to find specific data
def select_from_DB(city_list,start_month,start_date,end_month,end_date):
	start_time = datetime.datetime(2019, int(start_month), int(start_date), 0, 0, 0, 0)
	end_time = datetime.datetime(2019, int(end_month), int(end_date), 23, 59, 59, 59)
	selected_data = connect_DB(city_list,start_time,end_time)

	return selected_data

# select content by hashtag
def select_from_content(data,brand_list):
	
	selected_data = []
	remain_data = []

	for brand in brand_list:
		
		for row in data:
			
			if '#' + brand in row['text'].encode("utf-8").lower():
				selected_data.append(row)
			
			else:
				remain_data.append(row)

		data = remain_data
		remain_data = []


	return selected_data

# remove useless info and make data format clean
def data_preprocess(dataset):

	clean_wordset = ''

	# Get the stopword list
	stopword_list = []
	with open("stopword.txt","r") as file:
		for word in file: 
			stopword_list.append(word.strip('\n')) 

	for row in dataset:
		
		# remove all the '\n' to make sentence format clean
		row['text'] = row['text'].replace('\n','')
		
		# remove url 、 pic and useless symbols
		tmp = []
		for word in row['text'].split(' '):
			if '/' not in word and '@' not in word and '=' not in word:
				word = word.encode("utf-8").replace('•','').replace('?','').replace('!','').replace('#','').replace(':','').replace('.','').replace(',','').replace(')','').replace('(','')
				if len(word) > 1:
					tmp.append(word.lower())

		# remove stop word
		for word in tmp:
			if word not in stopword_list:
				clean_wordset = clean_wordset + word.strip('\n') + ' '

	return clean_wordset

# N-gram generator
def generate_ngrams(s, n):

	ngram_sentence = ''

	# Break sentence in the token, remove empty tokens
	tokens = [token for token in s.split(" ") if token != ""]
	# Concatentate the tokens into ngrams and return
	ngrams = zip(*[tokens[i:] for i in range(n)])
	
	for ngram in ngrams:
		ngram_sentence = ngram_sentence + "_".join(ngram) + ' '

	return ngram_sentence 

# Word Cloud
def wordcloud_generator(wordset):
	
	# background image mask
	car_mask = np.array(Image.open("images/222.png"))
	wordcloud = WordCloud(max_font_size=25, max_words=10, background_color="white", mask=car_mask, contour_width=3, contour_color='firebrick').generate(wordset)
	plt.figure(figsize=(10,10))
	plt.imshow(wordcloud, interpolation="bilinear")
	plt.axis("off")
	plt.savefig('images/wordcloud.png')
	plt.close()

def word_freq(wordset):
	if len(wordset) >= 1:
		word_freq_dict = Counter(wordset.split())
		keys = word_freq_dict.keys() 
		values = word_freq_dict.values()
		values,keys = zip(*sorted(zip(values, keys), reverse=True))
		return keys, values

	else:
		return 0,0

# Count each brand in select city
def brand_count(city_data,brand_list):
	brand_count = []

	for brand in brand_list:
		count = 0
		
		for row in city_data:
			text = row['text'].encode("utf-8").lower()

			if '#' + brand.lower() in text:
				count = count + 1

		brand_count.append(count)

	return brand_list,brand_count

# for hotmap data
def generate_hotmap_data(brand,start_month,start_date,end_month,end_date):
	city_list = ['Birmingham', 'Anchorage', 'Phoenix', 'LosAngeles', 'Denver', 'Billings', 'Omaha', 'LasVegas', 'Manchester', 'Newark', 'Albuquerque', 'NewYork', 'Charlotte', 'Fargo', 'Columbus', 'OklahomaCity', 'Portland', 'Philadelphia', 'Providence', 'Columbia', 'SiouxFalls', 'Memphis', 'Houston', 'SaltLakeCity', 'Burlington', 'VirginiaBeach', 'Seattle', 'Charleston', 'Milwaukee', 'Cheyenne']

	result = []
	for city in city_list:
		select_data = select_from_DB([city],start_month,start_date,end_month,end_date)
		key,count = brand_count(select_data,brand)
		result.append(count[0])
	
	return result

#dd = select_from_DB(['Phoenix'],10,1,11,30)
#dd = select_from_content(dd,['bmw'])
#dd = data_preprocess(dd)
#wordcloud_generator(dd)
