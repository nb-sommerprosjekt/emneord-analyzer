import os
import numpy as np
from collections import Counter

#import matplotlib.pyplot as plt

treshold = 1


file_paths = []
antall_emner = 0
totalt_antall = 0
emne_ordliste_liste = []
emneord = []
for root, dirs, files in os.walk("/disk1/bokhylla/emneUttrekk"):
	print("Lengden av files er:" +str(len(files)))
file_paths = []
antall_emner = 0
totalt_antall = 0
emne_ordliste_liste = []
emneord = []
for root, dirs, files in os.walk("/disk1/bokhylla/emneUttrekk"):
        print("Lengden av files er:" +str(len(files)))
        for file in files:
                if file.endswith(".emner"):
                        file_path = os.path.join(root, file)
                        f = open(file_path,"r")
                        text = f.readlines()
                        file_paths.append(file_path)
                        totalt_antall +=1
                        for line in text:
                                        if "TOPIC" in line:
                                                antall_emner +=1
                                                print(str(antall_emner)+ "/" +str(totalt_antall))
                                                line = line.replace("TOPIC:", "")
                                                line = line.replace("\n", "")
                                                emne_ordliste_liste.append(line.split(","))
#	for file in files:
#		if file.endswith(".emner"):
#			file_path = os.path.join(root, file)
#			f = open(file_path,"r")
#			text = f.readlines()
#			file_paths.append(file_path)
#			totalt_antall +=1
#			for line in text:
#					if "TOPIC" in line:
#						antall_emner +=1
#						print(str(antall_emner)+ "/" +str(totalt_antall))
#						line = line.replace("TOPIC:", "")
#						line = line.replace("\n", "")
#						emne_ordliste_liste.append(line.split(","))
emneordliste_og_path = zip(file_paths, emne_ordliste_liste)
emne_lengder = []
words = []
for emner in emne_ordliste_liste:
	emne_lengder.append(len(emner))
	for word in emner:
		word = word.strip()
		word = word.lower()
		words.append(word)


avg_emner = np.average(emne_lengder)
median_emner = np.median(emne_lengder)
freddy_file = open("emne_ordliste.txt", "w")
for word in words:
	freddy_file.write(word +"\n")
print("Antall oppforinger totalt: "+ str(len(emne_lengder)))
print("Gjennomsnittlig antall ganger emneord per doc: " + str(avg_emner))
print("Median antall ganger emneord per doc: " + str(median_emner))
enere = 0
word_freqs = {}
for word in words:
    if word in word_freqs:
        word_freqs[word] += 1
    else:
        word_freqs[word] = 1

k, v = [], []
for key, value in word_freqs.items():
    k.append(key)
    v.append(value)  
vokab_count =zip(k,v)
avg_vokab = np.average(v)
median_vokab = np.median(v)
print("Antall unike emneord:" + str(len(v)))
print("Gjennomsnittlig antall ganger hvert emneord har blitt brukt: " + str(avg_vokab))
print("Median antall ganger hvert emneord har blitt brukt: " + str(median_vokab))
enere = 0
for value in v :
	if value ==1:
		enere +=1
print("Antall emneord som bare blir brukt en gang:" + str(enere))
tuple_emne = [k, v]


biggerthanone = [x for x in list(vokab_count) if x[1]>=40]
with open("emnerMedOver40iFrekvens.txt", "w") as f:
    for i in biggerthanone:
        f.write(i[0]+" " + str(i[1]) +"\n")
#print(biggerthanone)
#print(biggerthanone)
top_emner = []
for emne_tupel in biggerthanone:
	top_emner.append(emne_tupel[0])
print(top_emner)
#result = [x for x in emneordliste_og_path if x in top_emner]
result =[]
for element in emneordliste_og_path:
	counter = 0
	for emne in top_emner:
		if emne in element[1]:
			
			counter +=1
			if counter ==5:
				result.append(element[0])
				break
print(len(result))
with open("min5over40frekvens.txt","w") as f:
    for i in result:
        f.write(i+"\n")    
#plt.subplot(2, 1, 1)
#binwidth =1
#n, bins, patches = plt.hist(emne_lengder, bins=range(min(emne_lengder), max(emne_lengder) + binwidth, binwidth))
#plt.axvline(avg_emner, color='k', linestyle='dashed', linewidth=1, label = "Gjennomsnitt")
#plt.axvline(median_emner, color='k', linestyle='-', linewidth=1, label = "median")
#plt.title("Antall emneord som brukes i hvert dokument")
#plt.xlabel("antall emneord")
#plt.ylabel("frekvens")
#plt.legend()




# plt.subplot(2, 1, 2)
# x = v
# binwidth =2
# n, bins, patches = plt.hist(v, bins=range(min(v), max(v) + binwidth, binwidth))
# plt.title("Frekvens av bruk for hvert emneord")
# plt.xlabel("Frekvens")
# plt.ylabel("Antall emneord")


# plt.subplot(2, 1, 2)
# x = v
# binwidth =2
# n, bins, patches = plt.hist(biggerthanone, bins=range(min(biggerthanone), max(biggerthanone) + binwidth, binwidth))
# plt.title("Frekvens av bruk for hvert emneord")
# plt.xlabel("Frekvens")
# plt.ylabel("Antall emneord")



#plt.show()

