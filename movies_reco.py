# -*- coding: utf-8 -*-
"""Movies_Reco.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1CHRQE-0bRBMIViQPL9k7eNQ-v0cVQHfT
"""

import numpy as np
import pandas as pd

movies = pd.read_csv("/content/tmdb_5000_movies.csv")
credits = pd.read_csv("/content/tmdb_5000_credits.csv")

movies.head(2)

movies.shape

credits.head()

movies = movies.merge(credits,on='title')

movies.head()

# removing columns
#these are the following column we are going to keeping
#id
# keyword
# title
# overview
# Cast
# crew
# we are keeping only these columns

movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

movies.head()
# this is the main data we are going to working on

import ast

# Creating helper function whcih will help us to give the "name" in genres
def convert(text):
  L = []
  for i in ast.literal_eval(text):
    L.append(i['name'])
  return L

# droping 3 movies which has no overview section bcz 3 is less number so that is not important as much
movies.dropna(inplace = True)

movies['genres'] = movies['genres'].apply(convert)
movies.head()

movies['keywords'] = movies['keywords'].apply(convert)
movies.head()

import ast
ast.literal_eval('[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]')

def convert3(text):
  L = []
  counter = 0
  for i in ast.literal_eval(text):
    if counter < 3:
        L.append(i['name'])
        counter += 1
  return L

movies['cast'] = movies['cast'].apply(convert)
movies.head()

movies['cast'] = movies['cast'].apply(lambda x:x[0:3])

def fetch_director(text):
  L = []
  for i in ast.literal_eval(text):
    if i['job'] == 'Director':
        L.append(i['name'])
  return L

movies['crew'] = movies['crew'].apply(fetch_director)

# converting "overview function" to list so we can concatenate the whole lists
# usinig lamda function
#movies['overview'] = movies['overview'].apply(lambda x:x.split())
movies.sample(5)

def collapse(L):
    L1 = []
    for i in L:
        L1.append(i.replace(" ",""))
    return L1

movies['cast'] = movies['cast'].apply(collapse)
movies['crew'] = movies['crew'].apply(collapse)
movies['genres'] = movies['genres'].apply(collapse)
movies['keywords'] = movies['keywords'].apply(collapse)

movies.head()

movies['overview'] = movies['overview'].apply(lambda x:x.split())

movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x:[i.replace("","")for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace("","")for i in x])
movies['crew'] = movies['crew'].apply(lambda x:[i.replace("","")for i in x])

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

# Creating new data farame from movies
new_df = movies.drop(columns=['overview','genres','keywords','cast','crew'])

# formaating tags into strings
new_df['tags'] = new_df['tags'].apply(lambda x:" ".join(x))
new_df.head()

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000, stop_words = 'english')

vectors = cv.fit_transform(new_df['tags']).toarray()

vectors.shape

from sklearn.metrics.pairwise import cosine_similarity

similarity = cosine_similarity(vectors)

similarity

!pip install nltk

import nltk
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

def stem(text):
  y = []
  for i in text.split():
      y.append(ps.stem(i))
  return " ".join(y)

new_df['tags'][0]

# seeking first movie
vectors[0]

similarity

similarity[0]

# crating a function which will give you the recommendation of other five movies
#def recommend(movie):
 # movie_index = new_df[new_df['title'] == movie ].index[0]
  #distances = similarity[movie_index]
  #return

def recommend(movie):
    index = new_df[new_df['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    for i in distances[1:6]:
        print(new_df.iloc[i[0]].title)

recommend('The Lego Movie')

