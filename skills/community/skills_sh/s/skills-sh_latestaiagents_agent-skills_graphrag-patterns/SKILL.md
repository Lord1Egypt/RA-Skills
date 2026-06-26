---
name: graphrag-patterns
description: |
  Implement GraphRAG patterns combining knowledge graphs with retrieval for complex reasoning.
  Use this skill when building RAG over interconnected data or needing relationship-aware retrieval.
  Activate when: GraphRAG, knowledge graph, graph retrieval, entity relationships, Neo4j RAG, graph database, connected data.
---

# GraphRAG Patterns

**Combine knowledge graphs with RAG for relationship-aware retrieval and reasoning.**

## When to Use

- Data has rich entity relationships
- Questions involve connections ("How is X related to Y?")
- Need multi-hop reasoning across documents
- Building over structured + unstructured data
- Want explainable retrieval paths

## GraphRAG Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    Documents                              │
└─────────────────────────┬────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
   ┌────────────┐  ┌────────────┐  ┌────────────┐
   │   Entity   │  │   Vector   │  │    Text    │
   │ Extraction │  │ Embeddings │  │   Chunks   │
   └─────┬──────┘  └─────┬──────┘  └─────┬──────┘
         │               │               │
         ▼               │               │
   ┌────────────┐        │               │
   │  Knowledge │        │               │
   │    Graph   │        │               │
   └─────┬──────┘        │               │
         │               │               │
         └───────────────┼───────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │    Hybrid Index     │
              │ (Graph + Vectors)   │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │   Graph-Aware RAG   │
              └─────────────────────┘
```

## Building the Knowledge Graph

### Entity & Relationship Extraction

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

EXTRACTION_PROMPT = """Extract entities and relationships from the text.

Text: {text}

Return JSON:
{{
  "entities": [
    {{"name": "...", "type": "PERSON|ORG|PRODUCT|CONCEPT|...", "description": "..."}}
  ],
  "relationships": [
    {{"source": "...", "target": "...", "type": "WORKS_FOR|USES|RELATED_TO|...", "description": "..."}}
  ]
}}
"""

def extract_graph_elements(text: str) -> dict:
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    prompt = ChatPromptTemplate.from_template(EXTRACTION_PROMPT)
    chain = prompt | llm
    result = chain.invoke({"text": text})
    return json.loads(result.content)
```

### Store in Neo4j

```python
from neo4j import GraphDatabase

class GraphStore:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def add_entity(self, entity: dict):
        with self.driver.session() as session:
            session.run("""
                MERGE (e:Entity {name: $name})
                SET e.type = $type, e.description = $description
                """,
                name=entity["name"],
                type=entity["type"],
                description=entity["description"]
            )

    def add_relationship(self, rel: dict):
        with self.driver.session() as session:
            session.run("""
                MATCH (a:Entity {name: $source})
                MATCH (b:Entity {name: $target})
                MERGE (a)-[r:RELATES {type: $type}]->(b)
                SET r.description = $description
                """,
                source=rel["source"],
                target=rel["target"],
                type=rel["type"],
                description=rel["description"]
            )

    def get_neighbors(self, entity: str, hops: int = 2) -> list:
        with self.driver.session() as session:
            result = session.run("""
                MATCH path = (e:Entity {name: $name})-[*1..$hops]-(related)
                RETURN path
                """,
                name=entity, hops=hops
            )
            return [record["path"] for record in result]
```

## GraphRAG Retrieval Strategies

### 1. Entity-Centric Retrieval

```python
def entity_centric_retrieve(query: str, graph: GraphStore, vectorstore) -> list:
    """Extract entities from query, expand via graph, retrieve chunks."""

    # Extract entities from query
    entities = extract_entities(query)

    # Get graph neighbors
    expanded_entities = set(entities)
    for entity in entities:
        neighbors = graph.get_neighbors(entity, hops=2)
        expanded_entities.update(neighbors)

    # Retrieve chunks mentioning these entities
    chunks = []
    for entity in expanded_entities:
        results = vectorstore.similarity_search(
            entity,
            k=3,
            filter={"entities": {"$contains": entity}}
        )
        chunks.extend(results)

    return deduplicate(chunks)
```

### 2. Path-Based Retrieval

```python
def path_retrieve(query: str, entity_a: str, entity_b: str, graph: GraphStore) -> str:
    """Find and explain paths between entities."""

    with graph.driver.session() as session:
        result = session.run("""
            MATCH path = shortestPath(
                (a:Entity {name: $entity_a})-[*..5]-(b:Entity {name: $entity_b})
            )
            RETURN path, length(path) as hops
            ORDER BY hops
            LIMIT 5
            """,
            entity_a=entity_a, entity_b=entity_b
        )

        paths = []
        for record in result:
            path = record["path"]
            path_str = " -> ".join([node["name"] for node in path.nodes])
            paths.append(path_str)

    return paths
```

### 3. Community-Based Retrieval (Microsoft GraphRAG)

```python
from graspologic.partition import hierarchical_leiden

def build_communities(graph: GraphStore) -> dict:
    """Detect communities for hierarchical summarization."""

    # Export graph to networkx
    nx_graph = graph.to_networkx()

    # Detect communities at multiple levels
    communities = hierarchical_leiden(nx_graph, max_cluster_size=10)

    # Summarize each community
    community_summaries = {}
    for community_id, members in communities.items():
        member_descriptions = [graph.get_entity(m)["description"] for m in members]
        summary = summarize_community(member_descriptions)
        community_summaries[community_id] = summary

    return community_summaries

def community_retrieve(query: str, community_summaries: dict) -> list:
    """Search community summaries first, then drill down."""

    # Find relevant communities
    relevant = vectorstore.similarity_search(
        query,
        k=3,
        filter={"type": "community_summary"}
    )

    # Get entities from those communities
    entities = []
    for community in relevant:
        entities.extend(community.metadata["members"])

    # Retrieve detailed chunks
    return retrieve_by_entities(entities)
```

## LangChain + Neo4j Integration

```python
from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain

# Connect to Neo4j
graph = Neo4jGraph(
    url="bolt://localhost:7687",
    username="neo4j",
    password="password"
)

# Natural language to Cypher
chain = GraphCypherQAChain.from_llm(
    llm=ChatOpenAI(model="gpt-4"),
    graph=graph,
    verbose=True,
    return_intermediate_steps=True
)

# Query in natural language
result = chain.invoke({
    "query": "Who are the engineers working on Project Atlas?"
})
# Automatically generates: MATCH (p:Person)-[:WORKS_ON]->(proj:Project {name: 'Atlas'}) RETURN p
```

## Hybrid Graph + Vector Pipeline

```python
class GraphRAG:
    def __init__(self, graph: GraphStore, vectorstore, llm):
        self.graph = graph
        self.vectorstore = vectorstore
        self.llm = llm

    def retrieve(self, query: str) -> list:
        # 1. Vector search for initial chunks
        vector_results = self.vectorstore.similarity_search(query, k=10)

        # 2. Extract entities from results
        entities = set()
        for doc in vector_results:
            entities.update(doc.metadata.get("entities", []))

        # 3. Expand via graph
        graph_context = []
        for entity in list(entities)[:5]:  # Limit expansion
            neighbors = self.graph.get_neighbors(entity, hops=1)
            for neighbor in neighbors:
                graph_context.append(f"{entity} -> {neighbor['relationship']} -> {neighbor['name']}")

        # 4. Combine contexts
        return {
            "chunks": vector_results,
            "graph_context": graph_context
        }

    def generate(self, query: str, context: dict) -> str:
        prompt = f"""Answer based on the context.

        Text chunks:
        {self._format_chunks(context['chunks'])}

        Entity relationships:
        {chr(10).join(context['graph_context'])}

        Question: {query}
        """
        return self.llm.invoke(prompt).content
```

## Best Practices

1. **Extract consistently** - use same LLM/prompt for all documents
2. **Normalize entities** - "AWS", "Amazon Web Services" → same node
3. **Limit graph depth** - 2-3 hops usually sufficient
4. **Cache traversals** - graph queries can be expensive
5. **Combine with vectors** - graph alone misses semantic similarity
6. **Version your schema** - entity/relationship types will evolve
