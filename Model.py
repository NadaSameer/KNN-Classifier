import math


# Train data related


class Record:
    distance = []

    def __init__(self):
        self.__rFeatures = []
        self.__actualClass = 0
        self.__predictedClass = 0

    def CalculateDist(self, testFeatures):
        rSum = 0
        t = 0
        while t < len(self.__rFeatures):
            diff = (self.__rFeatures[t] - testFeatures[t]) ** 2
            rSum += diff
            t += 1
        Record.distance.append(math.sqrt(rSum))

    def SetFeat(self, features):
        self.__rFeatures.extend(features)

    def SetActClass(self, clss):
        self.__actualClass = clss

    def SetPreClass(self, clss):
        self.__predictedClass = clss

    def GetFeat(self):
        return self.__rFeatures

    def GetActClass(self):
        return self.__actualClass

    def GetPreClass(self):
        return self.__predictedClass

    @staticmethod
    def EmptyDistance():
        Record.distance = []

    @staticmethod
    def GetDistance():
        return Record.distance


def ReadFile(fileName):
    file = open(fileName, "r")
    features = []
    classes = []
    for i in file:
        tempList = i.split()
        classes.append(tempList[-1])
        tempList.remove(tempList[-1])
        features.append(list(map(float, tempList)))
    return features, classes


def AssignValues(feat, clas):
    i = 0
    recordList = []
    while i < len(feat):
        rec = Record()
        rec.SetFeat(feat[i])
        rec.SetActClass(clas[i])
        recordList.append(rec)
        i += 1
    return recordList


def PredictClass(distList, kValue, trainObj):
    dist = distList
    minIndices = []  # Holds Indices of records with min distance
    minClasses = []  # Holds classes of records that have min distance
    classFreqDict = {}  # Holds a dictionary of each class frequency
    for l in range(kValue):
        minInd = dist.index(min(dist))
        minIndices.append(minInd)
        dist.remove(dist[minInd])
    for l in minIndices:
        minClasses.append(trainObj[l].GetActClass())
    minClassesSet = set(minClasses)  # Holds set of uniq min distance classes
    for l in minClassesSet:
        freq = minClasses.count(l)
        item = {l: freq}
        classFreqDict.update(item)
    maxValue = max(classFreqDict.values())
    maxValues = [key for key, value in classFreqDict.items() if value == maxValue]
    lenMaxVal = len(maxValues)
    if lenMaxVal > 1:
        indList = []
        for l in maxValues:
            indList.append(trainClass.index(l))
        return trainClass[min(indList)]
    return maxValues[0]


trainFeat, trainClass = ReadFile("yeast_training.txt")
trainRecords = AssignValues(trainFeat, trainClass)

testFeat, testClass = ReadFile("yeast_test.txt")
testRecords = AssignValues(testFeat, testClass)
for k in range(1, 10):
    validCount = 0
    print("k value: ", k)
    for i in testRecords:
        for j in trainRecords:
            j.CalculateDist(i.GetFeat())
        predicted = PredictClass(Record.GetDistance(), k, trainRecords)
        i.SetPreClass(predicted)
        Record.EmptyDistance()
        if i.GetPreClass() == i.GetActClass():
            validCount += 1
        # print("Predicted class: ", i.GetPreClass(), " Actual class: ", i.GetActClass())
    accuracy = math.ceil((validCount / len(testClass)) * 100)
    print("Number of correctly classified instances: ", validCount, " Total number of instances: ", len(testClass))
    print("Accuracy : ", accuracy)


# for i in testRecords:
#     print(i.rFeatures, i.rClass, '\n')



#-------------------------------------------------------------------------------
# ReadFile("yeast_training.txt")
# r1 = Record([2, 4, 6, 8, 1, 0], 1)
# r1.CalculateDist([3, 6, 9, 4, 8, 1])
# print(r1.distance)


# for i in range(len(list1)):
#     result = max((list1.count(x), x) for x in set(list1))

# print(result)