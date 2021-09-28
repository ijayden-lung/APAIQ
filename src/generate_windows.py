#!/usr/bin/env python
# coding: utf-8

import os
import glob
from collections import OrderedDict,defaultdict
import pipes
import pprint
import tempfile
import re
import argparse
#from pyfaidx import Fasta


def write_file(root_dir,dict_line,chromosome,strand,save_block,start,pre_pos,count,reference,window,name):
	ww = open(root_dir+'/%s.%s_%s_%d'%(name,chromosome,strand,save_block),'w')
	print('writing file '+root_dir+'/%s_%s_%d_%d-%d'%(chromosome,strand,save_block,start,pre_pos))
	pre_pos = 0
	pos_array = list(dict_line.keys())
	#for pos,val in dict_line.items():
	for i,pos in enumerate(pos_array):
		val = dict_line[pos]
	
		if(pos-pre_pos>=window):
			pre_pos = pos-window+1
		while(pos-pre_pos>=1):
			if pre_pos not in dict_line.keys():
				pre_base = reference[pre_pos-1]
				if(pre_base == 'N'):
					continue
				ww.write('%s:%d:%s\t%d\t%s\n'%(chromosome,pre_pos,strand,0,pre_base))
			pre_pos += 1
			
		ww.write('%s:%d:%s\t%s\n'%(chromosome,pos,strand,val))
		pre_pos = pos
		
		if(i < len(pos_array)-1):
			post_pos = pos_array[i+1]
			if(post_pos-pos>=window):
				post_pos = pos+window-1
		else:
			post_pos = pos+window-1
		while(post_pos - pre_pos>=1):
			if pre_pos not in dict_line.keys():
				pre_base = reference[pre_pos-1]
				if(pre_base == 'N'):
					continue
				ww.write('%s:%d:%s\t%d\t%s\n'%(chromosome,pre_pos,strand,0,pre_base))
			pre_pos += 1
			
	dict_line.clear()
	ww.close()
	

def split(root_dir,block_length,input_file,reference,window,chromosome,strand,name):
	
	wig_file = open(input_file, "r")
	lines = wig_file.readlines()
	wig_file.close()
	 
	num_lines = len(lines)
	num_blocks = num_lines/block_length
	len_blocks = num_lines/num_blocks
	
	pre_pos = 0
	dict_line = OrderedDict()
	count = 0
	separate_num=0
	save_block = 0
	start = 0
	
	for i, line in enumerate(lines):
		line = line.rstrip('\n')
		if(i==0):
			continue ###Skip header
		pos,rpm = line.split('\t')
		pos = int(pos)
		base = reference[pos-1]
		if(base == 'N'):
			continue
		#base = reference[chromosome][pos-1]
		rpm = float(rpm)
		if(rpm < 0):
			rpm = -rpm
		count += 1
		if(i==1):
			start=pos
		if(count>len_blocks and pos-pre_pos>1000 and save_block<num_blocks-1):
			write_file(root_dir,dict_line,chromosome,strand,save_block,start,pre_pos,count,reference,window,name)
			count = 0
			save_block += 1
			start  = pos
			
		
		dict_line[pos] = "%.5f\t%s"%(rpm,base)
		pre_pos = pos
		
	write_file(root_dir,dict_line,chromosome,strand,save_block,start,pre_pos,count,reference,window,name)
	

def get_genome_sequence(fa_file):
	f = open(fa_file,"r")
	line = f.readline()
	line = line.rstrip('\n')
	f.close()
	return line

def split_chr(root_dir,input_file,strand):
	wig_file = open(input_file, "r")
	for line in wig_file.readlines():
		line = line.rstrip('\n')
		if('variableStep' in line):
			info = line.split(' ')
			chromosome = info[1].split('chrom=')[1]
			if(len(chromosome)>3 or 'Y' in chromosome or 'M' in chromosome):
				continue

			if ('chr' not in chromosome):
				chromosome = 'chr'+chromosome
			out = open(root_dir+'/%s_%s.wig'%(chromosome,strand),'w')
		else:
			out.write("%s\n"%line)

def args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--out_dir', default=None, help='out dir')
	parser.add_argument('--input_file', default=None, help='unstranded wig file')
	parser.add_argument('--input_plus', default=None, help='plus strand wig file')
	parser.add_argument('--input_minus', default=None, help='minus strand wig file')
	parser.add_argument('--fa_file',default=None,help='path to one line fa file')
	parser.add_argument('--keep_temp',default=None,help='if you want to keep temporary file, set to "yes"')
	parser.add_argument('--window', default=201, type=int, help='input length')
	parser.add_argument('--name', default='sample',help='sample name')
  
	argv = parser.parse_args()

	out_dir = argv.out_dir
	input_file = argv.input_file
	input_plus = argv.input_plus
	input_minus = argv.input_minus
	fa_file = argv.fa_file
	keep_temp =  argv.keep_temp
	window = argv.window
	name= argv.name

	return out_dir,input_file,input_plus,input_minus,fa_file,keep_temp,window,name


def Generate_windows(root_dir,input_file,input_plus,input_minus,fa_file,keep_temp,window,name):
	block_length = 1e6
	window /= 1.5 ####No need more extendsion
	
	if not os.path.exists(root_dir):
		os.makedirs(root_dir) 

	root_dir = root_dir+'/data'
	if not os.path.exists(root_dir):
		os.makedirs(root_dir) 


	#all_ref = Fasta(fa_file)
	#print("Finished getting reference sequence from "+fa_file)

	if(input_file is not None):
		strand = '+'
		split_chr(root_dir,input_file,strand)
		wig_chr_files = glob.glob(root_dir+"/*"+strand+".wig")
		for wig_file in wig_chr_files:
			basename = wig_file.split('/')[-1]
			chromosome = basename.split('_')[0]
			reference = get_genome_sequence('%s.%s.fa'%(fa_file,chromosome))
			#reference=all_ref[chromosome]
			split(root_dir,block_length,wig_file,reference,window,chromosome,strand,name)
		block_files = glob.glob(root_dir+"/*+*")
		for block in block_files:
			minus_block = block.replace('+','-')
			os.system('cp %s %s'%(block,minus_block))
	if(input_plus is not None):
		strand = '+'
		split_chr(root_dir,input_plus,strand)
		wig_chr_files = glob.glob(root_dir+"/*"+strand+".wig")
		for wig_file in wig_chr_files:
			basename = wig_file.split('/')[-1]
			chromosome = basename.split('_')[0]
			reference = get_genome_sequence('%s.%s.fa'%(fa_file,chromosome))
			split(root_dir,block_length,wig_file,reference,window,chromosome,strand,name)
	if(input_minus is not None):
		strand = '-'
		split_chr(root_dir,input_minus,strand)
		wig_chr_files = glob.glob(root_dir+"/*"+strand+".wig")
		for wig_file in wig_chr_files:
			basename = wig_file.split('/')[-1]
			chromosome = basename.split('_')[0]
			reference = get_genome_sequence('%s.%s.fa'%(fa_file,chromosome))
			split(root_dir,block_length,wig_file,reference,window,chromosome,strand,name)
	print("Finished merging coverage and sequence information")
	os.system('rm *%s/*.wig'%root_dir)



if __name__ == "__main__":
	#print(args())
	Generate_windows(*args())

