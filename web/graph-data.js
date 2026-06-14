// Mock Knowledge Graph Data representing a professional and social network.
// This data is shared across Neo4j (Nodes & Relationships) and Gremlin (Vertices & Edges) views.

window.KNOWLEDGE_GRAPH_DATA = {
  nodes: [
    { id: "alice", label: "Person", name: "Alice", age: 28, properties: { age: 28, role: "Lead Engineer" } },
    { id: "bob", label: "Person", name: "Bob", age: 35, properties: { age: 35, role: "Product Manager" } },
    { id: "charlie", label: "Person", name: "Charlie", age: 32, properties: { age: 32, role: "Senior Scientist" } },
    { id: "ny", label: "City", name: "New York", properties: { population: "8.4M", country: "USA" } },
    { id: "sf", label: "City", name: "San Francisco", properties: { population: "880K", country: "USA" } },
    { id: "acme", label: "Company", name: "Acme Corp", properties: { industry: "Tech", founded: 2015 } },
    { id: "stark", label: "Company", name: "Stark Industries", properties: { industry: "Aerospace", founded: 1963 } }
  ],
  links: [
    { id: "e1", source: "alice", target: "ny", type: "LIVES_IN", properties: { since: 2018 } },
    { id: "e2", source: "bob", target: "sf", type: "LIVES_IN", properties: { since: 2021 } },
    { id: "e3", source: "charlie", target: "ny", type: "LIVES_IN", properties: { since: 2015 } },
    { id: "e4", source: "alice", target: "stark", type: "WORKS_AT", properties: { role: "Lead Engineer", salary: "$160k" } },
    { id: "e5", source: "bob", target: "acme", type: "WORKS_AT", properties: { role: "Product Manager", salary: "$140k" } },
    { id: "e6", source: "charlie", target: "stark", type: "WORKS_AT", properties: { role: "Senior Scientist", salary: "$150k" } },
    { id: "e7", source: "stark", target: "ny", type: "HQ_IN", properties: { building: "Stark Tower" } },
    { id: "e8", source: "acme", target: "sf", type: "HQ_IN", properties: { building: "Acme HQ" } },
    { id: "e9", source: "alice", target: "bob", type: "KNOWS", properties: { since: 2020, strength: "Close" } },
    { id: "e10", source: "bob", target: "charlie", type: "KNOWS", properties: { since: 2022, strength: "Professional" } }
  ]
};

// Simulation definitions for query/traversal visualizations.
// Each step highlights specific nodes and links after a delay.
window.GRAPH_SIMULATIONS = {
  // Neo4j Cypher MATCH (p:Person)-[:LIVES_IN]->(c:City) MATCH (com:Company)-[:HQ_IN]->(c)
  cypher_match: [
    {
      description: "Match all Person nodes living in a City",
      highlightNodes: ["alice", "bob", "charlie", "ny", "sf"],
      highlightLinks: ["e1", "e2", "e3"]
    },
    {
      description: "Match all Companies headquartered in those same Cities",
      highlightNodes: ["alice", "bob", "charlie", "ny", "sf", "stark", "acme"],
      highlightLinks: ["e1", "e2", "e3", "e7", "e8"]
    }
  ],

  // Gremlin Traversal: g.V().hasLabel("Person").out("LIVES_IN")
  gremlin_simple_traverse: [
    {
      description: "g.V().hasLabel('Person'): Find all starting Person vertices",
      highlightNodes: ["alice", "bob", "charlie"],
      highlightLinks: []
    },
    {
      description: ".out('LIVES_IN'): Traverse outgoing LIVES_IN edges to City vertices",
      highlightNodes: ["alice", "bob", "charlie", "ny", "sf"],
      highlightLinks: ["e1", "e2", "e3"]
    }
  ],

  // Ingestion: CREATE / addV
  op_insert_node: [
    {
      description: "Create new entity 'Dave' (Person)",
      tempNode: { id: "dave", label: "Person", name: "Dave", properties: { age: 29 } },
      highlightNodes: ["dave"]
    }
  ],

  // Ingestion: CREATE relationship / addE
  op_insert_edge: [
    {
      description: "Create edge KNOWS from Alice to Charlie",
      tempLink: { id: "e_temp", source: "alice", target: "charlie", type: "KNOWS", properties: { since: 2023 } },
      highlightNodes: ["alice", "charlie"],
      highlightLinks: ["e_temp"]
    }
  ],

  // Fetch Node: g.V(<id>) or MATCH (n)
  op_fetch_node: [
    {
      description: "Query and retrieve 'Alice' details",
      highlightNodes: ["alice"],
      highlightLinks: []
    }
  ],

  // Delete Node: DETACH DELETE or drop()
  op_delete_node: [
    {
      description: "Targeting 'Charlie' and its connected relationships for deletion",
      fadeNodes: ["charlie"],
      fadeLinks: ["e3", "e6", "e10"]
    }
  ],

  // Multi-hop Traverse: Bob -> KNOWS -> Charlie -> WORKS_AT -> Stark
  op_traverse_hops: [
    {
      description: "Step 1: Start at Bob",
      highlightNodes: ["bob"],
      highlightLinks: []
    },
    {
      description: "Step 2: Traverse out('KNOWS') to Charlie",
      highlightNodes: ["bob", "charlie"],
      highlightLinks: ["e10"]
    },
    {
      description: "Step 3: Traverse out('WORKS_AT') to Stark Industries",
      highlightNodes: ["bob", "charlie", "stark"],
      highlightLinks: ["e10", "e6"]
    }
  ],

  // Reverse Traverse: City <- LIVES_IN - Person
  op_reverse_traverse: [
    {
      description: "Step 1: Start at 'New York'",
      highlightNodes: ["ny"],
      highlightLinks: []
    },
    {
      description: "Step 2: Traverse in('LIVES_IN') / incoming links to find residents",
      highlightNodes: ["ny", "alice", "charlie"],
      highlightLinks: ["e1", "e3"]
    }
  ]
};
