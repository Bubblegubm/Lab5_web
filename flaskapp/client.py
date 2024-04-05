import requests
r = requests.get('http://localhost:4000/')
print(r.status_code)
print(r.text) 
