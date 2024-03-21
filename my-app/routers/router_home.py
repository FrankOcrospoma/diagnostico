from app import app
from flask import render_template, request, flash, redirect, url_for, session,  jsonify
from mysql.connector.errors import Error


# Importando cenexión a BD
from controllers.funciones_home import *

PATH_URL_CATEGORIA = "public/categorias"
PATH_URL_NOTICIA = "public/noticias"
PATH_URL_COMENTARIO = "public/comentarios"




@app.route("/lista-de-usuarios", methods=['GET'])
def usuarios():
    if 'conectado' in session:
        resp_usuariosBD = lista_usuariosBD()
        return render_template('public/usuarios/lista_usuarios.html', resp_usuariosBD=resp_usuariosBD)
    else:
        return redirect(url_for('inicioCpanel'))


@app.route('/borrar-usuario/<string:id>', methods=['GET'])
def borrarUsuario(id):
    resp = eliminarUsuario(id)
    if resp:
        flash('El Usuario fue eliminado correctamente', 'success')
        return redirect(url_for('usuarios'))



@app.route('/registrar-categoria', methods=['GET'])
def viewFormCategoria():
    if 'conectado' in session:
        return render_template(f'{PATH_URL_CATEGORIA}/form_categorias.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

@app.route('/form-registrar-categoria', methods=['POST'])
def formCategoria():
    if 'conectado' in session:
            resultado = procesar_form_categoria(request.form)
            if resultado:
                print(resultado)
                return redirect(url_for('crud_categoria'))
            else:
                flash('La categoria NO fue registrada.', 'error')
                return render_template(f'{PATH_URL_CATEGORIA}/form_categorias.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    
@app.route('/crud_categoria', methods=['GET'])
def crud_categoria():
    if 'conectado' in session:
        return render_template(f'{PATH_URL_CATEGORIA}/categorias.html', categorias=sql_lista_categoriasBD())
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Buscando categorías
@app.route("/buscando-categoria", methods=['POST'])
def viewBuscarCategoriaBD():
    resultadoBusqueda = buscarCategoriaBD(request.json['busqueda'])
    if resultadoBusqueda:
        return render_template(f'{PATH_URL_CATEGORIA}/resultado_busqueda_categoria.html', dataBusqueda=resultadoBusqueda)
    else:
        return jsonify({'fin': 0})


@app.route("/editar-categoria/<int:id>", methods=['GET'])
def viewEditarCategoria(id):
    if 'conectado' in session:
        respuestaCategoria = buscarCategoriaUnica(id)
        if respuestaCategoria:
            return render_template(f'{PATH_URL_CATEGORIA}/form_categorias_update.html', respuestaCategoria=respuestaCategoria)
        else:
            flash('La categoría no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Recibir formulario para actualizar información de categoría
@app.route('/actualizar-categoria', methods=['POST'])
def actualizarCategoria():
    resultData = procesar_actualizacion_form_categoria(request)
    return redirect(url_for('crud_categoria'))

@app.route('/borrar-categoria/<int:id_categoria>', methods=['GET'])
def borrarCategoria(id_categoria):
    resp = eliminarCategoria(id_categoria)
    if resp:
        flash('La categoría fue eliminada correctamente', 'success')
        return redirect(url_for('crud_categoria'))


##################################################
@app.route('/registrar-noticia', methods=['GET'])
def viewFormNoticia():
    if 'conectado' in session:
        categorias = sql_lista_categoriasBD()  # Obtener la lista de categorías
        return render_template(f'{PATH_URL_NOTICIA}/form_noticias.html', categorias=categorias)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

@app.route('/form-registrar-noticia', methods=['POST'])
def formNoticia():
    if 'conectado' in session:
            resultado = procesar_form_noticia(request.form)
            if resultado:
                print(resultado)
                return redirect(url_for('crud_noticia'))
            else:
                flash('La noticia NO fue registrada.', 'error')
                return render_template(f'{PATH_URL_NOTICIA}/form_noticias.html')
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    
@app.route('/crud-noticia', methods=['GET'])
def crud_noticia():
    if 'conectado' in session:
        return render_template(f'{PATH_URL_NOTICIA}/noticias.html', noticias=sql_lista_noticiasBD(), buscarCategoriaUnica=buscarCategoriaUnica)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))



# Buscando noticias
@app.route("/buscando-noticia", methods=['POST'])
def viewBuscarNoticiaBD():
    resultadoBusqueda = buscarNoticiaBD(request.json['busqueda'])
    if resultadoBusqueda:
        return render_template(f'{PATH_URL_NOTICIA}/resultado_busqueda_noticia.html', dataBusqueda=resultadoBusqueda, buscarCategoriaUnica=buscarCategoriaUnica )
    else:
        return jsonify({'fin': 0})


@app.route("/editar-noticia/<int:id>", methods=['GET'])
def viewEditarNoticia(id):
    if 'conectado' in session:
        
        respuestaNoticia = buscarNoticiaUnica(id)
        categorias = sql_lista_categoriasBD()  # Obtener la lista de categorías
        if respuestaNoticia:
            return render_template(f'{PATH_URL_NOTICIA}/form_noticias_update.html', respuestaNoticia=respuestaNoticia, categorias=categorias)
        else:
            flash('La noticia no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# Recibir formulario para actualizar información de noticia
@app.route('/actualizar-noticia', methods=['POST'])
def actualizarNoticia():
    resultData = procesar_actualizacion_form_noticia(request)
    return redirect(url_for('crud_noticia'))

@app.route('/borrar-noticia/<int:id_noticia>', methods=['GET'])
def borrarNoticia(id_noticia):
    resp = eliminarNoticia(id_noticia)
    if resp:
        flash('La noticia fue eliminada correctamente', 'success')
        return redirect(url_for('crud_noticia'))

###############################################################
    
@app.route('/registrar-comentario', methods=['GET'])
def viewFormComentario():
    if 'conectado' in session:
        noticias = sql_lista_noticiasBD()  # Obtener la lista de categorías

        return render_template(f'{PATH_URL_COMENTARIO}/form_comentarios.html', noticias = noticias)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

@app.route('/form-registrar-comentario', methods=['POST'])
def formComentario():
    if 'conectado' in session:

            resultado = procesar_form_comentario(request.form)
            if resultado:
                print(resultado)
                return redirect(url_for('crud_comentario'))
            else:
                flash('El comentario NO fue registrado.', 'error')
                return render_template(f'{PATH_URL_COMENTARIO}/form_comentarios.html')
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    
@app.route('/crud-comentario', methods=['GET'])
def crud_comentario():
    if 'conectado' in session:
        return render_template(f'{PATH_URL_COMENTARIO}/comentarios.html', comentarios=sql_lista_comentariosBD(), buscarNoticiaUnica = buscarNoticiaUnica)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# Buscando comentarios
@app.route("/buscando-comentario", methods=['POST'])
def viewBuscarComentarioBD():
    resultadoBusqueda = buscarComentarioBD(request.json['busqueda'])
    if resultadoBusqueda:
        return render_template(f'{PATH_URL_COMENTARIO}/resultado_busqueda_comentario.html', dataBusqueda=resultadoBusqueda,buscarNoticiaUnica=buscarNoticiaUnica)
    else:
        return jsonify({'fin': 0})


@app.route("/editar-comentario/<int:id>", methods=['GET'])
def viewEditarComentario(id):
    if 'conectado' in session:
        respuestaComentario = buscarComentarioUnico(id)
        noticias = sql_lista_noticiasBD()
        if respuestaComentario:
            return render_template(f'{PATH_URL_COMENTARIO}/form_comentarios_update.html', respuestaComentario=respuestaComentario, noticias=noticias)
        else:
            flash('El comentario no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# Recibir formulario para actualizar información de comentario
@app.route('/actualizar-comentario', methods=['POST'])
def actualizarComentario():
    resultData = procesar_actualizacion_form_comentario(request)
    return redirect(url_for('crud_comentario'))

@app.route('/borrar-comentario/<int:id_comentario>', methods=['GET'])
def borrarComentario(id_comentario):
    resp = eliminarComentario(id_comentario)
    if resp:
        flash('El comentario fue eliminado correctamente', 'success')
        return redirect(url_for('crud_comentario'))
