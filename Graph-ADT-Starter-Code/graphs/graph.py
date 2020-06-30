from collections import deque
from random import choice

class Vertex(object):
    """
    Defines a single vertex and its neighbors.
    """

    def __init__(self, vertex_id):
        """
        Initialize a vertex and its neighbors dictionary.
        
        Parameters:
        vertex_id (string): A unique identifier to identify this vertex.
        """
        self.id = vertex_id
        self.neighbors_dict = {} # id -> object

    def add_neighbor(self, vertex_obj):
        """
        Add a neighbor by storing it in the neighbors dictionary.

        Parameters:
        vertex_obj (Vertex): An instance of Vertex to be stored as a neighbor.
        """
        self.__neighbors_dict[vertex_obj.__id] = vertex_obj

    def __str__(self):
        """Output the list of neighbors of this vertex."""
        neighbor_ids = list(self.neighbors_dict.keys())
        return f'{self.id} adjacent to {neighbor_ids}'

    def __repr__(self):
        """Output the list of neighbors of this vertex."""
        return self.__str__()

    def get_neighbors(self):
        """Return the neighbors of this vertex."""
        return list(self.neighbors_dict.values())

    def get_id(self):
        """Return the id of this vertex."""
        return self.id


class Graph:
    """ Graph Class
    Represents a directed or undirected graph.
    """
    def __init__(self, is_directed=True):
        """
        Initialize a graph object with an empty vertex dictionary.

        Parameters:
        is_directed (boolean): Whether the graph is directed (edges go in only one direction).
        """
        self.vertex_dict = {} # id -> object
        self.is_directed = is_directed

    def add_vertex(self, vertex_id):
        """
        Add a new vertex object to the graph with the given key and return the vertex.
        
        Parameters:
        vertex_id (string): The unique identifier for the new vertex.

        Returns:
        Vertex: The new vertex object.
        """
        self.__vertex_dict[vertex_id] = Vertex(vertex_id)
        return self.__vertex_dict[vertex_id]

    def get_vertex(self, vertex_id):
        """Return the vertex if it exists."""
        if vertex_id not in self.vertex_dict:
            return None

        vertex_obj = self.vertex_dict[vertex_id]
        return vertex_obj

    def add_edge(self, vertex_id1, vertex_id2):
        """
        Add an edge from vertex with id `vertex_id1` to vertex with id `vertex_id2`.

        Parameters:
        vertex_id1 (string): The unique identifier of the first vertex.
        vertex_id2 (string): The unique identifier of the second vertex.
        """
        v2 = self.get_vertex(vertex_id2)
        self.__vertex_dict[vertex_id1].add_neighbor(v2)
        if not self.__is_directed:
            self.__vertex_dict[vertex_id2].add_neighbor(self.__vertex_dict[vertex_id1])
        
    def get_vertices(self):
        """
        Return all vertices in the graph.
        
        Returns:
        List<Vertex>: The vertex objects contained in the graph.
        """
        return list(self.vertex_dict.values())

    def contains_id(self, vertex_id):
        return vertex_id in self.vertex_dict

    def __str__(self):
        """Return a string representation of the graph."""
        return f'Graph with vertices: {self.get_vertices()}'

    def __repr__(self):
        """Return a string representation of the graph."""
        return self.__str__()

    def bfs_traversal(self, start_id):
        """
        Traverse the graph using breadth-first search.
        """
        if not self.contains_id(start_id):
            raise KeyError("One or both vertices are not in the graph!")

        # Keep a set to denote which vertices we've seen before
        seen = set()
        seen.add(start_id)

        # Keep a queue so that we visit vertices in the appropriate order
        queue = deque()
        queue.append(self.get_vertex(start_id))

        while queue:
            current_vertex_obj = queue.popleft()
            current_vertex_id = current_vertex_obj.get_id()

            # Process current node
            print('Processing vertex {}'.format(current_vertex_id))

            # Add its neighbors to the queue
            for neighbor in current_vertex_obj.get_neighbors():
                if neighbor.get_id() not in seen:
                    seen.add(neighbor.get_id())
                    queue.appendleft(neighbor)

        return # everything has been processed

    def find_shortest_path(self, start_id, target_id):
        """
        Find and return the shortest path from start_id to target_id.

        Parameters:
        start_id (string): The id of the start vertex.
        target_id (string): The id of the target (end) vertex.

        Returns:
        list<string>: A list of all vertex ids in the shortest path, from start to end.
        """
        if not self.contains_id(start_id) or not self.contains_id(target_id):
            raise KeyError("One or both vertices are not in the graph!")

        # vertex keys we've seen before and their paths from the start vertex
        vertex_id_to_path = {
            start_id: [start_id] # only one thing in the path
        }

        # queue of vertices to visit next
        queue = deque() 
        queue.append(self.get_vertex(start_id))

        # while queue is not empty
        while queue:
            current_vertex_obj = queue.pop() # vertex obj to visit next
            current_vertex_id = current_vertex_obj.get_id()

            neighbors = current_vertex_obj.get_neighbors()

            for neighbor in neighbors:
                if neighbor.get_id() not in vertex_id_to_path:
                    current_path = vertex_id_to_path[current_vertex_id]
                    # extend the path by 1 vertex
                    next_path = current_path + [neighbor.get_id()]
                    vertex_id_to_path[neighbor.get_id()] = next_path
                    queue.appendleft(neighbor)

        if target_id not in vertex_id_to_path: # path not found
            return None

        return vertex_id_to_path[target_id]

    def find_vertices_n_away(self, start_id, target_distance):
        """
        Find and return all vertices n distance away.
        
        Arguments:
        start_id (string): The id of the start vertex.
        target_distance (integer): The distance from the start vertex we are looking for

        Returns:
        list<string>: All vertex ids that are `target_distance` away from the start vertex
        """
    
        vertices_n_distance = {
            start_id: 0
        }
        solutions = []
        seen = set()
        seen.add(start_id)

        queue = deque()
        queue.append(self.get_vertex(start_id))

        stop = False

        while queue:
            # stop = False
            vertex_object = queue.pop()
            vertex_id = vertex_object.get_id()

            neighbors = vertex_object.get_neighbors()

            # flag if we reach a vertex that is right before the final vertex
            # to avoid running extra traversals
            if vertices_n_distance[vertex_id] == target_distance - 1:
                stop = True

            for neighbor in neighbors:
                neighbor_id = neighbor.get_id()
                if neighbor_id not in seen:
                    if neighbor_id not in vertices_n_distance:
                        vertices_n_distance[neighbor_id] = vertices_n_distance[vertex_id]
                    vertices_n_distance[neighbor_id] += 1
                    if vertices_n_distance[neighbor_id] == target_distance:
                        solutions.append(neighbor_id)
                    if stop == False:
                        seen.add(neighbor_id)
                        queue.appendleft(neighbor)
        return solutions

    def is_bipartite(self):
        """Return True if the graph is bipartite, and False otherwise."""

        start_id = choice(list(self.__vertex_dict.keys()))

        queue = deque()
        queue.append(self.get_vertex(start_id))

        colors = {
            start_id: "red"
        }

        while queue:
            v_obj = queue.pop()
            v_id = v_obj.get_id()

            neighbors = v_obj.get_neighbors()

            for n in neighbors:
                n_id = n.get_id()
                if n_id not in colors:
                    colors[n_id] = "blue" if colors[v_id] == "red" else "red"
                    queue.appendleft(n)
                else:
                    if colors[n_id] == colors[v_id]:
                        return False
        return True
    
    def get_connected_components(self):
        """
        Return a list of all connected components, with each connected component
        represented as a list of vertex ids.
        """
        start_id = choice(list(self.__vertex_dict.keys()))

        # must be a list, can't be a set because random.choice does not it
        remaining_ids = list(self.__vertex_dict.keys())
        remaining_ids.remove(start_id) 

        seen = set()
        seen.add(start_id)

        queue = deque()
        queue.append(self.get_vertex(start_id))

        components = []
        com = []
        while queue:
            v_obj = queue.pop()
            v_id = v_obj.get_id()
            com.append(v_id)

            neighbors = v_obj.get_neighbors()

            for n in neighbors:
                n_id = n.get_id()
                if n_id not in seen:
                    seen.add(n_id)
                    queue.appendleft(n)
                    remaining_ids.remove(n_id)

            # if there is no vertex left in the queue
            if len(queue) == 0:
                components.append(com)
                # if there are no more components left to traverse through
                if len(remaining_ids) == 0:
                    break
                com = []
                new_start = choice(remaining_ids)
                seen.add(new_start)
                queue.appendleft(self.get_vertex(new_start))
                remaining_ids.remove(new_start)

        return components

    def find_path_dfs_iter(self, start_id, target_id):
        """
        Use DFS with a stack to find a path from start_id to target_id.
        """
        if not self.contains_id(start_id) or not self.contains_id(target_id):
            raise KeyError("One or both vertices are not in the graph!")

        paths = {
            start_id: [start_id]
        }

        stack = deque()
        stack.append(self.get_vertex(start_id))

        while stack: 
            v_obj = stack.pop()
            v_id = v_obj.get_id()

            neighbors = v_obj.get_neighbors()

            for n in neighbors:
                n_id = n.get_id()
                if  n_id not in paths:
                    current_path = paths[v_id]
                    next_path = current_path + [n_id]
                    if n_id == target_id:
                        return next_path
                    paths[n_id] = next_path
                    stack.append(n)
        return path

    def dfs_traversal(self, start_id):
        """Visit each vertex, starting with start_id, in DFS order."""

        visited = set()  # set of vertices we've visited so far

        def dfs_traversal_recursive(start_vertex):
            print(f'Visiting vertex {start_vertex.get_id()}')

            # recurse for each vertex in neighbors
            for neighbor in start_vertex.get_neighbors():
                if neighbor.get_id() not in visited:
                    visited.add(neighbor.get_id())
                    dfs_traversal_recursive(neighbor)
            return

        visited.add(start_id)
        start_vertex = self.get_vertex(start_id)
        dfs_traversal_recursive(start_vertex)

    # help from Geek for Geeks: https://www.geeksforgeeks.org/detect-cycle-in-a-graph/
    def contains_cycle(self):
        """
        Return True if the directed graph contains a cycle, False otherwise.
        """
        def dfs_cycle(vertex, visited, recursion_stack):
            v_id = vertex.get_id()
            visited.append(v_id)
            neighbors = vertex.get_neighbors()
            for n in neighbors:
                n_id = n.get_id()
                if n_id in visited:
                    recursion_stack.append(True)
                    return
                else:
                    recursion_stack.append(False)
                    dfs_cycle(n, visited, recursion_stack)
            return recursion_stack[-1]
        
        start_id = list(self.__vertex_dict.keys())[0]
        start_obj = self.get_vertex(start_id)
        visited, recursion_stack = [start_id], []
        is_cycle = dfs_cycle(start_obj, visited, recursion_stack)
        return is_cycle

    def topological_sort(self):
        """
        Return a valid ordering of vertices in a directed acyclic graph.
        If the graph contains a cycle, throw a ValueError.
        """
        # will submit this part late
        pass 


if __name__ == "__main__":
    graph = Graph(is_directed=True)
    graph.add_vertex('A')
    graph.add_vertex('B')
    graph.add_vertex('C')
    # graph.add_vertex('D')
    # graph.add_vertex('E')
    # graph.add_vertex('F')
    # graph.add_vertex('G')
    # graph.add_vertex('H')
    # graph.add_vertex('Y')
    # graph.add_vertex('Z')

    graph.add_edge('A', 'B')
    # graph.add_edge('A', 'D')
    graph.add_edge('B', 'C')
    # graph.add_edge('C', 'D')
    graph.add_edge('C', 'A')

    # graph.add_edge('A', 'B')
    # graph.add_edge('A', 'E')
    # graph.add_edge('B', 'C')
    # graph.add_edge('C', 'D')
    # graph.add_edge('B', 'D')
    # graph.add_edge('E', 'F')
    # graph.add_edge('G', 'D')

    # graph.add_edge('A', 'B')
    # graph.add_edge('A', 'C')
    # graph.add_edge('B', 'C')
    # graph.add_edge('C', 'Z')
    # graph.add_edge('D', 'E')
    # graph.add_edge('E', 'F')
    # graph.add_edge('F', 'Y')
    # graph.add_edge('G', 'H')

    # print(graph.is_bipartite())
    # print(graph.get_connected_components())
    # print(graph.bfs_traversal('A'))
    # print(graph.find_path_dfs_iter('A', 'F'))
    # print(graph.topological_sort())
    print(graph.contains_cycle())
