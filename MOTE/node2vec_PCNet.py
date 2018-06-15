import math
import numpy as np
import networkx as nx
import random


class Graph():
	def __init__(self, nx_G, is_directed, p, q):
		self.G = nx_G
		self.is_directed = is_directed
		self.p = p
		self.q = q


	def simulate_walks(self, num_walks, walk_length):
		'''
		Repeatedly simulate random walks from each node.
		'''
		G = self.G
		walks = []
		nodes = list(G.nodes())
		N = len(G.nodes())
		
                score = []
                for i in range(N):
                    score.append(0.001)

                with open("graph/score", "r") as fi2:
                    lines = fi2.readlines()
                    for line in lines:
                        S = line.split()
                        idx = int(S[0])
                        sc = float(S[1])
                        
                        """
                        if (sc < 0.0001):
                            score[idx] = 1.0
                        else:
                            score[idx] = 0.0
                        """
                        score[idx] = -math.log(sc)
			#score[idx] = 1.0


                print "score[19738] =", score[19738]
                print "score[9988] =", score[9988]


                out_adj = {}            # store neighbors for each node
                for node in nodes:
                        if (self.is_directed):
                                out_adj[node] = G.successors(node)
                        else:
                                out_adj[node] = G.neighbors(node)
                                
                print 'Walk iteration:'
                for i in range(num_walks):
                        random.shuffle(nodes)           # shuffle node set before doing random walks
                        print "Step:", i+1, "/", num_walks
                        for node in nodes:              # Wishky walk from this node
                                walk = [node]
                                l = 0
                                
                                while (l < walk_length-1):
                                        u = walk[l]
                                        if (out_adj[u] == []):          # cannot go further
                                                break

                                        total = 0.0
                                        r = random.random()
                                        summ = 0.0
                                        
                                        for v in out_adj[u]:
                                                total = total + score[v]*G[u][v]['weight']
                                                
                                        for v in out_adj[u]:
                                                summ = summ + score[v]*G[u][v]['weight']
                                                if (summ/total > r):
                                                        break
                                                
                                        walk.append(v)
                                        l = l + 1
                                        
                                walks.append(walk)
                                #print i, walk
                                        
                return walks

                """
		print 'Walk iteration:'
		for walk_iter in range(num_walks):
			print str(walk_iter+1), '/', str(num_walks)
			random.shuffle(nodes)           # shuffle node set before doing random walks
			for node in nodes:
				walks.append(self.node2vec_walk(walk_length=walk_length, start_node=node, node_score=score))

		return walks
		"""
