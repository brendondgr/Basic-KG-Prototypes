# Knowledge Graph Tutorial & Playground (Neo4j vs Gremlin)

A client-server web prototype designed to teach and compare the two major property graph paradigms: **Neo4j (Cypher)** and **Gremlin (Apache TinkerPop)**. 

The application runs on a real Python/Flask backend, parsing standard CSV datafiles from the `data/` directory to build an in-memory graph representation. It executes traversals and mutations dynamically on the server and feeds the results into an interactive D3.js force-directed canvas.

---

## Architecture Overview

- **`run.py`**: The entrypoint Flask server. It serves the static front-end resources and exposes JSON endpoints for loading graphs, simulating traversals, and querying driver scripts.
- **`data/`**: Represents the database table layer. Contains [nodes.csv](data/nodes.csv) (entity metadata) and [edges.csv](data/edges.csv) (directed links).
- **`utils/`**:
  - `data_loader.py`: Handles CSV parsing, schema configuration, and dynamic graph mapping in Python.
  - `neo4j_loader.py`: Implements Cypher pattern matching simulations and holds python-neo4j driver load templates.
  - `gremlin_loader.py`: Implements TinkerPop step-by-step traversal simulations and holds gremlinpython connection scripts.
- **`web/`**: Contains the front-end layout [kg-tutorial-prototype-2.html](web/kg-tutorial-prototype-2.html) using D3.js for visual rendering.

---

## Features

1. **Dual Paradigm Switching**: Toggle between Neo4j and Gremlin modes. Swapping instantly changes terminology (Nodes/Relationships vs. Vertices/Edges), active tutorials, and visual UI color themes (Slate-Teal vs. Slate-Purple).
2. **Interactive Force-directed Canvas**: Drag and move nodes dynamically. Surrounding links and arrowheads auto-align to node boundaries.
3. **Glassmorphic Property Inspector**: Hover over any node or edge in the visualization to review its properties inside a glassmorphic overlay.
4. **Backend Output Terminal**: Streams session execution logs, bytecode translations, and database actions directly from the Flask server, mimicking a real terminal output.
5. **Interactive Ingestion Scripts**: Click to inspect real Python scripts detailing how one would connect to and load `data/*.csv` files into a real running Neo4j or Gremlin instance.
6. **Live traversals simulation**: Run 6 core query playground operations (Fetch, Insert node, Insert edge, Delete node, Multi-hop traverse, Reverse traverse) and observe the backend-computed animation path highlight in real-time.

---

## Setup & Running

### Prerequisites
- Python 3.8 or higher installed on your system.

### 1. Install Dependencies
You can install the required packages (Flask) by running:
```bash
pip install -e .
```
*(Alternatively, run `pip install flask`)*

### 2. Run the Application
Start the Flask development server:
```bash
python run.py
```
*(On Windows systems, you can also use `py run.py`)*

### 3. Open in Browser
Visit the application at:
[**http://127.0.0.1:8543**](http://127.0.0.1:8543)

---

## Mock Database Schema

### Nodes (`data/nodes.csv`)
- **Person**: Alice (28), Bob (35), Charlie (32)
- **City**: New York (8.4M), San Francisco (880K)
- **Company**: Acme Corp (Tech, 2015), Stark Industries (Aerospace, 1963)

### Edges (`data/edges.csv`)
- `LIVES_IN` (e.g., Alice ➔ New York)
- `WORKS_AT` (e.g., Alice ➔ Stark Industries, with properties like `role` and `salary`)
- `HQ_IN` (e.g., Stark Industries ➔ New York)
- `KNOWS` (e.g., Alice ➔ Bob)
