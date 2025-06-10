#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 12:23:45 2025

Ce script s'exécute initialement dans un dossier contenant le fichier "gong.wav", que vous pourrez ensuite remplacer par votre acquisition.

@author: brian
"""
import math
try:
    import librosa  # nécessaire à l'import d'audio, acceptant à peu près n'importe quoi
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "librosa"])
    import librosa


import os
import numpy as np                   
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap  # pour la colormap des spectres tracés au cours du temps (t0,t1,t2)
import matplotlib as mpl  # pour la normalisation des couleurs 
#from IPython import get_ipython  # pour l'affichage des graphes dans une fenêtre hors IDE
#get_ipython().run_line_magic('matplotlib', 'qt')  # affichage des graphes dans une fenêtre hors IDE
def estimate_coef(x, y):
  """Implémentation simple d'une régression linéaire
  """
  # nb de points
  n = np.size(x)

  # moyenne des vecteurs en abscisse et ordonnée
  m_x = np.mean(x)
  m_y = np.mean(y)

  # calculating cross-deviation and deviation about x
  SS_xy = np.sum(y*x) - n*m_y*m_x
  SS_xx = np.sum(x*x) - n*m_x*m_x

  # calcul des coefficients de régression linéaire
  b_1 = SS_xy / SS_xx
  b_0 = m_y - b_1*m_x

  return (b_0, b_1)

# Augmenter la taille des polices pour tous les graphiques
mpl.rcParams.update({'font.size': 14})

plt.close("all")

# Le nom du fichier (à modifier si besoin)
file_path = 'v3.wav'

# ouverture du fichier audio
# sr = sampling rate, sr=None pour conserver la fréquence d'échantillonnage originelle, et mono=True car on ne veut pas gérer du stéréo ici
audio, sr = librosa.load(file_path, sr=None, mono=True)
print(f"Audio chargé contenant {len(audio)} échantillons à une fréquence d'échantillonnage de {sr} Hz.")

# Paramètres pour la TF
block_size = int(40000)  # taille temporelle ("largeur") de la fenêtre

hop_length = 10000  # nb de points du décallage lors d'un saut d'un t0 au t1, puis au t2 pour les spectres successifs
n_frames = (len(audio) - block_size) // hop_length + 1 #le nombre de TF sucessives que l'on va pouvoir calculer

if n_frames < 1:
    raise ValueError("Données audio insuffisantes: moins d'une fenêtre complète.")

# colormap personnalisée du bleu (début) au rouge (fin) pour reconnaitre les spectres
cmap = LinearSegmentedColormap.from_list("BlueRed", ["blue", "red"])

# Premier graphique : superposition des spectres successifs
plt.figure(figsize=(12, 8))
frame_start_times = []  # Pour enregistrer le temps de départ de chaque fenêtre (en secondes). On pourrait décider de centrer cette date sachant block_size et sr

# But : calculer et tracer le spectre pour chaque fenêtre glissante
for i in range(n_frames):
    start_idx = i * hop_length
    end_idx = start_idx + block_size
    block = audio[start_idx:end_idx]
    
    # Enregistrer le temps de départ (en secondes) de cette fenêtre
    frame_start_time = start_idx / sr
    frame_start_times.append(frame_start_time)
    
    #Calculer la FFT (rfft pour signal réel) et son amplitude
    fft_vals = np.fft.rfft(block)
    spectrum = np.abs(fft_vals)
    
    # axe des abscisses en fréquence
    freqs = np.fft.rfftfreq(block_size, d=1/sr)
    
    #On choisit une couleur selon la date du spectre (début = bleu, fin = rouge)
    color = cmap(i / (n_frames))
    
    # On trace le spectre
    alpha_value =  0.5+0.4 * (i / (n_frames))
    plt.plot(freqs, spectrum, color=color, alpha=alpha_value)

plt.xlabel("Fréquence (Hz)")
plt.ylabel("Amplitude (U.A.)")
plt.title("Spectres superposés au cours du temps")
plt.grid(True)

# création d'une barre de couleur indiquant la date chaque spectre
norm = mpl.colors.Normalize(vmin=min(frame_start_times), vmax=max(frame_start_times))
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=plt.gca())
cbar.set_label("Temps (s) du début de la fenêtre pour la TF")

plt.tight_layout()
plt.show()


#%%%

# Deuxième graphique : évolution de la densité spectrale de puissance  au cours du temps
fig2, ax2 = plt.subplots(figsize=(10, 5))

# Liste des intervalles [fi,fj] de fréquences pour lesquels calculer l'intégrale, ici on regarde potentiellement 3 modes différents.
#À ajuster à la main selon la corde choisie et les harmoniques étudiées.
intervals = [[245, 251],[329,333],[409,413],[494,499]]

# pour chaque intervalle, calculer la densité spectrale de puissance
for interval in intervals:
    integrals = []
    for i in range(n_frames):
        start_idx = i * hop_length
        end_idx = start_idx + block_size
        block = audio[start_idx:end_idx]
    
        # calcul de la TF et du spectre de puissance
        fft_vals = np.fft.rfft(block)
        spectrum = np.abs(fft_vals)**2
    
        #Liste d'abscisses en fréquence
        freqs = np.fft.rfftfreq(block_size, d=1/sr)
    
        # on sélectionne les indices correspondant à l'intervalle [fi,fj] en question
        mask = (freqs >= interval[0]) & (freqs <= interval[1])
        
        # Et on somme sur ces valeurs pour avoir l'intensité totale liée à ce mode.
        integral_value = np.trapz(spectrum[mask], freqs[mask])
        integrals.append(integral_value)
        
    integrals = [math.log(integrals) for integrals in integrals]
    # On trace l'évolution de l'intensité sonore en fonction du temps
    ax2.plot(np.asarray(frame_start_times), np.asarray(integrals), marker="o", linestyle="-",
             label=f"Intensité sonore à { (interval[0]+interval[1]) / 2 } Hz")
    
ax2.set_xlabel("Temps (s)")
ax2.set_ylabel("logarithme de l'Intensité sonore (∝ W/m²)")
ax2.set_title("")
ax2.grid(True)
ax2.legend()

plt.tight_layout()
plt.show()
fig,ax = plt.subplots(figsize=(13, 8))

#Insertion des valeurs  ------------------------------------------------------------------------------------



