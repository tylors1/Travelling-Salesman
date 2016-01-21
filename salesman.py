import random
import math
import copy
from matplotlib import pyplot as plt

#number of nodes
nodes = 25
strategies = 100
generations = 100
mutateP = .70
crossP = 1.0
count = 0
bestStrat = [[0 for i in range(nodes)], 0]
temp = [[0 for i in range(nodes)], 0]
graphX = [0 for i in range(nodes)]
graphY = [0 for i in range(nodes)]
tempTable = [0 for i in range(nodes)]
parent1 = [0 for i in range(nodes)]
parent2 = [0 for i in range(nodes)]


#create first generation
table = [ [ 0 for i in range(6) ] for j in range(strategies) ]
for d1 in range(strategies):
	    table[d1] = random.sample(range(1, nodes+1), nodes)
for i in range(strategies):
	print table[i]


print "TOP MEN are looking through:"
print strategies, "strategies in", generations, "generations with", nodes, "nodes in each strategy..."

#create locations for nodes
def createNodeLocations():
	print "Creating locations for nodes"
	nodeTable = [ [ 0 for i in range(nodes) ] for j in range(2) ]
	for i in range(2):
		nodeTable[i] = random.sample(range(1, nodes+1), nodes)
		print nodeTable[i]
	return nodeTable

def generateIteration():

	for i in range(strategies):
		p = random.random()
		p2 = random.random()
		mini = 0
		maxi = 0

		# mutation!
		if p > mutateP:
			indices = random.sample(range(0,nodes), 2)
			mini = min(indices)
			maxi = max(indices)
			iterator = 0
			for j in range(maxi,mini-1,-1):
				tempTable[iterator] = table[i][j]
				iterator += 1

			iterator = 0
			for j in range(mini, maxi+1):
				table[i][j] = tempTable[iterator]
				iterator += 1

		# ordered crossover!
		if p2 > crossP:
			if i < strategies-1:
				iterator = 0
				if (nodes % 2) == 0:
					mini = random.randint(0, nodes/2)
					maxi = mini + nodes/2 -1 
				else:
					mini = random.randint(0, (nodes-1)/2)
					maxi = mini + (nodes-1)/(2)
				parent1 = copy.deepcopy(table[i])
				parent2 = copy.deepcopy(table[i+1])

				tempTable2 = [0 for i in range(nodes)]
				for j in range(mini, maxi+1):
					tempTable2[j] = copy.deepcopy(parent1[j])

				for j in range(0, nodes):
					if tempTable2[j] == 0:
						for k in range(len(parent2)):
							if parent2[k] not in tempTable2:
								tempTable2[j] = copy.deepcopy(parent2[k])
								break
				table[i] = copy.deepcopy(tempTable2)

		if (count == generations - 1):
			print table[i]

		#Begin the tournament
		for i in range(strategies):
			indices = random.sample(range(0,strategies), 2)
			mini = min(indices)
			maxi = max(indices)
			distance1 = sumDistance(table[mini])
			distance2 = sumDistance(table[maxi])
			winner = min(distance1, distance2)
			if(winner == distance1):
				table[i] = copy.deepcopy(table[mini])
			else:
				table[i] = copy.deepcopy(table[maxi])
	return table

def tournament(mini, maxi):
	selections = random.sample(range(1,strategies), 2)
	return findDistance(table[selections[0]], table[selections[1]])


def chooseTwo():
	selections = random.sample(range(1,strategies), 2)
	return findDistance(table[selections[0]], table[selections[1]])


def sumDistance(s1):

	distSum = 0
	for i in range(nodes):
		if (i < nodes-1):
			node1 = s1[i]
			node2 = s1[i+1]
			distSum += math.hypot(nodeTable[0][node2-1] - nodeTable[0][node1-1], nodeTable[1][node2-1] - nodeTable[1][node1-1])
		else:
			node1 = s1[i]
			node2 = s1[0]
			distSum += math.hypot(nodeTable[0][node2-1] - nodeTable[0][node1-1], nodeTable[1][node2-1] - nodeTable[1][node1-1])
	return distSum

def findDistance(s1, s2):
	distance1 = sumDistance(s1)
	distance2 = sumDistance(s2)
	winner = min(distance1, distance2)
	if(winner == distance1):
		stratWinner = s1
		temp[1] = distance1
	else:
		stratWinner = s2
		temp[1] = distance2
	temp[0] = stratWinner
	return temp

def drawGraph():
	
	for i in range(0,nodes):
		graphX[i] = nodeTable[0][bestStrat[0][i]-1]
		graphY[i] = nodeTable[1][bestStrat[0][i]-1]

	plt.scatter(graphX, graphY)
	plt.plot(graphX, graphY)
	plt.show()

nodeTable = createNodeLocations()

while (count < generations):
	table = generateIteration()	
	temp = chooseTwo()

	if(temp[1] < bestStrat[1] or bestStrat[1] == 0):
		bestStrat = copy.deepcopy(temp)
	
	if (count == generations - 1):
		print "========================================================="
		print "Best we could find: ", bestStrat


	if(count % 10 == 0):
		print "Foraged", count, "berries"
		print "Best we got so far:", bestStrat
	count+=1

drawGraph()

