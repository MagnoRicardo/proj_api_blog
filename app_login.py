from requests.auth import HTTPBasicAuth
import requests

login = requests.get('http://localhost:5000/login', auth=('Magno Ricardo', '253689'))

print(login.json())

login_usuarios = requests.get('http://localhost:5000/usuarios', headers={'x-access-token':login.json()['token']})

print(login_usuarios.json())