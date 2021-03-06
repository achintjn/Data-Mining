# -*- coding: utf-8 -*-
"""Copy of Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16kuHODLZVDTLMO5Ml1kJFyLG_U5yYS6X
"""

import nltk
import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel
import matplotlib.pyplot as plt
from wordcloud import WordCloud,STOPWORDS
from mpl_toolkits.axes_grid1.inset_locator import mark_inset, inset_axes
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

from sklearn import datasets
from sklearn.feature_selection import chi2
from sklearn.feature_selection import SelectKBest

from nltk.tokenize import word_tokenize, wordpunct_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

stopwords = nltk.corpus.stopwords.words('english')
lemmatizer = WordNetLemmatizer()
stemmer = nltk.stem.porter.PorterStemmer()

"""Reading the data"""

#Reading the train and test data file to convert them in to data frame.
train_data = pd.read_table('train_new.txt',header=None,skiprows=0,names=['sentiment','review'])
test_data = pd.read_table('test_new.txt',header=None,skiprows=0,names=['review'])

# drop missing text labels in train to reduce noise
train_data = train_data.dropna()
test_data = test_data.dropna()

#remove small words
train_data['review'] = train_data['review'].apply(lambda x: ' '.join([word for word in x.split() if (len(word)>3)]))

#Printing some data to check how does it look
print("train data size: ",train_data.shape)
print("test data size: ",test_data.shape)

print(train_data['review'].iloc[1])
print(train_data.sentiment.value_counts())

"""Preprocessing the data"""

train_data_processed = []
#removing stopping words doing stemming on train data.
for i in range(0, len(train_data)):
    train_data['review'].iloc[i] = train_data['review'].iloc[i].replace("<br />"," ")
    review = re.sub('[^a-zA-Z]', ' ', train_data['review'].iloc[i])
    review = review.lower()
    review = review.split()
    review = [lemmatizer.lemmatize(word) for word in set(review) if not word in set(stopwords)]
    review = ' '.join(review)
    train_data_processed.append(review)
test_data_processed = []
#removing stopping words doing lemmatization on test data.
for i in range(0, len(test_data)):
    test_data['review'].iloc[i] = test_data['review'].iloc[i].replace("<br />"," ")
    review = re.sub('[^a-zA-Z]', ' ', test_data['review'].iloc[i])
    review = review.lower()
    review = review.split()
    review = [lemmatizer.lemmatize(word) for word in set(review) if not word in set(stopwords)]
    review = ' '.join(review)
    test_data_processed.append(review)

#checking the length and some sample data
type(train_data_processed)
print(len(train_data_processed))
print(len(test_data_processed))
print(train_data_processed[2])
print(train_data['sentiment'][2])
print(train_data_processed[:2])

"""Vectorizing - TFIDF"""

#tf idf and creating unigram, bigram and 3 gram for better precision #assignment
tf_idf = TfidfVectorizer(ngram_range=(1, 3))
#applying tf idf to training data
X_train_tf = tf_idf.fit_transform(train_data_processed)
#applying tf idf to training data
X_test_tf = tf_idf.transform(test_data_processed)

#printing features/attributes
tf_idf.get_feature_names_out()
print(X_train_tf.shape)

"""Plotting most used words"""

plt.figure(figsize = (20,20)) 
wc = WordCloud(max_words = 2000 , width = 1600 , height = 800).generate(" ".join(train_data[train_data.sentiment == 1].review))
plt.imshow(wc , interpolation = 'bilinear')

# #print(X_train_tf[0])
# print("n_samples: %d, n_features: %d" % X_train_tf.shape)

# X_train, X_test, y_train, y_test = train_test_split(X_train_tf,train_data['sentiment'],random_state=1, test_size= 0.2)
# #df = pd.DataFrame(X_train_tf.T.toarray(), index=feature_names, columns=corpus_index)
# #print(df)
# print(X_train.shape)
# print(X_test.shape)
# print(y_train.shape)
# print(y_test.shape)

"""Feature selection using Chi square."""

#assignment
ch2a = SelectKBest(chi2,k = 40000)
X_train_y_assn = ch2a.fit_transform(X_train_tf, train_data['sentiment'])
X_test_y_assn = ch2a.transform(X_test_tf)

"""Cosin similarity"""

cosine_sim = cosine_similarity(X_test_y_assn, X_train_y_assn)

def kNN_manual(k, X_test, X_train, y_train):

    """
    implementation of k nearest neighbor algorithm using cosine similarity
        
    k: an integer paramter for nearest neighbours (usually odd)
    
    X_test: sparse matrix for testing or to make predictions
    
    X_train: sparse matrix to train the model
    
    test_file: must be shape (int,)
    contains the preprocessed text for the kNN method to classify
    
    train_label: must be shape (int,)
    contains the labels from the training set
    """

    test_label = list()
    count = 1
    #looping over all the test file to get cos similarity on each document
    print(X_test.shape[0])
    for i in cosine_sim:
        #cosin similarity
        
        #sorting on arguments and extracting k nearest neighbours
        indices = np.argsort(-i)[:k]
        indices
        #count += 1
        #print(count)

        #getting those neighbours(labels) from training set
        nearest_neigh = []
        for j in indices:
            #print(y_train.iloc[j])
            nearest_neigh.append(y_train.iloc[j])

        #adding the labels of all the neighbours
        sum_labels = sum(nearest_neigh)

        #print(sum_labels)

        #classifying based on which label was most among that set
        if sum_labels > 0:
          test_label.append('+1')
        else:
          test_label.append('-1')
        test_label
        
    return test_label

to_submit = kNN_manual(475, X_test_y_assn, X_train_y_assn, train_data['sentiment'])

"""Creating a .txt file about the test data output"""

print(to_submit)
#to_submit = list(map(int, to_submit))
np.savetxt(r'format.txt', to_submit, fmt='%s')

"""If we want to check the accuracy of our train data splitting in test data. Optional"""

to_submit = list(map(int, to_submit))
print('Accuracy Score: ',i,' - ',metrics.accuracy_score(y_test,to_submit)*100,'%',sep='')

"""This loop I used to calculate the best K value to get the highest accuracy and plot some diagram."""

accuracies = []

for i in range(1,300):
    to_submit = kNN_manual(i, X_test, X_train, y_test, y_train)
    to_submit = list(map(int, to_submit))
    accuracies.append(metrics.accuracy_score(y_test,to_submit)*100)

# Plot the results 

fig, ax = plt.subplots(figsize=(8,6))
ax.plot(range(1,100), accuracies)
ax.set_xlabel('# of Nearest Neighbors (k)')
ax.set_ylabel('Accuracy (%)');