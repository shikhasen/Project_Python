from ftplib import FTP, error_perm
import os
import glob
import pandas
import numpy
import patoolib
import seaborn as sns


def ftpDownloader(stationId,startYear,endYear,url="ftp.pyclass.com",user="student@pyclass.com",passwd="student123"):
    ftp=FTP(url)       
    ftp.login(user,passwd)
    if not os.path.exists("C:\\Python_Project_Input"):           
        os.makedirs("C:\\Python_Project_Input")
    os.chdir("C:\\Python_Project_Input")
    for year in range(startYear,endYear+1):
        fullpath='/Data/%s/%s-%s.gz' % (year,stationId,year)    
        filename=os.path.basename(fullpath)
        try:
            with open(filename,"wb") as file:
                ftp.retrbinary('RETR %s' % fullpath, file.write)
            print("%s succesfully downloaded" % filename)
        except error_perm: 
            print("%s is not available" % filename)
            os.remove(filename)    
    ftp.close()
            
def extractFiles(indir="C:\\Python_Project_Input",out="C:\\Python_Project_Input\\Extracted"):
    os.chdir(indir)
    archives=glob.glob("*.gz")
    print (archives)
    if not os.path.exists(out):
       os.makedirs(out)
    files=os.listdir("Extracted")
    print(files)
    for archive in archives:
        if archive[:-3] not in files:
            patoolib.extract_archive(archive,outdir=out)
            
def addField(indir="C:\\Python_Project_Input\\Extracted"):
    os.chdir(indir)
    fileList=glob.glob("*")
    print ("fileList" ,fileList)
    for filename in fileList:
        df=pandas.read_csv(filename,sep='\s+',header=None)
        df["Station"]=[filename.rsplit("-",1)[0]]*df.shape[0]
        df.to_csv(filename+".csv",index=None,header=None)
        os.remove(filename)
        
def concatenate(indir="C:\\Python_Project_Input\\Extracted",outfile="C:\\Python_Project_Output\\Concatenated.csv"):
    os.chdir(indir)
    fileList=glob.glob("*.csv")
    dfList=[]
    colnames=["Year","Month","Day","Hour","Temp","DewTemp","Pressure","WindDir","WindSpeed","Sky","Precip1","Precip6","ID"]
    for filename in fileList:
        print (filename)
        df=pandas.read_csv(filename,header=None)
        dfList.append(df)
    concatDf=pandas.concat(dfList,axis=0)    
    concatDf.columns=colnames
    concatDf.head()
    concatDf.to_csv(outfile,index=None)
    
def merge(left="C:\\Python_Project_Output\\Concatenated.csv",right="C:\\CS\\station-info.txt",output="C:\\Python_Project_Output\\Concatenated-Merged.csv"):
    leftDf=pandas.read_csv(left)   
    rightDf=pandas.read_fwf(right,converters={"USAF":str,"WBAN":str})
    rightDf["USAF_WBAN"]=rightDf["USAF"]+"-"+rightDf["WBAN"]
    mergedDf=pandas.merge(leftDf,rightDf.ix[:,["USAF_WBAN","STATION NAME","LAT","LON"]],left_on="ID",right_on="USAF_WBAN")
    mergedDf.to_csv(output)

def pivot(infile="C:\\Python_Project_Output\\Concatenated-Merged.csv",outfile="C:\\Python_Project_Output\\Pivoted.csv"):
    df=pandas.read_csv(infile)
    df=df.replace(-9999,numpy.nan)
    df['Temp']=df["Temp"]/10.0
    table=pandas.pivot_table(df,index=["ID","LON","LAT","STATION NAME"],columns="Year",values="Temp")
    table.to_csv(outfile)
    return table

def plot(outfigure="C:\\Python_Project_Output\\Ploted.png"):
    df=pivot()
    df.T.plot(subplots=True,kind='bar')
    sns.plt.savefig(outfigure,dpi=200)
    
import simplekml 
kml=simplekml.Kml();   
kml.newpoint(name='Sample',coords=[(10,10)])
kml.newpoint(name='Sample',coords=[(15,15)])
kml.save("C:\\Python_Project_Output\\SamplePointonGoogleEarth.kml")

def kml(infile="C:\\Python_Project_Output\\Pivoted.csv",outfile="C:\\Python_Project_Output\\Weather.kml"):
    kml=simplekml.Kml();
    df=pandas.read_csv(infile,index_col=["ID","LON","LAT","STATION NAME"])
    for lon,lat,name in zip(df.index.get_level_values("LON"),df.index.get_level_values("LAT"),df.index.get_level_values("STATION NAME")):
        kml.newpoint(name=name,coords=[(lon,lat)])
        kml.save(outfile)
        
def milestoKm(miles):
    km=miles*1.6
    print(km)
    
m=input("Enter the miles you want to convert into km")
m=float(m)
milestoKm(m)

longitude=input("Enter Longitude: ")
latitude=input("Enter Latitude: ")
kml=simplekml.Kml(); 
kml.newpoint(name='Sample',coords=[(longitude,latitude)])
kml.save("C:\\Python_Project_Output\\UserGivenInput.kml")


stationIdString=input("Enter the station seperated by commas:")
startingYear=input("Enter start year: ")
endingYear=input("Enter end year: ")
stationIdList=stationIdString.split(',')



stationIdList=["010010-99999","010014-99999","010015-99999"]
for station in stationIdList:
    ftpDownloader(station,startingYear,endingYear)
    
extractFiles()
addField()
concatenate()
merge()
pivot()
plot()
kml()




    
    
    
    
    
    
    