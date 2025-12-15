import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------
# Funciones auxiliares
# -------------------------
def cargar_archivo():
    global df
    ruta = filedialog.askopenfilename(filetypes=[("CSV", "*.csv"), ("Excel", "*.xlsx")])
    if not ruta:
        return
    try:
        df = pd.read_csv(ruta) if ruta.endswith(".csv") else pd.read_excel(ruta)
        actualizar_tabla(df)
        messagebox.showinfo("OK", "Archivo cargado correctamente")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def guardar_archivo():
    if df.empty:
        messagebox.showerror("Error", "No hay datos para guardar")
        return
    ruta = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
    if ruta:
        df.to_csv(ruta, index=False)
        messagebox.showinfo("OK", "Archivo guardado correctamente")

def generar_dataset():
    global df
    n = 1000  # 1000 partidos
    rng = np.random.default_rng()

    df = pd.DataFrame({
        "Equipo": [f"Equipo {i+1}" for i in range(n)],
        "Prom_centro": rng.uniform(20, 70, n).round(1),
        "Prom_izq": rng.uniform(10, 40, n).round(1),
        "Prom_der": rng.uniform(10, 40, n).round(1),
        "Prom_largos": rng.uniform(5, 30, n).round(1),
        "Prob_centro": rng.uniform(0.4, 0.75, n).round(2),
        "Prob_izq": rng.uniform(0.25, 0.55, n).round(2),
        "Prob_der": rng.uniform(0.25, 0.55, n).round(2),
        "Prob_largos": rng.uniform(0.15, 0.35, n).round(2),
    })

    actualizar_tabla(df)
    messagebox.showinfo("OK", "Dataset aleatorio generado")

# -------------------------
# Procesamiento
# -------------------------
def preparar_datos(df):
    columnas_prom = ["Prom_centro", "Prom_izq", "Prom_der", "Prom_largos"]
    for col in columnas_prom:
        if col in df.columns:
            # Generar tiros aleatorios basados en promedio, con ligera variación
            df[col.replace("Prom_", "Tiros_")] = np.random.poisson(df[col] * np.random.uniform(0.8, 1.2))
    return df

def ejecutar_simulacion():
    if df.empty:
        messagebox.showerror("Error", "No hay dataset cargado o generado")
        return

    df_proc = preparar_datos(df.copy())
    resultados = []

    for _, row in df_proc.iterrows():
        tiros = [
            row["Tiros_centro"],
            row["Tiros_izq"],
            row["Tiros_der"],
            row["Tiros_largos"]
        ]
        probs = [row["Prob_centro"], row["Prob_izq"], row["Prob_der"], row["Prob_largos"]]
        aciertos = [np.random.binomial(tiros[i], probs[i]) for i in range(4)]
        resultados.append(aciertos)

    resultados = np.array(resultados)

    # Guardar aciertos en el dataframe para mostrar en tabla
    df_proc["Aciertos_centro"] = resultados[:, 0]
    df_proc["Aciertos_izq"] = resultados[:, 1]
    df_proc["Aciertos_der"] = resultados[:, 2]
    df_proc["Aciertos_largos"] = resultados[:, 3]

    actualizar_tabla(df_proc)

    # Graficar
    mostrar_graficas(resultados)

# -------------------------
# Gráficas
# -------------------------
def mostrar_graficas(resultados):
    zonas = ["Centro", "Izquierda", "Derecha", "Largos"]

    # Promedio de aciertos por zona
    promedios = resultados.mean(axis=0).reshape(1, 4)

    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    sns.heatmap(promedios, annot=True, fmt=".1f", cmap="YlGnBu", xticklabels=zonas, ax=ax[0])
    ax[0].set_title("Promedio de aciertos por zona")

    totales = resultados.sum(axis=0)
    ax[1].bar(zonas, totales, color="skyblue")
    ax[1].set_title("Total de aciertos por zona")
    ax[1].set_ylabel("Aciertos totales")

    plt.tight_layout()
    plt.show()

# -------------------------
# Tabla
# -------------------------
def actualizar_tabla(df):
    for i in tabla.get_children():
        tabla.delete(i)
    tabla["columns"] = list(df.columns)
    tabla["show"] = "headings"

    for col in df.columns:
        tabla.heading(col, text=col)
        tabla.column(col, width=120)

    for _, row in df.iterrows():
        tabla.insert("", "end", values=list(row))

# -------------------------
# Interfaz gráfica
# -------------------------
df = pd.DataFrame()

root = tk.Tk()
root.title("Simulación Deportiva Compacta")
root.geometry("1200x600")

# Botones
frame_btn = tk.Frame(root)
frame_btn.pack(pady=10)

btn_gen = tk.Button(frame_btn, text="Generar Dataset", width=18, command=generar_dataset)
btn_load = tk.Button(frame_btn, text="Cargar Archivo", width=18, command=cargar_archivo)
btn_save = tk.Button(frame_btn, text="Guardar Dataset", width=18, command=guardar_archivo)
btn_sim = tk.Button(frame_btn, text="Ejecutar Simulación", width=18, command=ejecutar_simulacion)

btn_gen.grid(row=0, column=0, padx=5)
btn_load.grid(row=0, column=1, padx=5)
btn_save.grid(row=0, column=2, padx=5)
btn_sim.grid(row=0, column=3, padx=5)

# Tabla
tabla = ttk.Treeview(root)
tabla.pack(expand=True, fill="both")

root.mainloop()
