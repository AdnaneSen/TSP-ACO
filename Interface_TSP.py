
# Crée une fenetre, un canevas, place le noeud de départ
# Puis onclique pour placer les autres noeuds.
# Possibilité d'effacer les noeuds en allanat en arrière.
# Deux listes contiennent les noeuds et leurs coordonnées


from tkinter import *
from tkinter.messagebox import showinfo
import random
import numpy as np
from TSP_Ant_colony import Node, Graph
from TSP_Ant_colony import ACO
import matplotlib.pyplot as plt

# --------------------------------------------------------


class ZoneAffichage(Canvas):
    def __init__(self, parent, w=500, h=400, _bg='white'):  # 500x400 : dessin final !
        self.__w = w
        self.__h = h
        self.__liste_noeuds = []

        # Pour avoir un contour pour le Canevas
        self.__fen_parent=parent
        Canvas.__init__(self, parent, width=w, height=h, bg=_bg, relief=RAISED, bd=5)


    def get_dims(self):
        return (self.__w, self.__h)

    def not_used_keep_dessiner_graphe(self):
        for b in self.__liste_noeuds:
            b.deplacement()
        self.after(50, self.dessiner_graphe)  # Important, sinon on fera une seul execution

    def creer_noeud(self, x_centre, y_centre, rayon , col, fill_color="white"):
        noeud=Balle(self, x_centre, y_centre, rayon , col)
        self.pack()
        return noeud
    
    def creer_arete(self, ax,ay,bx,by,color):
        arete = Edge(self, ax, ay, bx, by,color)
        self.pack()
        return arete

    def action_pour_un_clique(self, event):
        print("Trace : (x,y) = ", event.x, event.y)
        #showinfo('Résultat ', "Arrrgh : vous avez dans la fenetre" + '\nThanks !')
        
        # Placer un noeud à l'endroit cliqué
        self.__fen_parent.placer_un_noeud(event.x, event.y)


    def not_used_set_coordonnes_du_last_node(self, x_centre, y_centre):
        self.__last_node=(x_centre, y_centre)

    def placer_un_noeud_sur_canevas(self, x_centre, y_centre, col=None, fill_color="white"):
        w,h = self.get_dims()
        rayon=5
        if col == None :
            col= random.choice(['green', 'blue', 'red', 'magenta', 'black', 'maroon', 'purple', 'navy', 'dark cyan'])

        node=self.creer_noeud(x_centre, y_centre, rayon , col, fill_color)
        self.update()

        self.__fen_parent.set_coordonnes_du_last_node(x_centre, y_centre)
        return node.get_node_ident()
    
    def placer_une_arete_sur_canevas(self, ax,ay,bx,by,color):
        w,h=self.get_dims()
        # col=['green', 'blue', 'red', 'magenta', 'black', 'maroon', 'purple', 'navy', 'dark cyan']
        # color = np.random.choice(col)
        edge = self.creer_arete(ax,ay,bx,by,color)
        self.update()
        return edge.get_line_ident()


class FenPrincipale(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('ESSAI GRAPHE')
        self.__zoneAffichage = ZoneAffichage(self)

        self.__zoneAffichage.pack()
        
        self.__contour = Frame(self)
        self.__contour.pack(side =TOP)
        
        self.__contour2 = Frame(self)
        self.__contour2.pack(side = BOTTOM)
        
        self.__alpha_lab= Label(self.__contour,text="alpha").pack(side = LEFT, padx=5,pady=5)
        self.__alpha= Entry(self.__contour, width = 5)
        self.__alpha.insert(0,'1')
        self.__alpha.pack(side= LEFT,padx=5,pady=5)
        
        self.__beta_lab= Label(self.__contour,text="beta").pack(side = LEFT, padx=5,pady=5)
        self.__beta= Entry(self.__contour, width = 5)
        self.__beta.insert(0,'1')
        self.__beta.pack(side= LEFT,padx=5,pady=5)
        
        self.__rho_lab= Label(self.__contour,text="rho").pack(side = LEFT, padx=5,pady=5)
        self.__rho= Entry(self.__contour, width = 5)
        self.__rho.insert(0,'0.1')
        self.__rho.pack(side= LEFT,padx=5,pady=5)
        
        self.__n_ants_lab= Label(self.__contour,text="Nombre de fourmis").pack(side = LEFT, padx=5,pady=5)
        self.__n_ants= Entry(self.__contour, width = 5)
        self.__n_ants.insert(0,'10')
        self.__n_ants.pack(side= LEFT,padx=5,pady=5)
        
        self.__n_iterations_lab= Label(self.__contour,text="Nombre d'itérations").pack(side = LEFT, padx=5,pady=5)
        self.__n_iterations= Entry(self.__contour, width = 5)
        self.__n_iterations.insert(0,'50')
        self.__n_iterations.pack(side= LEFT,padx=5,pady=5)
        
        self.__textoutput = Text(self, height =1)
        self.__textoutput.pack(side= LEFT, fill = Y)

        # ----------------------------

        # Création d'un widget Button (bouton Effacer)
        self.__boutonEffacer = Button(self.__contour2, text='Effacer le dernier noeud', command=self.undo_last_noeud).pack(side=LEFT, padx=5, pady=5)

        # Création d'un boutton pour effecer les aretes
        self.__boutonEffacerArete = Button(self.__contour2, text = 'Effacer les lignes', command = self.delete_edges).pack(side = LEFT, padx=5, pady=5)

        # Création d'un widget Button (bouton Effacer) 
        self.__boutonEffacer = Button(self.__contour2, text='Effacer', command=self.effacer).pack(side=LEFT, padx=5, pady=5)

       # Création d'un bouton de résolution
        self.boutonRedoudre = Button(self.__contour2, text ='Résoudre', command =self.resolution).pack(side =LEFT, padx=5, pady=5)
       
        # Création d'un widget Button (bouton Quitter)
        self.__boutonQuitter = Button(self.__contour2, text='Quitter', command=self.destroy).pack(side=RIGHT, padx=5, pady=5)

        self.__zoneAffichage.bind('<Button-1>', self.__zoneAffichage.action_pour_un_clique)

        self.__liste_d_ident_d_objets_crees=[]
        self.__liste_coordonnes_centre_des_nodes=[]
        self.__color=['green', 'blue', 'red', 'magenta', 'black', 'maroon', 'purple', 'navy', 'dark cyan']

        #self.placer_noeud_depart() ----------------------------------------#Décommente si noeud de départ nécessaire

    def add_a_node_to_your_list(self, noeud) :
        self.__liste_d_ident_d_objets_crees.append(noeud)
        
    def placer_un_noeud(self, x, y):
        node=self.__zoneAffichage.placer_un_noeud_sur_canevas(x,y)
        self.add_a_node_to_your_list(node)
        self.set_coordonnes_du_last_node(x,y)
        self.__liste_coordonnes_centre_des_nodes.append((x,y))
        
    def placer_une_arete(self,ax,ay,bx,by):
        arete = self.zoneAffichage.placer_une_arete_sur_canvevas(ax,ay,bx,by)


    def set_coordonnes_du_last_node(self, x_centre, y_centre):
        self.__last_node=(x_centre, y_centre)

    def get_last_node(self):
        return self.__last_node

    def placer_noeud_depart(self):
        w,h = self.__zoneAffichage.get_dims()
        x_centre, y_centre=20, h//2
        node= self.__zoneAffichage.placer_un_noeud_sur_canevas(x_centre, y_centre, col="red", fill_color="red")
        self.add_a_node_to_your_list(node)
        self.__liste_coordonnes_centre_des_nodes.append((x_centre, y_centre))

    #--------------------------
    def delete_edges(self):
        node_list = self.__liste_coordonnes_centre_des_nodes.copy()
        self.effacer()
        for item in node_list:
            node= self.__zoneAffichage.placer_un_noeud_sur_canevas(item[0], item[1])
            self.add_a_node_to_your_list(node)
            self.__liste_coordonnes_centre_des_nodes.append((item[0], item[1]))

    def undo_last_noeud(self):
        print("Avant undo, liste contient {} elements".format(len(self.__liste_d_ident_d_objets_crees)))
        if len(self.__liste_d_ident_d_objets_crees)==1 :
            print("Peut pas enlever noeud départ")
            return

        x_centre,  y_centre=self.get_last_node()

        last_node=self.__liste_d_ident_d_objets_crees.pop()

        # Pour supprimer, il faut can_id du noeud, pas le noeud lui mm !!
        self.__zoneAffichage.delete(last_node)
        self.__zoneAffichage.update()

        x_last_node,y_last_node=self.__liste_coordonnes_centre_des_nodes.pop()
        self.set_coordonnes_du_last_node(x_last_node,y_last_node)
        print("Après undo, liste contient {} elements".format(len(self.__liste_d_ident_d_objets_crees)))

        

    def ajout_noeud(self):
        # Dessin d'un petit cercle
        x_centre,  y_centre = self.not_used_generer_un_point_XY_dans_une_bande()
        print("(x,y) =", x_centre, ' , ', y_centre)

        rayon=5
        col= random.choice(['green', 'blue', 'red', 'magenta', 'black', 'maroon', 'purple', 'navy', 'dark cyan'])
        self.__zoneAffichage.creer_noeud(x_centre, y_centre, rayon , col)
        self.__zoneAffichage.update()
        self.__last_node=(x_centre, y_centre)


    def effacer(self):
        """ Efface la zone graphique """
        self.__zoneAffichage.delete(ALL)
        self.__liste_d_ident_d_objets_crees.clear()
        self.__liste_coordonnes_centre_des_nodes.clear()
        #self.placer_noeud_depart() --------------------------------- #Décommente si noeud de départ nécessaire
        
    def resolution(self):
        
        #contient l'emnsemble des coordonnées des noeuds sous formes de tuples (x,y)
        list_coord= self.__liste_coordonnes_centre_des_nodes
        
        #Lecture des Noeuds
        nodes = [Node(list_coord[i][0],list_coord[i][1]) for i in range(len(list_coord))]
        
        #Lecture du graph
        graph=Graph(nodes)
        
        #Application de l'algorithme TSP_Ant colony
        aco=ACO(graph)
        
        #Calcul du meilleur trajet
        alpha = float(self.__alpha.get())
        beta = float(self.__beta.get())
        n_iterations_bis = int(self.__n_iterations.get())
        n_ants_bis = int(self.__n_ants.get())
        rho = float(self.__rho.get())
        best_path = aco.solve(alpha= alpha, beta=beta, rho=rho, n_ants=n_ants_bis, n_iterations=n_iterations_bis, verbose=False)
        
        #Affichage de la distance parcourue
        print ('La distance optimale est :', best_path[1])
        
        #Lecture de la solution : liste de la suite des noeuds constituant la solution
        node_xy = [(best_path[0][i].x, best_path[0][i].y) for i in range(len(best_path[0]))]
        l=len(node_xy)
        
        #Procéder au tracé des aretes du graphe
        L=[0]*l
        color = np.random.choice(self.__color)
        self.__color.remove(color)
        for i in range(l-1):
            L[i]=self.__zoneAffichage.placer_une_arete_sur_canevas(node_xy[i][0], node_xy[i][1],node_xy[i+1][0], node_xy[i+1][1],color)
        
        #Boucler la trajectoire
        L[l-1]=self.__zoneAffichage.placer_une_arete_sur_canevas(node_xy[l-1][0], node_xy[l-1][1],node_xy[0][0], node_xy[0][1],color)
        
        #insérer la distance minimale obtenue
        self.__textoutput.insert(INSERT,'La distance optimale est :'+ str(best_path[1]))
#--------------------------
class Balle:
    def __init__(self, canvas, cx, cy, rayon, couleur, fill_color="white"):
        self.__cx, self.__cy = cx, cy
        self.__rayon = rayon
        self.__color = couleur
        self.__can = canvas  # Il le faut pour les déplacements

        self.__canid = self.__can.create_oval(cx - rayon, cy - rayon, cx + rayon, cy + rayon, outline=couleur, fill=fill_color)
        # Pour 3.6 : col: object  # essaie typage !

    def get_node_ident(self):
        return self.__canid

    def NoNeed_Here_not_used_generer_un_point_XY_dans_une_bande(self, last_x, last_y):
        w,h = self.__can.get_dims()
        #last_x, last_y=self.__last_node
        delta_x_centre = random.randint(10, 50); delta_y_centre = random.randint(10, 50)
        hasard_x=random.randint(0, 1); hasard_y=random.randint(0, 1)

        x_centre = last_x+random.randint(10, 50)* 1 if hasard_x else -1
        y_centre = last_y+random.randint(10, 50)* 1 if hasard_y else -1
        if x_centre < 0 :  x_centre*=-1
        if y_centre < 0 :  y_centre*=-1
        return (x_centre, y_centre)

    # Un seul déplacement
    def not_used_keep_deplacement(self):
        self.__can.move(self.__canid, 0, 0)

class Edge:
    def __init__(self, canvas, ax, ay, bx, by, color):
        self.__ax, self.__ay, self.__bx, self.__by=ax,ay,bx, by
        self.__can= canvas
        self.__color= color
        self.__canid = self.__can.create_line(ax,ay,bx,by, fill=color)
    def get_line_ident(self):
        return self.__canid

# ------------------------------------------------------
# Réutilisation des formes

# --------------------------------------------------------
if __name__ == "__main__":
    fen = FenPrincipale()
    fen.mainloop()
