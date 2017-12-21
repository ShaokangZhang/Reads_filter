# Reads filter scripts
Some reads filter scripts used to filter out contamination reads


# Introduction 
Two scripts, one is used to filter reads using a reference, the second one is used to filter reads using kraken and related speicies name.
Mapping based script is faster. But sometimes you may need to use both of them to filter.

# Dependencies 
For mapping based "BWA_mapping_based_filter.py":

1. Python 2.7; 

2. [Burrows-Wheeler Aligner](http://sourceforge.net/projects/bio-bwa/files/); 

3. [Samtools](http://sourceforge.net/projects/samtools/files/samtools/);

4. [Bedtools](http://bedtools.readthedocs.io/en/latest/).

For kraken based "reads_filter_based_on_kraken.py":

1. Kraken

2. Seqtk

# Executing the code 
Type "-h" for details.
