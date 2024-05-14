from flask import Flask, request, render_template, redirect, url_for, flash, session
from pymongo import MongoClient, collection
from bson.objectid import ObjectId

app = Flask(__name__, template_folder="./templates")
app.config['SECRET_KEY'] = "clave secreta"

elementsList = []

client = MongoClient('mongodb://localhost:27017/')
db = client['ProjectodbII_Ari']
examenes = db['examenes']
categorias = db['categorias']
indicaciones = db['user']

@app.route("/list", methods=["GET"])
def getList():
    elementsList = collection.find()

    return render_template('list.html.jinja', elementsList=elementsList)

#@app.route('/login', methods=['GET', 'POST'])#
#def login():
#    if request.method == 'POST':
#       username = request.form['username']
#        password = request.form['password'].encode()
#       user = user.find_one({'username': username, 'password': password})
#        if user:
#            session['user'] = username
#            return redirect('/')
#        else:
#            return render_template('login.html.jinja', mensaje='Credenciales incorrectas')
#    return render_template('login.html.jinja', mensaje='')

#@app.route('/')
#def index():
#    if 'username' in session:
#        return 'Bienvenido, ' + session['username']
#    else:
#       return redirect('/login')


@app.route('/exams')
def listar_examenes():
    lista_examenes = list(examenes.find())
    return render_template('lista_examenes.html', examenes=lista_examenes)

@app.route('/crear_examen', methods=['GET', 'POST'])
def crear_examen():
    if request.method == 'POST':
        codigo = request.form['codigo']
        categoria = request.form['categoria']
        tipo_muestra = request.form['tipo_muestra']
        precio = request.form['precio']
        indicaciones_lista = request.form.getlist('indicaciones')

        nuevo_examen = {
            'codigo': codigo,
            'categoria': categoria,
            'tipo_muestra': tipo_muestra,
            'precio': precio,
            'indicaciones': indicaciones_lista
        }
        examenes.insert_one(nuevo_examen)
        return redirect('/')
    else:
        categorias_lista = list(categorias.find())
        indicaciones_lista = list(indicaciones.find())
        return render_template('create_exam.html.jinja', categorias=categorias_lista, indicaciones=indicaciones_lista)
    
@app.route('/modificar_examen/<id>', methods=['GET', 'POST'])
def modificar_examen(id):
    examen = examenes.find_one({'_id': ObjectId(id)})
    if request.method == 'POST':
        codigo = request.form['codigo']
        categoria = request.form['categoria']
        tipo_muestra = request.form['tipo_muestra']
        precio = request.form['precio']
        indicaciones_lista = request.form.getlist('indicaciones')

        examenes.update_one({'_id': ObjectId(id)}, {'$set': {
            'codigo': codigo,
            'categoria': categoria,
            'tipo_muestra': tipo_muestra,
            'precio': precio,
            'indicaciones': indicaciones_lista
        }})
        return redirect('/')
    else:
        categorias_lista = list(categorias.find())
        indicaciones_lista = list(indicaciones.find())
        return render_template('modificar_examen.html', examen=examen, categorias=categorias_lista, indicaciones=indicaciones_lista)


@app.route('/<id>', methods=['GET'])
def get_element(id):
    oid = ObjectId(id)
    element = collection.find_one({'_id': oid})
    return render_template('detail.html.jinja', element = element)

@app.route('/update/<id>', methods=['GET', 'POST'])
def update_element(id):
    oid = ObjectId(id)
    element = collection.find_one({'_id': oid})
    if request.method == "POST":
        new_element = request.form
        collection.replace_one({'_id': oid}, 
                                         {'nombre': new_element['nombre'],
                                          'apellido': new_element['lastname'],
                                          'card': new_element['card'],
                                          'materia': new_element['subject'],
                                          'objetivo': new_element['objective'],
                                          'duracion': new_element['duration'],
                                          'nota': new_element['score']})    
        return redirect(url_for('getList'))
    return render_template("update.html.jinja", element=element)

@app.route('/delete/<id>', methods=['GET'])
def delete_element(id):
    oid = ObjectId(id)
    element = collection.delete_one({'_id': oid})
    return redirect(url_for('getList'))

if __name__ == "__main__":
    app.run(debug=True)