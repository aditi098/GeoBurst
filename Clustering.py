from math import sin, cos, sqrt, atan2, pow, asin, log
from math import sqrt
import json
import pandas as pd



def geographical_similarity(long1, long2, lat1, lat2):
    dgr = 0.017453292519943295769236907684886
    R = 6372.795
    h = 300
    latitudeArc = (float(lat1) - float(lat2)) * dgr
    longitudeArc = (float(long1) - float(long2)) * dgr
    latitudeH = sin(latitudeArc * 0.5)
    latitudeH *= latitudeH
    lontitudeH = sin(longitudeArc * 0.5)
    lontitudeH *= lontitudeH
    tmp = cos(float(lat1) * dgr) * cos(float(lat2) * dgr)
    d = R * 2.0 * asin(sqrt(latitudeH + lontitudeH * tmp))
    if (d > h):
        return 0
    else:
        g = 1 - (pow(d, 2) / pow(h, 2))
    return g

def semantic_analysis(t1, t2):
    dict1 = []
    dict2 = []
    for x in TFIDF_scores:
        if x['doc_id'] == t1:
            dict1.append({'key': x['key'], 'TFIDF_score': x['TFIDF_score']})
    for y in TFIDF_scores:
        if y['doc_id'] == t2:
            dict2.append({'key': y['key'], 'TFIDF_score': y['TFIDF_score']})

    common = []
    for x in dict1:
        for y in dict2:
            if (x['key'] == y['key']):
                common.append({'key': x['key'], 'TFIDF_score': x['TFIDF_score'] * y['TFIDF_score']})
    normal1 = 0
    normal2 = 0

    for x in dict1:
        normal1 = normal1 + pow(x['TFIDF_score'], 2)

    for y in dict2:
        normal2 = normal2 + pow(y['TFIDF_score'], 2)

    normal1 = sqrt(normal1)
    normal2 = sqrt(normal2)
    sum = 0

    for x in common:
        sum = sum + x['TFIDF_score']
    return sum / float((normal1 * normal2))


def calculate_authority():
    count_tweets = len(data.index)
    auth = []
    for tweet_id in range(len(data)):
        authority = 0
        geo = []
        sem = []
        for x in range(count_tweets):
            g = geographical_similarity(data.iloc[tweet_id]["Longitude"], data.iloc[x]["Longitude"],
                                        data.iloc[tweet_id]["Latitude"], data.iloc[x]["Latitude"])
            geo.append(g)
            s = semantic_analysis(tweet_id, x)
            sem.append(s)
            if (g > 0.0 and s > delta):
                authority = authority + g * s
        auth.append(authority)
        geo_similarity.append(geo)
        sem_similarity.append(sem)
    print("auth done")
    return auth


def pivot(tweet_id):
    count_tweets = len(data.index)
    authority = 0
    auth = 0
    for x in range(count_tweets):
        # g = geographical_similarity(data.iloc[tweet_id]["Longitude"], data.iloc[x]["Longitude"],
        # data.iloc[tweet_id]["Latitude"], data.iloc[x]["Latitude"])
        # s = semantic_analysis(tweet_id, x)
        g = geo_similarity[x][tweet_id]
        s = sem_similarity[x][tweet_id]
        if (g > 0.0 and s > delta):
            auth = authority_list[x]
        if (auth > authority):
            authority = auth
            pivot = x
    return pivot


def ascent(tweet_id):
    pivot_cur = tweet_id
    while True:
        pivot2 = pivot(pivot_cur)
        if (pivot2 == pivot_cur):
            break;
        pivot_cur = pivot2
    return pivot_cur

def create_cluster():
    pivot_list=[]
    cluster_all=[[] for _ in range(len(data))]
    cluster=[]
    for x in range(len(data)):
        pivot_list.append(ascent(x))
    for x in range(len(pivot_list)):
        cluster_all[pivot_list[x]].append(x)
    for x in cluster_all:
        if len(x) > 1:
            cluster.append(x)
    return cluster

delta=0.4
with open('TFIDF_Scores', 'r') as target:
    TFIDF_scores = json.load(target)
dataset = pd.read_csv("processed_dataset.csv", sep="\t")
data = dataset
geo_similarity =[]
sem_similarity =[]
authority_list = calculate_authority()
authority_dict= [{"TweetID": i , "Authority": authority_list[i]} for i in range(len(authority_list))]
with open('Authority_Scores', 'w') as fout:
    json.dump(authority_dict, fout)
cluster = create_cluster()
#Assigning relevance scores
relscores=[8,1,0,6,0,0,0,0,0,3,0,6,0,0,0,4,7,8,0,3,3,0,3,3,0,0,0,0,0,7,0,0,0,8,3,10,0,0,0,10,10] 

cluster_dict= [{"ClusterID": i , "Tweets": cluster[i],"Relevance Score ":relscores[i]} for i in range(len(cluster))]

with open('Clusters', 'w') as fout:
    json.dump(cluster_dict, fout)



