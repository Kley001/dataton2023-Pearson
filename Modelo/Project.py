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

#Problema de Optimización
prob = LpProblem("Asignacion de los Estados", LpMinimize)

#Variables 
empleados = workers['documento'].tolist()

franjas = demand['fecha_hora'].tolist()

estados = ["Trabaja", "Pausa Activa", "Almuerza", "Nada"]

x = LpVariable.dicts("x", (empleados, franjas, estados), cat='Binary')

#Función Objetivo
prob += lpSum([x[e][f][s] for e in empleados for f in franjas for s in estados])

#Restricción Mínimo 4 franjas horarias continuas antes de una pausa activa o almuerzo
for e in empleados:
    for i, f in enumerate(franjas):
        if i <= len(franjas) - 4:
            prob += lpSum([x[e][franjas[j]][estados[0]] 
                           for j in range(i, i+4)]) >= x[e][f][estados[1]] + x[e][f][estados[2]]

#Restricción Máximo 8 franjas horarias continuas sin una pausa activa
for e in empleados:
    for i, f in enumerate(franjas):
        if i <= len(franjas) - 8:
            prob += lpSum([x[e][franjas[j]][estados[1]] 
                           for j in range(i, i+8)]) == 0

#Restricción Tiempo de almuerzo con 6 franjas horarias continuas
for e in empleados:
    for i, f in enumerate(franjas):
        if i <= len(franjas) - 6:
            prob += lpSum([x[e][franjas[j]][estados[2]] 
                           for j in range(i, i+6)]) == x[e][f][estados[2]]

#Restricción Franja mínima y máxima para tomar el almuerzo
for e in empleados:
    prob += lpSum([x[e][f][estados[2]] for f in franjas[:17]]) == 0
    prob += lpSum([x[e][f][estados[2]] for f in franjas[25:]]) == 0

#Restricción Jornada laboral con 32 franjas diarias
for e in empleados:
    prob += lpSum([x[e][f][estados[0]] + x[e][f][estados[1]] 
                   for f in franjas]) == 32

#Restricción Último Estado de jornada laboral debe ser "Trabaja"
for e in empleados:
    prob += lpSum([x[e][f][estados[0]] + x[e][f][estados[1]] + x[e][f][estados[2]] 
                   for f in franjas]) >= 1

#Restricción Al menos 1 empleado en el estado "Trabaja" en cada franja horaria
for f in franjas:
    prob += lpSum([x[e][f][estados[0]] for e in empleados]) >= 1

#Solución
prob.solve()

#Mostrar Los Resultados
for e in empleados:
    for f in franjas:
        for s in estados:
            if x[e][f][s].varValue == 1:
                print(f"Empleado {e} en la franja horaria {f}: {s}")