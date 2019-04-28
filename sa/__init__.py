# --------------- initialization ----------------------
import urllib
import json
import time
import base64
import datetime
import json
import requests
import urllib

import flask
from flask_login import LoginManager


app = flask.Flask(__name__)
app.config.from_object('config')

lm = LoginManager()
lm.init_app(app)
lm.login_view = "login" 


import sa.views