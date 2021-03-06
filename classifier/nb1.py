#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 22:10:33 2017

@author: mattCohen
"""

############### UNUSED, but if desired could be substituted for SDG1 
from sklearn.naive_bayes import GaussianNB, MultinomialNB

import pandas as pd
import numpy as np
from pprint import pprint
from time import time
import logging
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

# #############################################################################
# Load some categories from the training set
categories = [
    'alt.atheism',
    'talk.religion.misc',
]
# Uncomment the following to do the analysis on all the categories
#categories = None

class DenseTransformer(TransformerMixin):

    def transform(self, X, y=None, **fit_params):
        return X.todense()

    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y, **fit_params)
        return self.transform(X)

    def fit(self, X, y=None, **fit_params):
        return self

# #############################################################################
# Define a pipeline combining a text feature extractor with a simple
# classifier
pipeline = Pipeline([
    ('vect', CountVectorizer()),
#    ('to_dense', DenseTransformer()), 
    ('tfidf', TfidfTransformer()),
#    ('clf', GaussianNB()),
    ('clf', MultinomialNB()),
])

parameters = {
#    'vect__max_df': (0.5, 0.75, 1.0),
#    'vect__ngram_range': ((1, 1), (1, 2)),  # unigrams or bigrams
#    'clf__alpha': (0.00001, 0.000001),
#    'clf__penalty': ('l2', 'elasticnet'),
}

if __name__ == "__main__":
    datadf = pd.read_csv('Classyfications.csv')
    datadf.body = datadf.body.apply(lambda x : unicode(x, errors='replace'))
    data_new = list(datadf.body)
    data_target = np.array(datadf.classification)
    

    grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=1)
    pprint(parameters)
    t0 = time()
    

    grid_search.fit(data_new, data_target)
    print("done in %0.3fs" % (time() - t0))
    print()

    print("Best score: %0.3f" % grid_search.best_score_)
    print("Best parameters set:")
    
    best_parameters = grid_search.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
        print("\t%s: %r" % (param_name, best_parameters[param_name]))
        
        
    grid_search.predict(["I\'m a dad", 'I\'m a daddy, looking for a little girl 18', 'When I\'m a dad i will use this'])
    