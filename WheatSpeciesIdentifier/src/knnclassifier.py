'''
Created on Dec 11, 2015

@author: Rajeshkumar
'''
import math
import operator


def euclideanDistance(dataPoint1, dataPoint2):
    data1 = dataPoint1
    
    length = len(data1)
    distance = 0
    for i in range(length):
        distance += pow((float(data1[i]) - float(dataPoint2[i])), 2)
    return math.sqrt(distance)

def knnclassifier(trainingData, testData,k):
    classValue = ""
    distArray = list()
    classVal = list()
    for row in trainingData:
        classVal.append(row[-1])
        distance = euclideanDistance(testData, row[0])
        distArray.append([row,distance])
    set1 = set(classVal)
    classVal = list(set1)
    classCount = [0]*len(classVal)
    distArray.sort(key=operator.itemgetter(1))
    for x in range(int(k)):
        for y in range(len(classVal)):
            if distArray[x][0][-1] == classVal[y]:
                classCount[y] = classCount[y]+1
    max = 0
    index = 0
    for x in range(len(classCount)):
        if classCount[x]>max:
            max = classCount[x]
            index = x 
    classValue = classVal[index] 
    return classValue

    


