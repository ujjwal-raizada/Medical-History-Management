import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request, flash, redirect, url_for, render_template

from forms import AddMedicalHistoryForm, ViewMedicalHistoryForm, LoginForm
from Blockchain import Blockchain
from controllers import mine, create_transaction, full_chain, register_nodes, consensus
from zkp import gen_public_sig

from config import Config
from login import check_login

server = Flask(__name__)
server.config.from_object(Config)

loggedin = False
loggedin_user = ''
password = ''

@server.route('/', methods=['GET'])
def home():

    if(not loggedin):
        return redirect('/login')

    return render_template('index.html')

@server.route('/addreport', methods=['POST', 'GET'])
def addreport():

    global loggedin

    if(not loggedin):
        return redirect('/login')

    form = AddMedicalHistoryForm(request.form)

    
    global loggedin_user
    global password

    if (request.method == 'POST' and form.validate()):
        user = form.username.data
        report = form.report.data

        signature = gen_public_sig(password, report)

        create_transaction(user, loggedin_user, report, signature)
        mine(user)

        return redirect(url_for('home'))

    return render_template('addreport.html', form=form)


@server.route('/viewreport', methods=['POST', 'GET'])
def viewreport():

    if(not loggedin):
        return redirect('/login')

    form = ViewMedicalHistoryForm(request.form)

    if (request.method == 'POST' and form.validate()):
        
        chain = full_chain(form.username.data)
        print(chain)
        report_view = []
        for block in chain['chain']:
            report_view.append(block['transactions'])

        print(report_view)

        return render_template('viewreport.html', data=report_view, form=form)

    return render_template('viewreport.html', form=form)


@server.route('/login', methods=['GET', 'POST'])
def login():

    global loggedin
    global loggedin_user
    global password

    form = LoginForm()

    if (request.method == 'POST' and form.validate_on_submit()):

        username = form.username.data
        password = form.password.data

        temp  = check_login(username, password)

        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))

        if(temp != 0):
            loggedin = True
            loggedin_user = username
            return redirect('/')

        else:
            flash('Invalid username or password')
            return redirect('/login')

    return render_template('login.html', title='Sign In', form=form)



if __name__ == '__main__':
    server.run(host='0.0.0.0', port=5000)


