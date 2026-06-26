# SurrealDB Graph Queries

SurrealDB is a multi-model database with first-class graph capabilities. Unlike bolt-on graph layers, SurrealDB treats records as nodes and edge tables as typed, queryable relationships. Graph traversal uses arrow syntax (`->`, `<-`, `<->`) directly in SurrealQL, enabling complex relationship queries without separate graph query languages.

---

## RELATE Statement

The `RELATE` statement creates graph edges (relationships) between records. Each relationship is stored in an edge table with automatic `in` and `out` fields pointing to the source and target records.

### Basic Syntax

```surrealql
-- General form (verified against v3.0.5 RELATE grammar — see the
-- precision comment under "Setting Properties on Edges" below).
-- RELATE only accepts CONTENT or SET; there is NO MERGE clause.
RELATE @from->@edge->@to [CONTENT @value | SET @field = @value ...];

-- Create a simple relationship
RELATE person:alice->knows->person:bob;

-- The edge record is stored in the 'knows' table with:
--   in: person:alice
--   out: person:bob
SELECT * FROM knows;
-- Returns: [{ id: knows:..., in: person:alice, out: person:bob }]
```

### Setting Properties on Edges

Edge tables are full SurrealDB tables -- you can store arbitrary data on them.

```surrealql
-- Using SET for individual fields
RELATE person:alice->knows->person:bob SET
    since = d'2023-06-15',
    strength = 0.85,
    context = 'work';

-- Using CONTENT for full object replacement
RELATE person:alice->follows->person:charlie CONTENT {
    since: time::now(),
    notifications: true,
    tags: ['tech', 'surrealdb']
};

-- To update an existing relationship's properties, use UPDATE on the
-- edge record (RELATE creates new edges; it does not accept MERGE).
-- Verified against v3.0.5: RELATE grammar is
--   RELATE [ ONLY ] @from -> @table -> @to [ CONTENT @value | SET @field = @value ... ]
--                  [ RETURN ... ] [ TIMEOUT @duration ]
-- — there is no MERGE clause on RELATE.
UPDATE knows SET last_interaction = time::now()
WHERE in = person:alice AND out = person:bob;
```

### Creating Multiple Relationships at Once

```surrealql
-- Relate multiple sources to one target
RELATE [person:alice, person:bob, person:charlie]->likes->post:123;

-- Relate one source to multiple targets
RELATE person:alice->follows->[person:bob, person:charlie, person:dave];

-- Relate multiple to multiple (creates cartesian product)
RELATE [person:alice, person:bob]->likes->[post:1, post:2];
-- Creates 4 edges: alice->post:1, alice->post:2, bob->post:1, bob->post:2
```

### Typed Edge Tables with Schema Enforcement

```surrealql
-- Define the edge table with typed in/out fields
DEFINE TABLE wrote SCHEMAFULL;
DEFINE FIELD in ON TABLE wrote TYPE record<person>;
DEFINE FIELD out ON TABLE wrote TYPE record<article>;
DEFINE FIELD written_at ON TABLE wrote TYPE datetime DEFAULT time::now();
DEFINE FIELD word_count ON TABLE wrote TYPE int;

-- Enforce unique relationships (one person can write an article only once)
DEFINE INDEX unique_author_article ON TABLE wrote COLUMNS in, out UNIQUE;

-- This succeeds
RELATE person:aristotle->wrote->article:metaphysics SET word_count = 45000;

-- This fails because of the UNIQUE index
RELATE person:aristotle->wrote->article:metaphysics SET word_count = 50000;

-- This also fails because 'in' must be a person record
RELATE article:foo->wrote->article:bar;
-- Error: Expected a record<person>, but found record<article>
```

### `TYPE RELATION`, `FROM`/`TO`, and `ENFORCED`

The `SCHEMAFULL + record<…> in/out` pattern above works, but v3 also
provides a dedicated relation-table form on `DEFINE TABLE`. `TYPE
RELATION` declares that a table is an edge table (vs. `TYPE NORMAL`
for record tables); the `FROM` / `TO` clauses (alias `IN` / `OUT`)
constrain which record types may appear at each end; `ENFORCED`
upgrades the constraint from "rejected at RELATE time" to "rejected
both at RELATE time and on any direct CREATE/UPDATE that would put
an invalid edge in the table."

```surrealql
-- Equivalent to the SCHEMAFULL + DEFINE FIELD in/out pattern, but
-- with the relation contract declared on DEFINE TABLE itself.
DEFINE TABLE wrote TYPE RELATION FROM person TO article SCHEMAFULL;
DEFINE FIELD written_at ON TABLE wrote TYPE datetime DEFAULT time::now();
DEFINE FIELD word_count ON TABLE wrote TYPE int;

-- Multi-type endpoints — accept several record types on either side
-- using `|`. Useful for polymorphic edges (e.g. comments on either
-- posts or articles).
DEFINE TABLE commented_on TYPE RELATION FROM person TO post|article;

-- ENFORCED — also reject INSERT/UPDATE statements that would write
-- an invalid `in`/`out` directly (not just RELATE).
DEFINE TABLE wrote TYPE RELATION FROM person TO article ENFORCED;

-- IN/OUT are accepted as aliases for FROM/TO; pick one form and stay
-- consistent within a codebase.
DEFINE TABLE follows TYPE RELATION IN person OUT person;
```

When to choose which form:

- **`TYPE RELATION FROM … TO …`** — preferred for new code. The
  relation contract lives on the table definition where readers
  expect it; tooling (and `INFO FOR TABLE`) reports the table as a
  relation; less boilerplate than `DEFINE FIELD in TYPE record<…>`
  twice.
- **`SCHEMAFULL` + `DEFINE FIELD in/out TYPE record<…>`** — still
  valid; useful when migrating older code or when you need
  per-field control beyond what `TYPE RELATION` exposes.
- **`ENFORCED`** — add when the application path is mixed (some
  callers RELATE, others CREATE/UPDATE the edge record directly)
  and you want the type contract honored on every write.

### Bidirectional Edges

```surrealql
-- Some relationships are inherently bidirectional
-- Model friendship as a single edge, query from either direction
DEFINE TABLE friends_with SCHEMAFULL;
DEFINE FIELD in ON TABLE friends_with TYPE record<person>;
DEFINE FIELD out ON TABLE friends_with TYPE record<person>;
DEFINE FIELD since ON TABLE friends_with TYPE datetime;

RELATE person:alice->friends_with->person:bob SET since = d'2023-01-01';

-- Query from either side using <-> operator
SELECT *, <->friends_with<->person AS friends FROM person:alice;
SELECT *, <->friends_with<->person AS friends FROM person:bob;

-- Exclude self-references from results
SELECT *,
    array::complement(<->friends_with<->person, [id]) AS friends
FROM person;
```

### Self-Referential Edges

```surrealql
-- A person can manage themselves (e.g., solo founder)
DEFINE TABLE manages SCHEMAFULL;
DEFINE FIELD in ON TABLE manages TYPE record<person>;
DEFINE FIELD out ON TABLE manages TYPE record<person>;
DEFINE FIELD role ON TABLE manages TYPE string;

-- Hierarchical management
RELATE person:ceo->manages->person:vp_eng SET role = 'direct_report';
RELATE person:vp_eng->manages->person:lead_1 SET role = 'direct_report';
RELATE person:vp_eng->manages->person:lead_2 SET role = 'direct_report';
RELATE person:lead_1->manages->person:dev_1 SET role = 'direct_report';
RELATE person:lead_1->manages->person:dev_2 SET role = 'direct_report';

-- Self-referential: person references themselves
RELATE person:freelancer->manages->person:freelancer SET role = 'self';
```

---

## Graph Traversal

SurrealDB uses arrow operators for graph traversal directly within `SELECT` statements or as standalone expressions.

### Forward Traversal (`->`)

Follow edges from a record outward through the `out` direction.

```surrealql
-- Find all articles written by Aristotle
SELECT ->wrote->article FROM person:aristotle;
-- Returns: [{ "->wrote->article": [article:metaphysics, article:on_sleep] }]

-- Get specific fields from traversed records
SELECT ->wrote->article.title FROM person:aristotle;

-- Standalone expression (no SELECT needed)
RETURN person:aristotle->wrote->article;

-- Destructured form with aliases
person:aristotle.{ name, articles: ->wrote->article.title };
```

### Reverse Traversal (`<-`)

Follow edges backward through the `in` direction.

```surrealql
-- Find who wrote a specific article
SELECT <-wrote<-person FROM article:metaphysics;

-- Find all users who liked a post
SELECT <-likes<-person.name AS liked_by FROM post:123;

-- Standalone expression
RETURN article:metaphysics<-wrote<-person;

-- Find all followers of a person
SELECT <-follows<-person.name AS followers FROM person:alice;
```

### Bidirectional Traversal (`<->`)

Follow edges in both directions simultaneously.

```surrealql
-- Find all friends (regardless of who initiated the relationship)
SELECT <->friends_with<->person AS friends FROM person:alice;

-- Exclude self from results
SELECT
    array::complement(<->friends_with<->person, [id]) AS friends
FROM person:alice;

-- Works across any relationship
SELECT <->knows<->person AS connections FROM person:bob;
```

### Multi-Hop Traversal

Chain arrow operators to traverse multiple relationship levels.

```surrealql
-- Friends of friends
SELECT ->knows->person->knows->person AS friends_of_friends
FROM person:alice;

-- Author -> articles -> topics
SELECT ->wrote->article->tagged_with->topic AS interests
FROM person:aristotle;

-- User -> orders -> products -> categories
SELECT ->placed->order->contains->product->belongs_to->category
FROM user:customer_1;

-- Multi-hop with field selection at each level
SELECT
    ->manages->person.name AS direct_reports,
    ->manages->person->manages->person.name AS skip_level_reports
FROM person:ceo;

-- Traversal through different edge types
SELECT
    ->likes->post<-wrote<-person AS liked_same_posts
FROM person:alice;
```

### Filtered Traversal

Apply WHERE conditions during traversal to filter intermediate results.

```surrealql
-- Only traverse 'knows' edges created after 2020
SELECT ->(knows WHERE since > d'2020-01-01')->person.name AS recent_contacts
FROM person:alice;

-- Filter on edge properties
SELECT ->(rated WHERE score >= 4.0)->movie.title AS highly_rated
FROM user:alice;

-- Filter on target node properties
SELECT ->knows->(person WHERE age > 30).name AS older_contacts
FROM person:alice;

-- Combine edge and node filters
SELECT
    ->(knows WHERE strength > 0.7)->(person WHERE active = true).name
    AS strong_active_contacts
FROM person:alice;

-- Multi-hop with filters at each level
SELECT
    ->(manages WHERE role = 'direct_report')
    ->person
    ->(manages WHERE role = 'direct_report')
    ->person.name AS skip_level_reports
FROM person:ceo;
```

### Aliased Traversal

Use `AS` on a full traversal expression in the SELECT projection to
name the result. (Pre-v1.5.1 revisions of this rule documented `AS`
*inside* a parenthesised arrow filter -- e.g. `->(knows WHERE since
> d'2023-01-01' AS recent_connections)->person.name` -- but no
official v3 test exercises that form. Stick to the SELECT-projection
position shown below.)

```surrealql
-- Alias the full traversal result
SELECT
    ->reports_to->person AS manager,
    ->reports_to->person->reports_to->person AS skip_level
FROM person:alice;
```

### Recursive Traversal Patterns (`{depth}` and `{lo..hi}`)

SurrealDB v3 has **first-class graph depth control**: the `.{...}`
destructuring modifier applied to a record reference. This is the
primary mechanism -- chaining fixed-hop arrows manually is the
fallback when you need per-hop projection differences.

```surrealql
-- Exactly N hops (here, N = 1).
person:alice.{1}->reports_to->person;

-- Up to N hops (1, 2, ..., or N -- shortest matches first).
person:alice.{..3}->knows->person;

-- A bounded range of hops (M to N inclusive).
person:alice.{1..3}->reports_to->person;

-- Unbounded recursion until the graph runs out (be careful on cyclic
-- or fan-out-heavy graphs -- combine with `+collect` or a hop cap).
org:company.{..}.children;
```

#### Recursive destructuring with `.@`

The `.@` placeholder applies the same destructuring pattern at every
recursion level, so a single expression can build a full nested tree
from a graph traversal.

```surrealql
-- Build the entire management tree under alice in one query.
person:alice.{..}.{
    name,
    reports_to: ->reports_to->person.@
};

-- Works with REFERENCE link fields too, not just edge traversals.
org:company.{..}.{ name, sub_orgs: children.@ };
```

#### Wildcard edge traversal (`->?`, `<-?`, `<->?`)

When you need to traverse "any edge type" rather than a specific
table, use `?` as the edge placeholder.

```surrealql
person:alice->?;          -- every outgoing edge of any type
person:alice->?->?;       -- every record reachable through any edge in two hops
person:alice<-?;          -- every incoming edge of any type
person:alice<->?;         -- every adjacent record, in either direction
```

#### Path-collection modifiers (`+collect`, `+path`, `+inclusive`)

Modifiers on the depth/range modifier change what the traversal
returns. They compose with `{N}` / `{..N}` / `{lo..hi}` / `{..}`.

```surrealql
-- Deduplicated set of nodes reached (a "collect" set).
person:alice.{..+collect}->reports_to->person;

-- Same, but include the start node in the collected set.
person:alice.{..+collect+inclusive}->knows->person;

-- All distinct paths (each result is a path array, not a node).
person:alice.{..+path}->reports_to->person;

-- Bounded path collection.
person:alice.{..3+path}->knows->person;
```

If you have to fall back to manual fixed-hop chains (rare in v3 -- only
when you need per-hop projection differences the destructuring form
can't express), the pattern looks like:

```surrealql
SELECT
    name,
    ->manages->person.name AS level_1,
    ->manages->person->manages->person.name AS level_2,
    ->manages->person->manages->person->manages->person.name AS level_3
FROM person:ceo;
```

Reach for the `{1..3}` form first, fixed chains only as a fallback.

---

## Advanced Graph Patterns

### Shortest-Path Queries (native `+shortest=target`)

SurrealDB v3 has a **native shortest-path modifier** -- pre-v1.5.1
revisions of this rule built a hand-rolled BFS for this and were
wrong. Use the `+shortest=target` modifier on the depth/range
destructuring instead.

```surrealql
-- Find the shortest reports-to chain from alice to the CEO.
person:alice.{..+shortest=person:ceo}->reports_to->person;

-- Bounded variant: only consider paths of at most 3 hops.
person:alice.{..3+shortest=person:ceo}->reports_to->person;

-- Include the start node in the returned path. `+inclusive` is the
-- only sub-modifier valid after `+shortest=` (verified against the
-- v3.0.5 parser — `parse_recurse_instruction` returns a single
-- `Option<RecurseInstruction>`, so `Path` / `Collect` / `Shortest`
-- are mutually exclusive; only `+inclusive` is accepted as a
-- secondary flag on `+shortest`).
person:alice.{..+shortest=person:ceo+inclusive}->reports_to->person;
```

`+shortest=` already returns the full path array (intermediate +
target nodes) by default — verified against the upstream language
test `language-tests/tests/language/graph/path_shortest.surql`,
where test 0 returns
`[person:lead_infra, person:dir_platform, person:vp_eng, person:ceo]`.
There is no separate "+path" sub-modifier on `+shortest=` (those
two recurse instructions are mutually exclusive in the parser);
add `+inclusive` if you also want the start node in the array.

`+shortest=` evaluates lazily and returns the first path that
matches the target record, so it terminates as soon as the BFS
front reaches the target -- no need to test increasing depths
manually. Reach for the manual depth-by-depth approach only when you
need behaviour `+shortest` does not express (e.g. enumerating *all*
shortest paths, or weighted shortest paths -- neither is in the
v3.0.5 surface).

### Degree Centrality Calculations

```surrealql
-- Out-degree: number of outgoing relationships
SELECT
    id,
    name,
    count(->knows->person) AS out_degree
FROM person
ORDER BY out_degree DESC;

-- In-degree: number of incoming relationships
SELECT
    id,
    name,
    count(<-knows<-person) AS in_degree
FROM person
ORDER BY in_degree DESC;

-- Total degree (bidirectional)
SELECT
    id,
    name,
    count(->knows->person) AS out_degree,
    count(<-knows<-person) AS in_degree,
    count(->knows->person) + count(<-knows<-person) AS total_degree
FROM person
ORDER BY total_degree DESC;

-- Weighted centrality using edge properties
SELECT
    id,
    name,
    math::sum(->knows.strength) AS weighted_out_degree,
    math::sum(<-knows.strength) AS weighted_in_degree
FROM person
ORDER BY weighted_out_degree DESC;
```

### Community Detection Patterns

```surrealql
-- Find clusters by shared connections (common neighbors)
SELECT
    p1.name AS person_a,
    p2.name AS person_b,
    array::intersect(
        p1->knows->person,
        p2->knows->person
    ) AS common_friends,
    count(array::intersect(
        p1->knows->person,
        p2->knows->person
    )) AS overlap_count
FROM person AS p1, person AS p2
WHERE p1.id != p2.id
ORDER BY overlap_count DESC;

-- Find tightly connected subgroups
-- People who all know each other (triads)
SELECT
    a.name AS person_a,
    b.name AS person_b,
    c.name AS person_c
FROM person AS a, person AS b, person AS c
WHERE
    a.id != b.id AND b.id != c.id AND a.id != c.id
    AND b IN a->knows->person
    AND c IN a->knows->person
    AND c IN b->knows->person;

-- Neighborhood overlap for community strength
DEFINE FUNCTION fn::jaccard_similarity($a: record<person>, $b: record<person>) {
    LET $neighbors_a = SELECT VALUE ->knows->person FROM ONLY $a;
    LET $neighbors_b = SELECT VALUE ->knows->person FROM ONLY $b;
    LET $intersection = array::intersect($neighbors_a, $neighbors_b);
    LET $union = array::union($neighbors_a, $neighbors_b);
    RETURN IF count($union) > 0 {
        count($intersection) / count($union)
    } ELSE {
        0.0
    };
};
```

### Recommendation Engine Using Graph Traversal

```surrealql
-- Collaborative filtering: "users who liked X also liked Y"
SELECT
    ->likes->product AS also_liked,
    count() AS frequency
FROM person
WHERE id IN (
    SELECT VALUE <-likes<-person FROM product:target_product
)
AND ->likes->product != product:target_product
GROUP BY also_liked
ORDER BY frequency DESC
LIMIT 10;

-- Content-based with graph enrichment:
-- Find products in categories the user has shown interest in
SELECT
    p.id,
    p.name,
    p.price
FROM product AS p
WHERE p->belongs_to->category IN (
    SELECT VALUE ->purchased->product->belongs_to->category
    FROM user:current_user
)
AND p.id NOT IN (
    SELECT VALUE ->purchased->product FROM user:current_user
)
ORDER BY p.rating DESC
LIMIT 20;

-- Hybrid: People with similar taste who liked other things
LET $my_likes = SELECT VALUE ->likes->product FROM ONLY user:alice;
LET $similar_users = SELECT
    id,
    count(array::intersect(->likes->product, $my_likes)) AS overlap
FROM user
WHERE id != user:alice
ORDER BY overlap DESC
LIMIT 10;

SELECT
    ->likes->product AS recommended,
    count() AS score
FROM $similar_users
WHERE ->likes->product NOT IN $my_likes
GROUP BY recommended
ORDER BY score DESC
LIMIT 10;
```

### Access Control Graphs

```surrealql
-- Model RBAC as a graph
DEFINE TABLE role SCHEMAFULL;
DEFINE FIELD name ON TABLE role TYPE string;

DEFINE TABLE permission SCHEMAFULL;
DEFINE FIELD resource ON TABLE permission TYPE string;
DEFINE FIELD action ON TABLE permission TYPE string;

DEFINE TABLE has_role SCHEMAFULL;
DEFINE FIELD in ON TABLE has_role TYPE record<user>;
DEFINE FIELD out ON TABLE has_role TYPE record<role>;

DEFINE TABLE grants SCHEMAFULL;
DEFINE FIELD in ON TABLE grants TYPE record<role>;
DEFINE FIELD out ON TABLE grants TYPE record<permission>;

DEFINE TABLE inherits SCHEMAFULL;
DEFINE FIELD in ON TABLE inherits TYPE record<role>;
DEFINE FIELD out ON TABLE inherits TYPE record<role>;

-- Setup hierarchy
CREATE role:admin SET name = 'Admin';
CREATE role:editor SET name = 'Editor';
CREATE role:viewer SET name = 'Viewer';

-- Role inheritance: admin inherits editor inherits viewer
RELATE role:admin->inherits->role:editor;
RELATE role:editor->inherits->role:viewer;

-- Assign permissions
CREATE permission:read_posts SET resource = 'posts', action = 'read';
CREATE permission:write_posts SET resource = 'posts', action = 'write';
CREATE permission:delete_posts SET resource = 'posts', action = 'delete';

RELATE role:viewer->grants->permission:read_posts;
RELATE role:editor->grants->permission:write_posts;
RELATE role:admin->grants->permission:delete_posts;

-- Assign user to role
RELATE user:alice->has_role->role:editor;

-- Check all permissions for a user (including inherited via role hierarchy)
SELECT
    ->has_role->role AS direct_roles,
    ->has_role->role->grants->permission AS direct_permissions,
    ->has_role->role->inherits->role AS inherited_roles,
    ->has_role->role->inherits->role->grants->permission AS inherited_permissions,
    array::flatten([
        ->has_role->role->grants->permission,
        ->has_role->role->inherits->role->grants->permission,
        ->has_role->role->inherits->role->inherits->role->grants->permission
    ]) AS all_permissions
FROM user:alice;

-- Check if user has a specific permission
DEFINE FUNCTION fn::has_permission($user: record<user>, $resource: string, $action: string) {
    LET $all_perms = array::flatten([
        SELECT VALUE ->has_role->role->grants->permission FROM ONLY $user,
        SELECT VALUE ->has_role->role->inherits->role->grants->permission FROM ONLY $user,
        SELECT VALUE ->has_role->role->inherits->role->inherits->role->grants->permission FROM ONLY $user
    ]);
    LET $matching = SELECT * FROM array::flatten($all_perms) WHERE resource = $resource AND action = $action;
    RETURN count($matching) > 0;
};
```

### Hierarchical Data (Org Charts, Categories)

```surrealql
-- Category tree
DEFINE TABLE category SCHEMAFULL;
DEFINE FIELD name ON TABLE category TYPE string;
DEFINE FIELD description ON TABLE category TYPE option<string>;

DEFINE TABLE subcategory_of SCHEMAFULL;
DEFINE FIELD in ON TABLE subcategory_of TYPE record<category>;
DEFINE FIELD out ON TABLE subcategory_of TYPE record<category>;

-- Build category hierarchy
CREATE category:electronics SET name = 'Electronics';
CREATE category:computers SET name = 'Computers';
CREATE category:laptops SET name = 'Laptops';
CREATE category:desktops SET name = 'Desktops';
CREATE category:gaming_laptops SET name = 'Gaming Laptops';

RELATE category:computers->subcategory_of->category:electronics;
RELATE category:laptops->subcategory_of->category:computers;
RELATE category:desktops->subcategory_of->category:computers;
RELATE category:gaming_laptops->subcategory_of->category:laptops;

-- Find all children of a category
SELECT <-subcategory_of<-category.name AS children FROM category:electronics;

-- Find parent chain (breadcrumb)
SELECT
    name,
    ->subcategory_of->category.name AS parent,
    ->subcategory_of->category->subcategory_of->category.name AS grandparent
FROM category:gaming_laptops;

-- Find all descendants (up to 3 levels)
SELECT
    name,
    array::flatten([
        <-subcategory_of<-category,
        <-subcategory_of<-category<-subcategory_of<-category,
        <-subcategory_of<-category<-subcategory_of<-category<-subcategory_of<-category
    ]) AS all_descendants
FROM category:electronics;

-- Org chart example
DEFINE TABLE employee SCHEMAFULL;
DEFINE FIELD name ON TABLE employee TYPE string;
DEFINE FIELD title ON TABLE employee TYPE string;
DEFINE FIELD department ON TABLE employee TYPE string;

DEFINE TABLE reports_to SCHEMAFULL;
DEFINE FIELD in ON TABLE reports_to TYPE record<employee>;
DEFINE FIELD out ON TABLE reports_to TYPE record<employee>;

-- Build org chart
CREATE employee:ceo SET name = 'Jane', title = 'CEO', department = 'Executive';
CREATE employee:cto SET name = 'John', title = 'CTO', department = 'Engineering';
CREATE employee:lead SET name = 'Sam', title = 'Tech Lead', department = 'Engineering';
CREATE employee:dev SET name = 'Alex', title = 'Developer', department = 'Engineering';

RELATE employee:cto->reports_to->employee:ceo;
RELATE employee:lead->reports_to->employee:cto;
RELATE employee:dev->reports_to->employee:lead;

-- Full reporting chain upward
SELECT
    name, title,
    ->reports_to->employee.name AS manager,
    ->reports_to->employee->reports_to->employee.name AS skip_manager,
    ->reports_to->employee->reports_to->employee->reports_to->employee.name AS exec
FROM employee:dev;
```

### Dependency Graphs

```surrealql
-- Package dependency management
DEFINE TABLE package SCHEMAFULL;
DEFINE FIELD name ON TABLE package TYPE string;
DEFINE FIELD version ON TABLE package TYPE string;

DEFINE TABLE depends_on SCHEMAFULL;
DEFINE FIELD in ON TABLE depends_on TYPE record<package>;
DEFINE FIELD out ON TABLE depends_on TYPE record<package>;
DEFINE FIELD version_constraint ON TABLE depends_on TYPE string;

-- Create packages and dependencies
CREATE package:app SET name = 'my-app', version = '1.0.0';
CREATE package:framework SET name = 'web-framework', version = '3.2.1';
CREATE package:orm SET name = 'orm-lib', version = '2.1.0';
CREATE package:db_driver SET name = 'db-driver', version = '1.5.0';
CREATE package:logger SET name = 'logger', version = '0.8.0';

RELATE package:app->depends_on->package:framework SET version_constraint = '^3.0.0';
RELATE package:app->depends_on->package:orm SET version_constraint = '^2.0.0';
RELATE package:orm->depends_on->package:db_driver SET version_constraint = '^1.0.0';
RELATE package:framework->depends_on->package:logger SET version_constraint = '^0.5.0';
RELATE package:orm->depends_on->package:logger SET version_constraint = '^0.7.0';

-- Find all transitive dependencies of a package
SELECT
    name,
    ->depends_on->package.name AS direct_deps,
    ->depends_on->package->depends_on->package.name AS transitive_deps,
    array::distinct(array::flatten([
        ->depends_on->package,
        ->depends_on->package->depends_on->package,
        ->depends_on->package->depends_on->package->depends_on->package
    ])) AS all_deps
FROM package:app;

-- Find reverse dependencies (what depends on this package?)
SELECT
    name,
    <-depends_on<-package.name AS depended_on_by,
    <-depends_on<-package<-depends_on<-package.name AS transitive_dependents
FROM package:logger;
-- Shows that both framework and orm (and transitively, app) depend on logger
```

### Workflow and State Machine Patterns

```surrealql
-- State machine for order processing
DEFINE TABLE state SCHEMAFULL;
DEFINE FIELD name ON TABLE state TYPE string;
DEFINE FIELD description ON TABLE state TYPE string;

DEFINE TABLE transition SCHEMAFULL;
DEFINE FIELD in ON TABLE transition TYPE record<state>;
DEFINE FIELD out ON TABLE transition TYPE record<state>;
DEFINE FIELD action ON TABLE transition TYPE string;
DEFINE FIELD guard ON TABLE transition TYPE option<string>;

-- Define states
CREATE state:draft SET name = 'Draft', description = 'Order not yet submitted';
CREATE state:pending SET name = 'Pending', description = 'Awaiting approval';
CREATE state:approved SET name = 'Approved', description = 'Order approved';
CREATE state:shipped SET name = 'Shipped', description = 'Order in transit';
CREATE state:delivered SET name = 'Delivered', description = 'Order received';
CREATE state:cancelled SET name = 'Cancelled', description = 'Order cancelled';

-- Define transitions
RELATE state:draft->transition->state:pending SET action = 'submit';
RELATE state:pending->transition->state:approved SET action = 'approve', guard = 'role:manager';
RELATE state:pending->transition->state:cancelled SET action = 'cancel';
RELATE state:approved->transition->state:shipped SET action = 'ship';
RELATE state:shipped->transition->state:delivered SET action = 'deliver';
RELATE state:approved->transition->state:cancelled SET action = 'cancel';

-- Find valid transitions from current state
SELECT
    ->transition->state.name AS next_states,
    ->transition.action AS available_actions
FROM state:pending;

-- Check if a transition is valid
DEFINE FUNCTION fn::can_transition($current: record<state>, $action: string) {
    LET $valid = SELECT * FROM transition
        WHERE in = $current AND action = $action;
    RETURN count($valid) > 0;
};

-- Apply a state transition to an order
DEFINE FUNCTION fn::apply_transition($order: record<order>, $action: string) {
    LET $current_state = (SELECT VALUE current_state FROM ONLY $order);
    LET $next = SELECT VALUE out FROM transition
        WHERE in = $current_state AND action = $action
        LIMIT 1;
    IF count($next) = 0 {
        THROW "Invalid transition: cannot " + $action + " from current state";
    };
    UPDATE $order SET
        current_state = $next[0],
        updated_at = time::now();
};
```

---

## Graph Gotchas

Graph-specific footguns verified in SurrealDB 3.1. For the full cross-domain
gotchas catalog (vector, security, MCP, migration, SDKs), see
`rules/gotchas.md`. Recommend **v3.1.4+** for production graph workloads.

### Inline edge filters (fixed v3.1.3)

Parenthesised edge filters now work reliably:

```surrealql
-- Returns matching edges (was empty on 3.1.0–3.1.2)
SELECT * FROM person:1->(knows WHERE since > d'2020-01-01');
```

Prefer this form over post-filtering when the predicate applies to edge fields.

### `$parent` scope in nested graph WHERE (fixed v3.1.0)

In subqueries inside graph traversals, `$parent` refers to the **current SELECT
row**, not an outer FOR/IF scope. `FROM ONLY $parent->edge->target` now
propagates `ONLY` and respects `ORDER BY` / `WHERE` on the traversal path
([PR #7194](https://github.com/surrealdb/surrealdb/pull/7194)).

### RELATION + partial UNIQUE index (fixed v3.1.0)

A three-field UNIQUE index on a RELATION table with a WHERE clause that only
binds two fields via `type::record()` could return zero rows while traversal
still worked ([#7280](https://github.com/surrealdb/surrealdb/issues/7280)).
After upgrade, verify with `EXPLAIN`; prefer indexing the full composite key.

### Single-scan traversals (v3.1.0 perf)

When permissions allow, `->edge->vertex` traversals use a single scan instead
of two. Deep multi-hop queries benefit without query changes.

### Record links vs graph edges (modeling)

Official guidance ([record links vs graph relations](https://surrealdb.com/docs/learn/data-models/graph/record-links-vs-graph-relations)):

| Pattern | Use when |
|---|---|
| Record link field | Simple reference, no edge metadata, single hop |
| Record reference (`DEFINE FIELD … TYPE record<table>`) | Typed FK-style reference |
| `TYPE RELATION` + `RELATE` | Edge properties, multi-hop analytics, Surrealist graph designer |

Use `ENFORCED` on relation tables when referential integrity matters. Set
`TIMEOUT` on recursive traversals (max depth 256).

### Agent memory + knowledge graph (demo pattern)

The upstream [`surrealdb/agent-memory`](https://github.com/surrealdb/agent-memory)
demo combines graph edges and vector search for agent memory. It requires
experimental flags and API keys — treat as a **reference architecture**, not a
production template. Stable building blocks: `rules/graph-queries.md`,
`rules/vector-search.md`, `rules/security.md`, built-in MCP or `surrealmcp`.

### Official video references

- [Record IDs, Expressions and Graphs (Stream #10)](https://www.youtube.com/watch?v=VFXXEn40GCA) — record links vs edges, bidirectional traversal
- [Graph-Style Relationships](https://www.youtube.com/watch?v=zwQwKvMa9sU) — RELATE and arrow syntax
- [Surrealist Tips: GraphQL](https://www.youtube.com/watch?v=jmFPjyiJEeI) — note Apollo naming breaking changes in 3.1

For MCP, DiskANN, and observability, prefer written [Release 3.1](https://surrealdb.com/releases/3.1) docs over pre-3.1 video content.

---

## Performance Considerations

### Graph Index Strategies

```surrealql
-- Index edge table fields for faster traversal
DEFINE INDEX idx_knows_in ON TABLE knows COLUMNS in;
DEFINE INDEX idx_knows_out ON TABLE knows COLUMNS out;
DEFINE INDEX idx_knows_in_out ON TABLE knows COLUMNS in, out UNIQUE;

-- Index edge properties used in filtered traversals
DEFINE INDEX idx_knows_since ON TABLE knows COLUMNS since;
DEFINE INDEX idx_knows_strength ON TABLE knows COLUMNS strength;

-- Composite index for common filter patterns
DEFINE INDEX idx_manages_role ON TABLE manages COLUMNS in, role;
```

### Traversal Depth Limits

Deep traversals can be expensive. Limit depth and result sets.

```surrealql
-- Limit results at each hop
SELECT ->(knows LIMIT 10)->person FROM person:alice;

-- Use LIMIT on the outer query
SELECT ->knows->person->knows->person AS fof
FROM person:alice
LIMIT 50;

-- Avoid unbounded multi-hop chains in production
-- BAD: unlimited depth chain
-- SELECT ->knows->person->knows->person->knows->person->knows->person->... FROM person:alice;

-- GOOD: bounded depth with explicit limits
SELECT
    ->knows->(person LIMIT 20) AS depth_1
FROM person:alice;
```

### Caching Patterns for Frequent Traversals

```surrealql
-- Precompute common graph aggregates
DEFINE EVENT update_friend_count ON TABLE knows WHEN $event = "CREATE" THEN {
    UPDATE $after.in SET friend_count += 1;
};

DEFINE EVENT decrement_friend_count ON TABLE knows WHEN $event = "DELETE" THEN {
    UPDATE $before.in SET friend_count -= 1;
};

-- Materialized view pattern: store computed traversal results
DEFINE TABLE user_stats SCHEMAFULL;
DEFINE FIELD user ON TABLE user_stats TYPE record<person>;
DEFINE FIELD friend_count ON TABLE user_stats TYPE int;
DEFINE FIELD follower_count ON TABLE user_stats TYPE int;
DEFINE FIELD following_count ON TABLE user_stats TYPE int;

-- Periodically refresh with a function
DEFINE FUNCTION fn::refresh_user_stats($user: record<person>) {
    UPSERT user_stats SET
        user = $user,
        friend_count = count((SELECT ->friends_with->person FROM ONLY $user)),
        follower_count = count((SELECT <-follows<-person FROM ONLY $user)),
        following_count = count((SELECT ->follows->person FROM ONLY $user));
};
```

### General Tips

- Index the `in` and `out` columns on edge tables for faster traversal lookups.
- For large graphs, prefer shallow traversals (1-2 hops) and use application logic or stored functions for deeper searches.
- Use `LIMIT` within filtered traversals to cap intermediate result sets.
- Avoid cartesian explosions: chaining multiple multi-target traversals can produce exponentially large intermediate results.
- Use SCHEMAFULL edge tables with typed `in`/`out` fields to prevent invalid relationships and improve query planning.
- Consider precomputing and caching graph metrics (degree, centrality) on the node records themselves if they are queried frequently.
- Use `EXPLAIN` (covered in the performance rules) to understand traversal query plans.
