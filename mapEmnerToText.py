import os
from collections import Counter

def traverseBokDir(dirPath):
    print("Henter inn stier til bøker")
    filePaths = []
    filenames = []
    baseNames = []
    txt_dict = {}
    for root, dirs, files in os.walk(dirPath):
            for file in files:
                if file.endswith(".txt"):
                    file_path = os.path.join(root, file)
                    #print(file_path)
                    #print(file)
                    filePaths.append(file_path)
                    filenames.append(file)
                    baseName = file.replace(".txt", "")
                    baseNames.append(file.replace(".txt",""))
                    txt_dict[baseName] =  {"path":file_path,"filename": file}
    return txt_dict

def getAllEmner(path):
    print("Henter emner fra filer")
    file_paths = []
    antall_emner = 0
    totalt_antall = 0
    emne_ordliste_liste = []
    emneord = []
    for root, dirs, files in os.walk("/disk1/bokhylla/emneUttrekk"):
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
                                                line = line.replace("TOPIC:", "")
                                                line = line.replace("\n", "")
                                                emne_ordliste_liste.append(line.split(","))
    emneordliste_og_path = zip(file_paths, emne_ordliste_liste)
    return list(emneordliste_og_path)
def getListOfEmnerAndFrequency(emnerOgPathList, minFreq = 0):
    print("Lager liste over emner og frekvenser")   
    emner = []
    for element in emnerOgPathList:
        for emne in element[1]:
           if len(emne)>1:
               emner.append(emne.lower())
    count = Counter(emner)
    emner, freq = count.keys(), count.values()
    emnerOgFreq = list(zip(emner,freq))
    emnerOgFreq.sort(key=lambda tup: tup[1], reverse = True)
    emnerOgFreq = [x for x in emnerOgFreq if x[1] >= minFreq]

    return emnerOgFreq

def makeEmneDict(listOfEmneFilePaths):
    print("lager emnedictionary")
    file_paths = listOfEmneFilePaths
    file_paths = [x.strip() for x in file_paths]
    fileNames = []
    baseNames = []
    emne_dict = {}
    for f in file_paths:
       path,filename = os.path.split(f)
      # fileNames.append(filename)
       baseName = os.path.basename(filename).replace(".emner","")
      # baseNames.append((os.path.basename(filename).replace(".emner","")))
       emne_dict[baseName] = {"path": path, "filename" : filename} 
    #print(baseNames)
    return emne_dict


#def parseEmneListe(path):
#    f = open(path, 'r')
#    emner_raw = f.readlines()
#    emner_clean = []
#    for line in emner_raw:
#        emne = ' '.join(line.split()[:-1])
#        emne = emne.lower()
#        if len(emne)>1:
#            emner_clean.append(emne)
#    return emner_clean 

def filterEmner(emner_og_fil_liste, emnerOfChoice, numEmnerPerFile):
    print("filtrerer emner")
    newEmneOgFilListe = []
    for f in emner_og_fil_liste:
       tempEmner = []
       for emne in f[1]:
           if emne.lower() in emnerOfChoice:
               tempEmner.append(emne.strip())
       newEmneOgFilListe.append([f[0],tempEmner])
    
    newEmneOgFilListe = [x for x in newEmneOgFilListe if len(x[1])>=numEmnerPerFile]
    return newEmneOgFilListe
    

if __name__ == '__main__':
    bokDir = "/disk1/bokhylla"
    bokEmnerDir = "/disk1/bokhylla/emneUttrekk"
#    topp_emnefil = "/disk1/emneord_analyse/min5over40frekvens.txt"
#    liste_over_top_emner = "/disk1/emneord_analyse/emnerMedOver40iFrekvens_sortert.txt"

    # Lager dictionary over alle paths til alle bøker, dict[basename] = {filepath :" ", filename : "" }
    txtDict = traverseBokDir(bokDir)
   
#    # Lager dictionary over alle paths til alle emnefiler, dict[basename] = {filepath :" ", filename : "" }
#    emneDict = parseListeOverEmneFiler(topp_emnefil)
   
    # Henter inn alle emnerordene og filnavn. Liste[0] = [filnavn,[emner]]
    emnerOgFilpaths = getAllEmner(bokEmnerDir)
    
    # Lager liste over alle emneFiler
    emneFilePaths = [x[0] for x in emnerOgFilpaths]

  # Lager dictionary over alle paths til alle emnefiler, dict[basename] = {filepath :" ", filename : "" }
    emneDict = makeEmneDict(emneFilePaths)
    
    # Finner ut frekvens av hvert emne, og gir ut en sortert liste av tupler med [emne, frekvens]. 
    emnerOgFrekvens = getListOfEmnerAndFrequency(emnerOgFilpaths,40)
    
    # Henter ut liste over alle emner på topplisten. Sortert med frekvens.
    liste_over_top_emner = [x[0].lower() for x in emnerOgFrekvens]   
    #print(liste_over_top_emner)
    

    # Lager ny liste over Emneordfiler + emneord der kun emneord som er med i 40 eller flere docs blir beholdt.
    # Alle dokumenter med mindre enn 5 emner blir også fjernet
    # output: list[0] = [emnefilpath, [emne1, emne2,emne3]]
    newEmnerOgFilPath = filterEmner(emnerOgFilpaths,liste_over_top_emner, 5)
    
    print("lengde av txtpaths: "+str(len(txtDict.keys())))
    print("lengde av emnepaths: "+str(len(emneDict.keys())))

   # new_topList = getListOfEmnerAndFrequency(emnerOgFilpaths,40)
   # print(len(new_topList))
    print(len(liste_over_top_emner))
    print("Antall filer opprinnelig: "+ str(len(emnerOgFilpaths)))
   # print(emnerOgFilpath[0])
    print("Antall filer med 5 eller flere popular emner: " + str(len(newEmnerOgFilPath)))
   # print(newEmnerOgFilPath)    
 
