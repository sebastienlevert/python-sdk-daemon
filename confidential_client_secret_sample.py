from azure.identity import ClientSecretCredential
from msgraphcore import GraphSession

import sys  # For simplicity, we'll read config file from 1st CLI param sys.argv[1]
import json
import requests.exceptions

if(len(sys.argv) == 2):
    config = json.load(open(sys.argv[1]))
else:
    config = json.load(open("parameters.local.json"))

tenant_id = config["tenant_id"]
client_id = config["client_id"]
client_secret = config["client_secret"]
scopes = config["scope"]
sample_user = config["sample_user"]

credential = ClientSecretCredential(
    tenant_id = tenant_id,
    client_id = client_id,
    client_secret = client_secret
)

graph_session = GraphSession(credential, scopes)

users = graph_session.get('/users')
print(json.dumps(users.json(), indent=2))

single_user = graph_session.get('/users/' + sample_user)
print(json.dumps(single_user.json(), indent=2))

body = {
    'message': {
        'subject': 'Python SDK Meet for lunch?',
        'body': {
            'contentType': 'Text',
            'content': 'The new cafeteria is open.'
        },
        'toRecipients': [
            {
                'emailAddress': {
                    'address': sample_user
                }
            }
        ]}
}

try:
    response = graph_session.post('/users/' + sample_user + '/sendMail',
        data=json.dumps(body),
        headers={'Content-Type': 'application/json'}
    )
    response.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(err)