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




Vaj=[-0.8978, -0.8561, -0.8081, -0.7436, -0.6838, -0.6067, -0.5784, -0.5185, -0.4132, -0.2461, -0.0444, 0.1923, 0.3419, 0.4235, 0.5384, 0.5666, 0.5799, 0.7099, 1.1280, 1.3909, 1.5334, 1.6370, 1.6943, 1.7315, 1.7610]


 #Le volume ajouté, préciser votre unité lors du ax.set_xlabel
for i in range(len(Vaj)):
    Vaj[i]=-(0.241-Vaj[i])


deltaVaj=[0.0002 for _ in Vaj]# L'incertitude expérimentale associée

y=[-38.142, -30.244, -22.573, -13.625, -6.958, -2.103, -1.928, -1.003, -0.299, 0.020, 0.022, 0.228, 0.751, 0.931, 1.194, 1.460,1.4, 2.793, 7.1, 11.622, 14.976, 20.549, 27.549, 35.732, 43.850]



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
ax.set_axisbelow(True)
plt.title("Courbe i(E) de l'eau sur electrode de graphite pour w=500")
plt.show()
plt.tight_layout()#mise en forme du graphique
plt.savefig("graphique_suivi_titrage.png")#sauvegarde de votre graphique en .png




