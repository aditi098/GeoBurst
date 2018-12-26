
import pandas as pd
from nltk.tokenize import word_tokenize
import math
import csv
from datetime import datetime
import pyproj
from shapely.geometry import shape
from shapely.ops import transform
import json



def create_cluster():
    with open('Clusters', 'r') as target:
        cluster_dict = json.load(target)
    cluster= [x['Tweets'] for x in cluster_dict]
    return cluster


def calculate_area(clusters):
    areas = []
    for x in clusters:
        lat_min = data.iloc[x[0]]['Latitude']
        lat_max = data.iloc[x[0]]['Latitude']
        long_min = data.iloc[x[0]]['Longitude']
        long_max = data.iloc[x[0]]['Longitude']

        for y in x:
            latitude = data.iloc[y]['Latitude']
            longitude = data.iloc[y]['Longitude']
            if latitude > lat_max:
                lat_max = latitude
            elif latitude < lat_min:
                lat_min = latitude
            if longitude > long_max:
                long_max = longitude
            elif longitude < long_min:
                long_min = longitude
        # geom = {'type': 'Polygon',
        #         'coordinates': [[[lat_min, long_min], [lat_min, long_max], [lat_max,long_max], [lat_max, long_min]]]}

        geom = {'type': 'Polygon',
                    'coordinates': [[[long_min,lat_min ], [long_max,lat_min], [long_max, lat_max], [long_min,lat_max]]]}
        s = shape(geom)
        proj = partial(pyproj.transform, pyproj.Proj(init='epsg:4326'), pyproj.Proj(init='epsg:3857'))
        s_new = transform(proj, s)
        projected_area = s_new.area/1000000
        areas.append(projected_area)
        areas = [0 if math.isnan(x) else x for x in areas]
    return areas


def partial(func, *args, **keywords):
    def newfunc(*fargs, **fkeywords):
        newkeywords = keywords.copy()
        newkeywords.update(fkeywords)
        return func(*(args + fargs), **newkeywords)

    newfunc.func = func
    newfunc.args = args
    newfunc.keywords = keywords
    return newfunc

def calc_datetime():
    date_time = []
    for x in range(len(data)):
        date_time.append(datetime.combine(datetime.strptime(data.iloc[x]["Date"], '%Y-%m-%d'),
                                          datetime.strptime(data.iloc[x]["Time"], '%H:%M').time()))
    return date_time


def calc_params(cluster):
    tweet_number = []
    user_number = []
    time_dif = []
    for x in cluster:
        tweet_number.append(len(x))
        user_number.append(len(x))
        time_min = date_time[x[0]]
        time_max = date_time[x[0]]
        for y in x:
            if date_time[y] > time_max:
                time_max = date_time[y]
            if date_time[y] < time_min:
                time_min = date_time[y]
        time_dif.append(time_max - time_min)
    return tweet_number, user_number, time_dif

def common_words(cluster):

    cluster_words=[]
    for y in cluster:
        tweet=data.iloc[y]['Tweet']
        words=word_tokenize(tweet)
        for word in words:
            if not word in cluster_words:
                cluster_words.append(word)
    return cluster_words

def calc_scores(cluster):
    a1 = 0.5
    a2 = 0.5
    a3 = 0.5
    a4 = 0.5
    scores = []
    for x in range(len(cluster)):
        scores.append(a1 * tweet_numbers[x] + a2 * user_numbers[x] + a3 * time_difs[x].total_seconds() + a4 * area[x])
    return scores


def max(list):
    index=0
    max=list[0]
    for x in range(len(list)):
        if list[x]>max:
            max=list[x]
            index=x
    return index

def ranking(scores):
    cluster_info=[]
    for x in range(len(scores)):
        max_index=max(scores)
        scores[max_index]=0
        tweets= [dataset_original.iloc[x]["Tweet"] for x in cluster[max_index]]
        cluster_info.append({"ClusterId": max_index, "ClusterRank": x+1, "TweetIds": cluster[max_index], "Tweets": tweets})
    keys = cluster_info[0].keys()
    with open('Cluster_Ranking_Results.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(cluster_info)

dataset = pd.read_csv("processed_dataset.csv", sep="\t")
data = dataset.head(n=100)
dataset_original = pd.read_csv("processed_dataset.csv", sep="\t")
cluster= create_cluster()
# print(cluster)
area = calculate_area(cluster)
date_time = calc_datetime()
tweet_numbers, user_numbers, time_difs = calc_params(cluster)
# print(tweet_numbers)
# print(user_numbers)
# print(time_difs)
# print(area)
scores= calc_scores(cluster)
#print(scores)
ranking(scores)