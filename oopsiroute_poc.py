# oopsiroute_poc.py
import heapq
import math
from collections import deque

class Graph:
    def __init__(self):
        # adjacency list: {node: {neighbor: weight, ...}, ...}
        self.nodes = {}

    # ------------------- Node / Edge Management -------------------
    def add_node(self, node):
        if node not in self.nodes:
            self.nodes[node] = {}
            print(f"[add_node] added {node}")

    def remove_node(self, node):
        if node in self.nodes:
            # Remove edges pointing to this node
            for n, neighbors in self.nodes.items():
                if node in neighbors:
                    del neighbors[node]
            # Remove the node
            del self.nodes[node]
            print(f"[remove_node] removed {node}")
        else:
            print(f"[remove_node] node {node} does not exist")

    def add_edge(self, u, v, weight=1.0):
        if u not in self.nodes or v not in self.nodes:
            raise KeyError(f"add_edge: one or both nodes not present: {u}, {v}")
        self.nodes[u][v] = weight
        self.nodes[v][u] = weight  # For undirected graph
        print(f"[add_edge] added edge {u} <-> {v} w={weight}")

    def remove_edge(self, u, v):
        if u in self.nodes and v in self.nodes[u]:
            del self.nodes[u][v]
        if v in self.nodes and u in self.nodes[v]:
            del self.nodes[v][u]
        print(f"[remove_edge] removed edge {u} <-> {v}")

    def neighbors(self, node):
        return self.nodes.get(node, {})

    # ------------------- BFS Traversal -------------------
    def bfs(self, start):
        visited = set()
        queue = deque([start])
        order = []

        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                order.append(node)
                for neighbor in self.nodes[node]:
                    if neighbor not in visited:
                        queue.append(neighbor)
        return order

    # ------------------- Dijkstra Shortest Path -------------------
    def dijkstra(self, source, target=None):
        dist = {n: math.inf for n in self.nodes}
        prev = {n: None for n in self.nodes}
        dist[source] = 0
        pq = [(0, source)]

        while pq:
            d, u = heapq.heappop(pq)
            if target is not None and u == target:
                break
            for v, w in self.neighbors(u).items():
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    prev[v] = u
                    heapq.heappush(pq, (dist[v], v))
        return dist, prev

    # ------------------- Reconstruct Path -------------------
    def reconstruct_path(self, prev, start, end):
        """Reconstruct the shortest path from start to end using prev dict"""
        path = []
        at = end
        while at is not None:
            path.insert(0, at)
            at = prev[at]
        if path and path[0] == start:
            return path
        return []  # no path exists

    # ------------------- Optional: A* (stub) -------------------
    def a_star(self, start, end, heuristic=None):
        """Simple A* skeleton. heuristic should be a function(node1, node2) -> float"""
        if heuristic is None:
            heuristic = lambda x, y: 0  # fallback to Dijkstra

        open_set = []
        heapq.heappush(open_set, (0, start))
        g_score = {n: math.inf for n in self.nodes}
        g_score[start] = 0
        prev = {n: None for n in self.nodes}

        while open_set:
            _, current = heapq.heappop(open_set)
            if current == end:
                break
            for neighbor, weight in self.neighbors(current).items():
                tentative_g = g_score[current] + weight
                if tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, end)
                    prev[neighbor] = current
                    heapq.heappush(open_set, (f_score, neighbor))
        return self.reconstruct_path(prev, start, end)

# ------------------- Demo / Test -------------------
if __name__ == "__main__":
    g = Graph()
    for node in ['A', 'B', 'C', 'D', 'E']:
        g.add_node(node)
    g.add_edge('A', 'B', 1)
    g.add_edge('B', 'C', 2)
    g.add_edge('A', 'D', 2)
    g.add_edge('D', 'E', 1.4)
    g.add_edge('C', 'E', 2.5)

    print("BFS from A:", g.bfs('A'))

    dist, prev = g.dijkstra('A', 'E')
    path = g.reconstruct_path(prev, 'A', 'E')
    print("Dijkstra A->E path:", path, "distance:", dist['E'])

    a_star_path = g.a_star('A', 'E')
    print("A* A->E path:", a_star_path)
