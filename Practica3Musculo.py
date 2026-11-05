"""
Práctica 3: Modelado y control del sistema musculoesqueletico 

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Morales Diaz Ramon Ivan 
Número de control: 24210589
Correo institucional: l24210589@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
import matplotlib.pyplot as plt
import numpy as np
import control as ctrl

#Datos
x0,t0,tend,dt,w,h = 0,0,10,1E-3,7,3.5
n = round((tend-t0)/dt) + 1
t = np.linspace(t0,tend,n)
F = np.zeros(n); F[round(1/dt):round(2/dt)] = 1

#Datos del PI
kP = 0.218837731319984
kI = 3640.74282297537

#Funcion de transferencia de control
a,b,c,d = 100*10e-6, 1-0.25, 100*(100e-6+10e-6), 1
num = [a,b]
den = [c,d]
control = ctrl.tf(num,den)
print(f"Funcion de transferencia del control: {control}\n")

#Funcion de transferencia de caso
num = [10e3*10e-6,1-0.25]
den = [10e3*(100e-6+10e-6),1]
caso = ctrl.tf(num,den)
print(f"Funcion de transferencia del caso: {caso}\n")

# Controlador PI
numPI = [kP, kI]
denPI = [1, 0]
PI = ctrl.tf(numPI,denPI)
sysPI = ctrl.feedback(ctrl.series(PI,caso),1,sign = -1)
print(f"Funcion de transferencia en Controlador: {sysPI}\n")

def closeloop(t,sysPI,u):
    _,y = ctrl.forced_response(sysPI,t,u,x0)
    return y

#Para plotear:
_, Fsx = ctrl.forced_response(control, t, F)   # Control
_, Fsy = ctrl.forced_response(caso, t, F)      # Caso
tratamiento = closeloop(t, sysPI, Fsx)

#Colores
clr1 = np.array([138, 99, 210])/255    
clr2 = np.array([201, 168, 0])/255    
clr3 = np.array([42, 26, 154])/255     
clr4 = np.array([0, 0, 0])/255         

#Grafica
fg = plt.figure(1)
fg.set_size_inches(w,h)

plt.rcParams["font.size"] = 11
plt.rcParams["font.serif"] = ["Times New Roman"]

plt.plot(t,F,"-",color=clr1,label="F(t)")
plt.plot(t,Fsy,":",color=clr3,label="Fsy(t): Caso")
plt.plot(t,Fsx,":",color=clr4,label="Fsx(t): Control")
plt.plot(t,tratamiento,"--",color=clr2,label="PID(t): Tratamiento")

plt.xlim(-0.25,10)
plt.xticks(np.arange(0, 11, 1))
plt.ylim(-0.1,1.1)
plt.yticks(np.arange(0, 1.1, 0.1))
plt.xlabel("t [s]")
plt.ylabel("F(t) [V]")
plt.legend(loc="best",ncol=2,frameon=False)
plt.grid()
plt.show()
fg.savefig("Tratamiento_python.pdf",bbox_inches="tight")