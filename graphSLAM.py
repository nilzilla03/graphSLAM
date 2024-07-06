import numpy as np

class Edge:
    def __init__(self, src, dst, weight):
        self.src = src
        self.dst = dst
        self.weight = weight

class Graph:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        self.edges = []

    def add_edge(self, src, dst, weight):
        if src < 0 or src >= self.num_vertices or dst < 0 or dst >= self.num_vertices:
            raise ValueError("Vertex index out of bounds")
        self.edges.append(Edge(src, dst, weight))

    def get_edges(self):
        return self.edges

    def get_num_vertices(self):
        return self.num_vertices

def measurementUpdate(Omega, Xi, G):
    for edge in G.edges:
        Omega[edge.src][edge.src] += 1
        Omega[edge.src][edge.dst] += -1
        Xi[edge.src] += -edge.weight

        Omega[edge.dst][edge.dst] +=1
        Omega[edge.dst][edge.src] += -1
        Xi[edge.dst] += edge.weight
    
    return Omega, Xi

def stateUpdate(Omega, Xi):
    Mu = np.linalg.inv(Omega) @ Xi
    return Mu

def graphOptimization(Omega, Xi, G):
    Omega, Xi = measurementUpdate(Omega, Xi, G)
    Mu = stateUpdate(Omega, Xi)
    return Mu

def graphSLAM(G, startPose):
    n = G.get_num_vertices()
    Omega = np.zeros((n, n))
    Xi = np.zeros((n, 1))

    Omega[0][0] = 1
    Xi[0] = startPose

    Mu = graphOptimization(Omega, Xi, G)
    return Mu

G = Graph(4)
G.add_edge(0,1,5)
G.add_edge(1,2,3)
G.add_edge(0,3,9)
G.add_edge(2,3,1)

Mu = graphSLAM(G, 2)
print(Mu)