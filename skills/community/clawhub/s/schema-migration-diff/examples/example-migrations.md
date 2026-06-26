# Schema Migration Examples

Complete schema migration examples for different domains.

## Example 1: University Schema Evolution

### Schema v1

```
Student: student_id, name, email, enrollment_year
Course: course_code, title
(Student)-[:ENROLLED_IN]->(Course)
```

### Schema v2

```
Student: student_id, full_name, email, enrollment_year, gpa
Course: course_code, title, credits, department_code
Department: dept_id, name
(Student)-[:ENROLLED_IN]->(Course)
(Course)-[:BELONGS_TO]->(Department)
```

### Diff Report

```
ADDED ENTITIES:
  + Department

ADDED PROPERTIES:
  + Student.gpa
  + Course.credits
  + Course.department_code

ADDED RELATIONSHIPS:
  + (Course)-[:BELONGS_TO]->(Department)

MODIFIED PROPERTIES:
  ~ Student.name → Student.full_name (rename)

Risk Level: Medium
Estimated Steps: 5
```

### Migration Script (Cypher)

```cypher
-- Step 1: Create Department entity and constraint
CREATE CONSTRAINT dept_id_unique FOR (d:Department) REQUIRE d.dept_id IS UNIQUE
CREATE (d:Department {dept_id: "CS", name: "Computer Science"})
CREATE (d:Department {dept_id: "MATH", name: "Mathematics"})

-- Step 2: Add new property to Course
MATCH (c:Course)
SET c.credits = 3,
    c.department_code = "CS"

-- Step 3: Add relationship
MATCH (c:Course), (d:Department)
WHERE c.department_code = d.dept_id
CREATE (c)-[:BELONGS_TO]->(d)

-- Step 4: Rename Student property
MATCH (s:Student)
WHERE s.name IS NOT NULL
SET s.full_name = s.name

-- Step 5: Add gpa property to Student
MATCH (s:Student)
SET s.gpa = 3.5

-- Step 6: Remove old property
MATCH (s:Student)
REMOVE s.name

-- Verification
MATCH (c:Course)-[:BELONGS_TO]->(d:Department)
RETURN COUNT(*) as new_relationships
```

---

## Example 2: E-Commerce Schema Evolution

### Schema v1

```
Product: product_id, name, price
Category: category_id, name
(Product)-[:IN_CATEGORY]->(Category)
```

### Schema v2

```
Product: product_id, name, price, supplier_id
Category: category_id, name, parent_category
Supplier: supplier_id, name, contact_email
(Product)-[:IN_CATEGORY]->(Category)
(Product)-[:SUPPLIED_BY]->(Supplier)
(Category)-[:PARENT_OF]->(Category) [self-referential]
```

### Migration Script (Cypher)

```cypher
-- Step 1: Create Supplier entity
CREATE CONSTRAINT supplier_id_unique 
FOR (s:Supplier) REQUIRE s.supplier_id IS UNIQUE

CREATE (s:Supplier {
  supplier_id: "SUP001",
  name: "Global Supplies",
  contact_email: "contact@supplies.com"
})

-- Step 2: Add supplier_id to products
MATCH (p:Product)
SET p.supplier_id = "SUP001"

-- Step 3: Create new relationships
MATCH (p:Product), (s:Supplier)
WHERE p.supplier_id = s.supplier_id
CREATE (p)-[:SUPPLIED_BY]->(s)

-- Step 4: Add parent_category to categories
MATCH (cat:Category)
SET cat.parent_category = NULL

-- Step 5: Create category hierarchy
MATCH (cat:Category {name: "Electronics"}),
      (parent:Category {name: "Products"})
CREATE (parent)-[:PARENT_OF]->(cat)

-- Verification
MATCH (p:Product)-[:SUPPLIED_BY]->(s:Supplier)
RETURN COUNT(*) as product_supplier_links
```

---

## Example 3: Research Domain Evolution

### Schema v1

```
Researcher: researcher_id, name
Paper: paper_id, title, year
(Researcher)-[:WROTE]->(Paper)
```

### Schema v2

```
Researcher: researcher_id, full_name, email, affiliation
Institution: institution_id, name, location
Paper: paper_id, title, year, doi
Conference: conference_id, name, year
(Researcher)-[:WROTE]->(Paper)
(Researcher)-[:AFFILIATED_WITH]->(Institution)
(Paper)-[:PRESENTED_AT]->(Conference)
```

### Migration Report

```
Schema Migration: Research v1 → v2
==================================

CHANGES DETECTED:

Entities:
  + Institution (new)
  + Conference (new)

Properties:
  ~ Researcher.name → Researcher.full_name (rename)
  + Researcher.email
  + Researcher.affiliation
  + Paper.doi

Relationships:
  + (Researcher)-[:AFFILIATED_WITH]->(Institution)
  + (Paper)-[:PRESENTED_AT]->(Conference)

RISK ASSESSMENT:
  Breaking Changes: 0
  Data Loss Risk: Low
  Rollback Complexity: Low
  Total Steps: 7
  Estimated Time: 45 minutes

RECOMMENDED APPROACH:
  1. Test on staging environment
  2. Create backups
  3. Execute in transaction
  4. Validate data integrity
  5. Monitor performance
  6. Plan rollback procedure
```

---

## Example 4: Social Network Evolution

### Schema v1

```
User: user_id, username
Post: post_id, content, created_date
(User)-[:CREATED]->(Post)
(User)-[:FOLLOWS]->(User)
```

### Schema v2

```
User: user_id, username, bio, verified
Post: post_id, content, created_date, likes_count
Comment: comment_id, text, created_date
(User)-[:CREATED]->(Post)
(User)-[:FOLLOWS]->(User)
(User)-[:LIKED]->(Post)
(User)-[:COMMENTED_ON]->(Post)
(Comment)-[:ON_POST]->(Post)
```

### Migration Steps

```cypher
-- Step 1: Add new properties to User
MATCH (u:User)
SET u.bio = "",
    u.verified = false

-- Step 2: Add new property to Post
MATCH (p:Post)
SET p.likes_count = 0

-- Step 3: Create Comment entity
CREATE CONSTRAINT comment_id_unique 
FOR (c:Comment) REQUIRE c.comment_id IS UNIQUE

-- Step 4: Create default comments if needed
-- (Assuming comments exist in old system as text)

-- Step 5: Add LIKED relationship
MATCH (u:User), (p:Post)
WHERE u.user_id IN ["U001", "U002"]
AND p.post_id = "P001"
CREATE (u)-[:LIKED]->(p)

-- Step 6: Update likes_count
MATCH (p:Post)-[:LIKED]-(u:User)
WITH p, COUNT(u) as like_count
SET p.likes_count = like_count

-- Step 7: Verify
MATCH (u:User)
WHERE u.bio IS NOT NULL
RETURN COUNT(u) as users_with_bio
```

---

## Comparison Table

| Domain | Added | Removed | Modified | Risk | Time |
|--------|-------|---------|----------|------|------|
| University | 3 entities, 3 props | 0 | 1 property | Medium | 30min |
| E-Commerce | 1 entity | 0 | 2 props | Low | 20min |
| Research | 2 entities, 5 props | 0 | 1 property | Low | 45min |
| Social | 1 entity, 2 props | 0 | 2 props | Medium | 40min |

---

See [migration-patterns.md](../references/migration-patterns.md) for detailed migration patterns and best practices.

