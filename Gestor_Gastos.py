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

    def limpiar_ventana(self):
    # Limpia la ventana principal borrando todos los widgets
        for widget in self.root.winfo_children():
            widget.destroy()



    #Brandon
    def crear_login(self):
        # Limpia cualquier widget o frame previo
        self.limpiar_ventana()
    
    # Crear un nuevo frame de login
        self.frame_login = tk.Frame(self.root, bg="#ffffff", highlightbackground="#2196f3", highlightthickness=2)
        self.frame_login.place(relx=0.5, rely=0.5, anchor="center", width=400, height=400)
    
    # Guardar referencia al frame actual
        self.frame_actual = self.frame_login
    

    # Intentar cargar la imagen
        try:
            imagen = Image.open("login.png")  # Cambia esto por la ruta correcta de tu imagen
            imagen = imagen.resize((70, 70), Image.Resampling.LANCZOS)
            self.imagen_login = ImageTk.PhotoImage(imagen)
            label_imagen = tk.Label(self.frame_login, image=self.imagen_login, bg="#ffffff")
            label_imagen.pack(pady=20)
        except Exception as e:
            print("Error al cargar la imagen:", e)

        label_imagen_texto = tk.Label(self.frame_login, text="Bienvenido", font=("Helvetica", 13, "bold"), bg="#ffffff", fg="#2196f3")
        label_imagen_texto.pack(pady=20)

        tk.Label(self.frame_login, text="Nombre de Usuario", bg="#ffffff", font=("Helvetica", 12, "bold")).pack(pady=5)
        self.entrada_usuario = tk.Entry(self.frame_login, font=("Helvetica", 12), bd=2, relief="solid")
        self.entrada_usuario.pack(pady=5)

        tk.Label(self.frame_login, text="Contraseña", bg="#ffffff", font=("Helvetica", 12, "bold")).pack(pady=5)
        self.entrada_contraseña = tk.Entry(self.frame_login, font=("Helvetica", 12), show="*", bd=2, relief="solid")
        self.entrada_contraseña.pack(pady=5)

        tk.Button(self.frame_login, text="Iniciar Sesión", bg="#4CAF50", fg="white", font=("Helvetica", 12), command=self.login).pack(pady=5)
        tk.Button(self.frame_login, text="Registrar Usuario", bg="#2196f3", fg="white", font=("Helvetica", 12), command=self.registrar_usuario).pack(pady=5)

    #Oscar
    """
    Maneja el proceso de inicio de sesión del usuario.
    
    - Verifica que los campos de nombre de usuario y contraseña no estén vacíos.
    - Valida las credenciales ingresadas contra la base de datos.
    - Si las credenciales son válidas, instancia al usuario y lo redirige a la interfaz de gastos.
    - Muestra un mensaje de error si las credenciales no son válidas.
    """
    def login(self):
        nombre = self.entrada_usuario.get().strip()
        contraseña = self.entrada_contraseña.get().strip()

        if not nombre or not contraseña:
            messagebox.showerror("Error", "El nombre de usuario y la contraseña son obligatorios.")
            return

        conn = sqlite3.connect('gastospersonales.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre_usuario, saldo FROM usuarios WHERE nombre_usuario = ? AND contraseña = ?", (nombre, contraseña))
        usuario_data = cursor.fetchone()
        conn.close()

        if usuario_data:
            usuario_id, nombre_usuario, saldo = usuario_data
            self.usuario = Usuario(nombre_usuario, saldo, contraseña, usuario_id)
            self.gestor = GestorDeGastos(self.usuario)
            self.crear_interfaz_gastos()
        else:
            messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos.") 

    """
    Cambia la interfaz actual del login a la interfaz de registro.
    - Elimina la ventana actual de login.
    - Muestra el formulario para registrar un nuevo usuario.
    """
    def registrar_usuario(self):
        self.frame_login.destroy()
        self.crear_interfaz_registro()

    """
    Valida si el texto ingresado en el campo de saldo es un número válido.
    
    - Permite solo caracteres numéricos o un campo vacío.
    - Retorna `True` si el texto es válido, de lo contrario, `False`.
    """
    def validar_saldo(self, texto):
        if texto.isdigit() or texto == "":
            return True
        else:
            return False
        
    """
    Crea la interfaz gráfica para registrar un nuevo usuario.
    
    - Contiene campos para nombre de usuario, contraseña, confirmación de contraseña y saldo inicial.
    - Proporciona botones para registrar al usuario o regresar a la ventana de login.
    """
    def crear_interfaz_registro(self):
        self.frame_registro = tk.Frame(self.root, bg="#ffffff")
        self.frame_registro.place(relx=0.5, rely=0.5, anchor="center", width=400, height=400)

        tk.Label(self.frame_registro, text="Registrar Usuario", font=("Helvetica", 16, "bold"), bg="#ffffff").pack(pady=10)
        tk.Label(self.frame_registro, text="Nombre de Usuario", bg="#ffffff").pack(pady=5)
        self.entrada_usuario_registro = tk.Entry(self.frame_registro)
        self.entrada_usuario_registro.pack(pady=5)

    # Campo de contraseña sin validación en tiempo real
        tk.Label(self.frame_registro, text="Contraseña", bg="#ffffff").pack(pady=5)
        self.entrada_contraseña_registro = tk.Entry(self.frame_registro, show="*")
        self.entrada_contraseña_registro.pack(pady=5)

        tk.Label(self.frame_registro, text="Confirmar Contraseña", bg="#ffffff").pack(pady=5)
        self.entrada_confirmar_contraseña = tk.Entry(self.frame_registro, show="*")
        self.entrada_confirmar_contraseña.pack(pady=5)

        tk.Label(self.frame_registro, text="Saldo Inicial", bg="#ffffff").pack(pady=5)
        self.entrada_saldo_registro = tk.Entry(self.frame_registro)
        self.entrada_saldo_registro.pack(pady=5)

        tk.Button(self.frame_registro, text="Registrar", bg="#4CAF50", fg="white", command=self.registrar).pack(pady=10)
        tk.Button(self.frame_registro, text="Volver al Login", bg="#2196f3", fg="white", command=self.crear_login).pack(pady=10)
        

    #Vladimir
    """
    Registra un nuevo usuario en la base de datos.
    
    - Valida los datos ingresados en el formulario de registro.
    - Verifica que el nombre de usuario no exista y que las contraseñas coincidan.
    - Guarda el nuevo usuario en la base de datos con el saldo inicial.
    - Muestra mensajes de éxito o error según corresponda.
    """
    def registrar(self):
        nombre = self.entrada_usuario_registro.get().strip()
        contraseña = self.entrada_contraseña_registro.get().strip()
        confirmar_contraseña = self.entrada_confirmar_contraseña.get().strip()
        saldo = self.entrada_saldo_registro.get().strip()

        if len(contraseña) < 8:
            messagebox.showerror('Error','La contraseña debe tener al menos 8 caracteres')
            return
        if not nombre or not contraseña or not confirmar_contraseña or not saldo:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if contraseña != confirmar_contraseña:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return
