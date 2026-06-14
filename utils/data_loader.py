import os
import csv

class DataLoader:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.nodes_path = os.path.join(data_dir, 'nodes.csv')
        self.edges_path = os.path.join(data_dir, 'edges.csv')

    def load_graph(self):
        """Reads CSV files and returns a structured graph dict for D3.js and loading simulators."""
        nodes = []
        links = []

        # Parse Nodes
        if os.path.exists(self.nodes_path):
            with open(self.nodes_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    node_id = row.get('id')
                    label = row.get('label')
                    name = row.get('name')
                    
                    # Gather other columns as properties
                    properties = {}
                    for k, v in row.items():
                        if k not in ['id', 'label', 'name'] and v and v.strip():
                            # Try to cast numeric properties
                            try:
                                if '.' in v:
                                    properties[k] = float(v)
                                else:
                                    properties[k] = int(v)
                            except ValueError:
                                properties[k] = v

                    nodes.append({
                        "id": node_id,
                        "label": label,
                        "name": name,
                        "properties": properties
                    })

        # Parse Edges
        if os.path.exists(self.edges_path):
            with open(self.edges_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    edge_id = row.get('id')
                    source = row.get('source')
                    target = row.get('target')
                    edge_type = row.get('type')

                    # Gather other columns as properties
                    properties = {}
                    for k, v in row.items():
                        if k not in ['id', 'source', 'target', 'type'] and v and v.strip():
                            try:
                                if '.' in v:
                                    properties[k] = float(v)
                                else:
                                    properties[k] = int(v)
                            except ValueError:
                                properties[k] = v

                    links.append({
                        "id": edge_id,
                        "source": source,
                        "target": target,
                        "type": edge_type,
                        "properties": properties
                    })

        return {
            "nodes": nodes,
            "links": links
        }
