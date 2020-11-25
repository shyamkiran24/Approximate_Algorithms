import time
from operator import itemgetter

class Vertex:
	def __init__(self,ide):
		self.ide = ide
		self.adjList = list()
		self.colored = None

o = open('roadNet-TX.txt','r')
V = dict()
vertexList = list()
vertexSet = set()
maximumDegree = 0
for line in o:
	lis = line.split()
	if lis[0] not in vertexSet:
		vertexSet.add(lis[0])
		V[lis[0]] = Vertex(lis[0])
	V[lis[0]].adjList.append(lis[1])
	if(len(V[lis[0]].adjList)>maximumDegree):
		maximumDegree = len(V[lis[0]].adjList)

maxColors = maximumDegree
numberColors = 0
#e = time.time()
for v in V:
	vertexList.append([v,len(V[v].adjList)])
vertexList.sort(key = itemgetter(1),reverse = True)
e = time.time()	
for v in V:
	for color in range(maxColors):
		flag = 0
		for adj in V[v].adjList:
			if(V[adj].colored==color):
				flag = 1
		if(flag==0):
			V[v].colored = color
			if(color>=numberColors):
				numberColors = color
			break
			

print(numberColors)
s = time.time()
print(s-e)
count = 0
for v in V:
	present = V[v].colored
	for adj in V[v].adjList:
		if(V[adj].colored==present):
			count+=1
				
print(count/2)