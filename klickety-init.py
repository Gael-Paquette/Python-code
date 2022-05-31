# Imports ---------------------------------------------------------------------
from tkinter import Tk, Frame, LEFT, RIGHT, Button, BOTH, Canvas, TOP, \
                    BOTTOM, ALL
import tkinter.font
import random

COULEURS = ["red", "blue", "green", "yellow", "magenta"]


def initialiser_plateau(hauteur, largeur):
    """Renvoie un plateau hauteur x largeur aléatoire de blocs de couleurs."""
    lst = []
    for x in range(hauteur):
        lst2 = []
        for y in range(largeur):
            couleurs_blocs = random.choice(COULEURS)
            lst2.append(couleurs_blocs)
        lst.append(lst2)
    return lst


def detecter_piece(plateau, ligne, colonne, piece):
    """Remplit l'ensemble piece, initialement vide, à l'aide des coordonnées
    des entrées de plateau appartenant à la même pièce que 
    plateau[ligne][colonne]."""
    c_blocs = plateau[ligne][colonne]
    piece.add((ligne, colonne))
    if (ligne < (len(plateau) - 1)) and (c_blocs == plateau[ligne + 1][colonne]) and ((ligne+1, colonne) not in piece):
        detecter_piece(plateau, ligne + 1, colonne, piece)
    if (colonne >= 1) and (c_blocs == plateau[ligne][colonne -1]) and ((ligne, colonne - 1) not in piece):
        detecter_piece(plateau, ligne, colonne - 1, piece)
    if (ligne >= 1) and (c_blocs == plateau[ligne - 1][colonne]) and ((ligne - 1, colonne) not in piece):
        detecter_piece(plateau, ligne - 1, colonne, piece)
    if (colonne < (len(plateau[0]) - 1)) and (c_blocs == plateau[ligne][colonne + 1]) and ((ligne, colonne + 1) not in piece):
        detecter_piece(plateau, ligne, colonne + 1, piece)
    return piece


def mettre_a_jour(plateau, piece):
    """Modifie plateau de manière à ce que les trous liés à la suppression de la
    pièce donnée fassent chuter les autres blocs. Les coordonnées renseignées
    par piece correspondent à des cases déjà à None dans plateau."""
    if type(piece) is not list: # On souhaite utiliser les indices de piece. Pour cela on change leur structure de donnée en liste.
        piece = (list(piece))
    mouvement = False
    for x in range(1, len(plateau) + 1):
        for y in range(len(plateau[0])):
            if (x,y) in piece and plateau[x - 1][y] != None:
                plateau[x - 1][y], plateau[x][y] = plateau[x][y], plateau[x - 1][y]
                piece.remove((x, y))
                piece.append((x - 1, y))
                mouvement = True
    if mouvement == True: mettre_a_jour(plateau, piece)
    return True

def eliminer_colonnes_vides(plateau):
    """Effectue les décalages nécessaires à la suppression des colonnes
    vides."""
    mouvement = True
    cpt = 1 # On utilise un compteur pour contrôler le déplacement des colonnes. En effet, lorsque on fait un déplacement de colonne, on commente la valeur du compteur. 
    while mouvement == True:
        mouvement = False
        for colonne in range(len(plateau[0]) - cpt): #Pour eviter de parcourir des colonnes non désirer on soustraire à len(plateau[0]) la valeur du cpt.
            if est_colonne_vide(plateau, colonne) == True:
                for ligne in range(len(plateau)):
                    plateau[ligne][colonne], plateau[ligne][colonne+1] = plateau[ligne][colonne+1], plateau[ligne][colonne]
                mouvement = True
                cpt += 1
    return True

def est_colonne_vide(plateau, colonne):
    """Fonction qui vérifie qu'une colonne est vide et renvoie True dans ce cas."""
    resultat = True
    for ligne in range(len(plateau)):
        if plateau[ligne][colonne] != None: resultat = False
    return resultat

def partie_finie(plateau):
    """Renvoie True si la partie est finie, c'est-à-dire si le plateau est vide
    ou si les seules pièces restantes sont de taille 1, et False sinon"""
    presence_piece_complexe = False
    for ligne in range(len(plateau) - 1):
        for colonne in range(len(plateau[0]) - 1):
            c_blocs = plateau[ligne][colonne]
            if c_blocs != None:
                if (ligne < (len(plateau))) and (c_blocs == plateau[ligne + 1][colonne]):
                    presence_piece_complexe = True
                if (colonne < (len(plateau[0]))) and (c_blocs == plateau[ligne][colonne + 1]):
                    presence_piece_complexe = True
                if (ligne >= 1) and (c_blocs == plateau[ligne - 1][colonne]):
                    presence_piece_complexe = True
                if (colonne >= 1) and (c_blocs == plateau[ligne][colonne -1]):
                    presence_piece_complexe = True
    return not(presence_piece_complexe)

# =============================================================================
# PARTIE A NE PAS MODIFIER ====================================================
# =============================================================================


class KlicketyGUI:
    """Interface pour le jeu Klickety."""
    def __init__(self):
        # initialisation des structures de données ----------------------------
        self.dim_plateau = (16,                 # nombre de lignes du plateau
                            10)                 # nombre de colonnes du plateau
        self.cote_case = 32          # la longueur du côté d'un bloc à dessiner
        self.hauteur_plateau = self.cote_case * self.dim_plateau[0]
        self.largeur_plateau = self.cote_case * self.dim_plateau[1]
        self.plateau = []

        # initialisation des éléments graphiques ------------------------------
        self.window = Tk()                              # la fenêtre principale
        self.window.resizable(0, 0)           # empêcher les redimensionnements
        self.partie_haut = Frame(
            self.window, width=self.largeur_plateau,
            height=self.hauteur_plateau
        )
        self.partie_haut.pack(side=TOP)
        self.partie_bas = Frame(self.window)
        self.partie_bas.pack(side=BOTTOM)

        # le canevas affichant le plateau de jeu
        self.plateau_affiche = Canvas(self.partie_haut,
                                      width=self.largeur_plateau,
                                      height=self.hauteur_plateau)
        self.plateau_affiche.pack()
        self.plateau_affiche.bind('<ButtonPress-1>', self.clic_plateau)

        # le bouton "Réinitialiser"
        self.btn = Button(self.partie_bas, text='Réinitialiser',
                          command=self.reinitialiser_jeu)
        self.btn.pack(fill=BOTH)

        # affichage du nombre de blocs restants
        self.nb_blocs = 0
        self.nb_blocs_affiche = Canvas(self.partie_bas,
                                       width=self.largeur_plateau, height=32)
        self.nb_blocs_affiche.pack(fill=BOTH)

        self.reinitialiser_jeu()

        self.window.title('Klickety')
        self.window.mainloop()

    def rafraichir_nombre_blocs(self, piece=None):
        """Rafraîchit l'affichage du nombre de blocs restants, sur base de la
        pièce que l'on vient de retirer."""
        self.nb_blocs_affiche.delete(ALL)
        if piece is None:  # appel initial, tous les blocs sont encore présents
            self.nb_blocs = self.dim_plateau[0] * self.dim_plateau[1]

        else:  # soustraire du nombre de blocs celui de la pièce retirée
            self.nb_blocs -= len(piece)

        self.nb_blocs_affiche.create_text(
            self.largeur_plateau // 2, self.cote_case // 2,
            text="Blocs restants: " + str(self.nb_blocs), fill="black"
        )

    def rafraichir_plateau(self):
        """Redessine le plateau de jeu à afficher."""
        # tracer les blocs
        self.plateau_affiche.delete(ALL)
        couleur_fond = "black"
        for i in range(self.dim_plateau[1]):                    # par défaut 10
            for j in range(self.dim_plateau[0]):                # par défaut 16
                # remarque: le canevas de tkinter interprète (i, j)
                # géométriquement (au lieu de (ligne, colonne)), d'où
                # l'inversion de coordonnées dans la ligne ci-dessous
                case = self.plateau[j][i]
                if case is not None:  # afficher le pion
                    self.plateau_affiche.create_rectangle(
                        i * self.cote_case, j * self.cote_case,
                        (i + 1) * self.cote_case, (j + 1) * self.cote_case,
                        outline=case, fill=case
                    )
                else:
                    self.plateau_affiche.create_rectangle(
                        i * self.cote_case, j * self.cote_case,
                        (i + 1) * self.cote_case, (j + 1) * self.cote_case,
                        outline=couleur_fond, fill=couleur_fond
                    )

        # tracer le contour des pièces
        # 1) tracer les séparations entre deux pièces adjacentes de
        # couleurs différentes dans la même colonne
        for i in range(0, self.dim_plateau[1]):                 # par défaut 10
            for j in range(1, self.dim_plateau[0]):             # par défaut 16
                if self.plateau[j - 1][i] != self.plateau[j][i]:
                    self.plateau_affiche.create_rectangle(
                        i * self.cote_case, j * self.cote_case,
                        (i + 1) * self.cote_case, j * self.cote_case,
                        outline=couleur_fond, fill=couleur_fond, width=1
                    )

        # 2) tracer les séparations entre deux pièces adjacentes de
        # couleurs différentes dans la même ligne
        for i in range(1, self.dim_plateau[1]):                 # par défaut 10
            for j in range(0, self.dim_plateau[0]):             # par défaut 16
                if self.plateau[j][i - 1] != self.plateau[j][i]:
                    self.plateau_affiche.create_rectangle(
                        i * self.cote_case, j * self.cote_case,
                        i * self.cote_case, (j + 1) * self.cote_case,
                        outline=couleur_fond, fill=couleur_fond, width=1
                    )

    def clic_plateau(self, event):
        """Récupère les coordonnées de la case sélectionnée, et joue le coup
        correspondant s'il est permis."""
        # remarque: le canevas de tkinter interprète (i, j) géométriquement
        # (au lieu de (ligne, colonne)), d'où l'inversion de coordonnées dans
        # la ligne ci-dessous
        (j, i) = (event.x // self.cote_case, event.y // self.cote_case)

        if self.plateau[i][j] is not None:
            piece = set()
            detecter_piece(self.plateau, i, j, piece)

            if len(piece) > 1:  # si la pièce est valide, on la retire
                # retirer la piece en mettant ses cases à None
                for (p, q) in piece:
                    self.plateau[p][q] = None

                # faire descendre les blocs situés au-dessus de la pièce
                mettre_a_jour(self.plateau, piece)

                # tasser le restant du plateau en supprimant les colonnes vides
                eliminer_colonnes_vides(self.plateau)

                # rafraîchir le plateau pour répercuter les modifications
                self.rafraichir_plateau()

                self.rafraichir_nombre_blocs(piece)
                if partie_finie(self.plateau):
                    self.plateau_affiche.create_text(
                        int(self.plateau_affiche.cget("width")) // 2,
                        self.cote_case // 2,
                        text="LA PARTIE EST TERMINÉE",
                        font=tkinter.font.Font(
                            family="Courier", size=12, weight=tkinter.font.BOLD
                        ),
                        fill="red"
                    )

    def reinitialiser_jeu(self):
        """Réinitialise le plateau de jeu et les scores."""
        self.reinitialiser_plateau()
        self.rafraichir_nombre_blocs()

    def reinitialiser_plateau(self):
        """Réinitialise le plateau de jeu."""
        # réinitialiser la matrice
        self.plateau = initialiser_plateau(*self.dim_plateau)

        # réinitialiser l'affichage
        self.plateau_affiche.delete(ALL)

        if self.plateau is not None:
            self.rafraichir_plateau()


if __name__ == "__main__":
    KlicketyGUI()
