# Please populate this file with your credentials provided by your city.  
credentials = {
    "City": { # city key is for clients with multiple tenant. it is recommended to leave the structure as is.
        "name" :"{yourCity}",
        "uaa": "https://auth.aa.cityiq.io",
        "metadata":"{yourMetaDataURL}",
        "event":"{yourEventServiceURL}",
        "websocket": "wss://{yourWebSocketURL}", 
        "developer": "{yourClientID}:{yourClientSecret}",
        "parking": "{yourParkingPredixZoneID}",
        "environment": "{yourEnvironmentPredixZoneID}",
        "pedestrian": "{yourPedestrianPredixZoneID}",
        "traffic": "{yourTrafficPredixZoneID}",
        "bbox": "{lat}:{long},{lat}:{long}"
    }
}