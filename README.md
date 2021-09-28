# APAIQ

## how to generate input wig files
if you use STAR for mapping, use option --outWigType wiggle. The deault output is normalized

generate from bam file

please intsall RSeQC

`conda install -c bioconda rseqc`

use infer_experiment.py to check the strandness

`infer_experiment.py -r hg38.refseq.bed12 -i test.bam`

use bam2wig.py to convert bam to big

`bam2wig.py -i test.bam -s chrom.sizes -u --strand='1+-,1-+,2++,2--'  -o test`

the output is not normalized

## generate oneline
`python toOneLine.py --fa_file /path/to/fafile --species hg38`

## run APAIQ
unstranded 

`python src/APAIQ.py --input_file=$WIG  --fa_file=$fa_file  --name=$sample_name --DB_file $DB --model $model`

starnded

`python APAIQ.py --input_plus='demo/test_chr21_partial.minus.wig' --input_minus='demo/test_chr21_partial.minus.wig'  --fa_file='oneLine/hg38'  --name='sample_name' --DB_file='demo/polyADB3_gencode.chr21.pAs.txt'  --model='model/snu398_model.ckpt'`


if wig file are not normalized,use option --depth=10 for 10 millions total single-end mapped reads, 5 millions total paired-end mapped reads
