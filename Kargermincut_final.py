import numpy as np 
import pandas as pd
import random

# print(a)
sample  = pd.read_csv('kargerMinCut.txt', header=None)

# Randomized contraction algorithm for the min cut problem
# # This is the part of exercise for the course https://www.coursera.org/learn/algorithms-divide-conquer/home/welcome


def kargermincut(graph):
    # Base condition to return the value of edges remaining
    # random.seed(j)
    # print(j)
    leng = len(graph)
    value = 0
    if(leng == 2):
        # print(graph)
        
        # print(value, type(value))
        # print(len(graph[0])-1)
        return len(graph[0]) -1
    #generating random edge value
    node1selection = random.randint(0,leng-1)
    node1 = graph[node1selection]
    node2selection = random.randint(1,len(node1)-1)
    for x in range(0,len(values)):
        if (int(values[x]) == int(node1[node2selection])):
            node2 = graph[x]
            node2selection = x
            del(values[x])
            break
    # print(node1,node2)
    #  deleting self reference
    
    l = [y for y in node1 if y!= node2[0]]
    graph[node1selection] = node1 = l
    # print(graph,node1)
    
    #updating reference to other variables
    for x in node2[1:]:
        if(x != node1[0]):
            node1.append(x)
        # print(node1,graph)
        # updating reflist of other vertices
        for z in range(0,leng):
            # # print(x,graph[z][0])
            if(x == graph[z][0]):
                for p in range(1,len(graph[z])):
                    # # print(graph[z][p])
                    if(graph[z][p] == node2[0]):
                        graph[z][p] = node1[0]
    del(graph[node2selection])
    # print(graph)
    return kargermincut(graph)

# main body

variation = 40000

for i in range(0,1000):
    
    a =[]
    serieslen = sample[0].count()
    global values
    values = []
    for x in range(0,serieslen):
        a.append(sample[0][x].split())
        values.append(a[x][0])
    values = [i for i in range(1,serieslen +1)]
    count = kargermincut(a)
    print(count)
    if(count <variation):
        variation = count
print("min cut",variation)