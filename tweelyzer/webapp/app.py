# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 00:00:11 2020

@author: Jatin Mishra
"""

from __future__ import division, print_function
# coding=utf-8
import re
import pickle

from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

# Keras
from tensorflow.keras.models import load_model
from keras.preprocessing import sequence

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from gevent.pywsgi import WSGIServer

import tweepy

# Define a flask app
app = Flask(__name__)


# Model saved with Keras model.save()
MODEL_PATH = 'tweet_sentiment_classifier.h5'

# Load your trained model
model = load_model(MODEL_PATH)

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
# test authentication
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

def tweet_text_cleaner(tweet):
    tweet = tweet.encode('utf-8').decode('unicode_escape')
    tweet = tweet.lower()
    tweet = BeautifulSoup(tweet, 'lxml').getText()
    tweet = re.sub(r'@[A-Za-z0-9]+', '', tweet)
    tweet = re.sub('http?://[A-Za-z0-9./]+', '', tweet)
    tweet = re.sub('https?://[A-Za-z0-9./]+','', tweet)
    tweet = re.sub('www?.[A-Za-z0-9./]+', '', tweet)
    tokens = word_tokenize(tweet)
    tweet = [word for word in tokens if not word in stop_words and word.isalpha()]
    return (" ".join(tweet))   

def get_tweet_and_make_pred(keyword):
    json_tweet = api.search(q=keyword, lang="en", count = 100)

    tweet = []
    for i in json_tweet:
        tweet.append(i.text)
        
    if len(tweet) > 0:
        with open('tokenizer.pickle', 'rb') as handle:
            loaded_tokenizer = pickle.load(handle)
            pred = model.predict_classes(sequence.pad_sequences(loaded_tokenizer.texts_to_sequences(tweet), maxlen=140))
            return pred
    else:
        return None

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    neutral_count = 0
    positive_count = 0
    negative_count = 0
    search_keyword = request.form['keyword'] 
    pred = get_tweet_and_make_pred(search_keyword)
    if pred is not None:
        for i in pred:
            if i == 0:
                negative_count += 1
            elif i == 1:
                neutral_count += 1
            else:
                positive_count += 1
        return "{},{},{}".format(negative_count, positive_count, neutral_count)
    else:
        return ""        
    

if __name__ == '__main__':
    app.run(debug=False, threaded=False)













