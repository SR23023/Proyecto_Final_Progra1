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
          

         try:
            saldo = float(saldo)
            if saldo <= 0:
                messagebox.showerror("Error", "El saldo inicial debe ser un numero positivo mayor que cero")
                return
        except ValueError:
            messagebox.showerror("Error", "Saldo inicial valido")
            return

        conn = sqlite3.connect('gastospersonales.db')
        cursor = conn.cursor()

        try:
             cursor.execute("INSERT INTO usuarios (nombre_usuario, contraseña, saldo) VALUES (?, ?, ?)", (nombre, contraseña, saldo))
             conn.commit()
             messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
             self.frame_registro.destroy()
             self.crear_login()
        except sqlite3.IntegrityError:
             messagebox.showerror("Error", "El usuario ya existe.")
        finally:
             conn.close()
            
    #Brandon
    """"
    Se representa una interfaz gráfica para gestionar gastos personales. Utiliza el módulo tkinter 
    para construir la interfaz y sqlite3 para manejar la persistencia de datos.

    Registra un nuevo usuario en la base de datos.
    
       - Valida los datos ingresados en el formulario de registro.
       - Verifica que el nombre de usuario no exista y que las contraseñas coincidan.
       - Guarda el nuevo usuario en la base de datos con el saldo inicial.
       - Muestra mensajes de éxito o error según corresponda.
    """
    def crear_interfaz_gastos(self):
        self.limpiar_ventana()

        self.frame_gastos = tk.Frame(self.root, bg="#e8f5e9", padx=20, pady=20)
        self.frame_gastos.pack(fill="both", expand=True)

        # Barra superior con bienvenida
        self.bienvenida_label = tk.Label(self.frame_gastos, text=f"Bienvenido {self.usuario.nombre}", font=("Arial", 14, "bold"), bg="#2196f3", fg="#ffffff")
        self.bienvenida_label.pack(fill="x", pady=5)

        self.etiqueta_saldo = tk.Label(self.frame_gastos, text=f"Saldo Actual: ${self.usuario.saldo:.2f}", font=("Arial", 12), bg="#ffffff", fg="#333333")
        self.etiqueta_saldo.pack(pady=10)


        # Sección para agregar gastos
        self.frame_agregar_gasto = tk.Frame(self.frame_gastos, bg="#ffffff", pady=10)
        self.frame_agregar_gasto.pack(fill="x", padx=10, pady=10)

        tk.Label(self.frame_agregar_gasto, text="Descripción:", font=("Arial", 12), bg="#ffffff", fg="#333333").grid(row=0, column=0, padx=10, pady=5)
        self.entrada_descripcion = tk.Entry(self.frame_agregar_gasto, font=("Arial", 12), bd=2, relief="solid")
        self.entrada_descripcion.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.frame_agregar_gasto, text="Monto:", font=("Arial", 12), bg="#ffffff", fg="#333333").grid(row=1, column=0, padx=10, pady=5)
        self.entrada_monto = tk.Entry(self.frame_agregar_gasto, font=("Arial", 12), bd=2, relief="solid")
        self.entrada_monto.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.frame_agregar_gasto, text="Categoría:", font=("Arial", 12), bg="#ffffff", fg="#333333").grid(row=2, column=0, padx=10, pady=5)
        self.categorias = ["Alimentos", "Transporte", "Entretenimiento", "Otros", "Hogar", "Medicamentos"]
        self.entrada_categoria = ttk.Combobox(self.frame_agregar_gasto, values=self.categorias, font=("Arial", 12))
        self.entrada_categoria.grid(row=2, column=1, padx=10, pady=5)
        self.entrada_categoria.current(0)

        self.entrada_otro = tk.Entry(self.frame_agregar_gasto, font=("Arial", 12), bd=2, relief="solid")
        self.entrada_otro.grid(row=3, column=1, padx=10, pady=5)
        self.entrada_otro.grid_remove()  # Ocultar el cuadro de texto inicialmente

    #Oscar
    # Gestión de eventos:
        """Se conecta un evento de selección de categoría en un combobox a la función `manejar_categoria_seleccionada`.
            Los botones ejecutan distintas funciones como agregar gastos, agregar fondos, borrar el historial, y cerrar sesión.Conectar el evento de selección del combobox a una función
            self.entrada_categoria.bind("<<ComboboxSelected>>", self.manejar_categoria_seleccionada)
        """
     # Botón para agregar el gasto
        tk.Button(self.frame_agregar_gasto, text="Agregar Gasto", bg="#4CAF50", fg="white", font=("Arial", 12), command=self.agregar_gasto).grid(row=4, columnspan=2, pady=10)


        # Sección para agregar fondos
        # Sección para agregar fondos
        self.frame_fondos = tk.Frame(self.frame_gastos, bg="#ffffff", pady=10)
        self.frame_fondos.pack(fill="x", padx=10, pady=10)

    # Agregar campos para ingresar descripción y monto de fondos
        tk.Label(self.frame_fondos, text="Descripción:", font=("Arial", 12), bg="#ffffff", fg="#333333").grid(row=0, column=0, padx=10, pady=5)
        self.entrada_descripcion_fondo = tk.Entry(self.frame_fondos, font=("Arial", 12), bd=2, relief="solid")
        self.entrada_descripcion_fondo.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.frame_fondos, text="Monto a agregar:", font=("Arial", 12), bg="#ffffff", fg="#333333").grid(row=1, column=0, padx=10, pady=5)
        self.entrada_monto_fondo = tk.Entry(self.frame_fondos, font=("Arial", 12), bd=2, relief="solid")
        self.entrada_monto_fondo.grid(row=1, column=1, padx=10, pady=5)

    # Botón para agregar fondos
        tk.Button(self.frame_fondos, text="Agregar Fondos", bg="#2196f3", fg="white", font=("Arial", 12), command=self.agregar_fondos).grid(row=2, columnspan=2, pady=10)

        # Función `crear_historial`: Genera un componente visual tipo tabla para mostrar los gastos registrados.
        self.crear_historial()

        tk.Button(self.frame_gastos, text="Cerrar Sesión", bg="#f44336", fg="white", font=("Arial", 12), command=self.cerrar_sesion).pack(side="right", padx=10,pady=10)
        tk.Button(self.frame_gastos, text="Borrar Historial", bg="#f44336", fg="white", font=("Arial", 12), command=self.borrar_historial).pack(side="left", padx=10,pady=10)

        self.crear_historial()

    #Vladimir
    #Función `borrar_historial`: Elimina los registros del historial desde la base de datos.
    def borrar_historial(self):
        # Confirmación antes de borrar el historial
        respuesta = messagebox.askyesno("Confirmación", "¿Estás seguro de que deseas borrar todo el historial de gastos?")
        
        if respuesta:  # Si el usuario confirma, procedemos
            try:
                # Conectar a la base de datos y eliminar los registros del historial
                # Utiliza sqlite3 para almacenar y recuperar datos, asegurando la persistencia entre sesiones.

                conn = sqlite3.connect('gastospersonales.db')
                cursor = conn.cursor()
                cursor.execute("DELETE FROM historial_gastos WHERE usuario_id = ?", (self.usuario.id_usuario,))
                conn.commit()
                conn.close()

                # Actualizar la vista del historial (vaciar la tabla)
                self.crear_historial()

                # Mostrar mensaje de éxito
                messagebox.showinfo("Éxito", "Historial de gastos borrado correctamente.")
            
            except sqlite3.Error as e:
                # Manejo de errores de la base de datos
                messagebox.showerror("Error", f"Hubo un error al borrar el historial: {e}")
    #Brandon
        """
        Función que se activa cuando se selecciona una categoría en el combobox.
        - Si la categoría seleccionada es "Otros", muestra un campo adicional (`entrada_otro`) para ingresar más detalles.
        - Si no, oculta dicho campo.

        Argumentos:
        event -- Evento disparado al seleccionar una categoría.

        - Esta función encapsula el comportamiento relacionado con la interacción del usuario y asegura que los campos sean 
          mostrados u ocultados de manera correcta según la categoría seleccionada.
        """
    def manejar_categoria_seleccionada(self,event):
        categoria_seleccionada = self.entrada_categoria.get()

        if categoria_seleccionada == "Otros":
            self.entrada_otro.grid()
        else:
            self.entrada_otro.grid.remove()

    def agregar_gasto(self):
        """
        Función para agregar un gasto al sistema.
        - Valida las entradas: descripción, monto y categoría.
        - Crea un objeto Gasto y lo agrega al sistema si los datos son válidos y el saldo es suficiente.
        - Actualiza el saldo y el historial de gastos.
        
        Abstracción: Detalles técnicos como la creación del objeto `Gasto` y la interacción con el gestor están ocultos 
          al usuario, facilitando el entendimiento del flujo principal.

        Manejo de errores:
        - Valida las entradas del usuario y utiliza `try-except` para capturar errores en el formato del monto.
        """
        
        descripcion = self.entrada_descripcion.get().strip()
        monto = self.entrada_monto.get().strip()
        categoria = self.entrada_categoria.get().strip()

    # Validar que el monto sea un número positivo
        
        try:
            
            monto = float(monto)
            if monto <= 0:
                messagebox.showerror("Error", "El monto debe ser mayor que cero.")
                return
        except ValueError:
            messagebox.showerror("Error", "Monto inválido. Debes ingresar un número válido.")
            return

        if not descripcion:
            messagebox.showerror("Error", "La descripción no puede estar vacía.")
            return

        if categoria == "":
            messagebox.showerror("Error", "La categoría no puede estar vacía.")
            return

    # Crear el gasto
        gasto = Gasto(descripcion, monto, categoria)

        if self.gestor.agregar_gasto(gasto):
            self.etiqueta_saldo.config(text=f"Saldo Actual: ${self.usuario.saldo:.2f}")
            messagebox.showinfo("Éxito", "Gasto agregado correctamente.")
            self.crear_historial()
        else:
            messagebox.showerror("Error", "Saldo insuficiente.")

        
     #Oscar
        """
        Función para agregar fondos al saldo disponible del usuario.
        - Valida las entradas: descripción y monto.
        - Actualiza el saldo en el sistema y registra el ingreso en la base de datos.
        - Actualiza la interfaz mostrando el nuevo saldo y el historial.

        Se encapsula la lógica de validación y actualización del saldo en esta función.
        """
    def agregar_fondos(self):
        descripcion_fondo = self.entrada_descripcion_fondo.get().strip()
        monto_fondo = self.entrada_monto_fondo.get().strip()

        try:
            monto_fondo = float(monto_fondo)
        except ValueError:
            messagebox.showerror("Error", "Monto invalido")
            return
        
        if not descripcion_fondo:
            messagebox.showerror("Error", "Descripción no puede estar vacía.")
            return
        if monto_fondo <= 0:
            messagebox.showerror("Error", "El monto debe ser mayor a cero")
            return
        
        self.gestor.agregar_fondos(monto_fondo)

        conn = sqlite3.connect('gastospersonales.db')
        cursor = conn.cursor()

        cursor.execute(''' 
        INSERT INTO historial_gastos (usuario_id, descripcion, cantidad, categoria)
        VALUES (?, ?, ?, ?)
        ''', (self.usuario.id_usuario, descripcion_fondo, monto_fondo, "Ingreso"))
        
        conn.commit()
        conn.close()

        self.etiqueta_saldo.config(text=f"Saldo Actual: ${self.usuario.saldo:.2f}")
        self.crear_historial()

        messagebox.showinfo("Éxito", f"Fondos agregados: ${monto_fondo:.2f} con la descripcion'{descripcion_fondo}'.")
    
     #Vladimir
        """
        Función para generar el historial de gastos en la interfaz.
        - Muestra un Treeview con los gastos del usuario extraídos de la base de datos.
        - Actualiza la tabla cada vez que se realiza una operación (como agregar o borrar un gasto).

         Oculta la lógica de recuperación de datos y configuración visual detrás de una función sencilla.
        """
    def crear_historial(self):
    # Si existe un frame previo, destruirlo para evitar errores
        if self.frame_historial is not None and self.frame_historial.winfo_exists():
            self.frame_historial.destroy()

    # Crear un nuevo frame para el historial
    # Ajustar el tamaño del frame para que esté alineado con los botones
        self.frame_historial = tk.Frame(self.root, bg="#ffffff", height=350)  # Ajusta la altura aquí según tus necesidades
        self.frame_historial.place(relx=0.5, rely=0.8, anchor="center", width=900, height=220)

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 12))  # Cambia 'Arial' y 12 por la fuente y tamaño que prefieras
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"))

    # Crear un nuevo Treeview en el frame con un número reducido de filas visibles
        self.tabla_historial = ttk.Treeview(self.frame_historial, columns=("Descripcion", "Monto", "Categoria", "Fecha"), show="headings", height=1)
        self.tabla_historial.pack(fill="both", expand=True)

    # Definir encabezados y ajustar columnas
        self.tabla_historial.heading("Descripcion", text="Descripción")
        self.tabla_historial.heading("Monto", text="Monto")
        self.tabla_historial.heading("Categoria", text="Categoría")
        self.tabla_historial.heading("Fecha", text="Fecha")

    # Ajustar el ancho de las columnas para ocupar menos espacio
        self.tabla_historial.column("Descripcion", width=150)
        self.tabla_historial.column("Monto", width=80)
        self.tabla_historial.column("Categoria", width=120)
        self.tabla_historial.column("Fecha", width=100)

    # Conectar a la base de datos y recuperar los datos para llenar la tabla
        conn = sqlite3.connect('gastospersonales.db')
        cursor = conn.cursor()
        cursor.execute("SELECT descripcion, cantidad, categoria, fecha FROM historial_gastos WHERE usuario_id = ? ORDER BY fecha ASC", (self.usuario.id_usuario,))
        gastos = cursor.fetchall()
        conn.close()

    # Insertar los datos en la tabla
        for gasto in gastos:
            descripcion, cantidad, categoria, fecha = gasto
            cantidad_formateada = f"${cantidad:.2f}"
            self.tabla_historial.insert("", "end", values=(descripcion, cantidad_formateada, categoria, fecha))

    def cerrar_sesion(self):
    # Limpia la ventana actual
        self.limpiar_ventana()
    
    # Elimina cualquier referencia a frames anteriores para evitar residuos
        self.frame_actual = None
        self.frame_gastos = None
    
    # Vuelve a crear la interfaz de login
        self.crear_login()


# Crear ventana principal
root = tk.Tk()
app = App(root)
root.mainloop()