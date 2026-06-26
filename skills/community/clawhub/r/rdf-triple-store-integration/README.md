# RDF Triple Store Integration

> Connect to RDF triple stores to query, manage, and analyze semantic knowledge graphs using SPARQL

## Directory Structure

```
rdf-tripple-store-integration/
├── README.md                      (This file - Quick reference)
├── SKILL.md                       (Skill definition with examples & best practices)
├── examples/
│   └── rdf-tripple-examples.md    (5 complete production examples)
├── references/
│   └── rdf-sparql-patterns.md     (30+ design patterns for SPARQL)
└── scripts/
    └── rdf_store_connector.py     (Production-ready Python implementation)
```

## Quick Start

### Installation

```bash
pip install rdflib sparqlwrapper
```

### Basic Connection

```python
from rdf_store_connector import RDFStoreConnector, ConnectionConfig

# Configure connection
config = ConnectionConfig(
    endpoint="http://localhost:3030/dataset/sparql",
    update_endpoint="http://localhost:3030/dataset/update"
)

# Create connector
connector = RDFStoreConnector()
connector.connect(config)

# Execute SPARQL query
result = connector.execute_query("""
    SELECT ?person ?name
    WHERE {
        ?person rdf:type ex:Person .
        ?person foaf:name ?name .
    }
    LIMIT 10
""")
print(result.records)

# Cleanup
connector.close()
```

## Features

✅ **Connection Management**
- SPARQL endpoint connectivity
- HTTP protocol support
- Connection pooling
- Authentication support

✅ **SPARQL Query Execution**
- Execute SELECT queries
- Execute CONSTRUCT queries
- Execute ASK queries
- Execute DESCRIBE queries
- Parameter binding for safety
- Result mapping to Python objects
- Error handling and status tracking

✅ **Triple Management**
- Insert triples (INSERT DATA)
- Update triples (DELETE/INSERT)
- Delete triples (DELETE WHERE)
- Batch operations
- Graph management (named graphs)

✅ **SPARQL Updates**
- Modify RDF data
- Transaction support
- Batch updates
- Rollback on error

✅ **Named Graphs**
- Create and manage named graphs
- Query specific graphs
- Graph inference
- Graph listing

✅ **Advanced Features**
- Reasoning/inference
- Ontology support (OWL, RDFS)
- SPARQL federation
- Statistics and monitoring

## Key Concepts

### RDF (Resource Description Framework)
- Triple-based data model
- Subject → Predicate → Object structure
- Resources identified by URIs
- Foundation of semantic web

### Triples
- Basic unit of RDF data
- Example: `<http://example.com/alice> <http://foaf.com/knows> <http://example.com/bob>`
- Subject, Predicate, Object

### SPARQL (SPARQL Protocol and RDF Query Language)
- Query language for RDF
- Supports SELECT, CONSTRUCT, ASK, DESCRIBE
- Pattern matching on triples
- Variable binding with ?variable

### Ontologies
- OWL (Web Ontology Language)
- RDFS (RDF Schema)
- Define classes, properties, constraints
- Enable reasoning and inference

### Named Graphs
- Collections of RDF triples
- Each triple associated with a graph URI
- Enable multi-dataset management
- Facilitate access control

## File Descriptions

| File | Purpose | Size |
|------|---------|------|
| README.md | Quick reference and getting started | This file |
| SKILL.md | Complete skill definition | 350+ lines |
| examples/rdf-tripple-examples.md | 5 production domain examples | 500+ lines |
| references/rdf-sparql-patterns.md | 30+ design patterns | 450+ lines |
| scripts/rdf_store_connector.py | Production Python implementation | 500+ lines |

## Common Use Cases

### 1. Semantic Knowledge Graphs
Query and manage knowledge organized using ontologies

### 2. Linked Open Data Integration
Work with linked data from DBpedia, Wikidata, etc.

### 3. Ontology-Based Applications
Build applications that leverage OWL ontologies

### 4. Enterprise Data Integration
Integrate diverse data sources using RDF

### 5. AI/ML Knowledge Representation
Represent knowledge for ML systems

## Integration Points

This skill integrates with:
- **Neo4j Integration** - Property graphs vs RDF graphs
- **Graph Query Optimization** - Optimize SPARQL queries
- **CSV Graph Loader** - Import CSV as RDF
- **REST API Wrapper** - Expose SPARQL as REST API
- **Ontology-Based Inference** - Leverage ontology reasoning
- **JanusGraph Connector** - Alternative graph database

## Quick Examples

### Query all entities of a type
```sparql
SELECT ?entity ?label
WHERE {
    ?entity rdf:type ex:Person .
    ?entity rdfs:label ?label .
}
```

### Insert a triple
```python
connector.insert_triple(
    subject="http://example.com/alice",
    predicate="http://foaf.com/knows",
    object="http://example.com/bob"
)
```

### Update data
```python
connector.update_data(
    delete_pattern="?s ex:age ?old_age",
    insert_pattern="?s ex:age ?new_age",
    where_clause="?s ex:age 30"
)
```

### Query with named graph
```sparql
SELECT ?s ?p ?o
FROM NAMED <http://example.com/graph1>
WHERE {
    GRAPH <http://example.com/graph1> {
        ?s ?p ?o
    }
}
```

### SPARQL federation
```sparql
SELECT ?s ?p ?o
WHERE {
    SERVICE <http://other-endpoint.com/sparql> {
        ?s ?p ?o
    }
}
```

## Performance Tips

1. **Use Filters** - Filter early in SPARQL queries
2. **Limit Results** - Add LIMIT clause to prevent large result sets
3. **Use Named Graphs** - Organize data into named graphs
4. **Create Indexes** - Index frequently queried predicates
5. **Batch Operations** - Group inserts into transactions
6. **Avoid Expensive Joins** - Minimize triple pattern joins

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection refused | Verify SPARQL endpoint is running and accessible |
| Query timeout | Add LIMIT, reduce pattern complexity, use named graphs |
| Memory errors | Limit result sets, use OFFSET/LIMIT for pagination |
| Invalid SPARQL | Validate syntax, use SPARQL validator tools |
| Authentication failed | Check credentials, verify auth headers |

## Related Documentation

- See **SKILL.md** for complete skill definition
- See **examples/rdf-tripple-examples.md** for detailed domain examples
- See **references/rdf-sparql-patterns.md** for design patterns
- See **scripts/rdf_store_connector.py** for implementation details

## Next Steps

1. Review the SKILL.md for comprehensive documentation
2. Check examples/rdf-tripple-examples.md for your use case
3. Look at references/rdf-sparql-patterns.md for design patterns
4. Use scripts/rdf_store_connector.py as reference implementation

---

**Status:** ✅ Production Ready | **Version:** 1.0.0 | **Last Updated:** April 12, 2026

