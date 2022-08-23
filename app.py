import pandas as pd
import os
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, SubmitField
from wtforms.validators import DataRequired, InputRequired, NumberRange

app = Flask(__name__)

# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = 'amcachavi'

# Flask-Bootstrap requires this line
Bootstrap(app)

df = pd.read_csv(os.path.join("data" , "tbl_team.csv"))
main_df = df[["str_team_name", "int_overall"]]

class GeneratorForm(FlaskForm):
    randomize = BooleanField("Randomize?")
    low_rating = IntegerField("Minimum Rating", validators=[InputRequired("Minimum Rating Required, enter 1 for randomizing any team"), NumberRange(min=1, max=99, message="Please enter a number between 1 and 99")])
    high_rating = IntegerField("Maximum Rating")
    number_of_teams = IntegerField("Number of Teams", validators=[InputRequired("Enter the number of teams you would like"), NumberRange(min=1, max=15, message="Please enter a number between 1 and 15")])


@app.route('/', methods=['GET', 'POST'])
def home():
    form = GeneratorForm()
    global main_df

    if form.validate_on_submit():
        return main_df[main_df["int_overall"] > form.low_rating.data].sample(int(form.number_of_teams.data)).to_html()
        # return "<h1>The form has been submitted with minimum rating: {}, maximum rating: {}, number of teams {}".format(form.low_rating.data, form.high_rating.data, form.number_of_teams.data)
    return render_template('test_form.html', form=form, tables=[main_df.to_html()])




# DO NOT EDIT BELOW THIS LINE
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False)