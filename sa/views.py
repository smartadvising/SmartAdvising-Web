import flask
from flask_login import login_user, logout_user, login_required, current_user

from sa import app
from sa.utils import call_api, sign_in_url, dict_without
from sa.forms import StudentForm, FAQForm, AdvisorForm


@login_required
@app.route('/')
def index():
    return flask.render_template('home.html')

    
@app.route('/login', methods=['GET', 'POST'])
def login(): 
    login_form = StudentForm()
    login_form.college.choices = [(c["id"], c["name"]) for c in call_api("get", "colleges")["colleges"]]
    
    if flask.request.method == 'POST':
        # process form here
        # login user_email and get student_id from api
        student = call_api("get", "students", {"email": ""})
        
        login_user(student_id)
        
        return flask.redirect(flask.urlfor('index'))
    
    return flask.render_template('login.html', login_form=login_form, o365_sign_in_url=sign_in_url())
    
@app.route('/logout')
def logout():
    logout_user()
    flask.session.clear()

    return flask.redirect(flask.url_for('login'))

    #student_id = [(s["id"], s["student_identifier"]) for s in call_api("get", "students")["students"]]
        #print("\n\n\n\nstudent_id:", student_id)
@app.route('/connect/get_token/')
def connect_o365_token():
    code = flask.request.args.get('code')
    if not code:
        app.logger.error("NO 'code' VALUE RECEIVED")
        return flask.Response(status=400)
        
    # keep this line
    token = get_oauth_token(code)
    jwt = get_jwt_from_id_token(token['id_token'])

    flask.session['user_email'] = jwt["upn"]
    flask.session['access_token'] = token["access_token"]

    return flask.redirect('/')
    

def get_resource(resource_name: str, real_url: str, without_keys: list, data: dict):
    return [
        dict_without(d, *without_keys)
        for d in call_api("get", real_url, data)[resource_name]
    ]
    

@app.route("/search/api/<resource_name>", methods=["GET"])
def search_api(resource_name):
    data = {}
    without_keys = []
    real_url = resource_name

    if resource_name == "majors":
        college_id = int(flask.request.args["college_id"])
        real_url = f"colleges/{college_id}/majors"

    return flask.jsonify(get_resource(resource_name, real_url, without_keys, data))