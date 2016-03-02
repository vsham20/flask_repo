import elasticsearch
from flask import render_template, flash, redirect, make_response, request,url_for
from flask.ext.login import login_user, logout_user, login_required
from app import app
from .forms import LoginForm
from .models import User
import openpyxl
import os
import requests
import re
import urllib

from pymongo import MongoClient


@app.route('/')
def main():
    return render_template('main.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    """
    else:
        client = MongoClient()
        db = client.bm
        details = db.user_entry.find()
        for i in details:
            print i['email']
            print 'fds'
            print request.form['email']
            if i['email'] == request.form['email'] and i['password'] ==request.form['pwd']:
                print "========"
                print request.form['email']
                print request.form['pwd']
                #usr = User(email = user,password_hash = pwd)
                #login_user(usr)
                return redirect(url_for('index'))
            return render_template("login.html")        

"""

    form = LoginForm()
    print 'dsd'
    if form.validate_on_submit() is False:
        print 'xf'
        user = User.query.filter_by(email=form.email.data).first()  
        print 'dsfs'                       
        if user is not None:
            login_user(user)
            return redirect(url_for('/index'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    #form = RegistrationForm()
    if request.method == 'GET':
        return render_template('Register.html')
        user = User(request.form['email'], request.form['email'])
        db.session.add(user)
        db.session.commit()
        flash('User successfully registered')
        return redirect(url_for('login'))
        """es = elasticsearch.Elasticsearch()
        es.index(index="user",doc_type="user_entry",id=1,body={
                        'email' : '%s' %request.form['email'],
                        'password' : '%s' %request.form['pwd']
                        })
        print request.form['email']
        print request.form['pwd']
        return redirect(url_for('login'))
    return render_template("Register.html")"""

@app.route('/logout')
#@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main'))


@app.route('/index')
#@login_required
def index():
    user = {"nickname":"Vaishali"}
    return render_template('index.html',jsob=user)

@app.route('/add_bookmark', methods=['GET','POST'])
def add_bookmarks():
    if request.method == 'GET':
        return render_template('add_bookmark.html')
    else:
        print request.form['link']
        print request.form['bookmark_name']
        es = elasticsearch.Elasticsearch()
        es.index(index="list_bookmarks",doc_type="bookmarks",body={
'website_name' : '%s' %request.form['bookmark_name'],
'website_link' : '%s' %request.form['link']
})

        return render_template('add_bookmark.html')
    #es = elasticsearch.Elasticsearch()
    #print request.form
        

@app.route('/previous_bookmark',methods=["GET", "POST"])
def previous_bookmarks():
    es = elasticsearch.Elasticsearch()
    res = es.search(index='list_bookmarks',doc_type='bookmarks',body={'filter':{'term':{'_index':'list_bookmarks'}}})['hits']['hits'] 
    if request.method == "GET":
        return render_template("previous_bookmarks.html",bookmark = res)
    else:
        value = request.form.getlist("check")
        print value
        es.index(index="saved_bookmarks", doc_type="bookmark", id=1,body={
            'website_name' : '%s' %value
            })
        return render_template("previous_bookmarks.html", bookmark = res) 

@app.route('/Download', methods=["GET","POST"])
def download():
    es = elasticsearch.Elasticsearch()
    res = es.search(index='saved_bookmarks', doc_type='bookmark', body={
'filter':{'term':{'_index':'saved_bookmarks'}}})['hits']['hits']
    return render_template('export_bookmark.html', res = res)


@app.route('/Import')
#print "hfhghghggh"
def Import():
    print "hfhghg"
    """
    url = 'http://127.0.0.1:5000/Download'
    response = requests.get(url)
    r = response.content
    print r
    """
    page = urllib.urlopen('/tmp/Download-1').read()
    print page
    list = [k.strip('&') for k in re.findall(r"(?<=39\;).+\&",page)]
    return render_template('import.html', list = list)


