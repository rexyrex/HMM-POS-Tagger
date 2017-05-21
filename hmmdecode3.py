import pickle
import sys


def calculateTags(line, words, tags, emsProb, transProb):
    prev = dict()
    backChain = dict()
    splitWords = line.strip().split()
    prev['Q0'] = 0
    
    for i in range(len(splitWords)):

        chain = dict()
        backChain[i] = dict()
        for tag in tags:
            if splitWords[i] in words:
                if emsProb[tag].get(splitWords[i]) is None:
                    continue
                else:
                    emitVal = emsProb[tag][splitWords[i]]
            else:
                emitVal = 0
                
            maxProb = -sys.maxsize
            maxBackPointer = ''
            testBool = False
            for p in prev:
                if (prev[p] + transProb[tag][p] + emitVal) >= maxProb:
                    maxProb = prev[p] + transProb[tag][p] + emitVal
                    maxBackPointer = p
                    testBool = True
            if not testBool:
                maxBackPointer = next(iter(prev))
            prob = maxProb
            backPointer = maxBackPointer

            chain[tag] = prob
            backChain[i][tag] = backPointer

        prev = chain    
    mbp = ''
    testBool = False
    maxProb = -sys.maxsize
    for p in prev:
        if prev[p] > maxProb:
            maxProb = prev[p]
            mbp = p
            testBool = True
    if not testBool:
        maxBackPointer = next(iter(prev))
    finalBack = mbp
     
    
    tagChain = [finalBack]
    for i in range(len(splitWords)-1,0,-1):
        finalBack = backChain[i][finalBack]
        tagChain.append(finalBack)    
    return tagChain[::-1]

actual_tags = []
viterbiTags = []
processedLines = []

fileReader = open('hmmmodel.txt', 'rb')
objectLoader = pickle.load(fileReader)
words,tags = objectLoader[0],objectLoader[1]
emsProb, transProb = objectLoader[2],objectLoader[3]
fileReader.close()

fileReader = open(sys.argv[1], 'r', encoding="utf-8")
raw_lines = fileReader.readlines()
fileReader.close()

for line in raw_lines:
    calculatedTags = calculateTags(line, words, tags, emsProb, transProb)
    viterbiTags += calculatedTags
    splitWords = line.strip().split()
    processedLine = []
    for word in range(len(splitWords)):
        processedLine.append(splitWords[word] + '/' + calculatedTags[word])
    processedLines.append(' '.join(processedLine))

fileWriter = open('hmmoutput.txt', 'w', encoding="utf-8")
for line in processedLines:
    fileWriter.write(line+'\n')
fileWriter.close()
