import sqlite3

#conectar a la base de datos
conn = sqlite3.connect('gastospersonales.db')
cursor = conn.cursor()

# Crear la tabla de usuarios
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

# Crear la tabla de gastos
cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        amount REAL NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')



# Confirmar cambios y cerrar conexión
conn.commit()
conn.close()

print("Base de datos 'gastospersonales.db' configurada correctamente.")
