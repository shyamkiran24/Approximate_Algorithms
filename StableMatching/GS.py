import time
import random
from collections import deque
o = open('foods.txt','r')
user = set()
product = set()
userList = deque()
productList = list()
use = dict()
prod =dict()

class Use:
	def __init__(self,ide):
		self.ide = ide
		self.adjList = list()
		self.match = None
#		self.rank = None
		self.p = 0
#product objects
class Prod:
	def __init__(self,ide):
		self.ide = ide
		self.adjList = list()
		self.match = None
		self.currank = None
		

for line in o:
	if line.startswith('product/productId:'):
		lis = line.split()
		pro = lis[1]
		if lis[1] not in product:
			product.add(lis[1])
			productList.append(lis[1])
			prod[lis[1]] = Prod(lis[1])
			continue
	if line.startswith('review/userId:'):
		lis = line.split()
		us = lis[1]
		if lis[1] not in user:
			user.add(lis[1])
			userList.append(lis[1])
			use[lis[1]] = Use(lis[1])
		
		use[us].adjList.append([prod[pro],len(prod[pro].adjList)])
		priority = len(prod[pro].adjList)
		prod[pro].adjList.append([use[us],priority])



stableMatch =set()
i = 0

def apply(a,b,rank):
	if(prod[b].match == None):
		#update
		prod[b].match = a
		use[a].match = b
		prod[b].currank = rank
		stableMatch.add((a,b))

		return True
	elif(rank<prod[b].currank):
		#update
		stableMatch.remove((prod[b].match,b))
		use[prod[b].match].match = None
		use[prod[b].match].p +=1
		userList.append(prod[b].match)
		prod[b].match = a
		use[a].match = b
		prod[b].currank = rank
		stableMatch.add((a,b))
		return True
	else:
		return False
e = time.time()
size1 = len(userList)
while(len(userList)>0):

	proposer = userList.popleft()
	i +=1
	prefListSize = len(use[proposer].adjList)
	while(use[proposer].p<prefListSize):
		result = apply(use[proposer].ide,use[proposer].adjList[use[proposer].p][0].ide,use[proposer].adjList[use[proposer].p][1])
		if result == True:
			break
		else:
			use[proposer].p +=1
s = time.time()
print(i)
print(len(stableMatch))
print(s-e)