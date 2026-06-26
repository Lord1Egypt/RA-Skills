# SurrealDB Vector Search

SurrealDB provides native vector storage and similarity search capabilities, making it suitable for AI/ML applications including RAG (Retrieval-Augmented Generation), semantic search, recommendations, and classification. Vectors are stored as array fields and searched using **HNSW** or **DiskANN** indexes with the same `<|K, EF|>` KNN operator (since v3.1.0).

---

## Vector Storage

### Storing Embeddings as Arrays

Vectors in SurrealDB are stored as standard array fields. Use typed array fields with float elements for embeddings.

```surrealql
-- Basic vector storage
CREATE document:1 SET
    title = 'Introduction to SurrealDB',
    content = 'SurrealDB is a multi-model database...',
    embedding = [0.123, -0.456, 0.789, ...];

-- With explicit type definitions
DEFINE TABLE document SCHEMAFULL;
DEFINE FIELD title ON TABLE document TYPE string;
DEFINE FIELD content ON TABLE document TYPE string;
DEFINE FIELD embedding ON TABLE document TYPE array<float>;
DEFINE FIELD metadata ON TABLE document TYPE object;
DEFINE FIELD created_at ON TABLE document TYPE datetime DEFAULT time::now();

-- Store a high-dimensional embedding (e.g., OpenAI text-embedding-3-large)
CREATE document:2 SET
    title = 'Vector Search Guide',
    content = 'This guide covers vector similarity...',
    embedding = [0.0012, -0.0034, 0.0056, ...],  -- 3072 dimensions
    metadata = { source: 'docs', chunk_index: 0 };
```

### Dimension Specifications

The embedding dimension must match the HNSW index definition exactly. Common dimensions from popular embedding models:

| Model | Dimensions |
|---|---|
| OpenAI text-embedding-3-small | 1536 |
| OpenAI text-embedding-3-large | 3072 |
| Cohere embed-v4 | 1024 |
| Mistral Embed | 1024 |
| Google text-embedding-005 | 768 |
| BAAI/bge-large-en-v1.5 | 1024 |
| all-MiniLM-L6-v2 | 384 |

```surrealql
-- Dimension must match between data and index
-- If your embedding model outputs 1536 dimensions:
DEFINE INDEX idx_embed ON TABLE document FIELDS embedding HNSW DIMENSION 1536;

-- Inserting a vector of wrong dimension will cause an index error
-- BAD: 768-dim vector into 1536-dim index
-- GOOD: ensure all vectors match the declared dimension
```

### Supported Data Types for Vectors

```surrealql
-- Float arrays (most common, default)
DEFINE FIELD embedding ON TABLE document TYPE array<float>;

-- The HNSW TYPE parameter controls storage precision in the index:
-- F32 (default) - 32-bit floating point, best accuracy
-- F64 - 64-bit floating point, highest precision, more memory
-- I16 - 16-bit integer, quantized, less memory
-- I32 - 32-bit integer

-- Example with explicit index type
DEFINE INDEX idx_embed ON TABLE document
    FIELDS embedding
    HNSW DIMENSION 1536 DIST COSINE TYPE F32;
```

---

## Index Types

### HNSW (Hierarchical Navigable Small World)

HNSW is the default vector index type for most workloads. It builds a multi-layered graph structure for approximate nearest neighbor search with sub-linear query time.

Note: MTREE was deprecated in SurrealDB 2.x and removed in 3.x.

### DiskANN (since v3.1.0)

DiskANN is an alternative vector index optimized for large, disk-backed datasets. It uses the **same** `<|K, EF|>` query operator as HNSW — only the `DEFINE INDEX` clause differs.

```surrealql
DEFINE INDEX idx_doc_diskann ON TABLE document
    FIELDS embedding
    DISKANN DIMENSION 1536 DIST COSINE TYPE F32 DEGREE 16 L_BUILD 64;

-- Query shape is identical to HNSW
SELECT *, embedding <|10, 40|> $query_vec AS score
FROM document
WHERE embedding <|10, 40|> $query_vec
ORDER BY score DESC
LIMIT 10;
```

| Consideration | HNSW | DiskANN |
|---|---|---|
| Best for | General-purpose ANN, in-memory or mixed | Very large indexes where graph lives primarily on disk |
| Platform | All supported targets | **64-bit only** (gated in v3.1.3+) |
| WASM / browser | Supported (subject to engine limits) | **Not supported** |
| Key params | `M`, `M0`, `LM`, `EFC`, `HASHED_VECTOR` | `DEGREE`, `L_BUILD` |

Choose HNSW unless profiling shows DiskANN wins on your dataset size and storage layout. See [Release 3.1](https://surrealdb.com/releases/3.1) for full parameter tables.

#### Full Configuration Options

```surrealql
DEFINE INDEX index_name ON TABLE table_name FIELDS field_name
    HNSW DIMENSION dim
    [DIST distance_function]
    [TYPE storage_type]
    [EFC construction_ef]
    [M max_connections]
    [M0 max_connections_layer0]
    [LM level_multiplier]
    [EXTEND_CANDIDATES]
    [KEEP_PRUNED_CONNECTIONS]
    [HASHED_VECTOR];
```

| Parameter | Description | Default | Guidance |
|---|---|---|---|
| DIMENSION | Vector dimensionality (must match data) | Required | Match your embedding model |
| DIST | Distance function: COSINE, EUCLIDEAN, MANHATTAN, MINKOWSKI, CHEBYSHEV, HAMMING, JACCARD, PEARSON | EUCLIDEAN | COSINE for normalized embeddings (most common) |
| TYPE | Storage type: F32, F64, I16, I32, I64 | F32 | F32 balances precision and memory |
| EFC | ef_construction: neighbors explored during build | 150 | Higher = better recall, slower build |
| M | Max connections per node (upper layers) | 12 | Higher = better recall, more memory |
| M0 | Max connections at layer 0 (the densest layer) | `2*M` | Usually leave as default |
| LM | HNSW level multiplier (`ml`); controls layer-assignment probability | `1 / ln(M)` (~0.402 at M=12) | Leave at default unless you've profiled the layer distribution |
| EXTEND_CANDIDATES | Extend candidate list during construction | Off | Enable for higher recall |
| KEEP_PRUNED_CONNECTIONS | Keep pruned connections | Off | Enable for higher recall |
| HASHED_VECTOR | Use hashed vector representation for retrieval (memory-optimised) | Off | Enable on large indexes where vector storage memory is the bottleneck |

> **HNSW parameter precision (verified at v3.0.5 — see
> `surrealdb/core/src/sql/statements/define/index.rs` and the
> `HnswParams` struct).** `M0` and `LM` are two **different** clauses
> on the parser side, with no relationship to each other or to the
> distance metric:
>
> - `M0 <n>` sets the maximum number of bidirectional connections at
>   layer 0 (the densest graph layer). Default `2*M`.
> - `LM <n>` sets the **HNSW level multiplier** (`ml` in the original
>   paper), used in the formula `l ← ⌊−ln(unif(0..1)) · ml⌋` to assign
>   each new point an insertion level. Default `1 / ln(M)` (≈0.402 at
>   `M=12`). Increasing `LM` makes the hierarchy flatter (more points
>   at higher layers); decreasing it makes the hierarchy taller.
>
> The Minkowski distance order is **not** controlled by `LM`. It is
> specified inline in the `DIST` clause: `DIST MINKOWSKI 3`. The
> upstream parser source (`Distance::Minkowski(distance)`) reads the
> order as the next token after the `MINKOWSKI` keyword.
>
> Pre-v1.5.3 revisions of this rule (and the v1.5.1 patch) labelled
> `LM` as "Minkowski distance order" — that label was wrong. If you
> copied an `HNSW ... LM N` snippet from those revisions thinking you
> were setting Minkowski order, you were silently setting the level
> multiplier instead (often dramatically flattening the HNSW
> hierarchy). To set a Minkowski distance order, write `DIST MINKOWSKI
> N`, not `LM N`. To set layer-0 connections, write `M0 N`.

> **`HASHED_VECTOR` storage semantics (verified at v3.0.5).** The
> bare `HASHED_VECTOR` keyword (no value — see parser
> `core/src/syn/parser/stmt/define.rs:1151-1154`) flips a bool
> (`use_hashed_vector`, default `false` at `:1114`) that changes
> how the **vector → document-IDs** lookup table is keyed. It does
> NOT quantise vectors, change graph storage, or alter search
> precision:
>
> - **Default (off):** the vec→docs lookup table is keyed by the
>   full serialised vector via `new_hv_key(&ser_vec)`
>   (`core/src/idx/mod.rs:115`). Per-entry KV key cost scales
>   with `dimension * sizeof(TYPE)` (e.g. ~6 KB per entry at
>   `DIMENSION 1536 TYPE F32`).
> - **With `HASHED_VECTOR`:** the vec→docs lookup table is keyed
>   by a constant 32-byte hash via
>   `new_hh_key(hash: [u8; 32])` (`core/src/idx/mod.rs:119`).
>   Hash collisions are tolerated by bucketing distinct vectors
>   under the same key with exact-match scan inside the bucket
>   (`ElementHashedDocs` / `get_element_docs(&ser_vec)`,
>   `core/src/idx/trees/hnsw/docs.rs:281-440`).
>
> Enable on large indexes where the vec→docs lookup table is the
> memory bottleneck — the per-entry KV key shrinks from
> `dimension * sizeof(TYPE)` bytes to a constant 32 bytes,
> independent of dimension. The tradeoff is an extra
> in-bucket scan when distinct vectors collide on the hash; for a
> good hash and reasonably distinct vectors this is negligible.
> The HNSW graph storage itself (graph edges, ef-construction
> state, the vectors used at search time) is unchanged. The
> keyword takes no argument: write
> `HNSW DIMENSION 1536 DIST COSINE HASHED_VECTOR`, not
> `HASHED_VECTOR true`.

#### Common Index Configurations

```surrealql
-- Standard cosine similarity index (most common for text embeddings)
DEFINE INDEX idx_doc_embedding ON TABLE document
    FIELDS embedding
    HNSW DIMENSION 1536 DIST COSINE;

-- High-recall configuration for critical search
DEFINE INDEX idx_high_recall ON TABLE document
    FIELDS embedding
    HNSW DIMENSION 1536
    DIST COSINE
    TYPE F32
    EFC 300
    M 32
    EXTEND_CANDIDATES
    KEEP_PRUNED_CONNECTIONS;

-- Memory-efficient configuration for large datasets
DEFINE INDEX idx_compact ON TABLE document
    FIELDS embedding
    HNSW DIMENSION 384
    DIST COSINE
    TYPE I16
    EFC 100
    M 8;

-- Euclidean distance for spatial/geometric data
DEFINE INDEX idx_spatial ON TABLE location
    FIELDS coordinates
    HNSW DIMENSION 3 DIST EUCLIDEAN;

-- Manhattan distance for grid-based or feature-counting data
DEFINE INDEX idx_features ON TABLE item
    FIELDS feature_vector
    HNSW DIMENSION 128 DIST MANHATTAN;
```

#### When to Use HNSW

HNSW is the right choice for all vector search workloads in SurrealDB 3.x. It provides:

- Sub-linear query time (logarithmic in dataset size)
- High recall rates (typically 95-99% with good parameters)
- Good performance on high-dimensional data
- Support for incremental inserts without full rebuild

Trade-offs to be aware of:

- Memory usage scales with M and dimension count
- Build time increases with EFC and dataset size
- Approximate results (not exact KNN) -- tune EFC and M for desired recall

### MTREE (Removed in 3.x)

MTREE was deprecated in SurrealDB 2.x and fully removed in SurrealDB 3.x. If migrating from 2.x, replace all MTREE index definitions with HNSW.

```surrealql
-- OLD (SurrealDB 2.x) - no longer works
-- DEFINE INDEX idx ON TABLE doc FIELDS embedding MTREE DIMENSION 1536;

-- NEW (SurrealDB 3.x) - use HNSW instead
DEFINE INDEX idx ON TABLE doc FIELDS embedding HNSW DIMENSION 1536 DIST COSINE;
```

---

## Search Patterns

### Basic KNN Search

The `<|K|>` operator performs K-nearest-neighbor search using the defined HNSW index.

```surrealql
-- Create index
DEFINE INDEX idx_embedding ON TABLE document
    FIELDS embedding
    HNSW DIMENSION 1536 DIST COSINE;

-- Insert documents with embeddings
CREATE document:1 SET title = 'SurrealDB Intro', embedding = [...];
CREATE document:2 SET title = 'Graph Databases', embedding = [...];
CREATE document:3 SET title = 'Vector Search', embedding = [...];

-- Find 10 nearest neighbors
LET $query_vector = [0.012, -0.034, 0.056, ...];  -- 1536 dimensions

SELECT
    id,
    title,
    vector::distance::knn() AS distance
FROM document
WHERE embedding <|10|> $query_vector
ORDER BY distance;
```

### KNN with Distance Threshold

```surrealql
-- Find 10 nearest neighbors within a maximum distance of 40
LET $query_vector = [0.012, -0.034, 0.056, ...];

SELECT
    id,
    title,
    vector::distance::knn() AS distance
FROM document
WHERE embedding <|10, 40|> $query_vector
ORDER BY distance;
```

### Vector Similarity Functions

SurrealDB provides built-in vector distance and similarity functions.

```surrealql
-- Cosine similarity (1 = identical, 0 = orthogonal, -1 = opposite)
SELECT
    id, title,
    vector::similarity::cosine(embedding, $query_vector) AS similarity
FROM document
ORDER BY similarity DESC
LIMIT 10;

-- Euclidean distance (0 = identical, higher = more different)
SELECT
    id, title,
    vector::distance::euclidean(embedding, $query_vector) AS distance
FROM document
ORDER BY distance ASC
LIMIT 10;

-- Manhattan distance
SELECT
    id, title,
    vector::distance::manhattan(embedding, $query_vector) AS distance
FROM document
ORDER BY distance ASC
LIMIT 10;

-- Chebyshev distance
SELECT
    id, title,
    vector::distance::chebyshev(embedding, $query_vector) AS distance
FROM document
ORDER BY distance ASC;

-- Hamming distance (for binary/integer vectors)
SELECT
    id,
    vector::distance::hamming(binary_features, $query_features) AS distance
FROM item
ORDER BY distance ASC;

-- Minkowski distance (generalised Lp norm; takes order as 3rd arg)
-- p=1 is equivalent to Manhattan; p=2 is equivalent to Euclidean;
-- as p grows, the metric weights larger-component differences more heavily,
-- with the limiting case (p -> infinity) approaching Chebyshev.
SELECT
    id, title,
    vector::distance::minkowski(embedding, $query_vector, 3) AS distance
FROM document
ORDER BY distance ASC
LIMIT 10;

-- Jaccard similarity over numeric token IDs (set semantics after dedup)
-- Note: vector::similarity::jaccard dispatches as (Vec<Number>, Vec<Number>)
-- per core/src/fnc/vector.rs:130. String tag arrays will fail runtime
-- coercion; map your tokens to stable numeric IDs first.
-- Wrap both arguments in array::distinct(...) to neutralise the v3.0.5
-- multiset-asymmetric numerator (see callout below) and keep scores in [0, 1].
LET $query_tag_ids = array::distinct([101, 205, 309]);

SELECT
    id, name,
    vector::similarity::jaccard(
        array::distinct(tag_ids),
        $query_tag_ids
    ) AS similarity
FROM article
ORDER BY similarity DESC
LIMIT 10;

-- Pearson correlation similarity (range [-1, 1]; mean-shift tolerant)
SELECT
    id, name,
    vector::similarity::pearson(rating_vector, $query_ratings) AS similarity
FROM user_profile
ORDER BY similarity DESC
LIMIT 10;
```

> **`vector::similarity::jaccard()` and `vector::similarity::pearson()`
> — appropriate use (verified at v3.0.5).** These two standalone
> functions return **similarities** (larger = more similar),
> unlike every `vector::distance::*` function above (smaller =
> closer). Source: `core/src/fnc/vector.rs:130-136` →
> `core/src/fnc/util/math/vector.rs:120-126` (jaccard) and
> `:132-147` (pearson).
>
> - `vector::similarity::jaccard(a, b)` dispatches as
>   `(Vec<Number>, Vec<Number>)` at
>   `core/src/fnc/vector.rs:130` — **numeric arrays only**;
>   string-token arrays fail runtime coercion via
>   `core/src/val/value/convert/coerce.rs`. Map your tokens to
>   stable numeric IDs first. **Implementation quirk (v3.0.5):**
>   the function does NOT compute textbook set Jaccard
>   `|A ∩ B| / |A ∪ B|`. Per
>   `core/src/fnc/util/math/vector.rs:120-126` it builds a
>   `union: HashSet<&Number>` from the first argument, then
>   counts every element of the second argument whose
>   `union.insert(n)` returns `false` (i.e. was already in the
>   running union — either originally from `a` or from an
>   earlier iteration of `b`). The denominator is the final
>   `union.len()` (deduped). The numerator is therefore
>   **multiset-weighted on the second argument (`b`)**: intra-array
>   duplicates in `b` are double-counted. Concrete divergence:
>   `vector::similarity::jaccard([1], [1, 1])` returns `2.0`,
>   not `1.0`. Pre-deduplicate both inputs (`array::distinct(...)`)
>   for textbook set-Jaccard semantics; otherwise the score is
>   **`[0, |b|]`-bounded**, not `[0, 1]`-bounded. Both inputs
>   empty yields `NaN` (`0 / 0`). Fixture coverage
>   (`core/tests/function.rs:3470-3484`) only exercises distinct
>   element vectors, where the multiset and set forms agree.
>   Suitable for **deduped numeric discrete-token vectors** —
>   stable tag IDs, sparse feature-id lists, hash-bucket
>   indicators — when callers ensure both inputs are
>   `array::distinct`-cleaned. NOT suitable for dense
>   floating-point embeddings: every element of a typical
>   embedding is effectively unique under set equality, so the
>   ratio degenerates and the metric is no longer meaningful.
> - `vector::similarity::pearson(a, b)` computes the Pearson
>   correlation coefficient
>   (`covar / (std_dev_a * std_dev_b)`). Range `[-1, 1]` for
>   finite, non-zero-variance inputs. **Edge cases:** for
>   exact constant operands whose `mean()` round-trip
>   recovers the same value, every centered term
>   `(a_i − mean(a)) * (b_i − mean(b))` is exactly `0.0`,
>   so covariance is also `0.0` and the result is
>   `0 / 0 = NaN`. This constant-operand sub-case cannot
>   produce `Infinity` (the simultaneous collapse forces a
>   `0 / 0` form). A separate f64 underflow regime — where
>   centered squared terms underflow to `0` while pairwise
>   products do not — can still drive `std_dev` to `0.0`
>   with non-zero covariance, producing `±Infinity` instead
>   of `NaN`; see the **Pearson zero-denominator path
>   divergence** callout below for the worked example. This zero-deviation path is reachable
>   for **integer** constant operands (e.g. `[1, 1, 1]`, where
>   `mean()` returns `1` exactly and each `x_i − mean` is
>   exactly `0.0`); for **some floating-point** constant
>   operands the zero-deviation `NaN` path is NOT taken.
>   This is **literal-dependent**: it depends on whether
>   the f64 sum-and-divide round-trip recovers the same f64
>   bit-pattern as the original element. Concretely, for
>   `[0.1, 0.1, 0.1]`, `mean()` accumulates via `try_add` to
>   the next f64 above `0.1`
>   (`0.10000000000000002`), so each `x_i − mean` is a
>   non-zero ~1e-17 and `std_dev_a` is a tiny positive
>   value — finite path. But for constants whose 3-element
>   f64 sum-and-divide DOES round-trip exactly to the same
>   element bit-pattern — e.g. `[0.3, 0.3, 0.3]`,
>   `[0.5, 0.5, 0.5]`, `[0.25, 0.25, 0.25]` — every
>   `x_i − mean` is exactly `0.0`, `deviation()` returns
>   `0.0`, and the result is back on the `0 / 0 = NaN`
>   path. Treat the float-constant outcome as
>   **value-dependent** rather than uniformly finite or
>   uniformly NaN. When a float constant DOES dodge the
>   zero-deviation path (e.g. the `0.1` case above), the
>   final ratio depends on the OTHER operand: identical
>   non-roundtrip-float-constant pairs
>   (e.g. `pearson([0.1, 0.1, 0.1], [0.1, 0.1, 0.1])`)
>   reduce to a `(σ²) / (σ * σ)` ratio that is `≈ 1.0`
>   modulo a possible 1-ulp `sqrt`-then-multiply rounding;
>   one such constant paired with one non-constant collapses
>   toward `≈ 0` — algebraically `Σ(b_i − mean(b)) = 0`, but
>   in f64 the rounded residual need not be exactly zero
>   (e.g. `b = [0.1, 0.2, 0.3]` has `mean(b) =
>   0.20000000000000004` and a residual sum of ~`-1.11e-16`),
>   so the numerator is `O(ε × |a|) ×` that rounded residual
>   — not literally `0` but bounded by ~`ε² × |a| × |b|`.
>   The final ratio after dividing by the tiny `std_dev(a)`
>   resolves to roughly `ε`-scale (Codex pass-3 trace example
>   `pearson([0.1, 0.1, 0.1], [0.1, 0.2, 0.3])` returns
>   `~4.53e-16`); one
>   **float**-constant paired with one **integer**-constant
>   operand still hits `NaN` because the integer side has
>   exact zero variance regardless of whether the float side
>   does. **Decimal-typed operands**
>   (e.g. `[0.1dec, 0.1dec, 0.1dec]`, or fields declared
>   `array<decimal>`) route through the `Decimal` branches
>   of `mean()` and `Number::try_add` and can keep the mean
>   exact — that puts them back on the integer-style
>   zero-deviation `NaN` path. Any `NaN` element
>   in either input propagates to a `NaN` result via
>   NaN-poisoned mean and covariance arithmetic (fixture
>   `core/tests/function.rs:3489-3495` asserts `"NaN"` as the
>   second expected result for the NaN-element test). Suitable
>   for
>   **mean-shift-tolerant similarity** — for example,
>   user-rating vectors (where one user rates consistently
>   higher than another but ranks items in the same relative
>   order) or time-series correlation.
>
> Both functions are also available as `DIST` values when defining
> an HNSW index, but **prefer the standalone scalar functions
> (this section) over `DIST JACCARD` / `DIST PEARSON` on an HNSW
> index** — see the inversion warning at the bottom of this rule.
> The standalone calls return raw similarity scores and let your
> own `ORDER BY` clause decide ranking direction; they do not
> participate in HNSW priority-list ordering, so they are not
> affected by the inversion bug.

### Combining KNN Index Search with Computed Similarity

```surrealql
-- Use the HNSW index for fast candidate retrieval,
-- then compute exact similarity for ranking
LET $query_vector = [0.012, -0.034, 0.056, ...];

SELECT
    id,
    title,
    vector::distance::knn() AS approx_distance,
    vector::similarity::cosine(embedding, $query_vector) AS exact_similarity
FROM document
WHERE embedding <|20|> $query_vector
ORDER BY exact_similarity DESC
LIMIT 10;
```

---

## Hybrid Search Patterns

### Vector + Full-Text Search

Combine vector similarity with SurrealDB's full-text search for hybrid retrieval.

```surrealql
-- Define both indexes
DEFINE ANALYZER doc_analyzer TOKENIZERS blank, class FILTERS lowercase, snowball(english);
DEFINE INDEX idx_ft_content ON TABLE document
    FIELDS content
    FULLTEXT ANALYZER doc_analyzer BM25;
DEFINE INDEX idx_vec_embedding ON TABLE document
    FIELDS embedding
    HNSW DIMENSION 1536 DIST COSINE;

-- Full-text search only
SELECT id, title, search::score(1) AS text_score
FROM document
WHERE content @1@ 'vector database performance'
ORDER BY text_score DESC
LIMIT 10;

-- Vector search only
SELECT id, title, vector::distance::knn() AS vec_distance
FROM document
WHERE embedding <|10|> $query_vector
ORDER BY vec_distance;

-- Hybrid approach: union results from both methods
-- Step 1: Get text search candidates
LET $text_results = SELECT id, title, search::score(1) AS score, 'text' AS source
    FROM document
    WHERE content @1@ 'vector database performance'
    ORDER BY score DESC
    LIMIT 20;

-- Step 2: Get vector search candidates
LET $vec_results = SELECT id, title, vector::distance::knn() AS score, 'vector' AS source
    FROM document
    WHERE embedding <|20|> $query_vector
    ORDER BY score;

-- Step 3: Merge and deduplicate
-- Application-level fusion is recommended for proper score normalization
```

### Vector + Metadata Filtering

```surrealql
-- Pre-filter by metadata, then vector search
-- Note: The metadata filter narrows the candidate set before KNN
LET $query_vector = [0.012, -0.034, 0.056, ...];

-- Filter by category and date, then find nearest vectors
SELECT
    id, title,
    vector::distance::knn() AS distance
FROM document
WHERE
    category = 'engineering'
    AND created_at > d'2025-01-01'
    AND embedding <|10|> $query_vector
ORDER BY distance;

-- Filter by tags
SELECT
    id, title,
    vector::distance::knn() AS distance
FROM document
WHERE
    'surrealdb' IN tags
    AND status = 'published'
    AND embedding <|10|> $query_vector
ORDER BY distance;

-- Multi-tenant vector search
SELECT
    id, title,
    vector::distance::knn() AS distance
FROM document
WHERE
    tenant_id = $auth.tenant
    AND embedding <|10|> $query_vector
ORDER BY distance;
```

---

## RAG (Retrieval-Augmented Generation) Patterns

### Document Chunking and Embedding Storage

```surrealql
-- Schema for chunked documents
DEFINE TABLE source_document SCHEMAFULL;
DEFINE FIELD title ON TABLE source_document TYPE string;
DEFINE FIELD url ON TABLE source_document TYPE option<string>;
DEFINE FIELD content ON TABLE source_document TYPE string;
DEFINE FIELD doc_type ON TABLE source_document TYPE string;
DEFINE FIELD created_at ON TABLE source_document TYPE datetime DEFAULT time::now();

DEFINE TABLE chunk SCHEMAFULL;
DEFINE FIELD source ON TABLE chunk TYPE record<source_document>;
DEFINE FIELD content ON TABLE chunk TYPE string;
DEFINE FIELD embedding ON TABLE chunk TYPE array<float>;
DEFINE FIELD chunk_index ON TABLE chunk TYPE int;
DEFINE FIELD token_count ON TABLE chunk TYPE int;
DEFINE FIELD metadata ON TABLE chunk TYPE object DEFAULT {};
DEFINE FIELD created_at ON TABLE chunk TYPE datetime DEFAULT time::now();

-- HNSW index on chunk embeddings
DEFINE INDEX idx_chunk_embedding ON TABLE chunk
    FIELDS embedding
    HNSW DIMENSION 1536 DIST COSINE;

-- Index for filtering by source
DEFINE INDEX idx_chunk_source ON TABLE chunk COLUMNS source;

-- Store a document and its chunks
CREATE source_document:doc1 SET
    title = 'SurrealDB Documentation',
    url = 'https://surrealdb.com/docs',
    content = 'Full document content...',
    doc_type = 'documentation';

-- Store chunks with embeddings (generated externally)
CREATE chunk SET
    source = source_document:doc1,
    content = 'SurrealDB is a multi-model database...',
    embedding = [0.012, -0.034, ...],
    chunk_index = 0,
    token_count = 256,
    metadata = { section: 'introduction' };

CREATE chunk SET
    source = source_document:doc1,
    content = 'Vector search in SurrealDB uses HNSW...',
    embedding = [0.045, -0.067, ...],
    chunk_index = 1,
    token_count = 312,
    metadata = { section: 'vector-search' };
```

### Context Window Assembly for RAG

```surrealql
-- Retrieve relevant chunks for a query
LET $query_embedding = [0.012, -0.034, 0.056, ...];

-- Step 1: Find most relevant chunks
LET $relevant_chunks = SELECT
    id,
    content,
    source,
    chunk_index,
    token_count,
    vector::distance::knn() AS distance
FROM chunk
WHERE embedding <|10|> $query_embedding
ORDER BY distance;

-- Step 2: Get surrounding chunks for context (context window expansion)
LET $expanded = SELECT
    c.id,
    c.content,
    c.chunk_index,
    c.source,
    c.token_count
FROM chunk AS c
WHERE c.source IN (SELECT VALUE source FROM $relevant_chunks)
AND c.chunk_index >= (
    SELECT VALUE chunk_index FROM $relevant_chunks WHERE source = c.source LIMIT 1
) - 1
AND c.chunk_index <= (
    SELECT VALUE chunk_index FROM $relevant_chunks WHERE source = c.source LIMIT 1
) + 1
ORDER BY c.source, c.chunk_index;

-- Step 3: Assemble context with source attribution
SELECT
    content,
    source.title AS source_title,
    source.url AS source_url,
    chunk_index
FROM $expanded
ORDER BY chunk_index;
```

### Multi-Collection RAG Search

```surrealql
-- Search across multiple document types
LET $query_embedding = [0.012, -0.034, 0.056, ...];

-- Search documentation chunks
LET $docs = SELECT
    id, content, 'documentation' AS type,
    vector::distance::knn() AS distance
FROM doc_chunk
WHERE embedding <|5|> $query_embedding
ORDER BY distance;

-- Search FAQ entries
LET $faqs = SELECT
    id, answer AS content, 'faq' AS type,
    vector::distance::knn() AS distance
FROM faq_entry
WHERE embedding <|5|> $query_embedding
ORDER BY distance;

-- Search knowledge base
LET $kb = SELECT
    id, content, 'knowledge_base' AS type,
    vector::distance::knn() AS distance
FROM kb_article_chunk
WHERE embedding <|5|> $query_embedding
ORDER BY distance;
```

---

## AI Integration Patterns

### Embedding Generation Pipeline

```surrealql
-- Track embedding generation status
DEFINE TABLE embedding_job SCHEMAFULL;
DEFINE FIELD source_table ON TABLE embedding_job TYPE string;
DEFINE FIELD source_id ON TABLE embedding_job TYPE record;
DEFINE FIELD status ON TABLE embedding_job TYPE string
    ASSERT $value IN ['pending', 'processing', 'completed', 'failed'];
DEFINE FIELD error ON TABLE embedding_job TYPE option<string>;
DEFINE FIELD created_at ON TABLE embedding_job TYPE datetime DEFAULT time::now();
DEFINE FIELD completed_at ON TABLE embedding_job TYPE option<datetime>;

-- Event-driven embedding generation
-- When a document is created, queue an embedding job
DEFINE EVENT on_document_create ON TABLE document WHEN $event = "CREATE" THEN {
    CREATE embedding_job SET
        source_table = 'document',
        source_id = $after.id,
        status = 'pending';
};

-- When a document is updated, re-queue embedding
DEFINE EVENT on_document_update ON TABLE document WHEN $event = "UPDATE"
    AND $before.content != $after.content THEN {
    CREATE embedding_job SET
        source_table = 'document',
        source_id = $after.id,
        status = 'pending';
};
```

### Semantic Similarity Search

```surrealql
-- Find semantically similar documents
LET $source_embedding = (SELECT VALUE embedding FROM ONLY document:target);

SELECT
    id,
    title,
    vector::similarity::cosine(embedding, $source_embedding) AS similarity
FROM document
WHERE id != document:target
AND embedding <|20|> $source_embedding
ORDER BY similarity DESC
LIMIT 10;

-- Semantic deduplication: find near-duplicates
SELECT
    d1.id AS doc_a,
    d2.id AS doc_b,
    vector::similarity::cosine(d1.embedding, d2.embedding) AS similarity
FROM document AS d1, document AS d2
WHERE d1.id < d2.id
AND vector::similarity::cosine(d1.embedding, d2.embedding) > 0.95
ORDER BY similarity DESC;
```

### Clustering with Vector Data

```surrealql
-- Assign cluster labels based on centroid similarity
-- (Centroids computed externally, stored in SurrealDB)
DEFINE TABLE cluster_centroid SCHEMAFULL;
DEFINE FIELD label ON TABLE cluster_centroid TYPE string;
DEFINE FIELD centroid ON TABLE cluster_centroid TYPE array<float>;
DEFINE FIELD description ON TABLE cluster_centroid TYPE string;

DEFINE INDEX idx_centroid ON TABLE cluster_centroid
    FIELDS centroid
    HNSW DIMENSION 1536 DIST COSINE;

-- Assign documents to nearest cluster
LET $doc = SELECT * FROM ONLY document:target;

SELECT
    label,
    description,
    vector::similarity::cosine(centroid, $doc.embedding) AS similarity
FROM cluster_centroid
WHERE centroid <|1|> $doc.embedding;

-- Batch assignment: label all unassigned documents
UPDATE document SET cluster = (
    SELECT VALUE label FROM cluster_centroid
    WHERE centroid <|1|> $parent.embedding
    LIMIT 1
) WHERE cluster IS NONE;
```

### Classification Using Stored Vectors

```surrealql
-- KNN classification: classify by majority vote of nearest labeled examples
DEFINE TABLE labeled_example SCHEMAFULL;
DEFINE FIELD text ON TABLE labeled_example TYPE string;
DEFINE FIELD embedding ON TABLE labeled_example TYPE array<float>;
DEFINE FIELD label ON TABLE labeled_example TYPE string;

DEFINE INDEX idx_labeled ON TABLE labeled_example
    FIELDS embedding
    HNSW DIMENSION 1536 DIST COSINE;

-- Classify a new item by finding K nearest labeled examples
LET $new_embedding = [0.012, -0.034, ...];

SELECT
    label,
    count() AS votes,
    math::mean(vector::similarity::cosine(embedding, $new_embedding)) AS avg_similarity
FROM labeled_example
WHERE embedding <|5|> $new_embedding
GROUP BY label
ORDER BY votes DESC, avg_similarity DESC
LIMIT 1;
```

---

## Production Considerations

### Index Build Time and Memory

```surrealql
-- Check index status
INFO FOR TABLE document;
-- Shows index definitions and their status

-- For large datasets, index building happens in the background
-- Monitor by checking if queries use the index:
-- If the index is still building, queries fall back to brute-force scan

-- Tune build parameters for your hardware:
-- More RAM available -> higher EFC and M for better recall
-- Limited RAM -> lower M and use I16 type for compression

-- Small dataset (<10K vectors): defaults are fine
DEFINE INDEX idx_small ON TABLE document
    FIELDS embedding
    HNSW DIMENSION 1536 DIST COSINE;

-- Medium dataset (10K-1M vectors): tune M and EFC
DEFINE INDEX idx_medium ON TABLE document
    FIELDS embedding
    HNSW DIMENSION 1536 DIST COSINE
    EFC 200
    M 16;

-- Large dataset (>1M vectors): optimize for memory
DEFINE INDEX idx_large ON TABLE document
    FIELDS embedding
    HNSW DIMENSION 1536 DIST COSINE
    TYPE I16
    EFC 150
    M 12;
```

### Query Latency Optimization

```surrealql
-- Return only the fields you need (avoid SELECT *)
SELECT id, title, vector::distance::knn() AS distance
FROM document
WHERE embedding <|10|> $query_vector
ORDER BY distance;

-- Pre-filter to reduce the candidate set
SELECT id, title, vector::distance::knn() AS distance
FROM document
WHERE category = 'engineering'      -- metadata filter first
AND embedding <|10|> $query_vector  -- then vector search
ORDER BY distance;

-- Use appropriate K value -- don't over-fetch
-- BAD: fetching 1000 when you only need 10
-- WHERE embedding <|1000|> $query_vector

-- GOOD: fetch slightly more than needed, then post-filter
-- WHERE embedding <|20|> $query_vector  -- fetch 20, return top 10
```

### Embedding Dimension Trade-offs

Higher dimensions provide more representational capacity but cost more in storage and query time.

| Dimension | Storage/vector | Index Memory | Query Speed | Use Case |
|---|---|---|---|---|
| 384 | 1.5 KB | Low | Fast | Simple similarity, prototyping |
| 768 | 3 KB | Medium | Good | General purpose |
| 1024 | 4 KB | Medium | Good | Balanced accuracy/speed |
| 1536 | 6 KB | High | Moderate | High accuracy text search |
| 3072 | 12 KB | Very High | Slower | Maximum accuracy |

```surrealql
-- If your embedding model supports dimension reduction (e.g., Matryoshka),
-- use the smallest dimension that meets your accuracy requirements.
-- Test with your actual data to find the sweet spot.
```

### Batch Insertion Patterns

```surrealql
-- Insert vectors in batches for better throughput
-- Single batch insert (preferred for bulk loading)
INSERT INTO document [
    { id: document:1, title: 'Doc 1', embedding: [0.1, 0.2, ...], content: '...' },
    { id: document:2, title: 'Doc 2', embedding: [0.3, 0.4, ...], content: '...' },
    { id: document:3, title: 'Doc 3', embedding: [0.5, 0.6, ...], content: '...' }
];

-- For very large imports, batch in groups of 100-500 records
-- to balance throughput with memory usage.
-- The HNSW index updates incrementally with each insert.
```

### Index Rebuild Strategies

```surrealql
-- If index quality degrades after many updates/deletes,
-- rebuild by removing and recreating

-- Remove existing index
REMOVE INDEX idx_embedding ON TABLE document;

-- Recreate with potentially tuned parameters
DEFINE INDEX idx_embedding ON TABLE document
    FIELDS embedding
    HNSW DIMENSION 1536 DIST COSINE
    EFC 200
    M 16;

-- The index will rebuild in the background from existing data.
-- Queries will work during rebuild but may be slower (brute-force fallback).
```

### Distance Function Selection Guide

| Function | Best For | Normalized Vectors | Range |
|---|---|---|---|
| COSINE | Text embeddings, semantic similarity | Yes (recommended) | [0, 2] (distance) |
| EUCLIDEAN | Spatial data, coordinate systems | No | [0, inf) |
| MANHATTAN | Feature counting, grid distances | No | [0, inf) |
| MINKOWSKI | Generalised distance (Lp norm); set order via `DIST MINKOWSKI <p>` | No | [0, inf) |
| CHEBYSHEV | Worst-case dimension difference | No | [0, inf) |
| HAMMING | Binary features, hash comparison | N/A | [0, dim] |
| JACCARD ⚠ | Numeric-token similarity (NOT distance — see warning below); pre-dedup inputs with `array::distinct(...)` for textbook set semantics | N/A | `NaN` if both inputs empty; otherwise `[0, |b|]` raw (multiset-asymmetric numerator) / `[0, 1]` after pre-dedup |
| PEARSON ⚠ | Correlation-based similarity (NOT distance — see warning below) | No | finite results in `[-1, 1]`; non-finite (`NaN` / `±Infinity`) possible for zero-denominator or NaN-element inputs (see callout) |

Most text embedding models produce normalized vectors, making COSINE the standard choice. If you are unsure, use COSINE.

> **⚠ JACCARD / PEARSON semantic inversion warning (v3.0.5).** The
> v3.0.5 catalog `Distance::compute` body
> (`catalog/schema/index.rs` lines 293–300) calls
> `jaccard_similarity()` and `pearson_similarity()` for these two
> `DIST` values, while every other `DIST` value computes a true
> distance (smaller = closer). Because the HNSW `KnnPriorityList`
> uses ascending `BTreeMap` order (smaller = nearer), configuring
> `DIST JACCARD` or `DIST PEARSON` on an HNSW index ranks the
> **least similar** results first — the search is silently
> inverted. Until upstream fixes this (track in the SurrealDB
> issue tracker), avoid `DIST JACCARD` / `DIST PEARSON` on HNSW
> indexes; use the standalone `vector::similarity::jaccard()` /
> `vector::similarity::pearson()` functions for ad-hoc scoring
> instead, or pick a true distance metric (`COSINE`, `EUCLIDEAN`,
> `MANHATTAN`, `CHEBYSHEV`, `HAMMING`) for indexed nearest-
> neighbour search.
>
> **Pearson zero-denominator path divergence (v3.0.5).** The
> standalone `vector::similarity::pearson()` and the
> catalog/brute-force `Distance::compute` path return `NaN`
> for exact zero-variance constant operands (the
> `0 / 0` case described in the callout above). They can
> ALSO return `±Infinity` when f64 **underflow** drives the
> denominator to `0.0` while covariance remains non-zero —
> e.g. `pearson([0.0, 1e-308], [0.0, 1e154])` centers to
> `dx_i ∈ {-5e-309, +5e-309}` and `dy_i ∈ {-5e153, +5e153}`;
> the squared centered terms `(5e-309)² ≈ 2.5e-617` underflow
> to `0.0`, so `std_dev_a = 0.0`. Pairwise products
> `dx_i * dy_i` stay at magnitude `2.5e-155` (well above the
> f64 minimum normal `~2.2e-308`), so covariance is non-zero
> at `~2.5e-155` and the final ratio is `+Infinity`
> (sign-dependent on the operand pairing). Treat any non-finite result (`NaN`,
> `+Inf`, `-Inf`) as a degenerate input regardless of which
> route produced it. The HNSW-internal Pearson implementation
> at
> `core/src/idx/trees/vector.rs:413-440` instead returns
> `0.0` when `denominator == 0.0` (the explicit
> `if denominator == 0.0 { return 0.0; }` short-circuit at
> `:435-437`) — that does NOT match the standalone path's
> non-finite behaviour (`NaN` for the `0 / 0`
> zero-variance case; `±Infinity` for the underflow-driven
> zero-denominator case). This divergence does NOT make
> `DIST PEARSON` safe for HNSW; the inversion bug above is
> the dominant reason to avoid it. The note here is so that
> readers debugging HNSW vs brute-force scoring understand
> why zero-denominator inputs produce different outputs
> depending on which evaluation path runs.
