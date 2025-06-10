#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 17:20:09 2024

@author: brian
objectifs du TP :
    - caractériser le bruit du générateur basse fréquence intégré à l'oscilloscope
    - Comprendre et prendre en main un algorithme de monte-carlo
    - mettre en évidence le phénomène de résonance stochastique
"""

# en cas d'erreur mentionnant scipy lors de la première installation, installer scipy en copiant la commande suivante dans la console : pip install scipy

import numpy as np
import matplotlib.pyplot as plt
from scipy import special
from scipy.optimize import curve_fit


plt.close('all') #On ferme tout graphique précédemment ouvert



fig,ax = plt.subplots(figsize=(13, 8))




Vaj=[-0.9178, -0.8747, -0.8353, -0.8049, -0.7610, -0.7275, -0.6548, -0.4922, -0.4313, -0.3595, -0.2320, -0.0777, 0.0937, 0.3400, 0.4030, 0.4830, 0.5771, 0.6695, 0.8034, 1.0647, 1.2777, 1.5164, 1.6065, 1.6668, 1.7078, 1.7370]
 #Le volume ajouté, préciser votre unité lors du ax.set_xlabel
for i in range(len(Vaj)):
    Vaj[i]=-(0.241-Vaj[i])


deltaVaj=[0.002 for _ in Vaj]# L'incertitude expérimentale associée

y=[-47.320, -39.348, -31.634, -25.579, -18.666, -15.624, -10.329, -3.941, -1.431, -0.603, -0.186, 0.200, 0.302, 0.789, 1.394, 1.406, 1.820, 2.020, 3.019, 5.404, 9.578, 13.715, 20.614, 27.975, 35.861, 43.960]

 #peut être un pH ou une conductivité, préciser le cas échéant votre unité lors du ax.set_xlabel.
deltay = [0.002 for _ in y] #L'incertitude associée à i





# On ajuste la fonction en utilisant curve_fit (minimisation de chi²)

Vaj = np.asarray(Vaj)
y = np.asarray(y)

N = int(1e3)
tempoY = []


ax.errorbar(Vaj,y,xerr=deltaVaj,yerr=deltay,marker='+', color = 'green', linestyle= '-',label='Mesures expérimentales',alpha=1) #le tracé des points expérimentaux


#si vous n'arrivez pas à faire converger l'ajustement, voici la ligne pour voir à quoi ressemble l'ajustement duquel vous faites partir l'algo
#plt.plot(x_fit, modele(x_fit, initial_guess[0], initial_guess[1]), color="black",linestyle= 'dotted' ,label="Ajustement avec les valeurs de départ")



#Affichage du graphique :
ax.legend(loc='best', fontsize=20)#légende des courbes
ax.set_xlabel('$E_{ET}$ (V)',fontsize=20)#légende des axes
ax.set_ylabel('i (mA)',fontsize=20)
ax.tick_params(axis='both', which='major', labelsize=20)
ax.tick_params(axis='both', which='minor', labelsize=20)

plt.text(-1.156, -20.6, r'H$_2 \longleftarrow$ H$_20$ ',   color='C0', fontsize=15)
plt.text(1.2, 20.6, r'HO$^{-} \longrightarrow$ O$_2$',   color='C0', fontsize=15)

# Mise en place d'une grille
ax.grid(which='major', color='#DDDDDD', linewidth=2)
ax.grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=1)
# Et on les affiche
ax.minorticks_on()
plt.title("Courbe i(E) de l'eau sur electrode de graphite pour w=0")
ax.set_axisbelow(True)
plt.show()
plt.tight_layout()#mise en forme du graphique
plt.savefig("graphique_suivi_titrage.png")#sauvegarde de votre graphique en .png




