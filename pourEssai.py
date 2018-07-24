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

# coller ici la fonction getnwid

# This function return the list of networks that are specified in the file.
def readCsv(fileName):
	readNetworks = []
	with open(fileName) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			readNetworks.append(row)
		return(readNetworks)

# This function create the Network
def addNetwork(parameters, p_apikey):

	# Check all parameters are present 

	
	for parameter in parameters:
		# Retrieve the Organisation ID. If null print ERROR and exit	
		orgid = getorgid(p_apikey,parameter['Organization'])
		print(orgid)

		if orgid == 'null':
			print('ERROR: The Organization name provided does not exit')
			sys.exit(2)

		# Check if a network exits with the name provided. If yes, print ERROR and exit. Otherwise, create the network.
		checkIfExist = getnwid(p_apikey, p_orgid, p_nwname)
		if checkIfExist == 'null':
			print('ERROR: A network with the name %s already exists. Please choose another name' %p_nwname)
			sys.exit(2)
		else:
			# Create the Network
			



def main(argv): 

	#  python pourEssai.py -f <file name>

	#intialize variables for command line argument
	fileName = ''
	apiKey = ''

	#get command line argument. If the option provided is not part of available option, print help and exit
	try:
		opts, args = getopt.getopt(argv,'f:k:')
	except getopt.GetoptError:
		printhelp()
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-f':
			fileName = arg
		if opt == '-k':
			apiKey = arg

	networks = readCsv(arg)
	
	# Check if parameters provided in the CSV file are correct
	# faire ici une fonction qui vérifie les paramètres

	addNetwork(networks,apiKey)

if __name__ == '__main__':
	main(sys.argv[1:])


