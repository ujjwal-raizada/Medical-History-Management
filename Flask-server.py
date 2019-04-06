import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request, flash, redirect, url_for, render_template

from forms import AddMedicalHistoryForm, ViewMedicalHistoryForm
from Blockchain import Blockchain
from controllers import mine, new_transaction, full_chain, register_nodes, consensus

server = Flask(__name__)

@server.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@server.route('/addreport', methods=['POST', 'GET'])
def addreport():
    form = AddMedicalHistoryForm(request.form)

    if (request.method == 'POST' and form.validate()):
        user = form.username.data
        report = form.report.data

        new_transaction(user, report)
        mine(user)

        return redirect(url_for('home'))

    return render_template('addreport.html', form=form)


@server.route('/viewreport', methods=['POST', 'GET'])
def viewreport():
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



if __name__ == '__main__':
    server.run(host='0.0.0.0', port=5000)


