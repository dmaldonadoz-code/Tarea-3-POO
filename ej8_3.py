import tkinter as tk
from tkinter import ttk, messagebox
import math

## LOGICA DE PROGRAMACION ##

class FiguraSolida: # Clase Padre (Base para las demás) 
    
    def __init__(self, nombre):
        self.nombre_figura = nombre

    def datos_figura(self): 
        return f"Figura seleccionada: {self.nombre_figura}"
    
    def calcular_volumen(self):
        raise NotImplementedError("Las clases hijas deben implementar 'calcular_volumen'")
    
    def calcular_superficie(self):
        raise NotImplementedError("Las clases hijas deben implementar 'calcular_superficie'")


class Cilindro(FiguraSolida): 
    
    def __init__(self, radio, altura):
        super().__init__("Cilindro")
        # Validación: Convertir y asegurar que sean positivos de acuerdo al libro
        r = float(radio)
        h = float(altura)
        if r <= 0 or h <= 0:
            raise ValueError("El radio y la altura deben ser mayores que cero.")
        
        self.radio = r
        self.altura = h
        
    def calcular_volumen(self): 
        return math.pi * (self.radio ** 2) * self.altura
        
    def calcular_superficie(self): 
        area_lateral = 2 * math.pi * self.radio * self.altura
        area_bases = 2 * math.pi * (self.radio ** 2)
        return area_lateral + area_bases
    
    def datos_figura(self): 
        base_info = super().datos_figura()
        return (
            f"{base_info}\n"
            f"Radio (r): {self.radio:.2f} cm\n"
            f"Altura (h): {self.altura:.2f} cm"
        )


class Esfera(FiguraSolida): 
    
    def __init__(self, radio):
        super().__init__("Esfera")
        r = float(radio)
        if r <= 0:
            raise ValueError("El radio debe ser mayor que cero.")
        self.radio = r
        
    def calcular_volumen(self): 
        return (4/3) * math.pi * (self.radio ** 3)

    def calcular_superficie(self): 
        return 4 * math.pi * (self.radio ** 2)

    def datos_figura(self): 
        base_info = super().datos_figura()
        return f"{base_info}\nRadio (r): {self.radio:.2f} cm"


class Piramide(FiguraSolida): 
    
    def __init__(self, base, altura, apotema):
        super().__init__("Pirámide (Base Cuadrada)")
        b = float(base)
        h = float(altura)
        ap = float(apotema)
        if b <= 0 or h <= 0 or ap <= 0:
            raise ValueError("El lado de la base, la altura y la apotema deben ser mayores que cero.")
        
        self.lado_base = b
        self.altura = h
        self.apotema = ap 
        
    def calcular_area_base(self): 
        return self.lado_base ** 2
    
    def calcular_perimetro_base(self): 
        return 4 * self.lado_base

    def calcular_volumen(self): 
        return (1/3) * self.calcular_area_base() * self.altura

    def calcular_superficie(self): 
        area_base = self.calcular_area_base()
        perimetro_base = self.calcular_perimetro_base()
        area_lateral = (perimetro_base * self.apotema) / 2
        return area_base + area_lateral

    def datos_figura(self): 
        base_info = super().datos_figura()
        return (
            f"{base_info}\n"
            f"Lado Base: {self.lado_base:.2f} cm\n"
            f"Altura (h): {self.altura:.2f} cm\n"
            f"Apotema: {self.apotema:.2f} cm"
        )


## INTERFAZ GRAFICA ##

class SolidosApp:
    def __init__(self, master):
        self.master = master
        master.title("Calculadora de Sólidos Geométricos")
        master.resizable(False, False)
        
        self.figura_seleccionada = tk.StringVar(value="Cilindro")
        self.cajas_entrada = {}
        self.labels_parametros = {}
        
        # Frame Principal
        frame_main = ttk.Frame(master, padding="15")
        frame_main.pack(padx=10, pady=10)

        # Selección de Figura
        ttk.Label(frame_main, text="1. Seleccione la Figura Sólida:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        opciones = ["Cilindro", "Esfera", "Pirámide"]
        self.menu_figuras = ttk.Combobox(frame_main, textvariable=self.figura_seleccionada, values=opciones, state="readonly", width=18)
        self.menu_figuras.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.menu_figuras.bind("<<ComboboxSelected>>", self.actualizar_parametros)

        # Parámetros de Entrada
        frame_params = ttk.LabelFrame(frame_main, text="2. Ingrese Parámetros", padding="10")
        frame_params.grid(row=1, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

        campos = [("param1", "Radio/Lado Base:"), ("param2", "Altura:"), ("param3", "Apotema:")]
        valores_defecto = ["5.0", "10.0", "12.0"]

        for i, (key, label_text) in enumerate(campos):
            label = ttk.Label(frame_params, text=label_text)
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
            self.labels_parametros[key] = label
            
            caja = ttk.Entry(frame_params, width=15)
            caja.grid(row=i, column=1, padx=5, pady=5)
            caja.insert(0, valores_defecto[i])
            self.cajas_entrada[key] = caja
        
        self.actualizar_parametros() 

        # Botón de Cálculo 
        ttk.Button(frame_main, text="Calcular Volumen y Superficie", command=self.calcular_solido).grid(row=4, column=0, columnspan=2, pady=10)

        # Área de Resultados
        frame_resultados = ttk.LabelFrame(frame_main, text="3. Resultados", padding="10")
        frame_resultados.grid(row=5, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

        self.resultado_figura = ttk.Label(frame_resultados, text="Figura: -")
        self.resultado_figura.pack(anchor='w', pady=2)
        self.resultado_volumen = ttk.Label(frame_resultados, text="Volumen (V): -")
        self.resultado_volumen.pack(anchor='w', pady=2)
        self.resultado_superficie = ttk.Label(frame_resultados, text="Superficie Total (A): -")
        self.resultado_superficie.pack(anchor='w', pady=2)
        self.resultado_detalles = ttk.Label(frame_resultados, text="Detalles: -")
        self.resultado_detalles.pack(anchor='w', pady=2)

    def actualizar_parametros(self, event=None):
        figura = self.figura_seleccionada.get()
        
        # Ocultar todos los campos antes de mostrar los específicos
        for label in self.labels_parametros.values():
            label.grid_remove()
        for caja in self.cajas_entrada.values():
            caja.grid_remove()

        if figura == "Cilindro":
            self.labels_parametros["param1"].config(text="Radio (r):")
            self.labels_parametros["param1"].grid(row=0, column=0, sticky="w"); self.cajas_entrada["param1"].grid(row=0, column=1)
            self.labels_parametros["param2"].config(text="Altura (h):")
            self.labels_parametros["param2"].grid(row=1, column=0, sticky="w"); self.cajas_entrada["param2"].grid(row=1, column=1)
        
        elif figura == "Esfera":
            self.labels_parametros["param1"].config(text="Radio (r):")
            self.labels_parametros["param1"].grid(row=0, column=0, sticky="w"); self.cajas_entrada["param1"].grid(row=0, column=1)
        
        elif figura == "Pirámide":
            self.labels_parametros["param1"].config(text="Lado Base:")
            self.labels_parametros["param1"].grid(row=0, column=0, sticky="w"); self.cajas_entrada["param1"].grid(row=0, column=1)
            self.labels_parametros["param2"].config(text="Altura (h):")
            self.labels_parametros["param2"].grid(row=1, column=0, sticky="w"); self.cajas_entrada["param2"].grid(row=1, column=1)
            self.labels_parametros["param3"].config(text="Apotema (a):")
            self.labels_parametros["param3"].grid(row=2, column=0, sticky="w"); self.cajas_entrada["param3"].grid(row=2, column=1)

    def calcular_solido(self):
        figura_tipo = self.figura_seleccionada.get()
        
        try:
            # Obtener y normalizar las entradas de texto
            val1_str = self.cajas_entrada["param1"].get().replace(',', '.').strip()
            val2_str = self.cajas_entrada["param2"].get().replace(',', '.').strip()
            val3_str = self.cajas_entrada["param3"].get().replace(',', '.').strip()
            
            nueva_figura = None

            if figura_tipo == "Cilindro":
                if not val1_str or not val2_str:
                    raise ValueError("Debe ingresar Radio y Altura.")
                nueva_figura = Cilindro(val1_str, val2_str)
            
            elif figura_tipo == "Esfera":
                if not val1_str:
                    raise ValueError("Debe ingresar el Radio.")
                nueva_figura = Esfera(val1_str)
            
            elif figura_tipo == "Pirámide":
                if not val1_str or not val2_str or not val3_str:
                    raise ValueError("Debe ingresar Lado Base, Altura y Apotema.")
                nueva_figura = Piramide(val1_str, val2_str, val3_str)

            if nueva_figura:
                # Ejecutar métodos polimórficos
                volumen = nueva_figura.calcular_volumen()
                superficie = nueva_figura.calcular_superficie()
                
                # Actualizar elementos visuales
                self.resultado_figura.config(text=f"Figura: {nueva_figura.nombre_figura}")
                self.resultado_volumen.config(text=f"Volumen (V): {volumen:.2f} cm³")
                self.resultado_superficie.config(text=f"Superficie Total (A): {superficie:.2f} cm²")
                
                detalles = nueva_figura.datos_figura().split('\n')[1:] 
                self.resultado_detalles.config(text="Detalles: " + " | ".join(detalles))
                
        except ValueError as e:
            # Captura tanto errores de conversión de texto como los números <= 0
            messagebox.showerror("Error de Entrada", f"Dato inválido: {e}")
        except Exception as e:
            messagebox.showerror("Error del Sistema", f"Ocurrió un error inesperado: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SolidosApp(root)
    root.mainloop()