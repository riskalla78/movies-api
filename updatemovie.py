""" 
# Exemplo de atualização de filme

import requests

url = 'http://127.0.0.1:5000/movies/update/1'
data = {'title': 'Updated Movie Title', 'rating': 9.0}
response = requests.put(url, json=data)
print(response.status_code)
print(response.json()) """