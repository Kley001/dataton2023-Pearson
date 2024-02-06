# -*- coding: utf-8 -*-
"""
Created on Oct 

@author: mn4n4m jiurgi Kley001
"""

import pandas as pd
from pulp import *

# Leer los datos de los archivos Excel
demand = pd.read_excel("", sheet_name="demand")
workers = pd.read_excel("", sheet_name="workers")
print(demand.head())
print(workers.head())

# Definimos las variables del modelo
n_empleados = len(workers) #Número de empleados
n_franjas_horarias = len(demand) #Número de franjas horarias

x = LpVariable.dicts("x", ((i, j, k) for i in range(n_empleados) for j in range(n_franjas_horarias) for k in range(4)), cat=LpBinary)

#x_ij1:	empleado i está en el estado Trabaja en la franja horaria j
#x_ij2:	empleado i está en el estado Pausa Activa en la franja horaria j
#x_ij3:	empleado i está en el estado Almuerza en la franja horaria j
#x_ij4:	empleado i está en el estado Nada en la franja horaria j

# Restricción 1: Un empleado no puede salir a su primera pausa activa o almuerzo si solo ha trabajado 3 franjas horarias.
#for i in range(n_empleados):
#  for j in range(n_franjas_horarias):    
#    if j <= 3:
#      x[i, j, 2] + x[i, j, 3] <= 1
#          
#    else:
#      x[i, j, 2] + x[i, j, 3] <= x[i, j - 4, 1]


# Restricción los empleados deben trabajar mínimo 4 franjas continuas para poder salir a una Pausa Activa o Almuerzo

for i in range(n_empleados):
    for j in range(n_franjas_horarias):
        if j >= 3:
            x[i, j, 2] + x[i, j, 3] <= x[i, j-3, 1]

# Restricción los empleados deben trabajar máximo 8 franjas continuas sin salir a una Pausa Activa

for i in range(n_empleados):
    for j in range(n_franjas_horarias):
        if j >= 7:
            x[i, j-7, 1] + x[i, j-6, 1] + x[i, j-5, 1] + x[i, j-4, 1] + x[i, j-3, 1] + x[i, j-2, 1] + x[i, j-1, 1] + x[i, j, 1] <= 7            

for i in range(n_empleados):
    for j in range(n_franjas_horarias):
        if j >= 7:
            suma_franja = sum(x[i, k, 1] for k in range(j-7, j+1))
            if suma_franja >= 8:
                suma_franja <= 7
