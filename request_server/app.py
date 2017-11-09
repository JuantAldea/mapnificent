from flask import Flask, jsonify
from flask_cors import CORS
import json
import requests
from beaker.cache import CacheManager

cache = CacheManager()
app = Flask(__name__)
CORS(app)

@app.route("/sreality")
@cache.cache("sreality", expire=300)
def sreality():
    url="""https://www.sreality.cz/api/en/v2/estates? \
    building_condition=1|2|6|9\
    &category_main_cb=1\
    &category_sub_cb=3|4|5|6|7\
    &category_type_cb=2\
    &czk_price_summary_order2=0|20000\
    &furnished=1\
    &locality_district_id=5010|5009|5008|5005|5006|5007|5004|5003|5001|5002\
    &locality_region_id=10\
    &per_page=800\
    &tms=1510013276202\
    &usable_area=40|10000000000"""
    url = "https://www.sreality.cz/api/en/v2/estates?building_condition=1%7C2%7C6%7C9&category_main_cb=1&category_sub_cb=2%7C3%7C4%7C5%7C6%7C7&category_type_cb=2&czk_price_summary_order2=0%7C20000&locality_district_id=5001%7C5002%7C5004%7C5003%7C5005%7C5006%7C5007%7C5008%7C5009%7C5010&locality_region_id=10&per_page=999&tms=1510159751265&usable_area=45%7C10000000000"
    response = requests.get(url)
    json_response = response.json()
    urlmap = json.loads(open("urlmap.json").read())
    json_results = {}
    print(len(json_response['_embedded']['estates']))
    for idx, estate in enumerate(json_response['_embedded']['estates']):
        seo = estate['seo']
        estate_id = estate["hash_id"]
        gps = estate["gps"]
        
        estate_url = "https://www.sreality.cz/en/detail/{}/{}/{}/{}/{}".format( \
            urlmap["category_type_cb_detail"][str(seo["category_type_cb"])], \
            urlmap["category_main_cb_detail"][str(seo["category_main_cb"])], \
            urlmap["category_sub_cb"][str(seo["category_sub_cb"])], \
            seo["locality"], \
            estate_id)
        json_results[str(idx)]={"url": estate_url, "gps": gps}
    return jsonify(json_results)


@app.route("/bezrealiky")
@cache.cache("bezrealiky", expire=300)
def bezrealiky():
    headers = {
        'Pragma': 'no-cache',
        'Origin': 'https://www.bezrealitky.cz',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept': 'application/json, text/plain, */*',
        'Cache-Control': 'no-cache',
        'Referer': 'https://www.bezrealitky.cz/vyhledat',
        'Connection': 'keep-alive',
        'DNT': '1',
    }

    data = '{"action":"map","squares":"[\\"{\\\\\\"swlat\\\\\\":48,\\\\\\"swlng\\\\\\":12,\\\\\\"nelat\\\\\\":50,\\\\\\"nelng\\\\\\":16}\\",\\"{\\\\\\"swlat\\\\\\":50,\\\\\\"swlng\\\\\\":12,\\\\\\"nelat\\\\\\":52,\\\\\\"nelng\\\\\\":16}\\"]","filter":{"order":"time_order_desc","advertoffertype":"nabidka-pronajem","estatetype":["byt","dum"],"disposition":[],"ownership":"","equipped":"","priceFrom":null,"priceTo":null,"construction":"","description":"","surfaceFrom":"","surfaceTo":"","balcony":"","terrace":"","polygons":[[{"lat":50.241935486043715,"lng":14.192962646484375},{"lat":50.27266552996841,"lng":14.271240234375},{"lat":50.27003230289287,"lng":14.695587158203125},{"lat":50.26037589105958,"lng":14.780731201171875},{"lat":50.23930055989883,"lng":14.868621826171875},{"lat":50.18041592143885,"lng":14.929046630859375},{"lat":50.09856007224113,"lng":14.937286376953125},{"lat":50.01656412776064,"lng":14.920806884765625},{"lat":49.95033627078014,"lng":14.86724853515625},{"lat":49.91674601684011,"lng":14.788970947265625},{"lat":49.90171121726089,"lng":14.703826904296875},{"lat":49.90171121726089,"lng":14.621429443359375},{"lat":49.90171121726089,"lng":14.539031982421875},{"lat":49.90171121726089,"lng":14.445648193359375},{"lat":49.91055578459882,"lng":14.360504150390625},{"lat":49.92558782740072,"lng":14.27947998046875},{"lat":49.95828842806968,"lng":14.192962646484375},{"lat":50.0227407426766,"lng":14.129791259765625},{"lat":50.11001070896015,"lng":14.121551513671875},{"lat":50.191846980704504,"lng":14.143524169921875},{"lat":50.241935486043715,"lng":14.192962646484375},{"lat":50.241935486043715,"lng":14.192962646484375},{"lat":50.241935486043715,"lng":14.192962646484375}]]}}'
    
    response = requests.post('https://www.bezrealitky.cz/api/search/map', headers=headers, data=data)
    estates = response.json()['squares'][1]['records']

    json_results = {}
    for idx, estate in enumerate(estates):
        estate_url = "https://www.bezrealitky.cz/{}".format(estates[idx]['url'])
        estate_gps = {'lat': estates[idx]['lat'], 'lon' : estates[idx]['lng']}
        json_results[str(idx)] = {"url": estate_url, "gps" : estate_gps}
    return jsonify(json_results)


if __name__ == "__main__":

    app.run(debug=True)

