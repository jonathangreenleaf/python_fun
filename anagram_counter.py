#!/usr/bin/env python
           
# take arbitrary word list (from file) or list
''' e.g., create 1MM wordlist
import random, string
file = open("wordlist.txt", "w")
for n in xrange(1000000):
    random_length = random.randint(1, 20)
    randword = ''.join([random.choice(string.ascii_letters) for n in xrange(random_length)])
    file.write(randword + '\n')
'''
word_file = "wordlist.txt"
words = open(word_file).read().splitlines()
words = words[0:1000000]
# test, just uncomment next line to assert = 5
#words = ['Act', 'cat', 'cat', 'dog', 'dog', 'aardvark']

# borrowing from this approach
#http://stackoverflow.com/questions/13692221/anagram-algorithm-in-java
#http://stackoverflow.com/questions/228730/how-do-i-iterate-through-the-alphabet-in-python
from collections import defaultdict


# given a sting, count the occurances of each character in a dict
def letterOccurrances(string):
    frequencies = defaultdict(lambda: 0)
    for character in string:
        frequencies[character.lower()] += 1
    return frequencies


# main counter
# given a batch of words, loop thru counting letter occurances
# sort the results, and store in dict - count the anagrams
def anagram_counter(words):

    # initialize
    anagram_count=0
    charseqs = dict()
    
    # this is O(n)
    # loop thru, comparing to see if anagram    
    for i, word in enumerate(words):
        
        # is letter Occurance pattern in the list already?
        char_cnts = sorted(letterOccurrances(words[i]).items())
        lookup = tuple(char_cnts)
        
        #dictionary key lookup O(1) - yay!
        #https://wiki.python.org/moin/DictionaryKeys
        
        try:
            #will throw exception if lookup not there, otherwise incr
            charseqs[lookup] = charseqs[lookup] + 1
            if charseqs[lookup] == 2:
                anagram_count+=2
            else:
                anagram_count+=1
        except KeyError:
            charseqs[lookup] = 1      
            
    return anagram_count


# create batches, call anagram_counter() on each
# maps raw word list into buckets of equal length words
# ie where anagram is possible within the bucket
# borrows from
# http://stackoverflow.com/questions/4895157/counting-the-word-length-in-a-file
occurrence = dict()
d = defaultdict(list)

# this is O(n)
for word in words:    
    if len(word) > 0:
        try:
            #will throw exception if word length not there, otherwise incr
            occurrence[len(word)] = occurrence[len(word)] + 1
            d[len(word)].append(word)
        except KeyError:
            occurrence[len(word)] = 1
            d[len(word)].append(word)

# word array like [(3, ['Act', 'cat', ..]), (8, ['aardvark'])]
word_array = d.items()

#start at smallest word length
word_length = min(d.keys())
word_list = []
anagram_total = 0

# this is O(n)
# where key is length and value is list of words of that length
for k,v in word_array:

    words_todo = len(v)
    word_list = []
    
    for word in v:
        
        if len(v) > 1:
            word_list.append(word)
            words_todo -= 1
            continue

    if len(v) > 1 & words_todo == 0:
        
        # parallel processing option
        result = anagram_counter(word_list)
        print 'processed ' + str(len(word_list)) + ' words '
        print ' of length = ' + str(len(word)) + \
              ' - found ' + str(result) + ' anagrams'
        anagram_total += result

print 'total anagrams found:' + str(anagram_total)


'''
# just for comparison (comment out lines 64-116)
# shorter 1 bucket approach (slower on large word lists)

anagram_total = 0
result = anagram_counter(words)

print 'processed ' + str(len(words)) + ' words ' +\
      ' - found ' + str(result) + ' anagrams'

anagram_total += result

print 'total anagrams found:' + str(anagram_total)
'''


'''
Summary:
The algorthim involves 3 simple loops O(3n) simplifying to O(n)
Word length clearly effects performance but not on order
of word count at scale.  Additionally, batching has some
practical advantages over the competing O(n) approach with
1 bucket.  At a certain scale however, batching anagram lookups
will see performance degrade on the same order of magnitude.
Batching affords a longer runway though and tees up parallel-
processing as an option.

T1 x buckets (with lines 63-115)
T2 1 bucket  (with 118-131 instead)
cnt(K) T1(s)  T2(s)
100    1.6    1.6
200    3.1    3.2
300    4.8    4.7
400    6.3    6.7
500    8.2    8.2
600    9.7    10.5
700    11.5   12.2
800    13.3   15.2
900    15.2   16.9
1000   17.4   19.7
2000   40.0   53.1
'''