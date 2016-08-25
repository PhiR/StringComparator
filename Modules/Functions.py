import string
import re
import pymssql
import csv
import difflib
from Modules import Parameters as p

# ----------------------------------------------------------------------
# Test 2 blaldsqjhkjhk
# printmatrix
# Prints the first n records of a 2D array row by row
# If n is greater than the length of the matrix, prints all the recoirds of the array
# if n=0, print the whole matrix
# ----------------------------------------------------------------------
def printmatrix(matrix,n):
    print ('Matrix of ' + str(len(matrix)) + ' elements')
    max = n
    if n > len(matrix) or n==0:
        max=len(matrix)

    print ('---------------------------')
    for i in range(max):
        print(matrix[i])

# ----------------------------------------------------------------------
# normalize
# Removes special characters from a string
# ----------------------------------------------------------------------
def normalize(s):
    # remove punctuation and replace by space
    for p in string.punctuation:
        s = s.replace(p, ' ')

    # Get rid of encoding issues
    s = s.replace('Ã®', 'î')
    s = s.replace('Ã©', 'é')
    s = s.replace('Ã©', 'ê')

    # Get of special characters
    s = s.replace('à', 'a')
    s = s.replace('â', 'a')
    s = s.replace('é', 'e')
    s = s.replace('è', 'e')
    s = s.replace('ê', 'e')
    s = s.replace('ë', 'e')
    s = s.replace('î', 'i')
    s = s.replace('ï', 'i')
    s = s.replace('ô', 'o')
    s = s.replace('ù', 'u')
    s = s.replace('û', 'u')
    s = s.replace('ç', 'ç')

    # CHANGE ABBREVIATIONS AND COMMON STRINGS
    s = s.replace('l ', ' ')
    s = s.replace('le ', ' ')
    s = s.replace('les ', ' ')
    s = s.replace('& ', ' et ')
    s = s.replace('saint ', 'st ')
    s = s.replace('sur ', 's ')
    s = s.replace('cedex ', ' ')
    s = s.replace('sarl ', ' ')
    s = s.replace(' sarl', ' ')
    s = s.replace(' s a r l', ' ')
    s = s.replace('eurl ', ' ')
    s = s.replace(' eurl', ' ')
    s = s.replace(' e u r l', ' ')
    s = s.replace('sas ', ' ')
    s = s.replace(' sas', ' ')
    s = s.replace(' s a s', ' ')
    s = s.replace('sa ', ' ')
    s = s.replace('s a ', ' ')

    # Remove double spaces
    s = re.sub(' +', ' ', s)

    # Make it lower case and get rid of spaces at the beginning and end
    return s.lower().strip()

# ----------------------------------------------------------------------
# retrieveSAPdata
# The city is normalized and has the company name removed from it
# ----------------------------------------------------------------------
def retrieveSAPdata(company):
    if p.local==0:
        connSel = pymssql.connect(server=p.DBServer, user=p.DBUser, password=p.DBPass, database=p.DB)
        cursorSel = connSel.cursor()
        print('Read SAP data from DB')
        if company in p.wheredict.keys():
            whereclause = p.wheredict[company]
        else:
            whereclause = " CUSTOMER_NAME_1 like '%" + company + "%';"
        SQLsentence = p.SQLbasesentence + whereclause
        cursorSel.execute(SQLsentence)
    else:
        print('Read SAP data from file')
        csvfile = open(p.fichierSAPCustomers+company+'.csv', newline='')
        cursorSel = csv.reader(csvfile, delimiter=';', quotechar='|')

    # ----------------------RETRIEVE DATA FROM SQL SERVER--------------------
    #row = cursorSel.fetchone()
    SapData = [[]]
    #while row:
    for row in cursorSel:
        print(row)
        SapCode = str(row[0])
        SapName = str(row[1])
        SapCity = str(row[2])
        SapStreet = str(row[3])
        SapZIP = str(row[4])
        SapNormName = normalize(SapName)
        SapNormCity = normalize(SapCity)
        SapNormCity = SapNormCity.replace(normalize(company), '').strip()

        SapNormStreet = normalize(SapStreet)
        SapNormStreet = SapNormStreet.replace(normalize(company), '').strip()

        SapData.append([company, SapCode, SapName, SapNormName, SapCity, SapNormCity, SapNormStreet,SapZIP])

        #row = cursorSel.fetchone()
    SapData.pop(0)  # Remove the first empty line

    # Close Connections if needed
    if p.local==0:
        cursorSel.close()
        connSel.close()
    else:
        csvfile.close()

    return SapData

# ----------------------------------------------------------------------
# exportSAPtocsv
# Exports Matchdata to csv
# ----------------------------------------------------------------------
def exportSAPtocsv(SAPData, company):
    with open(p.fichierSAPCustomers+company+'.csv', 'w') as mycsvfile:
        thedatawriter = csv.writer(mycsvfile,delimiter=';', lineterminator='\n')
        thedatawriter.writerow(['SapCode','SapName','SapCity','SapStreet','SapZIP'])
        for row in SAPData:
            thedatawriter.writerow([row[1],row[2],row[4],row[6],row[7]])

# ----------------------------------------------------------------------
# retrievecompanydata
# Retrieves company data from one of the marketing files
# The normalized name has the company name removed from it
# ----------------------------------------------------------------------
def retrievecompanydata(company):
    # -------------------RETRIEVE POINT P FILE AND STORE RAW AND NORMALIZED DATA IN AN ARRAY--------------
    # https://docs.python.org/2/library/csv.html
    HeaderRow = 1
    companyData = [[]]
    with open(p.filedict[company], newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=p.fichierDelimiter, quotechar='|')
        for row in spamreader:
            #All files have a different structure, we need to look for each data element in a different column depending on the company
            if company=='BRICORAMA':
                MktCode = str(row[1])
                MktName = str(row[2])
                MktZip = str(row[0])

            if company == 'CASTORAMA':
                MktCode = str(row[0])
                MktName = str(row[2])
                MktZip = str(row[1])

            if company in ['CHAUSSON MATERIAUX','POINT P']:
                MktCode = str(row[0])
                MktName = str(row[1])
                MktZip = str(row[2])

            if company=='BRICO DEPOT':
                MktCode = str(row[0])
                MktName = str(row[1])
                MktZip = ''

            MktNormName = normalize(MktName)
            MktNormName = MktNormName.replace(normalize(company), '').strip()
            if not (p.fichierHasHeader == 1 & HeaderRow == 1):  # Skip the first row if required
                companyData.append([company,MktCode, MktName, MktNormName, MktZip])
            HeaderRow = 0
    companyData.pop(0)  # Remove the first empty line
    return companyData

# ----------------------------------------------------------------------
# exporttocsv
# Exports Matchdata to csv
# ----------------------------------------------------------------------
def exporttocsv(MatchData):
    with open(p.fichierMatch, 'w') as mycsvfile:
        thedatawriter = csv.writer(mycsvfile,delimiter=';', lineterminator='\n')
        thedatawriter.writerow(['Enseigne','MktCode','MktName','MktZip','SAPCode','SAPName','SAPCity','SAPStreet','SAPZip','MatchCriteria'])
        for row in MatchData:
            thedatawriter.writerow(row)

# ----------------------------------------------------------------------
# stringmatch
# Returns the distance between string1 & string2
# If string1 is included
# ----------------------------------------------------------------------
def stringmatch(string1, string2):
    #Check if string1 and string2 are included in each other, return 1 if they are
    # words = string1.split()
    # for word in words:
    #     if word in string2 and len(word)>1:
    #         return 1
    if len(string1)==0 or len(string2)==0:
        return 0
    if string1 in string2:
        return 1
    if string2 in string1:
        return 1
    #otherwise return the difference between them
    return difflib.SequenceMatcher(None, string1, string2).ratio()