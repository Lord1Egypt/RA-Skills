# Common Query Patterns

## 1. Load a document skeleton for tree reconstruction
```sql
SELECT node_id, parent_id, structure, title, summary, node_order
FROM pageindex_nodes
WHERE workspace = $1 AND doc_id = $2
ORDER BY parent_id NULLS FIRST, node_order ASC;
```

## 2. Fetch node content for answer generation
```sql
SELECT n.node_id, n.title, n.summary, c.content
FROM pageindex_nodes n
JOIN pageindex_node_contents c ON n.node_id = c.node_id
WHERE n.workspace = $1 AND n.node_id = ANY($2);
```

## 3. Find anchor nodes from entity hits
```sql
SELECT DISTINCT node_id
FROM pageindex_entities
WHERE workspace = $1 AND canonical_name = ANY($2);
```

## 4. Find anchor nodes from relationship keywords
```sql
SELECT DISTINCT r.node_id
FROM pageindex_relationships r
WHERE r.workspace = $1
  AND EXISTS (
      SELECT 1
      FROM unnest(r.keywords) AS keyword
      WHERE lower(keyword) = ANY($2)
  );
```

## 5. Example hybrid lookup
```sql
SELECT n.title, n.summary, c.content
FROM pageindex_nodes n
JOIN pageindex_node_contents c ON n.node_id = c.node_id
WHERE n.workspace = $1
  AND n.node_id IN (
      SELECT DISTINCT node_id
      FROM pageindex_entities
      WHERE workspace = $1 AND canonical_name = ANY($2)
      UNION
      SELECT DISTINCT r.node_id
      FROM pageindex_relationships r
      WHERE r.workspace = $1
        AND EXISTS (
            SELECT 1
            FROM unnest(r.keywords) AS keyword
            WHERE lower(keyword) = ANY($2)
        )
  );
```
