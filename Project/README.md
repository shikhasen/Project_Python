Project Title: Weather Info Data Visualization using Python
The project downloads the data from the ftp://ftp.pyclass.com/Data/ and save into the local computer address and then data visualization is done for the Weather data using Python.
Prerequisites
What things you need to install the software and how to install them
Anaconda Python
Spyder Ipython Console (Comes by default with the Anaconda)
Jupyter Notebook (Either Sypder or Jupyter is required)
MS Excel

Project step by step Description: 
In order to do the data analysis using Pandas, first need to PIP install the Pandas libraries using command prompt. Pandas is the inbuilt library in Python for performing Data Analysis and operating different types of file.
In command line: Type PIP install Pandas
Pandas will be imported successfully and now it can be used in Spyder Ipython console or Jupyter by simply importing the Pandas library.Similarly, install other essential libraries. The code will look something like:
from ftplib import FTP, error_perm
import os
import glob
import pandas
import numpy
import patoolib
import seaborn as sns

1.	The data is downloaded by using function ftpDownloader mentioned in All_Function.py file and saved to the Python_Project_Input folder. The data are in the .gz format which needs to be extracted.
2.	The data is extracted by using function extractFiles mentioned in All_Function.py file and appearing as the .csv files in “Extracted” folder.
3.	addField function mentioned in All_Function.py file will add the “Station” column to the end of the sheet.
4.	Since the data in .csv files are of same type so I have concatenated all the files into a single file using function concatenate mentioned in All_Function.py file and saved to Python_Project_Output folder. This will also add the header to all the columns i.e Column Name. Now all the .csv files are merged into single csv file named “Concatenated.csv”.
5.	Merge function on All_Fnction.py will now merge the data of two files into a single file. On the left, the data from the “Concatenated.csv” file and on the right the data from the “Station-info.txt” file located in Python_Project_Input folder. The output is saved as “Concatenated-Merged.csv” in Python_Project_Output folder.
6.	Pivot function creates the pivot table as the output shown in “Pivoted.csv”. It takes the input as “Concatenated-Merged.csv” file.
7.	Plot function creates the visualization calling the pivot function and saves the output as the “Ploted.png” image in Python_Project_Output folder. For data visualization, I have imported seaborn and matlibplot library.
8.	Kml function will take the input from “Pivoted.csv” file and will produce the output as “Weather.kml” located in Python_Project_Output folder. For opening. kml files, you need to have google earth setup installed on your computer. Similarly, the kml function will also take the input from the users as the coordinates(Longitude and latitude) and will generate the sample point on google earth which is saved as SamplePointonGoogleEarth.kml in Python_Project_Output folder.
