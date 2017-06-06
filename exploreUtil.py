#EXPLORE DATA HERE
import copy
import re
from collections import defaultdict
import math
import string
import plotUtil
import csv

cleaningParams = string.punctuation.replace('$','')+'â€˜'

def explore(data, clusterNumbers, cluster_centers, weekCount):
	dataset = copy.deepcopy(data)
	dataset['cluster'] = copy.deepcopy(clusterNumbers)
	dataset['cluster_centers'] = copy.deepcopy(cluster_centers)
	dataset['weekcount'] = weekCount
	tfidfCalc(dataset)

def cleanToken(token):
	return token.strip(cleaningParams).lower()

def tfidfCalc(dataset):
	stopwords = set(line.strip() for line in open('stopwords.txt'))
	weeks = dataset['weekcount']
	dataset['cluster_strings'] = []
	dataset['article_strings'] = []
	dataset['top_set'] = []
	dataset['top_idf'] = []
	for w in range(weeks):
		N = len(dataset['cluster_centers'][w]['lat'])
		valid_indexes = dataset['cluster_centers'][w]['points']['index']

		#TF
		n_gram_min = 1
		n_gram_max = 4
		top_per_n = 2
		tf = {}
		articletf = {}
		df = defaultdict(int)
		seens = []
		for i in range(N):
			seens.append(set())

		def tf_line(line, index):
			cluster = dataset['cluster'][w][index]

			doc_tf = defaultdict(int)
			if cluster in tf:
				doc_tf = tf[cluster]
			else:
				tf[cluster] = doc_tf

			article_tf = defaultdict(int)
			if index in articletf:
				article_tf = articletf[index]
			else:
				articletf[index] = article_tf

			raw_tokens = re.split(r'[ -]+',line)

			tokens = []
			#do we want the df to be based on each article or cluster
			#picked article
			seen = set()#seens[cluster]
			for raw_token in raw_tokens:
				token = cleanToken(raw_token)
				if token in stopwords:
					continue
				if len(token) > 0:
					tokens.append(token)
					tokens_len = len(tokens)
					for n in range(n_gram_min,n_gram_max+1):
						if tokens_len < n:
							break
						ngram = tuple(tokens[-n:])
						article_tf[ngram] += 1
						doc_tf[ngram] += 1
						if ngram not in seen:
							df[ngram] += 1
							seen.add(ngram)
		index = 0
		for i in valid_indexes:
			title = dataset['title'][i]
			tf_line(title,index)
			index += 1
		index = 0
		for i in valid_indexes:
			topic = dataset['topic'][i]
			tf_line(topic,index)
			index += 1
		#IDF
		idf = defaultdict(float)
		for token, doc_count in df.items():
			idf[token] = math.log(1.0 + (N/(1.0+doc_count)))
			#idf[token] = 1

		#TF IDF
		tfidf = {}
		cluster_strings = []
		topset = {}
		for i in range(N):
			cluster_string = ''
			doc_tf = tf[i]
			doc_tfidf = {}
			tfidf[i] = doc_tfidf
			for token in doc_tf:
				doc_tfidf[token] = (1 + math.log(doc_tf[token])) * idf[token]
			#print(i)
			counts = defaultdict(int)
			perLength = top_per_n
			counter = 0
			used_tokens = set()
			for token in sorted(doc_tfidf, key=doc_tfidf.get, reverse=True):
				if counts[len(token)] >= perLength or token in used_tokens:
					continue
				flag = False
				for j in range(len(token)):
					subTuple = tuple(token[:j])+tuple(token[j+1:])
					if subTuple in used_tokens:
						flag = True
						break
					else:
						used_tokens.add(subTuple)
				if flag:
					continue
				#print(token, doc_tfidf[token], idf[token])
				topset[token] = doc_tfidf[token]
				used_tokens.add(token)
				cluster_string += ' '.join(token) + '<br>'
				counts[len(token)] += 1
				counter += 1
				if counter == (n_gram_max - n_gram_min + 1)*perLength:
					break
			cluster_strings.append(cluster_string)
		dataset['cluster_strings'].append(cluster_strings)
		#get top 3 tfidf ngrams also for articles
		article_strings = []
		index = 0
		for i in valid_indexes:
			cluster_string = ''
			doc_tf = articletf[index]
			doc_tfidf = {}
			for token in doc_tf:
				doc_tfidf[token] = (1 + math.log(doc_tf[token])) * idf[token]
			for token in sorted(doc_tfidf, key=doc_tfidf.get, reverse=True)[:3]:
				cluster_string += ' '.join(token) + '<br>'
			article_strings.append(cluster_string)
			index += 1
		dataset['article_strings'].append(article_strings)
	plotUtil.plotTfidf(dataset)
	
