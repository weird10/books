from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.sighting  import Sighting

@app.route('/sighting')
def create_sighting():
    return render_template('add_sighting.html')

@app.route('/sighting/create', methods=['POST'])
def sighting_create():
    if Sighting.create_sighting(request.form):
        return redirect('/user/profile')
    return redirect('/user/profile')

@app.route('/sighting/edit/<int:id>')
def sighting_edit(id):
    data ={
        'id' : id
    }
    this_sighting = Sighting.get_by_sighting_id(data)  
    return render_template('sighting_edit.html', this_sighting=this_sighting )

@app.route('/sighting/edit', methods=['POST'])
def sighting_update():
    if Sighting.edit_sighting(request.form):
        return redirect('/user/profile')
    return redirect('/user/profile') 

@app.route('/sighting/<int:id>')
def view_sighting(id):
    data ={
        'id': id
    }
    this_sighting = Sighting.get_by_sighting_id(data)
    return render_template('sighting_show.html', this_sighting=this_sighting)
