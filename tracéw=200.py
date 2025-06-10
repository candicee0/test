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




Vaj=[-0.9144,-0.8766, -0.8352, -0.7959, -0.7723, -0.7110, -0.6970, -0.6419, -0.5940, -0.5185, -0.3915, 0.0875, 0.2238, 0.2542, 0.2794, 0.3601, 0.4614, 0.6361, 0.7442, 1.2866, 1.4272, 1.5585, 1.6512, 1.6908, 1.7250, 1.7556]

 #Le volume ajouté, préciser votre unité lors du ax.set_xlabel
for i in range(len(Vaj)):
    Vaj[i]=-(0.241-Vaj[i])

deltaVaj=[0.002 for _ in Vaj]# L'incertitude expérimentale associée

y=[-46.87,-38.896, -31.050, -23.672, -17.091, -12.772, -10.238, -3.408, -1.847, -1.197, -0.452, -0.400, -0.040, -0.028, 0.080, 0.403, 0.513, 1.840, 3.200, 6.520, 8.426, 13.286, 20.162, 27.777, 35.726, 43.900]


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
plt.title("Courbe i(E) de l'eau sur electrode de graphite pour w=200")
ax.set_axisbelow(True)
plt.show()

plt.tight_layout()#mise en forme du graphique
plt.savefig("graphique_suivi_titrage.png")#sauvegarde de votre graphique en .png




