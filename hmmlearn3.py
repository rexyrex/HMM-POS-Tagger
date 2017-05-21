import pickle
import sys
import math


        
def initializeWordsAndTags(nWordsGivenTag,totalWordsInTag):
    for t in tags:
        nWordsGivenTag[t] = dict()
        totalWordsInTag[t] = float(0)
        
def initializeTagInfo(outgoingTags,tagDict):  
    for tag in tags:
        tagDict[tag] = dict()
        outgoingTags[tag] = 0
    outgoingTags['Q0'] = 0
    tagDict['Q0']=dict()
    
def updateTagCounts(splitWords,outgoingTags,tagDict):
    tag_line = []
    for term in splitWords:
        tag_line.append(term.split('/')[-1])
    for i in range(1, len(tag_line)):
        tagDict[tag_line[i - 1]][tag_line[i]] = tagDict[tag_line[i - 1]].get(tag_line[i], 0) + 1
        outgoingTags[tag_line[i - 1]] += 1
        
def updateEmsCount(splitWords,nWordsGivenTag,totalWordsInTag):
    for wAndT in splitWords: #wAndT = word and Tag combo
        word = '/'.join(wAndT.split('/')[:-1])
        tag = wAndT.split('/')[-1]
        nWordsGivenTag[tag][word] = nWordsGivenTag[tag].get(word, 0) + 1
        totalWordsInTag[tag] += 1
        
def getTransProb(tags, lines):
    outgoingTags = dict()
    tagDict = dict()
    initializeTagInfo(outgoingTags,tagDict)
    for line in lines:
        splitWords = line.split(' ')
        updateTagCounts(splitWords,outgoingTags, tagDict)
    transProb = dict()
    tags.add('Q0')
    for t1 in tags:
        for t2 in tags:
            if transProb.get(t2) is None:
                transProb[t2] = dict()
            transProb[t2][t1] = math.log((float(tagDict[t1].get(t2, 0) + 1)) / float(outgoingTags[t1] + len(tags)))
    tags.discard('Q0')
    return transProb

def getEmsProb(tags, lines):
    nWordsGivenTag = dict() 
    totalWordsInTag = dict()
    initializeWordsAndTags(nWordsGivenTag,totalWordsInTag)

    for line in lines:
        splitWords = line.split(' ')[1:]
        updateEmsCount(splitWords,nWordsGivenTag,totalWordsInTag)
    emsProb = dict()
    for tag in tags:
        for c in nWordsGivenTag[tag]:
            if emsProb.get(tag) is None:
                emsProb[tag] = dict()
            emsProb[tag][c] = math.log(float(nWordsGivenTag[tag][c]) / float(totalWordsInTag[tag]))
    return emsProb

processed_lines = []
words = set()
tags = set()

fileReader = open(sys.argv[1], 'r', encoding="utf-8")
lines = fileReader.readlines()
for line in lines:
    line = '/Q0 ' + line.strip()
    processed_lines.append(line)
fileReader.close()


for line in processed_lines:
    terms = line.split(' ')[1:]
    for term in terms:  
        words.add(term.split('/')[0])     
        tags.add(term.split('/')[-1])

emsProb = getEmsProb(tags, processed_lines)
transProb = getTransProb(tags, processed_lines)

fileWriter=  open('hmmmodel.txt', 'wb')
pickle.dump([words, tags, emsProb, transProb], fileWriter)
fileWriter.close()
        
#     fileWriter = open('hmmmodel.txt','w')
#     
#     fileWriter.write(str(vocabulary.__len__()) + '\n' )
#     fileWriter.write(str(tags.__len__()) + '\n')
#     fileWriter.write(str(emission_probability.__len__()) + '\n')
#     fileWriter.write(str(transition_probability.__len__()) + '\n')
# 
#     fileWriter.close()

