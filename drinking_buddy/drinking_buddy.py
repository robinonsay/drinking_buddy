from flask import Flask, make_response, render_template, flash
from flask import request
from flask import redirect, url_for
import serial
import os
import atexit
import datetime

app = Flask(__name__)
app.secret_key = 'some_secret'
port = os.environ['DRINKING_BUDDY_PORT']
arduino_s = serial.Serial(port, 9600)
drinks = {'red': bytearray(b'\x1F\x05\x00'),
          'blue': bytearray(b'\x00\x0A\x1F'),
          'none': bytearray(b'\x00\x0A\x00'),
          'purple': bytearray(b'\x10\x09\x10')}

users = {}
MAX_RATE = 1/300 * 5


def exit_handler():
    print("Closing Arduino Port")
    arduino_s.close()


atexit.register(exit_handler)


@app.route('/')
def index():
    # resp = make_response(render_template(...))
    resp = make_response(render_template('index.html'))
    if 'userId' in request.cookies:
        ip = request.cookies['userId']
        if ip not in users:
            users[ip] = 0
        users[ip] += 1
    else:
        ip = request.remote_addr
        users[ip] = 0
    resp.set_cookie('userId', ip)
    resp.set_cookie('num_orders', str(users[ip]))
    return resp


@app.route('/order', methods=['GET'])
def place_order():
    order_placed = request.args['drink']
    resp = make_response(redirect(url_for('index')))
    now = datetime.datetime.now()
    rate = 0
    if 'drinks_per_sec' in request.cookies and 'last_order' in request.cookies:
        last = datetime.datetime.fromisoformat(request.cookies['last_order'])
        rate = float(request.cookies['drinks_per_sec'])
        rate = rate + 1/((now-last).total_seconds())
        if rate > MAX_RATE:
            print("max exceeded")
            flash('Slow down their bud, You can have your next drink in {} min(s)'.format(60 * rate), 'error')
            return resp
        resp.set_cookie('drinks_per_sec', str(rate), max_age=60*60)
        resp.set_cookie('last_order', str(now))
    else:
        resp.set_cookie('drinks_per_sec', str(0), max_age=60*60)
        resp.set_cookie('last_order', str(now))
    try:
        order = drinks[order_placed]
        arduino_s.write(order)
    except KeyError:
        return 'Invalid Order', 404
    except serial.serialutil.SerialException:
        pass
    return resp
