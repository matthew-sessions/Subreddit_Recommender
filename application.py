from flask import Flask, render_template, request, url_for, redirect, jsonify
from decouple import config
from get_data import *
import joblib
from model import *
import pandas as pd

test = "thisisatest"   #config('test')

application = Flask(__name__)

loadcv = joblib.load('models/tf.joblib')
loaddf = joblib.load('models/tfarray.joblib')
loaddf = loaddf.todense()


@application.route('/')
def home():
    return render_template('home.html')

@application.route('/search')
def search():
    title = request.args.get('title')
    block = request.args.get('block')
    words = title + ' ' + block.strip()
    data = transform_get(words, loadcv, loaddf)
    res = get_subreddit_info(data)

    return(render_template('search.html', res=res))

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
