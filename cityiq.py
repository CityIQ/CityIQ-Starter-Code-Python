import requests
import credentials
import base64
import json
import argparse
import time

class CityIq(object):
    # # Set up 
    def __init__(self, tenantName):
        try:
            self.tenant = credentials.credentials[tenantName]
        except KeyError:
            raise Exception("Tenant string specified is not in credentials.py")
        self.token = None
        self.assets = None
        self.locations = None
        self.events = None
        self.bbox = self.tenant["bbox"]
       
    def getTenantName(self):
        return self.tenant["name"]

    # # fetching token - only time to use UAA url 
    def fetchToken(self):
        headers = {'Authorization': 'Basic '+ (base64.b64encode(bytes(self.tenant["developer"], 'ascii'))).decode('ascii')}
        response = requests.request("GET", self.tenant["uaa"]+"/oauth/token?grant_type=client_credentials", headers=headers)
        self.token = response.json()["access_token"]
    
    def setToken(self, token):
        self.token = token

    def getToken(self):
        return self.token

    # # bbox set up * optional, can be an input to make manipulating large amounts of nodes easier
    def setBbox(self, bbox):
        self.bbox = bbox
    
    def getBbox(self):
        return self.bbox

    # # gets the assets or locations by the input parameter filters
    # # path must be "assets" OR "locations" 
    # # zone must be "parking", "traffic" "pedestrian" environment" "bicycle" - as seen in credentials.py 
    # # filterQ is optional but recommended: 
    # #     filterQ is the payload associated to q= in the params.  This can be :
    # #     "eventTypes:PKIN","eventTypes:PKOUT","eventTypes:PEDEVT", etc...
    # #     "assetType:NODE", "assetType:CAMERA", "assetType:ENV_SENSOR", etc...
    # # page is the page# you are querying (starting with 0)
    # # size is the number of assets to apppear on a page 
    def fetchMetadata(self, path, zone, filterQ=None, page=0, size=100):
        if self.token is not None:
            query = {
                "bbox":self.bbox, 
                "size": str(size),
                "page": str(page)
            }
            if filterQ is not None:
                query["q"] = filterQ 
            headers = {'Authorization': 'Bearer '+ self.token, 'Predix-Zone-Id': self.tenant[zone]}
            response = requests.request("GET", self.tenant["metadata"]+"/"+path+"/search", headers=headers, params=query)

            try:
                # assigns differently depending on if assets or locations
                if path == "assets":
                    self.assets = response.json()["content"]
                else :
                    self.locations = response.json()["content"]

                # informs of more metadata available
                if response.json()["totalElements"] > response.json()["numberOfElements"]:
                    print("More Metadata assets are available for this query.")
                    print("TotalElements: " + str(response.json()["totalElements"]) + ". Your specified size: " + str(response.json()["size"]))
            except:
                print("Error when fetching metadata")
                print(self.tenant["metadata"]+"/"+path+"/search")
                print(response,"\n\n")
            
            return response
        else:
            print("Token required to fetch metadata")

    def getAssets(self):
        return self.assets

    def getLocations(self):
        return self.locations
        

    # # fetches Events and saves to self.events
    # # path can be "assets" OR "locations"
    # # Uid is the assetUid or locationUid
    # # evType is the eventType as a string i.e. "PKIN"
    # # startTime is time since epoch in milliseconds
    # # endtime is time since epoch in milliseconds
    # # pageSize is the number of elements response is restricted to
    def fetchEvents(self, path, Uid, evType, startTime, endTime, pageSize=100):
        if self.token is not None:

            # set the zone based on eventType
            if evType == 'PKIN' or evType == 'PKOUT':
                zone = self.tenant["parking"]
            elif evType == 'TFEVT':
                zone = self.tenant["traffic"]
            elif evType == 'PEDEVT':
                zone = self.tenant["pedestrian"]
            elif evType == 'TEMPERATURE' or evType == 'PRESSURE' :
                zone = self.tenant["environment"]
            elif evType == 'BICYCLE':
                zone = self.tenant["bicycle"]
            else :
                print("Invalid event type")
                return 

            # set the query
            query = {
                "pageSize": str(pageSize),
                "eventType": evType,
                "startTime": startTime,
                "endTime": endTime
            }
            headers = {'Authorization': 'Bearer '+ self.token, 'predix-zone-id': zone}
            response = requests.request("GET", self.tenant["event"]+"/"+path+"/"+Uid+"/events", headers=headers, params=query)
            try:
                # sets the content to events
                self.events = response.json()["content"]
                details = response.json()["metaData"]
                # informs on pageSize exceeded
                if len(self.events) == int(pageSize):
                    print("There are a total of "+str(details["totalRecords"])+" events in this timeframe")
                    print("You are limiting your response to "+str(details["request_limit"])+" (pageSize)")

                return response
            except Exception as e:
                print("fetchEvents Failed")
                print(response)
                print(e)
                return response

    def getEvents(self):
        return self.events

# for testing purposes
def main(args):
    # use for testing, call above functions here to execute from command line
    return

# for testing purposes
def parse_args():
    '''parse args'''
    parser = argparse.ArgumentParser()
    # put your parser.add_arguments(..) here
    return parser.parse_args()

if __name__ == '__main__':
    main(parse_args())