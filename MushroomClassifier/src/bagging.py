from __future__ import with_statement
import csv
import random
from src.decisionTree  import *

def fetchDataset(lines, attrs):
    data = []
    for line in lines:
        data.append(dict(zip(attrs,[datum.strip() for datum in line])))
    return data

def findAccuracy(testData,classData):
    right=0
    wrong=0
    for x in testData:
        c=classData.pop(0)[0]
        if x==c :
            right+=1
        else:
            wrong+=1
    print "The Correctly predicted classes are %i "%(right)
    print "The Incorrectly predicted classes are %i "%(wrong)
    print "The Accuracy is = %.2f%%"%(float(right)/float(right+wrong)*100)

def majVotClass(classes):
    count = {}
    for class1 in classes:
        targetClass=class1[0]
        if targetClass in count:
            count[targetClass] += 1
        else:
            count[targetClass] = 1
    popularClass = sorted(count, key = count.get, reverse = True)
    top = popularClass[:1]
    return top
with open("MushroomTrain.csv", 'r') as f:
    lines = [row for row in csv.reader(f.read().splitlines())]

trainSize=len(lines)
classifiers = []

attributes = ["class", "cap-shape", "cap-surface", "cap-color", "bruises"]
targetAttr = attributes[0]
numberOfBagging = input("Number of bagging user requires")
for i in range(numberOfBagging):
    baggingDataSet=[]
    dataSet=[]
    for x in range(trainSize):
        index= random.randrange(0,trainSize-1,1)
        dataSet.append(lines[index])
    baggingDataSet = fetchDataset(dataSet, attributes)
    tree = createDTree(baggingDataSet, attributes, targetAttr, gain)
    classifiers.append(tree)
with open("MushroomTest.csv", 'r') as f:
    lines = [row for row in csv.reader(f.read().splitlines())]
testClass = []
for  i in lines:
    testClass.append(i[0])
testData= fetchDataset(lines, attributes)
occuringClass = []
for data in testData:
    results=[]
    list= [data]
    for classifier in classifiers:
        results.append(classify(classifier, list))
    occuringClass.append(majVotClass(results))
for i in occuringClass:
    print i[0]   
print "After Applying Bagging %i times for Training data"%numberOfBagging
findAccuracy(testClass, occuringClass)
