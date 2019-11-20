from operator import attrgetter


# Sorry, I was too lazy to actually make this any better. It should be in a 'helper file' in larger projects
def are_values_unique(x):
    """ Asserts values are unique in a list """
    seen = set()
    return not any(i in seen or seen.add(i) for i in x)


class Vertex:
    """ Represents a vertex, for instance: A, B, C ... """

    def __init__(self, label: str):
        self.label = label

        # Needed for Kruskal's algorithm. Updated at the startup automatically
        self.ties = []
        self.has_visited = False
        self.neighbours = []

    @property
    def unvisited_neighbours(self) -> list:
        return [n for n in self.neighbours if not n.has_visited]

    def __repr__(self):
        return "Vertex {0}".format(self.label)


class Connection:
    """ Represents a Connection between two Vertex objects, with an associated weight """

    def __init__(self, vertex_one: Vertex, vertex_two: Vertex, weight: float):
        self.vertex_one = vertex_one
        self.vertex_two = vertex_two
        self.weight = weight
        self.has_chosen = False

    def __repr__(self):
        return "Connection {0} - {1} - {2}".format(self.vertex_one.label, self.weight, self.vertex_two.label)


class Graph:
    """ Represents a whole Graph. It also facilitates developers to create them with helper functions """

    def __init__(self, vertexes=None, connections=None):
        if connections is None:
            connections = []
        if vertexes is None:
            vertexes = []
        self.vertexes = vertexes
        self.connections = connections
        self.__origin_index__ = None
        self.__destination_index__ = None

    def get_vertex_by_label(self, label: str) -> Vertex:
        if not label or not isinstance(label, str):
            raise ValueError("Label must be a string")

        vertex = None
        for v in self.vertexes:
            if v.label == label:
                vertex = v
                break
        return vertex

    def get_cost_from_to(self, v1: Vertex, v2: Vertex) -> float:
        distance = 0
        for c in self.connections:
            if (c.vertex_one == v1 and c.vertex_two == v2) or (c.vertex_one == v2 and c.vertex_two == v1):
                distance = c.weight
                break
        return distance

    def add_vertex(self, label: str):
        if label in [x.label for x in self.vertexes]:
            raise IndexError("Labels must be unique. We have found a duplicate in Vertex labeled: {0}".format(label))
        self.vertexes.append(Vertex(label=label.upper()))

    def add_vertexes(self, list_of_labels: list):
        if not all(isinstance(e, str) for e in list_of_labels):
            raise ValueError("List of vertexes labels must contain only strings")

        list_of_labels_upper = [x.upper() for x in list_of_labels]
        if not are_values_unique(list_of_labels_upper):
            raise IndexError("All values of vertexes labels must be unique. Please check again.")

        for label in list_of_labels_upper:
            self.add_vertex(label)

    def add_connection(self, label_one: str, weight: float, label_two: str):
        if not label_one or not label_two or not isinstance(label_one, str) or not isinstance(label_two, str):
            raise ValueError("Connection labels must be of type string.")
        label_one = label_one.upper()
        label_two = label_two.upper()
        if label_one == label_two:
            raise ValueError("Connection labels cannot be identical."
                             "\nGot: {0} - {1} - {2}".format(label_one, weight, label_two))

        vertex_one = self.get_vertex_by_label(label=label_one)
        if not vertex_one:
            raise ValueError("A Vertex with label {0} was not found".format(label_one))
        vertex_two = self.get_vertex_by_label(label=label_two)
        if not vertex_two:
            raise ValueError("A Vertex with label {0} was not found".format(vertex_two))

        try:
            weight = float(weight)
        except ValueError:
            raise ValueError("Weight must be a number")

        if weight <= 0:
            raise ValueError("Weights must be positive and greater than 0")

        for c in self.connections:
            if (c.vertex_one == vertex_one and c.vertex_two == vertex_two) or (
                    c.vertex_one == vertex_two and c.vertex_two == vertex_one):
                raise ValueError("You have assigned two weights for the same vertexes."
                                 "\nAssigned: {0} - {1} - {2}"
                                 "\nAttempted: {3} - {4} - {5}".format(c.vertex_one.label, c.weight, c.vertex_two.label,
                                                                       c.vertex_one.label, weight, c.vertex_two.label))

        self.connections.append(Connection(vertex_one=vertex_one, weight=weight, vertex_two=vertex_two))
        vertex_one.neighbours.append(vertex_two)
        vertex_two.neighbours.append(vertex_one)

    def add_connections(self, tuple_of_connections: list):
        for c in tuple_of_connections:
            self.add_connection(c[0], c[1], c[2])


class SpanningTree:
    """ Represents a SpanningTree """

    def __init__(self, connections=None):
        if connections is None:
            self.connections = []
        else:
            self.connections = connections

    def __repr__(self):
        rep_str = ''
        for c in self.connections:
            rep_str = rep_str + str(c) + '\n'

        return rep_str


class SpanningBranch:
    """ Represents a SpanningTree Branch"""

    def __init__(self, branch_id: int, connections=None):
        if not isinstance(branch_id, int) or branch_id < 0:
            raise TypeError("branch_id must be an integer >= 0")

        self.id = branch_id
        if connections is None:
            self.connections = []
        else:
            self.connections = connections

    def merge(self, other):
        if not isinstance(other, SpanningBranch):
            raise TypeError("A SpanningBranch can only be merged with another SpanningBranch")
        for c in other.connections:
            self.connections.append(c)

    def __repr__(self):
        rep_str = ''
        for c in self.connections:
            rep_str = rep_str + str(c) + '\n'

        return rep_str


    @property
    def vertexes(self):
        vertxs = []
        for c in self.connections:
            if c.vertex_one not in vertxs:
                vertxs.append(c.vertex_one)
            if c.vertex_two not in vertxs:
                vertxs.append(c.vertex_two)

        return vertxs


class Kruskal:
    def __init__(self, graph=None):
        if isinstance(graph, Graph):
            self.graph = graph
        else:
            self.graph = Graph()

        self.spanning_tree = SpanningTree()
        self.ordered_connections = []

    def order_list(self):
        self.ordered_connections = sorted(self.graph.connections,
                                          key=lambda c: c.weight)

    def solve(self) -> SpanningTree:
        if not self.graph.vertexes or len(self.graph.vertexes) <= 0:
            raise ValueError("No graph found. Use Kruskal.graph.add_vertex() / Kruskal.graph.add_edge() to get started")

        # Weight ordering
        if not self.ordered_connections:
            self.order_list()   # This might be a bottleneck in big problems...

        spanning_branches = []  # Variable to hold disconnected branches
        for c in self.ordered_connections:  # For each connection
            """
                # If you want to stop whenever the minimum spanning tree length is completed
                if len(spanning_branches) == len(self.graph.vertexes) - 1:
                    break
            """
            # If node 1 and node 2 were not visited
            if not c.vertex_one.has_visited and not c.vertex_two.has_visited:
                # Creates a new SpanningBranch
                branch = SpanningBranch(branch_id=len(spanning_branches), connections=[c])
                spanning_branches.append(branch)
                c.has_chosen = True
                c.vertex_one.has_visited = True
                c.vertex_two.has_visited = True

            # Connecting unvisited node to a branch
            elif (not c.vertex_one.has_visited and c.vertex_two.has_visited) \
                    or (not c.vertex_two.has_visited and c.vertex_one.has_visited):

                vertex_visited = None   # See which vertex has been visited
                if c.vertex_one.has_visited:
                    vertex_visited = c.vertex_one
                else:
                    vertex_visited = c.vertex_two

                # For each existing spanning branch
                for b in spanning_branches:
                    # Find where the visited vertex is
                    if vertex_visited in b.vertexes:
                        # Insert the non visited vertex into the visited vertex SpanningBranch
                        c.has_chosen = True
                        c.vertex_one.has_visited = True
                        c.vertex_two.has_visited = True
                        b.connections.append(c)
                        break

            # Cycle detection
            elif c.vertex_one.has_visited and c.vertex_two.has_visited:
                vertex_one_branch = None
                # Finds vertex one branch
                for index1, b in enumerate(spanning_branches):
                    if c.vertex_one in b.vertexes:
                        vertex_one_branch = b
                        break

                vertex_two_branch = None
                # Finds vertex two branch
                for index2, b in enumerate(spanning_branches):
                    if c.vertex_two in b.vertexes:
                        vertex_two_branch = b
                        break

                # If they are not on the same branch
                if vertex_one_branch.id != vertex_two_branch.id:
                    # Gets the branch with minimum id
                    if vertex_two_branch.id < vertex_one_branch.id:
                        root_branch = vertex_two_branch
                        merge_branch = vertex_one_branch
                    else:
                        root_branch = vertex_one_branch
                        merge_branch = vertex_two_branch

                    # Merge branches and insert connection on the merged branch
                    c.has_chosen = True
                    c.vertex_one.has_visited = True
                    c.vertex_two.has_visited = True
                    root_branch.connections.append(c)
                    root_branch.merge(merge_branch)
                    spanning_branches.remove(merge_branch)

        if len(spanning_branches) > 1:
            raise InterruptedError("[FATAL ERROR]: Not all branches were connected")

        if len(spanning_branches) <= 0:
            raise InterruptedError("[FATAL ERROR]: No spanning branches were detected")

        self.spanning_tree = SpanningTree(connections=spanning_branches[0].connections)
        return self.spanning_tree


if __name__ == '__main__':
    """ Example on how to setup and run the Kruskal's algorithm """
    # Initiates an instance of Kruskal's class
    k = Kruskal()
    # Add vertexes with any custom Label
    k.graph.add_vertexes(['A', 'B', 'C', 'D', 'E'])
    # Adds connections between the vertexes. Labels must match with already added vertexes
    k.graph.add_connections([
        ('A', 3, 'B'),
        ('A', 1, 'E'),
        ('B', 5, 'C'),
        ('B', 4, 'E'),
        ('C', 6, 'E'),
        ('C', 2, 'D'),
        ('D', 7, 'E')
    ])

    # Solves and returns a SpanningTree object, with all the information stored inside it
    minimum_spanning_tree = k.solve()
    print(minimum_spanning_tree)




