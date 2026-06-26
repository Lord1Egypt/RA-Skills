# Domain Ontology Examples

Complete RDF/OWL ontology examples for different domains.

## Example 1: Research System Ontology

### Domain Description

```
A research institution contains researchers and academic staff.
Researchers conduct research in different domains and write papers.
Papers have authors, titles, and publication dates.
Researchers are affiliated with institutions and work in departments.
Papers are published in venues (conferences, journals).
Researchers can have advisors and students (other researchers).
```

### Turtle Ontology

```turtle
@prefix ex: <http://example.org/research#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix dc: <http://purl.org/dc/elements/1.1/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Classes
ex:Researcher a owl:Class ;
  rdfs:subClassOf foaf:Person ;
  rdfs:label "Researcher" ;
  rdfs:comment "A person who conducts research" .

ex:Paper a owl:Class ;
  rdfs:label "Paper" ;
  rdfs:comment "A research publication" .

ex:Institution a owl:Class ;
  rdfs:label "Institution" ;
  rdfs:comment "A research institution" .

ex:Department a owl:Class ;
  rdfs:label "Department" ;
  rdfs:comment "An academic department" .

ex:ResearchArea a owl:Class ;
  rdfs:label "Research Area" ;
  rdfs:comment "A research domain" .

ex:Venue a owl:Class ;
  rdfs:label "Venue" ;
  rdfs:comment "A publication venue (conference, journal)" .

# Object Properties
ex:writes a owl:ObjectProperty ;
  rdfs:label "writes" ;
  rdfs:domain ex:Researcher ;
  rdfs:range ex:Paper .

ex:writtenBy a owl:ObjectProperty ;
  rdfs:label "written by" ;
  owl:inverseOf ex:writes ;
  rdfs:domain ex:Paper ;
  rdfs:range ex:Researcher .

ex:affiliatedWith a owl:ObjectProperty ;
  rdfs:label "affiliated with" ;
  rdfs:domain ex:Researcher ;
  rdfs:range ex:Institution .

ex:worksIn a owl:ObjectProperty ;
  rdfs:label "works in" ;
  rdfs:domain ex:Researcher ;
  rdfs:range ex:Department .

ex:conductedIn a owl:ObjectProperty ;
  rdfs:label "conducted in" ;
  rdfs:domain ex:ResearchArea ;
  rdfs:range ex:Department .

ex:publishedIn a owl:ObjectProperty ;
  rdfs:label "published in" ;
  rdfs:domain ex:Paper ;
  rdfs:range ex:Venue .

ex:advisor a owl:ObjectProperty ;
  rdfs:label "advisor" ;
  rdfs:domain ex:Researcher ;
  rdfs:range ex:Researcher .

ex:student a owl:ObjectProperty ;
  rdfs:label "student" ;
  owl:inverseOf ex:advisor ;
  rdfs:domain ex:Researcher ;
  rdfs:range ex:Researcher .

# Datatype Properties
ex:title a owl:DatatypeProperty ;
  rdfs:label "title" ;
  rdfs:range xsd:string .

ex:abstract a owl:DatatypeProperty ;
  rdfs:label "abstract" ;
  rdfs:range xsd:string .

ex:publicationDate a owl:DatatypeProperty ;
  rdfs:label "publication date" ;
  rdfs:range xsd:date .

ex:email a owl:DatatypeProperty ;
  rdfs:label "email" ;
  rdfs:range xsd:string .

ex:uri a owl:DatatypeProperty ;
  rdfs:label "URI" ;
  rdfs:range xsd:anyURI .
```

---

## Example 2: E-Commerce Product Ontology

### Domain Description

```
An e-commerce system has products organized in categories.
Products have prices, descriptions, and inventory.
Customers purchase products through orders.
Products can have reviews from customers.
Each order contains order items with quantities and prices.
Suppliers provide products to the system.
```

### Turtle Ontology

```turtle
@prefix ex: <http://example.org/ecommerce#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix dc: <http://purl.org/dc/elements/1.1/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Classes
ex:Product a owl:Class ;
  rdfs:label "Product" .

ex:Category a owl:Class ;
  rdfs:label "Category" .

ex:Customer a owl:Class ;
  rdfs:subClassOf foaf:Person ;
  rdfs:label "Customer" .

ex:Order a owl:Class ;
  rdfs:label "Order" .

ex:OrderItem a owl:Class ;
  rdfs:label "Order Item" .

ex:Review a owl:Class ;
  rdfs:label "Review" .

ex:Supplier a owl:Class ;
  rdfs:label "Supplier" .

# Object Properties
ex:inCategory a owl:ObjectProperty ;
  rdfs:domain ex:Product ;
  rdfs:range ex:Category ;
  rdfs:label "in category" .

ex:places a owl:ObjectProperty ;
  rdfs:domain ex:Customer ;
  rdfs:range ex:Order ;
  rdfs:label "places" .

ex:contains a owl:ObjectProperty ;
  rdfs:domain ex:Order ;
  rdfs:range ex:OrderItem ;
  rdfs:label "contains" .

ex:refersTo a owl:ObjectProperty ;
  rdfs:domain ex:OrderItem ;
  rdfs:range ex:Product ;
  rdfs:label "refers to" .

ex:reviewsProduct a owl:ObjectProperty ;
  rdfs:domain ex:Review ;
  rdfs:range ex:Product ;
  rdfs:label "reviews product" .

ex:reviewedBy a owl:ObjectProperty ;
  rdfs:domain ex:Product ;
  rdfs:range ex:Review ;
  owl:inverseOf ex:reviewsProduct ;
  rdfs:label "reviewed by" .

ex:suppliedBy a owl:ObjectProperty ;
  rdfs:domain ex:Product ;
  rdfs:range ex:Supplier ;
  rdfs:label "supplied by" .

# Datatype Properties
ex:name a owl:DatatypeProperty ;
  rdfs:range xsd:string ;
  rdfs:label "name" .

ex:price a owl:DatatypeProperty ;
  rdfs:range xsd:decimal ;
  rdfs:label "price" .

ex:quantity a owl:DatatypeProperty ;
  rdfs:range xsd:integer ;
  rdfs:label "quantity" .

ex:rating a owl:DatatypeProperty ;
  rdfs:range xsd:decimal ;
  rdfs:label "rating" .

ex:description a owl:DatatypeProperty ;
  rdfs:range xsd:string ;
  rdfs:label "description" .

ex:orderDate a owl:DatatypeProperty ;
  rdfs:range xsd:date ;
  rdfs:label "order date" .
```

---

## Example 3: Library Management Ontology

### Domain Description

```
A library contains books and members.
Books have titles, authors, ISBN, and publication dates.
Members can borrow books for limited periods.
Books are organized by subject and genre.
Members have membership status and contact information.
Librarians manage the library system.
```

### Turtle Ontology

```turtle
@prefix ex: <http://example.org/library#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix dc: <http://purl.org/dc/elements/1.1/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Classes
ex:Book a owl:Class ;
  rdfs:label "Book" .

ex:Member a owl:Class ;
  rdfs:subClassOf foaf:Person ;
  rdfs:label "Member" .

ex:Librarian a owl:Class ;
  rdfs:subClassOf foaf:Person ;
  rdfs:label "Librarian" .

ex:Subject a owl:Class ;
  rdfs:label "Subject" .

ex:Genre a owl:Class ;
  rdfs:label "Genre" .

ex:Borrowing a owl:Class ;
  rdfs:label "Borrowing" .

# Object Properties
ex:author a owl:ObjectProperty ;
  rdfs:domain ex:Book ;
  rdfs:range foaf:Person ;
  rdfs:label "author" .

ex:hasSubject a owl:ObjectProperty ;
  rdfs:domain ex:Book ;
  rdfs:range ex:Subject ;
  rdfs:label "has subject" .

ex:hasGenre a owl:ObjectProperty ;
  rdfs:domain ex:Book ;
  rdfs:range ex:Genre ;
  rdfs:label "has genre" .

ex:borrows a owl:ObjectProperty ;
  rdfs:domain ex:Member ;
  rdfs:range ex:Borrowing ;
  rdfs:label "borrows" .

ex:borrowsBook a owl:ObjectProperty ;
  rdfs:domain ex:Borrowing ;
  rdfs:range ex:Book ;
  rdfs:label "borrows book" .

ex:manages a owl:ObjectProperty ;
  rdfs:domain ex:Librarian ;
  rdfs:range ex:Book ;
  rdfs:label "manages" .

# Datatype Properties
ex:title a owl:DatatypeProperty ;
  rdfs:range xsd:string ;
  rdfs:label "title" .

ex:isbn a owl:DatatypeProperty ;
  rdfs:range xsd:string ;
  rdfs:label "ISBN" .

ex:publishedDate a owl:DatatypeProperty ;
  rdfs:range xsd:date ;
  rdfs:label "published date" .

ex:membershipStatus a owl:DatatypeProperty ;
  rdfs:range xsd:string ;
  rdfs:label "membership status" .

ex:borrowDate a owl:DatatypeProperty ;
  rdfs:range xsd:date ;
  rdfs:label "borrow date" .

ex:dueDate a owl:DatatypeProperty ;
  rdfs:range xsd:date ;
  rdfs:label "due date" .
```

---

## Comparison Table

| Aspect | Research | E-Commerce | Library |
|--------|----------|-----------|---------|
| **Classes** | 7 | 7 | 6 |
| **Object Properties** | 8 | 7 | 7 |
| **Datatype Properties** | 5 | 7 | 7 |
| **External Vocabularies** | FOAF, Dublin Core | FOAF | FOAF, Dublin Core |
| **Complexity** | Medium | Medium | Medium |

---

See [ontology-patterns.md](../references/ontology-patterns.md) for design patterns and reusable components.

