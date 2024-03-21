
# Para subir archivo tipo foto al servidor
from werkzeug.utils import secure_filename
import uuid  # Modulo de python para crear un string

from conexion.conexionBD import connectionBD  # Conexión a BD

import datetime
import re
import os

from os import remove  # Modulo  para remover archivo
from os import path  # Modulo para obtener la ruta o directorio


import openpyxl  # Para generar el excel
# biblioteca o modulo send_file para forzar la descarga
from flask import send_file


# Lista de Usuarios creados
def lista_usuariosBD():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "SELECT id, name_surname, email_user, created_user FROM users"
                cursor.execute(querySQL,)
                usuariosBD = cursor.fetchall()
        return usuariosBD
    except Exception as e:
        print(f"Error en lista_usuariosBD : {e}")
        return []



# Eliminar usuario
def eliminarUsuario(id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "DELETE FROM users WHERE id=%s"
                cursor.execute(querySQL, (id,))
                conexion_MySQLdb.commit()
                resultado_eliminar = cursor.rowcount

        return resultado_eliminar
    except Exception as e:
        print(f"Error en eliminarUsuario : {e}")
        return []
    

# Lista de Categorías
def sql_lista_categoriasBD():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = ("""
                    SELECT 
                        id,
                        nombre
                    FROM categoria
                    ORDER BY id DESC
                    """)
                cursor.execute(querySQL,)
                categoriasBD = cursor.fetchall()
        return categoriasBD
    except Exception as e:
        print(f"Error en la función sql_lista_categoriasBD: {e}")
        return None

def procesar_form_categoria(dataForm):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                sql = "INSERT INTO categoria (nombre) VALUES (%s)"
                valores = (dataForm['nombre_categoria'],)
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                resultado_insert = cursor.rowcount
                return resultado_insert
    except Exception as e:
         return f'Se produjo un error en procesar_form_categoria: {str(e)}'


def buscarCategoriaBD(search):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = ("""
                    SELECT 
                        id,
                        nombre
                    FROM categoria
                    WHERE nombre LIKE %s 
                    ORDER BY id DESC
                """)
                search_pattern = f"%{search}%"
                cursor.execute(querySQL, (search_pattern,))
                resultado_busqueda = cursor.fetchall()
                return resultado_busqueda
    except Exception as e:
        print(f"Ocurrió un error en buscarCategoriaBD: {e}")
        return []

def buscarCategoriaUnica(id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = ("SELECT id, nombre FROM categoria WHERE id = %s LIMIT 1")
                cursor.execute(querySQL, (id,))
                categoria = cursor.fetchone()
                return categoria
    except Exception as e:
        print(f"Ocurrió un error en buscarCategoriaUnica: {e}")
        return None

def procesar_actualizacion_form_categoria(data):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                nombre_categoria = data.form['nombre_categoria']
                id_categoria = data.form['id_categoria']
                querySQL = "UPDATE categoria SET nombre = %s WHERE id = %s"
                values = (nombre_categoria, id_categoria)
                cursor.execute(querySQL, values)
                conexion_MySQLdb.commit()
                return cursor.rowcount or []
    except Exception as e:
        print(f"Ocurrió un error en procesar_actualizacion_form_categoria: {e}")
        return None

def eliminarCategoria(id_categoria):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "DELETE FROM categoria WHERE id = %s"
                cursor.execute(querySQL, (id_categoria,))
                conexion_MySQLdb.commit()
                return cursor.rowcount
    except Exception as e:
        print(f"Error en eliminarCategoria: {e}")
        return None

# Lista de Categorías
def sql_lista_categoriasBD():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = ("""
                    SELECT 
                        id,
                        nombre
                    FROM categoria
                    ORDER BY id DESC
                    """)
                cursor.execute(querySQL,)
                categoriasBD = cursor.fetchall()
        return categoriasBD
    except Exception as e:
        print(f"Error en la función sql_lista_categoriasBD: {e}")
        return None

########################################################



    # Lista de Noticias
def sql_lista_noticiasBD():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = ("""
                    SELECT 
                        id,
                        titulo,
                        contenido,
                        fecha_publicacion,
                        autor,
                        categoria_id,
                        precio
                    FROM noticia
                    ORDER BY id DESC
                    """)
                cursor.execute(querySQL,)
                noticiasBD = cursor.fetchall()
        return noticiasBD
    except Exception as e:
        print(f"Error en la función sql_lista_noticiasBD: {e}")
        return None

def procesar_form_noticia(dataForm):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                sql = "INSERT INTO noticia (titulo, contenido, fecha_publicacion, autor, categoria_id, precio) VALUES (%s, %s, %s, %s, %s, %s)"
                # Asegúrate de que los nombres aquí coincidan con los atributos 'name' de tu formulario HTML.
                valores = (dataForm['titulo_noticia'], dataForm['contenido_noticia'], dataForm['fecha_publicacion'], dataForm['autor_noticia'], dataForm['categoria_noticia'], dataForm['precio_noticia'])
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                resultado_insert = cursor.rowcount
                return resultado_insert
    except Exception as e:
         return f'Se produjo un error en procesar_form_noticia: {str(e)}'


def buscarNoticiaBD(search):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = ("""
                    SELECT 
                        id,
                        titulo,
                        contenido,
                        fecha_publicacion,
                        autor,
                        categoria_id,
                        precio
                    FROM noticia
                    WHERE titulo LIKE %s OR contenido LIKE %s OR autor LIKE %s
                    ORDER BY id DESC
                """)
                search_pattern = f"%{search}%"
                cursor.execute(querySQL, (search_pattern, search_pattern, search_pattern))
                resultado_busqueda = cursor.fetchall()
                return resultado_busqueda
    except Exception as e:
        print(f"Ocurrió un error en buscarNoticiaBD: {e}")
        return []

def buscarNoticiaUnica(id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = ("SELECT id, titulo, contenido, fecha_publicacion, autor, categoria_id, precio FROM noticia WHERE id = %s LIMIT 1")
                cursor.execute(querySQL, (id,))
                noticia = cursor.fetchone()
                return noticia
    except Exception as e:
        print(f"Ocurrió un error en buscarNoticiaUnica: {e}")
        return None

def procesar_actualizacion_form_noticia(data):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Asegúrate de que estos nombres coincidan con los del formulario
                titulo = data.form['titulo_noticia']
                contenido = data.form['contenido_noticia']
                fecha_publicacion = data.form['fecha_publicacion']
                autor = data.form['autor_noticia']
                categoria_id = data.form['categoria_noticia']
                precio = data.form['precio_noticia']
                id_noticia = data.form['id_noticia']
                
                querySQL = "UPDATE noticia SET titulo = %s, contenido = %s, fecha_publicacion = %s, autor = %s, categoria_id = %s, precio = %s WHERE id = %s"
                values = (titulo, contenido, fecha_publicacion, autor, categoria_id, precio, id_noticia)
                
                cursor.execute(querySQL, values)
                conexion_MySQLdb.commit()
                
                return cursor.rowcount
    except Exception as e:
        print(f"Ocurrió un error en procesar_actualizacion_form_noticia: {e}")
        return None


def eliminarNoticia(id_noticia):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "DELETE FROM noticia WHERE id = %s"
                cursor.execute(querySQL, (id_noticia,))
                conexion_MySQLdb.commit()
                return cursor.rowcount
    except Exception as e:
        print(f"Error en eliminarNoticia: {e}")
        return None
###############################################################
    
def sql_lista_comentariosBD():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = ("""
                    SELECT 
                        id,
                        autor,
                        contenido,
                        fecha_creacion,
                        noticia_id
                    FROM comentario
                    ORDER BY id DESC
                    """)
                cursor.execute(querySQL,)
                comentariosBD = cursor.fetchall()
        return comentariosBD
    except Exception as e:
        print(f"Error en la función sql_lista_comentariosBD: {e}")
        return None

def procesar_form_comentario(dataForm):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                sql = "INSERT INTO comentario (autor, contenido, fecha_creacion, noticia_id) VALUES (%s, %s, %s, %s)"
                # Asegúrate de que los nombres aquí coincidan con los atributos 'name' de tu formulario HTML.
                valores = (dataForm['autor_comentario'], dataForm['contenido_comentario'], dataForm['fecha_creacion'], dataForm['noticia_id'])
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                resultado_insert = cursor.rowcount
                return resultado_insert
    except Exception as e:
        return f'Se produjo un error en procesar_form_comentario: {str(e)}'


def buscarComentarioBD(search):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = ("""
                    SELECT 
                        id,
                        autor,
                        contenido,
                        fecha_creacion,
                        noticia_id
                    FROM comentario
                    WHERE autor LIKE %s OR contenido LIKE %s
                    ORDER BY id DESC
                """)
                search_pattern = f"%{search}%"
                cursor.execute(querySQL, (search_pattern, search_pattern))
                resultado_busqueda = cursor.fetchall()
                return resultado_busqueda
    except Exception as e:
        print(f"Ocurrió un error en buscarComentarioBD: {e}")
        return []

def buscarComentarioUnico(id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = ("SELECT id, autor, contenido, fecha_creacion, noticia_id FROM comentario WHERE id = %s LIMIT 1")
                cursor.execute(querySQL, (id,))
                comentario = cursor.fetchone()
                return comentario
    except Exception as e:
        print(f"Ocurrió un error en buscarComentarioUnico: {e}")
        return None

def procesar_actualizacion_form_comentario(data):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Asegúrate de que estos nombres coincidan con los del formulario
                autor = data.form['autor_comentario']
                contenido = data.form['contenido_comentario']
                fecha_creacion = data.form['fecha_creacion']
                noticia_id = data.form['noticia_id']
                id_comentario = data.form['id_comentario']
                
                querySQL = "UPDATE comentario SET autor = %s, contenido = %s, fecha_creacion = %s, id = %s WHERE id = %s"
                values = (autor, contenido, fecha_creacion, noticia_id, id_comentario)
                
                cursor.execute(querySQL, values)
                conexion_MySQLdb.commit()
                
                return cursor.rowcount
    except Exception as e:
        print(f"Ocurrió un error en procesar_actualizacion_form_comentario: {e}")
        return None


def eliminarComentario(id_comentario):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "DELETE FROM comentario WHERE id = %s"
                cursor.execute(querySQL, (id_comentario,))
                conexion_MySQLdb.commit()
                return cursor.rowcount
    except Exception as e:
        print(f"Error en eliminarComentario: {e}")
        return None
