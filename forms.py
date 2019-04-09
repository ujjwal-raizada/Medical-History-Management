from wtforms import Form, StringField, TextAreaField, PasswordField, BooleanField, SubmitField, validators
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

class ViewMedicalHistoryForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])

class AddMedicalHistoryForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    report = TextAreaField('Report', [validators.length(min=10, max=200)])

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators = [DataRequired()])
	remember_me = BooleanField('Remember me')
	submit = SubmitField('Sign In')