# ---------------------- configuration -------------------------
import os
import pathlib

# server_address will be changed if we decide to pay for hosting at some point
BASEDIR = os.path.abspath(os.path.dirname(__file__))
SERVER_ADDRESS = 'http://localhost:5000'

DEBUG = True
SECRET_KEY = '<SECRET>'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.join(BASEDIR, 'database'), 'office365.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# this is the AppId and AppKey from SmartAdvising-web on Azure Active Directory
O365_APP_ID = '542bde55-03a4-4c7c-b0b7-21e1029fe271'
O365_APP_KEY = 'UNLtGDr3CYOf76zLAyQuj1hMLzBW6giHUSJFMH6nva8='
O365_REDIRECT_URI = pathlib.posixpath.join(SERVER_ADDRESS, 'connect/get_token')
O365_AUTH_URL = 'https://login.microsoftonline.com/common/oauth2/authorize'
O365_TOKEN_URL = 'https://login.microsoftonline.com/common/oauth2/token'
APP_TOKEN = "6vDahPFC9waiEwI3UMHbz5paBkTPRFZshJeDL7ZYnFXvbcoYRGtFPD6Ogh8iy6nI"
API_URL = "https://bvet7wmxma.execute-api.us-east-1.amazonaws.com/prod/{}"