import os
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import GoogleCredentials

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./key_for_dialogflow.json"
