#
# NOTES ROUTES
#

import time

from flask import request, render_template, make_response, redirect

import storage

from main import app
from main import verify_login

@app.route('/notes', methods=['GET'])
def get_notes():
    response = verify_login(request)
    if response:
        return response
    message = request.cookies.get("message")
    key = request.cookies.get("session_key")
    session = storage.get_session(key)
    response = make_response(render_template("notes.html", message=message, session=session))
    storage.update_session(key, {"pages":(session.get("pages",0) + 1)})
    response.set_cookie("session_key", key, max_age=600)
    response.set_cookie("message","",expires=0)
    return response

@app.route('/notes', methods=['POST'])
def post_notes():
    response = verify_login(request)
    if response:
        return response
    key = request.cookies.get("session_key")
    session = storage.get_session(key)
    note = request.form.get("note")
    if note != None and note != "":
        storage.add_note({'user': str(session['user']),
                          'text': str(note)})
    response =  make_response(redirect("/notes"))
    response.set_cookie("session_key", key, max_age=600)
    response.set_cookie("message","",expires=0)
    return response
