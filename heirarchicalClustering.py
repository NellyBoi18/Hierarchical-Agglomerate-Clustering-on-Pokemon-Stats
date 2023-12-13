import csv
import math
import numpy as np
import scipy.cluster.hierarchy as sp
import matplotlib.pyplot as plt

# Input: string, the path to a file to be read
# Output: list; each element of the list is a dict representing one row of the file read; 
#         the key of dict is a string(such as ‘Attack’) and the value of the string is a string(such as ‘111’)
def load_data(filepath):
    with open(filepath) as file:
        reader = csv.DictReader(file)
        listOfDicts = list(reader)

    for row in listOfDicts:
        del row['#']
        del row['Name']
        del row['Type 1']
        del row['Type 2']
        del row['Total']
        del row['Generation']
        del row['Legendary']

    return listOfDicts

# Input: dict representing one Pokemon.
# Output: numpy array of shape (6,) and dtype int64. 
#         The first element is x1 and so on with the sixth element being x6.
def calc_features(row):
    x1 = int(row['Attack'])
    x2 = int(row['Sp. Atk'])
    x3 = int(row['Speed'])
    x4 = int(row['Defense'])
    x5 = int(row['Sp. Def'])
    x6 = int(row['HP'])
    
    array = np.array([[x1, x2, x3, x4, x5, x6],])
    array = np.int64(array)
    print(array)

    return array

# Input: list of numpy arrays of shape (6, )
# Output: numpy array Z of the shape (n−1)×4.
def hac(features):
    length = len(features) # length of list
    point = {} # points 
    Z = {} # final cluster
    merged = {} # list of points already merged
    # Declaring all arrays/lists
    for x in range(length):
        point[x] = None
    print(type(point))
    point = list(point)
    print("point", type(point))
    Z = [[None for x in range(4)] for y in range(length - 1)]
    print("Z", type(Z))
    merged = [[None for x in range(3)] for y in range(length - 1)]

    # iterating through features
    for row in range(length - 1):
        max = [math.inf, math.inf, math.inf] # set to max to find lowest
        
        # Finding shortest distance
        for i in range(length):
            for j in range(length):
                duplicate = False
                if ((point[i] != point[j]) or (point[i] == None and point[j] == None)):
                    print("not equal", i, j)
                    # Checking if any duplicates merged already
                    for x in range(row):
                        if (i == merged[x][1] and j == merged[x][2]):
                            duplicate = True
                        if (i == merged[x][2] and j == merged[x][1]):
                            duplicate = True
                    # Calculating distance using Euclidean distance formula in Numpy
                    distance = np.linalg.norm(features[i] - features[j])
                    if (i != j):
                        if (distance < max[0]):
                            if (not duplicate):
                                max[0] = distance
                                max[1] = i
                                max[2] = j
                                print("0", max[2])
                    # Tie
                    if (i != j):
                        if (distance == max[0]):
                            if (not duplicate):
                                if (i < max[1]):
                                    if (i < max[2]):
                                        max[0] = distance
                                        max[1] = i
                                        max[2] = j
                                        print("1", max[2])
                                if (j < max[1]):
                                    if (j < max[2]):
                                        max[0] = distance
                                        max[1] = i
                                        max[2] = j
                                        print("2", max[2])
                                if (i < max[1]):
                                    if (i == max[2]):
                                        if (j < max[1]):
                                            max[0] = distance
                                            max[1] = i
                                            max[2] = j
                                            print("3", max[2])
                                if (i < max[2]):
                                    if (i == max[1]):
                                        if (j < max[2]):
                                            max[0] = distance
                                            max[1] = i
                                            max[2] = j
                                            print("4", max[2])
                                if (j < max[1]):
                                    if (j == max[2]):
                                        if (i < max[1]):
                                            max[0] = distance
                                            max[1] = i
                                            max[2] = j
                                            print("5", max[2])
                                if (j < max[2]):
                                    if (j == max[1]):
                                        if (i < max[2]):
                                            max[0] = distance
                                            max[1] = i
                                            max[2] = j
                                            print("6", max[2])
        
        # Moving points to merged 
        merged[row][0] = max[0]
        merged[row][2] = max[1]
        merged[row][1] = max[2]
        tempCluster1 = point[max[1]]
        tempCluster2 = point[max[2]]
        print("point", point)
        print(max[2])
        print(point[4])
        print("HERE", tempCluster2)

        # New cluster for points
        tempPoint1 = 0
        tempPoint2 = 0
        
        # Number of points in cluster
        totalPokemon = 2
        if (tempCluster1 == None): # If empty
            tempPoint1 = max[1]
            point[max[1]] = row
        else:
            tempPoint1 = tempCluster1
            tempPoint1 += length
            if (Z[tempCluster1][3] == None):
                totalPokemon += -1
            else:
                totalPokemon += Z[tempCluster1][3] - 1
            for x in point:
                if (point[x] == tempCluster1):
                    point[x] = row
        
        if (tempCluster2 == None): # If empty
            tempPoint2 == max[2]
            point[max[2]] = row
        else:
            tempPoint2 = tempCluster2
            tempPoint2 += length
            print(tempCluster2)
            if (Z[tempCluster2][3] == None):
                totalPokemon += -1
            else:
                totalPokemon += Z[tempCluster2][3] - 1
            print(type(point))
            for x in point:
                if (point[x] == tempCluster2):
                    point = row
        
        if (tempPoint1 < tempPoint2):
            Z[row][0] = tempPoint1
            Z[row][1] = tempPoint2
        else:
            Z[row][0] = tempPoint2
            Z[row][1] = tempPoint1
        
        Z[row][2] = max[0]
        Z[row][3] = totalPokemon

    return np.array(Z)

# Input: numpy array Z output from hac
# Output: None, simply plt.show() a graph that visualizes the hierarchical clustering.
def imshow_hac(Z):
    sp.dendrogram(Z)
    plt.show()
    
    return

data = load_data('Pokemon.csv')
row1 = calc_features(data[1])
row2 = calc_features(data[2])
row3 = calc_features(data[3])
row4 = calc_features(data[4])
row50 = calc_features(data[50])
listOfNPArrays = [row1, row2, row3, row4, row50]
print(listOfNPArrays)
Z = hac(listOfNPArrays)
print(Z)
imshow_hac(Z)
