import csv
import matplotlib.pyplot as plt
import numpy
import sys
import time

#find closest word to input string1 using input dictionary
def find_closest_word(string1, dictionary):
    closest_word = ""
    min_distance = float("inf")
    
    #iterate through words in dictionary and calculate distance w/ string1
    for string2 in dictionary:
        distance = levenshtein_distance(string1, string2, 1, 1, 1)
        
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
            d[0, j] = i*insertion_cost
    
    #iterate through each letter in string1 and string2
    for j in range(1, len(string2)):
        for i in range(1, len(string1)):
            #if they are the same character, do not add any more cost and just save previous cost
            if string1[i] == string2[j]:
                d[i, j] = d[i-1, j-1]
            #if they are not the same, use method that is least costly
            else:
                d[i, j] = min(d[i-1, j] + deletion_cost, d[i, j-1] + insertion_cost, d[i-1, j-1] + substitution_cost)
                
            
    return d[len(string1)-1, len(string2)-1]
    
    
def qwerty_levenshtein_distance(string1, string2, deletion_cost, insertion_cost):
    d = dict()
    
    #HARDCODE MANHATTAN DISTANCE???
    
    for i in range(len(string1)):
            d[i, 0] = i*deletion_cost
    
    for j in range(len(string2)):
            d[0, j] = i*insertion_cost
    
    #iterate through each letter in string1 and string2
    for j in range(1, len(string2)):
        for i in range(1, len(string1)):
            #if they are the same character, do not add any more cost and just save previous cost
            if string1[i] == string2[j]:
                d[i, j] = d[i-1, j-1]
            #if they are not the same, save which method is least costly- use sub multidimensional array to get sub cost
            else:
                d[i, j] = min(d[i-1, j] + deletion_cost, d[i, j-1] + insertion_cost, d[i-1, j-1] + substitution_cost(string1[i], string2[j]))
                
            
    return d[len(string1)-1, len(string2)-1]
    
            
#measure the error of algorithm by calculating success rate
def measure_error(typos, truewords, dictionarywords):
    counter = 0.0
    total = len(typos)
    start = time.time()
    
    #iterate through typo words and find replacement word using lev algorithm
    for i in range(total):
        replacement = find_closest_word(typos[i], dictionarywords)
        
        #if the algo was correct, increment counter
        if replacement == truewords[i]:
            print typos[i]
            print replacement
            print truewords[i]
            counter+= 1

    #find success rate 
    rate = counter/total
    #print time it took to run this computation
    print "it took this long to measure error: " + str((time.time() - start))
    return rate

def main():
    #read two files from command line
    typo_file = open(sys.argv[1], "r")
    dict_file = open(sys.argv[2], "r")
    
    #look for indicator flag to see if it needs to measure error 
    if len(sys.argv) > 3:
        indicator = sys.argv[3]
    
    #initiate output file 
    corrected_file = open('corrected.txt', 'w')
    
    #initiate arrays for typo words, true words, and dictionary words
    typo_words = []
    true_words = []
    dict_words = []

    
    body = typo_file.readlines()
    dict_body = dict_file.readlines()

    #populate true words and typo words from inputted file
    for line in body:
        pair = line.split()  
        typo_words.append(pair[0]) 
        true_words.append(pair[1])

    #populate dictionary words from inputted file
    for line in dict_body:
        for w in line.split():
            dict_words.append(w)
    
    #measure error if indicated in command line 
    if len(sys.argv) > 3:
        if indicator == "1":
            measure_error(typo_words, true_words, dict_words)         
    #if nothing is indicated, run standard program that outputs a corrected file
    else:
        for w in typo_words:
            print "hi"
            replacement = find_closest_word(w, dict_words)
            replacement = str(replacement)
            corrected_file.write(replacement+'\n')
            corrected_file.flush()

    
    corrected_file.close()
    dict_file.close()
    typo_file.close()


if __name__ == "__main__":
    main()
    

            