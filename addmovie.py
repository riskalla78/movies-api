
""" #Exemplo de adição de filme na API

import requests

url = 'http://127.0.0.1:5000/movies/add'
data = {'title': 'New Movie'}

response = requests.post(url, json=data)
print(response.status_code)
print(response.json())
 """