from graphs.graph import Graph

def read_graph_from_file(filename):
    """
    Read in data from the specified filename, and create and return a graph
    object corresponding to that data.

    Arguments:
    filename (string): The relative path of the file to be processed

    Returns:
    Graph: A directed or undirected Graph object containing the specified
    vertices and edges
    """

    # Use 'open' to open the file
    f = open(filename, "r").read().split()

    # Use the first line (G or D) to determine whether graph is directed
    # and create a graph object
    is_directed = True if f[0] == "D" else False
    graph = Graph(is_directed=is_directed)

    # Use the second line to add the vertices to the graph
    vertices = f[1].split(',')
    for v in vertices:
        graph.add_vertex(v)

    # Use the 3rd+ line to add the edges to the graph
    edges = f[2:]
    for e in edges:
        v1, v2 = e.strip(')(').split(',')
        graph.add_edge(v1, v2)
    
    return graph


if __name__ == '__main__':

    graph = read_graph_from_file('test.txt')

    # print(graph)
