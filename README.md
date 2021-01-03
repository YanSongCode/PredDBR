# PredDBR:
 Protein-DNA binding residues prediction via bagging strategy and Sequence-based Cube-Format Feature.
	
## Pre-requisite:
   - Python, Java, Pytorch
   - SANN tool (https://github.com/newtonjoo/sann)
   - HHblits tool (https://toolkit.tuebingen.mpg.de/#/hhblits)
   - NCBI nr database (https://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/)
   - Uniclust30 database (http://wwwuser.gwdg.de/~compbiol/uniclust/)
   
## Installation:

*Download this repository PredDBR at https://github.com/YanSongCode/PredDBR.git or https://github.com/YanSongCode/PredDBR/archive/PredDBR.zip first.
 Then, uncompress it and run it and run the following command lines on linux System.
~~~
 1. unzip  -n PredDBR.zip -d ./
 2. cd PredDBR-PredDBRR
 3. cd tools/
 4. tar zxvf blast-2.2.26.tar.gz
 5. tar zxvf junh_BlastpgpSSITEOutputPARSER.tar.gz
 6. tar zxvf psipred321.tar.gz
 7. cd ..
 8. edit "config.properties" by modify the relevant path of tools or database
~~~	
*The file of "config.properties" should be set as follows:

  SANN_RUNNER_PATH=xx/SANN/sann/bin/sann.sh
  BLASTPGP_DB_PATH=xx/nr
  PSIPRED321_FOLDER_DIR=xx/psipred321/
  HHBLITS_EXE_PATH=xx/hhblits
  HHBLITS_DB_PATH=xx/uniclust30_2018_08_hhsuite/uniclust30_2018_08/uniclust30_2018_08
  SITESEA_DB_FOLDER=xx/SiteSea
  BLASTPGP_EXE_PATH=./tools/blast-2.2.26/blastpgp
  BLAST_BIN_DIR=./tools/blast-2.2.26/
  BLASTPGP_OUTPUT_PARSER_DIR=./tools/junh_BlastpgpSSITEOutputPARSER
  #the environment of pytorch
  PYTHON=xx/anaconda3/bin/python

## Run:

	java -jar PredDBR.jar [input] [input] [input] [input]
	
	[input]Protein_name(String)  
	[input]Protein_sequence(String)	
	[input]Folder path to save the process files and result file
	[input]{PDNA-543,PDNA-335}(String)

	Note: 
	
       a. you should input four parameters: Protein_name, Protein_sequence, Folder path to save the process files and result file, training set;
       
	      the forth parameter is a fixed parameters : "PDNA-543" or "PDNA-335"; "PDNA-543" represents the models constrcuted on dataset PDNA-543,
	 
	      "PDNA-335" represents the models constrcuted on dataset PDNA-335
	 
       b. the path of prediction result: "{Folder path to save the process files and result file}/PredDBR_Prod".

       c. give an example: java -jar PredDBR.jar 1A02_F RRIRRERNKMAAAKSRNRRRELTDTLQAETDQLEDEKSALQTEIANLLKEKEK ./result  PDNA-543
   
## Update History:

- First release 2020-12-28

## References 
[1] Jun Hu, Yan-Song Bai, Lin-Lin Zheng, Ning-Xin Jia, Dong-Jun Yu, Gui-Jun Zhang. Protein-DNA Binding Residue Prediction via Bagging Strategy and Sequence-based Cube-Format Feature. submitted
