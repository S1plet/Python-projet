#Chatbot features file, author: LAM Pascal, LANG Felix

from functions import*
cleaned_d = os.curdir + "/cleaned"
assert os.path.exists(cleaned_d), "You must first have a 'cleaned directory' before choosing this option"
tfScores = list_tfScores(cleaned_d)
idfScores = IDF_score(tfScores)
tfidf_matrix =  TF_IDF_Matrix(idfScores,tfScores)
tfidf_transpose = transpose(tfidf_matrix)
j = 0
unimportant_words = []
for i in range(len(tfidf_transpose)):
    if tfidf_transpose[i] == [0]*len(tfidf_transpose[i]):
        unimportant_words.append(list(idfScores.keys())[i])
print("The unimpotant words are :", unimportant_words)

highest_words = []
maxScore = 0
maxIndex = 0
for i in range(len(tfidf_matrix)):
    if max(tfidf_matrix[i]) > maxScore:
        maxScore = max(tfidf_matrix[i])
        maxIndex = tfidf_matrix[i].index(maxScore)
        highest_words = [list(idfScores.keys())[maxIndex]] 
    elif max(tfidf_matrix[i]) == maxScore:
        maxIndex = tfidf_matrix[i].index(maxScore) 
        highest_words.append(list(idfScores.keys())[maxIndex])
print("The highest TF-IDF words are :", highest_words)



    
        
        

        


        



