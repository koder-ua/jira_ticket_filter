import os.path

key_cert_data = None
key_cert = 'moslinuxbot.pem'

with open(os.path.join(os.path.dirname(__file__), key_cert), 'r') as key_cert_file:
    key_cert_data = key_cert_file.read()

options = {
    'server': 'https://mirantis.jira.com'
}

oauth_dict = {
    'access_token': '***',
    'access_token_secret': '***',
    'consumer_key': '***',
    'key_cert': key_cert_data
}