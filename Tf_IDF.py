import pandas as pd
from nltk.tokenize import word_tokenize
import math
import json


def count_words(doc):
    count = 0
    words = word_tokenize(doc)
    for word in words:
        count += 1
    return count


# get docid and doc_length for each doc in tweets_set
def get_doc(tweets_set):
    doc_info = []
    i = -1
    for doc in tweets_set:
        i += 1
        count = count_words(doc)
        temp = {'doc_id': i, 'doc_length': count}
        doc_info.append(temp)
    return doc_info


# creates a frequency dictionary for each word in each document
def create_freq_dict(tweets_set):
    i = -1
    freqdictlist = []
    for doc in tweets_set:
        # print(doc)
        i += 1
        freqdict = {}
        words = word_tokenize(doc)
        for word in words:
            # word=word.lower()
            if word in freqdict:
                freqdict[word] += 1
            else:
                freqdict[word] = 1
        temp = {'doc_id': i, 'freqdict': freqdict}
        freqdictlist.append(temp)
    return freqdictlist


def computeTF(doc_info, freqdictlist):
    TF_scores = []
    for tempdict in freqdictlist:
        id = tempdict['doc_id']
        for k in tempdict['freqdict']:
            wt = tempdict['freqdict'][k]
            if wt > 0:
                twt = 1 + math.log(wt, 10)
            else:
                twt = 0
            temp = {'doc_id': id, 'TF_score': twt, 'key': k}  # check why id-1
            TF_scores.append(temp)
    return TF_scores


def computeIDF(doc_info, freqdictlist):
    IDF_scores = []
    counter = -1
    for dict in freqdictlist:
        counter += 1
        for k in dict['freqdict'].keys():
            count = sum([k in tempdict['freqdict'] for tempdict in freqdictlist])
            temp = {'doc_id': counter, 'IDF_score': math.log(len(doc_info) / float(count), 10), 'key': k}
            IDF_scores.append(temp)
    return IDF_scores

def computeTFIDF():
    TF_scores = computeTF(doc_info, freqdictlist)
    IDF_scores = computeIDF(doc_info, freqdictlist)

    TFIDF_scores = []
    for j in IDF_scores:
        for i in TF_scores:
            if j['key'] == i['key'] and j['doc_id'] == i['doc_id']:
                temp = {'doc_id': j['doc_id'], 'TFIDF_score': j['IDF_score'] * i['TF_score'], 'key': i['key']}
                TFIDF_scores.append(temp)
    return TFIDF_scores


dataset = pd.read_csv("processed_dataset.csv", sep="\t")
data = dataset
tweets_set = data.Tweet
doc_info = get_doc(tweets_set)
freqdictlist = create_freq_dict(tweets_set)
TFIDF_scores = computeTFIDF()
with open('TFIDF_Scores', 'w') as fout:
    json.dump(TFIDF_scores, fout)




