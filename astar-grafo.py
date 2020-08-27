class Graph:
    
    def __init__(self, graph_dict=None, directed=True):
        self.graph_dict = graph_dict or {}
        self.directed = directed
        if not directed:
            self.make_undirected()


    def make_undirected(self):
        for a in list(self.graph_dict.keys()):
            for (b, dist) in self.graph_dict[a].items():
                self.graph_dict.setdefault(b, {})[a] = dist

                
    def connect(self, A, B, distance=1):
        self.graph_dict.setdefault(A, {})[B] = distance
        if not self.directed:
            self.graph_dict.setdefault(B, {})[A] = distance

    #Obtenemos a los vecinos
    def get(self, a, b=None):
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)


    #Retornamos una lista de nodos en el grafo
    def nodes(self):
        s1 = set([k for k in self.graph_dict.keys()])
        s2 = set([k2 for v in self.graph_dict.values() for k2, v2 in v.items()])
        nodes = s1.union(s2)
        return list(nodes)


class Node:


    def __init__(self, name:str, parent:str):
        self.name = name
        self.parent = parent
        self.g = 0 # Distancia acumulada hasta el actual nodo
        self.h = 0 # Distancia Manhatam
        self.f = 0 # Total de costo


    # Operador de == 
    def __eq__(self, other):
        return self.name == other.name

    # Ordenamos ascendentemente
    def __lt__(self, other):
         return self.f < other.f


    # Imprimimos el nodo
    def __repr__(self):
        return ('({0},{1})'.format(self.position, self.f))

# A* start
def astar_search(graph, heuristics, start, end):
    
    #Creamos la OpenList y la CloseList
    open = []
    closed = []

    start_node = Node(start, None)
    goal_node = Node(end, None)

    # Añadimos el primer nodo a la OpenList
    open.append(start_node)
    
    # Loop hasta que quede vacía la OpenList
    while len(open) > 0:

        open.sort()

        #Obtenemos el nodo con menos costo
        current_node = open.pop(0)

        #Al evaluarlo lo ponemos en la CloseList
        closed.append(current_node)
       
       #si el nodo actual es igual al nodo meta 
        if current_node == goal_node:
            path = []

            while current_node != start_node:
                path.append(current_node.name + ': (g = ' + str(current_node.g) + ', h = ' + str(current_node.h) + ', f = ' + str(current_node.f) + ')')
                current_node = current_node.parent
            path.append(start_node.name + ': (g = ' + str(start_node.g) + ', h = ' + str(start_node.h) + ', f = '+ str(start_node.f) + ')')

            return path[::-1]

        #Obtiene a los nodos hijos del nodo actual (vecinos)
        neighbors = graph.get(current_node.name)

        for key, value in neighbors.items():

            neighbor = Node(key, current_node)

            # Si el nodo está en la CloseList no se evalua
            if(neighbor in closed):
                continue

            # Aquí calculamos los g, h y f del nodo vecino
            neighbor.g = current_node.g + graph.get(current_node.name, neighbor.name)
            neighbor.h = heuristics.get(neighbor.name)
            neighbor.f = neighbor.g + neighbor.h

            #Si el f es menor al de todos los nodos que están en la lista de abierto no se le agrega a la OpenList
            if(add_to_open(open, neighbor) == True):
                open.append(neighbor)

    return None

def add_to_open(open, neighbor):
    for node in open:
        if (neighbor == node and neighbor.f > node.f):
            return False
    return True

def main():
    graph = Graph()

    graph.connect('Arad', 'Zerind', 75)
    graph.connect('Arad', 'Sibiu', 140)
    graph.connect('Arad', 'Timisoara', 118)

    graph.connect('Zerind', 'Oradea', 71)
    graph.connect('Oradea', 'Sibiu', 151)
    graph.connect('Timisoara', 'Lugoj', 111)
    
    graph.connect('Lugoj', 'Mehadia', 70)
    graph.connect('Mehadia', 'Dobreta', 75)
    graph.connect('Dobreta', 'Craiova', 120)

    graph.connect('Craiova', 'Rimnicu Vilcea', 146)
    graph.connect('Craiova', 'Pitesti', 146)

    graph.connect('Rimnicu Vilcea','Sibiu', 80)
    graph.connect('Rimnicu Vilcea','Pitesti', 97)

    graph.connect('Pitesti','Bucharest', 101)
    graph.connect('Fagaras','Sibiu', 99)

    graph.connect('Bucharest','Fagaras', 211)
    graph.connect('Bucharest','Giurgi', 90)
    graph.connect('Bucharest','Urziceni', 85)

    graph.connect('Urziceni','Vaslui', 142)
    graph.connect('Urziceni','Hirsova', 98)

    graph.connect('Hirsova','Eforie', 86)
    graph.connect('Vaslui','Iasi', 92)
    graph.connect('Iasi','Neamt', 87)
    

    graph.make_undirected()
    heuristics = {}
    heuristics['Arad'] = 366
    heuristics['Bucharest'] = 0
    heuristics['Craiova'] = 160
    heuristics['Dobreta'] = 242
    heuristics['Eforie'] = 161
    heuristics['Fagaras'] = 178
    heuristics['Giurgiu'] = 77
    heuristics['Hirsova'] = 151
    heuristics['Iasi'] = 226
    heuristics['Lugoj'] = 244
    heuristics['Mehadia'] = 241
    heuristics['Neamt'] = 234
    heuristics['Oradea'] = 380
    heuristics['Pitesti'] = 98
    heuristics['Rimnicu Vilcea'] = 193
    heuristics['Sibiu'] = 253
    heuristics['Timisoara'] = 329
    heuristics['Urziceni'] = 80
    heuristics['Vaslui'] = 199
    heuristics['Zerind'] = 374

    path = astar_search(graph, heuristics, 'Timisoara', 'Bucharest')

    print(path)
    print()


if __name__ == "__main__": main()
