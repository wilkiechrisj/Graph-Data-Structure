# Course: CS261 Data Structures
# Author: Christopher Wilkie
# Assignment: DirectedGraph
# Description: A collection of functions used to create and manipulate directedGraphs

class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        Adds a vertex to a DirectedGraph.
        """

        self.v_count += 1
        vertex = [0] * self.v_count

        for element in self.adj_matrix:
            element.append(0)

        self.adj_matrix.append(vertex)

        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Adds a weighted edge to a DirectedGraph from the "src" source to the "dst" destination.
        If the input is invalid returns None. Weights must be a positive integer.
        """

        if weight <= 0 or src == dst or src < 0 or dst < 0:
            return None

        try:
            self.adj_matrix[src][dst] = weight
        except IndexError:
            return None

        return None

    def remove_edge(self, src: int, dst: int) -> None:
        """
        Removes a weighted edge from a DirectedGraph
        """

        if src == dst or src < 0 or dst < 0:
            return None

        try:
            self.adj_matrix[src][dst] = 0
        except IndexError:
            return None

        return None

    def get_vertices(self) -> []:
        """
        Returns a list of vertices contained in a DirectedGraph.
        """

        vertices = [num for num in range(self.v_count)]

        return vertices

    def get_edges(self) -> []:
        """
        Returns a list of edges represented as tuples (source, destination, weight).
        """

        edge_list = []
        source = -1

        for vertex in self.adj_matrix:

            source += 1
            destination = -1

            for edge in vertex:

                destination += 1

                if edge == 0:
                    continue
                else:
                    edge_list.append((source, destination, edge))

        return edge_list

    def is_valid_path(self, path: []) -> bool:
        """
        Takes a list representing a path of vertices as an argument.
        Returns true if the path is valid, False if otherwise.
        """

        source = 0
        destination = 1

        while destination < len(path):

            if self.adj_matrix[path[source]][path[destination]] == 0:
                return False

            source += 1
            destination += 1

        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Returns a list of vertices visited during DFS search.
        Vertices are picked in numerical order.
        """

        if v_start > self.v_count or v_start < 0:
            return []

        visited = []
        stack = [v_start]

        while stack:

            vertex = stack.pop()

            if vertex in visited:
                continue

            visited.append(vertex)

            if vertex == v_end:
                return visited

            to_stack = []
            index = 0

            for element in self.adj_matrix[vertex]:
                if element != 0:
                    to_stack.append(index)
                index += 1

            to_stack.sort(reverse=True)

            for element in to_stack:
                if element != vertex and element not in visited:
                    stack.append(element)

        return visited

    def bfs(self, v_start, v_end=None) -> []:
        """
        Returns a list of vertices visited during BFS search.
        Vertices are picked in numerical order.
        """

        if v_start > self.v_count or v_start < 0:
            return []

        visited = []
        queue = [v_start]

        while queue:

            vertex = queue.pop(0)

            if vertex in visited:
                continue

            visited.append(vertex)

            if vertex == v_end:
                return visited

            to_queue = []
            index = 0

            for element in self.adj_matrix[vertex]:
                if element != 0:
                    to_queue.append(index)
                index += 1

            to_queue.sort()

            for element in to_queue:
                if element != vertex and element not in visited:
                    queue.append(element)

        return visited

    def has_cycle(self):
        """
        Returns True if the graph is cyclic, False if it is acyclic.
        """

        vertices = self.get_vertices()

        while vertices:

            vertex = vertices.pop()
            connects = []
            index = 0

            for element in self.adj_matrix[vertex]:
                if element != 0:
                    connects.append(index)
                index += 1

            for element in connects:
                route = self.dfs(element)

                if vertex in route:
                    return True

        return False

    def dijkstra(self, src: int) -> []:
        """
        Uses Dijkstra's algorithm to determine the shortest possible path to any vertex from the provided source vertex.
        Returns a list of the "distance" required to reach each vertex in the order provided by the get_vertices fxn.
        If it is impossible to reach a certain vertex, its "distance" is represented by "inf".
        """

        table = dict()
        weights = []
        vertices = self.get_vertices()
        visited = []
        queue = [src]

        for element in vertices:
            table[element] = [float('inf'), None]

        if src in table:
            table[src] = [0, None]

        while queue:

            vertex = queue.pop(0)
            visited.append(vertex)
            vertex_weights = self.adj_matrix[vertex]
            index = 0

            for element in vertex_weights:
                if element != 0:
                    if table[index][0] > element + table[vertex][0]:
                        table[index][0] = element + table[vertex][0]
                        table[index][1] = vertex
                        for pair in table:
                            if table[pair][1] == index:
                                table[pair][0] = table[index][0] + self.adj_matrix[index][pair]
                    if index not in visited:
                        queue.append(index)
                index += 1

        for element in table:
            weights.append(table[element][0])

        return weights


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(12):
        g.add_vertex()
    edges = [(7, 0, 4), (6, 2, 17), (0, 4, 10), (11, 4, 10),
             (7, 5, 10), (8, 5, 19), (11, 5, 1), (5, 4, 9), (5, 6, 16), (8, 6, 3), (9, 7, 3),
             (5, 8, 5), (7, 8, 8), (1, 11, 5)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)
    print(g.dijkstra(1))

    """
    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)


    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    """