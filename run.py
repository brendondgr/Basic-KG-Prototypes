import os
from flask import Flask, jsonify, request, send_from_directory
from utils.data_loader import DataLoader
from utils.neo4j_loader import Neo4jLoader
from utils.gremlin_loader import GremlinLoader

app = Flask(__name__)

# Initialize loaders and global memory graph state
data_loader = DataLoader(data_dir='data')
neo4j_helper = Neo4jLoader()
gremlin_helper = GremlinLoader()

# In-memory graph state loaded from CSVs
GRAPH_STATE = data_loader.load_graph()

# Note: Graph visualization physics & dynamic transitions are handled on the frontend
# in `web/kg-tutorial-prototype-2.html`. We fixed the "extreme reaction" to new nodes
# by initializing node positions close to their neighbors and reducing D3 restart alpha.

@app.route('/')
def index():
    """Serves the main Knowledge Graph tutorial HTML page."""
    return send_from_directory('web', 'kg-tutorial-prototype-2.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serves static files in the web directory (D3 scripts, CSS, etc.)."""
    return send_from_directory('web', path)

@app.route('/api/graph', methods=['GET'])
def get_graph():
    """API endpoint to retrieve the current graph nodes and edges."""
    return jsonify(GRAPH_STATE)

@app.route('/api/reset', methods=['POST'])
def reset_graph():
    """API endpoint to reload the graph from original CSV datafiles."""
    global GRAPH_STATE
    try:
        GRAPH_STATE = data_loader.load_graph()
        return jsonify({"status": "success", "message": "Graph successfully reset from CSVs.", "graph": GRAPH_STATE})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/simulate', methods=['POST'])
def simulate_query():
    """
    API endpoint to execute a query (Cypher or Gremlin) against the backend graph.
    Returns visual traversal highlights and backend execution logs.
    """
    data = request.json or {}
    query = data.get('query', '')
    paradigm = data.get('paradigm', 'neo4j').lower()
    
    if not query:
        return jsonify({"error": "No query string provided."}), 400
        
    if paradigm == 'neo4j':
        result = neo4j_helper.run_query_on_memory(GRAPH_STATE, query)
    elif paradigm == 'gremlin':
        result = gremlin_helper.run_query_on_memory(GRAPH_STATE, query)
    else:
        return jsonify({"error": f"Unsupported paradigm: {paradigm}"}), 400
        
    return jsonify({
        "steps": result["steps"],
        "logs": result["logs"]
    })

@app.route('/api/ingestion-code/<paradigm>', methods=['GET'])
def get_ingestion_code(paradigm):
    """API endpoint to get the real Python connection and ingestion driver script."""
    paradigm = paradigm.lower()
    if paradigm == 'neo4j':
        code = neo4j_helper.get_ingestion_code()
    elif paradigm == 'gremlin':
        code = gremlin_helper.get_ingestion_code()
    else:
        return jsonify({"error": f"Unsupported paradigm: {paradigm}"}), 400
        
    return jsonify({
        "paradigm": paradigm,
        "code": code
    })

if __name__ == '__main__':
    print("--------------------------------------------------")
    print(" Knowledge Graph Flask server running on http://127.0.0.1:8543")
    print(" Serves: web/kg-tutorial-prototype-2.html")
    print("--------------------------------------------------")
    app.run(host='0.0.0.0', port=8543, debug=True)
