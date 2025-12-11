import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

DIST=["Corta","Media","Larga"]
OBJ=["centro","izq","der","largos"]
rng=np.random.default_rng()

root=tk.Tk(); root.title("Simulación Penales 1000 equipos")
txt=tk.Text(root,width=55,height=12); txt.pack(pady=5)
frame=tk.Frame(root); frame.pack()

def generar_csv():
    if not os.path.exists("equipos_1000.csv"):
        N=1000
        data={"Equipo":[f"Rival {i+1}" for i in range(N)],
              "Prom_centro": rng.integers(2,10,N),
              "Prom_izq": rng.integers(1,7,N),
              "Prom_der": rng.integers(1,7,N),
              "Prom_largos": rng.integers(0,4,N),
              "Prob_centro": np.round(rng.uniform(0.4,0.9,N),2),
              "Prob_izq": np.round(rng.uniform(0.25,0.8,N),2),
              "Prob_der": np.round(rng.uniform(0.25,0.8,N),2),
              "Prob_largos": np.round(rng.uniform(0.05,0.45,N),2)}
        pd.DataFrame(data).to_csv("equipos_1000.csv",index=False)
        txt.insert("end","Archivo 'equipos_1000.csv' generado automáticamente.\n")
    else: txt.insert("end","Archivo 'equipos_1000.csv' ya existe.\n")

def cargar():
    global df
    ruta=filedialog.askopenfilename(initialdir=".",filetypes=[("CSV","*.csv"),("Excel","*.xlsx")])
    if ruta: df=pd.read_csv(ruta) if ruta.endswith(".csv") else pd.read_excel(ruta); txt.insert("end",f"'{os.path.basename(ruta)}' cargado.\n")

def simular():
    matriz=np.zeros((3,4),int); tiros_totales=np.zeros((3,4),int); detalles=[]
    for _,r in df.iterrows():
        fila={}
        for di,d in enumerate(DIST):
            for oi,o in enumerate(OBJ):
                prom_partido=max(0.1, r[f"Prom_{o}"]*rng.normal(1,0.25))
                tiros=rng.poisson(prom_partido)
                goles=rng.binomial(tiros,r[f"Prob_{o}"])
                matriz[di,oi]+=goles
                tiros_totales[di,oi]+=tiros
                fila[f"{d}_{o}"]=goles
        detalles.append(fila)
    pd.DataFrame(detalles).to_csv("resultados.csv",index=False)
    mostrar_resultados(matriz, tiros_totales)

def mostrar_resultados(m, t):
    txt.delete("1.0","end")
    txt.insert("end","Matriz de goles:\n"+str(pd.DataFrame(m,index=DIST,columns=[x.capitalize() for x in OBJ]))+"\n\n")
    pct=(1 - m/t.clip(min=1))*100
    txt.insert("end","Porcentaje de atajadas (%):\n"+str(pd.DataFrame(np.round(pct,1),index=DIST,columns=[x.capitalize() for x in OBJ]))+"\n")
    for w in frame.winfo_children(): w.destroy()
    fig, ax = plt.subplots(figsize=(5,4))
    im=ax.imshow(m/t.clip(min=1), cmap="Reds")
    ax.set_xticks(range(len(OBJ))); ax.set_xticklabels([x.capitalize() for x in OBJ])
    ax.set_yticks(range(len(DIST))); ax.set_yticklabels(DIST)
    for i in range(3):
        for j in range(4): ax.text(j,i,f"{m[i,j]}",ha="center",va="center",color="black")
    fig.colorbar(im, ax=ax, label="Goles/tiros")
    canvas=FigureCanvasTkAgg(fig,master=frame); canvas.draw(); canvas.get_tk_widget().pack()

tk.Button(root,text="Generar archivo de 1000 equipos",command=generar_csv).pack(pady=2)
tk.Button(root,text="Cargar archivo CSV/Excel",command=cargar).pack(pady=2)
tk.Button(root,text="Simular 1000 partidos",command=simular).pack(pady=2)
root.mainloop()
