import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import math

ctk.set_appearance_mode("dark")
AZUL_FONDO = "#0D1B2A"
AZUL_PANEL = "#1B263B"
AZUL_DETALLE = "#3B8ED0"
CIAN_RESALTADO = "#00FFFF"

class Calculadora(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SISTEMA DE PLANIFICACIÓN ESTADÍSTICA V3.5")
        self.geometry("1200x880")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- PANEL LATERAL ---
        self.sidebar = ctk.CTkFrame(self, width=320, corner_radius=0, fg_color=AZUL_PANEL)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="CONFIGURACIÓN", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)

        # 1. Tipo de estimación
        self.tipo_var = ctk.IntVar(value=1) 
        ctk.CTkRadioButton(self.sidebar, text="ESTIMACIÓN DE MEDIA", variable=self.tipo_var, value=1, command=self.actualizar_labels).pack(pady=5, padx=20, anchor="w")
        ctk.CTkRadioButton(self.sidebar, text="ESTIMACIÓN DE PROPORCIÓN", variable=self.tipo_var, value=2, command=self.actualizar_labels).pack(pady=5, padx=20, anchor="w")

        # 2. Nivel de Confianza
        ctk.CTkLabel(self.sidebar, text="NIVEL DE CONFIANZA (%):").pack(pady=(15, 0))
        self.opt_conf = ctk.CTkOptionMenu(self.sidebar, values=["90", "95", "99"], fg_color=AZUL_DETALLE)
        self.opt_conf.pack(pady=5, padx=20, fill="x")
        self.opt_conf.set("99")

        # 3. Margen de Error
        self.lbl_error = ctk.CTkLabel(self.sidebar, text="MARGEN DE ERROR (Unidades):")
        self.lbl_error.pack(pady=(15, 0))
        self.ent_error = ctk.CTkEntry(self.sidebar, placeholder_text="Ej: 1.0", border_color=AZUL_DETALLE)
        self.ent_error.pack(pady=5, padx=20, fill="x")
        self.lbl_ayuda_error = ctk.CTkLabel(self.sidebar, text="* En Media use unidades (kg, $, m).", 
                                           font=ctk.CTkFont(size=11, slant="italic"), text_color="#AAAAAA")
        self.lbl_ayuda_error.pack(pady=(0, 10))

        # 4. Variable (p o Sigma)
        self.lbl_variable = ctk.CTkLabel(self.sidebar, text="DESVIACIÓN ESTÁNDAR (σ):")
        self.lbl_variable.pack(pady=(10, 0))
        self.ent_variable = ctk.CTkEntry(self.sidebar, placeholder_text="Ej: 10", border_color=AZUL_DETALLE)
        self.ent_variable.pack(pady=5, padx=20, fill="x")

        # 5. POBLACIÓN
        ctk.CTkLabel(self.sidebar, text="TIPO DE POBLACIÓN:").pack(pady=(15, 0))
        self.opt_pob = ctk.CTkOptionMenu(self.sidebar, values=["INFINITA", "FINITA"], command=self.gestionar_campo_poblacion, fg_color=AZUL_DETALLE)
        self.opt_pob.pack(pady=5, padx=20, fill="x")
        
        self.container_n = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.container_n.pack(pady=0, padx=0, fill="x")
        self.lbl_n_pob = ctk.CTkLabel(self.container_n, text="TAMAÑO POBLACIÓN (N):")
        self.ent_pob = ctk.CTkEntry(self.container_n, placeholder_text="Máx: 8,000,000,000", border_color=AZUL_DETALLE)
        self.lbl_nota_pob = ctk.CTkLabel(self.container_n, text="* Límite basado en la población mundial.", 
                                        font=ctk.CTkFont(size=10, slant="italic"), text_color="#AAAAAA")

        ctk.CTkButton(self.sidebar, text="EJECUTAR ANÁLISIS", font=ctk.CTkFont(weight="bold"), 
                      fg_color="#28A745", hover_color="#218838", command=self.ejecutar).pack(side="bottom", pady=40, padx=20, fill="x")

        # --- PANEL CENTRAL ---
        self.main_panel = ctk.CTkFrame(self, fg_color=AZUL_FONDO)
        self.main_panel.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.txt_res = ctk.CTkTextbox(self.main_panel, height=220, font=ctk.CTkFont(family="Consolas", size=14), border_color=AZUL_DETALLE, border_width=1)
        self.txt_res.pack(pady=20, padx=20, fill="x")
        self.txt_res._textbox.tag_config("HIGHLIGHT", foreground=CIAN_RESALTADO, font=ctk.CTkFont(size=16, weight="bold"))

        self.graph_container = ctk.CTkFrame(self.main_panel, fg_color="transparent")
        self.graph_container.pack(fill="both", expand=True, padx=20, pady=10)

    def gestionar_campo_poblacion(self, seleccion):
        if seleccion == "FINITA":
            self.lbl_n_pob.pack(pady=(5, 0))
            self.ent_pob.pack(pady=5, padx=20, fill="x")
            self.lbl_nota_pob.pack(pady=(0, 5))
        else:
            self.lbl_n_pob.pack_forget()
            self.ent_pob.pack_forget()
            self.lbl_nota_pob.pack_forget()

    def actualizar_labels(self):
        if self.tipo_var.get() == 1:
            self.lbl_error.configure(text="MARGEN DE ERROR (Unidades):")
            self.lbl_ayuda_error.configure(text="* Use el valor real de error (ej: 1.0 kg).")
            self.lbl_variable.configure(text="DESVIACIÓN ESTÁNDAR (σ):")
            self.ent_variable.configure(placeholder_text="Ej: 10")
            self.ent_error.configure(placeholder_text="Ej: 1.0")
        else:
            self.lbl_error.configure(text="MARGEN DE ERROR (%):")
            self.lbl_ayuda_error.configure(text="* Use porcentaje del 1 al 20 (ej: 5).")
            self.lbl_variable.configure(text="PROPORCIÓN p (1 - 99%):")
            self.ent_variable.configure(placeholder_text="Ej: 50")
            self.ent_error.configure(placeholder_text="Ej: 5")

    def ejecutar(self):
        try:
            # 1. Validar campos vacíos y formato numérico
            try:
                val_err = float(self.ent_error.get())
                val_var = float(self.ent_variable.get())
            except ValueError:
                raise ValueError("Solo se aceptan números en los campos de Error y Desviación/Proporción.")

            z_map = {"90": 1.645, "95": 1.96, "99": 2.576}
            Z = z_map[self.opt_conf.get()]

            if self.tipo_var.get() == 1:
                E = val_err
                n_inf = (Z * val_var / E)**2
                detalles = f"n = ({Z} * {val_var} / {E})²"
                unidad_grafica = "Unidades"
            else:
                E = val_err / 100
                p = val_var / 100
                n_inf = (Z**2 * p * (1-p)) / (E**2)
                detalles = f"n = ({Z}² * {p} * {1-p}) / {E}²"
                unidad_grafica = "%"

            # 2. Validar Población Finita y Límite
            tipo_pob = self.opt_pob.get()
            N = None
            if tipo_pob == "FINITA":
                try:
                    # Limpiar puntos o comas que el usuario pudiera poner por costumbre
                    raw_n = self.ent_pob.get().replace(".", "").replace(",", "")
                    N = int(raw_n)
                except ValueError:
                    raise ValueError("El tamaño de población (N) debe ser un número entero sin letras.")
                
                if N > 8000000000:
                    raise ValueError("El tamaño de población no puede exceder los 8,000,000,000 (Población Mundial).")
                if N <= 1:
                    raise ValueError("La población debe ser mayor a 1.")
                
                n_final = math.ceil(n_inf / (1 + (n_inf / N)))
            else:
                n_final = math.ceil(n_inf)

            # Reporte Visual
            self.txt_res.delete("1.0", tk.END)
            resumen = (f" REPORTE TÉCNICO DE MUESTREO\n"
                       f" {'='*45}\n"
                       f" • NIVEL DE CONFIANZA: {self.opt_conf.get()}% (Z={Z})\n"
                       f" • ERROR DEFINIDO: {val_err} ({'Unidades' if self.tipo_var.get()==1 else '%'})\n"
                       f" • POBLACIÓN: {tipo_pob} {'(N='+f'{N:,}'+')' if N else ''}\n"
                       f" • FÓRMULA BASE: {detalles}\n"
                       f" {'-'*45}\n")
            self.txt_res.insert(tk.END, resumen)
            self.txt_res.insert(tk.END, f" MUESTRA RECOMENDADA: {n_final} SUJETOS", "HIGHLIGHT")

            self.dibujar_grafica(Z, val_var, self.tipo_var.get(), N, val_err, n_final, unidad_grafica)

        except ValueError as e:
            messagebox.showwarning("Dato Inválido", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    def dibujar_grafica(self, Z, val, tipo, N, e_act, n_act, unidad_label):
        for w in self.graph_container.winfo_children(): w.destroy()
        
        if tipo == 1:
            e_min = e_act * 0.2 if e_act > 0 else 0.1
            e_rango = np.linspace(e_min, e_act * 4, 100)
        else:
            e_rango = np.linspace(0.01, 0.25, 100)

        muestras = []
        for e in e_rango:
            if tipo == 1: ni = (Z*val/e)**2
            else: ni = (Z**2 * (val/100) * (1-(val/100))) / (e**2)
            if N: ni = ni / (1 + (ni / N))
            muestras.append(ni)

        fig, ax = plt.subplots(figsize=(6, 4), facecolor=AZUL_FONDO)
        x_vals = e_rango if tipo == 1 else e_rango * 100
        ax.plot(x_vals, muestras, color=AZUL_DETALLE, linewidth=2, label="Curva de Muestra")
        ax.scatter([e_act], [n_act], color="red", s=80, zorder=5, label="Tu Cálculo")
        
        ax.set_facecolor(AZUL_FONDO)
        ax.tick_params(colors='white', labelsize=9)
        ax.set_xlabel(f"ERROR ({unidad_label})", color='white')
        ax.set_ylabel("TAMAÑO MUESTRA (n)", color='white')
        ax.grid(True, alpha=0.1, color='white')
        ax.legend()
        
        canvas = FigureCanvasTkAgg(fig, master=self.graph_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

if __name__ == "__main__":
    app = Calculadora()
    app.mainloop()