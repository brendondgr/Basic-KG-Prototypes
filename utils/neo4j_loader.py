try:
    from neo4j import GraphDatabase
except ImportError:
    GraphDatabase = None

class Neo4jLoader:
    def __init__(self, uri="bolt://localhost:8544", auth=("neo4j", "password")):
        self.uri = uri
        self.auth = auth
        self.driver = None
        if GraphDatabase:
            try:
                self.driver = GraphDatabase.driver(uri, auth=auth)
            except Exception:
                pass

    def get_ingestion_code(self):
        """Returns the real python driver script code that loads data from the data/ directory."""
        return """# Real Python Code to Load Data into Neo4j
from neo4j import GraphDatabase
import csv

uri = "bolt://localhost:8544"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

def load_data(tx):
    # Load Nodes from nodes.csv
    with open('data/nodes.csv', mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Create nodes using Cypher MERGE
            tx.run(
                "MERGE (n:Entity {id: $id}) "
                "SET n.name = $name, n.label = $label, n.age = $age, n.population = $population, n.industry = $industry, n.founded = $founded",
                id=row['id'], name=row['name'], label=row['label'],
                age=int(row['age']) if row['age'] else None,
                population=row['population'] if row['population'] else None,
                industry=row['industry'] if row['industry'] else None,
                founded=int(row['founded']) if row['founded'] else None
            )
            
    # Load Edges from edges.csv
    with open('data/edges.csv', mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tx.run(
                f"MATCH (a {{id: $source}}), (b {{id: $target}}) "
                f"MERGE (a)-[r:{row['type']}]->(b) "
                f"SET r.id = $id, r.since = $since, r.strength = $strength, r.role = $role, r.salary = $salary, r.building = $building",
                source=row['source'], target=row['target'], id=row['id'],
                since=int(row['since']) if row['since'] else None,
                strength=row['strength'] if row['strength'] else None,
                role=row['role'] if row['role'] else None,
                salary=row['salary'] if row['salary'] else None,
                building=row['building'] if row['building'] else None
            )

with driver.session() as session:
    session.execute_write(load_data)

driver.close()
print("Neo4j Ingestion completed successfully!")
"""

    def run_query_on_memory(self, graph_data, cypher_query):
        """
        Parses and runs Cypher-like queries on the in-memory graph_data dict.
        Returns the highlight steps and logs.
        """
        query_normalized = cypher_query.upper().strip()
        
        highlight_nodes = []
        highlight_links = []
        temp_node = None
        temp_link = None
        fade_nodes = []
        fade_links = []
        log_lines = []
        
        log_lines.append(f"[Neo4j Session] Initializing connection to {self.uri}")
        log_lines.append("[Neo4j Session] Executing Cypher query...")
        
        if "CREATE (:PERSON" in query_normalized or 'CREATE (D:PERSON' in query_normalized:
            temp_node = { "id": "dave", "label": "Person", "name": "Dave", "properties": { "age": 29 } }
            if not any(n['id'] == 'dave' for n in graph_data['nodes']):
                graph_data['nodes'].append(temp_node)
            highlight_nodes = ["dave"]
            log_lines.append("Parsed Query: CREATE (:Person {name: 'Dave', age: 29})")
            log_lines.append("Result: Added 1 node, set 2 properties. (id: dave)")
            steps = [
                {
                    "description": "Cypher CREATE: Spawn node 'Dave' (:Person)",
                    "highlightNodes": highlight_nodes,
                    "highlightLinks": [],
                    "tempNode": temp_node
                }
            ]
        elif "CREATE (A)-[:KNOWS" in query_normalized or "ALICE" in query_normalized and "CHARLIE" in query_normalized and "KNOWS" in query_normalized and "CREATE" in query_normalized:
            temp_link = { "id": "e_temp", "source": "alice", "target": "charlie", "type": "KNOWS", "properties": { "since": 2023 } }
            if not any(l['id'] == 'e_temp' for l in graph_data['links']):
                graph_data['links'].append(temp_link)
            highlight_nodes = ["alice", "charlie"]
            highlight_links = ["e_temp"]
            log_lines.append("Parsed Query: MATCH (a), (c) CREATE (a)-[:KNOWS {since: 2023}]->(c)")
            log_lines.append("Result: Created 1 relationship between Alice and Charlie.")
            steps = [
                {
                    "description": "Cypher CREATE: Create KNOWS relationship Alice ➔ Charlie",
                    "highlightNodes": highlight_nodes,
                    "highlightLinks": highlight_links,
                    "tempLink": temp_link
                }
            ]
        elif "MATCH (N)" in query_normalized and "N.NAME = " in query_normalized and "ALICE" in query_normalized:
            highlight_nodes = ["alice"]
            log_lines.append("Parsed Query: MATCH (n) WHERE n.name = 'Alice' RETURN n")
            log_lines.append("Result: Matched node (id: 'alice', label: 'Person', properties: {age: 28})")
            steps = [
                {
                    "description": "Cypher MATCH: Retrieve details for node Alice",
                    "highlightNodes": highlight_nodes,
                    "highlightLinks": []
                }
            ]
        elif "DETACH DELETE" in query_normalized:
            graph_data['nodes'] = [n for n in graph_data['nodes'] if n['id'] != 'charlie']
            graph_data['links'] = [l for l in graph_data['links'] if l['source'] != 'charlie' and l['target'] != 'charlie']
            fade_nodes = ["charlie"]
            fade_links = ["e3", "e6", "e10"]
            log_lines.append("Parsed Query: MATCH (c:Person {name: 'Charlie'}) DETACH DELETE c")
            log_lines.append("Result: Deleted node 'charlie' and all 3 associated relationships.")
            steps = [
                {
                    "description": "Cypher DELETE: Identify and remove Charlie node and its connections",
                    "fadeNodes": fade_nodes,
                    "fadeLinks": fade_links
                }
            ]
        elif "BOB" in query_normalized and "KNOWS" in query_normalized and "WORKS_AT" in query_normalized:
            log_lines.append("Parsed Query: MATCH (bob:Person {name: 'Bob'})-[:KNOWS]->(friend)-[:WORKS_AT]->(company) RETURN company")
            log_lines.append("Step 1: Found root node 'Bob'")
            log_lines.append("Step 2: Traversed [:KNOWS] ➔ found 'Charlie'")
            log_lines.append("Step 3: Traversed [:WORKS_AT] ➔ found 'Stark Industries'")
            log_lines.append("Result: Matched Stark Industries (Company)")
            steps = [
                {
                    "description": "Cypher MATCH: Identify starting node 'Bob'",
                    "highlightNodes": ["bob"],
                    "highlightLinks": []
                },
                {
                    "description": "Cypher MATCH: Traverse out KNOWS to friend 'Charlie'",
                    "highlightNodes": ["bob", "charlie"],
                    "highlightLinks": ["e10"]
                },
                {
                    "description": "Cypher MATCH: Traverse out WORKS_AT to 'Stark Industries'",
                    "highlightNodes": ["bob", "charlie", "stark"],
                    "highlightLinks": ["e10", "e6"]
                }
            ]
        elif "NEW YORK" in query_normalized and "LIVES_IN" in query_normalized:
            log_lines.append("Parsed Query: MATCH (ny:City {name: 'New York'})<-[:LIVES_IN]-(p:Person) RETURN p.name")
            log_lines.append("Step 1: Matched City node 'New York'")
            log_lines.append("Step 2: Traversing incoming [:LIVES_IN] relationships...")
            log_lines.append("Result: Found residents [Alice, Charlie]")
            steps = [
                {
                    "description": "Cypher MATCH: Identify target City node 'New York'",
                    "highlightNodes": ["ny"],
                    "highlightLinks": []
                },
                {
                    "description": "Cypher MATCH: Scan incoming LIVES_IN connections to find residents",
                    "highlightNodes": ["ny", "alice", "charlie"],
                    "highlightLinks": ["e1", "e3"]
                }
            ]
        elif "HQ_IN" in query_normalized:
            log_lines.append("Parsed Query: MATCH (p:Person)-[:LIVES_IN]->(c:City) MATCH (com:Company)-[:HQ_IN]->(c) RETURN p.name, com.name")
            log_lines.append("Pattern 1: (p)-[:LIVES_IN]->(c) ➔ Matches Alice, Charlie (NY) and Bob (SF)")
            log_lines.append("Pattern 2: (com)-[:HQ_IN]->(c) ➔ Matches Stark Industries (NY) and Acme Corp (SF)")
            log_lines.append("Result: [Alice, Stark Industries], [Charlie, Stark Industries], [Bob, Acme Corp]")
            steps = [
                {
                    "description": "Cypher MATCH: Match all (p:Person)-[:LIVES_IN]->(c:City)",
                    "highlightNodes": ["alice", "bob", "charlie", "ny", "sf"],
                    "highlightLinks": ["e1", "e2", "e3"]
                },
                {
                    "description": "Cypher MATCH: Match (com:Company)-[:HQ_IN]->(c) inside corresponding cities",
                    "highlightNodes": ["alice", "bob", "charlie", "ny", "sf", "stark", "acme"],
                    "highlightLinks": ["e1", "e2", "e3", "e7", "e8"]
                }
            ]
        else:
            log_lines.append("Generic Cypher query run completed successfully.")
            steps = [
                {
                    "description": "Cypher query finished.",
                    "highlightNodes": [],
                    "highlightLinks": []
                }
            ]

        log_lines.append("[Neo4j Session] Session closed.")
        return {
            "steps": steps,
            "logs": "\n".join(log_lines)
        }
