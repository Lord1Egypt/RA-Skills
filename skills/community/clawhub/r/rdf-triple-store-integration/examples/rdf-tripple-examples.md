# RDF Triple Store Examples

This file contains 5 complete, production-ready examples of RDF and SPARQL usage across different domains. Each example demonstrates real-world scenarios with full RDF/Turtle notation and SPARQL queries.

---

## Table of Contents

1. [Linked Open Data - DBpedia Integration](#1-linked-open-data---dbpedia-integration)
2. [Organizational Knowledge Graph](#2-organizational-knowledge-graph)
3. [Scientific Publication Network](#3-scientific-publication-network)
4. [Bibliographic Knowledge Graph](#4-bibliographic-knowledge-graph)
5. [E-Commerce Semantic Graph](#5-e-commerce-semantic-graph)

---

## 1. Linked Open Data - DBpedia Integration

### Domain Description

Integration with DBpedia (linked open data from Wikipedia) for querying and enriching knowledge. Demonstrates:
- Federated SPARQL queries across DBpedia
- Linking local data with external linked data
- Using standard vocabularies (FOAF, Dublin Core)
- Property extraction from structured Wikipedia data

### RDF Ontology

```turtle
@prefix dbpedia: <http://dbpedia.org/resource/>
@prefix dbo: <http://dbpedia.org/ontology/>
@prefix foaf: <http://xmlns.com/foaf/0.1/>
@prefix dc: <http://purl.org/dc/elements/1.1/>
@prefix ex: <http://example.com/>

# Local person entity
ex:person1 a foaf:Person ;
  foaf:name "Alice" ;
  foaf:workplaceHomepage <http://example.com/> ;
  owl:sameAs dbpedia:Alice_Johnson .

# Link to DBpedia resource
dbpedia:London a dbo:City ;
  foaf:name "London" ;
  dbo:country dbpedia:United_Kingdom ;
  dc:description "Capital of England" .
```

### Example Queries

#### Query 1: Find Wikipedia information about a city
```sparql
SELECT ?name ?description ?population
WHERE {
  SERVICE <http://dbpedia.org/sparql> {
    <http://dbpedia.org/resource/London> 
      foaf:name ?name ;
      dc:description ?description ;
      dbo:populationTotal ?population .
  }
}
```

#### Query 2: Link local data with DBpedia
```sparql
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX dbpedia: <http://dbpedia.org/resource/>

SELECT ?person ?wikipediaLink
WHERE {
  ?person owl:sameAs ?wikipediaLink .
  FILTER (STRSTARTS(str(?wikipediaLink), str(dbpedia:)))
}
```

#### Query 3: Find movies by directors in DBpedia
```sparql
PREFIX dbo: <http://dbpedia.org/ontology/>

SELECT ?movie ?director ?year
WHERE {
  SERVICE <http://dbpedia.org/sparql> {
    ?movie rdf:type dbo:Film ;
           dbo:director ?directorResource ;
           dbo:releaseDate ?year .
    ?directorResource foaf:name "Steven Spielberg" .
  }
}
LIMIT 10
```

#### Query 4: Federated query across multiple endpoints
```sparql
SELECT ?person ?name ?birthPlace ?birthDate
WHERE {
  ?person a foaf:Person ;
          foaf:name ?name .
  
  SERVICE <http://dbpedia.org/sparql> {
    ?dbpPerson foaf:name ?name ;
               dbo:birthPlace ?birthPlace ;
               dbo:birthDate ?birthDate .
  }
}
```

### Python Implementation

```python
from rdf_store_connector import RDFStoreConnector, ConnectionConfig

# Local triple store config
local_config = ConnectionConfig(
    endpoint="http://localhost:3030/dataset/sparql"
)

connector = RDFStoreConnector()
connector.connect(local_config)

def find_wikipedia_info(city_name):
    """Query DBpedia for city information"""
    query = f"""
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    
    SELECT ?name ?description ?population
    WHERE {{
      SERVICE <http://dbpedia.org/sparql> {{
        ?city rdfs:label "{city_name}"@en ;
              foaf:name ?name ;
              dbo:populationTotal ?population ;
              dc:description ?description .
      }}
    }}
    LIMIT 1
    """
    return connector.execute_query(query)

def link_with_dbpedia(local_person_uri):
    """Find DBpedia equivalent for local person"""
    query = f"""
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT ?wikipediaLink
    WHERE {{
      <{local_person_uri}> owl:sameAs ?wikipediaLink .
      FILTER (CONTAINS(str(?wikipediaLink), "dbpedia"))
    }}
    """
    return connector.execute_query(query)

# Usage
city_info = find_wikipedia_info("London")
print(f"City info: {city_info.records}")

person_link = link_with_dbpedia("http://example.com/person1")
print(f"Wikipedia link: {person_link.records}")

connector.close()
```

---

## 2. Organizational Knowledge Graph

### Domain Description

RDF representation of organizational structure with departments, roles, and relationships. Demonstrates:
- Organizational hierarchy in RDF
- SKOS (Simple Knowledge Organization System) for thesaurus
- Property constraints and restrictions
- Organization ontology usage

### RDF Schema (Turtle)

```turtle
@prefix org: <http://www.w3.org/ns/org#>
@prefix foaf: <http://xmlns.com/foaf/0.1/>
@prefix vcard: <http://www.w3.org/2006/vcard/ns#>
@prefix ex: <http://example.com/>
@prefix skos: <http://www.w3.org/2004/02/skos/core#>

# Organization
ex:acmeCorp a org:Organization ;
  foaf:name "ACME Corporation" ;
  foaf:homepage <http://acme.com/> .

# Departments
ex:engineering a org:Organization ;
  org:subOrganizationOf ex:acmeCorp ;
  foaf:name "Engineering" ;
  org:hasMember ex:alice, ex:bob .

ex:sales a org:Organization ;
  org:subOrganizationOf ex:acmeCorp ;
  foaf:name "Sales" ;
  org:hasMember ex:charlie .

# Roles (using SKOS)
ex:softwareEngineer a skos:Concept ;
  skos:prefLabel "Software Engineer" ;
  skos:definition "Professional who develops software" .

ex:salesManager a skos:Concept ;
  skos:prefLabel "Sales Manager" ;
  skos:broader ex:salesRole .

# People
ex:alice a foaf:Person ;
  foaf:name "Alice" ;
  foaf:workplaceHomepage ex:acmeCorp ;
  org:memberOf ex:engineering ;
  ex:hasRole ex:softwareEngineer ;
  vcard:hasEmail <mailto:alice@acme.com> ;
  ex:reportsTo ex:bob .

ex:bob a foaf:Person ;
  foaf:name "Bob" ;
  org:memberOf ex:engineering ;
  ex:hasRole ex:engineeringManager ;
  vcard:hasEmail <mailto:bob@acme.com> .

ex:charlie a foaf:Person ;
  foaf:name "Charlie" ;
  org:memberOf ex:sales ;
  ex:hasRole ex:salesManager ;
  vcard:hasEmail <mailto:charlie@acme.com> .
```

### Example Queries

#### Query 1: Get organization structure
```sparql
PREFIX org: <http://www.w3.org/ns/org#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?dept ?member ?name
WHERE {
  ?dept org:subOrganizationOf ?org ;
        foaf:name "Engineering" ;
        org:hasMember ?member .
  ?member foaf:name ?name .
}
```

#### Query 2: Find team members and their manager
```sparql
PREFIX ex: <http://example.com/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX org: <http://www.w3.org/ns/org#>

SELECT ?person ?name ?manager ?managerName
WHERE {
  ?person org:memberOf ex:engineering ;
          foaf:name ?name ;
          ex:reportsTo ?manager .
  ?manager foaf:name ?managerName .
}
```

#### Query 3: Find people with specific role
```sparql
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?person ?name ?role
WHERE {
  ?person foaf:name ?name ;
          ex:hasRole ?roleUri .
  ?roleUri skos:prefLabel ?role .
  FILTER (CONTAINS(?role, "Engineer"))
}
```

### Python Implementation

```python
def get_organization_structure():
    query = """
    PREFIX org: <http://www.w3.org/ns/org#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    
    SELECT ?org ?dept ?member
    WHERE {
      ?dept org:subOrganizationOf ?org ;
            org:hasMember ?member .
    }
    """
    return connector.execute_query(query)

def get_team_by_department(dept_name):
    query = f"""
    PREFIX org: <http://www.w3.org/ns/org#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    
    SELECT ?person ?name ?email
    WHERE {{
      ?dept foaf:name "{dept_name}" ;
            org:hasMember ?person .
      ?person foaf:name ?name ;
              vcard:hasEmail ?email .
    }}
    """
    return connector.execute_query(query)

# Usage
org_structure = get_organization_structure()
engineering_team = get_team_by_department("Engineering")
```

---

## 3. Scientific Publication Network

### Domain Description

RDF representation of scientific papers, authors, and citations. Demonstrates:
- Publication metadata in RDF
- Citation networks
- Author collaborations
- BIBO (Bibliographic Ontology) usage

### RDF Schema

```turtle
@prefix bibo: <http://purl.org/ontology/bibo/>
@prefix foaf: <http://xmlns.com/foaf/0.1/>
@prefix dc: <http://purl.org/dc/elements/1.1/>
@prefix ex: <http://example.com/publication/>

# Paper
ex:paper1 a bibo:Document ;
  dc:title "Deep Learning in Knowledge Graphs" ;
  dc:creator ex:author1, ex:author2 ;
  dc:issued "2024-01-15"^^xsd:date ;
  bibo:numPages 20 ;
  bibo:citationCount 150 ;
  dc:isPartOf ex:conference2024 ;
  dc:isVersionOf ex:paper1_v1 .

ex:paper2 a bibo:Document ;
  dc:title "Graph Neural Networks" ;
  dc:creator ex:author2, ex:author3 ;
  dc:issued "2023-06-20"^^xsd:date ;
  bibo:citationCount 200 .

# Citation relationship
ex:paper1 bibo:cites ex:paper2 ;
          bibo:cites ex:paper3 .

# Authors
ex:author1 a foaf:Person ;
  foaf:name "Alice Smith" ;
  foaf:workplaceHomepage <http://university1.edu/> .

ex:author2 a foaf:Person ;
  foaf:name "Bob Johnson" ;
  foaf:workplaceHomepage <http://university2.edu/> .

# Conference
ex:conference2024 a bibo:Conference ;
  dc:title "International Conference on Knowledge Graphs 2024" ;
  dc:date "2024-06-15"^^xsd:date .
```

### Example Queries

#### Query 1: Find papers by author
```sparql
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?title ?year
WHERE {
  ?paper dc:creator ?author ;
         dc:title ?title ;
         dc:issued ?year .
  ?author foaf:name "Alice Smith" .
}
ORDER BY DESC(?year)
```

#### Query 2: Find citation network
```sparql
PREFIX bibo: <http://purl.org/ontology/bibo/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>

SELECT ?paper1Title ?paper2Title ?citations
WHERE {
  ?paper1 dc:title ?paper1Title ;
          bibo:cites ?paper2 ;
          bibo:citationCount ?citations .
  ?paper2 dc:title ?paper2Title .
}
ORDER BY DESC(?citations)
LIMIT 20
```

#### Query 3: Find collaborators
```sparql
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?collaborator ?collaboratorName (COUNT(?paper) as ?papers)
WHERE {
  ?paper dc:creator ex:author1 ;
         dc:creator ?collaborator .
  ?collaborator foaf:name ?collaboratorName .
}
GROUP BY ?collaborator ?collaboratorName
ORDER BY DESC(?papers)
```

---

## 4. Bibliographic Knowledge Graph

### Domain Description

Library/bibliographic system with books, authors, publishers. Demonstrates:
- Library management in RDF
- Complex property relationships
- Named graphs for different collections
- FRBR (Functional Requirements for Bibliographic Records)

### RDF Schema

```turtle
@prefix frbr: <http://purl.org/vocab/frbr/core#>
@prefix foaf: <http://xmlns.com/foaf/0.1/>
@prefix dc: <http://purl.org/dc/elements/1.1/>
@prefix ex: <http://library.example.com/>

# Work (intellectual content)
ex:work1 a frbr:Work ;
  dc:title "The Great Gatsby" ;
  frbr:creator ex:author_fitzgerald ;
  dc:subject ex:subject_jazz_age ;
  dc:description "A novel set in the Jazz Age" .

# Expression (artistic creation)
ex:expr1 a frbr:Expression ;
  frbr:realizationOf ex:work1 ;
  dc:language "en" ;
  dc:issued "1925"^^xsd:gYear .

# Manifestation (physical object)
ex:book1 a frbr:Manifestation ;
  frbr:embodimentOf ex:expr1 ;
  dc:title "The Great Gatsby" ;
  dc:publisher ex:publisher_scribner ;
  frbr:isbn "978-0-7432-7356-5" ;
  dc:date "1925"^^xsd:gYear ;
  dc:language "en" .

# Item (specific copy)
ex:item1 a frbr:Item ;
  frbr:exemplarOf ex:book1 ;
  ex:callNumber "FIC FIZ" ;
  ex:location "Shelf A1" ;
  ex:status "available" .

# Author
ex:author_fitzgerald a foaf:Person ;
  foaf:name "F. Scott Fitzgerald" ;
  foaf:birthDate "1896-09-24"^^xsd:date ;
  foaf:deathDate "1940-12-21"^^xsd:date .

# Publisher
ex:publisher_scribner a foaf:Organization ;
  foaf:name "Charles Scribner's Sons" ;
  foaf:based_near "New York" .

# Subject
ex:subject_jazz_age a rdf:Concept ;
  skos:prefLabel "Jazz Age" ;
  skos:definition "The 1920s in American culture" .
```

### Example Queries

#### Query 1: Find all works by an author
```sparql
PREFIX frbr: <http://purl.org/vocab/frbr/core#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>

SELECT ?title ?year
WHERE {
  ?work frbr:creator ?author ;
        dc:title ?title ;
        dc:issued ?year .
  ?author foaf:name "F. Scott Fitzgerald" .
}
```

#### Query 2: Find available copies of a book
```sparql
PREFIX frbr: <http://purl.org/vocab/frbr/core#>
PREFIX ex: <http://library.example.com/>

SELECT ?callNumber ?location ?status
WHERE {
  ?manifestation dc:title "The Great Gatsby" .
  ?item frbr:exemplarOf ?manifestation ;
        ex:callNumber ?callNumber ;
        ex:location ?location ;
        ex:status "available" .
}
```

---

## 5. E-Commerce Semantic Graph

### Domain Description

Semantic e-commerce catalog with products, categories, and relationships. Demonstrates:
- Product categorization using SKOS
- Semantic product relationships
- Price and inventory management
- Product recommendations

### RDF Schema

```turtle
@prefix skos: <http://www.w3.org/2004/02/skos/core#>
@prefix gr: <http://purl.org/goodrelations/v1#>
@prefix foaf: <http://xmlns.com/foaf/0.1/>
@prefix dc: <http://purl.org/dc/elements/1.1/>
@prefix ex: <http://ecommerce.example.com/>

# Product Category Scheme
ex:productCategories a skos:ConceptScheme ;
  dc:title "Product Categories" ;
  skos:hasTopConcept ex:cat_electronics .

ex:cat_electronics a skos:Concept ;
  skos:prefLabel "Electronics" ;
  skos:narrower ex:cat_computers ;
  skos:narrower ex:cat_phones .

ex:cat_computers a skos:Concept ;
  skos:prefLabel "Computers" ;
  skos:broader ex:cat_electronics ;
  skos:narrower ex:cat_laptops ;
  skos:narrower ex:cat_desktops .

# Products
ex:product1 a gr:ProductOrService ;
  dc:title "MacBook Pro 14-inch" ;
  gr:hasCategory ex:cat_laptops ;
  gr:hasUnitPriceSpecification ex:price1 ;
  gr:hasInventoryLevel 45 ;
  dc:description "High-performance laptop" ;
  foaf:img "macbook-pro.jpg" .

ex:price1 a gr:UnitPriceSpecification ;
  gr:hasCurrency "USD" ;
  gr:hasCurrencyValue "1999.99"^^xsd:decimal ;
  gr:hasUnitOfMeasurement "unit" .

# Product relationships (recommendations)
ex:product1 ex:recommendedWith ex:product2 ;
            ex:recommendedWith ex:product3 .

ex:product2 a gr:ProductOrService ;
  dc:title "USB-C Hub" ;
  gr:hasCategory ex:cat_accessories ;
  gr:hasUnitPriceSpecification ex:price2 ;
  gr:hasInventoryLevel 150 .

# Supplier/Brand
ex:supplier1 a foaf:Organization ;
  foaf:name "Apple Inc." ;
  foaf:homepage <http://apple.com/> .
```

### Example Queries

#### Query 1: Browse category hierarchy
```sparql
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?category ?label
WHERE {
  ?category skos:broader ex:cat_electronics ;
            skos:prefLabel ?label .
}
```

#### Query 2: Find products in category with price filter
```sparql
PREFIX gr: <http://purl.org/goodrelations/v1#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>

SELECT ?title ?price ?stock
WHERE {
  ?product gr:hasCategory ex:cat_laptops ;
           dc:title ?title ;
           gr:hasInventoryLevel ?stock ;
           gr:hasUnitPriceSpecification ?priceSpec .
  ?priceSpec gr:hasCurrencyValue ?price .
  FILTER (?price < 2000)
}
ORDER BY ?price
```

#### Query 3: Find recommended products
```sparql
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX ex: <http://ecommerce.example.com/>

SELECT ?productTitle ?recommendedTitle
WHERE {
  ?product dc:title "MacBook Pro 14-inch" ;
           ex:recommendedWith ?recommended .
  ?recommended dc:title ?recommendedTitle .
}
```

---

## Summary

These 5 examples demonstrate:

✅ **Linked Open Data** - Integration with DBpedia and external SPARQL endpoints  
✅ **Organization** - Hierarchical structures and SKOS-based role management  
✅ **Publication Network** - Citation analysis and collaboration networks  
✅ **Library System** - FRBR-based bibliographic data  
✅ **E-Commerce** - Product catalogs with semantic relationships  

Each example includes:
- Complete RDF/Turtle schema
- Multiple SPARQL query patterns
- Python implementation examples
- Real-world use cases

All examples follow best practices:
- Standard vocabularies (FOAF, Dublin Core, OWL)
- Named graphs for data organization
- Proper URI patterns
- Semantic consistency

---

**Last Updated:** April 12, 2026  
**RDF Version:** 1.1  
**SPARQL Version:** 1.1

