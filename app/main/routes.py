from flask import Flask,render_template, flash, redirect, url_for, request, session
from app import db
from app.main.forms import MyForm, TmachineForm,MyForm1
from app.models import Tmachine
from ast import literal_eval
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from turing_machine.dtm import DTM
from turing_machine.ntm import NTM
from turing_machine.xdtm import XDTM
from table import table,table_df
import time
from app import parser1
from turing_machine import exceptions
from sqlalchemy import exc
from app.main import bp



@bp.route('/', methods=['GET', 'POST'])
def index():
    form = TmachineForm()
    form.opts.query = Tmachine.query.filter(Tmachine.id >= 1)
    if form.validate_on_submit():
        name = form.opts.data.id
        druh = form.opts.data.tm_d_n_x
        return redirect(url_for('main.vstup',name = name,druh = druh))
    return render_template('index.html', form=form)


@bp.route('/vstup/<name>/<druh>', methods=['GET','POST'])
def vstup(name,druh):
    form = TmachineForm()

    counter = 0
    session["counter"] = counter
    form.opts.query = Tmachine.query.filter(Tmachine.id >= 1)
    if request.method == 'POST':
        if form.validate_on_submit() and form.submit.data:
            name = form.opts.data.id
            druh = form.opts.data.tm_d_n_x
        if request.form.get('Vstup') == 'Zapíš na pásku':
            vstup = request.form.get('vstup')
            name = session.get("newname")
            druh = session.get("newdruh")
            vs = True
            df, input_symbols , input_symbols_dict = table_df.table(name,druh)
            for i in vstup:
                if i not in input_symbols_dict:
                    vs = False
            if vs and vstup != "":
                session["newvstup"] = vstup
                return redirect(url_for('main.simulacia',vstup=vstup,druh = druh,name = name ))
            else:
                success_message = ("vstup: (")+vstup + (") nie je zo vstupnej abecedy: ") +input_symbols
                if vstup == "":
                    success_message = ("vstup je prázdny, zadajte vstupné slovo zo vstupnej abecedy: ") +input_symbols
                flash(success_message)
        
    df, input_symbols , input_symbols_dict = table_df.table(name,druh)
    session["newname"] = name
    session["newdruh"] = druh
    session["newinput_symbols"] = input_symbols
    return render_template('vstup.html', form = form, data1 = input_symbols, dataframe=df.to_html())     
    
@bp.route('/simuluj')
def simuluj():
    form = MyForm1()
    name = session.get("newname")
    druh = session.get("newdruh")
    vstup = session.get("newvstup")
    input_symbols = session.get("newinput_symbols")
    cas = session.get("cas")
    counter = session.get("counter")

    counter +=1
    session["counter"] = counter
    if druh == "ntm":
        if counter == 0:
            df,list_of_table,stroj, list_of_tape, final = table.table(name,vstup,druh)
            session['new_final'] = final
        else:
            final = session.get('new_final')
            df,list_of_table,stroj, list_of_tape = table.ntm_table_final(name,vstup,final)     
    elif druh == "xtm":
        df,list_of_table,stroj, list_of_tape, length = table.table(name,vstup,druh)
    else:
        df,list_of_table,stroj, list_of_tape = table.table(name,vstup,druh)

    if counter < len(list_of_table)-1:
        dff = list_of_table[counter]
        dff = dff.set_table_attributes('border="1" class="dataframe table table-hover table-bordered"')
        dff = dff.set_precision(3)
        df_tape = list_of_tape[counter]

        if druh == "xtm":
            dfz = []
            for i in range (length):
                dfz.append(list_of_tape[counter*length+i])
            if length == 2:
                return render_template("simuluj.html",content = cas,form=form,data1 = input_symbols,dataframe = dfz[0].to_html(),dataframe1 = dfz[1].to_html() ,data = dff)
            elif length == 3:
                return render_template("simuluj.html",content = cas,form=form,data1 = input_symbols,dataframe = dfz[0].to_html(),dataframe1 = dfz[1].to_html(), dataframe2= dfz[2].to_html(),data = dff)
            elif length == 4:
                return render_template("simuluj.html",content = cas,form=form,data1 = input_symbols,dataframe = dfz[0].to_html(),dataframe1 = dfz[1].to_html(), dataframe2= dfz[2].to_html(), dataframe3= dfz[3].to_html(),data = dff)
            elif length == 5:
                z[5] = render_template("simuluj.html",content = cas,form=form,data1 = input_symbols,dataframe = dfz[0].to_html(),dataframe1 = dfz[1].to_html(), dataframe2= dfz[2].to_html(), dataframe3= dfz[3].to_html(),dataframe4 = dfz[4].to_html(),data = dff)
            elif length == 6:
                z[6] = render_template("simuluj.html",content = cas,form=form,data1 = input_symbols,dataframe = dfz[0].to_html(),dataframe1 = dfz[1].to_html(), dataframe2= dfz[2].to_html(), dataframe3= dfz[3].to_html(),dataframe4 = dfz[4].to_html(), dataframe5 = dfz[5].to_html(),data = dff)
            elif length == 7:
                z[7] = render_template("simuluj.html",content = cas,form=form,data1 = input_symbols,dataframe = dfz[0].to_html(),dataframe1 = dfz[1].to_html(), dataframe2= dfz[2].to_html(), dataframe3= dfz[3].to_html(),dataframe4 = dfz[4].to_html(), dataframe5 = dfz[5].to_html(), dataframe6 = dfz[6].to_html(),data = dff)
        else:
            return render_template("simuluj.html",content = cas,form=form,data1 = input_symbols,dataframe = df_tape.to_html(classes=["table-bordered", "table-striped", "table-hover"]), data = dff)
    else:
        return redirect(url_for('main.simulacia',vstup=vstup,druh = druh,name = name ))
   
@bp.route('/simulacia/<name>/<druh>/<vstup>', methods=['GET','POST'])
def simulacia(vstup,druh, name):
    form = TmachineForm()
    form.opts.query = Tmachine.query.filter(Tmachine.id >= 1)
    name = session.get("newname")
    druh = session.get("newdruh")
    vstup = session.get("newvstup")
    input_symbols = session.get("newinput_symbols")
    counter = session.get("counter")
    
    if druh == "ntm":
        if counter == 0:
            df,list_of_table,stroj, list_of_tape, final = table.table(name,vstup,druh)
            session['new_final'] = final
        else:
            final = session.get('new_final')
            df,list_of_table,stroj, list_of_tape = table.ntm_table_final(name,vstup,final)
            
    elif druh == "xtm":
        df,list_of_table,stroj, list_of_tape, length = table.table(name,vstup,druh)
    else:
        df,list_of_table,stroj, list_of_tape = table.table(name,vstup,druh)

    if request.method == 'POST':
        if form.validate_on_submit() and form.submit.data:
            name = form.opts.data.id
            druh = form.opts.data.tm_d_n_x
            return redirect(url_for('main.vstup',name = name,druh = druh))
        elif request.form.get('Akceptuje/Zamieta') == 'Akceptuje/Zamieta':
            leng = len(list_of_table)
            counter = leng-1
        elif request.form.get('Krok vpred') == 'Krok vpred':
            if counter < len(list_of_table)-1:
                counter +=1
        elif request.form.get('Krok späť') == 'Krok späť':
            if counter > 0:
                counter -= 1
        elif request.form.get('Vstup') == 'Zapíš na pásku':
            vstup = request.form.get('vstup')
            name = session.get("newname")
            druh = session.get("newdruh")
            vs = True
            df, input_symbols , input_symbols_dict = table_df.table(name,druh)
            for i in vstup:
                if i not in input_symbols_dict:
                    vs = False
            if vs and vstup != "":
                session["newvstup"] = vstup
                counter = 0
                session["counter"] = counter   
                return redirect(url_for('main.simulacia',vstup=vstup,druh = druh,name = name ))
            else:
                success_message = ("vstup: (")+vstup + (") nie je zo vstupnej abecedy: ") +input_symbols
                if vstup == "":
                    success_message = ("vstup je prázdny, zadajte vstupné slovo zo vstupnej abecedy: ") +input_symbols
                flash(success_message)
                return redirect(url_for('main.vstup',name = name,druh = druh))   
        elif request.form.get('Simulácia') == 'Simulácia':
            counter -= 1
            session["counter"] = counter 
            try:
                cas = float(request.form.get('cas'))  
                session["cas"] = cas/1000
            except ValueError:
                cas = None
                success_message = ('Časové oneskorenie musí byť číslo väčšie ako 0')
                flash(success_message)
            if cas and cas>0:
                return redirect(url_for('main.simuluj'))
            else:
                success_message = ('Časové oneskorenie musí byť číslo väčšie ako 0')
                flash(success_message)
                return redirect(url_for('main.simulacia',vstup=vstup,druh = druh,name = name ))

    if counter == len(list_of_table)-1:
        if stroj:
            success_message = ('Turingov stroj akceptuje vstup: '+vstup)
        else:
            success_message = ('Turingov stroj zamieta vstup: '+vstup )
        flash(success_message)

    session["counter"] = counter  
    dff = list_of_table[counter]
    dff = dff.set_table_attributes('border="1" class="dataframe table table-hover table-bordered"')
    dff = dff.set_precision(3)
    df_tape = list_of_tape[counter]
  

    if druh == "xtm":
        dfz = []
        for i in range (length):
            dfz.append(list_of_tape[counter*length+i])
        if length == 2:
            return render_template("simulacia.html",form=form,data1 = input_symbols,dataframe = dfz[0].to_html(),dataframe1 = dfz[1].to_html() ,data = dff)
        elif length == 3:
            return render_template("simulacia.html",form=form,data1 = input_symbols,dataframe = dfz[0].to_html(),dataframe1 = dfz[1].to_html(), dataframe2= dfz[2].to_html(),data = dff)
        elif length == 4:
            return render_template("simulacia.html",form=form,data1 = input_symbols,dataframe = dfz[0].to_html(),dataframe1 = dfz[1].to_html(), dataframe2= dfz[2].to_html(), dataframe3= dfz[3].to_html(),data = dff)
        elif length == 5:
            z[5] = render_template("simulacia.html",form=form,data1 = input_symbols,dataframe = dfz[0].to_html(),dataframe1 = dfz[1].to_html(), dataframe2= dfz[2].to_html(), dataframe3= dfz[3].to_html(),dataframe4 = dfz[4].to_html(),data = dff)
        elif length == 6:
            z[6] = render_template("simulacia.html",form=form,data1 = input_symbols,dataframe = dfz[0].to_html(),dataframe1 = dfz[1].to_html(), dataframe2= dfz[2].to_html(), dataframe3= dfz[3].to_html(),dataframe4 = dfz[4].to_html(), dataframe5 = dfz[5].to_html(),data = dff)
        elif length == 7:
             z[7] = render_template("simulacia.html",form=form,data1 = input_symbols,dataframe = dfz[0].to_html(),dataframe1 = dfz[1].to_html(), dataframe2= dfz[2].to_html(), dataframe3= dfz[3].to_html(),dataframe4 = dfz[4].to_html(), dataframe5 = dfz[5].to_html(), dataframe6 = dfz[6].to_html(),data = dff)
    else:
        return render_template("simulacia.html",form=form,data1 = input_symbols,dataframe = df_tape.to_html(classes=["table-bordered", "table-striped", "table-hover"]), data = dff)


@bp.route('/dtm', methods=['GET', 'POST'])
def dtm():
    form = MyForm()
    if form.validate_on_submit():
        tm = False
        states = parser1.dict_parse(form.states.data)
        states_dict = literal_eval(states)
        input_s = parser1.dict_parse(form.input_symbols.data)
        input_symbols_dict = literal_eval(input_s)
        tape_s = parser1.dict_parse(form.tape_symbols.data)
        tape_symbols_dict = literal_eval(tape_s)
        
        initial_state_d = form.initial_state.data
        if form.left_end.data:    
            left_end_d = form.left_end.data
        else:
            left_end_d = '>'
        try:
            transitions_d = literal_eval(form.prechody.data)
        except:
            transitions_d = {}
            success_message = ("Neočakávaná chyba v prechodovej funkcii")
            flash(success_message)
            
        if form.blank_symbol.data:
            blank_symbol_d = form.blank_symbol.data
        else:
            blank_symbol_d = '#'
        reject_state_d = form.reject_state.data
        final_states_d = form.final_states.data
        try:
            dtm = DTM(
            states = states_dict,
            input_symbols= input_symbols_dict,
            tape_symbols= tape_symbols_dict,
            left_end = left_end_d,
            transitions = transitions_d,
            initial_state = initial_state_d,
            blank_symbol = blank_symbol_d,
            reject_state = reject_state_d,
            final_states = final_states_d
            )
            if dtm:
                tm = True
        except(exceptions.InvalidStateError,exceptions.InvalidSymbolError,exceptions.MissingStateError,exceptions.MissingSymbolError,
               exceptions.InitialStateError,exceptions.FinalStateError,exceptions.RejectStateError,exceptions.LeftEndError,
               exceptions.RejectionError,exceptions.InvalidDirectionError) as err:
            tm = False
            success_message = (err)
            flash(success_message)
        if tm:
            try:
                tmachine = Tmachine(definicia= form.funkcia.data,tm_d_n_x='dtm',
                                    states =states,input_symbols = input_s,
                                    tape_symbols = tape_s,left_end = left_end_d,
                                    transitions = form.prechody.data, initial_state = initial_state_d,
                                    blank_symbol = blank_symbol_d,reject_state = reject_state_d,
                                    final_states = final_states_d)
                db.session.add(tmachine)
                db.session.commit()
                success_message = ('Nový DTM: '+form.funkcia.data+' je vytvorený')
                flash(success_message)
                return redirect(url_for('index'))  
            except exc.IntegrityError:
                db.session().rollback()
                tm = False
                success_message = ("Definícia/Názov TM už existuje prosím zvolte iný názov")
                flash(success_message)        
    return render_template('dtm.html',  title='DTM', form=form)


@bp.route('/ntm', methods=['GET', 'POST'])
def ntm():
    form = MyForm()
    if form.validate_on_submit():
        tm = False
        states = parser1.dict_parse(form.states.data)
        states_dict = literal_eval(states)
        input_s = parser1.dict_parse(form.input_symbols.data)
        input_symbols_dict = literal_eval(input_s)
        tape_s = parser1.dict_parse(form.tape_symbols.data)
        tape_symbols_dict = literal_eval(tape_s)
        
        initial_state_d = form.initial_state.data
        if form.left_end.data:    
            left_end_d = form.left_end.data
        else:
            left_end_d = '>'
        try:
            transitions_d = literal_eval(form.prechody.data)
        except:
            transitions_d = {}
            success_message = ("Neočakávaná chyba v prechodovej funkcii")
            flash(success_message)
            
        if form.blank_symbol.data:
            blank_symbol_d = form.blank_symbol.data
        else:
            blank_symbol_d = '#'
        reject_state_d = form.reject_state.data
        final_states_d = form.final_states.data
        try:
            ntm = NTM(
            states = states_dict,
            input_symbols= input_symbols_dict,
            tape_symbols= tape_symbols_dict,
            left_end = left_end_d,
            transitions = transitions_d,
            initial_state = initial_state_d,
            blank_symbol = blank_symbol_d,
            reject_state = reject_state_d,
            final_states = final_states_d
            )
            if ntm:
                tm = True
        except(exceptions.InvalidStateError,exceptions.InvalidSymbolError,exceptions.MissingStateError,exceptions.MissingSymbolError,
               exceptions.InitialStateError,exceptions.FinalStateError,exceptions.RejectStateError,exceptions.LeftEndError,
               exceptions.RejectionError,exceptions.InvalidDirectionError) as err:
            tm = False
            success_message = (err)
            flash(success_message)
        if tm:
            try:
                tmachine = Tmachine(definicia= form.funkcia.data,tm_d_n_x='ntm',
                                    states =states,input_symbols = input_s,
                                    tape_symbols = tape_s,left_end = left_end_d,
                                    transitions = form.prechody.data, initial_state = initial_state_d,
                                    blank_symbol = blank_symbol_d,reject_state = reject_state_d,
                                    final_states = final_states_d)
                db.session.add(tmachine)
                db.session.commit()
                success_message = ('Nový NTM: '+form.funkcia.data+' je vytvorený')
                flash(success_message)
                return redirect(url_for('index'))
            except exc.IntegrityError:
                db.session().rollback()
                tm = False
                success_message = ("Definícia/Názov TM už existuje prosím zvolte iný názov")
                flash(success_message)   
    return render_template('ntm.html',  title='NTM', form=form)

@bp.route('/xtm', methods=['GET', 'POST'])
def xtm():
    form = MyForm()
    if form.validate_on_submit():
        tm = False
        states = parser1.dict_parse(form.states.data)
        states_dict = literal_eval(states)
        input_s = parser1.dict_parse(form.input_symbols.data)
        input_symbols_dict = literal_eval(input_s)
        tape_s = parser1.dict_parse(form.tape_symbols.data)
        tape_symbols_dict = literal_eval(tape_s)

        initial_state_d = form.initial_state.data
        if form.left_end.data:    
            left_end_d = form.left_end.data
        else:
            left_end_d = '>'
        try:
            transitions_d = literal_eval(form.prechody.data)
        except:
            transitions_d = {}
            success_message = ("Neočakávaná chyba v prechodovej funkcii")
            flash(success_message)

        if form.blank_symbol.data:
            blank_symbol_d = form.blank_symbol.data
        else:
            blank_symbol_d = '#'
        reject_state_d = form.reject_state.data
        final_states_d = form.final_states.data
        try:
            xdtm = XDTM(
            states = states_dict,
            input_symbols= input_symbols_dict,
            tape_symbols= tape_symbols_dict,
            left_end = left_end_d,
            transitions = transitions_d,
            initial_state = initial_state_d,
            blank_symbol = blank_symbol_d,
            reject_state = reject_state_d,
            final_states = final_states_d
            )
            if xdtm:
                tm = True
        except(exceptions.InvalidStateError,exceptions.InvalidSymbolError,exceptions.MissingStateError,exceptions.MissingSymbolError,
               exceptions.InitialStateError,exceptions.FinalStateError,exceptions.RejectStateError,exceptions.LeftEndError,
               exceptions.RejectionError,exceptions.InvalidDirectionError,exceptions.Badcounttapes) as err:
            tm = False
            success_message = (err)
            flash(success_message)
        if tm:
            try:
                tmachine = Tmachine(definicia= form.funkcia.data,tm_d_n_x='xtm',
                                    states =states,input_symbols = input_s,
                                    tape_symbols = tape_s,left_end = left_end_d,
                                    transitions = form.prechody.data, initial_state = initial_state_d,
                                    blank_symbol = blank_symbol_d,reject_state = reject_state_d,
                                    final_states = final_states_d)
                db.session.add(tmachine)
                db.session.commit()
                success_message = ('Nový viac páskový DTM: '+form.funkcia.data+' je vytvorený')
                flash(success_message)
                return redirect(url_for('index'))
            except exc.IntegrityError:
                db.session().rollback()
                tm = False
                success_message = ("Definícia/Názov TM už existuje prosím zvolte iný názov")
                flash(success_message)
    return render_template('xtm.html',  title='XTM', form=form)

    
    

    
   


