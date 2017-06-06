#K-Means clustering
# https://en.wikipedia.org/wiki/K-means_clustering
# https://en.wikipedia.org/wiki/Lloyd%27s_algorithm
#
# 
#
import math
import random
import plotly
from math import pi, sin, cos
from collections import namedtuple
from random import random, choice
from copy import copy
import plotUtil
import datetime

def run(dataset):
	# The K in k-means. How many clusters do we start with?
	# We will need to change this via some optmization
	# Elbow is a good place
	# https://en.wikipedia.org/wiki/Determining_the_number_of_clusters_in_a_data_set
	K = 7

	#for the weekly ones, sqrt(n/2) is a good ball park
	#learned that in a class


	x = dataset['longitude']
	y = dataset['latitude']

	points = [Point(x=x[i],y=y[i]) for i in range(len(x))]

	#ELBOW METHOD
	elbow_method(points)

	dates = copy(dataset['date'])
	
	start_date = min(dates)
	end_date = max(dates)
	date_delta = end_date - start_date
	weekCount = int(math.ceil(date_delta.days/1.0))+1
	#print(weekCount)
	cluster_centers_list = {}
	closestClusterNumbers = {}
	weekCount_Range = range(weekCount)
	cluster_centers_list['date_range'] = []
	for w in weekCount_Range:
		cluster_centers_list[w] = {}
		points = []
		delta_weeks = datetime.timedelta(days=(1+w))
		single_week = datetime.timedelta(weeks=1)
		
		cluster_centers_list[w]['points'] = {}
		cluster_centers_list[w]['points']['index'] = []
		cluster_centers_list[w]['points']['topic'] = []
		for j in range(len(x)):
			if w == weekCount_Range[-1] or (dates[j] <= start_date + delta_weeks and dates[j] >= start_date + delta_weeks - single_week):
				points.append(Point(x=x[j],y=y[j]))
				cluster_centers_list[w]['points']['index'].append(j)
				cluster_centers_list[w]['points']['topic'].append(dataset['topic'][j])
		#print(len(points))
		k = K
		if w != weekCount_Range[-1]:
			cluster_centers_list['date_range'].append(str(start_date + delta_weeks - single_week) + ' , ' + str(start_date + delta_weeks))
			k = int(math.sqrt(len(points)/2))+2
		else:
			cluster_centers_list['date_range'].append(str(start_date) + ' , ' + str(end_date))
		cluster_centers = lloyd(points, k)

		closestClusterNumbers[w] = []
		cluster_centers_list[w]['points']['lon'] = []
		cluster_centers_list[w]['points']['lat'] = []
		for p in points:
			closestClusterNumbers[w].append(nearest_cluster_center(p,cluster_centers)[0])
			cluster_centers_list[w]['points']['lon'].append(p.x)
			cluster_centers_list[w]['points']['lat'].append(p.y)
		
		
		cluster_centers_list[w]['lon'] = []
		cluster_centers_list[w]['lat'] = []
		for c in cluster_centers:
			cluster_centers_list[w]['lon'].append(c.x)
			cluster_centers_list[w]['lat'].append(c.y)

	plotUtil.plotDataCluster(dataset,cluster_centers_list,closestClusterNumbers, weekCount)

	return (cluster_centers_list, closestClusterNumbers, weekCount)
	#print("Plotting points, launching browser ...")
	#plotClusters(centroids, C)

def elbow_method(points):
	#creates a graph to determine k
	#change k manually after visual
	ks = []
	sses = []
	iterations = 4
	for k in range(2,30):
		small_sum = 0
		for iteration in range(iterations):
			cluster_centers = lloyd(points, k)
			small_sum += sumSquaredError(points,cluster_centers)
		sse = small_sum/iterations
		ks.append(k)
		sses.append(sse)
	plotUtil.plotElbowMethod(ks, sses)

def sumSquaredError(points, cluster_centers):
	sse = 0
	for p in points:
		sse += nearest_cluster_center(p,cluster_centers)[1]
	return sse

class Point:
	__slots__ = ["x", "y", "group","topic"]
	def __init__(self, x=0.0, y=0.0, group=0):
		self.x, self.y, self.group = x, y, group

def nearest_cluster_center(point, cluster_centers):
	#Distance and index of the closest cluster center
	def sqr_distance_2D(a, b):
		return (a.x - b.x) ** 2  +  (a.y - b.y) ** 2

	FLOAT_MAX = 1e100
	min_index = point.group
	min_dist = FLOAT_MAX

	for i, cc in enumerate(cluster_centers):
		d = sqr_distance_2D(cc, point)
		if min_dist > d:
			min_dist = d
			min_index = i

	return (min_index, min_dist)


def kpp(points, cluster_centers):
	cluster_centers[0] = copy(choice(points))
	d = [0.0 for _ in range(len(points))]

	for i in range(1, len(cluster_centers)):
		sum = 0
		for j, p in enumerate(points):
			d[j] = nearest_cluster_center(p, cluster_centers[:i])[1]
			sum += d[j]

		sum *= random()

		for j, di in enumerate(d):
			sum -= di
			if sum > 0:
				continue
			cluster_centers[i] = copy(points[j])
			break

	for p in points:
		p.group = nearest_cluster_center(p, cluster_centers)[0]



def lloyd(points, nclusters):
	cluster_centers = [Point() for _ in range(nclusters)]

	# call k++ init
	kpp(points, cluster_centers)

	lenpts10 = len(points) >> 10

	changed = 0
	while True:
		# group element for centroids are used as counters
		for cc in cluster_centers:
			cc.x = 0
			cc.y = 0
			cc.group = 0

		for p in points:
			cluster_centers[p.group].group += 1
			cluster_centers[p.group].x += p.x
			cluster_centers[p.group].y += p.y

		for cc in cluster_centers:
			cc.x /= cc.group
			cc.y /= cc.group

		# find closest centroid of each PointPtr
		changed = 0
		for p in points:
			min_i = nearest_cluster_center(p, cluster_centers)[0]
			if min_i != p.group:
				changed += 1
				p.group = min_i

		# stop when 99.9% of points are good
		if changed <= lenpts10:
			break

	for i, cc in enumerate(cluster_centers):
		cc.group = i

	return cluster_centers
