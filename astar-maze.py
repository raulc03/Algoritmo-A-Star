import numpy as np

class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self,other):
        return self.position == other.position

#Devuelve el camino solución
def return_path(current_node, maze):
    path = []
    no_rows, no_colums = np.shape(maze)
    
    result = [[-1 for i in range(no_colums)] for j in range(no_rows)]
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent

    path = path[::-1]
    start_value = 0
    
    for i in range(len(path)):
        result[path[i][0]][path[i][1]] = start_value
        start_value += 1

    return result

def search(maze, start, end):
    #inicializamos los nodos "start" "end"

    start_node = Node(None, tuple(start))
    start_node.g = start_node.h = start_node.f = 0

    end_node = Node(None, tuple(end))
    end_node.g=end_node.h = end_node.f = 0

    #open list
    yet_to_visit_list = []

    #close list
    visited_list = []

    yet_to_visit_list.append(start_node)

    outer_iterations = 0
    #maxima operaciones que se pueden dar por si se encuentra un loop
    max_iterations = (len(maze)//2) ** 10

    move = [[-1, 0, 10], #izquierda
            [0, -1, 10], #arriba
            [1,  0, 10], #derecha
            [0,  1, 10], #abajo
            [-1, -1,14], #izquirda arriba
            [-1, 1, 14], #izquierda abajo
            [1,  1, 14], #derecha abajo
            [1, -1, 14]] #derecha arriba

    no_rows, no_columns = np.shape(maze)

    #mietras la openList no esté vacía
    while len(yet_to_visit_list) > 0:
        outer_iterations +=1

        current_node = yet_to_visit_list[0]
        current_index = 0

        #Se escoge el nodo con menor F
        for index, item in enumerate(yet_to_visit_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

                
        if outer_iterations > max_iterations:
            print("Se ha dado muchas interacciones")
            return return_path(current_node,maze)

        #Quitamos de la OpenList al nodo con menor F
        yet_to_visit_list.pop(current_index)
        #Añadimos a la LIsta de Cerrados al nodo con menor F
        visited_list.append(current_node)

        if current_node == end_node:
            return return_path(current_node, maze)


        children = []
        
        #Encuentro cada vecino y lo añado a la Lista Children
        for new_position in move:
            node_position = (current_node.position[0] + new_position[0], 
                             current_node.position[1]+new_position[1])
            
            if(node_position[0] > (no_rows -1) or 
               node_position[0] < 0 or 
               node_position[1] > (no_columns -1 ) or 
               node_position[1] < 0):
                continue
            
            #Si el vecino es inválido no se lo toma
            if maze[node_position[0]][node_position[1]] != 0:
                continue
            
            new_node = Node(current_node, node_position)
            new_node.g = current_node.g + new_position[2]

            children.append(new_node)

        #Por cada vecino se evalua la mejor opción para moverse
        for child in children:
            if len([visited_child for visited_child in visited_list if visited_child == child]) > 0:
                continue

            child.h = (((child.position[0]- end_node.position[0])**2)+
                       ((child.position[1] - end_node.position[1])**2))
            
            child.f = child.g + child.h

            if len([i for i in yet_to_visit_list if child == i and child.g > i.g]) > 0:
                continue

            yet_to_visit_list.append(child)

if __name__ == '__main__':

    #maze = [[0,0,0,0],
    #        [0,1,0,0],
    #        [0,1,0,0],
    #        [0,0,0,1]]

    maze = [[0, 0, 0, 0, 1 ,0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]]

    start= [2,1]
    end = [2,6]
    cost = 1

    path = search(maze, start, end)

    print('\n'.join([''.join(["{:" ">3d}".format(item) for item in row])
                     for row in path]))