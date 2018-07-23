# meraki-LH

import sys, csv, requests, getopt
import meraki
#print(sys.path)

def printhelp():
	# definir une fonction help qui décris le programme, arguments ...
	# l'argument doit avoir le .csv
	print('Under construction...')

# looks up org id for a specific 
# org name on failure returns 'null'
# Copied from github.com/meraki/automation-scripts
def getorgid(p_apikey, p_orgname):
	r = requests.get('https://dashboard.meraki.com/api/v0/organizations', headers={'X-Cisco-Meraki-API-Key': p_apikey, 'Content-Type': 'application/json'})
	
	if r.status_code != requests.codes.ok:
		return 'null'
	
	rjson = r.json()
	
	for record in rjson:
		if record['name'] == p_orgname:
			return record['id']
	return('null')

# This function return the list of networks that are specified in the file.
def readCsv(fileName):
	readNetworks = []
	with open(fileName) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			readNetworks.append(row)
		return(readNetworks)

# This function create the Network
def addNetwork(parameters):

	# Check all parameters are present 

	# retrieve the Organisation ID
	for parameter in parameters:
		orgid = getorgid('eec14f52ff0eac69260516253842f296ef9e0e2c',parameter['Organization'])
		print(orgid)



def main(argv): 

	#  python pourEssai.py -f <file name>

	#intialize variables for command line argument
	fileName = ''

	#get command line argument
	try:
		opts, args = getopt.getopt(argv,'f:')
	except getopt.GetoptError:
		printhelp()
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-f':
			fileName = arg

	networks = readCsv(arg)
	#print(networks[0]['Nom'])
	#print(len(networks))
	addNetwork(networks)

if __name__ == '__main__':
	main(sys.argv[1:])


