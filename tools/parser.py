import json
import requests
from pprint import pprint as pp

urlmap = json.loads(open("urlmap.json").read())
#url = "https://www.sreality.cz/api/en/v2/estates?building_condition=1%7C2%7C6%7C9&category_main_cb=1&category_sub_cb=3%7C4%7C5%7C6%7C7&category_type_cb=2&czk_price_summary_order2=14000%7C14000&furnished=1&locality_district_id=5008%7C5001%7C5002%7C5003%7C5004&locality_region_id=10&per_page=20&tms=1509986269244&usable_area=40%7C10000000000"
url = "https://www.sreality.cz/api/en/v2/estates?building_condition=1%7C2%7C6%7C9&category_main_cb=1&category_sub_cb=3%7C4%7C5%7C6%7C7&category_type_cb=2&czk_price_summary_order2=14000%7C14000&furnished=1&locality_district_id=5008&locality_region_id=10&per_page=400&tms=1509984156268&usable_area=40%7C10000000000"
url = "https://www.sreality.cz/api/en/v2/estates?building_condition=1%7C2%7C6%7C9&category_main_cb=1&category_sub_cb=3%7C4%7C5%7C6%7C7&category_type_cb=2&czk_price_summary_order2=0%7C20000&locality_district_id=5002%7C5001%7C5003%7C5004%7C5007%7C5006%7C5005%7C5008%7C5009%7C5010&locality_region_id=10&per_page=800&tms=1510009970911&usable_area=40%7C10000000000"
#furnished
url="https://www.sreality.cz/api/en/v2/estates?building_condition=1%7C2%7C6%7C9&category_main_cb=1&category_sub_cb=3%7C4%7C5%7C6%7C7&category_type_cb=2&czk_price_summary_order2=0%7C20000&furnished=1&locality_district_id=5010%7C5009%7C5008%7C5005%7C5006%7C5007%7C5004%7C5003%7C5001%7C5002&locality_region_id=10&per_page=800&tms=1510013276202&usable_area=40%7C10000000000"
response = requests.get(url)
json_response = response.json()
json_results = {}
for idx, estate in enumerate(json_response['_embedded']['estates']):
	seo = estate['seo']
	estate_id = estate["hash_id"]
	gps = estate["gps"]
	#https://www.sreality.cz/en/detail/lease/flat/2+kt/praha-liben-na-uboci/272564572
	estate_url = "https://www.sreality.cz/en/detail/{}/{}/{}/{}/{}".format( \
		urlmap["category_type_cb_detail"][str(seo["category_type_cb"])], \
		urlmap["category_main_cb_detail"][str(seo["category_main_cb"])], \
		urlmap["category_sub_cb"][str(seo["category_sub_cb"])], \
		seo["locality"], \
		estate_id)
	json_results[str(idx)]={"url": estate_url, "gps": gps}
#	print("{} -> {}".format(gps, estate_url))
print("var estates_data = {};".format(json.loads(json.dumps(json_results))))




