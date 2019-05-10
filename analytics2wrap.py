# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 13:16:00 2019
@author: ishan.m.jain
"""

import requests
import json
import pandas as pd
from time import sleep


#headers, auth_token, company_id, reporturl, y, y2
dimentionlist = []
dataframelist = []


#####################################################################
#	To create connection to the API. 
#	Call with auth token, company id, and client id in parameters
#####################################################################
def create_con(auth_token,company_id,client_id):
    global headers
    headers={'Authorization': auth_token,
    'x-proxy-global-company-id':''+company_id +'',
    'x-api-key':''+client_id+'',
    'Accept': 'application/json',
    'Content-Type': 'application/json'}
    y = json.dumps(headers)
    global reporturl
    reporturl = 'https://analytics.adobe.io/api/'+company_id+'/reports'
    return headers, reporturl


def find_id(response):
   dim = json.loads(response)
   rows = dim['rows']
   result_dict = {i["itemId"]:i["value"]  for i in rows}
   return result_dict


#####################################################################
#	To get item id of a dimention 
#	Call with dimention name and date range in parameters
#	Date range format = 2019-03-01T00:00:00.000/2019-04-01T00:00:00.000
#	The function returns the dimention and item ids in a dictionary
#####################################################################
def get_item_id(element, date_range, global_company_id):
    element = '{"rsid":"'+global_company_id+'","globalFilters":[{"type":"dateRange","dateRange":"'+date_range+'"}],"metricContainer":{"metrics":[{"columnId":"0","id":"metrics/occurrences","sort":"desc"}]},"dimension":"variables/'+element+'","settings":{"countRepeatInstances":"true","limit":10000,"page":0},"statistics":{"functions":["col-max","col-min"]}}'
    #print(element)
    y2 = json.dumps(element)
    element2  = requests.post(url = reporturl, headers = headers, data = element).text
    #print(element2)
    element2 = find_id(element2)
    dimentionlist.append(element2)
    return element2


