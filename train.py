import os
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

train_path = '/home/andrew/dev/emneord_classification/data/train.csv'

data_raw = pd.read_csv(train_path)
#print(data_raw.shape)
print("Number of rows in data = ", data_raw.shape[0])
print("Number of columns in data = ", data_raw.shape[1])

print("Missing values:")
missing_values_check = data_raw.isnull().sum()
print(missing_values_check)

categories = list(data_raw.columns.values)
categories = categories[2:]
print('')
print('Categories:')
print(categories)
print(' ')
counts = []
for category in categories:
	counts.append((category, data_raw[category].sum()))

df_stats = pd.DataFrame(counts,  columns = ['category', 'number of comments'])
print(df_stats)

sns.set(font_scale = 2)
plt.figure(figsize=(15,8))

ax = sns.barplot(categories, data_raw.iloc[:, 2:].sum().values)
plt.title("Comments in each category", fontsize = 24)
plt.ylabel("Number of comments", fontsize = 18)
plt.xlabel("Comment type", fontsize = 18)

#Adding the text labels
rects = ax.patches
labels = data_raw.iloc[:,2:].sum().values

for rect, label in zip(rects,labels):
	height = rect.get_height()
	ax.text(rect.get_x() + rect.get_width()/2, height + 5, label, ha = 'center', va = 'bottom', fontsize = 18)
plt.show()

rowSums = data_raw.iloc[:, 2:].sum(axis = 1)
multiLabel_counts = rowSums.value_counts()
multiLabel_counts = multiLabel_counts.iloc[1:]

sns.set(font_scale = 2)
plt.figure(figsize= (15,8))

ax = sns.barplot(multiLabel_counts.index, multiLabel_counts.values)

plt.title("Comments having multiple labels ")
plt.ylabel('number of comments', fontsize = 18)
plt.xlabel('Number of labels', fontsize =18)

#Adding the textlabels
rects = ax.patches
labels = multiLabel_counts.values
for rect, label in zip(rects, labels):
	height = rect.get_height()
	ax.text(rect.get_x() + rect.get_width()/2, height + 5, label, ha = 'center', va = 'bottom')
plt.show()


### DATA PREPROCESSING

data = data_raw
data = data_raw.loc[np.random.choice(data_raw.index, size = 2000)]
print(data.shape)


import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import re
import sys
import warnings

if not sys.warnoptions:
	warnings.simplefilter("ignore")

def cleanHtml(sentence):
	cleanr = re.compile('<.*?>')
	cleantext = re.sub(cleanr, ' ', str(sentence))
	return cleantext

def cleanPunc(sentence):
	cleaned = re.sub(r'[?|!|\'|"|#]',r'',sentence)
	cleaned = re.sub(r'[.|,|)|(|\|/]',r' ',cleaned)
	cleaned = cleaned.strip()
	cleaned = cleaned.replace("\n"," ")
	return cleaned
def keepAlpha(sentence):
    alpha_sent = ""
    for word in sentence.split():
        alpha_word = re.sub('[^a-z A-Z]+', ' ', word)
        alpha_sent += alpha_word
        alpha_sent += " "
    alpha_sent = alpha_sent.strip()
    return alpha_sent

data['comment_text'] = data['comment_text'].str.lower()
data['comment_text'] = data['comment_text'].apply(cleanHtml)
data['comment_text'] = data['comment_text'].apply(cleanPunc)
data['comment_text'] = data['comment_text'].apply(keepAlpha)



stop_words = set(stopwords.words('english'))
stop_words.update(['zero','one','two','three','four','five','six','seven','eight','nine','ten','may','also','across','among','beside','however','yet','within'])
re_stop_words = re.compile(r"\b(" + "|".join(stop_words) + ")\\W", re.I)
def removeStopWords(sentence):
    global re_stop_words
    return re_stop_words.sub(" ", sentence)

data['comment_text'] = data['comment_text'].apply(removeStopWords)
print(data.head)




stemmer = SnowballStemmer("english")
def stemming(sentence):
    stemSentence = ""
    for word in sentence.split():
        stem = stemmer.stem(word)
        stemSentence += stem
        stemSentence += " "
    stemSentence = stemSentence.strip()
    return stemSentence

data['comment_text'] = data['comment_text'].apply(stemming)
print(data.head())

from sklearn.model_selection import train_test_split

train, test = train_test_split(data, random_state=42, test_size=0.30, shuffle=True)

print(train.shape)
print(test.shape)

train_text = train['comment_text']
test_text = test['comment_text']



from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(strip_accents='unicode', analyzer='word', ngram_range=(1,3), norm='l2')
vectorizer.fit(train_text)
vectorizer.fit(test_text)

x_train = vectorizer.transform(train_text)
y_train = train.drop(labels = ['id','comment_text'], axis=1)

x_test = vectorizer.transform(test_text)
y_test = test.drop(labels = ['id','comment_text'], axis=1)

from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.multiclass import OneVsRestClassifier

LogReg_pipeline = Pipeline([
                ('clf', OneVsRestClassifier(LogisticRegression(solver='sag'), n_jobs=-1)),
            ])

for category in categories:
    print('**Processing {} comments...**'.format(category))
    
    # Training logistic regression model on train data
    LogReg_pipeline.fit(x_train, train[category])
    
    # calculating test accuracy
    prediction = LogReg_pipeline.predict(x_test)
    print('Test accuracy is {}'.format(accuracy_score(test[category], prediction)))
    print("\n")



# using binary relevance
from skmultilearn.problem_transform import BinaryRelevance
from sklearn.naive_bayes import GaussianNB

# initialize binary relevance multi-label classifier
# with a gaussian naive bayes base classifier
classifier = BinaryRelevance(GaussianNB())

# train
classifier.fit(x_train, y_train)

# predict
predictions = classifier.predict(x_test)

# accuracy
print("Multiple binary classifications")
print("Accuracy = ",accuracy_score(y_test,predictions))
print("\n")

from skmultilearn.problem_transform import ClassifierChain
from sklearn.linear_model import LogisticRegression

# initialize classifier chains multi-label classifier
classifier = ClassifierChain(LogisticRegression())

# Training logistic regression model on train data
classifier.fit(x_train, y_train)

# predict
predictions = classifier.predict(x_test)

# accuracy
print("Classifier Chains")
print("Accuracy = ",accuracy_score(y_test,predictions))
print("\n")


# using Label Powerset
from skmultilearn.problem_transform import LabelPowerset
# initialize label powerset multi-label classifier
classifier = LabelPowerset(LogisticRegression())

# train
classifier.fit(x_train, y_train)

# predict
predictions = classifier.predict(x_test)

# accuracy
print("Label powerset")
print("Accuracy = ",accuracy_score(y_test,predictions))
print("\n")


from skmultilearn.adapt import MLkNN
from scipy.sparse import csr_matrix, lil_matrix

classifier_new = MLkNN(k=10)

# Note that this classifier can throw up errors when handling sparse matrices.

x_train = lil_matrix(x_train).toarray()
y_train = lil_matrix(y_train).toarray()
x_test = lil_matrix(x_test).toarray()

# train
classifier_new.fit(x_train, y_train)

# predict
predictions_new = classifier_new.predict(x_test)

# accuracy
print("Adapted algorithm")
print("Accuracy = ",accuracy_score(y_test,predictions_new))
print("\n")

