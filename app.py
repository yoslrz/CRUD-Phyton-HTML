from flask import Flask
from flask import render_template,request,redirect
from flaskext.mysql import MySQL
from flask import send_from_directory
import os

app = Flask(__name__)

mysql = MySQL()
#Datos par la conexion de la base de datos
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='p_crud'
#Crea la conexion
mysql.init_app(app)

CARPETA = os.path.join('imagen')
app.config['CARPETA']= CARPETA

@app.route('/imagen/<nombre>')
def imagen(nombre):
    return send_from_directory(app.config['CARPETA'],nombre)

#mapeo de la aplicacion 
@app.route('/')
def inicio():
    sql = "SELECT * FROM `p_crud`.`persona`;"
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql)
    datos = cursor.fetchall()
    print(datos)
    conexion.commit() 
    #redirecciona a la pagina de inicio
    return render_template('crud/index.html',datos=datos)

#Eliminar Registro
@app.route('/borrar/<int:id>')
def borrar(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM persona WHERE id=%s", (id))
    conexion.commit()
    return redirect('/')

#metodo para acceder a la pantalla de actualizacion de informacion, carga datos
@app.route('/editar/<int:id>')
def editar(id):
   conexion = mysql.connect()
   cursor = conexion.cursor()
   cursor.execute("SELECT * FROM `p_crud`.`persona` WHERE id=%s",(id))
   datos = cursor.fetchall();
   print(datos)
   return render_template('crud/actualiza.html',datos=datos)


#Actualiza la informacion de la bd
@app.route('/actualiza', methods=['POST'])
def actualiza():
    nombre = request.form['nombre']
    apellido_pat = request.form['apellido_pat']
    apellido_mat = request.form['apellido_mat']
    cargo = request.form['cargo']
    correo= request.form['correo']
    ide = request.form['id']
    datos = (nombre,apellido_pat,apellido_mat,cargo,correo,ide)
    sql = "UPDATE `p_crud`.`persona` SET `nombre` =%s, `apellido_pat`=%s, `apellido_mat`=%s, `cargo`=%s, `correo`=%s WHERE id=%s;"
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit() 
    return redirect('/')

#Accede a pantalla de registro
@app.route('/registro')
def registro():
    return render_template('crud/registro.html')

#Obtine informacion del formulario y la guarda en la base de datos 
@app.route('/guardar', methods=['POST'])
def guarda():
    #obtencion de Datos del formulario
    nombre = request.form['nombre']
    apellido_pat = request.form['apellido_pat']
    apellido_mat = request.form['apellido_mat']
    cargo = request.form['cargo']
    correo= request.form['correo']
    datos = (nombre,apellido_pat,apellido_mat,cargo,correo)
    #Ingreso a la base de datos
    sql = "INSERT INTO `p_crud`.`persona` (`nombre`, `apellido_pat`, `apellido_mat`, `cargo`, `correo`) VALUES ( %s, %s, %s, %s, %s);"
    #crea la conexion
    conexion = mysql.connect()
    #guarda la informacion de los datos
    cursor = conexion.cursor()
    #ejecuta
    cursor.execute(sql,datos)
    #guarda los cambios
    conexion.commit() 
    return redirect('/')

#corre aplicacion 
if __name__ == '__main__':
    app.run(debug=True)