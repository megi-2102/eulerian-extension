import tkinter as tk
from tkinter import simpledialog, ttk
import matplotlib.pyplot as plt
import networkx as nx
from itertools import permutations
import copy
import time

# Check if a directed graph is Eulerian:
# A graph is Eulerian if it is weakly connected and each node has equal in-degree and out-degree
def is_eulerian(G):
    return nx.is_weakly_connected(G) and all(G.in_degree(n) == G.out_degree(n) for n in G)

# Identify nodes with unbalanced degrees
def get_unbalanced_nodes(G):
    out_extra, in_extra = [], []
    for node in G:
        in_deg, out_deg = G.in_degree(node), G.out_degree(node)
        if out_deg > in_deg:
            # Node has extra outgoing edges → needs incoming connections
            in_extra.extend([node] * (out_deg - in_deg))
        elif in_deg > out_deg:
            # Node has extra incoming edges → needs outgoing connections
            out_extra.extend([node] * (in_deg - out_deg))
    return out_extra, in_extra

# Connect disconnected components to make the graph weakly connected
def connect_components(G):
    comps = list(nx.weakly_connected_components(G))
    if len(comps) <= 1:
        return []
    # Use a representative node from each component to connect them in sequence
    reps = [next(iter(comp)) for comp in comps]
    edges = [(reps[i], reps[i+1]) for i in range(len(reps)-1)]
    G.add_edges_from(edges)
    return edges

# Main function to convert a graph to Eulerian by adding the minimal number of edges
def make_eulerian(G):
    out_nodes, in_nodes = get_unbalanced_nodes(G)
    best_graph, best_edges = None, None

    if len(out_nodes) <= 8:
        # Use brute-force: try all permutations of in_nodes
        for perm in permutations(in_nodes):
            tempG = copy.deepcopy(G)
            added = [(u, v) for u, v in zip(out_nodes, perm) if u != v]
            tempG.add_edges_from(added)

            # Ensure connectivity
            added += connect_components(tempG)

            # Keep best (minimal edge addition) Eulerian graph
            if is_eulerian(tempG) and (best_edges is None or len(added) < len(best_edges)):
                best_graph, best_edges = tempG, added

        if best_graph:
            G.clear()
            G.add_edges_from(best_graph.edges())
            return best_edges
        return []
    else:
        # Use greedy matching for larger graphs (faster but not always optimal)
        added = [(u, v) for u, v in zip(out_nodes, in_nodes)]
        G.add_edges_from(added)

        # Connect components if needed
        added += connect_components(G)
        return added

# Display the graph using matplotlib
def visualize_graph(G, title):
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=1500, font_size=12)
    plt.title(title)
    plt.show()

# Run test on selected graph or custom graph
def run_selected_graph(name, custom_edges=None):
    # Predefined graph structures
    presets = {
        "Already Eulerian": [("A", "B"), ("B", "C"), ("C", "A")],
        "Simple Imbalance": [("A", "B"), ("B", "C"), ("C", "D")],
        "Disconnected Components": [("A", "B"), ("C", "D"), ("E", "F")],
        "Star Structure": [("Center", "A"), ("Center", "B"), ("Center", "C")],
        "Back Edges": [("A", "B"), ("B", "C"), ("C", "A"), ("C", "D"), ("D", "A")],
        "Custom Graph": custom_edges or []
    }

    G = nx.DiGraph()
    G.add_edges_from(presets[name])

    print(f"\nSelected Graph: {name}")
    print("Before:")
    for n in G:
        print(f"Node {n}: in={G.in_degree(n)}, out={G.out_degree(n)}")
    print("Is Eulerian:", is_eulerian(G))

    visualize_graph(G, f"Before: {name}")

    if not is_eulerian(G):
        start = time.time()
        added = make_eulerian(G)
        end = time.time()
        print("\nAfter:")
        for n in G:
            print(f"Node {n}: in={G.in_degree(n)}, out={G.out_degree(n)}")
        print("Is Eulerian:", is_eulerian(G))
        print("Edges added:", len(added), "→", added)
        print("Time taken:", end - start, "seconds")
        visualize_graph(G, f"After: {name}")

# Convert user input string into a list of edge tuples
def parse_custom_input(s):
    try:
        return [tuple(edge.strip().split("->")) for edge in s.split(",")]
    except:
        print("Invalid format. Use: A->B,B->C")
        return []

# Launch the GUI using tkinter
def launch_ui():
    root = tk.Tk()
    root.title("Eulerian Graph Tester")

    tk.Label(root, text="Select a graph to test:").pack(pady=10)
    # Dropdown menu options
    options = [
        "Already Eulerian", "Simple Imbalance", "Disconnected Components",
        "Star Structure", "Back Edges", "Custom Graph"
    ]

    combo = ttk.Combobox(root, values=options)
    combo.pack(pady=10)
    combo.current(0)

    # When "Run Test" is clicked
    def run():
        selection = combo.get()
        if selection == "Custom Graph":
            user_input = simpledialog.askstring("Input", "Enter edges (e.g. A->B,B->C)")
            custom = parse_custom_input(user_input)
            run_selected_graph(selection, custom)
        else:
            run_selected_graph(selection)

    tk.Button(root, text="Run Test", command=run).pack(pady=10)
    root.mainloop()

# Start the application
if __name__ == "__main__":
    launch_ui()
