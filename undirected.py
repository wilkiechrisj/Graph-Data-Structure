# Course: CS261 Data Structures
# Author: Christopher Wilkie
# Assignment: UndirectedGraph
# Description: A collection of functions used to create and manipulate UndirectedGraphs


class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str, connect=None) -> None:
        """
        Adds a vertex to an UndirectedGraph.
        """

        for vertex in self.adj_list:
            if vertex == v:
                return None

        if connect is None:
            self.adj_list[v] = []
        else:
            self.adj_list[v] = connect

        return None
        
    def add_edge(self, u: str, v: str) -> None:
        """
        Adds an edge to an UndirectedGraph.
        """

        if u == v:
            return None

        v_in = False
        u_in = False

        for vertex in self.adj_list:
            if vertex == v:
                if u not in self.adj_list[v]:
                    self.adj_list[vertex].append(u)
            if vertex == u:
                if v not in self.adj_list[u]:
                    self.adj_list[vertex].append(v)

        if not u_in:
            self.add_vertex(u, [v])

        if not v_in:
            self.add_vertex(v, [u])

        return None

    def remove_edge(self, v: str, u: str) -> None:
        """
        Removes an edge from an UndirectedGraph.
        """

        v_in = False
        u_in = False

        for vertex in self.adj_list:
            if vertex == v:
                v_in = True
            if vertex == u:
                u_in = True

        if v_in and u_in:
            if u in self.adj_list[v]:
                self.adj_list[v].remove(u)
                self.adj_list[u].remove(v)

        return None

    def remove_vertex(self, v: str) -> None:
        """
        Removes a vertex and all its edges from an UndirectedGraph.
        """

        if v not in self.adj_list:
            return None

        del self.adj_list[v]

        for vertex in self.adj_list:
            if v in self.adj_list[vertex]:
                self.adj_list[vertex].remove(v)

        return None

    def get_vertices(self) -> []:
        """
        Returns a list of vertices.
        """

        vertices = []

        for vertex in self.adj_list:
            vertices.append(vertex)

        return vertices

    def get_edges(self) -> []:
        """
        Returns a list of edges in a graph represented by tuples containing the two connected vertices.
        """

        edge_tuples = []

        for vertex in self.adj_list:
            for connect in self.adj_list[vertex]:
                if (connect, vertex) not in edge_tuples:
                    edge_tuples.append((vertex, connect))

        return edge_tuples

    def is_valid_path(self, path: []) -> bool:
        """
        Takes a list representing a path as an argument and determines if it is a valid path.
        Returns True if so, False if not.
        """

        connections = len(path)
        start = 0
        end = 1

        if connections == 1:
            if path[start] not in self.adj_list:
                return False

        while end < connections:
            if path[start] in self.adj_list and path[end] in self.adj_list:
                if path[start] in self.adj_list[path[end]]:
                    start += 1
                    end += 1
                else:
                    return False
            else:
                return False

        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Returns a list of vertices visited during DFS search.
        Vertices are picked in alphabetical order.
        """

        if v_start not in self.adj_list:
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

            to_stack = self.adj_list[vertex].copy()
            to_stack.sort(reverse=True)

            for element in to_stack:
                if element != vertex and element not in visited:
                    stack.append(element)

        return visited

    def bfs(self, v_start, v_end=None) -> []:
        """
        Returns a list of vertices visited during BFS search.
        Vertices are picked in alphabetical order.
        """
        
        if v_start not in self.adj_list:
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

            to_queue = self.adj_list[vertex].copy()
            to_queue.sort()

            for element in to_queue:
                if element != vertex and element not in visited:
                    queue.append(element)

        return visited

    def count_connected_components(self):
        """
        Returns a number representing the amount of connected components of a graph
        EX: The count would be > 1 if any "islands" of vertices exist.
        """

        vertices = []
        connections = 0

        for element in self.adj_list:
            vertices.append(element)

        while vertices:

            connections += 1

            connected = self.dfs(vertices[0])

            for element in connected:
                if element in vertices:
                    vertices.remove(element)

        return connections

    def has_cycle(self):
        """
        Returns True if the graph is cyclic, False if it is acyclic.
        """

        vertices = []

        for element in self.adj_list:
            vertices.append(element)

        while vertices:

            vertex = vertices.pop()
            connects = self.adj_list[vertex].copy()

            for element in connects:
                self.remove_edge(vertex, element)
                route = self.dfs(element)
                self.add_edge(vertex, element)

                if vertex in route:
                    return True

        return False


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)

    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)

    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')

    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))

    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')

    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()

    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
