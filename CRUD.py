from tkinter import *  # Biblioteca para crear interfaces gráficas
from tkinter import messagebox  # Biblioteca para mostrar mensajes emergentes
from tkinter import ttk  # Biblioteca para los widgets mejorados de tkinter
from tkinter import filedialog  # Biblioteca para seleccionar archivos
import sqlite3  # Biblioteca para trabajar con bases de datos SQLite
from PIL import Image, ImageTk  # Biblioteca para manejar imágenes

# Desarrollo de la Interfaz Gráfica
root = Tk()
root.title("Aplicación CRUD con Base de Datos")
root.geometry("900x700")

# Variables para almacenar los datos de entrada
miId = StringVar()
miNombre = StringVar()
miCargo = StringVar()
miSalario = StringVar()
miImagen = StringVar()

# Función para conectar y crear la base de datos
def conexionBBDD():
    miConexion = sqlite3.connect("base")
    miCursor = miConexion.cursor()
    try:
        # Crear la tabla empleado si no existe
        miCursor.execute('''
            CREATE TABLE empleado (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NOMBRE VARCHAR(50) NOT NULL,
            CARGO VARCHAR(50) NOT NULL,
            SALARIO INT NOT NULL,
            IMAGEN TEXT)
        ''')
        messagebox.showinfo("CONEXION", "Base de Datos Creada exitosamente")
    except sqlite3.OperationalError:
        # La tabla ya existe, agregar la columna IMAGEN si no existe
        try:
            miCursor.execute("ALTER TABLE empleado ADD COLUMN IMAGEN TEXT")
        except sqlite3.OperationalError:
            pass  # La columna ya existe
        messagebox.showinfo("CONEXION", "Conexión exitosa con la base de datos")

# Función para eliminar la base de datos
def eliminarBBDD():
    miConexion = sqlite3.connect("base")
    miCursor = miConexion.cursor()
    if messagebox.askyesno(message="¿Los Datos se perderán definitivamente, Desea continuar?", title="ADVERTENCIA"):
        # Eliminar la tabla empleado
        miCursor.execute("DROP TABLE empleado")
    else:
        pass
    limpiarCampos()
    mostrar()

# Función para salir de la aplicación
def salirAplicacion():
    valor = messagebox.askquestion("Salir", "¿Está seguro que desea salir de la Aplicación?")
    if valor == "yes":
        root.destroy()

# Función para limpiar los campos de entrada
def limpiarCampos():
    miId.set("")
    miNombre.set("")
    miCargo.set("")
    miSalario.set("")
    miImagen.set("")
    panel.config(image='')

# Función para mostrar un mensaje de información
def mensaje():
    acerca = '''
    Aplicación CRUD
    Versión 1.0
    Tecnología Python Tkinter
    '''
    messagebox.showinfo(title="INFORMACION", message=acerca)

################################ Métodos CRUD ##############################

# Función para crear un nuevo registro en la base de datos
def crear():
    miConexion = sqlite3.connect("base")
    miCursor = miConexion.cursor()
    try:
        datos = miNombre.get(), miCargo.get(), miSalario.get(), miImagen.get()
        # Insertar un nuevo registro en la tabla empleado
        miCursor.execute("INSERT INTO empleado (NOMBRE, CARGO, SALARIO, IMAGEN) VALUES (?, ?, ?, ?)", datos)
        miConexion.commit()
    except Exception as e:
        messagebox.showwarning("ADVERTENCIA", f"Ocurrió un error al crear el registro: {str(e)}")
        pass
    limpiarCampos()
    mostrar()

# Función para mostrar los registros de la base de datos
def mostrar():
    miConexion = sqlite3.connect("base")
    miCursor = miConexion.cursor()
    registros = tree.get_children()
    for elemento in registros:
        tree.delete(elemento)
    try:
        # Seleccionar todos los registros de la tabla empleado
        miCursor.execute("SELECT * FROM empleado")
        for row in miCursor:
            tree.insert("", 0, text=row[0], values=(row[1], row[2], row[3], row[4]))
    except:
        pass

# Configuración de la tabla para mostrar los registros
tree = ttk.Treeview(height=10, columns=('#0', '#1', '#2', '#3', '#4'))
tree.place(x=0, y=300, width=900)
tree.column('#0', width=100)
tree.heading('#0', text="ID", anchor=CENTER)
tree.heading('#1', text="Nombre del Empleado", anchor=CENTER)
tree.heading('#2', text="Cargo", anchor=CENTER)
tree.heading('#3', text="Salario", anchor=CENTER)
tree.heading('#4', text="Imagen", anchor=CENTER)

# Función para seleccionar un registro usando un doble clic
def seleccionarUsandoClick(event):
    item = tree.identify('item', event.x, event.y)
    miId.set(tree.item(item, "text"))
    miNombre.set(tree.item(item, "values")[0])
    miCargo.set(tree.item(item, "values")[1])
    miSalario.set(tree.item(item, "values")[2])
    miImagen.set(tree.item(item, "values")[3])
    mostrarImagen(miImagen.get())

tree.bind("<Double-1>", seleccionarUsandoClick)

# Función para actualizar un registro en la base de datos
def actualizar():
    miConexion = sqlite3.connect("base")
    miCursor = miConexion.cursor()
    try:
        datos = miNombre.get(), miCargo.get(), miSalario.get(), miImagen.get()
        # Actualizar un registro existente en la tabla empleado
        miCursor.execute("UPDATE empleado SET NOMBRE=?, CARGO=?, SALARIO=?, IMAGEN=? WHERE ID=" + miId.get(), datos)
        miConexion.commit()
    except Exception as e:
        messagebox.showwarning("ADVERTENCIA", f"Ocurrió un error al actualizar el registro: {str(e)}")
        pass
    limpiarCampos()
    mostrar()

# Función para borrar un registro de la base de datos
def borrar():
    miConexion = sqlite3.connect("base")
    miCursor = miConexion.cursor()
    try:
        if messagebox.askyesno(message="¿Realmente desea eliminar el registro?", title="ADVERTENCIA"):
            # Eliminar un registro de la tabla empleado
            miCursor.execute("DELETE FROM empleado WHERE ID=" + miId.get())
            miConexion.commit()
    except Exception as e:
        messagebox.showwarning("ADVERTENCIA", f"Ocurrió un error al tratar de eliminar el registro: {str(e)}")
        pass
    limpiarCampos()
    mostrar()

# Función para cargar una imagen
def cargarImagen():
    filename = filedialog.askopenfilename(title="Seleccionar Imagen", filetypes=[("Image files", "*.jpg *.png *.bmp *.gif")])
    miImagen.set(filename)
    mostrarImagen(filename)

# Función para mostrar una imagen
def mostrarImagen(filepath):
    try:
        img = Image.open(filepath)
        img = img.resize((100, 100), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        panel.config(image=img)
        panel.image = img
    except Exception as e:
        panel.config(image='')
        messagebox.showwarning("ADVERTENCIA", f"Ocurrió un error al mostrar la imagen: {str(e)}")

# Creación de los menús
menubar = Menu(root)
menubasedat = Menu(menubar, tearoff=0)
menubasedat.add_command(label="Crear/Conectar Base de Datos", command=conexionBBDD)
menubasedat.add_command(label="Eliminar Base de Datos", command=eliminarBBDD)
menubasedat.add_command(label="Salir", command=salirAplicacion)
menubar.add_cascade(label="Inicio", menu=menubasedat)

ayudamenu = Menu(menubar, tearoff=0)
ayudamenu.add_command(label="Resetear Campos", command=limpiarCampos)
ayudamenu.add_command(label="Acerca", command=mensaje)
menubar.add_cascade(label="Ayuda", menu=ayudamenu)

# Creación de etiquetas y cajas de texto
frame_campos = Frame(root)
frame_campos.pack(pady=10)

Label(frame_campos, text="Nombre").grid(row=0, column=0, padx=10, pady=5)
Entry(frame_campos, textvariable=miNombre, width=40).grid(row=0, column=1, padx=10, pady=5)

Label(frame_campos, text="Cargo").grid(row=1, column=0, padx=10, pady=5)
Entry(frame_campos, textvariable=miCargo, width=40).grid(row=1, column=1, padx=10, pady=5)

Label(frame_campos, text="Salario").grid(row=2, column=0, padx=10, pady=5)
Entry(frame_campos, textvariable=miSalario, width=40).grid(row=2, column=1, padx=10, pady=5)

Button(frame_campos, text="Cargar Imagen", command=cargarImagen).grid(row=3, column=0, padx=10, pady=5)
panel = Label(frame_campos)
panel.grid(row=3, column=1, padx=10, pady=5)

# Creación de botones
frame_botones = Frame(root)
frame_botones.pack(pady=10)

Button(frame_botones, text="Crear Registro", command=crear).grid(row=0, column=0, padx=10, pady=5)
Button(frame_botones, text="Modificar Registro", command=actualizar).grid(row=0, column=1, padx=10, pady=5)
Button(frame_botones, text="Mostrar Lista", command=mostrar).grid(row=0, column=2, padx=10, pady=5)
Button(frame_botones, text="Eliminar Registro", bg="red", command=borrar).grid(row=0, column=3, padx=10, pady=5)

# Configuración del menú
root.config(menu=menubar)

# Bucle principal de la aplicación
root.mainloop()
