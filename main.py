from flask import Flask, render_template, request
from forms import UserForm
from flask import flash
from flask_wtf.csrf import CSRFProtect
from flask import g
from config import DevelopmentConfig

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
  g.nombre = "Mario"
  print("Before 1")
 
@app.after_request
def after_reques(response):
  print("After 3")
  return response

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
  
  app.run()