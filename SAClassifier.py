from gensim.models import Word2Vec
import string

from nltk.corpus import movie_reviews as mr
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.classify import NaiveBayesClassifier as nbc
from nltk.tag.stanford import StanfordPOSTagger
from nltk.stem.wordnet import WordNetLemmatizer as lemma

import nltk
import random

""" MODELLING NLTK MOVIE REVIEWS - NB, CBOW, NO STOPWORDS """
# REMOVE STOPWORDS, PUNCTUATION AND CREATE TUPLES (WORDS,CLASS)
stop = stopwords.words('english')
documents = [([w for w in mr.words(i) if w.lower() not in stop and w.lower() not in string.punctuation], i.split('/')[0]) for i in mr.fileids()]
#potato = lemma().lemmatize([i for i,j in documents])

random.shuffle(documents)

# DEFINE WORDS AS KEYS AND OCCURENCES AS VALUES
#word_features = FreqDist(chain(*[i for i,j in documents])) #from itertools import chain
word_features = FreqDist([x for y,z in documents for x in y])
word_features = list(word_features.keys())#[:1000]

# TERM-DOC MATRIX, SAMPLING TRAIN AND TEST SETS AT 80-20
numtrain = int(len(documents) * 80 / 100)
train_set = [({i:(i in tokens) for i in word_features}, tag) for tokens,tag in documents[:numtrain]]
test_set = [({i:(i in tokens) for i in word_features}, tag) for tokens,tag in documents[numtrain:]]

# RUN CLASSIFIER AND RETURN PERFORMANCE MEASURES
classifier = nbc.train(train_set)
print (nltk.classify.accuracy(classifier, test_set)*100)
classifier.show_most_informative_features(5)

""" MODELLING NLTK MOVIE REVIEWS - NB, WORD2VEC """
w2v = Word2Vec(mr.sents())
w2v.most_similar("damon", topn=5)

