from tkinter import Tk, Text, Button, END, re

# Clase principal para crear la interfaz de la calculadora
class Interfaz:
    def __init__(self, ventana):
        # Configuración inicial de la ventana principal
        self.ventana = ventana
        self.ventana.title("Calculadora")  # Título de la ventana
        self.ventana.resizable(0, 0)  # Evitar redimensionamiento
        self.ventana.configure(background="#84a59e")  # Color de fondo

        # Crear la pantalla donde se mostrarán las operaciones y resultados
        self.pantalla = Text(
            ventana, state="disabled", bd=10, insertwidth=5,
            width=33, height=2, background="#f5cac2",  # Configuración de estilo
            foreground="black", font=("Calibri", 15)
        )
        self.pantalla.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

        # Inicializar atributos de la calculadora
        self.operacion = ""  # Almacena la operación actual como cadena
        self.resultado_mostrado = False  # Controla si un resultado está siendo mostrado

        # Crear los botones de la calculadora
        self.crearBotones()

        # Vincular eventos de teclado para facilitar el uso
        self.ventana.bind("<Key>", self.teclaPresionada)

    # Método para crear un botón con valores y configuraciones específicas
    def crearBoton(self, valor, escribir=True, ancho=6, alto=1, bg="#f7ede3", fg="black"):
        return Button(
            self.ventana, text=valor, width=ancho, height=alto, 
            background=bg, foreground=fg, font=("Helvetica", 15), 
            command=lambda: self.click(valor, escribir)  # Asignar evento click
        )

    # Método para crear y posicionar todos los botones en la interfaz
    def crearBotones(self):
        # Lista de botones con su configuración respectiva
        botones = [
            self.crearBoton(7), self.crearBoton(8), self.crearBoton(9), self.crearBoton("C", escribir=False),
            self.crearBoton(4), self.crearBoton(5), self.crearBoton(6), self.crearBoton(u"\u00F7"),
            self.crearBoton(1), self.crearBoton(2), self.crearBoton(3), self.crearBoton("*"),
            self.crearBoton("."), self.crearBoton(0), self.crearBoton("+"), self.crearBoton("-"),
            # Botón de igual con un color diferente
            self.crearBoton("=", escribir=False, ancho=20, alto=1, bg="#4CAF50", fg="white")
        ]

        # Ubicar botones en un diseño de cuadrícula (grid)
        contador = 0
        for fila in range(1, 5):
            for columna in range(4):
                botones[contador].grid(row=fila, column=columna)  # Colocar el botón en su posición
                contador += 1

        # Botón "=" ocupa toda la última fila
        botones[16].grid(row=5, column=0, columnspan=4, padx=5, pady=5)

    # Método que controla la lógica al hacer clic en un botón
    def click(self, texto, escribir):
        if not escribir:  # Si el botón no es de escritura (por ejemplo, "=" o "C")
            if texto == "=" and self.operacion:  # Si se presiona "=" y hay una operación en curso
                try:
                    # Reemplazar el símbolo de división Unicode por el operador de Python "/"
                    self.operacion = re.sub(u"\u00F7", "/", self.operacion)
                    if "/0" in self.operacion:  # Verificar división entre 0
                        raise ZeroDivisionError
                    resultado = str(eval(self.operacion))  # Evaluar la operación
                except ZeroDivisionError:
                    resultado = "Error: Div/0"  # Mensaje de error por división entre 0
                    self.operacion = ""  # Reiniciar la operación en caso de error
                except Exception:
                    resultado = "Error"  # Mensaje genérico de error
                    self.operacion = ""
                else:
                    self.operacion = resultado  # Usar el resultado como base para nuevas operaciones
                finally:
                    self.resultado_mostrado = True  # Indicar que un resultado fue mostrado
                    self.limpiarPantalla()  # Limpiar la pantalla
                    self.mostrarEnPantalla(resultado)  # Mostrar el resultado
            elif texto == "C":  # Si se presiona "C", limpiar todo
                self.operacion = ""  # Reiniciar operación
                self.limpiarPantalla()
        else:  # Si es un botón de escritura (número u operador)
            if self.resultado_mostrado:  # Si un resultado está en pantalla
                self.operacion = ""  # Reiniciar la operación
                self.limpiarPantalla()
                self.resultado_mostrado = False  # Resetear el estado de resultado mostrado
            self.operacion += str(texto)  # Añadir el texto del botón a la operación
            self.mostrarEnPantalla(texto)  # Mostrar el texto en la pantalla

    # Método para limpiar la pantalla
    def limpiarPantalla(self):
        self.pantalla.configure(state="normal")  # Hacer editable la pantalla temporalmente
        self.pantalla.delete("1.0", END)  # Borrar todo el contenido
        self.pantalla.configure(state="disabled")  # Volver a desactivar la edición

    # Método para mostrar texto en la pantalla
    def mostrarEnPantalla(self, valor):
        self.pantalla.configure(state="normal")  # Hacer editable la pantalla temporalmente
        self.pantalla.insert(END, valor)  # Insertar el valor en la pantalla
        self.pantalla.configure(state="disabled")  # Volver a desactivar la edición

    # Método que controla las teclas presionadas en el teclado
    def teclaPresionada(self, evento):
        tecla = evento.char  # Obtener la tecla presionada
        if tecla in "0123456789.+-*/":  # Si es un carácter válido
            self.click(tecla, escribir=True)
        elif tecla == "\r":  # Enter para calcular el resultado
            self.click("=", escribir=False)
        elif tecla == "\x08":  # Backspace para borrar el último carácter
            self.operacion = self.operacion[:-1]  # Eliminar el último carácter de la operación
            self.limpiarPantalla()
            self.mostrarEnPantalla(self.operacion)  # Actualizar la pantalla

# Crear la ventana principal de la aplicación
ventana_principal = Tk()
calculadora = Interfaz(ventana_principal)  # Instanciar la interfaz de la calculadora
ventana_principal.mainloop()  # Iniciar el bucle principal de la aplicación
