from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.user import User
from flask_app.models.sighting import Sighting
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

#index
@app.route('/')
def index():
    return render_template('index.html', info = request.form)

@app.route('/create/user', methods=['POST'])
def create_user():
    if User.create_user(request.form):
        return redirect('/user/profile')
    return redirect('/')

@app.route('/user/profile')
def show_user_profile():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": session['user_id'],
    }
    all_sightings=Sighting.get_all_sightings()
    return render_template('user_profile.html', all_sightings=all_sightings, all_view=all_sightings)


@app.route('/login', methods=['POST'])
def login():
    if not User.login(request.form):
        return redirect('/')
    return redirect('/user/profile')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/beskeptic', methods=['POST'])
def be_skeptic():
    data = {
        'user_id': request.form['user_id'],
        'sighting_id': request.form['sighting_id']
    }
    User.be_skeptic(data)
    print('GREAT SUCCESS')
    return redirect("/user/profile")





#create

#read

#update

#delete