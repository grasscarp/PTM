# Pathogen Transmission Model
PTM can help users visualize the transmission process of pathogens, basing on the inputted information, which should be a csv file containing the dates, locations, sequence types and labels of samples and neighbors (gNN) as well as the SNP between them.  

## Requirment
PTM was written by Python3. While running, plotnine, pandas will be imported. PTM support Chinese, but you should download "SimHei" first if you don't have this font.  

## Usage
**usage: PTM.py [-h] [--date DATE] [--same_st SAME_ST] [--same_ward SAME_WARD] [--thresh THRESH] path st**  

**positional arguments:**  
```
  path                                  input path of a csv file  
  st                                    the sequence type of pathogens being showed  
```
**optional arguments:**  
```
  -h, --help                            show this help message and exit  
  --date DATE, -d DATE                  format of inputted date (default: %Y-%m-%d)  
  --same_st SAME_ST, -s SAME_ST         only link pathogens of same sequence type (default: True)  
  --same_ward SAME_WARD, -w SAME_WARD   only link pathogens from same ward (default: False)  
  --thresh THRESH, -t THRESH            the threshold of SNP number to link (default: 2)  
```
for example, run  
```
C:\Users\cfish>python PTM.py E:\gNN.csv 307 -w True -t 10
```
to visualize the transmission in same locations, with the SNP threshold of 10.  

## Input
The inputted csv should contain the following columns:  

 ID | gNN | SNP | ID ward | ID date | ID ST | gNN ward | gNN date | gNN st 
 ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ----
 1-1 | 30-6 | 20 | Ward 3 | 2017-01-08 | 875 | Ward 1 | 2016-08-23 | 11
 1-10 | 7-6 | 1 | Ward 8 | 2018-11-29 | 11 | Ward 9 | 2016-06-06 | 11
 
 If the date format isn't "%Y-%m-%d", you should tell PTM through the optional parameter -d.
 
 ## Output
 
