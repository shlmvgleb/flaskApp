import requests


requests.post('http://127.0.0.1:5000/', data={
    "name": 'user - ' + input()
})