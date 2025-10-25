# oopsiroute_api.py
from flask import Flask, request, jsonify
from oopsiroute_poc import Graph

app = Flask(__name__)

# ------------------- Initialize Graph -------------------
g = Graph()

# Add nodes
for node in ['A', 'B', 'C', 'D', 'E']:
    g.add_node(node)

# Add edges (after nodes are added)
g.add_edge('A', 'B', 1)
g.add_edge('B', 'C', 2)
g.add_edge('A', 'D', 2)
g.add_edge('D', 'E', 1.4)
g.add_edge('C', 'E', 2.5)

# ------------------- Flask Routes -------------------
@app.route('/')
def home():
    return "OopsiRoute API is running!"

@app.route('/route', methods=['GET'])
def get_route():
    """
    Returns shortest path and distance between source and destination nodes.
    Example usage:
    http://127.0.0.1:5000/route?src=A&dest=E
    """
    src = request.args.get('src', 'A')
    dest = request.args.get('dest', 'E')

    # Validate nodes exist
    if src not in g.nodes or dest not in g.nodes:
        return jsonify({"error": f"One or both nodes not found: {src}, {dest}"}), 400

    # Compute shortest path using Dijkstra
    dist, prev = g.dijkstra(src, dest)
    path = g.reconstruct_path(prev, src, dest)

    if not path:
        return jsonify({"error": f"No path found between {src} and {dest}"}), 404

    return jsonify({
        "source": src,
        "destination": dest,
        "path": path,
        "distance": dist[dest]
    })

# ------------------- Optional: Test Connectivity -------------------
@app.route('/bfs', methods=['GET'])
def get_bfs():
    start = request.args.get('start', 'A')
    if start not in g.nodes:
        return jsonify({"error": f"Node not found: {start}"}), 400
    order = g.bfs(start)
    return jsonify({"start": start, "bfs_order": order})

# ------------------- Run Flask App -------------------
if __name__ == '__main__':
    # Use 0.0.0.0 so the Android emulator can access it
    app.run(host='0.0.0.0', port=5000, debug=True)
