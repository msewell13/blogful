from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class AddEntry(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	content = StringField('Content', validators=[DataRequired()])

class DeleteEntry(FlaskForm):
	pass