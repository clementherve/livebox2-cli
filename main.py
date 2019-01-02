#! /usr/bin/env python3

import requests as r
import json
import sys


#GLOBAL SCOPE
USERNAME = 'admin'
PASSWORD = 'admin'



###################################
### CONNECT TO THE LIVEBOX
###################################
def liveboxConnect():
	
	liveboxLogin = 'http://192.168.1.1/authenticate?username='+USERNAME+'&password='+PASSWORD
	payload = {"password":PASSWORD, "username":USERNAME}

	session = r.session()
	resp = session.post(liveboxLogin, data=payload)
	cookie = r.utils.dict_from_cookiejar(session.cookies)

	contextID = json.loads(resp.text)['data']['contextID']

	return {'session':session, 'contextID': contextID}



###################################
### CREATE HEADER
###################################

def header(ContextID):
	return {
		'X-Context':ContextID,
		'X-Prototype-Version':'1.7',
		'Content-Type':'application/x-sah-ws-1-call+json; charset=UTF-8',
		'Accept':'text/javascript'
		}



###################################
### CHECK WIFI STATUS
###################################

def wifiGetState(obj):
	url = 'http://192.168.1.1/sysbus/NeMo/Intf/lan:getMIBs'

	session = obj['session']
	contextID = obj['contextID']

	data = {
		'parameters':{"flag":"wlanvap","mibs":"base wlanvap","traverse":"down"},
		'method':'getMIBs',
		'service':'NeMo.Intf.lan'
		}

	resp = session.post(url, data=json.dumps(data), headers=header(contextID))
	jsonResp = json.loads(resp.text)
	enabledState = jsonResp['result']['status']['base']['wl0']['Status']
	
	return enabledState


###################################
### SET WIFI ENABLE STATE
###################################

def wifiSetState(state, obj):
	url = 'http://192.168.1.1/sysbus/NeMo/Intf/wl0:setWLANConfig'
	
	session = obj['session']
	contextID = obj['contextID']

	data = {
		"method":"setWLANConfig", 
		"service":"NeMo.Intf.wl0", 
		"parameters":{"mibs":{"penable":{"wifi0_ath":{"PersistentEnable":state,"Enable":state}}}}
		}
	resp = session.post(url, data=json.dumps(data), headers=header(contextID))


###################################
### UI
###################################
def userInterface():
	obj = liveboxConnect()
	print('**Livebox Connected **')
	state = wifiGetState(obj)

	if state:
		print('[wifi]: ENABLED')
		user = input('Desactivate? [y/n] ')
		if user == 'y':
			wifiSetState(False, obj)
	else:
		print('[wifi]: DISABLED')
		user = input('Activate? [y/n] ')
		if user == 'y':
			wifiSetState(True, obj)





userInterface()
