#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys

from flask import render_template, url_for, jsonify, request, abort
from werkzeug import secure_filename

from app import app
from parser.parser import parse_list

reload(sys)
sys.setdefaultencoding('utf-8')

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        (products, header, not_parseable) = parse_list(file)
        return render_template(
            'list.html',
            file=filename,
            products=json.dumps(products),
            header=json.dumps(header),
            not_parseable=json.dumps(not_parseable)
        )

    else:
        return render_template(
            'upload.html'
        )

import os

@app.route('/test')
def test():
    file = "basis_september2013.pdf"
    (products, header, not_parseable) = parse_list("%s/../%s"%(os.path.dirname(os.path.abspath(__file__)), file))
    return render_template(
        'list.html',
        file=file,
        products=json.dumps(products),
        header=json.dumps(header),
        not_parseable=json.dumps(not_parseable)
    )