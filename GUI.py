import json						
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

with open('Cluster_Ranking', 'r') as target:
	clusters_dic = json.load(target)

cluster_list = [x["TweetIds"] for x in clusters_dic]#a list of lists
ranks=[x["ClusterRank"] for x in clusters_dic]
cluster_tweets=[x["Tweets"] for x in clusters_dic]
relscores=[8,1,0,6,0,0,0,0,0,3,0,6,0,0,0,4,7,8,0,3,3,0,3,3,0,0,0,0,0,7,0,0,0,8,3,10,0,0,0,10,10] 

data = pd.read_csv('dataset_1000.csv',sep='\t')

#markers = ['o', '^', 's', 'd', 'x', '+', '<', '>']
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
markerCount = 0
colorCount = 0
clusterNo = 0
fig, ax = plt.subplots()
print ("The graph shows clusters of geo-tagged tweets alongwith their ranks")
for cluster in cluster_list:
	# print "Cluster: ", clusterNo
	number_tweets=len(cluster)
	pivot=cluster[0]
	#for point in cluster:
	x = data.at[pivot, 'Latitude']
	y = data.at[pivot, 'Longitude']
	marker = colors[colorCount] + 'o'
	plt.plot(x, y, marker, markersize=10*number_tweets,alpha=0.4)
	ax.annotate(ranks[clusterNo],(x,y))
		# print "Point: ", point, " x: ", x," y: ", "marker: ", marker
	colorCount = (colorCount + 1)%8
	# if colorCount == 8:
	# 	colorCount = 0
	#markerCount = (markerCount + 1)%8
	print ("Cluster Rank is ",ranks[clusterNo]," \n"," Tweets in the cluster are:" , "\n")
	for x in range(len(cluster_tweets[clusterNo])):
		print ("Tweet", x+1, " ",cluster_tweets[x])
	print ("\n")
	clusterNo += 1
	# print "####"
plt.xlabel('Latitude')
plt.ylabel('Longitude')
os.system('xdg-open Authority_Scores')
os.system('xdg-open processed_dataset.csv')
os.system('xdg-open TFIDF_Scores')
os.system('xdg-open Clusters')
os.system('xdg-open Cluster_Ranking')
plt.show()



