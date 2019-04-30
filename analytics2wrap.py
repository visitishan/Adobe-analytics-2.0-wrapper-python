# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 13:16:00 2019
@author: ishan.m.jain
"""

import requests
import json
import pandas as pd
from time import sleep


headers, auth_token, company_id, reporturl, y, y2, date_range = 0

def create_con(auth_token,company_id,client_id):
	global headers
	headers={'Authorization':'Bearer '+auth_token+'',
	'x-proxy-global-company-id':''+company_id +'',
	'x-api-key':''+client_id+'',
	'Accept': 'application/json',
	'Content-Type': 'application/json'}
	y = json.dumps(headers)
	global reporturl
	reporturl = "https://analytics.adobe.io/api/"+company_id+"/reports"



def find_id(response):
   dim = json.loads(response)
   rows = dim['rows']
   result_dict = {i["itemId"]:i["value"]  for i in rows}
   return result_dict



def get_item_id(element, date_range):
	global date_range
	element = '{"rsid":"'+company_id+'","globalFilters":[{"type":"dateRange","dateRange":"'+date_range+'"}],"metricContainer":{"metrics":[{"columnId":"0","id":"metrics/occurrences","sort":"desc"}]},"dimension":"variables/'+element+'","settings":{"countRepeatInstances":"true","limit":10000,"page":0},"statistics":{"functions":["col-max","col-min"]}}'
	y2 = json.dumps(element)
	element2  = requests.post(url = reporturl, headers = headers, data = element).text
	element2 = find_id(element2)
	return element2

