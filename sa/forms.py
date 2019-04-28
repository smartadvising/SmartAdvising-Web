import decimal
import datetime
import json

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField  
from wtforms.validators import DataRequired


class FAQForm(FlaskForm):
    Question = StringField('Question', validators=[DataRequired()])
    Answer = StringField('Answer', validators=[DataRequired()])
    submit = SubmitField('submit')
    
class StudentForm(FlaskForm):
    college = SelectField('College', validators=[DataRequired()])
    major = SelectField('Major', choices=[(0, "")], validators=[DataRequired()])
    division = SelectField(u'Division', choices=[(1, "Undergraduate"), (2, "Graduate")])
    submit = SubmitField('submit')
    
class AdvisorForm(FlaskForm):
    college = StringField('Question', validators=[DataRequired()])
    department = StringField('Answer', validators=[DataRequired()])
    submit = SubmitField('submit')

    
