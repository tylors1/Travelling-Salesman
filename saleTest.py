import random
import math
import pprint
from matplotlib import pyplot as plt

def create_nodes(num_nodes, num_rows):
    elements = range(0, num_nodes)
    return [random.sample(elements, num_nodes) for _ in range(num_rows)]

def mutate(table, node_table, mutate_probability, cross_probability):
	for next_id, row in enumerate(table, 1):
		nodes = len(row)
		#mutation
		if random.random() > mutate_probability:
			mini, maxi = sorted(random.sample(range(nodes),2))
			row[mini:maxi+1] = row[mini:maxi+1][::-1]

		#crossover
		if random.random() > cross_probability:
			try:
				next_row = table[next_id]
			except IndexError:
				pass
			else:
				half_length = nodes//2
				mini = random.randint(0, half_length)
				maxi = mini + half_length - 1 + (nodes % 2)

				crossed = [None] * nodes
				crossed[mini:maxi+1] = next_row[mini:maxi+1]
				iterator = 0
				for element in row:
					if element in crossed:
						continue
					while mini <= iterator <= maxi:
						iterator += 1
					crossed[iterator] = element
					iterator += 1
				row[:] = crossed

def tournament_selection(table, node_table):
	s1 = table
	s2 = table
	for n, row in enumerate(table,0):
		s1[n] = sample_best(table, node_table)
		s2[n] = s1[n][0]
		
	return s2

def sample_best(table, node_table):
	t1, t2 = random.sample(table[1:], 2)
	return distance(t1, t2, node_table)

def distance(s1, s2, node_table):
    distance1 = sum_distances(s1, node_table)
    distance2 = sum_distances(s2, node_table)

    if distance1 < distance2:
        return list(s1), distance1
    else:
        return list(s2), distance2

def sum_distances(strategy, node_table):
    dist = 0
    first_row, second_row = node_table

    for idx_next_node, node1 in enumerate(strategy, 1):
        try:
            node2 = strategy[idx_next_node]
        except IndexError:
            node2 = strategy[0]
        dist += math.hypot(
            first_row[node2-1] - first_row[node1-1],
            second_row[node2-1] - second_row[node1-1])

    return dist

def draw_graph(node_table, strategy):
    graphX = [node_table[0][index - 1] for index in strategy]
    graphY = [node_table[1][index - 1] for index in strategy]

    plt.scatter(graphX, graphY)
    plt.plot(graphX, graphY)
    plt.show()


def main(nodes=50, strategies=100, generations=20000, mutateP=.7, crossP=.7):
	#create node locations
	node_table = create_nodes(nodes, 2)

	#create first generation
	table = create_nodes(nodes, strategies)

	print "TOP MEN are looking through:"
	print strategies, "strategies in", generations, "generations with",
	print nodes, "nodes in each strategy..."

	best_score = None
	for count in range(generations):
		mutate(table, node_table, mutateP, crossP)
		table = tournament_selection(table, node_table)
		strategy, score = sample_best(table, node_table)

		if best_score is None or score < best_score:
			best_strategy = strategy
			best_score = score

		if count % 500 == 0:
			print "Foraged", count, "berries"
			print "Best we got so far:", best_score, "with: ", best_strategy

	print "=========================================================================="
	print "Best we could find: ", best_score, "for strategy", best_strategy

	draw_graph(node_table, best_strategy)

main()
