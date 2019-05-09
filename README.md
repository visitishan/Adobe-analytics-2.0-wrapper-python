# Adobe-analytics-2.0-wrapper-python
Python wrapper for the Adobe analytics API 2.0

### To generate OAuth Access token -
Refer video tutorials - https://www.youtube.com/watch?v=lrg1MuVi0Fo 
And - https://www.youtube.com/watch?v=j1kI3peSXhY

### Sample Code
Replace the values in aaaaaaaaaaaaaaaa with your values
```sh
import analytics2wrap as aa
import json
import requests

company_id = 'aaaaaaaaaaaaaaaaaaaa'
auth_token = "Bearer aaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
client_id = 'aaaaaaaaaaaaaa'
date_range = '2019-03-01T00:00:00.000/2019-04-01T00:00:00.000'

#global_comapny_id will look like aaaaaaaaa.bbbbbb.digitalwebsite
global_company_id = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'

headers, reporturl = aa.create_con(auth_token,company_id,client_id)

# this will return key value pairs of dimention items with their item ids
dimention = aa.get_item_id('dimention',date_range,global_company_id)
print(mobile)

```
