from flask import Flask, render_template, flash, redirect, url_for, request
from wtforms import Form, StringField, validators
from csv import reader
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from math import log10, sqrt
from collections import OrderedDict
import string
from nltk.corpus import stopwords
import random
import time
def remove(s): 
    return "".join(s.split()) 


all_shingles = []
stop_words = set(stopwords.words('english'))

#K is 3
def get_all_shingles():
    f = open('bible_data_set.csv', 'r')

    k = reader(f)

    l = 0
    
    
    for i in k:
        l = l+1
        #terms_list = list(map(lambda x: PorterStemmer().stem(x), word_tokenize(i[4] + i[1])))
        real_terms_list = word_tokenize(i[4])
        
        filtered_list = [] 
        for w in real_terms_list: 
            w = w.lower()
            if w not in stop_words and w not in string.punctuation and w not in ["-"]: 
                filtered_list.append(w) 
        sentence = "".join(filtered_list)
        
        for j in range(0, len(sentence)-3):
            shingle = sentence[j:j+3]
            if shingle not in all_shingles:
                all_shingles.append(shingle)
        
        
        if(l == 10000):
            break
            
        

    f.close()
    
shingle_doc_matrix = []
def create_matrix():
    f = open('bible_data_set.csv', 'r')
    
    k =list( reader(f) )
    for j in all_shingles:
        shingle_doc_matrix.append([])
    
    l=0
    pre_store = []
    
    for s in range(0, 10000):
        doc = k[s][4]
        real_terms_list = word_tokenize(doc)
        filtered_list = []
        for w in real_terms_list:
            w = w.lower()
            if w not in stop_words and w not in string.punctuation and w not in ["-"]: 
                filtered_list.append(w) 
        sentence = "".join(filtered_list)
        shingle_list_doc = set()
        for t in range(0, len(sentence) - 3):
            shingle = sentence[t:t+3]
            shingle_list_doc.add(shingle)
            
        pre_store.append(shingle_list_doc)
        
    for j in all_shingles:
        new_shingle = all_shingles[l]
        doc_size = 0
        for i in range(0,10000):
            set_doc = pre_store[i]
            if(new_shingle not in set_doc):
                shingle_doc_matrix[l].append(1)
            else:
                shingle_doc_matrix[l].append( 0)
        
        l = l+1
        
        
final_matrix = []
num_hash_values = 10
#We have taken 10 Hash Functions
def create_k_signature():
    hash_functions = []
    for i in range(0, num_hash_values):
        a = random.randint(1, 6623)
        b = random.randint(1, 6623)
        hash_functions.append([a,b])
    
    for j in range(0, num_hash_values):
        final_matrix.append([])
        for i in range(0, 10000):
            final_matrix[j].append(99999)
            
    
    for i in range(0, 6624):
        
        for j in range(0, 10000):
#            print(i, j);
            if shingle_doc_matrix[i][j] == 1:
                vals = []
                for k in range(0, num_hash_values):
                    vals.append((hash_functions[k][0]*i+hash_functions[k][1])%(6624) )
                for k in range(0, num_hash_values):
                    if (final_matrix[k][j] > vals[k]):
                        final_matrix[k][j] = vals[k]
                    
                    
        

if __name__ ==  '__main__':
    curr_time = time.time()
    get_all_shingles()
    all_shingles.sort()
    print("All shingles collected and sorted")
    print("Time taken: " + str(time.time() - curr_time) + " secs")
    curr_time = time.time()
    create_matrix()
    print("Big matrix created")
    print("Time taken: " + str(time.time() - curr_time) + " secs")
    curr_time = time.time()
    create_k_signature()
    print("signature matrix created" + " for " + str(num_hash_values) + " hash functions")
    print("Time taken: " + str(time.time() - curr_time) + " secs")
    #print(final_matrix)
    
    

