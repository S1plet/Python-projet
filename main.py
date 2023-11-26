from functions import *

directory = str(input("Enter the directory in which the files are located. (The directory specified should look like this: C:/Users/PC/Documents/Chatbot/speeches)"))
exit = False
while exit == False:
    menu()
    choice = int(input())
    if choice == 1:
        files_names = list_of_files(directory, "txt")
        print(extractNames(files_names))
    elif choice == 2:
        files_names = extractNames(list_of_files(directory, "txt"))
        listFirstNames = ["Jacques", "Valerie", "Francois", "Emmanuel", "Francois", "Nicolas"]
        print(associateNames(listFirstNames,files_names))
    elif choice == 3:
        files_names = extractNames(list_of_files(directory, "txt"))
        listFirstNames = ["Jacques", "Valerie", "Francois", "Emmanuel", "Francois", "Nicolas"]
        list_names = associateNames(listFirstNames,files_names)
        for name in list_names:
            print(name)
    elif choice == 4:
        convertFilesToLowercase(directory)
    elif choice == 5:
        cleaned_d = os.curdir + "/cleaned"
        assert os.path.exists(cleaned_d), "You must first have a 'cleaned directory' before choosing this option"
        removePunctFromFiles(cleaned_d)
    elif choice == 6:
        cleaned_d = os.curdir + "/cleaned"
        assert os.path.exists(cleaned_d), "You must first have a 'cleaned directory' before choosing this option"
        tfScores = list_tfScores(cleaned_d)
        for dict in tfScores:
            print(dict, "\n")
    elif choice == 7:
        cleaned_d = os.curdir + "/cleaned"
        assert os.path.exists(cleaned_d), "You must first have a 'cleaned directory' before choosing this option"
        tfScores = list_tfScores(cleaned_d)
        print(IDF_score(tfScores))
    elif choice == 8:
        cleaned_d = os.curdir + "/cleaned"
        assert os.path.exists(cleaned_d), "You must first have a 'cleaned directory' before choosing this option"
        tfScores = list_tfScores(cleaned_d)
        idfScores = IDF_score(tfScores)
        print(TF_IDF_Matrix(idfScores,tfScores))
    elif choice == 9:
        exit = True
    else:
        print("This option does not exist !")