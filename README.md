# PredDBR:

	 Protein-DNA binding residues prediction via bagging strategy and Sequence-based Cube-Format Feature feature.
	
## Pre-requisite:
   - python, java, pytorch
   - SANN tool (https://github.com/newtonjoo/sann)
   - hhblits tool (https://toolkit.tuebingen.mpg.de/#/hhblits)
   - NCBI nr database (https://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/)
   - uniclust30 database (http://wwwuser.gwdg.de/~compbiol/uniclust/)
   
## installation

* Download all files and folders
~~~
	1. unzip  PredDBR.zip -d /PredDBR
	
	2. cd PredDBR
	
	3. Configure config.properties by modify the relevant path of tools or database
~~~	

## Run

	java -jar PredDBR.jar [input] [input] [input] [input]
	
	[input]Protein_name(String)  
	[input]Protein_sequence(String)	
	[input]Folder path to save the process files and result file
	[input]{PDNA-543,PDNA-335}(String)
	
	Note: 
	
	a.you should input four parameters: Protein_name, Protein_sequence, Folder path to save the process files and result file, training set;
	
	the forth parameter is a fixed parameters : "PDNA-543" or "PDNA-335"; "PDNA-543" represents the models constrcuted on dataset PDNA-543,
	  
	"PDNA-335" represents the models constrcuted on dataset PDNA-335
	 
		
	b.the path of prediction result: "{Folder path to save the process files and result file}/PredDBR_Prod".
	
	c. give an example:
		java -jar PredDBR.jar 1A02_F RRIRRERNKMAAAKSRNRRRELTDTLQAETDQLEDEKSALQTEIANLLKEKEK ./result  PDNA-543 

## References 
[1] Jun Hu, Yan-Song Bai, Lin-Lin Zheng, Ning-Xin Jia, Dong-Jun Yu, Gui-Jun Zhang. Protein-DNA Binding Residue Prediction via Bagging Strategy and Sequence-based Cube-Format Feature. sumitted
