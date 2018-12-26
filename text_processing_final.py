import pandas as pd
import re
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer

#Input Dataset

data = pd.read_csv("dataset_pro.csv", sep="\t")

#Remove duplicates from the dataset

data.sort_values("Tweet", inplace = True)
data.drop_duplicates(subset ="Tweet",
                     keep = False, inplace = True)
data.sort_index(inplace = True)

#Remove tweets with less than 2 words

temp = []

for index, row in data.iterrows():
	if len(str(row['Tweet']).split()) <= 2:
	 	continue
	temp.append(row.tolist())

data = pd.DataFrame(temp,columns=['UserName','Date', 'Time', 'Longitude', 'Latitude', 'Tweet'])

#Text Processing

sw = stopwords.words('english')
all_sw = set (sw + list(string.punctuation))

tokenizer = TweetTokenizer()
ps = PorterStemmer()

updated_tweets = []
tweets = list(data["Tweet"])

for tweet in tweets:
	tweet = re.sub(r'[^\x00-\x7F]+',' ', tweet)
	tweet = tweet.lower().strip()
	tweet = re.sub('[\']', ' ', tweet)
	tweet = tokenizer.tokenize(tweet)
	processed_tweet = [t for t in tweet if t not in all_sw]
	processed_tweet = [ps.stem(word) for word in processed_tweet]
	processed_tweet = ' '.join(processed_tweet)
	processed_tweet = re.sub('[.:()]', '', processed_tweet)
	updated_tweets.append(processed_tweet)

new_tweet_df = pd.DataFrame({"Tweet": updated_tweets})

data.update(new_tweet_df)

#Output processed dataset

data.to_csv('processed_dataset.csv', sep='\t')
