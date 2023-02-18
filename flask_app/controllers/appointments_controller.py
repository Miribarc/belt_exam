from flask import render_template, redirect, session, request, flash
from flask_app import app

#Importación de modelos
from flask_app.models.users import User
from flask_app.models.appointments import Appointment

@app.route('/new/appointment')
def new_appointment():
    if 'user_id' not in session:
        return redirect('/')

    #Yo sé que en sesión tengo el id de mi usuario (session['user_id'])
    #Queremos una función que en base a ese id me regrese una instancia del usuario
    formulario = {"id": session['user_id']}

    user = User.get_by_id(formulario) #Recibo la instancia de usuario en base a su ID
    

    return render_template('new_appointment.html', user=user)

@app.route('/create/appointment', methods=['POST'])
def create_appointment():
    if 'user_id' not in session:
        return redirect('/')
        
    if not Appointment.valida_appointment(request.form):
        return redirect('/new/appointment')
    
    Appointment.save(request.form)

    return redirect('/appointments')


@app.route('/edit/appointment/<int:id>')
def edit_appointment(id):
    if 'user_id' not in session:
        return redirect('/')

    #Yo sé que en sesión tengo el id de mi usuario (session['user_id'])
    #Queremos una función que en base a ese id me regrese una instancia del usuario
    formulario = {"id": session['user_id']}

    user = User.get_by_id(formulario) #Recibo la instancia de usuario en base a su ID

    #Cuál es la calificación que se va a editar
    formulario_task = {"id": id}
    appointment = Appointment.get_by_id(formulario_task)
    
    return render_template('edit_appointment.html', user=user, appointment=appointment)

@app.route('/update/appointment', methods=['POST'])
def update_appointment():
    if 'user_id' not in session:
        return redirect('/')
    
    #Validación de Calificación
    if not Appointment.valida_appointment(request.form):
        return redirect('/edit/appointment/'+request.form['id'])
    
    Appointment.update(request.form)

    return redirect('/appointments')

@app.route('/delete/appointment/<int:id>')
def delete_appointment(id):
    if 'user_id' not in session:
        return redirect('/')

    formulario = {"id": id}
    Appointment.delete(formulario)

    return redirect('/appointments')
