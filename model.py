import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
nltk.download('stopwords')
from pyresparser import ResumeParser
import re

augmented_dataset=pd.read_csv("resume.csv")

corpus=[]
def clean_function(resumeText):
    resumeText = re.sub('http\S+\s*', ' ', resumeText)  # remove URLs
    resumeText = re.sub('RT|cc', ' ', resumeText)  # remove RT and cc
    resumeText = re.sub('#\S+', '', resumeText)  # remove hashtags
    resumeText = re.sub('@\S+', '  ', resumeText)  # remove mentions
    resumeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', resumeText)  # remove punctuations
    resumeText = re.sub(r'[^\x00-\x7f]',r' ', resumeText)
    resumeText = re.sub('\s+', ' ', resumeText)  # remove extra whitespace
    resumeText=resumeText.lower()
    corpus.append(resumeText)
    return resumeText

augmented_dataset['skills'] = augmented_dataset['skills'].apply(lambda x: clean_function(x))

def role(skills):
    cv=CountVectorizer()
    x=cv.fit_transform(corpus).toarray()
    y=augmented_dataset.iloc[:,0].values

    # predicting one job role using classification:
    classifier = DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
    classifier.fit(x, y)
    # y_pred = classifier.predict(x)
    req=[skills.lower()]
    req=cv.transform(req)
    category=classifier.predict(req)

    # recommender system to match similar job roles:
    sim=cosine_similarity(x)

    def recommend(job):
        jid=augmented_dataset[augmented_dataset['roles']==job].index[0]
        dist=sim[jid]
        jlist=sorted(list(enumerate(dist)),reverse=True,key=lambda x:x[1])[1:13]
        jobset=set()
        for i in jlist:
            jobset.add(augmented_dataset.iloc[i[0]].roles)
        return jobset
    
    string=' '.join([str(elem) for elem in category])
    
    return recommend(string)
