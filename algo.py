import numpy as np
import copy

import data

# Algorithme de la puissance inverse avec deflation :
# - Entree : K (matrice : rigidite), M (matrice : masse), xo (vecteur : propre initial), m (entier : nombre de vp qu'on calcule), iteMax (entier), err (reel : tolerance erreur)
# - Sortie : vp (list : liste des valeurs propres), V (liste : liste des vecteurs propres) 
def puInv(K,M,x0,m,iteMax,err):
    # Factorisation QR de K, faites une fois.        
    [Q,R] = qr(K)
    (n,p) = K.shape
    
    # On determine les modes statiques, c est a dire le noyau de K :
    DDzero = []
    for i in range(n):
        if(np.abs(R[i,i]) < 1e-15):
            DDzero.append(i)
    VVzero = []        
    for e in DDzero:
        y = remontee(R[0:e,0:e],R[0:e,e])
        vv = x0*0
        vv[0:e] = -y
        vv[e] = 1
        normvv = np.sqrt(np.dot(np.dot(M,vv),vv))
        vv = vv / normvv
        VVzero.append(vv)
     
    # Liste valeurs propres   
    vp = []
    # Liste vecteurs prorpes
    V = [] 
    ite = 1
    x00 = np.copy(x0)*1.0
    for k in range(m):
        print("Etape ",k)
        x0 = x00  + np.random.rand(len(x0))*err
        
        # On elimine les modes statiques du vecteur x0
        for i in VVzero:
            x0 = x0 - np.dot(np.dot(M,x0),i)*i
        
        # Deflation :
        for i in range(k):
            # Completer ICI :
            x0 = x0 - np.dot(np.dot(M,x0),V[i])*V[i]
                
        # M-Normalisation :
        x0 = x0 / np.sqrt(np.dot(np.dot(M,x0),x0))
        
        # Calcul de x1 = K^{-1} M x0 :
        ty = np.dot(Q.transpose(),np.dot(M,x0))
        y = remontee(R[0:p,0:p],ty[0:p])
        
        # M-Normalisation :
        x1 = y / np.sqrt(np.dot(np.dot(M,y),y))
        
        # On commence les iterations :
        ite = 0
        while(np.abs(np.abs(np.dot(x0,x1))  -1) > err and ite < iteMax):
            # On elimine les modes statiques
            for i in VVzero:
                x1 = x1 - np.dot(np.dot(M,x1),i)*i
                
            # Deflation : 
            # Completer ICI :      
            for i in range(k):
                x1 = x1 - np.dot(np.dot(M,x1),V[i])*V[i]
            
            # M-Normalisation :    
            x0 = x1/np.sqrt(np.dot(np.dot(M,x1),x1))
            
            
            # Calcul de x_{k+1} = K^{-1} M x_k :        
            ty = np.dot(Q.transpose(),np.dot(M,x0))
            y = remontee(R[0:p,0:p],ty[0:p])
            
            # M-Normalisation :
            x1 = y/np.sqrt(np.dot(np.dot(M,y),y))
            
            # Iteration suivante :
            ite = ite+1
            
        print("Nb ite :",ite,np.abs(np.abs(np.dot(x0,x1)) -1))
        
        # On ajoute le vecteur x0 à la liste de vecteurs propres
        V.append(x0)
        jmax = 0
        emax = -1.0
        for j,e in enumerate(y):
            if np.abs(e) >= emax: 
                jmax = j
                emax = np.abs(e)
        # et on ajoute la nouvelle valeur propre.        
        vp.append(x0[jmax]/y[jmax])
        print("valeur propre ",vp[-1])
        print("\n")
    return [vp,V]


# Resolution de U x = b
#  - Entree : U (matrice), b (vecteur)
#  - Sortie : x (Vecteur)
def remontee(U,b):
    (n,p) = U.shape
    x = np.zeros(n)
    for l in range(n-1,-1,-1):
        x[l] = b[l]
        for c in range(l+1,n):
            x[l] = x[l] - U[l,c]*x[c]
        if (np.abs(U[l,l]) < 1e-10 ):
            x[l] = 0.0
        else :
            x[l] = x[l] / U[l,l]

    return x

# Resolution de L x = b
#  - Entree : L (matrice), b (vecteur)
#  - Sortie : x (Vecteur)
def descente(L,b):
    (n,p) = L.shape
    x = np.zeros(n)
    for l in range(n):
        x[l] = b[l]
        for c in range(l):
            x[l] = x[l] - L[l,c]*x[c]
        x[l] = x[l] / L[l,l]

    return x


# Factorisation QR
#  - Entree : A (matrice)
#  - Sortie : Q (matrice), R (matrice)
def qr(A):
    (n,p) = A.shape
    # Declaration des variables et initialisation
    Q = np.zeros((n,p))
    R = np.zeros((p,p))
    
    
    # Orthonormalisation G.S.
    for i in range(p):
        v = A[:,i]
        for j in range(i):
            scal = np.dot(v,Q[:,j])
            v = v - scal * Q[:,j]
            R[j,i] = scal
        normV = np.sqrt(np.dot(v,v))
        R[i,i] = normV
        if (normV > 1e-15):
            Q[:,i] = v / normV
    return [Q,R]
    
