#!/usr/bin/python3
#-*- coding: utf-8 -*-

import numpy as np
import affichage

import algo
import data

import random

"""
    Etude des modes d'un pont 
"""

## Attention : Pour executer le programme, il faut utiliser python3 main.py

##----------------------------------
# But du programme :
# 1. Visualisation pont.
# 2. Calcul des modes propores.
butPrgm = "1"
print("Que souhaitez vous faire ?")
print(" 1. Visualiser la structure du pont.")
print(" 2. Calculer les modes.")
butPrgm = input("Entrer le choix : ")

print("Debut")
##----------------------------------

##----------------------------------
nomData = ""
# Choix des donnees :
# 1. Pont simple
# 2. Votre Pont
choixData = "1"
print("Choix donnees ?")
print(" 1. Pont simple")
print(" 2. Votre Pont.")
choixData = input("Entrer le choix : ")


listeNoeuds = []
listeArcs = []
listeMasse = []
listeFixation = []

if (choixData=="1"):
    listeNoeuds = np.genfromtxt("PontN.data", delimiter="\t")
    listeArcs = np.genfromtxt("PontA.data", delimiter="\t")
    listeMasse = np.genfromtxt("PontM.data", delimiter="\t")
    listeFixation = np.genfromtxt("PontF.data", delimiter="\t")

print("")

if (choixData=="2"):
    listeNoeuds = np.genfromtxt("NotrePontN.data", delimiter="\t")
    listeArcs = np.genfromtxt("NotrePontA.data", delimiter="\t")
    listeMasse = np.genfromtxt("NotrePontM.data", delimiter="\t")
    listeFixation = np.genfromtxt("NotrePontF.data", delimiter="\t")

print("")
##----------------------------------


##----------------------------------
# Visualiser donnees dessin :
if (butPrgm=="1"):
    
    affichage.afficherPont(listeNoeuds, listeArcs)
##----------------------------------    
    
    
##----------------------------------
# Test dessin :
if (butPrgm=="2"):
    
    [M,K] = data.generateMatricePont(listeNoeuds, listeArcs, listeMasse, listeFixation)
    
    
    
    # Nombre de modes calculé :
    nbMode = 1
    print("Combien de modes souhaitez-vous calculer ?")
    nbMode = input("Entrer le choix : ")
    nbMode = int(nbMode)
        
    # Resolution du probleme aux valeurs propres
    (dimX,dimY) = M.shape
    print(dimX,dimY)
    x0 = np.random.rand(dimY)*0.9+1.0
    # Calcul des modes :
    [LL,VV] = algo.puInv(K,M,x0,nbMode,100,1e-5)
    # print(VV)
     
    # Affinage :
    print("Affinage :")
    for i in range(nbMode):
        print("Mode ",i," / ",nbMode)
        #res = algo.puInv(K - (LL[i]-1e-10)*np.identity(dimX),D,VV[i],1,500,1e-10)
        res = algo.puInv(K - (LL[i]-1e-10)*M,M,VV[i],1,500,1e-10)
        LL[i] = res[0][0]+LL[i]
        VV[i] = np.copy(res[1][0])*1.0

    print("Liste valeurs propres : ")
    print(LL)

    choixMode = "0"
    while(choixMode != "-1"):
        print("Quel mode souhaitez-vous visualiser ? (Entrer un nombre entre 0 et Nmode-1, ou -1 pour arreter le programme)")
        choixMode = input("Entre le choix : ")
        mode = int(choixMode)
        
        if(choixMode == "-1"):
            break
        
        vv = np.random.rand(len(listeNoeuds)*3)*0.0
        listePts = []
        for i in range(len(listeNoeuds)):
            fixe = False
            for e in listeFixation:
                if (i==int(e)):
                    fixe = True
                    break
            if(fixe == False):
                listePts.append(i)
            
        for j,e in enumerate(listePts):
            vv[3*e] = VV[mode][3*j]
            vv[3*e+1] = VV[mode][3*j+1]
            vv[3*e+2] = VV[mode][3*j+2]        
    
        affichage.afficherAnimationPont(listeNoeuds, listeArcs,LL[mode],vv)
##----------------------------------



print("FIN \n")
########################################
