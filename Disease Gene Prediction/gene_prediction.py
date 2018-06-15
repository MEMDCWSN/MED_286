import numpy as np
from scipy.spatial import distance
import networkx as nx
from sets import Set
import math

DEPTH = 1
# NOTE THIS VERSION IS FOR UNDIRECTED GRAPHS

#dG = nx.read_edgelist("citation.edgelist", create_using=nx.DiGraph(), nodetype=int)
#dG = nx.read_edgelist("karate.edgelist", create_using=nx.Graph(), nodetype=int)
#dG = nx.read_edgelist("[LP]ppi.edgelist", create_using=nx.Graph(), nodetype=int)
#dG = nx.read_edgelist("ppi.edgelist", create_using=nx.Graph(), nodetype=int)
#print Nb[4613]

#wG = nx.DiGraph()
ALPHA = 1.0
PVAL_CUTOFF = 0.0001
N_neighbor = 10
print "N_neighbor =", N_neighbor

#FILE_INP = "./1st_PCNet_100_100.emb"
#FILE_INP = "../emb/PCNet_100_100.emb"
#FILE_INP = "../emb/PCNet_supervised_m45_100_100.emb"
#FILE_INP = "../emb/PCNet_trisupervised_100_100.emb"
#FILE_INP = "../emb/PCNet_supervised_100_100.emb"
#FILE_INP = "../emb/PCNet_trisupervised_noscores_100_100.emb"
FILE_INP = "../emb/PCNet_raw_tri_100_100.emb"

print FILE_INP

fi1 = open(FILE_INP, "r")
line = fi1.readline()
S = line.split()
N, d = int(S[0]), int(S[1])
print N, d
emb_vec = {}
for i in range(N):
    line = fi1.readline()
    S = line.split()
    vec = []
    for j in range(d):
        vec.append(float(S[j+1]))
    emb_vec[int(S[0])] = vec
fi1.close()

score = []
for i in range(N):
    score.append(0.0)

seed_nodes = []
with open("./score", "r") as fi2:
    lines = fi2.readlines()
    for line in lines:
        S = line.split()
        idx = int(S[0])
        sc = float(S[1])
	if (sc <= PVAL_CUTOFF):
            seed_nodes.append(idx)
            #score[idx] = sc
	    score[idx] = 1.0

print "score[19738] =", score[19738]
print "score[9988] =", score[9988]

#dG = nx.read_edgelist("/home/duong/Documents/Code/github/node2vec/graph/PCNet.edgelist", create_using=nx.Graph(), nodetype=int)
dG = nx.read_edgelist("./PCNet.edgelist", create_using=nx.Graph(), nodetype=int)

"""
G = dG.to_undirected()
print G.edges()[:100]
Nb = {}
for u in G.nodes():
    #print u
    temp = []
    for v in seed_nodes:
        temp.append([distance.euclidean(emb_vec[u], emb_vec[v]), v])
    temp.sort()
    #print temp
    
    Nb[u] = []
    for [dis, v] in temp[:N_neighbor]:		# select the top nearest neighbors
	if (u != v):
            Nb[u].append([v, dis])
    
   

    #for v in nx.neighbors(G, u):
        #Nb[u].append([v, distance.euclidean(emb_vec[u], emb_vec[v])])
    

    
p = []
n_p = []
for i in range(N):
    p.append(score[i])
    n_p.append(score[i])

N_loop = 0
while (True):
    N_loop = N_loop + 1
    print "N_loop =", N_loop
    
    for u in G.nodes():
        summ = 0.0
        weight = 0.0
        for [v, dis] in Nb[u]:
            if (p[v] > 0.0):
                summ = summ + p[v]/dis
                weight = weight + 1.0/dis

        if (summ > 0.0):
            if (p[u] > 0.0):
                n_p[u] = (p[u] + (summ / weight)) / 2
            else:		# considering
                n_p[u] = summ / weight

    if (np.allclose(p, n_p)):
        break

    p = np.copy(n_p)


"""

G = dG.to_undirected()
print G.edges()[:100]
Nb = {}
for u in G.nodes():
    #print u
    Nb[u] = []
    for v in nx.neighbors(G, u):
        Nb[u].append([v, distance.euclidean(emb_vec[u], emb_vec[v])])
	#Nb[u].append([v, distance.cosine(emb_vec[u], emb_vec[v])])
    if (u % 1000 == 0):
        print "u, Nb[u] =",  u, Nb[u]

p = []
n_p = []
for i in range(N):
    p.append(score[i])
    n_p.append(score[i])

N_loop = 0
while (True):
    N_loop = N_loop + 1
    print "N_loop =", N_loop

    for u in G.nodes():
        summ = 0.0
        weight = 0.0
	for [v, dis] in Nb[u]:
            #summ = summ + p[v]/dis/degree[v]
            #weight = weight + 1.0/dis/degree[v]
            summ = summ + p[v]/dis
            weight = weight + 1.0/dis

        n_p[u] = ALPHA*summ/weight + (1-ALPHA)*score[u]

        #print("n_p =", n_p)
    if (np.allclose(p, n_p, rtol = 0.0, atol = 0.000000000001)):
        break

    p = np.copy(n_p)
        
    
temp = []
for i in range(N):
    temp.append([n_p[i], i])

print "top 1500"
temp.sort(reverse = True)
#thresh = temp[100]
#print "threshould =", thresh
for [sc, idx] in temp[:1500]:
    print idx, sc
