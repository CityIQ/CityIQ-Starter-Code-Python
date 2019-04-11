# # Run $ python3 demo.py in your command line and see events within the last specified timeframe (see startTime and endTime)
from cityiq import CityIq
import time
import json

# set time frame for use when querying for events (epoch time in milliseconds)
endTime = int(time.time())*1000 # time when demo.py is run
startTime = endTime-(12*3600000) 

print("====================================================================================")
print('initiating demo')

print("Getting the token")
myCIQ = CityIq("SD")
myCIQ.fetchToken()

print("====================================================================================")
print("++++++++++Getting Parking Data++++++++++++")

print("Getting Parking Metadata")
# gettting assets - assets with PKIN events, page 0 with 10 assets per page
print("Getting Assets")
myCIQ.fetchMetadata("assets","parking","eventTypes:PKIN",page=0, size=10)
assets = myCIQ.getAssets()
# set a random asset in the list for future use
randAssetUid = assets[0]["assetUid"]

print("-------------------------------------------")
print("Get events for assetUid "+randAssetUid)
# getting events
myCIQ.fetchEvents("assets", randAssetUid, "PKIN", startTime, endTime, pageSize=1)
assetEvents = myCIQ.getEvents()
# printing events
print(json.dumps(assetEvents,indent=4,sort_keys=True))
# save a random locationUid for event querying to follow
randLocationUid = assetEvents[0]["locationUid"]

print("-------------------------------------------")
print("Get events for locationUid "+randLocationUid)
# getting events
myCIQ.fetchEvents("locations", randLocationUid, "PKIN", startTime, endTime, pageSize=1)
locationEvents = myCIQ.getEvents()
print(json.dumps(locationEvents,indent=4,sort_keys=True))

print("====================================================================================")
print("++++++++++Getting Traffic Data++++++++++++")

print("Getting Traffic Metadata")
# gettting assets - assets with TFEVT events, page 0 with 10 assets per page
print("Getting Assets")
myCIQ.fetchMetadata("assets","traffic","eventTypes:TFEVT",page=0, size=10)
assets = myCIQ.getAssets()
# set a random asset in the list for future use
randAssetUid = assets[0]["assetUid"]

print("-------------------------------------------")
print("Get events for assetUid "+randAssetUid)
# getting events
myCIQ.fetchEvents("assets", randAssetUid, "TFEVT", startTime, endTime, pageSize=1)
assetEvents = myCIQ.getEvents()
# printing events
print(json.dumps(assetEvents,indent=4,sort_keys=True))


print("====================================================================================")
print("++++++++++Getting Pedestrian Data++++++++++++")

print("Getting Pedestrian Metadata")
# gettting assets - assets with PEDEVT events, page 0 with 10 assets per page
print("Getting Assets")
myCIQ.fetchMetadata("assets","pedestrian","eventTypes:PEDEVT",page=0, size=10)
assets = myCIQ.getAssets()
# set a random asset in the list for future use
randAssetUid = assets[0]["assetUid"]

print("-------------------------------------------")
print("Get events for assetUid "+randAssetUid)
# getting events
myCIQ.fetchEvents("assets", randAssetUid, "PEDEVT", startTime, endTime, pageSize=1)
assetEvents = myCIQ.getEvents()
# printing events
print(json.dumps(assetEvents,indent=4,sort_keys=True))


print("====================================================================================")
print("++++++++++Getting Environmental Data++++++++++++")

print("Getting Environmental Metadata")
# gettting assets - assets with Humidity events, page 0 with 10 assets per page
print("Getting Assets")
myCIQ.fetchMetadata("assets","environment","eventTypes:HUMIDITY",page=0, size=10)
assets = myCIQ.getAssets()
# set a random asset in the list for future use
randAssetUid = assets[0]["assetUid"]

print("-------------------------------------------")
print("Get events for assetUid "+randAssetUid)
# getting events
myCIQ.fetchEvents("assets", randAssetUid, "HUMIDITY", startTime, endTime, pageSize=1)
assetEvents = myCIQ.getEvents()
# printing events
print(json.dumps(assetEvents,indent=4,sort_keys=True))


