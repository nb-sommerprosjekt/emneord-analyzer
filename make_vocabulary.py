import os
import string
from nltk.corpus import stopwords
import sys

vocab = {}
for root, dirs, files in os.walk("/disk1/bokhylla"):
        print("Lengden av files er:" +str(len(files)))
        for file in files:
                if file.endswith(".txt"):
                        file_path = os.path.join(root, file)
                        f = open(file_path,"r")
                        text = f.read()
                        words = text.split()
                        table = str.maketrans('','', string.punctuation)
                        words_stripped = [w.translate(table) for w in words]
                        words_stripped = [word.lower() for word in set(words_stripped)]
                        words = [word for word in words_stripped if word.isalpha()]
                        words_stripped = [w for w in words_stripped if w not in set(stopwords.words('norwegian'))]
                        words_stripped = [w for w in words_stripped if not w.isdigit()]
                        for word in words_stripped:
                            if word in vocab:
                                vocab[word] +=1
                            else:
                                vocab[word] =1
                                print("added new word: " + word + " to vocabulary")

with open("vocab.txt", "w") as f:
    for key in sorted(vocab.keys()):
        f.write(key + " " + str(vocab[key])+ "\n")
