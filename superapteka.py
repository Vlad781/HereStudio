import requests
import json
from bs4 import BeautifulSoup
import re

url = 'https://superapteka.ru/ajax/selectPharmacyPopup.php'

def ToGeojson(data, dataGeojson):

  for d in data:
    geojson = {
			"type": "Feature",
			"properties" : {
			"pharmacyID": d["pharmacyID"],
		},
			"geometry" : {
			"type": "Point",
			"coordinates": [d["longitude"], d["latitude"]],
		}
		}
    dataGeojson.append(geojson)
  
  return dataGeojson


def proc_ids(url, ids):
  reg_data = None
  
  p_geojson = []
  print(ids)
    
  for reg_id in ids:
    # Change payload to get date for each region

    y = str(reg_id)  
    
    y = y[2:-2]
    print("SELECTED_CITY " + str(y))
    headers = {
    'Cookie': 'BITRIX_SM_GUEST_ID=901756; BITRIX_SM_LAST_VISIT=31.01.2021+14%3A26%3A13; BITRIX_SM_SALE_UID=61494420	; IWEB_CITY=20237; SELECTED_CITY=' + str(y) +    ';   PHPSESSID=9qelhda3dfmo1ln2evtpn4t4l5'
    }
    response = requests.post(url,cookies=headers)
      
    data = json.loads(response.text)

    data = data['COORDINATES_PHARMACIES']

      #Convert into geojson
    reg_data = ToGeojson(data, p_geojson)
    reg_data = {
        "type": "FeatureCollection",
        "features": reg_data
    }
    

  return reg_data

def get_cities (url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features='html.parser')
    grid = soup.find('div', {'class': 'city-select__city-items'})
    items = grid.find_all('a', {'class': 'city-select__link'})
    cities = []
    for item in items:
        cities.append({item['data-city-id']})
    return cities
    

def main ():
    cities = get_cities('https://superapteka.ru/')
    print(cities)
    
    reg_data=proc_ids(url,cities)
    
    o = open("super.geojson", 'w')
    o.write(json.dumps(reg_data))
    o.close

if __name__ == '__main__':
    main()