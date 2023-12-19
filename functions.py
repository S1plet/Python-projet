#Chatbot functions file, authors: LAM Pascal, LANG Felix

#import Modules
import os
from shutil import rmtree
from string import punctuation
import re
import math
import numpy

#Puts the file names with a specific extension in a list. Returns a list of file names with a specified extension from a specified directory.
def list_of_files(directory: str, extension: str):
    #Loops through the directory and appends to a list file names ending the specified extension 
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension): #Checks if the file name ends with the specified extension 
            files_names.append(filename)
    return files_names

#Extracts the names of presidents from the name of a file. Returns a list of names in alphabetical order from a list of files
def extractNames(listOfFiles: list):
    #Loops through the list of files and slices them to return only the names of the President
    for i in range(len(listOfFiles)):
        listOfFiles[i]= listOfFiles[i][11:len(listOfFiles[i])-4] #Removes the "Nomination" part
        if ord(listOfFiles[i][-1]) >= 48 and ord(listOfFiles[i][-1]) <= 57: 
            listOfFiles[i] = listOfFiles[i][:-1] #Removes the number at the end of certain files
    return sorted(list(set(listOfFiles)))

#Associates names from 2 lists. Returns a list of full names from a list of first names and a list of last names
def associateNames(listFirstName: list,listLastName: list):
    #Concatenates the list of Last Names to the list of First Names
    assert len(listFirstName) == len(listLastName), "The lists have to be the same size" #This raises an assertion error if the lists entered as parameter are not the same size
    listNames = []
    for i in range(len(listFirstName)):
        listNames.append(listFirstName[i] + " " + listLastName[i])
    return listNames

#Converts text files in lowercase to a "cleaned" directory from a directory entered as parameter. Returns None because we don't need need it to return anything
def convertFilesToLowercase(directory: str):
    #Creates a new "cleaned" folder to then create files in it where it copies the text but puts it in lowercase
    folder = os.curdir + "/cleaned"
    if os.path.exists(folder):
        rmtree(folder) #Deletes the "cleaned" directory if it already exists so that we can use this function continuously without having to manually delete the directory every time
    os.mkdir(folder)
    for filename in os.listdir(directory):
        f =  open(directory + "/" + filename, "r", encoding="utf-8")
        cleaned_f = open(folder + "/" + filename, "w", encoding="utf-8")
        for lines in f:
            cleaned_f.write(lines.casefold()) #Converts to lowercase and writes the lines of the file to another file in the "cleaned" directory

#Removes the punctuation of a string entered as parameter. Returns the string without punctuation
def _removePunctuationInText(text: str):
    #Loops through the string to check if any characters are punctuation characters and replaces them by a space
    for car in text:
        if car in list(punctuation):
            text = text.replace(car, " ") #Replaces the punctuation by a space
    return text

#Removes the punctuation of files from a "cleaned" directory entered as parameter. Returns None because we don't need need it to return anything
def removePunctFromFiles(cleaned_d: str):
    #Loops through the texts of each file in the "cleaned" directory to put them in lowercase using the previous function
    for file in os.listdir(cleaned_d):
        f = open(cleaned_d + "/"+ file, "r", encoding="utf-8")
        lines = f.readlines()
        f = open(cleaned_d + "/"+ file, "w", encoding="utf-8")
        for line in lines:
            line = _removePunctuationInText(line)
            f.write(re.sub(" +", " ",line)) #Replaces any double+ spaces by a single space

#Calculates the number of occurences of each word in the string entered as parameter. Returns a dictionnary where the keys are the words in the string and the values are the number of occurences in the string
def _wordOccurences(string: str):
    #Converts the string as a list to loop through the words and count the number of occurences
    l = string.split(" ")
    dico = {}
    for word in l:
        if word not in dico:
            dico[word] = 1
        else:
            dico[word] += 1
    return dico

#Calculates the TF-score of a single file entered as parameter by using the function above. Returns a dictionnary where the keys are the words in the file and the values are the TF-scores
def _TF_Score(file: str):
    #Uses the previous function on the text of a file
    text = ""
    for line in file:
        string = line[:-1]
        text += string
    return(_wordOccurences(text))

#Uses the previous function to return a list of dictionnaries containing the TF-scores of each word. Each dictionnary corresponds to a file in the "cleaned" directory
def list_tfScores(cleaned_d: str):
    #Appends the TF-Score of each word of each file to a list
    l = []
    for file in os.listdir(cleaned_d):
        f = open(cleaned_d + "/" + file, "r", encoding="utf-8")
        l.append(_TF_Score(f))
    return l

#Calculates the IDF-scores of every word in the corpus by using the list of TF-scores entered as parameter. Returns a dictionnary where the keys are the words in the corpus and the values are the IDF-scores
def IDF_score(listOfTFScores: list):
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
    del idf_dict[''] #Had to use this to delete an unknown character
    return idf_dict

#Calculates the TD-IDF Matrix of the corpus using the IDF dictionnaray and the TF list. Returns a 2D list where the rows are the files and the columns are the words.
def TF_IDF_Matrix(idf_dict: dict,list_tf: list):
    #Loops through the list of TF-Scores and the IDF-dictionnary to calculate the TF-IDF score. Assigns 0 to words that are present in the corpus but not in a file.
    mat = []
    for dict in list_tf:
        score_list = []
        for key in idf_dict.keys():
            if key not in dict.keys():
                score_list.append(0)
            else:
                score_list.append(round(idf_dict[key]*dict[key],2))
        mat.append(score_list)
    return mat

#Calculates the transpose of a matrix  
def transpose(matrix: list):
    result = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
    return result

#Removes punctuation, puts in lowercase a string entered as parameter and returns it as a list.
def _question_tokenization(question: str):
    #Removes punctuation, puts in lowercase and then converts as a list the question
    question = _removePunctuationInText(question,list(punctuation))
    question = re.sub(" +", " ", question) #Replaces double+ space by a single space
    question = question.casefold()
    l_question = question.split(" ")
    if l_question[len(l_question)-1] == "": #Had to use this to remove an unknown character
        l_question = l_question[:-1]
    return l_question

#Identifies the words in a list that are also present in the corpus. Returns a list of string
def _question_words_in_corpus(list_str: list, idf_dict: dict):
    #Loops through the words in the question and appends them to a list if it is also present in the IDF dictionnary 
    words_in_corpus = []
    for word in list_str:
        if word in idf_dict.keys():
            words_in_corpus.append(word)
    return words_in_corpus

#Calculates the TD-IDF vector for the question entered as parameter. Returns a list containing the TD-IDF scores
def TF_IDF_question(question: str):
    #Calculates first the TF-Score and then the TF-IDF Score of the question. Assigns 0 to words who are not present in the question
    global TfIdf_vector
    TfIdf_vector = []
    list_question = _question_tokenization(question)
    for word in idf_dict.keys():
        if word not in _question_words_in_corpus(list_question, idf_dict):
            TfIdf_vector.append(0)
        else:
            tfscore = 0
            for term in _question_words_in_corpus(list_question, idf_dict):
                if term == word:
                    tfscore += 1
            TfIdf_vector.append(round(tfscore*idf_dict[word],3))
    return TfIdf_vector
                
                
            

#Calculates the cosine similarity of 2 vectors. Returns a float corresponding to the similarity score
def _cosine_similarity(list1: list, list2: list):
    #Calculates the norm first then the similarity score
    normA = math.sqrt(sum(val**2 for val in list1))
    normB = math.sqrt(sum(val**2 for val in list2))
    similarity_score = (numpy.dot(list1, list2))/(normA*normB)
    return similarity_score   

#Finds the most relevant file to the question from a list of files. Returns a string corresponding to the name of that file 
def most_relevantDoc(tfidf_question, tfidf_corpus, listoffiles):
    #Loops through the rows in the corpus and calculates the cosine similarity of each word keeping only the highest one so that it can return the most relevant document
    max_similarity = 0
    max_index = 0
    for i in range(len(tfidf_corpus)):
        similarity = _cosine_similarity(tfidf_question, tfidf_corpus[i])
        if  similarity > max_similarity:
            max_similarity = similarity
            max_index = i
    file = listoffiles[max_index]
    return file

#Finds the word in the question who has the highest TF-IDF score in the corpus. Returns a string corresponding to that word
def _max_tfIdfScore():
    #Takes the word with the highest TF-IDF score in the question and returns it
    maxWordScore = max(TfIdf_vector)
    maxIndex = TfIdf_vector.index(maxWordScore)
    word = list(idf_dict.keys())[maxIndex]
    return word
  
  
#Generates a response depending on how the question is formulated using the file entered as parameter. Returns a string corresponding to the response 
def generate_reponse(question : str, file: str):
    #Checks first if the question starts by one of the question starters then reads the most relevant file to return the sentence where the first occurence of the word with the highest TF-IDF value.
    question_starters ={
        "Comment" : "Apres analyse,",
        "Pourquoi" : "Car,",
        "Peux-tu" : "Oui, bien sur!"
    }
    word = _max_tfIdfScore()
    f = open(os.curdir + "/cleaned/" + file, "r", encoding="utf-8")
    response = ""
    for key in question_starters.keys():
        if key in question:
            response += question_starters[key]
    for sentence in f.readlines():
        if word in sentence:
            response += f" {sentence}"
            return response   
    
    
            
    
    
#Displays the menu in the terminal
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
    print("[9]: Chatbot Mode")
    print("[10]: Exit")



























