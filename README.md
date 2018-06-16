# MED_286
This project aims at improving the GWAS gene ranking based on the PCNet network.

There are two main steps in our framework. First, we design a network embedding method based on supervised random walks and use the node representations to construct edge strengths of the gene-and-gene interactions. The supervised random walks are guided by the network’s motif counts and the GWAS topSNP scores (prior scores). Second, a network propagation is adopted on the embedding based edge weights to find the final ranking for the genes.

Use the following commands to perform the two steps:

Step 1 - Embedding the PCNet: "python embed_PCNet.py --weighted --undirected --input graph/raw_tri_PCNet.edgelist --output emb/PCNet.emb"

Step 2 - For propagating scores and out the ranking of top 1500 genes: "python gene_prediction.py"

Forder "Network data" contains the network input files and training data (including prior scores) and a mapping between PCNet's nodes and the correspoding genes.
