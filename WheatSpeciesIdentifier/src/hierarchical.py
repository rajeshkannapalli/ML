'''
Created on Dec 11, 2015

@author: Rajeshkumar
'''
import math
import uuid

def printMatrix(matrix):
    for i in matrix:
        print i
        
def computeMean(param0, param1):
    clusteroid = [0]*(len(param0))
    for i in range(len(param0)):
        clusteroid[i] = ((float(param0[i]))+(float(param1[i])))/2
    return clusteroid

def updateDict(dict, k, l):
    items = list(dict.iterkeys())
    for i in items:
        if dict[i] == l:
            dict[i] = k
            
    return dict
 
def euclideanDistance(dataPoint1, dataPoint2):
    data1 = dataPoint1
    data2 = dataPoint2
    length = len(data1)
    distance = 0
    for i in range(length):
        try:
            distance += pow((float(data1[i]) - float(data2[i])), 2)
        except Exception as e:
            print data1
            print data2
            print 1/0
    
    return math.sqrt(distance)



def hierarchical(trainingData,limitValue):
    result = list()
    dict = {}
    for i in range(len(trainingData)):
        dict[" ".join(trainingData[i])] = uuid.uuid4()
    
    
    clusteroid = [0]*(len(trainingData[0]))
    # clusters = [clusteroid]*len(trainingData)
    
    
    clusteroids = list(trainingData)
#     clusters = [[None]*len(clusteroids[0])]*len(clusteroids)
    while(len(clusteroids)>limitValue):
        min = 10000
        k = 0
        l = 0
        matrix = [[0]*len(clusteroids) for _ in range(len(clusteroids))]
        for i in range(len(matrix)):
            sample1 = clusteroids[i]
        
            for j in range(i+1):
                sample2 = clusteroids[j]
                distance = euclideanDistance(sample1, sample2)
                matrix[i][j] = distance
                if i != j:
                    if distance < min:
                        min = distance
                        k = i
                        l = j
        clusteroid = computeMean(clusteroids[k],clusteroids[l])
        dict = updateDict(dict, dict[" ".join(clusteroids[k])],dict[" ".join(clusteroids[l])])
        clusteroid = [str(c) for c in clusteroid]
        dict[" ".join(clusteroid)] = dict[" ".join(clusteroids[k])]
        clusteroids[k] = clusteroid
        del clusteroids[l]
        limit = len(set(dict.values()))
    initialClassValues = set(dict.values())
    value = 5
    for classValue in initialClassValues:
        dict = updateDict(dict, value, classValue) 
        value = value +1
    for data in trainingData:
        label = dict[" ".join(data)]
        clusterSpecimen = [data,str(label)]
        result.append(clusterSpecimen)
        print "Class label for "+ str(data) + " is ----- "+str(label)      
    return result




