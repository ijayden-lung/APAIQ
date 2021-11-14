# APAIQ

## generate input files

APAIQ is available for two input format, wigle and bedGraph

#### generate from mapping tools

if you use STAR for mapping, use option --outWigType wiggle or --outWigType bedGraph. It generates RPM normalized wig or bedGraph output

#### generate from bam file


##### example for generating wig file
please intsall RSeQC

`conda install -c bioconda rseqc`

use infer_experiment.py to check the strandness

`infer_experiment.py -r hg38.refseq.bed12 -i test.bam`

use bam2wig.py to convert bam to big. use -u option for unique mapped reads

`bam2wig.py -i test.bam -s chrom.sizes -u --strand='1+-,1-+,2++,2--'  -o test`

the output is not normalized

##### example for generating wig file
please install bedtools 

`conda install -c bioconda bedtools`

here are examples for '1+-,1-+,2++,2--' strandness library

1. generate plus strand bedGraph file. Use -q 255 for unique mapped reads the upstream tool is STAR
```
samtools view -q 255 -b -f 128 -F 16 test.bam > test.fwd1.bam
samtools view -q 255 -b -f 80 test.bam > test.fwd2.bam
samtools merge -f test.fwd.bam test.fwd1.bam test.fwd2.bam
samtools index test.fwd.bam
bedtools genomecov -ibam test.fwd.bam -split -bg >test.fwd.bedGraph
```
2. generate minus strand bedGraph file. Use -q 255 for unique mapped reads the upstream tool is STAR
```
samtools view -q 255 -b -f 144 test.bam > test.rev1.bam
samtools view -q 255 -b -f 64 -F 16 test.bam > test.rev2.bam
samtools merge -f test.rev.bam test.rev1.bam test.rev2.bam
samtools index test.rev.bam
bedtools genomecov -ibam test.rev.bam -split -bg >test.rev.bedGraph
```

## generate oneline fa file
`python toOneLine.py --fa_file /path/to/fafile --species hg38`

## run APAIQ
if the input files are not normalized, please use option --depth. For example, --depth=10 for 10 millions total single-end mapped reads or  5 millions total paired-end mapped reads

unstranded 

`python src/APAIQ.py --input_file=$input_file  --fa_file=$fa_file  --name=$sample_name --DB_file $DB --model $model --depth=1`

starnded

`python APAIQ.py --input_plus='demo/fwd.bedGraph' --input_minus='demo/rev.bedGraph'  --fa_file='oneLine/hg38'  --name='sample_name' --DB_file='demo/polyADB3_gencode.chr21.pAs.txt'  --model='model/snu398_model.ckpt' --depth=1`



### Options
	--input_file <wig file or bedGraph file>			input file for unstranded only

	--input_plus <wig or bedGraph file>			input file for transcripts that originated from the forward strand

	--input_minus <wig or bedGraph file>			input file for transcripts that originated from the reverse strand

	--fa_file				path to one line fa file with species name

	--name					sample name

	--model					model

	--depth					default=1. For unnormalized input. use --depth=10 for 10 millions total single-end mapped reads, 5 millions total paired-end mapped reads

	--out_dir				default='out_dir'. output directory. 
	
	--RNASeqRCThreshold			default=0.05. Minimum RPM threshold for scaning item

	--window				default=201. Window sizes of the scaning item. Please do not change this value if you used the pre-trained model

	--keep_temp				use --keep_temp='yes', if you want to keep the temporary files.
	

## run regression
	`python APAIQ.py --input_plus='demo/fwd.norm.bedGraph' --input_minus='demo/rev.norm.bedGraph'   --model='model/snu398_regression.ckpt' --factor_path='model/normalize_factor' --pas_file='demo/regression_chr21_input.bed'`

