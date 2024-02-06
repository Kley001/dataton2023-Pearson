pip install pulp

# -*- coding: utf-8 -*-
"""
Created on Oct

@authors: mn4n4m-jiurgi-Kley001 'Pearson'
"""

import pandas as pd
from pulp import *


# Leer los Datos de los Archivos Excel
demand = pd.read_excel("", sheet_name="demand")
workers = pd.read_excel("", sheet_name="workers")

print("Datos de demanda:")
print(demand.head())
print("\nDatos de los trabajadores:")
print(workers.head())

# Problema de Optimización
prob = LpProblem("Asignacion de los Estados", LpMinimize)

# Variables
empleados = workers['documento'].tolist()
franjas = demand['fecha_hora'].tolist()
estados = ["Trabaja", "Pausa Activa", "Almuerza", "Nada"]

x = LpVariable.dicts("x", (empleados, franjas, estados), cat='Binary')

# Función Objetivo
prob += lpSum([x[e][f][s] for e in empleados for f in franjas for s in estados])


# Restricción Mínimo 4 franjas horarias continuas antes de una pausa activa o almuerzo
for e in empleados:
    for i, f in enumerate(franjas):
        if i <= len(franjas) - 4:
            prob += lpSum([x[e][franjas[j]][estados[0]] for j in range(i, i+4)]) >= x[e][f][estados[1]] + x[e][f][estados[2]]

# Restricción Máximo 8 franjas horarias continuas sin una pausa activa
for e in empleados:
    for i, f in enumerate(franjas):
        if i <= len(franjas) - 8:
            prob += lpSum([x[e][franjas[j]][estados[1]] for j in range(i, i+8)]) == 0
# Restricción Franja mínima y máxima para tomar el almuerzo
for e in empleados:
    prob += lpSum([x[e][f][estados[2]] for f in franjas[:16]]) == 0
    prob += lpSum([x[e][f][estados[2]] for f in franjas[24:]]) == 0


# Restricción Tiempo de almuerzo con 6 franjas horarias continuas
for e in empleados:
    for i, f in enumerate(franjas):
        if i <= len(franjas) - 6:
            prob += lpSum([x[e][franjas[j]][estados[2]] for j in range(i, i+6)]) == 1



# Restricción Jornada laboral con 32 franjas diarias
for e in empleados:
    prob += lpSum([x[e][f][estados[0]] + x[e][f][estados[1]] for f in franjas]) == 32

# Restricción Último Estado de jornada laboral debe ser "Trabaja"
for e in empleados:
    prob += lpSum([x[e][f][estados[0]] + x[e][f][estados[1]] + x[e][f][estados[2]] for f in franjas]) >= 1

# Restricción Al menos 1 empleado en el estado "Trabaja" en cada franja horaria
for f in franjas:
    prob += lpSum([x[e][f][estados[0]] for e in empleados]) >= 1

# Restricción: Cada empleado puede iniciar en diferentes franjas horarias
for e1 in empleados:
    for e2 in empleados:
        if e1 != e2:
            for f in franjas:
                prob += x[e1][f][estados[0]] + x[e2][f][estados[0]] <= 1
'''
# Restricción: Si la jornada no inicia con "Trabaja," asignar "Nada"
for e in empleados:
    for i, f in enumerate(franjas):
        if i > 0:
            prob += x[e][f][estados[0]] + x[e][franjas[i-1]][estados[0]] + x[e][f][estados[3]] == 2

# Restricción: Si la jornada no termina con "Trabaja," asignar "Nada"
for e in empleados:
    for i, f in enumerate(franjas):
        if i < len(franjas) - 1:
            prob += x[e][f][estados[0]] + x[e][franjas[i+1]][estados[0]] + x[e][f][estados[3]] == 2
'''

# Solución
prob.solve()

# Mostrar Los Resultados
for e in empleados:
    for f in franjas:
        for s in estados:
            if x[e][f][s].varValue == 1:
                print(f"Empleado {e} en la franja horaria {f}: {s}")

import pandas as pd

# Crear un diccionario para almacenar la solución
solucion = {"Empleado": [], "Franja Horaria": [], "Estado": []}

# Recopilar la solución
for e in empleados:
    for f in franjas:
        for s in estados:
            if x[e][f][s].varValue == 1:
                solucion["Empleado"].append(e)
                solucion["Franja Horaria"].append(f)
                solucion["Estado"].append(s)

# Crear un DataFrame a partir del diccionario de solución
df_solucion = pd.DataFrame(solucion)

# Mostrar el DataFrame
print(df_solucion)

# Ruta al directorio en Google Colab donde deseas guardar el archivo CSV
directorio = "/content/"

# Nombre de archivo CSV
nombre_archivo = "solucion.csv"

# Guardar el DataFrame en un archivo CSV
df_solucion.to_csv(directorio + nombre_archivo, index=False)

'''

opción

# Definir las variables binarias para controlar si la demanda supera la capacidad
y = LpVariable.dicts("exceso_demanda", franjas, cat='Binary')

# Restricciones para y[f]: y[f] = 1 si la demanda supera la capacidad en la franja f
for f in franjas:
    prob += y[f] >= demanda[f] - lpSum(x[e][f][s] for e in empleados for s in estados) - capacidad[f]  # y[f] >= demanda - capacidad
    prob += y[f] <= demanda[f] - lpSum(x[e][f][s] for e in empleados for s in estados) + capacidad[f]  # y[f] <= demanda + capacidad

# Función objetivo: Minimizar la suma de las variables binarias
prob += lpSum(y[f] for f in franjas)

# Resuelve el problema
prob.solve()

# Mostrar Los Resultados
for e in empleados:
    for f in franjas:
        for s in estados:
            if x[e][f][s].varValue == 1:
                print(f"Empleado {e} en la franja horaria {f}: {s}")