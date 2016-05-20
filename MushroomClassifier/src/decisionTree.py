from __future__ import with_statement
import sys
import os.path
import csv
import math
import collections


def frequenctItem(list1):
    high = 0
    mostFrequent = None
    for value in unique(list1):
        if list1.count(value) > high:
            mostFrequent = value
            high = list1.count(value)
    return mostFrequent

def unique(list1):
    uniqueList = []
    for item in list1:
        if uniqueList.count(item) <= 0:
            uniqueList.append(item)
    return uniqueList



def choseAttribute(data, attrs, target, fit):
    maxGain = 0.0
    bestAttr = None
    for attr in attrs:
        gain = fit(data, attr, target)
        if (gain >= maxGain and attr != target):
            maxGain = gain
            bestAttr = attr
    return bestAttr

def fetchExamples(data, attr, value):
    data = data[:]
    arrayList = []
    if not data:
        return arrayList
    else:
        record = data.pop()
        if record[attr] == value:
            arrayList.append(record)
            arrayList.extend(fetchExamples(data, attr, value))
            return arrayList
        else:
            arrayList.extend(fetchExamples(data, attr, value))
            return arrayList

def fetchClassification(record, tree):
    if type(tree) == type("string"):
        return tree
    else:
        attr = tree.keys()[0]
        t = tree[attr][record[attr]]
        return fetchClassification(record, t)

def classify(tree, data):
    data = data[:]
    classification = []
    for record in data:
        classification.append(fetchClassification(record, tree))
    return classification

def createDTree(data, attrs, target, fit):
    data = data[:]
    values = [record[target] for record in data]
    default = frequenctItem([record[target] for record in data])
    if not data or (len(attrs) - 1) <= 0:
        return default
    elif values.count(values[0]) == len(values):
        return values[0]
    else:
        best = choseAttribute(data, attrs, target,
                                fit)
        tree = {best:collections.defaultdict(lambda: default)}
        values1 = unique([record[best] for record in data])
        for val in values1:
            subtree = createDTree(
                fetchExamples(data, best, val),
                [attr for attr in attrs if attr != best],
                target,
                fit)
            tree[best][val] = subtree
    return tree


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

def entropy(data, targetAttr):
    valFrequency = {}
    dataEntropy = 0.0
    for record in data:
        if (valFrequency.has_key(record[targetAttr])):
            valFrequency[record[targetAttr]] += 1.0
        else:
            valFrequency[record[targetAttr]] = 1.0
    for frequency in valFrequency.values():
        dataEntropy += (-frequency/len(data)) * math.log(frequency/len(data), 2) 
    return dataEntropy
    
def gain(data, attr, targetAttr):
    valFrequency = {}
    subEntropy = 0.0
    for record in data:
        if (valFrequency.has_key(record[attr])):
            valFrequency[record[attr]] += 1.0
        else:
            valFrequency[record[attr]] = 1.0
    for val in valFrequency.keys():
        valProb = valFrequency[val] / sum(valFrequency.values())
        dataSubset = [record for record in data if record[attr] == val]
        subEntropy += valProb * entropy(dataSubset, targetAttr)
    entropygain = (entropy(data, targetAttr) - subEntropy)
    return entropygain
 
def fetchFiles():
    if len(sys.argv) < 3:
        trainFile = "MushroomTrain.csv"
        testFile ="MushroomTest.csv"
    else:
        trainFile = sys.argv[1]
        testFile = sys.argv[2]
    def file_exists(filename):
        if os.path.isfile(filename):
            return True
        else:
            print "Error: The file '%s' does not exist." % filename
            return False

    if ((not file_exists(trainFile)) or
        (not file_exists(testFile))):
        sys.exit(0)
    return trainFile, testFile

def fetchAttrs(filename):
    with open(filename, 'r') as fin:
        header = fin.readline().strip()
    attributes = [attr.strip() for attr in header.split(",")]
    return attributes

def fetchData(filename, attributes):
    with open(filename, 'r') as f:
        lines = [row for row in csv.reader(f.read().splitlines())]
    data = []
    for line in lines:
        data.append(dict(zip(attributes,[datum.strip() for datum in line])))
    return data
    
def printTree(tree, str):
    if type(tree) == dict:
        print "%s%s" % (str, tree.keys()[0])
        for item in tree.values()[0].keys():
            print "%s\t%s" % (str, item)
            printTree(tree.values()[0][item], str + "\t")
    else:
        print "%s\t->\t%s" % (str, tree)
if __name__ == "__main__":
    trainFile, testFile = fetchFiles()
    attributes = ["class", "cap-shape", "cap-surface", "cap-color", "bruises"]
    targetAttr = attributes[0]
    training_data = fetchData(trainFile, attributes)
    testData = fetchData(testFile, attributes)
    dtree = createDTree(training_data, attributes, targetAttr, gain)
#     print dtree
    print "Decision Tree"
    
    printTree(dtree, "")
    classification = classify(dtree, testData)
    print "Result of Classification on Test Data"
     

    with open(testFile, 'r') as f:
       lines = [row for row in csv.reader(f.read().splitlines())]
    testClass=[]
    for l in lines:
        testClass.append(l[0])
    findAccuracy(testClass, classification)
