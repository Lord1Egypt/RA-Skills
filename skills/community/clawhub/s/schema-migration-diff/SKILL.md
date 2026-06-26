---
name: graph_schema_migration_diff
title: Graph Schema Migration Diff
description: Analyze differences between knowledge graph schema versions and generate migration plans and scripts for safe schema evolution.
category: graph-modeling
tags:
  - knowledge-graph
  - schema-migration
  - graph-evolution
  - rdf
  - owl
  - neo4j
  - cypher
  - developer-tools
version: 1.0.0
author: community
license: MIT
---

# Graph Schema Migration Diff

**Detect schema differences and generate migration plans for graph evolution.**

This skill compares two knowledge graph schema versions and generates safe migration strategies.

## Quick Start

### Use When
- Upgrading graph schemas
- Analyzing schema changes between versions
- Planning schema evolution
- Generating migration scripts
- Migrating existing data
- Refactoring graph models

### Inputs
- Schema Version 1 (RDF, OWL, or property graph)
- Schema Version 2 (RDF, OWL, or property graph)
- Migration scope (full or partial)

### Outputs
- Schema diff report
- Change categories (added, removed, modified)
- Migration plan
- Migration scripts (Cypher, SPARQL, or Python)
- Risk assessment

## Example

**Schema v1:**
```
Student: student_id, name, email
Course: course_code, title
(Student)-[:ENROLLED_IN]->(Course)
```

**Schema v2:**
```
Student: student_id, full_name, email
Course: course_code, title, credits
Department: dept_id, name
(Student)-[:ENROLLED_IN]->(Course)
(Course)-[:BELONGS_TO]->(Department)
```

**Diff Report:**
```
ADDED:
  + Department label
  + Course.credits property
  + (Course)-[:BELONGS_TO]->(Department) relationship

MODIFIED:
  ~ Student.name → Student.full_name (rename)

REMOVED:
  (none)

Risk: Medium | Complexity: Medium
```

## Change Detection

### Entity Changes
- Added entities (new node labels/classes)
- Removed entities (deleted labels/classes)
- Renamed entities

### Property Changes
- Added properties (new attributes)
- Removed properties (deleted attributes)
- Renamed properties (property name changes)
- Type changes (property type modifications)

### Relationship Changes
- Added relationships (new relationship types)
- Removed relationships (deleted relationship types)
- Direction changes
- Cardinality changes

### Constraint Changes
- Added constraints (new unique, required)
- Removed constraints (deleted constraints)
- Modified constraints

## Execution Steps

1. **Parse Schemas** – Load both schema versions
2. **Extract Structure** – Build schema graphs
3. **Compare** – Detect differences systematically
4. **Categorize Changes** – Classify by type
5. **Assess Risk** – Evaluate migration impact
6. **Generate Plan** – Create migration strategy
7. **Generate Scripts** – Output executable migrations

## Output Formats

### Migration Plan (Text)
```
Schema Migration: v1 → v2
========================

ENTITY CHANGES:
  + Department

PROPERTY CHANGES:
  Student.name → Student.full_name

RELATIONSHIP CHANGES:
  + (Course)-[:BELONGS_TO]->(Department)

Migration Steps: 3
Risk Level: Medium
Estimated Time: 30 minutes
```

### Cypher Migration
```cypher
-- 1. Add constraint for new entity
CREATE CONSTRAINT department_id_unique 
FOR (d:Department) REQUIRE d.department_id IS UNIQUE

-- 2. Rename property
MATCH (s:Student)
WHERE s.name IS NOT NULL
SET s.full_name = s.name
REMOVE s.name

-- 3. Add new relationship
CREATE (c:Course)-[:BELONGS_TO]->(d:Department)
```

## Recommended Libraries

- **Graph Analysis:** networkx, rdflib
- **Schema Comparison:** deepdiff, dictdiffer
- **RDF/OWL:** owlready2, pyshacl
- **Neo4j:** neo4j, py2neo

## Best Practices

✓ Test migrations on staging data first  
✓ Create backups before migration  
✓ Maintain backward compatibility  
✓ Document all schema changes  
✓ Version all schemas  
✓ Review migration scripts carefully  
✓ Perform migrations incrementally  
✓ Validate data after migration  

## References

See [migration-patterns.md](references/migration-patterns.md) for migration strategies and [example-migrations.md](examples/example-migrations.md) for domain migration examples.

---

**Version:** 1.0.0
