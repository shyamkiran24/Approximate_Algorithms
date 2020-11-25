import csv
import sys
import time
import math

from collections import defaultdict
#expected length/max length
M = 700.0

class Node:                            
	def __init__(self,v,h):
		self.v = v
		self.parent = None
		self.d = 0.0                    
		self.g = sys.maxsize
		self.h = h
		self.f = sys.maxsize
		

class Graph:
	def __init__(self, edges):
		self.adjList = defaultdict(list)
		for line in edges:
			if line:
				evalue = float(line[2])
				newNode = [int(line[1]),evalue]
				self.adjList[int(line[0])].insert(0,newNode)
				newNode = [int(line[0]),evalue]
				self.adjList[int(line[1])].insert(0,newNode)




    
#Print path
def Track(nod,u,result):
	result.writerow([nod[u].g])
	k = u
	count = 0
	print("total cost of path: ",nod[u].g)
	while k != None:
#		print(nod[k].v)
#		print(len(graph.adjList[k]))
		count = count+1
		k = nod[k].parent
	print("Number of nodes on path: ",count)  
	result.writerow([count]) 
      
class Heap:
	def __init__(self):
		self.list = list()
		self.pos = dict()
		self.size = 0
	def swapMinHeapNode(self,id1,id2):
		temp = self.list[id1]
		self.list[id1] = self.list[id2]
		self.list[id2] = temp
	
	def minHeapify(self,idx):
		smallest = idx
		left = 2*idx + 1
		right = 2*idx + 2

		if left<self.size and self.list[left][0] < self.list[smallest][0]:
			smallest = left
		if right < self.size and self.list[right][0] < self.list[smallest][0]:
			smallest = right
		if smallest != idx:
			self.pos[self.list[smallest][1]] = idx
			self.pos[self.list[idx][1]] = smallest
			self.swapMinHeapNode(smallest,idx)
			self.minHeapify(smallest)

	def heappop(self):
		miniv = self.list[0]
		lastNode = self.list[self.size-1]
		self.list[0] = lastNode
		self.pos[lastNode[1]] = 0
		self.list[self.size-1] = miniv
		self.pos[miniv[1]] = self.size-1
		self.size = self.size-1
		self.list.pop()
		self.minHeapify(0)
		return miniv

	def decreaseKey(self,fnew,v):
		i = self.pos[v]
		self.list[i][0] = fnew
		while i>0 and self.list[i][0] < self.list[(i-1)//2][0]:
			self.pos[ self.list[i][1] ] = (i-1)//2
			self.pos[ self.list[(i-1)//2][1] ] = i
			self.swapMinHeapNode(i,(i-1)//2)
			i = (i-1)//2


	def heapinsert(self,f,v):
		newNode = [f,v]
		self.size = self.size + 1
		self.list.append(newNode)
		self.pos[v] = self.size-1
		self.decreaseKey(f,v)

def Astar(graph,src,dest,nod,result,itercount,total):
	
	fnew = 0.0
	gnew = 0.0
	hnew = 0.0
	nod[src].g = 0.0
	
	nod[src].f = 0.0
	openList = Heap()
	closedList = list()
	openSet = set()
	closedSet = set()
	openSet.add(nod[src])
	openList.heapinsert(0,nod[src].v)
	#openList contains all explored nodes, and the node is popped off once it is retreived from queue
	#all expanded nodes are in closed list
	while(True):
		mini = openList.heappop()

		u = mini[1]
	
		
		itercount =itercount + 1

	#Approximations added here
		if(u==dest):
			print(total)

			print(itercount)
			Track(nod,u,result)
			return
		
		openSet.remove(nod[u])
		closedList.append(nod[u])
		closedSet.add(nod[u])
		
		for adj in graph.adjList[u]:
			
	#		if adj[0] == dest:
	#			nod[adj[0]].g = nod[u].g + adj[1]
	#			nod[adj[0]].parent = u
	#			print(itercount)
	#			Track(nod,adj[0],result)
	#			return
	
			gnew = nod[u].g + adj[1]

			
		
			bait = (nod[u].d+1)/M
		
			
			bait1 = (1-bait)
	
			fnew = gnew + (1+(5*(bait1)))*(nod[adj[0]].h)


		#Approximations added here
		#	fnew = gnew + nod[adj[0]].h
			
			if ((nod[adj[0]] in closedSet)and gnew > nod[adj[0]].g):continue

			elif((nod[adj[0]] in closedSet)and gnew < nod[adj[0]].g):
				nod[adj[0]].g = gnew
				nod[adj[0]].parent = u
				nod[adj[0]].d = nod[u].d +1
				nod[adj[0]].f = fnew


			elif (nod[adj[0]] in openSet) & (fnew < nod[adj[0]].f) & (nod[adj[0]] != nod[u].parent):
				nod[adj[0]].g = gnew
				nod[adj[0]].parent = u
				nod[adj[0]].d = nod[u].d+1
				nod[adj[0]].f = fnew
				openList.decreaseKey(fnew,nod[adj[0]].v)
			else :
				if (fnew < nod[adj[0]].f):
					nod[adj[0]].g = gnew
					nod[adj[0]].parent = u
					nod[adj[0]].d = nod[u].d + 1
					nod[adj[0]].f = fnew
					openList.heapinsert(fnew,nod[adj[0]].v)
					openSet.add(nod[adj[0]])
					


				

if __name__ == '__main__':
    e = open('roadNet-PA1.csv','r') 
    n = open('HvaluesRN-PA.csv','r')

    edges = csv.reader(e)
    nodes = csv.reader(n)
    res = open('results3.csv','a')
    result = csv.writer(res)
    #Nodes

    nod = dict()
    for line in nodes:
    	if line:
    		hvalue = float(line[1])
    			
    		nod[int(line[0])] = Node(int(line[0]), hvalue)
    
    graph = Graph(edges)
    for i in graph.adjList:
    	if(len(graph.adjList[i])==0):
    		print(i)
    s = time.time()
    itercount = 0
    total = 0
    Astar(graph,1056668,0,nod,result,itercount,total)
    e = time.time()
    print(e-s)
    result.writerow(['roadNet-PA1',1056668,0,(e-s),M,5])
    