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




###############################################################################
#   To create breakdown payload. Call with specific dimention key. Example -
#
#   "metricFilters":[
#   {"id":"0","type":"breakdown","dimension":"variables/campaign.2","itemId":"'+each_campaign2+'"},
#   {"id":"1","type":"breakdown","dimension":"variables/campaign.4","itemId":"'+ each_campaign4+'"},
#   {"id":"2","type":"breakdown","dimension":"variables/evar10","itemId":"'+ each_evar10+'"},
#   {"id":"3","type":"breakdown","dimension":"variables/mobiledevicetype","itemId":"'+ device+'"},
#   {"id":"4","type":"breakdown","dimension":"variables/daterangemonth","itemId":"'+ each_month+'"}
#   ]},
#
###############################################################################
a = 0
mid = ""
def create_breakdowns(dimention, dimention_item):
    prefix = '''"metricFilters":['''
    mid = mid + '''{"id":"'''+a+'''","type":"breakdown","dimension":"variables/'''+dimention+'''","itemId":"'''+dimention_item+'''"},'''
    a=a+1
    end = ''']},'''
    breakdownpayload = prefix+mid+end
    
    #for metrics and filters - "filters":["0","1","2","3","4"]} part
    metric_filter_count_list = []
    for i in range(a):
        metric_filter_count_list.append(str(i))
   
    return(breakdownpayload)





###############################################################################
#   To create metric and filter payload. Example - 
#
#   "metricContainer":{"metrics":[
#   {"columnId":"0","id":"metrics/visits","sort":"desc","filters":["0","1","2","3","4"]},
#   {"columnId":"1","id":"metrics/visitors","filters":["0","1","2","3","4"]},
#   {"columnId":"2","id":"metrics/pageviews","filters":["0","1","2","3","4"]},
#   {"columnId":"3","id":"cm_pageviews_visit_defaultmetric","filters":["0","1","2","3","4"]},
#   {"columnId":"4","id":"cm1077_589d9cdd7245ec2f0d4ed931","filters":["0","1","2","3","4"]},
#   {"columnId":"5","id":"metrics/event7","filters":["0","1","2","3","4"]},
#   ],
#
###############################################################################

    
b = 0
metric_mid = ""
def create_metric_and_filters(metric):
    metric_prefix = '''"metricContainer":{"metrics":['''
    metric_mid = metric_mid + '''{"columnId":"'''+b+'''","id":"metrics/'''+metric+'''","sort":"desc","filters":'''+metric_filter_count_list+'''},'''
    b=b+1
    metric_end = '''],'''
    final_metric = metric_prefix + metric_mid + metric_end
    return(final_metric)

    
    


###############################################################################
#   To create a final payload that will be sent to the API for data. 
###############################################################################

def create_final_payload(global_company_id,date_range, last_breakdown):
    final_start = '''{"rsid":"'''+global_company_id+'''","globalFilters":[{"type":"dateRange","dateRange":"'''+date_range+'''"}],'''
    final_end = '''"dimension":"variables/'''+last_breakdown+'''","settings":{"countRepeatInstances":true,"limit":1000,"page":0},"statistics":{"functions":["col-max","col-min"]}}'''
    final_payload = final_start + final_metric + breakdownpayload + final_end
    return(final_payload)


    
    
    
    
    
    