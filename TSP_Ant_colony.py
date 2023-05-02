# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 15:22:10 2023

@author: Adnane Sennoune
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class Node:
    indice = -1                          #indice est utilisée pour donner un index unique 
                                         #à chaque instance de la classe Noeud.    
    def __new__(cls, *args, **kwargs):   #Création d'un nouveau noeud
    
        cls.indice += 1
        return super().__new__(cls)

    def __init__(self, x, y, name=None):
        self.x = x
        self.y = y
        self.name = name
        self.index = Node.indice

    def __eq__(self, other):
        return self.index == other.index  #deux instances de la classe Node sont 
                                          #égales ssi elles ont le même index
    def show_node(self):
        return 'node({},{})'.format(self.x,self.y)
    

def euclidean_distance(node1, node2):
    return np.sqrt(((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2))

class Edge:
    def __init__(self, node1, node2, distance_function=euclidean_distance):
        self.node1 = node1
        self.node2 = node2
        self.distance = distance_function(node1, node2)
        self.pheromone = 1

    def edge_value(self, alpha, beta, d_avg):   #Numérateur de la formule de probabilité
        return (self.pheromone ** alpha) * (d_avg/ self.distance) ** beta   


class Graph:
    def __init__(self, nodes, distance_function=euclidean_distance, seed=None):
        self.nodes = {node.index: node for node in nodes}
        self.edges = {}
        self.rng = np.random.default_rng(seed=seed)

        nodes_index = sorted(self.nodes)
        #Remplissage du dictionnaire edge par l'ensemble des aretes
        for i, index_node1 in enumerate(nodes_index):
            for index_node2 in nodes_index[i + 1:]:
                self.edges[(index_node1, index_node2)] = Edge(self.nodes[index_node1], self.nodes[index_node2], distance_function)
    
    def edge_from_node(self, node1, node2):
        return self.edges[min(node1.index, node2.index), max(node1.index, node2.index)]

    def select_node(self, current_node, nodes, alpha, beta, d_avg):
        if len(nodes) == 1:
            return nodes[0]

        probabilities = np.array([self.edge_from_node(current_node, node).edge_value(alpha, beta, d_avg) for node in nodes])
        probabilities = probabilities / np.sum(probabilities)
        next_node = self.rng.choice(nodes, p=probabilities)
        return next_node
    
    def evaporate_pheromone(self, rho):          #Mise à jour/vaporisation du pheromone dans les aretes
        for edge in self.edges.values():
            edge.pheromone = (1 - rho) * edge.pheromone

    def edges_pheromone(self):                   #Récupération des quantités du phéromone contenues dans les aretes
        pheromones = dict()
        for k, edge in self.edges.items():
            pheromones[k] = edge.pheromone
        return pheromones
    
    
class Ant:
    def __init__(self, graph, d_avg=1.):
        self.position = None                #Position actuelle de la fourmi
        self.nodes_to_visit = []            
        self.graph = graph
        self.distance = 0                   #Distance traversé par la fourmi
        self.edges_visited = []
        self.path = []                      #Liste du chemin de la fourmi
        self.d_avg = d_avg


    def initialization(self, start):        #Initialisation de la position d'une fourmi dans un graphe
        self.position = start
        self.nodes_to_visit = [node for node in self.graph.nodes.values() if node != self.position]
        self.distance = 0
        self.edges_visited = []
        self.path = [start]

    def do_step(self, alpha, beta):         #faire une itération de parcours de tous les noeuds
        while self.nodes_to_visit:
            next_node = self.graph.select_node(self.position, self.nodes_to_visit, alpha, beta, self.d_avg)
            self.nodes_to_visit.remove(next_node)
            self.path.append(next_node)
            next_edge = self.graph.edge_from_node(self.position, next_node)
            self.edges_visited.append(next_edge)
            self.distance += next_edge.distance
            self.position = next_node
            
    def update_pheromone(self, p):    #Mise à jour de la quantité de phéromone pour les aretes visitées
        for edge in self.edges_visited:
            edge.pheromone += p / self.distance
            
            
class ACO:
    
    def __init__(self, graph, seed=None):
        self.graph = graph
        self.ants = []
        self.rng = np.random.default_rng(seed=seed)

    #la fonction d'implementation de l'algorithme ACO
    def solve(self, alpha=1, beta=1, rho=0.1, n_ants=10, n_iterations=50, verbose = None):
        #distance moyenne des aretes
        d_avg = np.sum(np.fromiter((edge.distance for edge in self.graph.edges.values()), dtype=float)) / (len(self.graph.edges))

        #min_distance initialisée à la distance maximale qui peut etre traversée par une fourmi
        min_distance = d_avg * len(self.graph.nodes)
        
        self.ants = []
        best_path = None                             #Le meilleur chemin
        NODES = list(self.graph.nodes.values())      #liste des noeuds
        for i in range(n_ants):
            self.ants.append(Ant(self.graph, d_avg))
        
        
        for iteration in range(n_iterations):
            #Affichage du progrès de l'algorithme pour chaque 10 itérations
            if iteration % 10 == 0:
                print('Iteration {}/{} :'.format(iteration, n_iterations), min_distance)
            
            #Initialiser la position des fourmis pour un noeud aléatoire et effectuer une itération
            for ant in self.ants:
                ant.initialization(NODES[self.rng.integers(len(NODES))])
                ant.do_step(alpha, beta)
            
            #Evaporation de phéromone dans toutes les aretes
            self.graph.evaporate_pheromone(rho)
            
            #Mise à jour du niveau de phéromone localement et choix du meilleur trajet 
            for ant in self.ants:
                ant.update_pheromone(min_distance / len(self.ants))
                if ant.distance < min_distance:
                    min_distance = ant.distance
                    best_path = ant.path

        # si on veut visualiser le trajet sous forme de liste
        best_path_xy=[]
        for node in best_path:
            best_path_xy.append(node.show_node())
        best_path_xy.append(best_path_xy[0])
        
        return best_path, min_distance,best_path_xy
    
if __name__ == '__main__':
    #Définition des noeuds du graphe
    #C'est juste un exemple
    #Création du graphe
    nodes = [Node(220, 350, 'Bordeaux'), Node(330, 600, 'Tours'), Node(120, 600, 'Nantes'), Node(400, 150, 'Toulouse'), Node(600, 460, 'Clermont'), Node(840, 450, 'Lyon'), Node(820, 130,'Marseille'), Node(550, 750,'Paris'), Node(620, 950,'Lille'),Node(1050, 700,'Strasbourg') ]
    france_img = mpimg.imread('france.jpg')
    
    
    
    x = [node.x for node in nodes]
    y = [node.y for node in nodes]
    labels = [node.name for node in nodes]

    fig, ax = plt.subplots()
    ax.scatter(x, y)
    ax.imshow(france_img, extent=[-100, 1100, -100, 1000])

    for i, label in enumerate(labels):
        ax.annotate(label, (x[i], y[i]))

    
    
    graph = Graph(nodes)
    #Création de l'algorithme ACO
    aco = ACO(graph)
    #Résolution du problème du voyageur de commerce
    best_path, min_distance,best_path_xy=aco.solve(alpha=1, beta=2, rho=0.1, n_ants=10, n_iterations=50, verbose=None)
    
    best_path_x = [node.x for node in best_path]
    best_path_y = [node.y for node in best_path]

# ajouter les coordonnées du premier nœud pour boucler le chemin
    best_path_x.append(best_path[0].x)
    best_path_y.append(best_path[0].y)

# tracer le chemin optimal en reliant les nœuds dans l'ordre de best_path
    ax.plot(best_path_x, best_path_y, c='r', linewidth=2)
    
    ax.set_xlim([-100, 1100])
    ax.set_ylim([-100, 1000])

    ax.grid()
    
    plt.figure()
    plt.show()  
    
    print(f"la distance optimale est {min_distance}")
    print(best_path_xy)
    
    # N=list(range(1,20))
    # D=[]
    # for n in N:
    #     best_path, min_distance,best_path_xy=aco.solve(alpha=1, beta=2, rho=0.1, n_ants=n, n_iterations=20, verbose=None)
    #     D.append(min_distance)
    # plt.plot(N,D)
    # plt.figure()
    # plt.show()
    
    # R=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
    # D=[]
    # for r in R:
    #     best_path, min_distance,best_path_xy=aco.solve(alpha=1, beta=2, rho=r, n_ants=10, n_iterations=20, verbose=None)
    #     D.append(min_distance)
    # plt.plot(R,D)
    # plt.figure()
    # plt.show()