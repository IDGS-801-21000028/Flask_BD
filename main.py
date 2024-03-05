from flask import Flask, render_template, request, redirect, url_for
from forms import *
from flask import flash
from flask_wtf.csrf import CSRFProtect
from flask import g
from config import DevelopmentConfig

from models import db
from models import Alumnos

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()

#21 de febrero de 2024
#Agregando un manejador de error
@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'),404

#Funciones before y after
@app.before_request
def before_request():
  g.nombre = "Diego"
 
@app.after_request
def after_reques(response):
  return response

@app.route("/", methods = ['GET','POST'])
def index():
  crate_form= UserForm2(request.form)
  if request.method == 'POST':
    alum = Alumnos(
      nombre=crate_form.nombre.data,
      apaterno = crate_form.apaterno.data,
      email = crate_form.email.data
    )    
    db.session.add(alum)
    db.session.commit()
    alum = Alumnos()  
  
  return render_template("index.html", form=crate_form)

@app.route("/eliminar", methods = ['GET','POST'])
def eliminar():
  create_form = UserForm2(request.form)
  if request.method == 'GET':
    id = request.args.get('id')
    alum1 = db.session.query(Alumnos).filter(Alumnos.id==id).first()
    create_form.id.data = request.args.get('id')
    create_form.nombre.data = alum1.nombre
    create_form.apaterno.data = alum1.apaterno
    create_form.email.data = alum1.email
  if request.method == 'POST':
    id = create_form.id.data    
    alumno = Alumnos.query.get(id)
    #delete from alumnos where id=id
    db.session.delete(alumno)
    db.session.commit()
    return redirect(url_for('ABC_Completo'))    
  return render_template("Eliminar.html", form=create_form)

@app.route("/modificar", methods = ['GET','POST'])
def modificar():
  create_form = UserForm2(request.form)
  if request.method == 'GET':
    id = request.args.get('id')
    alum1 = db.session.query(Alumnos).filter(Alumnos.id==id).first()
    create_form.id.data = request.args.get('id')
    create_form.nombre.data = alum1.nombre
    create_form.apaterno.data = alum1.apaterno
    create_form.email.data = alum1.email
  if request.method == 'POST':
    id = create_form.id.data    
    alumno = Alumnos.query.get(id)
    #delete from alumnos where id=id
    alumno.nombre = create_form.nombre.data
    alumno.apaterno =create_form.apaterno.data
    alumno.email = create_form.email.data
    db.session.add(alumno)
    db.session.commit()
    return redirect(url_for('ABC_Completo'))    
  return render_template("Modificar.html", form=create_form)

@app.route("/ABC_Completo", methods = ['GET','POST'])
def ABC_Completo():
  alumno = Alumnos.query.all()
  return render_template("ABC_Completo.html", alumno=alumno)

# Enviar datos del back al front
@app.route("/alumnos", methods = ['GET','POST'])
def alumnos():  
  alumno_clase = UserForm(request.form)  
  nom = ""
  apa = ""
  ama = ""
  edad = 0
  email = ""
  if request.method == 'POST' and alumno_clase.validate():
    nom = alumno_clase.nombre.data
    apa = alumno_clase.apaterno.data
    ama = alumno_clase.amaterno.data    
    email = alumno_clase.email.data
    edad = alumno_clase.edad.data 
    
    mensaje = "Bienvenido {} {}".format(nom, apa)
    flash(mensaje)
  
  print("Alumno: {}".format(g.nombre))
  return render_template("alumnos.html", form = alumno_clase, nom=nom, apa=apa, ama=ama, edad=edad, email=email)


if __name__ == "__main__":  
  csrf.init_app(app)  
  db.init_app(app)
  
  with app.app_context():
    db.create_all()
        
  app.run()