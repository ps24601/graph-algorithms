import numpy as np 
import pandas as  pd

# This is heap implementation of Dijkstra's shortest-path algorithm
## # # # This is the part of exercise for the course https://www.coursera.org/learn/algorithms-graphs-data-structures/home/welcome


df = pd.read_csv('dijkstraData.txt',delim_whitespace=True,names = [i for i in range(0,31)]) #max value of edges from any node is 30
graph = []
# print(df.info())
# print(df.head(2))
for i in range(1,201):  #Converting dataframe into usable format using list
    a = df[df[0]==i]

# print(a.isnull().values.any())
    count = a.isnull().sum().sum() # counting number of empty columns for any node
    count = 31-count
    temp = [0] *((count*2) - 2)
    temp = np.array(temp)
    temp = np.reshape(temp,(count-1,2))
   
    for i in range(1,count):
        b = np.array(a[i])
        b = np.array(b[0].split(','))
    
        temp[i-1,:] = b

    graph.append(temp)


X = {1:0} # distance matrix of all vertices from source

X_unexplored = [i for i in range(0,201)] # variant of df for tracking unexplored set, used currently only for initial heap initialization
heap_matrix = {}
heap = [[None,None]] *200 # unexplored data, [i,j] i = node name, j = smallest distance from X
heap[0] = [0,0] # first element is source
counter =1 # for heap end

def heapinitialize(heapi,r):   #first time heap initialization subroutine
    if(heapi[1] >= heap[int(r/2)][1]):
        heap[r] = heapi
    else:
        heap[r] = heap[int(r/2)]
        heap[int(r/2)] = heapi
        heapinitialize(heap[int(r/2)],int(r/2))

# Outer Loop for first time heap initialization
for i in graph[0]:  
    X_unexplored[i[0]] = None # marking node explored
    heap_matrix[i[0]] = i[1]
    # print(i[1],heap[int(counter/2)][1])
    if(counter ==1): # initial condition
        heap[counter] = i
    else:
        heapinitialize(i,counter)
    counter = counter +1


print('heap end value after initialization',counter)
print('heap after initialization ',heap)    
print('heap matrix',heap_matrix)
print(X)

heapend = counter

# np.savetxt("graph.txt", graph,fmt='%s')

def heapdel():     # deletion only from root, whereby heapend value moves to root and then bubble down to actual place
     # value to delete
    global heapend

    if(heapend ==1):
        print("Heap is empty")
        return heapend
    elif(heapend == 2):
        heap[1] ==  [None,None]
        heapend = 1
        return heapend
    else:
        temp = heap[heapend-1]    #pulling last element
        heap[heapend-1] = [None,None]
        heapend = heapend -1
        heap[1] = temp
        bubbledown(temp,1)

    # print(heap)
    # print(heapend)


def bubbledown(pairvalue,i): # bubble down subroutine
    if(2*i +1 < heapend):
        if( (pairvalue[1] > heap[2*i][1]) or (pairvalue[1] > heap[2*i +1][1]) ):
            if( heap[2*i][1] < heap[2*i +1][1] ):
                heap[i] = heap[2*i]
                heap[2*i] = pairvalue
                bubbledown(pairvalue,2*i)
            else:
                heap[i] = heap[2*i +1]
                heap[2*i +1] = pairvalue
                bubbledown(pairvalue, 2*i +1)
        else:
            heap[i] = pairvalue
    elif(2*i > heapend -1):
        heap[i] = pairvalue
    elif(pairvalue[1] > heap[2*i][1]):
        heap[i] = heap[2*i]
        heap[2*i] = pairvalue
        bubbledown(pairvalue,2*i)
    return



def bubbleup(pairvalue,i): # bubbleup subroutine
    # print("bubbleup",pairvalue,i)
    if(i==1):
        heap[i] = pairvalue
    elif(heap[int(i/2)][1]> pairvalue[1]):
        heap[i]= heap[int(i/2)]
        heap[int(i/2)] = pairvalue
        bubbleup(pairvalue,int(i/2))
    else:
        heap[i] = pairvalue
    return

    # print("finishing bubbleup",heap)



def remove(vw):
    # print(heap,heapend)
    for i in range(1,heapend):
        if( (vw[0] == heap[i][0]) and (vw[1] == heap[i][1])):
            # print(heap[i])
            heap[i][1] = -1
            bubbleup(heap[i],i)
            break
    heapdel()
    # print(heap)
    return



while(heapend != 1): # running main loop
    print("x", X)
    print("heap", heap)
    print("heapend",heapend)
    print("heap_matrix", heap_matrix)
    X[heap[1][0]] = heap[1][1]  # adding root of heap to X
    newelement = heap[1]   # saving value of root in temp variable
    # print("called from while")
    heapdel()
    
    # updating heap
    for i in graph[newelement[0]-1]: 
        print("calling graph values",heapend,i)
        if(i[0] in X.keys()):
            continue
        elif(i[0] in heap_matrix.keys()):
            if(heap_matrix[i[0]] > (newelement[1] + i[1])):
                # print("calling from remove",)
                # print(heap,heapend)
                remove(np.array([i[0],heap_matrix[i[0]]]))
                heap_matrix[i[0]] = newelement[1] + i[1]
                heap[heapend] = np.array([i[0],newelement[1] + i[1]])
                bubbleup(np.array([i[0],newelement[1] + i[1]]),heapend)
                heapend = heapend +1     
        else:
            heap_matrix[i[0]] = newelement[1] + i[1]
            heap[heapend] = np.array([i[0],newelement[1] + i[1]])
            bubbleup(np.array([i[0],newelement[1] + i[1]]),heapend)
            heapend = heapend +1

        print('exiting for',heap,heapend)
        
   



print(X)
print(heap)
print(heapend)

np.savetxt("X.txt", X,fmt='%s')
# np.savetxt("heap_matrix.txt", heap_matrix,fmt='%s')
