# OralMorphineMilligramEquivalent
Using 4 Patient Daily MME definitions to calculate Patient Daily MME and answering the questions:


1.	What data quality check procedures would you take when calculating MMEs at the patient level? (Hint: what kind of data/record would be excluded from the sample?)

2.	Report the percentage of patients who meet the 90 MME per day threshold in 2019 Quarter 3 using the four definitions in the below example. Please write the code using SAS, R, or Python.
Please see the python code in the attachement file

3.	Report item 2 among patients who had overlapping Long-Acting (LA) and Short-Acting (SA) opioid prescriptions in 2019 Quarter 3.



Example: A patient receives 30mg extended-release oxycodone twice-a-day for around-the-clock pain for 30 days (#60), and one 5mg oxycodone twice a day as needed for breakthrough pain for 7 days (#14). Both prescriptions are dispensed on the first day of a 30-day month. No additional prescriptions are observed in the next 2 months. 

The numerator is total MME:
units x strength x conversion factor

For the first prescription this is 60 tablets x 30mg per tablet x 1.5 for a common conversion from morphine to oxycodone = 2,700 MME. The second prescription is 14 tablets x 5mg per tablet x 1.5 = 105 MME. The total is 2,805 MME. 

The person-time denominator to obtain average daily MME is what varies across research studies (following definition 1-3), and can have a dramatic effect on the interpretation of whether this is a high dose scenario (Daily MME >90). 

(1) Summing days supply
The sum of days supply: 30 + 7 = 37
2805 / 37 = 75.8 daily MME

(2) Accounting for overlap
Total days exposed accounting for overlap is 30 days.
2805/ 30 = 93.5 daily MME

(3) Defined observation window
In a study with 90-day observation windows the denominator would be 90.
2805 / 90 = 31.2 daily MME
With a 30-day window daily MME would be 93.5 MME. 

(4) Maximum daily MME
As written, the highest dose on any given day (on opioid medication) is (60mg + 10mg) x 1.5 = 105 maximum daily MME

Assuming you receive a file	The CDC_Oral_Morphine_Milligram_Equivalents_Sept_2018 file  provides details on how to calculate the Morphine Milligram Equivalents (MMEs) for opioid prescriptions (prescription level).

Assuming you receive a file containing prescription dispensation records in 2019 (prescription fill date in 2019) with the data structure as Table 1
Table 1. Prescription Dispensation Records
<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;}
.tg td{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  overflow:hidden;padding:10px 5px;word-break:normal;}
.tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
.tg .tg-0pky{border-color:inherit;text-align:left;vertical-align:top}
</style>
<table class="tg">
<thead>
  <tr>
    <th class="tg-0pky">&nbsp;&nbsp;&nbsp;<br>Column Name&nbsp;&nbsp;&nbsp;</th>
    <th class="tg-0pky">&nbsp;&nbsp;&nbsp;<br>Description&nbsp;&nbsp;&nbsp;</th>
    <th class="tg-0pky"></th>
    <th class="tg-0pky"></th>
    <th class="tg-0pky"></th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-0pky">&nbsp;&nbsp;&nbsp;<br>PatientID&nbsp;&nbsp;&nbsp;</td>
    <td class="tg-0pky">&nbsp;&nbsp;&nbsp;<br>Patient Identifier&nbsp;&nbsp;&nbsp;</td>
    <td class="tg-0pky"></td>
    <td class="tg-0pky"></td>
    <td class="tg-0pky"></td>
  </tr>
  <tr>
    <td class="tg-0pky">&nbsp;&nbsp;&nbsp;<br>NDC&nbsp;&nbsp;&nbsp;</td>
    <td class="tg-0pky">&nbsp;&nbsp;&nbsp;<br>National Drug Code&nbsp;&nbsp;&nbsp;</td>
    <td class="tg-0pky"></td>
    <td class="tg-0pky"></td>
    <td class="tg-0pky"></td>
  </tr>
  <tr>
    <td class="tg-0pky">&nbsp;&nbsp;&nbsp;<br>RxFillDate&nbsp;&nbsp;&nbsp;</td>
    <td class="tg-0pky">&nbsp;&nbsp;&nbsp;<br>Prescription Fill Date&nbsp;&nbsp;&nbsp;</td>
    <td class="tg-0pky"></td>
    <td class="tg-0pky"></td>
    <td class="tg-0pky"></td>
  </tr>
  <tr>
    <td class="tg-0pky">&nbsp;&nbsp;&nbsp;<br>RxDaysSupply&nbsp;&nbsp;&nbsp;</td>
    <td class="tg-0pky">&nbsp;&nbsp;&nbsp;<br>Prescription Days of Supply&nbsp;&nbsp;&nbsp;</td>
    <td class="tg-0pky"></td>
    <td class="tg-0pky"></td>
    <td class="tg-0pky"></td>
  </tr>
  <tr>
    <td class="tg-0pky">&nbsp;&nbsp;&nbsp;<br>Unit&nbsp;&nbsp;&nbsp;</td>
    <td class="tg-0pky">&nbsp;&nbsp;&nbsp;<br>Number of Units&nbsp;&nbsp;&nbsp;</td>
    <td class="tg-0pky"></td>
    <td class="tg-0pky"></td>
    <td class="tg-0pky"></td>
  </tr>
</tbody>
</table>


