import csv
import sys
from collections import defaultdict
import time
dist = dict()
N = 334863
class Graph:
	def __init__(self,edges):
		self.adjList = defaultdict(list)
		for line in edges:
			if line:
				newNode = [int(line[1]),float(line[2])]
				self.adjList[int(line[0])].insert(0,newNode)
				newNode = [int(line[0]),float(line[2])]
				self.adjList[int(line[1])].insert(0,newNode)
				dist[int(line[0])] = sys.maxsize
				dist[int(line[1])] = sys.maxsize

class Heap(): 
  
    def __init__(self): 
        self.array = [] 
        self.size = 0
        self.pos = dict() 
  
    def newMinHeapNode(self, v, dist): 
        minHeapNode = [v, dist] 
        return minHeapNode 
  
    
    def swapMinHeapNode(self,a, b): 
        t = self.array[a] 
        self.array[a] = self.array[b] 
        self.array[b] = t 
  
  
    def minHeapify(self, idx): 
        smallest = idx 
        left = 2*idx + 1
        right = 2*idx + 2
  
        if left < self.size and self.array[left][1] < self.array[smallest][1]: 
            smallest = left 
  
        if right < self.size and self.array[right][1]< self.array[smallest][1]: 
            smallest = right 
  
        
        if smallest != idx: 
  
            # Swap positions 
            self.pos[ self.array[smallest][0] ] = idx 
            self.pos[ self.array[idx][0] ] = smallest 
  
            # Swap nodes 
            self.swapMinHeapNode(smallest, idx) 
  
            self.minHeapify(smallest) 
  
   
    def extractMin(self): 
  
        # Return NULL wif heap is empty 
        if self.isEmpty() == True: 
            return
  
        # Store the root node 
        root = self.array[0] 
  
        # Replace root node with last node 
        lastNode = self.array[self.size - 1] 
        self.array[0] = lastNode 
  
        # Update position of last node 
        self.pos[lastNode[0]] = 0
        self.pos[root[0]] = self.size - 1
  
        # Reduce heap size and heapify root 
        self.size -= 1
        self.minHeapify(0) 
  
        return root 
  
    def isEmpty(self): 
        return True if self.size == 0 else False
  
    def decreaseKey(self, v, dist): 
  
       
  
        i = self.pos[v] 
  
       
        self.array[i][1] = dist 
  
  
        while i > 0 and self.array[i][1] < self.array[(i - 1) // 2][1]: 
  
            # Swap this node with its parent 
            self.pos[ self.array[i][0] ] = (i-1)//2
            self.pos[ self.array[(i-1)//2][0] ] = i 
            self.swapMinHeapNode(i, (i - 1)//2 ) 
  
          
            i = (i - 1) // 2; 
  
   
    def isInMinHeap(self, v): 
  
        if self.pos[v] < self.size: 
            return True
        return False
def printArr(dist,nodes):

	for i in dist:
		row = [i,dist[i]]
		nodes.writerow(row)

def Dijkstra(src,graph,nodes):
	minHeap = Heap()
	a = 0
	print(len(dist))
	for i in dist:
		minHeap.array.append(minHeap.newMinHeapNode(i,dist[i]))
		minHeap.pos[i] = a
		a = a+1
	
	dist[src] = 0
	minHeap.decreaseKey(src,dist[src])
	minHeap.size = N
	while minHeap.isEmpty() == False:
		newHeapNode = minHeap.extractMin()
		u = newHeapNode[0]
		
		for adj in graph.adjList[u]:
			v = adj[0]
		
			if minHeap.isInMinHeap(v) and dist[u] != sys.maxsize and adj[1] + dist[u] < dist[v]:
				dist[v] = adj[1] + dist[u]
				
				minHeap.decreaseKey(v,dist[v])
		
	printArr(dist,nodes)



e = open('com-amazon.ungraph.csv','r')
n = open('Hvalues-amazon.csv','w')
nodes = csv.writer(n)
edges = csv.reader(e)
graph = Graph(edges)
s = time.time()
Dijkstra(1,graph,nodes)
e = time.time()
print(e-s)

