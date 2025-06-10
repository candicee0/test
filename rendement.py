from numpy import *
import matplotlib.pyplot as plt
Pcharge = [0, 200, 400, 600, 800]
umas=1 # En %
Pmas_RECU = [63, 68, 70, 78, 82]  # Puissance maximale reçue
Pmcc_recu = [30, 29.9, 29.9, 29.7, 29.7]
umcc=0.1  # Puissance MCC reçue
Pmcc_sortie = [18, 23, 28, 31, 38]
uch=umas
n=[]
un=[]
for i in range(len(Pcharge)):
    n.append(Pmcc_sortie[i]/(Pmas_RECU[i]+Pmcc_recu[i]))
    un.append(sqrt((1/(Pmas_RECU[i]+Pmcc_recu[i]) * uch)**2+(Pmcc_sortie[i]/(Pmas_RECU[i]+Pmcc_recu[i])**2 *umcc)**2+(Pmcc_sortie[i]/(Pmas_RECU[i]+Pmcc_recu[i])**2 *umas)**2))
plt.errorbar(Pcharge, n, yerr=un, fmt='o', label="Données", capsize=5, color='blue')
plt.plot(Pcharge, n, linestyle='--', color='blue', alpha=0.7)
# Ajout des labels, titre et légende
plt.xlabel('Pcharge')
plt.ylabel('rendement ')
plt.title('Courbe avec incertitudes')
plt.legend()
plt.grid(True)

# Affichage
plt.show()
plt.tight_layout()#mise en forme du graphique
plt.savefig("image_graphique.png")