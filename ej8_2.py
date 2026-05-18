import tkinter as tk
from tkinter import ttk, messagebox

## Lógica de programación ##

class Notas:

    def __init__(self):
        # El libro trabaja con un array de 5 elementos
        self.lista_notas = [0.0] * 5
        
    def asignar_notas(self, *notas):
        """Asigna y valida las notas ingresadas desde la interfaz."""
        try:
            for i in range(5):
                valor = float(notas[i].strip())
                # Validación opcional pero recomendada: rango de notas de 0 a 5
                if valor < 0.0 or valor > 5.0:
                    raise ValueError(f"La nota {i+1} debe estar entre 0.0 y 5.0.")
                self.lista_notas[i] = valor
        except ValueError as e:
            if "entre 0.0 y 5.0" in str(e):
                raise e
            raise ValueError("Todas las notas deben ser valores numéricos válidos.")

    def calcular_promedio(self):
        return sum(self.lista_notas) / len(self.lista_notas)
    
    def mayor_nota(self):
        return max(self.lista_notas)
    
    def menor_nota(self):
        return min(self.lista_notas)
    
    def calculo_varianza(self):
        media = self.calcular_promedio()
        suma_diferencias_cuadrado = 0
        
        for nota in self.lista_notas:
            suma_diferencias_cuadrado += (nota - media) ** 2
            
        # AJUSTE SEGUIN TEXTO GUÍA: División por (n - 1) para desviación muestral
        # Como son 5 notas, divide por 4.
        varianza = suma_diferencias_cuadrado / (len(self.lista_notas) - 1)
        return varianza

    def desviacion_estandar(self):
        varianza = self.calculo_varianza()
        return varianza ** 0.5


## Interfaz gráfica ##

class NotasApp:
    def __init__(self, master):
        self.master = master
        master.title("Estadística de Notas - Actividad 3")
        master.resizable(False, False)

        # Crear la instancia de la clase de lógica
        self.calculadora = Notas() 
        
        self.cajas_notas = []
        
        # Frame para las Entradas
        frame_entrada = ttk.LabelFrame(master, text=" Ingrese las Notas ", padding="15") 
        frame_entrada.pack(padx=15, pady=10, fill="x")

        for i in range(5):
            ttk.Label(frame_entrada, text=f"Nota {i+1}:").grid(row=i, column=0, padx=5, pady=5, sticky="w") 
            caja = ttk.Entry(frame_entrada, width=12)
            caja.grid(row=i, column=1, padx=5, pady=5) 
            caja.insert(0, "0.0") 
            self.cajas_notas.append(caja)

        # Botón de cálculo 
        ttk.Button(master, text="Calcular Resultados", command=self.calcular_notas).pack(pady=10) 

        # Frame para los Resultados
        frame_resultados = ttk.LabelFrame(master, text=" Resultados Estadísticos ", padding="15")
        frame_resultados.pack(padx=15, pady=10, fill="x")
        
        self.resultado_promedio = ttk.Label(frame_resultados, text="Promedio: -")
        self.resultado_promedio.pack(anchor='w', pady=3)
        self.resultado_mayor = ttk.Label(frame_resultados, text="Nota Mayor: -")
        self.resultado_mayor.pack(anchor='w', pady=3)
        self.resultado_menor = ttk.Label(frame_resultados, text="Nota Menor: -")
        self.resultado_menor.pack(anchor='w', pady=3)
        self.resultado_desviacion = ttk.Label(frame_resultados, text="Desviación Estándar: -")
        self.resultado_desviacion.pack(anchor='w', pady=3)

    def calcular_notas(self):
        try:
            # Obtener los valores de las cajas de texto
            notas_input = [caja.get() for caja in self.cajas_notas]

            # Enviar los valores desempaquetados a la lógica
            self.calculadora.asignar_notas(*notas_input) 
            
            # Realizar operaciones
            promedio = self.calculadora.calcular_promedio()
            mayor = self.calculadora.mayor_nota()
            menor = self.calculadora.menor_nota()
            desviacion = self.calculadora.desviacion_estandar()

            # Actualizar la interfaz con los formatos correctos
            self.resultado_promedio.config(text=f"Promedio: {promedio:.2f}")
            self.resultado_mayor.config(text=f"Nota Mayor: {mayor:.1f}")
            self.resultado_menor.config(text=f"Nota Menor: {menor:.1f}")
            self.resultado_desviacion.config(text=f"Desviación Estándar: {desviacion:.2f}")
            
        except ValueError as e:
            messagebox.showerror("Error de Entrada", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = NotasApp(root)
    root.mainloop()