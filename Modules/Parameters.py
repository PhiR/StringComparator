# ----------------------------------------------------------------------
# Generic VARIABLES
# ----------------------------------------------------------------------
# List that contains all companies that are being considered
# If that list changes, other changes have to be made
#   1. filedict to specify where the data file for the company is
#   2. wheredict to specify what the criteria is for extracting data from SAP for that company
#   3. retrievecompanydata to specify in what order the company code, zip code and city name is
companylist=['BRICORAMA']
#companylist=['BRICORAMA', 'CHAUSSON MATERIAUX', 'CASTORAMA', 'POINT P', 'BRICO DEPOT']

local = 1# 1=use local data, 0=Connect to DB and use network folders
threshold=0.8 # This is the mininum distance between mktCity and SAPCity acceptable to consider that we have a match

# ----------------------------------------------------------------------
# FILES VARIABLES
# ----------------------------------------------------------------------
if local==1:
    fichierRoot = R"C:\Users\P1890385\PycharmProjects\StringComparator\PricingAssitant\\"
else:
    fichierRoot = R"\\VFOXYZAPROD.za.if.atcsg.net\A97DFS-PlacoFrance_503-BI_PDF\DataImport\MatchingClient\PricingAssistant\\"

fichierBricorama = fichierRoot + R"bricorama_agency.csv"
fichierChausson = fichierRoot + R"chausson-materiaux_agency.csv"
fichierCastorama = fichierRoot + R"castorama_agency.csv"
fichierPointP = fichierRoot + R"pointp_agency.csv"
fichierBricoDepot = fichierRoot + R"bricodepot_agency.csv"
fichierSAPCustomers = fichierRoot + R"SAPCustomers_"
fichierMatch = fichierRoot + R"match.csv"

fichierDelimiter = ','
fichierHasHeader = 1  # If set to 1, the first line of the csv files will not be read

#A dictionary to hold a list of what file is attached to what company
filedict = {'BRICORAMA': fichierBricorama,
             'CHAUSSON MATERIAUX': fichierChausson,
             'CASTORAMA': fichierCastorama,
             'POINT P': fichierPointP,
             'BRICO DEPOT': fichierBricoDepot
             }

# ----------------------------------------------------------------------
# DB CONNECTION VARIABLES
# ----------------------------------------------------------------------
DBServer = 'SV000230.za.if.atcsg.net'
DBUser = 'TESTDTW'
DBPass = 'ALICANTE'
DB = 'SIGMA_BI'

ExportSAPToFile=0 #0=Do not export SAP data to file, 1=Export to file

# ----------------------------------------------------------------------
# SQL Parameters
# ----------------------------------------------------------------------
#Dictionary to match company names with Where clause
wheredict = {'BRICORAMA': " CUSTOMER_NAME_1 like '%BRICORAMA%';",
             'CHAUSSON MATERIAUX': " CUSTOMER_NAME_1 like '%CHAUSSON MATERIAUX%';",
             'CASTORAMA': " CUSTOMER_NAME_1 like '%CASTORAMA%';",
             'POINT P': " CUSTOMER_NAME_1 like '%POINT P%';",
             'BRICO DEPOT': " CUSTOMER_NAME_1 like '%BRICO DEPOT%';"
             }

#Base SQL Sentence to return Customer information
SQLbasesentence = "SELECT TOP 10000 CUSTOMER_ID, CUSTOMER_NAME_1, CITY, STREET, ZIP FROM DM_CUSTOMER_ORG_EMBI WHERE COUNTRY_ID='FR' AND "