---
name: vector-indexing
description: How to enable and query vector indexes for similarity search in Harper.
metadata:
  mode: generate
  sources:
    - reference/v5/database/schema.md#Vector Indexing
  sourceCommit: 4fe4c9c95e0974eaa77032f6f10e36fbd8ec64ac
  inputHash: d90b1b74597d08a6
---

# Vector Indexing

Instructions for the agent to enable HNSW vector indexes on table fields and query them for similarity search in Harper.

## When to Use

Apply this rule when adding a vector similarity search capability to a Harper table — for example, storing text embeddings and querying for nearest neighbors, filtering by distance threshold, or tuning index construction and search parameters. Use it alongside [adding-tables-with-schemas.md](adding-tables-with-schemas.md) when defining the schema that hosts the vector field.

## How It Works

1. **Declare the vector index on a field**: Add `@indexed(type: "HNSW")` to a `[Float]` field inside a `@table` type. This creates an HNSW (Hierarchical Navigable Small World) index for approximate nearest-neighbor search.

   ```graphql
   type Document @table {
   	id: Long @primaryKey
   	textEmbeddings: [Float] @indexed(type: "HNSW")
   }
   ```

2. **Query by nearest neighbors using `sort`**: Call `.search()` with a `sort` descriptor that specifies the indexed `attribute` and a `target` vector. Use `limit` to cap results.

   ```javascript
   let results = Document.search({
   	sort: { attribute: 'textEmbeddings', target: searchVector },
   	limit: 5,
   });
   ```

3. **Combine with filter conditions**: Add a `conditions` array alongside `sort` to pre-filter records before ranking by similarity.

   ```javascript
   let results = Document.search({
   	conditions: [{ attribute: 'price', comparator: 'lt', value: 50 }],
   	sort: { attribute: 'textEmbeddings', target: searchVector },
   	limit: 5,
   });
   ```

4. **Filter by distance threshold**: To return only records within a similarity cutoff (without ranking), place `target` directly on the condition alongside `comparator` and `value`. This bounds result quality rather than ranking by similarity.

   ```javascript
   let results = Document.search({
   	conditions: {
   		attribute: 'textEmbeddings',
   		comparator: 'lt',
   		value: 0.1,
   		target: searchVector,
   	},
   });
   ```

5. **Include computed distance in results**: Use the special `$distance` field in `select` to return the distance from the target vector. Available in both `sort`-based and threshold-based queries.

   ```javascript
   let results = Document.search({
   	select: ['name', '$distance'],
   	sort: { attribute: 'textEmbeddings', target: searchVector },
   	limit: 5,
   });
   ```

6. **Tune per-query search options**: Pass `distance` and `ef` directly on the `sort` descriptor to override index defaults for a single query.

   ```javascript
   let results = Document.search({
   	sort: { attribute: 'textEmbeddings', target: searchVector, distance: 'dotProduct', ef: 200 },
   	limit: 5,
   });
   ```

   - `distance` — overrides the distance function for this query: `"cosine"`, `"euclidean"`, or `"dotProduct"`.
   - `ef` — overrides the search exploration budget. Higher values improve recall at the cost of latency.

7. **Configure HNSW index parameters**: Pass parameters directly in the `@indexed` directive. Structural parameters (`distance`, `M`, `efConstruction`, `quantization`) trigger an index rebuild when changed; `efConstructionSearch` does not.

   ```graphql
   type Document @table {
   	id: Long @primaryKey
   	textEmbeddings: [Float]
   		@indexed(type: "HNSW", distance: "euclidean", optimizeRouting: 0, efConstructionSearch: 100)
   }
   ```

8. **Enable vector quantization**: Use `quantization: "int8"` to store vectors as 8-bit integers, reducing index size and memory usage. Harper re-ranks nearest-neighbor `sort` results against full-precision vectors automatically.

   ```graphql
   type Document @table {
   	id: Long @primaryKey
   	textEmbeddings: [Float] @indexed(type: "HNSW", quantization: "int8")
   }
   ```

## Examples

Full schema with custom HNSW parameters and a nearest-neighbor query with distance output:

```graphql
type Document @table {
	id: Long @primaryKey
	textEmbeddings: [Float]
		@indexed(type: "HNSW", distance: "euclidean", optimizeRouting: 0, efConstructionSearch: 100)
}
```

```javascript
// Nearest-neighbor search with distance scores
let results = Document.search({
	select: ['name', '$distance'],
	sort: { attribute: 'textEmbeddings', target: searchVector },
	limit: 5,
});

// Distance-threshold query (no ranking)
let closeMatches = Document.search({
	conditions: {
		attribute: 'textEmbeddings',
		comparator: 'lt',
		value: 0.1,
		target: searchVector,
	},
});
```

## Notes

### HNSW Parameters

| Parameter              | Default           | Description                                                                                            |
| ---------------------- | ----------------- | ------------------------------------------------------------------------------------------------------ |
| `distance`             | `"cosine"`        | Distance function: `"cosine"`, `"euclidean"`, or `"dotProduct"`                                        |
| `efConstruction`       | `100`             | Max nodes explored during index construction. Higher = better recall, lower = better performance       |
| `M`                    | `16`              | Preferred connections per graph layer. Higher = more space, better recall for high-dimensional data    |
| `optimizeRouting`      | `0.5`             | Heuristic aggressiveness for omitting redundant connections (0 = off, 1 = most aggressive)             |
| `mL`                   | computed from `M` | Normalization factor for level generation                                                              |
| `efConstructionSearch` | auto-scaled       | Max nodes explored during search. When unset, auto-scales with index size; setting it fixes the budget |
| `quantization`         | —                 | `"int8"` stores vectors quantized to int8                                                              |

- The `distance` option on a per-query `sort` descriptor accepts `"cosine"`, `"euclidean"`, or `"dotProduct"`.
- When no `ef` is passed and `efConstructionSearch` (or `efConstruction`) is not explicitly set on the index, the search budget auto-scales with index size.
- `efConstruction` seeds the initial value of `efConstructionSearch`; setting either one fixes the search budget.
- The correct parameter name is `efConstructionSearch` (not `efSearchConstruction`).
- `$distance` is available in both `sort`-based ranking and `conditions`-based threshold queries.
- For `quantization: "int8"`, distance-threshold (`lt`/`le`) queries filter on approximate distance; `sort` queries re-rank against full-precision vectors.
