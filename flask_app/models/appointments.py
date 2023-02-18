from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

from datetime import datetime

class Appointment:

    def __init__(self, data):
        self.id = data['id']
        self.task = data['task']
        self.date = data['date']
        self.status = data['status']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @staticmethod
    def valida_appointment(formulario):
        es_valido = True

        if formulario['task'] == '':
            flash('Task is not empty', 'appointments')
            es_valido = False
        
        if formulario['status'] == '':
            flash('Please assign status', 'appointments')
            es_valido = False
                
        if formulario['date'] == '':
            flash('Enter a valid date', 'appointments')
            es_valido = False
        else:
            fecha_obj = datetime.strptime(formulario['date'], '%Y-%m-%d')
            hoy = datetime.now()
            if hoy > fecha_obj:
                flash('The date must be in the future', 'appointments')
                es_valido = False
        
        return es_valido
    
    @classmethod
    def get_by_id(cls, formulario):
        query = "SELECT * FROM appointments WHERE id = %(id)s"
        result = connectToMySQL('belt_exam').query_db(query, formulario)
        appointment = cls(result[0])
        return appointment

    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO appointments (task, date, status, user_id) VALUES (%(task)s, %(date)s, %(status)s, %(user_id)s)"
        result = connectToMySQL('belt_exam').query_db(query, formulario)
        return result
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM appointments WHERE DATE(date)>=(NOW())"
        results = connectToMySQL('belt_exam').query_db(query)
        appointments = []

        for appointment in results:
            appointments.append(cls(appointment))
        
        return appointments

    @classmethod
    def get_by_date(cls):
        query = "SELECT * FROM appointments WHERE DATE(date) < DATE(NOW())"
        results = connectToMySQL('belt_exam').query_db(query)
        dates = []

        for date in results:
            dates.append(cls(date))
        
        return dates
    

    @classmethod
    def update(cls, formulario):
        query = "UPDATE appointments SET task=%(task)s, date=%(date)s, status=%(status)s, user_id=%(user_id)s WHERE id=%(id)s"
        result = connectToMySQL('belt_exam').query_db(query, formulario)
        return result
    

    @classmethod
    def delete(cls, formulario):
        query = "DELETE FROM appointments WHERE id = %(id)s"
        result = connectToMySQL('belt_exam').query_db(query, formulario)
        return result
