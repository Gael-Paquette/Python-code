# Importations  des bibliothèques nécessaire pour utiliser le programme
from fltk import*
from math import floor, ceil
import sys
import doctest

#Dimension du jeu
taille_case = 50 # Dimension d'une case de SlitherLink
taille_fenetre = 15 # Dimension de la fenetre d'ouverture du jeu, de partie et de fin de jeu
taille_marge = 20 # Espace autorisés pour cliquer sur un segment de la grille
largeur_plateau = 40 # en nombre de cases
hauteur_plateau = 40 # en nombre de cases

ACCUEIL = True # Variable ACCUEILL qui permet de faire marcher le programme tant que ACCUEIL == True, Si ACCUEIL vaut False alors le programme s'éteint

#=====================================================================================================================
#===== Définition des fonctions nécessaires à la réalisation du jeu SlitherLink ======================================
#=====================================================================================================================

def grille_jeu(fichier):
    """
        Fonction prenant en paramètre un fichier de type texte afin de récupérer la grille.
        Elle renvoie un liste nommer 'indices' qui renvoie la grille.

        :param fichier:
        :return indices: list
    """
    indices = []
    fiche = open(fichier , 'r')
    for ligne in fiche:
        lst = []
        for element in ligne:
            if element != "\n":
                if element == "_":
                    element = None
                    lst.append(element)
                else:
                    try:
                        element = int(element)
                    except:
                        print("Les caractères utilisés dans le fichier ne respectent pas les règles pré-définie.")
                        sys.exit()
                    lst.append(element)
        indices.append(lst)
    return indices

def sommets_grille(indices):
    """
        Fonction qui prend en paramètre la liste indice et définit tous les sommets
        de la grille.
        
        :param indices: list
        :return sommets: list
    """
    sommets = []
    for x in range(len(indices[0])+1):
        for y in range(len(indices)+1):
            sommets.append((x,y))
    return sommets

def liste_segments(sommets, indices):
    """
        Fonction qui prend en paramètres les listes sommets et indices
        et qui renvoient la liste des segments possibles de la grille.

        :param sommets: list
        :param indices: list
        :return segments: list
    """
    segments = []
    for i in range(1, len(sommets)): # Construction de tous les segments à l'horizontale
        x, y = sommets[i-1]
        if y != (len(indices)):
            segments.append(((sommets[i-1]),(sommets[i])))
    for j in range(len(indices), len(sommets)): # Construction de tous les segments à la verticale
        segments.append(((sommets[j-len(indices)]), (sommets[j])))
    print(segments)
    return segments

def liste_cases(indices):
    """
        Fonction qui prend en paramètres la liste indices et qui renvoient
        la liste des coordonnées de chaque case.

        :param indices: list
        :return cases: list
    """
    cases = []
    for x in range(len(indices[0])):
        for y in range(len(indices)):
            cases.append((x,y))
    return cases

def affichage_grille(indices):
    """
        Fonction qui prend en paramètres la liste indices et la dictionnaire etat et qui
        affiche la grille et les indices de chaque case graphiquement. Elle renvoie la taille de la grille c'est à dire la dernière coordonnées du point afficher sur l'écran (en bas à droite)

        :param indices: list
        :return taille_grille: tuple
    """
    taille_grille = (0, 0) #Tupple de valeur qui permet de récupérer la taille de grille en largeur et longueur.
    # tracage des points nécessaire à la création de la grille de jeu
    x, y = 20, -30
    distance_point = 50
    for abscisse in range(len(indices[0])+1):
        for ordonnee in range(len(indices)+1):
            y = y + distance_point 
            point(x, y, couleur='black',epaisseur=3, tag='')
            if (abscisse == (len(indices[0]))) and (ordonnee == (len(indices))):
                taille_grille = (x, y)
        y = -30
        x = x + distance_point 
    # Marquage des indices sur les cases correspondante
    x0, y0 = -30, 20
    distance_point = 50
    for absc2 in range(len(indices[0])):
        for ordo2 in range(len(indices)):
            if indices[absc2][ordo2] != None:
                nombre = int(indices[absc2][ordo2])
                texte(x0 + 65, y0 + 20, nombre, taille=15, couleur='black')
            x0 = x0 + distance_point
        x0 = -30
        y0 = y0 + distance_point
    return taille_grille

def clic_vers_segment(x, y, taille_marge, taille_case, taille_grille):
    """
        Fonction qui convertie les coordonnées du clic du joueur en couple de points
        qui correspond au segment interdit. Ainsi on retrouve un couple de points compatible avec les fonctions de la tâche 1.

        :param x: int (abscisse du clic)
        :param y: int (ordonnee du clic)
        :param taille_marge: int (taille d'une marge)
        :param taille_case: int (taille d'une case)
        :param taille_grille: tuple (taille de la grille en longueur et en largeur)
        :return value or None: tuple (liste domportant une liste de deux coordonnées de points)
    """
    i, j = taille_grille
    if (x > i) or (y > j):
        return None
    elif (x < 20) or (y < 20):
        return None
    else:
        dx = (x - taille_marge) /taille_case
        dy = (y - taille_marge) /taille_case
        horizontal_line, vertical_line = False, False
        if -0.2 <= (dx - round(dx)) <= 0.2:
            x1, x2, vertical_line = round(dx), round(dx), True
        if -0.2 <= (dy - round(dy)) <= 0.2:
            y1, y2, horizontal_line = round(dy), round(dy), True
        if horizontal_line is True:
            x1, x2 = floor(dx), ceil(dx)
        if vertical_line is True:
            y1, y2 = floor(dy), ceil(dy)
        if (horizontal_line != vertical_line) and (0 <= x1 < i and 0 <= x2 < i and 0 <= y1 < j and 0 <= y2 < j):
            return ((y1, x1),(y2, x2))
        else:
            return None
   
def est_trace(etat, segment):
    """
        Fonction renvoyant True si segment est tracé dans etat, et False sinon.

        :param etat: dict
        :param segment: tuple
        :return True or False: boolean
    """
    if segment in etat:
        if etat[segment] == 1:
            return True
    return False

def est_interdit(etat, segment):
    """
        Fonction renvoyant True si segment est interdit dans etat, et False sinon.

        :param etat: dict
        :param segment: tuple
        :return True or False: boolean
    """
    if segment in etat:
        if etat[segment] == -1:
            return True
    return False

def est_vierge(etat, segment):
    """
        Fonction renvoyant True si segment est vierge dans etat, et False sinon.

        :param etat: dict
        :param segment: tuple
        :return True or False: boolean
    """
    if segment not in etat:
        return True
    return False

def tracer_segment(etat, segment):
    """
        Fonction modifiant etat afin de représenter le fait que segment est maintenant tracé.

        :param etat: dict
        :param segment: tuple
        :return True or False: boolean
    """
    for key in etat:
        if key ==  segment:
            etat[key] = 1
    else:
        etat[segment] = 1
    return etat

def interdire_segment(etat, segment):
    """
        Fonction modifiant etat afin de représenter le fait que segment est maintenant interdit.

        :param etat: dict
        :param segment: tuple
        :return True or False: boolean
    """
    for key in etat:
        if key == segment:
            etat[key] = -1
    else:
        etat[segment] = -1
    return etat
    
def effacer_segment(etat, segment):
    """
        Fonction modifiant etat afin de représenter le fait que segment est maintenant vierge.

        :param etat: dict
        :param segment: tuple
        :return True or False: boolean
    """
    if segment in etat:
        try:
            del etat[segment]
        except KeyError:
            pass
    return etat

def segments_traces(etat):
    """
        Fonction renvoyant la liste de tous les segments tracés dans le dictionnaire etat.

        :param etat: dict
        :return segment_traces: list
    """
    segments_traces = []
    for cle in etat:
        if etat[cle] == 1:
            if cle not in segments_traces:
                segments_traces.append(cle)
    return segments_traces

def segment_traces_adjacents(etat, sommet):
    """
        Fonction renvoyant la liste des segments tracés adjacents à sommet dans etat.

        :param etat: dict
        :param sommet: tuple
        :return segments_adjacents: list
    """
    segments_adjacents = []
    for cle in etat:
        if sommet in cle:
            if etat[cle] == 1:
                segments_adjacents.append(cle)
    return segments_adjacents
                
def segments_interdits(etat):
    """
        Fonction renvoyant la liste de tous les segments interdits présent dans le dictionnaire etat.

        :param etat: dict
        :param segments_interdits: list
    """
    segments_interdits = []
    for key in etat:
        if etat[key] == -1:
            if key not in segments_interdits:
                segments_interdits.append(key)
    return segments_interdits

def segments_interdits_adjacents(etat, sommet):
    """
        Fonction renvoyant la liste des segments interdits adjacents à sommet dans etat.

        :param etat: dict
        :param sommet: tuple
        :return segments_interdit: list
    """
    segments_interdit = []
    for key in etat:
        if sommet in key:
            if etat[key] == -1:
                segments_interdit.append(key)
    return segments_interdit

def segments_vierges(etat, sommet, segments):
    """
        Fonction renvoyant la liste des segments vierges adjacents à sommet dans etat.

        :param etat: dict
        :param sommet: tuple
        :param segments: list
        :return segments_vierges: list
    """
    segments_vierges = []
    for key in etat:
        if sommet not in key:
            for segment in segments:
                a, b = segment
                if ((a == sommet) or (b == sommet)) and (segment not in segments_vierges):
                    segments_vierges.append(segment)
    return segments_vierges

def statut_case(indices, etat, case):
    """
        Fonction recevant le tableau indices, l'état de la grille et les coordonnées d'une case
        et renvoyant None si ceet case ne porte aucun indice, 0 si l'indice est satisfait,
        un entier positif si il est encore possible de satisfaire l'indice en traçant des segments autour de la case,
        un entier negatif si il n'est plus possible de satisfaire l'indice parce que trop de segments sont déjà trcés ou interdits autour de la case.

        :param indices: list
        :param etat: dict
        :param case: tuple
        :return nb or None: int or None
    """
    for abscisse in range(len(indices[0])):
        for ordonnee in range(len(indices)):
            if (abscisse, ordonnee) == case:
                x, y = case
                cpt = 0
                for key in etat:
                    a, b = key
                    if ((a == case) or (b == (x+1, y+1))) and (etat[key] == 1):
                        cpt += 1
                if indices[x][y] != None:
                    if cpt == int(indices[x][y]):
                        return 0
                    elif cpt > int(indices[x][y]):
                        nb = cpt - indices[x][y]
                        return -nb
                    elif cpt < int(indices[x][y]):
                        nb = indices[x][y] - cpt
                        return nb
                else:
                    return None

def condition_fin1(indices, etat, cases):
    """
        Fonction qui renvoie True si l'indice de chaque case est satisfait et False sinon.

        :param indices: list
        :param etat: dict
        :param cases: list
        :return True of False: boolean
    """
    statuts_cases = []
    for case in cases:
        statuts_cases.append(statut_case(indices, etat, case))

    for elem in statuts_cases:
        if elem != 0 and elem != None:
            return False
    return True

def longueur_boucle(etat, segment):
    """
        Fonction qui prend en paramètres le dictionnaire etat et un segment et qui calcul et renvoye la longueur de la boucle.

        :param etat: dict
        :param segment: tuple
        :return len_boucle: int
    """
    depart, courant = segment
    precedent = depart
    len_boucle = 1
    while courant != depart:
        segment_trace = segment_traces_adjacents(etat, courant)
        if len(segment_trace) != 2:
            return None
        for segment in segment_trace:
            for sommet in segment:
                if sommet != precedent and sommet != courant:
                    len_boucle += 1
                    precedent = courant
                    courant = sommet
                    if courant == depart:
                        return len_boucle

def effacement_segments(tracage_segments):
    """
        Fonction qui prend en paramètres la liste des segments vierges, et la liste du tracage des segments.
        Puis qui s'occupe d'effacer les segments précédent.

        :param tracage_segments: list
    """
    for element in tracage_segments:
        efface(element)

def affichage_etat_segments(liste_segments_traces, liste_segments_interdits):
    """
        Fonction qui prend en paramètres la liste de tous les segments tracés, ainsi que la liste des segments interdits.
        Puis qui s'occupe d'afficher l'état en question pour chaque segments.

        :param liste_segments_traces: list
        :param liste_segments_interdits: list
        :return tracage_segments: list
    """
    tracage_segments = list()
    for segment_trace in liste_segments_traces:
        A, B = segment_trace
        x1, y1 = A
        x2, y2 = B
        x1, y1, x2, y2 = 20 + y1 * 50, 20 + x1 * 50, 20 + y2 * 50, 20 + x2 * 50
        if y1 == y2:
            segment_trace = ligne(x1 + 3, y1, x2 - 3, y2, couleur='black', epaisseur=2, tag='')
            tracage_segments.append(segment_trace)
        elif x1 == x2:
            segment_trace = ligne(x1, y1 + 3, x2, y2 - 3, couleur='black', epaisseur=2, tag='')
            tracage_segments.append(segment_trace)
    for segment_interdit in liste_segments_interdits:
        C, D = segment_interdit
        i1, j1 = C
        i2, j2 = D
        i1, j1, i2, j2 = 20 + j1 * 50, 20 + i1 * 50, 20 + j2 * 50, 20 + i2 * 50
        if j1 == j2:
            milieu = (i1 + i2)//2
            segment_interdit = ligne(milieu - 5, j1 - 5, milieu + 5, j2 + 5, couleur='red', epaisseur=2, tag='')
            tracage_segments.append(segment_interdit)
            segment_interdit = ligne(milieu - 5, j1 + 5, milieu + 5, j2 - 5, couleur='red', epaisseur=2, tag='')
            tracage_segments.append(segment_interdit)
        elif i1 == i2:
            milieu = (j1 + j2)//2
            segment_interdit = ligne(i1 - 5, milieu - 5, i2 + 5, milieu + 5, couleur='red', epaisseur=2, tag='')
            tracage_segments.append(segment_interdit)
            segment_interdit = ligne(i1 + 5, milieu - 5, i2 - 5, milieu + 5, couleur='red', epaisseur=2, tag='')
            tracage_segments.append(segment_interdit)
    return tracage_segments

#===============================================================================================================================
#==== Solveur ==================================================================================================================
#===============================================================================================================================
def solveur(etat, sommet, indices, cases):
    """
        Fonction qui prend en paramètres le dictionnaire etat, un sommet, la liste indices et la liste cases.
        Et qui renvoie une solution à la grille.

        :param etat: dict
        :param sommet: list
        :param indices: list
        :param cases: list
        :return True or false: boolean
    """
    segments_adjacent = segment_traces_adjacents(etat, sommet)
    if len(segments_adjacent) == 2:
        if condition_fin1(indices, etat, cases):
            return True
        return False
    if len(segments_adjacent) > 2:
        return False
    adjacents_non_traces = segments_vierges(etat, sommet, segments)
    
    for segment in adjacents_non_traces :
        cases_des_segment = case_d_un_segment(segment)
        for case in cases_des_segment:
            if statut_case(indices, etat, case) != None:
                if statut_case(indices, etat, case)>= 0: #TODO
                    tracer_segment(etat, segment)
                    solution = solveur(etat, segment, indices, cases)
                    if solution == True:
                        return True
                    else:
                        effacer_segment(etat, segment)
                        return False
            
def case_d_un_segment(segment):
    """
        Fonction qui prend en paramètre un segment et qui renvoie une liste des cases adjacentes au segment.

        :param segment: tuple
        :return case: list
    """
    A, B = segment
    x1, y1 = A
    x2, y2 = B
    cases = []
    if x1 == x2:
        cases.append((x1, y1 - 1))
        cases.append((x1, y1 + 1))
    elif y1 == y2:
        cases.append((x1 - 1, y1))
        cases.append((x1 + 1, y1))
    return cases

def chemin_optimal(indices, cases, n):
    """
        Fonction qui prend en paramètres la liste indices, la liste cases et une variable n.
        Puis qui renvoie les coordonées du prochain sommets.

        :param indices: list
        :param cases: list
        :param n: int
        :return : tuple
    """
    ### lors de l'appel de fonction on pose n = 3###
    if n < 1:
        return None
    for i in range(len(indices)):
        for j in range(len(indices[0])):
            if indices[i][j] == n:
                return ((i, j))
            elif i == len(indices) and j == len(indices[0]):
                return chemin_optimal(indices, cases, n - 1)
            
#===============================================================================================================================
#===== Corps du programme qui permet le fonctionnement du jeu SlitherLink ======================================================
#===============================================================================================================================

if __name__ == "__main__":
    while ACCUEIL == True:
        # Création de la fenêtre Tk pour le jeu
        cree_fenetre(taille_fenetre * largeur_plateau, taille_fenetre * hauteur_plateau)
        rectangle(0, 0, 600, 600, couleur='grey', remplissage='grey') # Fond d'écran de la page d'accueil.
        # Phase d'initialisation du jeu
        bouton_start = [(250,350),(350,400)] # Création d'un bouton start pour pouvoir lancer le jeu.
        rectangle(bouton_start[0][0], bouton_start[0][1], bouton_start[1][0], bouton_start[1][1], couleur='purple', remplissage='purple', epaisseur=1, tag='accueil') # Permet de définir la forme du bouton
        texte(270, 360, f"START", taille=15, couleur = 'white') # Texte présent sur le bouton, dans ce cas 'START'.
        texte(170, 270, f"Welcome to the game 'SlitherLink'\n    Press start button to play", taille=15, couleur="black") # Texte descriptif de début de partie

        Jouer = False # Initialisation de la variable 'Jouer' qui permettra de jongler entre les différentes phases du jeu SlitherLink
        appuyer = attend_clic_gauche() # Permet de savoir quand l'utilisateur à cliquer sur quelle chose
        while Jouer == False:
            if bouton_start[0][0] <= appuyer[0] and appuyer[0] <= bouton_start[1][0] and \
               bouton_start[0][1] <= appuyer[1] and appuyer[1] <= bouton_start[1][1]:
                # On teste si l'utilisateur à cliquer sur le bouton_start pour commencer une nouvelle partie. Si c'est la cas alors la partie commence
                # Sinon, le programme attend que l'utilisatedru appuye sur le bouton_start
                efface_tout()
                Jouer = True

        # Phase de choix de la grille
        rectangle(0, 0, 600, 600, couleur='white', remplissage='white') # Fond d'écran de la page de choix.
        texte(170, 270, f"Please choose the game gird \n", taille=15, couleur="black") # Texte descriptif de début de partie
        # Phase de choix de la grille
        bouton_grille1 = [(200,350),(300,400)] # Création d'un bouton_grille1 pour pouvoir choisir la grille.
        rectangle(bouton_grille1[0][0], bouton_grille1[0][1], bouton_grille1[1][0], bouton_grille1[1][1], couleur='skyblue', remplissage='skyblue', epaisseur=1, tag='choix') # Permet de définir la forme du bouton
        texte(225, 360, f"Grille 1", taille=15, couleur='black') # Texte présent sur le bouton, dans ce cas 'Grille 1'.
        bouton_grille2 = [(330,350),(430,400)] # Création d'un bouton_grille2 pour pouvoir choisir la grille.
        rectangle(bouton_grille2[0][0], bouton_grille2[0][1], bouton_grille2[1][0], bouton_grille2[1][1], couleur='purple', remplissage='purple', epaisseur=1, tag='choix') # Permet de définir la forme du bouton
        texte(355, 360, f"Grille 2", taille=15, couleur='black') # Texte présent sur le bouton, dans ce cas 'Grille 2'.

        choix = True
        appuyer = attend_clic_gauche() # Permet de savoir lorsque l'utilisateur à cliquer sur quelle chose
        # Cette boucle while, permet au joueur de choisir la grille qu'il souhaite jouer
        while choix == True:
            if bouton_grille1[0][0] <= appuyer[0] and appuyer[0] <= bouton_grille1[1][0] and \
               bouton_grille1[0][1] <= appuyer[1] and appuyer[1] <= bouton_grille1[1][1]: 
                fichier = "grille1.txt" # En fonction de ou la joueur à cliquer, on a affecte à la varible 'fichier' la grille demander par le joueur
                efface_tout()
                choix = False
            if bouton_grille2[0][0] <= appuyer[0] and appuyer[0] <= bouton_grille2[1][0] and \
               bouton_grille2[0][1] <= appuyer[1] and appuyer[1] <= bouton_grille2[1][1]:
                fichier = "grille2.txt" # En fonction, de ou la joueur à cliquer, on a affecte à la varible 'fichier' la grille demander par le joueur
                efface_tout()
                choix = False
        ferme_fenetre()
        
        # Initialisation du jeu
        indices = grille_jeu(fichier) # Permet de récupèrer la liste indices crée par la fonction grille_jeu(fichier)
        etat = {} # Initialisation du dictionnaire état qui s'occupera de classer les segments et leurs états
        sommets = sommets_grille(indices) # Permet de récupèrer la liste sommets crée par la foncion sommets_grille(indices)
        segments = liste_segments(sommets, indices) # Permet de récupèrer la liste de sommets crée par la fonction liste_segments(sommets, indices)
        cases = liste_cases(indices) # Permet de récupèrer la liste cases crée par la fonction liste_cases(indices)
        taille_grille_largeur = round((len(indices[0])) * 3.83333333) 
        taille_grille_hauteur = round((len(indices)) * 3.83333333)
        cree_fenetre(taille_fenetre * taille_grille_largeur, taille_fenetre * taille_grille_hauteur) # créeation de la fenetre dédiée au jeu SlitherLink
        taille_grille = affichage_grille(indices) # Permet de récupèrer la taille de la grille et en même temps afficher la grille et les indices
        tracage_segments = list() # Initialisation de la liste tracage_segments nécessaire pour l'affichage des segments et leur effacement

        # Boucle principale
        while Jouer == True:
            ev = attend_ev() 
            tev = type_ev(ev)
            # Action dépendant du type d'évenement reçu
            
            if tev == 'Quitte': #on sort de la boucle
                break
            
            if tev == "ClicDroit": # Si l'évenement est un clic_droit alors on rentre dans cette condition
                x, y = abscisse(ev), ordonnee(ev) # récupération des coordonnées du clic droit
                segment_interdit = clic_vers_segment(x, y, taille_marge, taille_case, taille_grille) # récupération du segment qui correspond au segment sur lequelle l'utilisateur à cliquer
                if segment_interdit != None: 
                    if (est_interdit(etat, segment_interdit) == False) and (est_vierge(etat, segment_interdit) == True):
                        etat = interdire_segment(etat, segment_interdit) # On donne la valeur de -1 au segment en question
                    else:
                        etat = effacer_segment(etat, segment_interdit) # On supprime le segment en question si il étati déjà dans le dictionnaire état
                    
            elif tev == "ClicGauche": # Si l'évènement est un clic_droit alors on rentre dans cette condition
                x, y = abscisse(ev), ordonnee(ev) # récupération des coordonnées du clic gauche
                segment_trace = clic_vers_segment(x, y, taille_marge, taille_case, taille_grille) # récupération du segment qui correspond au segment su lequelle l'utilisateur à cliquer
                if segment_trace != None:
                    if (est_trace(etat, segment_trace) == False) and (est_vierge(etat, segment_trace) == True):
                        etat = tracer_segment(etat, segment_trace) # On donne la valeur de 1 au segment en question
                    else:
                        etat = effacer_segment(etat, segment_trace) # on supprime le segment en question si il était déjà dans le dicitonnaire état
                    
            else: # Dans les autres cas, on ne fait rien 
                pass

            liste_segments_traces = segments_traces(etat) # on récupère la totalité des segments tracées
            nb_segments_traces = 0
            for segment in liste_segments_traces:
                nb_segments_traces +=1
            liste_segments_interdits = segments_interdits(etat) # on récupère la totalité des segments interdits
            effacement_segments(tracage_segments) # on efface les segments du tours précédant
            tracage_segments = affichage_etat_segments(liste_segments_traces, liste_segments_interdits) # puis on réaffiche les nouveaux segments
            
            # conditions de victoire
            if condition_fin1(indices, etat, cases) == True:
                print("Tous les indices de la grille sont satisfaits")
                for segment in liste_segments_traces:
                    taille_boucle = longueur_boucle(etat, segment)
                    if taille_boucle != None:
                        if taille_boucle == nb_segments_traces:
                            Jouer = False
                            break
            else:
                print("Les indices de la grille ne sont pas tous satisfaits")
            mise_a_jour()
            
        ferme_fenetre()
        # Création de la fenêtre Tk pour la conclusion du jeu
        cree_fenetre(taille_fenetre * largeur_plateau, taille_fenetre * hauteur_plateau)
        rectangle(0, 0, 600, 600, couleur='grey', remplissage='grey') # Fond d'écran de la page d'accueil.
        #Phase de fin de jeu
        bouton_yes = [(200,350),(300,400)] # Création d'un bouton_yes pour pouvoir relancer une nouvelle partie.
        rectangle(bouton_yes[0][0], bouton_yes[0][1], bouton_yes[1][0], bouton_yes[1][1], couleur='green', remplissage='green', epaisseur=1, tag='YES') # Permet de définir la forme du bouton
        texte(225, 360, f"YES", taille=15, couleur = 'white') # Texte présent sur le bouton, dans ce cas 'YES'.
        bouton_no = [(330,350),(410,400)] # Création d'un bouton_no pour pouvoir quitter definitivement le jeu.
        rectangle(bouton_no[0][0], bouton_no[0][1], bouton_no[1][0], bouton_no[1][1], couleur='red', remplissage='red', epaisseur=1, tag='NO') # Permet de définir la forme du bouton
        texte(355, 360, f"NO", taille=15, couleur = 'white') # Texte présent sur le bouton, dans ce cas 'NO'.
        texte(170, 270, f"Yes ! You've found the solution \n    Congratulations to you !\nDo you want to play again ?", taille=15, couleur="black") # Texte descriptif de fin de partie

        appuyer = attend_clic_gauche()
        while appuyer:
            if bouton_yes[0][0] <= appuyer[0] and appuyer[0] <= bouton_yes[1][0] and \
               bouton_yes[0][1] <= appuyer[1] and appuyer[1] <= bouton_yes[1][1]:
                # on teste si l'utilisateur à appuyer sur le bouton_yes si c'est le cas, alors l'utilisateur revient sur la page d'acceuil et peut recommencer à jouer.
                efface_tout()
                ACCUEIL = True
                break
            elif bouton_no[0][0] <= appuyer[0] and appuyer[0] <= bouton_no[1][0] and \
                 bouton_no[0][1] <= appuyer[1] and appuyer[1] <= bouton_no[1][1]:
                # on teste si l'utilisateur à appuyer sur le bouton_no si c'est le cas, alors l'utilisateur quitte définitivement le jeu, et le programme s'arrête.
                efface_tout()
                ACCUEIL = False
                break
        mise_a_jour()
        # Fermeture de la fenetre
        ferme_fenetre()

        for sommet in sommets:
            solution = solveur(etat, sommet, indices, cases)
            if solution == True:
                print("Il existait donc bien une solution à la grille")
        meilleure_chemin = chemin_optimal(indices, cases, 3)
        print("Le meilleur chemin était", meilleure_chemin)
    # Sortie du programme
    sys.exit()
