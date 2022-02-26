# Probe design
The goal of this project is to design probes for marker genes in specified tissues such that those probes could be used in MERFISH

# Constraints
1. We don't want any individual gene to dominate a cell's signal, so there is a maximum expression of 200
2. We want to be able to observe individual genes, so there is a minimum expression of 5 in at least one cell type
3. We don't want the cumulative signal of an individual cell to be too strong as it will hamper imaging. There is a maximum cumulative expression of 500
4. We want the bits of our codebook to contain uniform information (they're "on" the same amount)
5. ~160 genes will be selected for a specific tissue as most informative of the separation between 

# Reference data
We will be using the reference Smart-Seq and 10X mouse expression data for which there are 19 and 21 regions 
