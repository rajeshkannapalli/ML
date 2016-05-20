'''
Created on Dec 11, 2015

@author: Rajeshkumar
'''
import random
from src.hierarchical import hierarchical
from src.knnclassifier import knnclassifier
import operator

def computeMean(param0, param1):
    clusteroid = [0]*(len(param0))
    for i in range(len(param0)):
        clusteroid[i] = ((float(param0[i]))+(float(param1[i])))/2
    return clusteroid

def findAccuracy(originalData, predictedData):
    accuracy = 0
    size = len(originalData)
    for i in range(size):
        orgRow = originalData[i][0:-1]
        orgValue = originalData[i][-1]
        for j in range(size):
            predRow = predictedData[j][0]
            predValue = predictedData[j][-1]
            if orgRow == predRow:
                if orgValue == predValue:
                    accuracy = accuracy +1
                break
                
    accuracy1 = float(accuracy)/float(size)
    return accuracy1


def modifyResultClassValues1(result, trainingDataOriginal):
    classVal = list()
    classMappingList = dict()
    for row in trainingDataOriginal:
        classVal.append(row[-1])
    set1 = set(classVal)
    classVal = list(set1)
    for value in classVal:
        classItems = list()
        centroid = [0]*(len(trainingDataOriginal[0])-1)
        for row in trainingDataOriginal:
            if row[-1] == value:
                classItems.append(row)
        for item in classItems:
            centroid = computeMean(centroid, item[0:7])
        predClassValue = knnclassifier(result, centroid,5)
        classMappingList[predClassValue] =value
    return classMappingList   

def modifyResultClassValues(result, trainingDataOriginal):
    trnData = list()
    for data in trainingDataOriginal:
        trnData.append([data[0:7],data[-1]])
    classVal = list()
    classMappingList = dict()
    for row in result:
        classVal.append(row[-1])
    set1 = set(classVal)
    classVal = list(set1)
    for value in classVal:
        classItems = list()
        centroid = [0]*(len(trainingDataOriginal[0])-1)
        for row in result:
            if row[-1] == value:
                classItems.append(row)
        for item in classItems:
            centroid = computeMean(centroid, item[0])
        predClassValue = knnclassifier(trnData, centroid,5)
        classMappingList[value] =predClassValue
    return classMappingList 

        

def main():
    #fetch data
    fOpen = open("seeds_dataset.txt",'r')
    sampleDataSet = fOpen.readlines()
    for i in range(len(sampleDataSet)):
        sampleDataSet[i] = sampleDataSet[i].strip()
        sampleDataSet[i] = sampleDataSet[i].split("\t")
        if len(sampleDataSet[i]) != 7:
            #filtering for extra tabs
            sampleDataSet[i] = filter(None, sampleDataSet[i])
    #creating sample training and test data
    trainingDataOriginal = random.sample(sampleDataSet, int(0.7*len(sampleDataSet)))
    trainingData = list()
    for i  in range(len(trainingDataOriginal)):
        trainingData.append(trainingDataOriginal[i][0:7])
    testDataOriginal = list()
    for c in sampleDataSet:
        if c not in trainingDataOriginal:
            testDataOriginal.append(c)
    testData = list()
    for i  in range(len(testDataOriginal)):
        testData.append(testDataOriginal[i][0:7])
#perform hierarchical clustering over training data
    result = hierarchical(trainingData,3)
    classMappingList = modifyResultClassValues(result, trainingDataOriginal)
    for i in range(len(result)):
        result[i][-1]= classMappingList[result[i][-1]]
        
    testDataResult = list()
    for data in testData:
        classValue = knnclassifier(result, data,5)
        testDataResult.append([data,classValue])
    print "Values for Class Labels are as follows"
    for data in testDataResult:
        print "Class label for test data :"+str(data[0])+" is -->"+data[1]
    
    print "training Accuracy:-"+str(findAccuracy(trainingDataOriginal,result))
    print "test Accuracy:-"+str(findAccuracy(testDataOriginal,testDataResult))
    
    
main()