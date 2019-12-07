from flask import Flask, render_template, request, url_for, redirect, jsonify
from decouple import config
from get_data import *


test = "thisisatest"   #config('test')

application = Flask(__name__)

@application.route('/')
def home():
    return 'status' + test


@application.route('/test')
def vals():
    res = get_subreddit_info([1,6,8,5])
    return(jsonify(res))

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
