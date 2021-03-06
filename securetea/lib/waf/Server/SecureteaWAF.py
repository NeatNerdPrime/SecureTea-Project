# -*- coding: utf-8 -*-
u""" WAF ML Module .

Project:
    ╔═╗┌─┐┌─┐┬ ┬┬─┐┌─┐╔╦╗┌─┐┌─┐
    ╚═╗├┤ │  │ │├┬┘├┤  ║ ├┤ ├─┤
    ╚═╝└─┘└─┘└─┘┴└─└─┘ ╩ └─┘┴ ┴
    Author: Shaik Ajmal R <shaikajmal.r2000@gmail.com>
    Version:
    Module: SecureTea

"""

import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB,MultinomialNB
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline


class WAF:
    """

    """

    def __init__(self,live_data):
        """


        """


        self.live_data=[live_data]
        self.data=pd.read_csv("../data/data.csv",encoding="cp1252")
        self.target=self.data["label"]
        self.path_vectorizer=TfidfVectorizer(ngram_range=(1,3),encoding="cp1252")
        self.body_vectorizer=TfidfVectorizer(ngram_range=(1,3),encoding="cp1252")
        self.model=GaussianNB()

        # Feature selection

        self.X=self.data[['path','path_len','useragent_len','spaces', 'curly_open', 'curly_close', 'brackets_open','brackets_close', 'greater_than', 'lesser_than', 'single_quote','double_quote', 'directory', 'semi_colon', 'double_dash', 'amp']]

        self.X_train,self.X_test,self.Y_train,self.Y_test=train_test_split(self.X,self.target,test_size=0.2)


    def train_model(self):
        """


        """

        # Column Transformer

        self.column_transformer = ColumnTransformer([('tf-1', self.path_vectorizer, 'path')], remainder='passthrough', sparse_threshold=0)

        # Creating Pipeline

        self.pipe=Pipeline([

                  ('TF_IDF Vectorizer', self.column_transformer),
                  ('run_model', self.model)
                ])

        # Train Model
        print("Train completed")
        self.pipe.fit(self.X_train,self.Y_train)
        print("Train completed")


    def predict_model(self):

        with open("../data/model","rb") as f:
            self.model2=pickle.load(f)



        self.live_df= pd.DataFrame(self.live_data,
                          columns=['path', 'path_len', 'useragent_len', 'spaces', 'curly_open', 'curly_close',
                                   'brackets_open',
                                   'brackets_close', 'greater_than', 'lesser_than', 'single_quote',
                                   'double_quote', 'directory', 'semi_colon', 'double_dash', 'amp'])
        return self.model2.predict(self.live_df)





