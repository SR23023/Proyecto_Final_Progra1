import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3

# Clase Usuario
"""
 Representa un usuario con información personal y saldo.

    Atributos:
        - nombre (str): Nombre del usuario.
        - saldo (float): Cantidad de dinero disponible.
        - contraseña (str): Contraseña del usuario.
        - id_usuario (int): Identificador único del usuario.

    Métodos:
        - verificar_saldo(monto): Verifica si el usuario tiene saldo suficiente.
        - actualizar_saldo(monto): Reduce el saldo del usuario.
        - agregar_fondos(monto): Incrementa el saldo del usuario.
    
        Encapsulación (los datos y métodos del usuario están agrupados en la clase).
"""
class Usuario:
    def __init__(self, nombre, saldo, contraseña, id_usuario):
        self.nombre = nombre
        self.saldo = saldo
        self.contraseña = contraseña
        self.id_usuario = id_usuario

    def verificar_saldo(self, monto):
        return self.saldo >= monto

    def actualizar_saldo(self, monto):
        self.saldo -= monto

    def agregar_fondos(self, monto):
        self.saldo += monto


# Clase Gasto
    """
    Representa un gasto realizado por un usuario.

    Atributos:
        - descripcion (str): Detalle del gasto.
        - monto (float): Cantidad de dinero gastado.
        - categoria (str): Categoría del gasto (e.g., comida, transporte).

        Abstracción (simplifica el manejo de datos de un gasto en una estructura clara).
    """
class Gasto:
    def __init__(self, descripcion, monto, categoria):
        self.descripcion = descripcion
        self.monto = monto
        self.categoria = categoria

#Vladimir
# Clase GestorDeGastos
    """
    Administra los gastos y fondos de un usuario.

    Atributos:
        - usuario (Usuario): Usuario asociado al gestor.

    Métodos:
        - agregar_gasto(gasto): Registra un gasto si hay saldo suficiente.
        - agregar_fondos(monto): Añade fondos al saldo del usuario.

      Asociación (la clase está relacionada directamente con la clase Usuario).
    """
class GestorDeGastos:
    def __init__(self, usuario):
        self.usuario = usuario

    def agregar_gasto(self, gasto):
        if self.usuario.verificar_saldo(gasto.monto):
            conn = sqlite3.connect('gastospersonales.db')
            cursor = conn.cursor()
            cursor.execute('''  
                INSERT INTO historial_gastos (usuario_id, descripcion, cantidad, categoria)
                VALUES (?, ?, ?, ?)
            ''', (self.usuario.id_usuario, gasto.descripcion, gasto.monto, gasto.categoria))

            cursor.execute(''' 
                UPDATE usuarios SET saldo = ? WHERE id = ? 
            ''', (self.usuario.saldo - gasto.monto, self.usuario.id_usuario))

            conn.commit()
            conn.close()

            self.usuario.actualizar_saldo(gasto.monto)
            return True
        else:
            return False

    def agregar_fondos(self, monto):
        conn = sqlite3.connect('gastospersonales.db')
        cursor = conn.cursor()

        cursor.execute(''' 
            UPDATE usuarios SET saldo = ? WHERE id = ? 
        ''', (self.usuario.saldo + monto, self.usuario.id_usuario))

        conn.commit()
        conn.close()

        self.usuario.agregar_fondos(monto)

 
# Clase de la interfaz gráfica
    """
    Proporciona una interfaz gráfica para el gestor de gastos personales.

    Atributos:
        - root (tk.Tk): Ventana principal de la aplicación.

    Métodos:
        - crear_base_de_datos(): Crea las tablas necesarias en la base de datos.
        - limpiar_ventana(): Elimina los widgets de la ventana principal.
        - crear_login(): Muestra la interfaz de inicio de sesión.
    
     Modularidad (separación clara entre lógica y presentación).
    """
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Gastos Personales")
        self.root.geometry("900x650")
        self.root.configure(bg="#f0f4f7")
        self.frame_historial = None
        self.tabla_historial = None

   
        self.crear_base_de_datos()
        self.crear_login()

    def crear_base_de_datos(self):
        conn = sqlite3.connect('gastospersonales.db')
        cursor = conn.cursor()

        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_usuario TEXT UNIQUE NOT NULL,
                contraseña TEXT NOT NULL,
                saldo REAL DEFAULT 0.0
            )
        ''')

        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS historial_gastos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                descripcion TEXT NOT NULL,
                cantidad REAL NOT NULL,
                categoria TEXT NOT NULL,
                fecha TEXT DEFAULT (date('now')),
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        ''')

        conn.commit()
        conn.close()