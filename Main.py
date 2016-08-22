# ----------------------------------------------------------------------
# AUTHOR        PHILIPPE ROULET
# CREATION DATE 04/08/2016
# IMPORTS CUSTOMER NAMES AND CITY FROM A FLAT FILE PROVIDED BY MARKETING
# IMPORTS ALL FRENCH CUSTOMER AND CITY NAMES FROM BI DB
# FOR EACH CUSTOMER AND CITY OF THE FLAT FILE, MATCH WITH THE MOST SIMILAR FROM SAP
# ----------------------------------------------------------------------
import difflib
from Modules import Functions as f
from Modules import Parameters as p

ZIPMatch = 0
CityMatch = 0
StreetMatch = 0
NoMatch = 0
ApproxMatch = 0
bestscore=0
MatchData = [[]]
#----------Loop through all companies--------
for company in p.companylist:
    # -----------Get SAP data----------
    SAPData = f.retrieveSAPdata(company)
    SAPData.pop(0)
    f.printmatrix (SAPData,2)
    if p.ExportSAPToFile==1:
        f.exportSAPtocsv(SAPData,company)

    # -----------Get MKT data----------
    MktData = f.retrievecompanydata(company)
    MktData.pop(0)
    f.printmatrix (MktData,2)

    # -----------Get Match data----------
    #-----------------Go through each record of the Mkt array and find the closest match in the SAP data-------
    #Loop through mkt data
    ZIPMatch = 0
    CityMatch = 0
    StreetMatch = 0
    NoMatch = 0
    for Mktindex in range(len(MktData)):
        Match = 0
        for SAPindex in range(len(SAPData)):
            # Check if the SAP ZIP matches the Mkt ZIP
            if SAPData[SAPindex][7] == MktData[Mktindex][4]:
                MatchData.append([MktData[Mktindex][0],  #Company
                                  MktData[Mktindex][1],  #Mkt agency code
                                  MktData[Mktindex][2],  #Mkt City
                                  MktData[Mktindex][4],  #Mkt ZIP
                                  SAPData[SAPindex][1],  #SAP Customer Code
                                  SAPData[SAPindex][2],  #SAP Customer Name
                                  SAPData[SAPindex][4],  #SAP City
                                  SAPData[SAPindex][6],  #SAP Street
                                  SAPData[SAPindex][7],  #SAp ZIP
                                  'ZIP'
                                  ])
                ZIPMatch += 1 #Augmented assignment: Rather than creating a new object and assigning that to the targer, the old object is modified instead. also it is evaluated only once
                Match = 1
                break

            # Check if the SAP norm city matches the Mkt norm city
            if SAPData[SAPindex][5] == MktData[Mktindex][3]:
                MatchData.append([MktData[Mktindex][0],  #Company
                                  MktData[Mktindex][1],  #Mkt agency code
                                  MktData[Mktindex][2],  #Mkt City
                                  MktData[Mktindex][4],  #Mkt ZIP
                                  SAPData[SAPindex][1],  #SAP Customer Code
                                  SAPData[SAPindex][2],  #SAP Customer Name
                                  SAPData[SAPindex][4],  #SAP City
                                  SAPData[SAPindex][6],  #SAP Street
                                  SAPData[SAPindex][7],  #SAp ZIP
                                  'City'
                                  ])
                CityMatch += 1
                Match = 1
                break

            # Check if the SAP norm street matches the Mkt norm city
            if SAPData[SAPindex][6] == MktData[Mktindex][3]:
                MatchData.append([MktData[Mktindex][0],  # Company
                              MktData[Mktindex][1],  # Mkt agency code
                              MktData[Mktindex][2],  # Mkt City
                              MktData[Mktindex][4],  # Mkt ZIP
                              SAPData[SAPindex][1],  # SAP Customer Code
                              SAPData[SAPindex][2],  # SAP Customer Name
                              SAPData[SAPindex][4],  # SAP City
                              SAPData[SAPindex][6],  # SAP Street
                              SAPData[SAPindex][7],  # SAp ZIP
                              'Street'
                              ])
                StreetMatch += 1
                Match = 1
                break

        #We are out of the SAP loop, if no match has been found, take most similar town name with reasonable score
        if Match==0:
            #Find nearest city name
            bestscore=0
            #print('mkt Norm City: ' + MktData[Mktindex][3])
            for SAPindex in range(len(SAPData)):
                #Get the difference between MktCity and SAPCity
                score =  f.stringmatch(MktData[Mktindex][3],SAPData[SAPindex][5])
                #If the score is better than the last best one, remember the SAP record
                if score>bestscore:
                    #print('   SAP Match Norm City:' + SAPData[SAPindex][5] + '- ' + str(score))
                    bestscore=score
                    SAPMatch=SAPData[SAPindex]
            #Out of the SAP loop, the match is reasonable, keep it
            if bestscore>p.threshold:
                MatchData.append([MktData[Mktindex][0],  # Company
                                  MktData[Mktindex][1],  # Mkt agency code
                                  MktData[Mktindex][2],  # Mkt City
                                  MktData[Mktindex][4],  # Mkt ZIP
                                  SAPMatch[1],  # SAP Customer Code
                                  SAPMatch[2],  # SAP Customer Name
                                  SAPMatch[4],  # SAP City
                                  SAPMatch[6],  # SAP Street
                                  SAPMatch[7],  # SAp ZIP
                                  'Approx city name'
                                  ])
                print('match:')
                print (SAPMatch)
                ApproxMatch += 1
                Match = 1
            bestscore = 0

            #If no nearest match
            if Match == 0:
                MatchData.append([MktData[Mktindex][0],  # Company
                                  MktData[Mktindex][1],  # Mkt agency code
                                  MktData[Mktindex][2],  # Mkt City
                                  MktData[Mktindex][4],  # Mkt ZIP
                                  '',  # SAP Customer Code
                                  '',  # SAP Customer Name
                                  '',  # SAP City
                                  '',  # SAP Street
                                  '',  # SAp ZIP
                                  'No Match'
                                  ])
                NoMatch += 1

#---------Clean up and print results--------
MatchData.pop(0)  # Remove the first empty line
f.printmatrix(MatchData, 10)
print ('ZIP Matches: ' + str(ZIPMatch))
print ('City Matches: ' + str(CityMatch))
print ('Street Matches: ' + str(StreetMatch))
print ('Approx Matches: ' + str(ApproxMatch))
print ('No Matches: ' + str(NoMatch))

#----------Export to csv--------------
f.exporttocsv(MatchData)





