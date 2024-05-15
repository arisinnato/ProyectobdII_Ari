from flask import Flask, request, render_template, redirect, url_for, flash, session
from pymongo import MongoClient, collection
from bson.objectid import ObjectId
from collections import defaultdict

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

######################################## EXAMENES ################################################################################

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
        return render_template('mod_examen.html.jinja', examen=examen, categorias=categorias_lista, indicaciones=indicaciones_lista)

@app.route('/consultar_examen/<id>')
def consultar_examen(id):
    examen = examenes.find_one({'_id': ObjectId(id)})
    return render_template('consultar_examen.html', examen=examen)

################################# CATEGORIA ###############################################

@app.route('/crear_categoria', methods=['GET', 'POST'])
def crear_categoria():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']

        nueva_categoria = {
            'nombre': nombre,
            'descripcion': descripcion
        }
        categorias.insert_one(nueva_categoria)
        return redirect('/')
    else:
        return render_template('crear_categoria.html')

@app.route('/modificar_categoria/<id>', methods=['GET', 'POST'])
def modificar_categoria(id):
    categoria = categorias.find_one({'_id': ObjectId(id)})
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']

        categorias.update_one({'_id': ObjectId(id)}, {'$set': {
            'nombre': nombre,
            'descripcion': descripcion
        }})
        return redirect('/')
    else:
        return render_template('modificar_categoria.html', categoria=categoria)

@app.route('/eliminar_categoria/<id>', methods=['POST'])
def eliminar_categoria(id):
    categorias.delete_one({'_id': ObjectId(id)})
    return redirect('/')


################################ CATALOGO ###########################################

@app.route('/consultar_catalogo', methods=['GET', 'POST'])
def consultar_catalogo():
    if request.method == 'GET':
        filtro_categoria = request.args.get('filtro_categoria')
        if filtro_categoria:
            examenes_filtrados = examenes.find({'categoria': filtro_categoria})
        else:
            examenes_filtrados = examenes.find()

        lista_examenes = list(examenes_filtrados)
        return render_template('consultar_catalogo.html', examenes=lista_examenes, categorias=categorias.find())


############################################ REPORTE ##############################################

@app.route('/ver_reporte')
def ver_reporte():
    # Cantidad de exámenes por categoría
    cantidad_por_categoria = defaultdict(int)
    for examen in examenes.find():
        cantidad_por_categoria[examen['categoria']] += 1

    # Indicación de examen más común
    indicaciones_frecuencia = defaultdict(int)
    for examen in examenes.find():
        for indicacion in examen['indicaciones']:
            indicaciones_frecuencia[indicacion] += 1
    indicacion_mas_comun = max(indicaciones_frecuencia, key=indicaciones_frecuencia.get)

    # Lista de exámenes por precio según intervalos
    cantidad_por_intervalo = defaultdict(int)
    for examen in examenes.find():
        precio = examen['precio']
        if precio <= 100:
            cantidad_por_intervalo['1 - 100 bs'] += 1
        elif precio <= 200:
            cantidad_por_intervalo['101 - 200 bs'] += 1
        elif precio <= 300:
            cantidad_por_intervalo['201 - 300 bs'] += 1
        elif precio <= 500:
            cantidad_por_intervalo['301 - 500 bs'] += 1
        else:
            cantidad_por_intervalo['501+ bs'] += 1

    return render_template('ver_reporte.html', cantidad_por_categoria=cantidad_por_categoria, indicacion_mas_comun=indicacion_mas_comun, cantidad_por_intervalo=cantidad_por_intervalo)






#@app.route('/<id>', methods=['GET'])
#def get_element(id):
#    oid = ObjectId(id)
#    element = collection.find_one({'_id': oid})
 #   return render_template('detail.html.jinja', element = element)

#@app.route('/update/<id>', methods=['GET', 'POST'])
#def update_element(id):
 #   oid = ObjectId(id)
 #   element = collection.find_one({'_id': oid})
 #   if request.method == "POST":
 #       new_element = request.form
 #       collection.replace_one({'_id': oid}, 
  #                                       {'nombre': new_element['nombre'],
  #                                        'apellido': new_element['lastname'],
 #                                         'card': new_element['card'],
 #                                         'materia': new_element['subject'],
  #                                        'objetivo': new_element['objective'],
  #                                        'duracion': new_element['duration'],
   #                                       'nota': new_element['score']})    
   #     return redirect(url_for('getList'))
 #   return render_template("update.html.jinja", element=element)

#@app.route('/delete/<id>', methods=['GET'])
#def delete_element(id):
 #   oid = ObjectId(id)
 #   element = collection.delete_one({'_id': oid})
 #   return redirect(url_for('getList'))

if __name__ == "__main__":
    app.run(debug=True)