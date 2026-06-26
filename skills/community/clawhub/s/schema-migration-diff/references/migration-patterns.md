# Schema Migration Patterns

This guide provides patterns for safely migrating between graph schema versions.

## Property Rename Migration

### Pattern: Rename Property

```
v1: Student.name
v2: Student.full_name
```

### Neo4j Cypher

```cypher
-- Step 1: Add new property with values
MATCH (s:Student)
WHERE s.name IS NOT NULL
SET s.full_name = s.name

-- Step 2: Remove old property
MATCH (s:Student)
WHERE s.full_name IS NOT NULL
REMOVE s.name

-- Verify migration
MATCH (s:Student)
WHERE s.name IS NOT NULL
RETURN COUNT(s) as remaining_old_prop
```

### RDF/OWL

```turtle
-- Add new property
?student :fullName ?name .

-- Keep old temporarily (for data preservation)
?student :name ?name ;
         :fullName ?name .

-- Later: Remove old property
DELETE { ?student :name ?name }
```

---

## Add New Entity

### Pattern: Add Entity Type

```
v1: (no Department)
v2: Department entity added
```

### Neo4j

```cypher
-- 1. Create constraint for new entity
CREATE CONSTRAINT department_id_unique 
FOR (d:Department) 
REQUIRE d.department_id IS UNIQUE

-- 2. Create index
CREATE INDEX dept_name_idx FOR (d:Department) ON (d.name)

-- 3. Populate with initial data (if needed)
CREATE (d:Department {
  department_id: "D001",
  name: "Computer Science"
})
```

### RDF/OWL

```turtle
-- Define new class
:Department a owl:Class ;
  rdfs:label "Department" .

-- Define properties
:dept_id a owl:DatatypeProperty ;
  rdfs:domain :Department .
```

---

## Add New Relationship

### Pattern: Add Relationship Type

```
v1: (no Course-Department relationship)
v2: (Course)-[:BELONGS_TO]->(Department)
```

### Neo4j

```cypher
-- Create relationship with data
MATCH (c:Course), (d:Department)
WHERE c.department_code = d.department_id
CREATE (c)-[:BELONGS_TO]->(d)

-- Verify
MATCH (c:Course)-[:BELONGS_TO]->(d:Department)
RETURN COUNT(*) as relationships_created
```

### Data Migration

```cypher
-- Handle orphaned courses
MATCH (c:Course)
WHERE NOT (c)-[:BELONGS_TO]->()
SET c.unmigrated = true
RETURN c
```

---

## Remove Property (with Care)

### Pattern: Deprecate then Remove

```
v1: Student.legacy_field
v2: (removed)
```

### Step 1: Add Deprecation Warning

```cypher
-- Mark as deprecated
MATCH (s:Student)
WHERE s.legacy_field IS NOT NULL
SET s.deprecated_properties = ["legacy_field"]
```

### Step 2: Migrate Data

```cypher
-- Move to archive if needed
MATCH (s:Student)
WHERE s.legacy_field IS NOT NULL
SET s.archived_legacy = s.legacy_field
```

### Step 3: Remove

```cypher
-- Remove after verification period
MATCH (s:Student)
WHERE s.archived_legacy IS NOT NULL
REMOVE s.legacy_field
```

---

## Change Relationship Cardinality

### Pattern: Single → Multiple

```
v1: (Person)-[:WORKS_FOR]->(Company) [max 1]
v2: (Person)-[:WORKS_FOR]->(Company) [max 5]
```

### Cypher

```cypher
-- Verify existing cardinality
MATCH (p:Person)-[r:WORKS_FOR]->(c:Company)
WITH p, COUNT(r) as job_count
WHERE job_count > 1
RETURN p, job_count
-- Should return empty if changing from max 1

-- Add new relationships
MATCH (p:Person), (c:Company)
WHERE p.id = "P001" AND c.id = "C002"
CREATE (p)-[:WORKS_FOR]->(c)
```

---

## Schema Version Management

### Pattern: Track Schema Versions

```cypher
-- Create schema version node
CREATE (sv:SchemaVersion {
  version: "2.0",
  release_date: date.today(),
  migration_status: "in_progress"
})

-- Track changes
CREATE (sv)-[:CHANGED_ENTITIES]->(changes)
CREATE (sv)-[:EXECUTED_MIGRATIONS]->(migrations)
```

---

## Backward Compatibility

### Pattern: Maintain Old and New

```cypher
-- Keep old properties/relationships during transition
MATCH (s:Student)
SET s.name = s.full_name,
    s.full_name = s.full_name

-- Dual-write during transition period
MATCH (s:Student {student_id: "S001"})
SET s.name = "Alice",
    s.full_name = "Alice"

-- After transition, remove old
MATCH (s:Student)
REMOVE s.name
```

---

## Rollback Patterns

### Pattern: Create Rollback Script

```cypher
-- Reverse property rename
MATCH (s:Student)
WHERE s.full_name IS NOT NULL
SET s.name = s.full_name
REMOVE s.full_name

-- Reverse relationship creation
MATCH (c:Course)-[r:BELONGS_TO]->()
WHERE r.migrated = true
DELETE r

-- Reverse constraint
DROP CONSTRAINT department_id_unique
```

---

## Testing Migration Safety

### Pattern: Validation Checks

```cypher
-- 1. Count entities before
WITH COUNT(*) as before_count
MATCH (n) RETURN before_count

-- 2. Execute migration
-- (migration steps)

-- 3. Count entities after
MATCH (n)
WITH COUNT(*) as after_count
WHERE after_count = before_count
RETURN "Count check passed"

-- 4. Validate relationships
MATCH (s:Student)-[:ENROLLED_IN]->(c:Course)
WITH COUNT(*) as relationship_count
WHERE relationship_count > 0
RETURN "Relationship check passed"

-- 5. Check data integrity
MATCH (s:Student)
WHERE s.student_id IS NULL
RETURN COUNT(s) as missing_ids
-- Should return 0
```

---

## Common Issues & Solutions

| Issue | Detection | Solution |
|-------|-----------|----------|
| Property rename fails | Some values null | Update NULL values first |
| Orphaned nodes | No relationships | Review and reassign |
| Duplicates created | COUNT increased | Run deduplication |
| Circular refs | Path found | Review and resolve |
| Data type mismatch | Cast error | Convert types first |

---

## Best Practices

✓ Always backup before migration  
✓ Test on staging environment  
✓ Document all changes  
✓ Use transactions for atomicity  
✓ Validate after each step  
✓ Keep rollback scripts ready  
✓ Version all schemas  
✓ Communicate changes to team  

---

See [example-migrations.md](../examples/example-migrations.md) for complete migration examples.

