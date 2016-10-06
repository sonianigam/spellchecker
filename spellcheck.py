import matplotlib.pyplot as plt
import itertools
import numpy
import sys
import time
import re

#find closest word to input string1 using input dictionary
def find_closest_word(string1, dictionary, param1=1, param2=1, param3=1):
    closest_word = ""
    min_distance = float("inf")
    
    #iterate through words in dictionary and calculate distance w/ string1
    for string2 in dictionary:
        distance = levenshtein_distance(string1, string2, param1, param2, param3)
        
        #if the distance is smaller, save as closest word
        if distance < min_distance:
            min_distance = distance
            closest_word = string2
    return closest_word
    
#find closest word to input string1 and input dictionary, uses qwerty lev algo
def qwerty_find_closest_word(string1, dictionary, param1=1, param2=1):
    closest_word = ""
    min_distance = float("inf")
    
    #iterate through words in dictionary and calculate distance w/ string1
    for string2 in dictionary:
        distance = qwerty_levenshtein_distance(string1, string2, param1, param2)
        
        #if the distance is smaller, save as closest word
        if distance < min_distance:
            min_distance = distance
            closest_word = string2
            
    return closest_word


#calculate levenshtein distance between string1 and string2 using inputted deletion, insertion, and substitution costs
def levenshtein_distance(string1, string2, deletion_cost, insertion_cost, substitution_cost):
    d = dict()
    
    #initializing "multidimensional array" (in dict form)
    for i in range(len(string1)):
            d[i, 0] = i*deletion_cost
    
    for j in range(len(string2)):
            d[0, j] = j*insertion_cost
    
    #iterate through each letter in string1 and string2
    for j in range(1, len(string2)):
        for i in range(1, len(string1)):
            #if they are the same character, do not add any more cost and just save previous cost
            if string1[i].lower() == string2[j].lower():
                d[i, j] = d[i-1, j-1]
            #if they are not the same, use method that is least costly
            else:
                d[i, j] = min(d[i-1, j] + deletion_cost, d[i, j-1] + insertion_cost, d[i-1, j-1] + substitution_cost)
    return d[len(string1)-1, len(string2)-1]
    
    
#calculates lev distance where sub value is found using manhattan distance func
def qwerty_levenshtein_distance(string1, string2, deletion_cost, insertion_cost):
    d = dict()

    for i in range(len(string1)):
            d[i, 0] = i*deletion_cost
    
    for j in range(len(string2)):
            d[0, j] = i*insertion_cost
    
    #iterate through each letter in string1 and string2
    for j in range(1, len(string2)):
        for i in range(1, len(string1)):

            #if they are the same character, do not add any more cost and just save previous cost
            if string1[i].lower() == string2[j].lower():
                d[i, j] = d[i-1, j-1]
            #if they are not the same, save which method is least costly- use sub multidimensional array to get sub cost
            else:
                d[i, j] = min(d[i-1, j] + deletion_cost, d[i, j-1] + insertion_cost, d[i-1, j-1] + manhattan_distance(string1[i], string2[j]))
    return d[len(string1)-1, len(string2)-1]
    
    
#calculate manhattan distance between two coordinates in (x, y) form
def manhattan_distance(c1, c2):
    #maps keyboard to coordinate system
    coordinates = {
        "a": (1, 2), "b": (5, 1), "c": (3, 1), "d": (3, 2), "e": (3, 3), "f": (4, 2), "g": (5, 2), "h": (6, 2), "i": (8, 3), "j": (7, 2), "k": (8, 2), "l": (9, 2), "m": (7, 1), 
        "n": (6, 1), "o": (9, 3), "p": (10, 3), "q": (1, 3), "r": (4, 3), "s": (2, 3), "t": (5, 3), "u": (7, 3), "v": (4, 1), "w": (2, 3), "x": (2, 1), "y": (6, 3),
        "z": (1, 1), "1": (1, 4), "2": (2, 4), "3": (3, 4), "4": (4, 4), "5": (5, 4), "6": (6, 4), "7": (7, 4), "8": (8, 4),  "9": (9, 4), "0": (10, 4)
    }
    
    #returns 0 if no alphanumeric characters
    if (c1.isalnum() and c2.isalnum()) == False:
        return 0
    #calculates difference between two coordinate points
    else:
        coordinate_one = coordinates[c1.lower()]
        coordinate_two = coordinates[c2.lower()]
        
        x_dist = abs(coordinate_one[0] - coordinate_two[0])
        y_dist = abs(coordinate_one[1] - coordinate_two[1])
        
        distance = x_dist + y_dist
        return distance
    
            
#measure the error of algorithm by calculating success rate
def measure_error(typos, truewords, dictionarywords):
    counter = 0.0
    total = len(typos)
    start = time.time()
    
    #iterate through typo words and find replacement word using lev algorithm
    for i in range(total):
        replacement = find_closest_word(typos[i].lower(), dictionarywords)
        #if the algo was correct, increment counter
        if replacement != truewords[i]:
            counter+= 1

    #find success rate 
    rate = counter/total
    #print time it took to run this computation
    print "it took this long to measure error: " + str((time.time() - start))
    print "error rate is: " + str(rate)
    return rate
    
#measure the error of algorithm by calculating success rate using qwerty lev algo
def qwerty_measure_error(typos, truewords, dictionarywords, param1=1, param2=1):
    counter = 0.0
    total = len(typos)
    start = time.time()
    
    #iterate through typo words and find replacement word using lev algorithm
    for i in range(total):
        replacement = qwerty_find_closest_word(typos[i].lower(), dictionarywords, param1, param2)
        #if the algo was correct, increment counter
        if replacement != truewords[i]:
            counter+= 1

    #find success rate 
    rate = counter/total
    #print time it took to run this computation
    print "it took this long to measure error: " + str((time.time() - start))
    print "error rate is: " + str(rate)
    return rate
    
#measure the error of algorithm by calculating success rate
def experiment_measure_error(typos, truewords, dictionarywords, param1, param2, param3):
    counter = 0.0
    total = len(typos)
    start = time.time()
    
    #iterate through typo words and find replacement word using lev algorithm
    for i in range(total):
        replacement = find_closest_word(typos[i].lower(), dictionarywords, param1, param2, param3)
        #if the algo was correct, increment counter
        if replacement != truewords[i]:
            counter+= 1

    #find success rate 
    rate = counter/total
    #print time it took to run this computation
    print "it took this long to measure error: " + str((time.time() - start))
    print "error rate is: " + str(rate)
    return rate

#measure the error of algorithm by calculating success rate
def qwerty_experiment_measure_error(typos, truewords, dictionarywords, param1, param2):
    counter = 0.0
    total = len(typos)
    start = time.time()
    
    #iterate through typo words and find replacement word using lev algorithm
    for i in range(total):
        replacement = qwerty_find_closest_word(typos[i].lower(), dictionarywords, param1, param2)
        #if the algo was correct, increment counter
        if replacement != truewords[i]:
            counter+= 1

    #find success rate 
    rate = counter/total
    #print time it took to run this computation
    print "it took this long to measure error: " + str((time.time() - start))
    print "error rate is: " + str(rate)
    return rate

def main():
    #read two files from command line
    typo_file = open(sys.argv[1], "r")
    dict_file = open(sys.argv[2], "r")
    
    #look for indicator flag to see if it needs to measure error 
    if len(sys.argv) > 3:
        indicator = sys.argv[3]
    
    #initialize output file 
    corrected_file = open('corrected.txt', 'w')
    
    #initialize array for dictionary words
    dict_words = []
    body = typo_file.readlines()
    dict_body = dict_file.readlines()
    
    #populate dictionary words from inputted file
    for line in dict_body:
        for w in line.split():
            dict_words.append(w)
    
    #measure error if indicated in command line 
    if len(sys.argv) > 3:
        #run standard measure error
        if indicator == "1":
            #initialize arrays for typo words, true words
            typo_words = []
            true_words = []
            
            #populate true words and typo words from inputted file
            for line in body:
                pair = line.split()  
                typo_words.append(pair[0]) 
                true_words.append(pair[1])
                 
            measure_error(typo_words, true_words, dict_words) 
        
        #run qwerty measure error
        if indicator == "2":
            #initialize arrays for typo words, true words
            typo_words = []
            true_words = []
            
            #populate true words and typo words from inputted file
            for line in body:
                pair = line.split()  
                typo_words.append(pair[0]) 
                true_words.append(pair[1])
                 
            qwerty_measure_error(typo_words, true_words, dict_words) 
        
        #run experiment using standard measure error
        if indicator == "3":
            typo_words = []
            true_words = []
            parameters = [1, 2, 3, 4]
            x_values = []
            y_values = []
            counter = 1
            
            #maintain param with the lowest error
            best_error = float("inf")
            best_param = []
            
            #aggregate sample set of data
            for x in range(35):
                pair = body[x].split()  
                typo_words.append(pair[0]) 
                true_words.append(pair[1])
            
            #create list of all parameter combos
            combos = itertools.product(parameters, repeat=3)
            
            #iterate through each paramter type
            for param in combos:
                param1 = param[0]
                param2 = param[1]
                param3 = param[2]
                
                #get rate, aggregate trial number and error rate  as x, y values
                rate = experiment_measure_error(typo_words, true_words, dict_words, param1, param2, param3) 
                x_values.append(rate)
                y_values.append(counter)
                
                print param
                print x_values
                print y_values
                print counter
                
                #increment trial 
                counter += 1
                
                #save param with lowest error
                if rate < best_error:
                    best_error = rate
                    best_param = param
                
            #plot graph with trial number and error rates   
            plt.plot(y_values, x_values, "ro")
            plt.ylabel('error rate')
            plt.xlabel('trial number')
            plt.axis([0, 64, 0, 1])
            print "saving plot image"
            plt.savefig('plot.png')
                
            print "best param is: " + str(best_param)
            print "with the error: " + str(best_error)
        #run experiment using qwerty measure error
        if indicator == "4":
            
            typo_words = []
            true_words = []
            parameters = [1, 2, 3, 4]
            x_values = []
            y_values = []
            counter = 1
            best_error = float("inf")
            best_param = []
            
            #aggregate sample data
            for x in range(35):
                pair = body[x].split()  
                typo_words.append(pair[0]) 
                true_words.append(pair[1])
            
            #get all combinations of the paramters
            combos = itertools.product(parameters, repeat=2)
            
            #iterate through the parameters
            for param in combos:
                param1 = param[0]
                param2 = param[1]
                
                #get rate, aggregate trial number and error rate  as x, y values
                rate = qwerty_experiment_measure_error(typo_words, true_words, dict_words, param1, param2) 
                x_values.append(rate)
                y_values.append(counter)
                
                print param
                print x_values
                print y_values
                print counter
                
                #increment trial number
                counter += 1
                
                #save param with lowest error rate
                if rate < best_error:
                    best_error = rate
                    best_param = param
                
            #graph trial number against error rates
            plt.plot(y_values, x_values, "ro")
            plt.ylabel('error rate')
            plt.xlabel('trial number')
            plt.axis([0, 64, 0, 1])
            print "saving plot image"
            plt.savefig('plot.png')
                
            print "best param is: " + str(best_param)
            print "with the error: " + str(best_error)
                    

                 
    #if nothing is indicated, run standard program that outputs a corrected file
    else:
        for x in body:
            #split each line into words using all but alphanum as delimiters
                body_list = re.split('(\W)', x)
                for word in body_list:
                    if word.isalnum() == False:
                        #write symbol to file
                        corrected_file.write(word)
                        corrected_file.flush()
                    else:
                        #find closest word 
                        replacement = find_closest_word(word, dict_words)
                        replacement = str(replacement)
                        #write corrected word to file
                        corrected_file.write(replacement)
                        #refresh file
                        corrected_file.flush()

    #close all files
    corrected_file.close()
    dict_file.close()
    typo_file.close()


if __name__ == "__main__":
    main()
    

            