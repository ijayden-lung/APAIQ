#!/usr/bin/python
import argparse
import os

def args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--fa_file',default=None,help='path to fa file to generate chromosome separte oneline file')
	argv = parser.parse_args()
	fa_file = argv.fa_file
	return fa_file

def main(fa_file):
	fa = open(fa_file,'r')
	if not os.path.exists('oneLine'):
		os.makedirs('oneLine')
	skip = False
	for line in fa.readlines():
		line = line.rstrip('\n')
		if('>' in line):
			chro = line.split(' ')[0]
			chro = chro[1:]
			if(len(chro)>3 or 'M' in chro):
				skip = True
				continue
			else:
				ww = open('oneLine/'+chro+'.fa','w')
				ww.write('%s\n'%line)
				skip = False
		else:
			if(skip):
				continue
			ww.write(line)

	ww.close()

if __name__ == "__main__":
	main(args())
