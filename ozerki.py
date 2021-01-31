import requests
import json
from bs4 import BeautifulSoup
import re

url = 'https://ozerki.ru/ajax/selectPharmacyPopup.php'

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
    'Cookie': 'BITRIX_SM_GUEST_ID=34873155; BITRIX_SM_LAST_VISIT=31.01.2021+21%3A24%3A02; BITRIX_SM_SALE_UID=489938618; IWEB_CITY=20237; SELECTED_CITY=' + str(y) +'; _ga_RH6LDE1WZ7=GS1.1.1612117074.5.1.1612117445.54; _ga=GA1.1.1697514696.1611903948; _userGUID=0:kkhxzq2g:qZ79DzjVQCrzUIElMIvKI3tPMWS_Dn_Y; flocktory-uuid=060dfc3b-b434-4bf7-8bde-4a39b1119c96-3; uxs_uid=6a4f0e20-6200-11eb-8fd7-cdf55085a791; uxs_mig=1; _ym_uid=1611903949565562368; _ym_d=1611903949; PHPSESSID=au1r3ultbd3lail8sc09m8d5k4; _gid=GA1.2.1717850241.1612091307; _ym_isad=2; dSesn=e2cd26db-a13d-5568-c163-8872f2d8a896; _dvs=0:kklgvscx:OaHA0FC1ru_RzYqbTt_cOo_SWjr60bma; _ym_visorc=w; _gat_UA-96845663-1=1'
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
    grid = soup.find('div', {'class': 'location__grid'})
    items = grid.find_all('a', {'class': 'location__item'})
    cities = []
    for item in items:
        cities.append({item['data-city-id']})
    return cities
    

def main ():
    cities = get_cities('https://ozerki.ru/')
    print(cities)
    
    reg_data=proc_ids(url,cities)
    
    o = open("oz.geojson", 'w')
    o.write(json.dumps(reg_data))
    o.close

if __name__ == '__main__':
    main()