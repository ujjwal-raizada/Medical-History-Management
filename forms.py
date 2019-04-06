from wtforms import Form, StringField, TextAreaField, validators

class ViewMedicalHistoryForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])

class AddMedicalHistoryForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    report = TextAreaField('Report', [validators.length(min=10, max=200)])
