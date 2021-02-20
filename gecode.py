import clipboard

import requests
import time
import math
import re


regex = r'^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)(,| )\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$'
last = ""
from pprint import pprint

def main():
    global last
    
    get_clipboard = clipboard.paste()
    last = get_clipboard
    
    if re.match(regex, get_clipboard):        
        geo_req = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?&latlng={get_clipboard}&components=formatted_address&key=AIzaSyCgaM66LrgRfqGOhLuj695Gux6I4jBuNBI")
        geo_res = geo_req.json()
        try:
            address = geo_res["results"][0]["formatted_address"]
        except IndexError:
            address = "No address found"
        pprint(address)
        message = f"""
Address:
    {address}
"""
        # print(message)
    

    
if __name__ == '__main__':
    while True:
        now = clipboard.paste()

        if now != last:
            main()

        time.sleep(.1)
        