#/bin/bash


###requirements
#python=3.7.3
#biopython=1.68
conda create -n 'APAIQ' python=3.7.3 biopython -y 
conda activate 'APAIQ'
#tensorflow=2.1.0
#tensorflow-estimator=2.1.0
conda install -c conda-forge tensorflow=2.1.0  tensorflow-estimator=2.1.0  -y
#pandas=0.25.3
conda install -c anaconda pandas=0.25.3  -y
