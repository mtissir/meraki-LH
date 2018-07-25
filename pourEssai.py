# meraki-LH

import sys, csv, requests, getopt, json
import meraki
#print(sys.path)

def printhelp():
	# definir une fonction help qui décris le programme, arguments ...
	# l'argument doit avoir le .csv
	print('Under construction...')

	
#looks up network id for a network name
#on failure returns 'null'
#copied and modified from github.com/meraki/automation-scripts	
def getnwid(p_apikey, p_orgid, p_nwname):


	r = requests.get('https://dashboard.meraki.com/api/v0/organizations/%s/networks' % p_orgid, headers={'X-Cisco-Meraki-API-Key': p_apikey, 'Content-Type': 'application/json'})
	
	if r.status_code != requests.codes.ok:
		return 'null'
	
	rjson = r.json()
	
	for record in rjson:
		if record['name'] == p_nwname:
			return record['id']
	return('null') 		
	
# looks up org id for a specific 
# org name on failure returns 'null'
# Copied from github.com/meraki/automation-scripts
def getorgid(p_apikey, p_orgname):
	print(p_apikey)
	r = requests.get('https://api.meraki.com/api/v0/organizations', headers={'X-Cisco-Meraki-API-Key': p_apikey, 'Content-Type': 'application/json'})
	rjson = r.json()
	print(rjson)

	if r.status_code != requests.codes.ok:
		return 'null'
		
	for record in rjson:
		if record['name'] == p_orgname:
			return record['id']
	return('null')

def createNw(p_apikey, orgid, tz, tags, name, p_type):
	
	r = requests.post('https://dashboard.meraki.com/api/v0/organizations/%s/networks' %orgid, data=json.dumps({'timeZone': tz, 'tags': tags, 'name': name, 'type': p_type}), headers={'X-Cisco-Meraki-API-Key': p_apikey, 'Content-Type': 'application/json'})
	print(r.status_code)
	
	rjson = r.json()

	if r.status_code == 201 :
		print('Network %s created' %parameter['Name'])
		ntwId = rjson['id'] #Store the id of newly created network for coming API calls
		print('New network ID: %s' %ntwId)
		return(ntwId)

	else : 
		print('Network %s creation failed:' %parameter['Name'])
		print(r.content)
		return('null')

def addVlan(p_apikey, ntwId, vlanSubnet, applianceIP, vlanID, vlanName):

	paramData = {'id': vlanID, 'name': vlanName, 'subnet': vlanSubnet, 'applianceIP': applianceIP}
	print(paramData)
	paramData = json.dumps(paramData)

	r = requests.post('https://dashboard.meraki.com/api/v0/networks/%s/vlans' %ntwId, data=paramData, headers={'X-Cisco-Meraki-API-Key': p_apikey, 'Content-Type': 'application/json'})

	if r.status_code == 201 :
		print('Vlan %s created' vlanSubnet)
		return(vlanID)

	else : 
		print('Vlan %s creation failed:' vlanSubnet)
		print(r.content)
		return('null')

def updateVlan(p_apikey, ntwId, vlanSubnet, applianceIP, vlanID, vlanName)


# This function return the parameters that are specified in the file.
def readCsv(fileName):
	readNetworks = []
	with open(fileName) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			readNetworks.append(row)
		return(readNetworks)

# This function create the Network
def addNetwork(parameters, p_apikey):

	# Check all parameters are present. Faire ici une fonction qui regarde les paramètres

	for parameter in parameters:
		# Retrieve the Organisation ID. If null print ERROR and exit	
		orgid = getorgid(p_apikey,parameter['Organization'])
	
		if orgid == 'null':
			print('ERROR: The Organization %s provided does not exit' %parameter['Organization'])
			sys.exit(2)

		# Check if a network exits with the name provided. If yes, print ERROR and exit. Otherwise, create the network.
		checkIfExist = getnwid(p_apikey, orgid, parameter['Name'])
		if checkIfExist != 'null':
			print('ERROR: A network with the name %s already exists. Network not created' %p_nwname)
			continue
		
		# Create the Network
		ntwId = createNw(p_apikey, orgid, parameter['TimeZone'], parameter['Tag'], parameter['Name'], 'appliance')

		if ntwId == 'null' :
			continue

		#Update Default VLAN


		#Add a VLAN
		#vlan = addVlan(p_apikey, ntwId, parameter['LocalSubnet'], parameter['MX_IP'] , vlanID, vlanName):	


		#Update VPN settings
		SagamuID = getnwid(p_apikey, orgid, 'EMEA-NG-Sagamu')
		AshakaID = getnwid(p_apikey, orgid, 'EMEA-NG-Ashaka')

		print(SagamuID)
		print(AshakaID)

		hubs = []
		hubs.append({'hubId': SagamuID, 'useDefaultRoute': True})
		hubs.append({'hubId': AshakaID, 'useDefaultRoute': True})


		subnets = []
		subnets.append({'localSubnet': parameter['LocalSubnet'],'useVpn': True})

		paramData = {'mode': 'spoke', 'hubs': hubs, 'subnets':subnets}
		print(paramData)
		paramData = json.dumps(paramData)

		r = requests.put('https://dashboard.meraki.com/api/v0/networks/%s/siteToSiteVpn' %ntwId, data=paramData, headers={'X-Cisco-Meraki-API-Key': p_apikey, 'Content-Type': 'application/json'})

		#print(r)
		#print(r.json())
		print(r.status_code)
		if r.status_code == requests.codes.ok :
			print('VPN Settings for the Network %s have been updated' %parameter['Name'])

		else : 
			print('Update of VPN setting for Network %s failed. This step will be ignored' %parameter['Name'])
			print(r)
			print(r.json())
			continue



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
			networks = readCsv(arg)
		if opt == '-k':
			apiKey = arg
			print(apiKey)

	# Check if parameters provided in the CSV file are correct
	# faire ici une fonction qui vérifie les paramètres

	addNetwork(networks,apiKey)

if __name__ == '__main__':
	main(sys.argv[1:])


