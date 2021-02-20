import clipboard

import requests
import time
import math
import re

KEY = open("key","r").read()

regex = r'^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)(,| )\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$'
last = ""

def get_response(coords: str):
    url = f"https://maps.googleapis.com/maps/api/elevation/json?locations={coords}&key={KEY}"

    request = requests.get(url)
    
    return request.json()
    
def get_slope(x, y, radius: int = 10, resolution: int = 300) -> float:
    """Get the "instantaneous" slope at given coordinate x, y.
    
        x: longitudinal coordinate
        y: latitudinal coordinate
        diameter: Distance between center point and outside points (meters)
        resolution: Number of points to check for around the x, y (maximum 377)
        
    """
    
    one_degree_to_meters = 111198.94090183832
    
    radius_in_coords = radius / one_degree_to_meters
    points = [(math.cos(2*math.pi/resolution*x)*radius_in_coords,math.sin(2*math.pi/resolution*x)*radius_in_coords) for x in range(0,resolution+1)]
    final = [(x+xd, y+yd) for xd, yd in points]
    with open("lmaoooo","w") as f:
        for point, point2 in points:
            f.write(f"{point:.20f},{point2:.20f}\n")

    link_list = ""
    for x, y in final:
        link_list += f"{str(x)},{str(y)}|"
    link_list = link_list[:-1]

    link = f"https://maps.googleapis.com/maps/api/elevation/json?locations={link_list}&key={KEY}"
    req = requests.get(link)
    data = req.json()

    results = data["results"]
    elevations = {(x["elevation"], (x["location"]["lat"], x["location"]["lng"])) for x in results}

    maximum = max(elevations)
    minimum = min(elevations)

    x1, y1 = maximum[1]
    x2, y2 = minimum[1]
    
    # Pythagorean Theorum
    distance = math.sqrt((x2-x1)**2 + (y2-y1)**2) * one_degree_to_meters
    deg = math.degrees(math.atan((maximum[0] - minimum[0]) / distance))

    return deg

def main():
    global last
    
    get_clipboard = clipboard.paste()
    last = get_clipboard
    
    if r := re.match(regex, get_clipboard):
        elevation = get_response(get_clipboard)

        resp = elevation["results"][0]["elevation"]
        res = round(elevation["results"][0]["resolution"]*3.28084, 2)
        meters = round(resp, 2)
        feet = round(meters * 3.28084, 2)
        
        x, y = (float(i) for i in get_clipboard.split(","))
        slope = round(get_slope(x, y), 1)
        
        link = f"https://maps.googleapis.com/maps/api/geocode/json?&latlng={get_clipboard}&components=formatted_address&key={KEY}"
        geo_req = requests.get(link)
        geo_res = geo_req.json()

        try:
            address = geo_res["results"][0]["formatted_address"]
        except IndexError:
            address = "No address found"

        message = f"""
Coordinates:
    {get_clipboard}
Address:
    {address}
Elevation:
    {feet} ft
Slope:
    {slope}°
"""
        print(message)
    

    
if __name__ == '__main__':
    while True:
        now = clipboard.paste()

        if now != last:
            main()

        time.sleep(.1)
        