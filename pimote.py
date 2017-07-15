#!/usr/bin/python
import logging
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, Response
from functools import wraps
import os
 
app = Flask(__name__)

logging.basicConfig()
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def check_auth(username, password):
  return username == 'api_user_wes' and password == 'errant-deckhand-heart-volume-raglan'

def authenticate():
  return Response(
  'You do not have permission to view this page', 401,
  {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
      auth = request.authorization
      if not auth or not check_auth(auth.username, auth.password):
         return authenticate()
      return f(*args, **kwargs)
  return decorated
   
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('home.html')
 
@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'ch8tt3ris' and request.form['username'] == 'thearchers':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()
    
@app.route('/lightson/')
def lights_on():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        os.system('python /home/pi/web-server/lights-on.py')
        return render_template('home.html')

@app.route('/lightsoff/')
def lights_off():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        os.system('python /home/pi/web-server/lights-off.py')
        return render_template('home.html')

@app.route('/socket1-on/')
def socket1_on():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        os.system('python /home/pi/web-server/socket1-on.py')
        return render_template('home.html')

@app.route('/socket1-off/')
def socket1_off():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        os.system('python /home/pi/web-server/socket1-off.py')
        return render_template('home.html')

@app.route('/socket2-on/')
def socket2_on():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        os.system('python /home/pi/web-server/socket2-on.py')
        return render_template('home.html')

@app.route('/socket2-off/')
def socket2_off():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        os.system('python /home/pi/web-server/socket2-off.py')
        return render_template('home.html')
 
@app.route("/logout/")
def logout():
    session['logged_in'] = False
    return render_template('logout.html')
    
@app.route("/api-all-on/")
@requires_auth
def api_all_on():
    os.system('python /home/pi/web-server/lights-on.py')
    
@app.route("/api-all-off/")
@requires_auth
def api_all_off():
    os.system('python /home/pi/web-server/lights-off.py')

@app.route("/api-socket1-on/")
@requires_auth
def api_socket1_on():
    os.system('python /home/pi/web-server/socket1-on.py')
    
@app.route("/api-socket1-off/")
@requires_auth
def api_socket1_off():
    os.system('python /home/pi/web-server/socket1-off.py')

@app.route("/api-socket2-on/")
@requires_auth
def api_socket2_on():
    os.system('python /home/pi/web-server/socket2-on.py')

@app.route("/api-socket2-off/")
@requires_auth
def api_socket2_off():
    os.system('python /home/pi/web-server/socket2-off.py')

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=9292)
