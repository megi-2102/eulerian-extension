**Eulerian Graph Tester**
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
This project is a Python application that allows users to test and visualize directed graphs and transform them into Eulerian graphs by adding the minimal number of edges.

It uses Tkinter for the GUI, NetworkX for graph operations, and Matplotlib for visualization.

♦ Features ♦

• Check if a directed graph is Eulerian (each node has equal in-degree and out-degree, and the graph is weakly connected).
		
• Identify unbalanced nodes and automatically add edges to make the graph Eulerian.
		
• Uses brute-force for small graphs (optimal solution) and a greedy approach for larger graphs (faster).
		
• Visualize graphs before and after transformation.
		
• GUI interface with predefined graphs and custom graph input.


♦ Installation ♦

1. Clone this repository from GitHub.

2. Install dependencies with:
		pip install matplotlib networkx
		(Tkinter is included with most Python installations).


♦ Usage ♦

Run the program with:
python EulerianExtension.py


♦ Steps: ♦

1. When running the program, a GUI window will appear.

2. Choose a predefined graph or select Custom Graph and enter edges in the format A->B,B->C,C->A.

3. The program will display node degrees, check if the graph is Eulerian, and show added edges if needed.

4. The graph will be visualized before and after making it Eulerian.


♦ Example ♦

	Input Graph: A → B → C → D
	Output Graph: A → B → C → D → A
	The program adds the minimal edge D → A to make the graph Eulerian.


♦ Technologies ♦

• Python 3.x
		
• Tkinter
		
• Matplotlib
		
• NetworkX


♦ Future Improvements ♦

• Save results as images or JSON.
		
• Add support for weighted graphs.
		
• Use advanced heuristics for very large graphs.


♦ License ♦

This project is open-source under the MIT License.
