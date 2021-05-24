################################ Question 1 ##############################################
#1.	What data quality check procedures would you take when calculating MMEs at the patient level? (Hint: what kind of data/record would be excluded from the sample?)
#Answers:Remove the rows and columns with Null/NaN values
#Remove non Opioids related records 
#Remove Buprenorphine related records
#Remove Tapentadol related record
#Remove records not in the timeframe





################################ Question 2.1 ##############################################

#Prescription.csv is the Prescription Dispensation Records
#Opioids.csv is the Opioids tab from CDC_Oral_Morphine_Milligram_Equivalents_Sept_2018.xlsx

#import the Prescription Data and Opioids Data
import pandas as pd
df=pd.read_csv(r"C:\Users\yangf\Desktop\Prescription.csv",engine='python')
dfmme=pd.read_csv(r"C:\Users\yangf\Desktop\Opioids.csv",engine='python')

##-------------------------------------------------------------------------
## 2.1.1 Data Cleaning
##-------------------------------------------------------------------------

#remove rows and columns with Null/NaN values in Prescription Data
df = df.dropna(how='any',axis=0) 

#combine Prescription and Opioids Data on NDC, inner join
df = pd.merge(df,dfmme[['NDC','Master_Form','Drug','LongShortActing',
                        'Strength_Per_Unit','UOM','MME_Conversion_Factor']],on='NDC', how='inner')

#remove rows and columns with Null/NaN values in new merged table, which removes non Opioids 
#related records as well as Buprenorphine related records
df = df.dropna(how='any',axis=0) 

#removes Tapentadol related record
df = df[(df["Drug"] != 'Tapentadol SA')&(df["Drug"] != 'Tapentadol LA')]

#Pick the Q3 data
df = df[(df["RxFillDate"] >= '7/1/2019')&(df["RxFillDate"] <= '9/30/2019')]
################################ Question 2.2 ##############################################

##-------------------------------------------------------------------------
## 2.1.2 Data Processing For Further Calculation
##-------------------------------------------------------------------------

#Create Adjust_Strength_Per_Unit for UOM =MCG
df['Adjust_Strength_Per_Unit']=(df['Strength_Per_Unit']/1000).where(((df['UOM']== 'MCG')|(df['UOM']== 'MCG/SPARY')), df['Strength_Per_Unit'])

#Adjust_RxDaysSupply for Fentanyl in Patch
df['Adjust_RxDaysSupply']=(df['RxDaysSupply']*3).where((((df['Drug']== 'Fentanyl LA')|(df['Drug']== 'Fentanyl SA'))& (df['Master_Form']== 'Patch, Extended Release')), df['RxDaysSupply'])

#MME_Total_Per_Row for each row
df['MME_Total_Per_Row']=df['Adjust_Strength_Per_Unit']*df['Unit']*df['MME_Conversion_Factor']

#MME_Daily for each row
df['MME_Daily']=df['MME_Total_Per_Row']/df['Adjust_RxDaysSupply']

#Patient_Sum for MME_Total_Per_Row for each patient
df['Patient_MME_Sum'] = df.groupby(['PatientID'])['MME_Total_Per_Row'].transform(sum)

#Save the Q3 merged file 
df.to_csv(r"C:\Users\yangf\Desktop\mergeq3.csv")
##-------------------------------------------------------------------------
## 2.2 Create a table for Patient erveryday medicine usage
##-------------------------------------------------------------------------
import numpy as np
from datetime import timedelta
data=pd.read_csv(r"C:\Users\yangf\Desktop\mergeq3.csv",engine='python',parse_dates=['RxFillDate'])

# only keep date, remove auto-generated time
data['RxFillDate'] = data['RxFillDate'].dt.date

# obtain the number of patient (length of unique id) 
patient_ids = set(data["PatientID"])

rows = []
for p in patient_ids:
    # obtain one patient id's information
    patient = data.loc[data["PatientID"]==p]
    
    ndc = patient["NDC"]
    mme_daily = patient["MME_Daily"]
    rxfilldate = patient["RxFillDate"]
    date_diff = patient["Adjust_RxDaysSupply"]
    longshortacting = patient["LongShortActing"]

   
    # repeat patient id info with added date for each row
    for i in range(0, len(ndc)):
        # length of period for one patient ID and one ndc
        d_diff = int(date_diff.iloc[i])
        # obtain start date of the ndc
        date = rxfilldate.iloc[i]
        # append the original row for the start date
        rows.append([p, ndc.iloc[i], mme_daily.iloc[i], longshortacting.iloc[i],date_diff.iloc[i], date])
        
        # for the remaining period dates
        for j in range(0, d_diff-1):
            # add one day for each column
            date = date + timedelta(days=1)
            # append row
            rows.append([p, ndc.iloc[i], mme_daily.iloc[i], longshortacting.iloc[i],date_diff.iloc[i], date])
            

# get column name for the new dataframe 
new_header = ("PatientID","NDC","MME_Daily","LongShortActing","Adjust_RxDaysSupply", "Date") 

# put data into new dataframe 
new_data = pd.DataFrame(rows, columns=new_header)


#the total MME amount for each patient for each day
new_data["Daily_PerDate_PerPatient"] = (new_data.groupby(["PatientID","Date"])["MME_Daily"].transform(sum))

new_data.to_csv(r"C:\Users\yangf\Desktop\patientdataperday.csv")
##-------------------------------------------------------------------------
## 2.2.1 Definition 1 Summing_days_supply
##-------------------------------------------------------------------------

df=pd.read_csv(r"C:\Users\yangf\Desktop\mergeq3.csv",engine='python')

#sum of supply for each patient
df["Summing_days_supply"] = (df.groupby(["PatientID"])["Adjust_RxDaysSupply"].transform(sum))
#Daily MME using Definition 1 
df["Summing_days_supply_MME"]=df["Patient_MME_Sum"]/df["Summing_days_supply"] 

#select unique PatientID
def1=df.drop_duplicates(['PatientID'],keep = 'first')

#select limited columns
def1=def1[['PatientID', 'Summing_days_supply_MME']]

#create new field Meet_90_MME, if the patient meet the 90 MME per day threshold, value will be 1
def1["Meet_90_MME"]=(def1.Summing_days_supply_MME >= 90).astype(int)

#print out the percentage of patient meet the 90 MME per day (frequency of Meet_90_MME=1)
print(def1.Meet_90_MME.value_counts(normalize=True))

def1.to_csv(r"C:\Users\yangf\Desktop\Definition1.csv")
0    0.979275
1    0.020725
Name: Meet_90_MME, dtype: float64
##-------------------------------------------------------------------------
## 2.2.2 Definition 2 account for overlap
##-------------------------------------------------------------------------

def2=pd.read_csv(r"C:\Users\yangf\Desktop\patientdataperday.csv",engine='python')

#count total number of days that medicine coverd
def2.drop_duplicates(["PatientID","Date"], inplace=True,keep = 'first')

def2 =def2.groupby(["PatientID"])["Date"].count().reset_index(name="DaysCount")

#get the total mme for per patient during Q3
mergeq3=pd.read_csv(r"C:\Users\yangf\Desktop\mergeq3.csv",engine='python')
mergeq3.drop_duplicates(["PatientID"], inplace=True,keep = 'first')

#combine two Prescription and Opioids Data on NDC, inner join
def2 = pd.merge(def2,mergeq3[['Patient_MME_Sum','PatientID']],on='PatientID', how='inner')

#caculate MME per day account for overlap
def2["OverlapMME"]=def2.Patient_MME_Sum/def2.DaysCount
#create new field Meet_90_MME, if the patient meet the 90 MME per day threshold, value will be 1
def2["Meet_90_MME"]=(def2.OverlapMME >= 90).astype(int)

#print out the percentage of patient meet the 90 MME per day (frequency of Meet_90_MME=1)
print(def2.Meet_90_MME.value_counts(normalize=True))

def2.to_csv(r"C:\Users\yangf\Desktop\Definition2.csv")
0    0.974093
1    0.025907
Name: Meet_90_MME, dtype: float64
##-------------------------------------------------------------------------
## 2.2.3 Definition 3 Defined_observation_window
##-------------------------------------------------------------------------

df=pd.read_csv(r"C:\Users\yangf\Desktop\mergeq3.csv",engine='python')

#Daily MME using Definition 3 Defined_observation_window
df['Defined_observation_window_MME']=df['Patient_MME_Sum']/92

#select unique PatientID
def3=df.drop_duplicates(['PatientID'],keep = 'first')

#select limited columns
def3=def3[['PatientID', 'Defined_observation_window_MME']]

#create new field Meet_90_MME, if the patient meet the 90 MME per day threshold, value will be 1
def3["Meet_90_MME"]=(def3.Defined_observation_window_MME >= 90).astype(int)

#print out the percentage of patient meet the 90 MME per day (frequency of Meet_90_MME=1)
print(def3.Meet_90_MME.value_counts(normalize=True))

def3.to_csv(r"C:\Users\yangf\Desktop\Definition3.csv")
0    0.997409
1    0.002591
Name: Meet_90_MME, dtype: float64
##-------------------------------------------------------------------------
## 2.2.4 Definition 4 Max Daily
##-------------------------------------------------------------------------

def4=pd.read_csv(r"C:\Users\yangf\Desktop\patientdataperday.csv",engine='python')

#sort by "PatientID","Daily_PerDate_PerPatient" , leaving the Max MME the top row for each patient
def4.sort_values(["PatientID","Daily_PerDate_PerPatient"], ascending=[True, False], inplace=True)

#delete duplicate, only leave the max mme per patient
def4.drop_duplicates(["PatientID"], inplace=True,keep = 'first')

#create new field Meet_90_MME, if the patient meet the 90 MME per day threshold, value will be 1
def4["Meet_90_MME"]=(def4.Daily_PerDate_PerPatient >= 90).astype(int)

#print out the percentage of patient meet the 90 MME per day (frequency of Meet_90_MME=1)
print(def4.Meet_90_MME.value_counts(normalize=True))

def4.to_csv(r"C:\Users\yangf\Desktop\Definition4.csv")
0    0.974093
1    0.025907
Name: Meet_90_MME, dtype: float64
################################ Question 2.3 ##############################################
##-------------------------------------------------------------------------
## 2.3  Create overlap table form patient data per day table
##-------------------------------------------------------------------------

overlap=pd.read_csv(r"C:\Users\yangf\Desktop\patientdataperday.csv",engine='python')
#select limited columns
overlap=overlap[['PatientID', 'Date','LongShortActing']]

#pick the patient that have SA and lA at the same day
overlap.drop_duplicates(['PatientID', 'Date','LongShortActing'], inplace=True,keep = 'first')
overlap =overlap.groupby(["PatientID","Date"])["PatientID"].count().reset_index(name="CountNumberofLASA")
overlap =overlap[(overlap["CountNumberofLASA"] >= 2)]
overlap.drop_duplicates(['PatientID'], inplace=True,keep = 'first')
overlap=overlap[['PatientID']]

overlap.to_csv(r"C:\Users\yangf\Desktop\overlap.csv")
##-------------------------------------------------------------------------
## 2.3.1  Definition 1: percentage of patients meet the 90 MME per day threshold and have LASA overlap 
##-------------------------------------------------------------------------

PatientID_Def1=pd.read_csv(r"C:\Users\yangf\Desktop\Definition1.csv",engine='python')

#number of total patient in Q3
total_Patient = PatientID_Def1.shape[0]
PatientID_Def1 = PatientID_Def1[(PatientID_Def1["Meet_90_MME"] == 1)]
PatientID_Def1 = pd.merge(PatientID_Def1,overlap[['PatientID']],on='PatientID', how='inner')
#number of total patient meet the 90 MME per day threshold and have LASA overlap in Q3 for definition 1
total_Patient_overlap=PatientID_Def1.shape[0]

# percentage of patients meet the 90 MME per day threshold and have LASA overlap
Percentage_Def1=(total_Patient_overlap)/total_Patient*100

print(Percentage_Def1 , '% Of patients meet the 90 MME per day threshold and have LASA overlap under definition 1')
0.2590673575129534 % Of patients meet the 90 MME per day threshold and have LASA overlap under definition 1
##-------------------------------------------------------------------------
## 2.3.2  Definition 2: percentage of patients meet the 90 MME per day threshold and have LASA overlap 
##-------------------------------------------------------------------------

PatientID_Def2=pd.read_csv(r"C:\Users\yangf\Desktop\Definition2.csv",engine='python')
#number of total patient in Q3
total_Patient = PatientID_Def2.shape[0]

PatientID_Def2 = PatientID_Def2[(PatientID_Def2["Meet_90_MME"] == 1)]
PatientID_Def2 = pd.merge(PatientID_Def2,overlap[['PatientID']],on='PatientID', how='inner')

#number of total patient meet the 90 MME per day threshold and have LASA overlap in Q3 for definition 2
total_Patient_overlap=PatientID_Def2.shape[0]

# percentage of patients meet the 90 MME per day threshold and have LASA overlap
Percentage_Def2=(total_Patient_overlap)/total_Patient*100


print(Percentage_Def2 , '% Of patients meet the 90 MME per day threshold and have LASA overlap under definition 2')
##-------------------------------------------------------------------------
## 2.3.3  Definition 3: percentage of patients meet the 90 MME per day threshold and have LASA overlap 
##-------------------------------------------------------------------------
PatientID_Def3=pd.read_csv(r"C:\Users\yangf\Desktop\Definition3.csv",engine='python')

#number of total patient in Q3
total_Patient = PatientID_Def3.shape[0]
PatientID_Def3 = PatientID_Def3[(PatientID_Def3["Meet_90_MME"] == 1)]
PatientID_Def3 = pd.merge(PatientID_Def3,overlap[['PatientID']],on='PatientID', how='inner')

#number of total patient meet the 90 MME per day threshold and have LASA overlap in Q3 for definition 3
total_Patient_overlap=PatientID_Def3.shape[0]

# percentage of patients meet the 90 MME per day threshold and have LASA overlap
Percentage_Def3=(total_Patient_overlap)/total_Patient*100

print(Percentage_Def3 , '% Of patients meet the 90 MME per day threshold and have LASA overlap under definition 3')

##-------------------------------------------------------------------------
## 2.3.4  Definition 4: percentage of patients meet the 90 MME per day threshold and have LASA overlap 
##-------------------------------------------------------------------------
PatientID_Def4=pd.read_csv(r"C:\Users\yangf\Desktop\Definition4.csv",engine='python')

#number of total patient in Q3
total_Patient = PatientID_Def4.shape[0]
PatientID_Def4 = PatientID_Def4[(PatientID_Def4["Meet_90_MME"] == 1)]
PatientID_Def4 = pd.merge(PatientID_Def4,overlap[['PatientID']],on='PatientID', how='inner')

#number of total patient meet the 90 MME per day threshold and have LASA overlap in Q3 for definition 2
total_Patient_overlap=PatientID_Def4.shape[0]

# percentage of patients meet the 90 MME per day threshold and have LASA overlap
Percentage_Def4=(total_Patient_overlap)/total_Patient*100

print(Percentage_Def4 , '% Of patients meet the 90 MME per day threshold and have LASA overlap under definition 4')
