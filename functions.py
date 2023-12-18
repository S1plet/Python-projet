import os
from shutil import rmtree
from string import punctuation
import re
import math
def list_of_files(directory, extension):
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names

def extractNames(listOfFiles):
    for i in range(len(listOfFiles)):
        listOfFiles[i]= listOfFiles[i][11:len(listOfFiles[i])-4]
        if ord(listOfFiles[i][-1]) >= 48 and ord(listOfFiles[i][-1]) <= 57:
            listOfFiles[i] = listOfFiles[i][:-1]
    return sorted(list(set(listOfFiles)))

def associateNames(listFirstName,listLastName):
    assert len(listFirstName) == len(listLastName), "The lists have to be the same size"
    listNames = []
    for i in range(len(listFirstName)):
        listNames.append(listFirstName[i] + " " + listLastName[i])
    return listNames

def convertFilesToLowercase(directory):
    folder = os.curdir + "/cleaned"
    if os.path.exists(folder):
        rmtree(folder)
    os.mkdir(folder)
    for filename in os.listdir(directory):
        f =  open(directory + "/" + filename, "r", encoding="utf-8")
        cleaned_f = open(folder + "/" + filename, "w", encoding="utf-8")
        for lines in f:
            cleaned_f.write(lines.casefold())

def _removePunctuationInText(text,li):
    for car in text:
        if car in li:
            text = text.replace(car, " ")
    return text

def removePunctFromFiles(cleaned_d):
    for file in os.listdir(cleaned_d):
        f = open(cleaned_d + "/"+ file, "r", encoding="utf-8")
        lines = f.readlines()
        f = open(cleaned_d + "/"+ file, "w", encoding="utf-8")
        for line in lines:
            line = _removePunctuationInText(line,list(punctuation))
            f.write(re.sub(" +", " ",line))

def _wordOccurences(string):
    l = string.split(" ")
    dico = {}
    for word in l:
        if word not in dico:
            dico[word] = 1
        else:
            dico[word] += 1
    return dico

def _TF_Score(file):
    text = ""
    for line in file:
        string = line[:-1]
        text += string
    return(_wordOccurences(text))

def list_tfScores(cleaned_d):
    global l 
    l = []
    for file in os.listdir(cleaned_d):
        f = open(cleaned_d + "/" + file, "r", encoding="utf-8")
        l.append(_TF_Score(f))
    return l

def IDF_score(listOfTFScores):
    global idf_dict
    idf_dict = {}
    for dico in listOfTFScores:
        for key in dico.keys():
            if key not in idf_dict:
                idf_dict[key] = dico[key]
            else:
                idf_dict[key] += dico[key]
    for key in idf_dict.keys():
        appearsInFile = 0
        for dico in listOfTFScores:
            if key in dico.keys():
                appearsInFile += 1
        idf_dict[key] = math.log10((8/appearsInFile))
    del idf_dict['']
    return idf_dict

def TF_IDF_Matrix(idf_dict,list_tf):
    mat = []
    for key in idf_dict.keys():
        score_list = []
        for dict in list_tf:
            if key not in dict.keys():
                score_list.append(0)
            else:
                score_list.append(round(idf_dict[key]*dict[key],2))
        mat.append(score_list)
    return mat 

#Calculate the TF-IDF Matrix for the question
def question_tokenization(question: str):
    question = _removePunctuationInText(question,list(punctuation))
    question = re.sub(" +", " ", question)
    question = question.casefold()
    l_question = question.split(" ")
    if l_question[len(l_question)-1] == "":
        l_question = l_question[:-1]
    return l_question

def question_words_in_corpus(list_words: list, idf_dict: dict):
    words_in_corpus = []
    for word in list_words:
        if word in idf_dict.keys():
            words_in_corpus.append(word)
    return words_in_corpus

def TF_IDF_question(question: str):
    TfIdf_score = []
    list_question = question_tokenization(question)
    for word in idf_dict.keys():
        if word not in question_words_in_corpus(list_question, idf_dict):
            TfIdf_score.append(0)
        else:
            tfscore = 0
            for term in question_words_in_corpus(list_question, idf_dict):
                if term == word:
                    tfscore += 1
            TfIdf_score.append(round(tfscore*idf_dict[word],3))
    return TfIdf_score
                
                
            

#Calculating similarity
def cosine_similarity():
    pass
    

def menu():
    print("Choose between the following options:")
    print("[1]: Extract names of the presidents from the names of the text files")
    print("[2]: Associate a first name with each president")
    print("[3]: Display the list of president's names")
    print("[4]: Convert files to lowercase into a 'cleaned' folder")
    print("[5]: Remove the punctuation in the files stored in the 'cleaned' folder")
    print("[6]: Display the TF-Score of each word for each file")
    print("[7]: Display the IDF-Score for each word")
    print("[8]: Display the TF-IDF Matrix")
    print("[9]: Exit")



























