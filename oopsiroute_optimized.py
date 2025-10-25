import pandas as pd
import time
import random
import psutil

# =========================================
# Optimized Route Calculation (Dijkstra)
# =========================================
def optimized_dijkstra(graph, src):
    distances = {node: float('inf') for node in graph}
    distances[src] = 0
    visited = set()
    while len(visited) < len(graph):
        min_node = min((node for node in graph if node not in visited),
                       key=lambda node: distances[node], default=None)
        if min_node is None:
            break
        visited.add(min_node)
        for neighbor, weight in graph[min_node].items():
            new_distance = distances[min_node] + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
    return distances

# =========================================
# Simulate performance tests
# =========================================
def run_benchmark():
    results = []
    print("Running Phase 3 benchmark...")

    for n_nodes in [10, 50, 100, 500, 1000]:
        # Generate random weighted graph
        graph = {i: {} for i in range(n_nodes)}
        for i in range(n_nodes):
            for j in range(random.randint(1, min(10, n_nodes - 1))):
                target = random.randint(0, n_nodes - 1)
                if target != i:
                    graph[i][target] = random.randint(1, 20)

        start_mem = psutil.Process().memory_info().rss / (1024 * 1024)
        start_time = time.time()

        optimized_dijkstra(graph, 0)

        end_time = time.time()
        end_mem = psutil.Process().memory_info().rss / (1024 * 1024)

        exec_time = end_time - start_time
        mem_used = max(0, end_mem - start_mem)

        results.append({
            "Nodes": n_nodes,
            "Time (s)": exec_time,
            "Memory (MB)": mem_used
        })
        print(f"{n_nodes} nodes -> {exec_time:.4f}s, {mem_used:.4f}MB")

    # Save results
    df = pd.DataFrame(results)
    df.to_csv("phase3_results.csv", index=False)
    print("\n📊 Results saved to phase3_results.csv")

# =========================================
# Main
# =========================================
if __name__ == "__main__":
    run_benchmark()
