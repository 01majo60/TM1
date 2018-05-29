from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_sqlalchemy import SQLAlchemy 
from app.models import Tmachine

class MyForm(FlaskForm):
    funkcia = StringField('Definícia TM', validators=[DataRequired("Políčko je prázdne zadajte názov/definíciu TM")])
    states = StringField('Q - množina stavov', validators=[DataRequired("Políčko je prázdne zadajte množinu stavov")])
    input_symbols = StringField('Σ - množina vstupných symbolov', validators=[DataRequired("Políčko je prázdne zadajte množinu vstupných symbolov")])
    tape_symbols = StringField('Γ - množina páskových symbolov', validators=[DataRequired("Políčko je prázdne zadajte množinu páskových symbolov")])
    left_end = StringField("Ľavá koncová značka defaultne: '>' ak necháte políčko prázdne ", validators=[])
    prechody = TextAreaField('Prechodová funkcia', validators=[DataRequired("Políčko je prázdne zadajte prechodovú funkciu")]) 
    initial_state = StringField('Počiatočný stav', validators=[DataRequired("Políčko je prázdne zadajte počiatočný stav")])
    blank_symbol = StringField("Symbol označujúci prázdne políčko defaultne: '#' ak necháte políčko prázdne", validators=[])
    reject_state = StringField('Zamietajúci stav', validators=[DataRequired("Políčko je prázdne zadajte zamietajúci stav")])
    final_states = StringField('Akceptujúci stav', validators=[DataRequired("Políčko je prázdne zadajte akceptujúci stav")])
    submit = SubmitField('Vytvor TM')

def validate_funkcia(self,funkcia):
    tmachine = Tmachine.query.filter_by(definicia=self.funkcia.data).first()
    if tmachine is not None:
        raise ValidationError('Prosím zvolte iné meno')

def tmachine_query():
    return Tmachine.query

class TmachineForm(FlaskForm):
    opts = QuerySelectField(query_factory=tmachine_query, allow_blank=False, get_label='definicia', validators=[DataRequired("Nie sú k dispozícii žiadne Turingove stroje, vytvorte Turingove stroje")])
    submit = SubmitField('Vyber TM')

class MyForm1(FlaskForm):
    pass

