#!/usr/bin/env python
"""
A simple Flask application that returns details on each of the HTTP status codes.
"""

from collections import OrderedDict
from flask import Flask, render_template, redirect, url_for, jsonify
from flask.ext.bootstrap import Bootstrap
from yaml import load
app = Flask(__name__)
bootstrap = Bootstrap(app)

CODES_FILE = "status-codes.yml"

def get_codes():
    """ Return a sorted dictionary of the status codes and their details. """
    with open(CODES_FILE) as codes:
        sorted_codes = OrderedDict(sorted(load(codes).items(), key=lambda t: t[0]))
        return sorted_codes

def get_code_details(code):
    """ Return the details of the status `code`. """
    codes = get_codes()
    if code in codes:
        return codes[code]

@app.route('/')
def index():
    """ The function for the main index page. """
    codes = get_codes()
    return render_template('index.html', codes=codes)

@app.route('/<code>')
def code(code):
    """ Returns redirect to html formatted endpoint for `code`. """
    return redirect(url_for('code_format', code=code, return_format='html'))

@app.route('/<code>/<return_format>')
def code_format(code, return_format):
    """ Returns appropriates formatted page based for `code`. """
    details = get_code_details(code.encode('ascii', 'ignore'))
    if details:
        if return_format == 'html':
            return render_template('code.html', code=code, details=details), \
                        code
        elif return_format == 'json':
            return jsonify({code: details}), \
                        code
        elif return_format == 'text':
            return render_template('code.txt', code=code, details=details), \
                        code, \
                       {'Content-Type': 'text/plain'}
    else:
        return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
