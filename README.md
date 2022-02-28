# Index-structure-and-mapping
Small project for INF589: Computational analysis of high-throughput sequencing data. Here we are dealing with index structure / mapping with Burrows-Wheeler transform (BWT)

## Instructions:
**Index structures/Mapping**
Implement a tool that constructs a BWT index and maps reads using the index.
- Use additional tables (suffix array, count tables). Take care of the size of
your index in main memory - can you implement the ‘tricks’ like storing
only every K-th row (e.g. K=100) and recompute in-between to save main
memory?
- Test on RNA viruses (HIV, SARS-Cov2, . . . ) and map simulated reads
without errors. Report performance (depending on genome size, read
lengths; use sufficiently many reads for a good estimation) and space
consumption.
- Can you show memory / speed trade-offs (e.g. by using count tables vs. no
count tables)? Take care to get an efficient implementation of search - note
that full count tables would allow linear search or at least O(n log n).

**Project alternative:** Use enhanced suffix array in place of BWT. Implement
linear search using LCP and child tables; compare against search without such
extra-tables. (Abouelhoda, et al. 2004)

**Remark:** No need for very efficient construction of the data structure; rather
focus on search efficiency (due to additional tables) and space consumption.

**Ideas**:
- Memory consumption: use https://pypi.org/project/memory-profiler/
- Time consumption: use https://docs.python.org/fr/3/library/time.html
