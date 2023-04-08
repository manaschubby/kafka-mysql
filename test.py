import requests
import json

url = "http://localhost:8083/connectors"

payload = json.dumps({
  "topics": [
    "jsontest"
  ]
})
headers = {
  'Content-Type': 'application/json',
  'Cookie': 'csrftoken=xzHw2iFslXIS1jnibFGhb63wwkisnTLO'
}

response = requests.request("GET", url, headers=headers, data=payload)

if(response.status_code!=200):
    raise ConnectionError
