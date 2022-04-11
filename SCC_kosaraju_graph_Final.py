import pandas as pd 
import numpy as np 
import sys
import threading

# algorithmfor  computing strongly connected components (SCCs), and to run this algorithm on the given graph.
# # # This is the part of exercise for the course https://www.coursera.org/learn/algorithms-graphs-data-structures/home/welcome

# resetting recursion and stack size limit  $ ulimit -s for setting hard limit from terminal
sys.setrecursionlimit(1000000)
threading.stack_size(64*1024*10000)

# reading data and storing as pd.series with columns 'head' & 'tail
# $ delim_whitespaces = True when python or C reader not able to detect the separator
graph = pd.read_csv('SCC.txt',delim_whitespace=True, names = ['head','tail'])
print(graph.info())

# count of vertices # 875714
vertices = 875714

# finishing value counter and leader counter
ft =  0
s = 0

# book keeping for explore, ft values and leader; first value in list signifies the node name (actual is x+1)

explore = [[x,1,0,0] for x in range(0,vertices)]
explore = np.array(explore)


# define DFS Reverse

def DFSreverse(vertex):
    # to see the progress
    print("DFS reverse called with {}".format(vertex))

    global ft; global explore
    explore[vertex-1][1] = 0 # setting node explored
    df = graph[graph['tail'] == vertex] #reading tail of edges as first DFS need to work on reversed graph
    
    for x in df['head']:
        if(explore[x-1][1] == 1):
            DFSreverse(x)
    ft = ft + 1 #increment finishing time value
    explore[vertex-1][2] = ft #book keeping of ft value

# DFS second loop

def DFS(vertex):
    global ft; global explore; global s
    temp1 = explore[explore[:,2] == vertex] # variable to read the ft value as DFS runs top down based on ft values

    explore[temp1[0][0]][3] = s  #setting leader of node as "s"
    explore[temp1[0][0]][1] = 0   #marking node explored
    df = graph[graph['head'] == (temp1[0,0]+1)] #reading head of edges

    for x in df['tail']:
        # progress msg
        print("checking DSF indices {}".format(x))

        if(explore[x-1][1] == 1):
            DFS(explore[x-1][2])

# For outer loop for DFS reverse

for i in range(vertices,0,-1):
    
    print("Dereverse with outer indices {} ongoing".format(i)) #progress msg
    if (explore[i-1][1] == 1):
        DFSreverse(i)

# np.savetxt("expoloreDrev.txt", explore,fmt='%s') # $ writing DFS reverse execution to file

# Book keeping changes for DFS second pass, setting all noodes unexplored
for i in range(0,vertices):
    explore[i][1] = 1

# For outer loop for DSF

for i in range(vertices,0,-1):
    print("DSF with outer indices {} ongoing".format(i))
    temp = explore[explore[:,2] == i]
    
    if(temp[0,1] == 1):
        s = temp[0,0]+1
        DFS(i)

# writing final book keeping to file
np.savetxt("explorefinal.txt", explore,fmt='%s')

# creating pivot from booking data for SCC - leader node and SCC size

df = pd.DataFrame(explore[:,3], columns = ['leader'])
pivot = df['leader'].value_counts(dropna=True, sort=True)
pivot = pd.DataFrame(pivot)
pivot = pivot.reset_index()
pivot.columns = ['Leader Value ','SCC size']




# printing top 10 entries
print(pivot.head(10))
      