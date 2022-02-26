# Probe design
The goal of this project is to design probes for marker genes in specified tissues such that those probes could be used in MERFISH

# Constraints
1. Maximum expression of 200 across all cell types
2. Minimum expression of 5 in at least one cell type
3. Maximum cumulative expression of 500
4. Uniform on/off bits in codebook 
5. 160 genes in 18 bit design 

# Reference data
We will be using the reference Smart-Seq and 10X mouse brain expression data from Allen 

# Workflow
1. Counts filters
2. PaintSHOP filters 
3. Other filters 
