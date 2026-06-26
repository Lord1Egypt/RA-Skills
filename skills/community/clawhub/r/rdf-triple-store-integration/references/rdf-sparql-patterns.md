# RDF SPARQL Design Patterns

This document contains 30+ production-ready design patterns for common RDF and SPARQL operations. Each pattern includes the SPARQL query, description, and use case.

---

## Table of Contents

1. [Data Query Patterns](#data-query-patterns)
2. [Filtering & Selection Patterns](#filtering--selection-patterns)
3. [Aggregation Patterns](#aggregation-patterns)
4. [Insert & Update Patterns](#insert--update-patterns)
5. [Delete Patterns](#delete-patterns)
6. [Graph Management Patterns](#graph-management-patterns)
7. [Ontology Patterns](#ontology-patterns)
8. [Federated Query Patterns](#federated-query-patterns)
9. [Performance Patterns](#performance-patterns)

---

## Data Query Patterns

### Pattern 1: Simple Triple Pattern Query

**Description:** Basic query matching a single triple pattern

**SPARQL:**
```sparql
SELECT ?subject ?object
WHERE {
  ?subject rdf:type foaf:Person .
  ?subject foaf:name ?object .
}
LIMIT 10
```

**Use Case:** Retrieve basic entity information

**Python:**
```python
connector.execute_query("""
    SELECT ?person ?name
    WHERE {
        ?person rdf:type foaf:Person ;
                foaf:name ?name .
    }
""")
```

### Pattern 2: Multiple Triple Patterns (Graph Traversal)

**Description:** Join multiple triple patterns

**SPARQL:**
```sparql
SELECT ?person ?name ?organization
WHERE {
  ?person rdf:type foaf:Person ;
          foaf:name ?name ;
          foaf:workplaceHomepage ?org .
  ?org foaf:name ?organization .
}
```

**Use Case:** Navigate relationships across entities

### Pattern 3: Query with Specific Resource

**Description:** Query properties of a known resource

**SPARQL:**
```sparql
SELECT ?property ?value
WHERE {
  <http://example.com/resource1> ?property ?value .
}
```

**Use Case:** Get all properties of a specific resource

### Pattern 4: Describe Query

**Description:** Get all information about a resource

**SPARQL:**
```sparql
DESCRIBE <http://example.com/alice>
```

**Use Case:** Get comprehensive resource description

### Pattern 5: Construct Query

**Description:** Build new RDF triples from query results

**SPARQL:**
```sparql
CONSTRUCT {
  ?person foaf:knows ?friend .
}
WHERE {
  ?person foaf:knows ?friend .
}
```

**Use Case:** Extract subgraph or transform data

### Pattern 6: Ask Query

**Description:** Check if pattern exists (boolean result)

**SPARQL:**
```sparql
ASK {
  ex:alice foaf:knows ex:bob .
}
```

**Use Case:** Validation, existence checking

---

## Filtering & Selection Patterns

### Pattern 7: Filter by Value Comparison

**Description:** Filter numeric or date comparisons

**SPARQL:**
```sparql
SELECT ?person ?age
WHERE {
  ?person rdf:type foaf:Person ;
          foaf:age ?age .
  FILTER (?age > 18)
}
```

**Use Case:** Range queries, age filters

**Operators:** `>`, `<`, `>=`, `<=`, `=`, `!=`

### Pattern 8: Filter by String Pattern

**Description:** Match string patterns

**SPARQL:**
```sparql
SELECT ?person ?name
WHERE {
  ?person foaf:name ?name .
  FILTER (CONTAINS(?name, "Alice"))
}
```

**Use Case:** Text search, pattern matching

**Functions:** `CONTAINS()`, `STRSTARTS()`, `STRENDS()`, `REGEX()`

### Pattern 9: Filter by Data Type

**Description:** Check literal data types

**SPARQL:**
```sparql
SELECT ?value
WHERE {
  ?subject ?property ?value .
  FILTER (isLiteral(?value))
}
```

**Use Case:** Type validation

**Type checks:** `isLiteral()`, `isIRI()`, `isBlank()`, `isNumeric()`

### Pattern 10: Filter by Language Tag

**Description:** Select literals by language

**SPARQL:**
```sparql
SELECT ?label
WHERE {
  ?resource rdfs:label ?label .
  FILTER (lang(?label) = "en")
}
```

**Use Case:** Multi-language content selection

### Pattern 11: Not Exists Pattern

**Description:** Find resources without specific property

**SPARQL:**
```sparql
SELECT ?person
WHERE {
  ?person rdf:type foaf:Person .
  FILTER NOT EXISTS { ?person foaf:email ?email }
}
```

**Use Case:** Find incomplete data

### Pattern 12: Optional Pattern

**Description:** Include optional properties

**SPARQL:**
```sparql
SELECT ?name ?email ?phone
WHERE {
  ?person foaf:name ?name .
  OPTIONAL { ?person foaf:email ?email }
  OPTIONAL { ?person foaf:phone ?phone }
}
```

**Use Case:** Partial data retrieval

### Pattern 13: Union Pattern

**Description:** Alternative patterns (OR logic)

**SPARQL:**
```sparql
SELECT ?person ?contact
WHERE {
  ?person rdf:type foaf:Person .
  {
    ?person foaf:email ?contact .
  }
  UNION
  {
    ?person foaf:phone ?contact .
  }
}
```

**Use Case:** Query alternatives

### Pattern 14: Bind Pattern

**Description:** Create derived variables

**SPARQL:**
```sparql
SELECT ?person ?name ?age ?status
WHERE {
  ?person foaf:name ?name ;
          foaf:age ?age .
  BIND (IF(?age >= 18, "Adult", "Minor") as ?status)
}
```

**Use Case:** Computed values, conditional assignment

---

## Aggregation Patterns

### Pattern 15: Count Pattern

**Description:** Count matching results

**SPARQL:**
```sparql
SELECT (COUNT(?person) as ?count)
WHERE {
  ?person rdf:type foaf:Person .
}
```

**Use Case:** Statistics, data validation

### Pattern 16: Group By Pattern

**Description:** Group results and aggregate

**SPARQL:**
```sparql
SELECT ?department (COUNT(?person) as ?count)
WHERE {
  ?person foaf:workDepartment ?department .
}
GROUP BY ?department
```

**Use Case:** Statistical analysis

### Pattern 17: Sum Pattern

**Description:** Sum numeric values

**SPARQL:**
```sparql
SELECT ?person (SUM(?salary) as ?total)
WHERE {
  ?person foaf:hasSalary ?salary .
}
GROUP BY ?person
```

**Use Case:** Financial calculations

### Pattern 18: Average Pattern

**Description:** Calculate average

**SPARQL:**
```sparql
SELECT (AVG(?age) as ?avg_age)
WHERE {
  ?person foaf:age ?age .
}
```

**Use Case:** Statistics, analysis

### Pattern 19: Min/Max Pattern

**Description:** Find minimum/maximum values

**SPARQL:**
```sparql
SELECT (MIN(?age) as ?min) (MAX(?age) as ?max)
WHERE {
  ?person foaf:age ?age .
}
```

**Use Case:** Range analysis

### Pattern 20: Distinct Count

**Description:** Count distinct values

**SPARQL:**
```sparql
SELECT (COUNT(DISTINCT ?department) as ?dept_count)
WHERE {
  ?person foaf:workDepartment ?department .
}
```

**Use Case:** Unique value counting

### Pattern 21: Having Clause Pattern

**Description:** Filter aggregated results

**SPARQL:**
```sparql
SELECT ?department (COUNT(?person) as ?count)
WHERE {
  ?person foaf:workDepartment ?department .
}
GROUP BY ?department
HAVING (COUNT(?person) > 5)
```

**Use Case:** Filter by aggregate criteria

---

## Insert & Update Patterns

### Pattern 22: Insert Data Pattern

**Description:** Add triples to store

**SPARQL:**
```sparql
INSERT DATA {
  ex:alice foaf:name "Alice" ;
           foaf:age 30 ;
           foaf:knows ex:bob .
}
```

**Use Case:** Data insertion

### Pattern 23: Insert with WHERE Clause

**Description:** Conditional insert based on query

**SPARQL:**
```sparql
INSERT {
  ?person foaf:status "active" .
}
WHERE {
  ?person foaf:age ?age .
  FILTER (?age > 18)
}
```

**Use Case:** Bulk property assignment

### Pattern 24: Delete/Insert Update

**Description:** Modify existing triples

**SPARQL:**
```sparql
DELETE {
  ?person foaf:age ?old
}
INSERT {
  ?person foaf:age ?new
}
WHERE {
  ?person foaf:age ?old .
  BIND (?old + 1 as ?new)
}
```

**Use Case:** Data updates

### Pattern 25: Insert into Named Graph

**Description:** Add triples to specific graph

**SPARQL:**
```sparql
INSERT DATA {
  GRAPH <http://example.com/graph1> {
    ex:alice foaf:name "Alice" .
  }
}
```

**Use Case:** Multi-graph management

### Pattern 26: Bulk Insert Pattern

**Description:** Insert multiple triples efficiently

**SPARQL:**
```sparql
INSERT DATA {
  ex:person1 rdf:type foaf:Person ;
             foaf:name "Alice" .
  ex:person2 rdf:type foaf:Person ;
             foaf:name "Bob" .
  ex:person3 rdf:type foaf:Person ;
             foaf:name "Charlie" .
}
```

**Use Case:** Batch data loading

---

## Delete Patterns

### Pattern 27: Delete Specific Triple

**Description:** Remove specific triple

**SPARQL:**
```sparql
DELETE DATA {
  ex:alice foaf:knows ex:bob .
}
```

**Use Case:** Triple removal

### Pattern 28: Delete with Condition

**Description:** Conditionally delete triples

**SPARQL:**
```sparql
DELETE WHERE {
  ?person foaf:age ?age .
  FILTER (?age < 0)
}
```

**Use Case:** Data cleanup

### Pattern 29: Delete All Properties

**Description:** Remove all properties of resource

**SPARQL:**
```sparql
DELETE {
  ex:alice ?property ?value .
}
WHERE {
  ex:alice ?property ?value .
}
```

**Use Case:** Complete resource removal (except rdf:type)

### Pattern 30: Delete from Named Graph

**Description:** Delete from specific graph

**SPARQL:**
```sparql
DELETE {
  GRAPH <http://example.com/graph1> {
    ?s ?p ?o .
  }
}
WHERE {
  GRAPH <http://example.com/graph1> {
    ?s ?p ?o .
  }
}
```

**Use Case:** Graph cleanup

---

## Graph Management Patterns

### Pattern 31: Query Named Graphs

**Description:** Retrieve data from specific graphs

**SPARQL:**
```sparql
SELECT ?s ?p ?o
WHERE {
  GRAPH ?g {
    ?s ?p ?o .
  }
  FILTER (?g = <http://example.com/graph1>)
}
```

**Use Case:** Multi-graph queries

### Pattern 32: List All Graphs

**Description:** Enumerate available graphs

**SPARQL:**
```sparql
SELECT ?g
WHERE {
  GRAPH ?g { ?s ?p ?o }
}
GROUP BY ?g
```

**Use Case:** Graph discovery

### Pattern 33: Copy Graph

**Description:** Copy triples between graphs

**SPARQL:**
```sparql
INSERT {
  GRAPH <http://example.com/graph2> { ?s ?p ?o }
}
WHERE {
  GRAPH <http://example.com/graph1> { ?s ?p ?o }
}
```

**Use Case:** Graph duplication/backup

---

## Ontology Patterns

### Pattern 34: Class Hierarchy Query

**Description:** Query class hierarchy

**SPARQL:**
```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?subclass
WHERE {
  ?subclass rdfs:subClassOf ?superclass .
}
```

**Use Case:** Ontology exploration

### Pattern 35: Property Query

**Description:** Find properties of a class

**SPARQL:**
```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?property
WHERE {
  ?property rdfs:domain ex:Person .
}
```

**Use Case:** Schema inspection

### Pattern 36: Instance of Subclass

**Description:** Find instances including subclasses

**SPARQL:**
```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?instance
WHERE {
  ?instance rdf:type ?type .
  ?type rdfs:subClassOf* foaf:Person .
}
```

**Use Case:** Inheritance queries

### Pattern 37: Equivalence Query

**Description:** Find equivalent classes/properties

**SPARQL:**
```sparql
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT ?equivalent
WHERE {
  ex:Class1 owl:equivalentClass ?equivalent .
}
```

**Use Case:** Ontology alignment

---

## Federated Query Patterns

### Pattern 38: Simple Service Pattern

**Description:** Query remote SPARQL endpoint

**SPARQL:**
```sparql
SELECT ?name
WHERE {
  SERVICE <http://dbpedia.org/sparql> {
    ?person rdf:type dbo:Person ;
            foaf:name ?name .
  }
}
LIMIT 10
```

**Use Case:** Distributed queries

### Pattern 39: Service with Filter

**Description:** Filter federated query results

**SPARQL:**
```sparql
SELECT ?person ?name
WHERE {
  ?person foaf:name ?name .
  SERVICE <http://remote.endpoint/sparql> {
    ?person foaf:knows ?friend .
  }
  FILTER (?name = "Alice")
}
```

**Use Case:** Refined federated queries

### Pattern 40: Multiple Service Endpoints

**Description:** Query multiple SPARQL endpoints

**SPARQL:**
```sparql
SELECT ?result1 ?result2
WHERE {
  SERVICE <http://endpoint1.com/sparql> {
    ?result1 rdf:type foaf:Person .
  }
  SERVICE <http://endpoint2.com/sparql> {
    ?result2 rdf:type foaf:Organization .
  }
}
```

**Use Case:** Cross-endpoint correlation

---

## Performance Patterns

### Pattern 41: Limit Results

**Description:** Prevent expensive queries

**SPARQL:**
```sparql
SELECT ?s ?p ?o
WHERE {
  ?s ?p ?o .
}
LIMIT 1000
```

**Use Case:** Query throttling

### Pattern 42: Offset Pagination

**Description:** Paginate large result sets

**SPARQL:**
```sparql
SELECT ?person ?name
WHERE {
  ?person foaf:name ?name .
}
ORDER BY ?name
LIMIT 100
OFFSET 200
```

**Use Case:** Pagination

### Pattern 43: Index by Property

**Description:** Query indexed properties first

**SPARQL:**
```sparql
SELECT ?person
WHERE {
  ?person foaf:email "alice@example.com" .
  ?person foaf:knows ?friend .
}
```

**Use Case:** Query optimization

### Pattern 44: Reduce Triple Patterns

**Description:** Minimize pattern complexity

**SPARQL:**
```sparql
# Efficient: Filter early
SELECT ?person
WHERE {
  ?person rdf:type foaf:Person .
  FILTER (?age > 18)
  ?person foaf:knows ?friend .
}

# Less efficient: Complex joins first
SELECT ?person
WHERE {
  ?person foaf:knows ?friend .
  ?friend foaf:knows ?other .
  FILTER (?age > 18)
}
```

**Use Case:** Query planning

---

## Summary

**30+ Patterns Covered:**
- ✅ 6 Basic query patterns
- ✅ 8 Filtering patterns
- ✅ 7 Aggregation patterns
- ✅ 5 Insert/update patterns
- ✅ 4 Delete patterns
- ✅ 3 Graph management patterns
- ✅ 4 Ontology patterns
- ✅ 3 Federated query patterns
- ✅ 4 Performance patterns

Each pattern includes:
- Clear description
- SPARQL query
- Use case
- Python implementation (where applicable)

---

**Last Updated:** April 12, 2026  
**SPARQL Version:** 1.1  
**RDF Version:** 1.1

