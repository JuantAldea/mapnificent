#https://www.sreality.cz/en/detail/lease/flat/2+kt/praha-liben-na-uboci/272564572
import json
import requests

urlmap = json.loads(open("urlmap.json").read())

url = "https://www.sreality.cz/api/en/v2/estates?building_condition=1%7C2%7C6%7C9&category_main_cb=1&category_sub_cb=3%7C4%7C5%7C6%7C7&category_type_cb=2&czk_price_summary_order2=14000%7C14000&furnished=1&locality_district_id=5008&locality_region_id=10&per_page=20&tms=1509984156268&usable_area=40%7C10000000000"
response = requests.get(url)
json_response = r.json()

seo = json_response['_embedded']['estates'][0]['seo']
id =  json_response['_embedded']['estates'][0]['hash_id']

url = "https://www.sreality.cz/en/detail/" 
      + urlmap["category_type_cb_detail"][seo["category_type_cb"]] + "/" \
      + urlmap["category_main_cb_detail"][seo["category_main_cb"]] + "/" \
      + urlmap[seo["category_main_cb"]] + "/" \
      + id
