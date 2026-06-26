---
name: rag-chunking-optimizer
description: Optimize RAG pipeline chunking strategy — analyze documents, recommend chunk sizes, splitting methods, overlap settings, and metadata enrichment for maximum retrieval quality.
metadata:
  tags: ["rag", "chunking", "llm", "embeddings", "ai", "retrieval"]
---

# RAG Chunking Optimizer

Analyze documents and recommend optimal chunking strategies for RAG (Retrieval-Augmented Generation) pipelines. Evaluates chunk sizes, splitting methods, overlap settings, metadata enrichment, and retrieval quality. Use when building or optimizing RAG applications.

## Usage

```
"Optimize chunking for my knowledge base documents"
"What's the best chunk size for these technical docs?"
"Analyze my current chunking strategy for retrieval quality"
"Help me set up semantic chunking for my RAG pipeline"
"Compare chunking strategies for my document types"
```

## How It Works

### 1. Document Analysis

Profile the document corpus:

```bash
# Analyze document types and sizes
find docs/ -type f \( -name "*.md" -o -name "*.txt" -o -name "*.pdf" -o -name "*.html" \) -exec wc -l {} + | sort -rn | head -20

# Check document structure patterns
for f in docs/*.md; do
  echo "=== $f ==="
  grep -c "^#" "$f"           # heading count
  grep -c "^```" "$f"          # code block count  
  wc -w < "$f"                 # word count
done
```

Classify documents by type:
- **Structured technical docs**: APIs, references, manuals → heading-based splitting
- **Narrative content**: articles, blog posts, reports → semantic/paragraph splitting
- **Code-heavy docs**: tutorials, examples → code-aware splitting
- **Tabular data**: specs, configurations → row/section splitting
- **Q&A / FAQ**: question-answer pairs → pair-based splitting
- **Legal/compliance**: contracts, policies → clause-based splitting

### 2. Chunking Strategy Evaluation

Evaluate strategies against the corpus:

**Fixed-size chunking:**
- Pros: Simple, predictable, works everywhere
- Cons: Breaks mid-sentence, loses context
- Best for: Homogeneous documents, initial prototyping
- Typical: 512-1024 tokens, 50-100 token overlap

**Recursive character splitting:**
- Split hierarchy: `\n\n` → `\n` → `. ` → ` ` → ``
- Pros: Respects natural boundaries, widely supported
- Cons: May still break semantic units
- Best for: General purpose, mixed content

**Semantic chunking:**
- Group sentences by embedding similarity
- Pros: Preserves meaning, variable-size chunks
- Cons: Slower, requires embedding model, harder to debug
- Best for: Narrative content, complex topics

**Heading-based (markdown/HTML):**
- Split on heading hierarchy (H1 → H2 → H3)
- Pros: Preserves document structure, natural sections
- Cons: Uneven chunk sizes, may be too large or small
- Best for: Structured documentation, wikis

**Code-aware chunking:**
- Split on function/class boundaries using AST
- Pros: Complete code units, preserves imports/context
- Cons: Language-specific, requires parsing
- Best for: Code documentation, API references

**Sliding window with context:**
- Overlapping windows with parent/sibling context
- Pros: Never loses boundary context
- Cons: Storage overhead, retrieval deduplication needed
- Best for: Dense technical content

### 3. Chunk Size Optimization

Factors that determine optimal chunk size:

- **Embedding model**: Match chunk size to model's sweet spot
  - `text-embedding-3-small`: 256-512 tokens optimal
  - `text-embedding-ada-002`: 512-1024 tokens
  - `voyage-3`: 512-1024 tokens
  - `BAAI/bge-large`: 256-512 tokens
- **Query type**: Short queries → smaller chunks; complex queries → larger
- **Answer density**: If answers span paragraphs → larger chunks
- **Context window**: LLM context limits how many chunks you can inject
- **Latency budget**: More chunks = more embedding comparisons

### 4. Overlap Analysis

Determine optimal overlap:

- **Too little overlap** (0-10%): Context lost at boundaries, retrieval misses
- **Optimal overlap** (10-20%): Maintains context without excessive duplication
- **Too much overlap** (>25%): Storage waste, retrieval returns near-duplicates

### 5. Metadata Enrichment

Recommend metadata to attach to each chunk:

- **Source metadata**: file path, section heading, page number
- **Structural metadata**: document type, heading hierarchy, position
- **Semantic metadata**: extracted entities, keywords, topic classification
- **Temporal metadata**: creation date, last modified, version
- **Relational metadata**: links to parent/child/sibling chunks

### 6. Quality Metrics

Evaluate chunking quality:

- **Semantic coherence**: Does each chunk contain a complete thought?
- **Retrieval precision**: Top-K results contain the answer?
- **Retrieval recall**: Can every answerable question find its chunk?
- **Chunk size distribution**: Normal distribution around target?
- **Boundary quality**: How often are sentences/concepts split?
- **Deduplication ratio**: How much content overlaps between chunks?

### 7. A/B Testing Framework

Design experiments to compare strategies:

```
Test matrix:
- Chunk sizes: [256, 512, 768, 1024] tokens
- Overlap: [0, 64, 128] tokens
- Method: [recursive, semantic, heading-based]
- Embedding model: [ada-002, voyage-3]

Evaluation set: 50 representative queries with known answers
Metrics: MRR@5, Recall@10, Answer accuracy, Latency
```

## Output

```
## RAG Chunking Analysis

**Corpus:** 234 documents, 1.2M tokens total
**Current strategy:** Fixed 1024 tokens, 100 overlap
**Recommendation:** Switch to heading-based + semantic hybrid

### Document Profile
| Type | Count | Avg Length | Recommended Strategy |
|------|-------|------------|---------------------|
| API docs | 89 | 2,400 tokens | Heading-based (H2 splits) |
| Tutorials | 45 | 5,800 tokens | Semantic chunking |
| Blog posts | 67 | 1,600 tokens | Recursive, 512 tokens |
| Changelogs | 33 | 800 tokens | Version-based splits |

### Recommended Configuration
```python
# Primary strategy: heading-based for structured docs
structured_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[("##", "Section"), ("###", "Subsection")],
    strip_headers=False
)

# Fallback: recursive for unstructured content
recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=64,
    separators=["\n\n", "\n", ". ", " "]
)
```

### Expected Improvement
| Metric | Current | Projected |
|--------|---------|-----------|
| MRR@5 | 0.62 | 0.78 (+26%) |
| Recall@10 | 0.71 | 0.89 (+25%) |
| Avg chunk coherence | 0.54 | 0.82 (+52%) |
| Storage overhead | 1.0x | 1.12x |

### Chunk Size Distribution (recommended)
- Min: 128 tokens (small subsections)
- Median: 420 tokens
- Max: 1,024 tokens (capped)
- Std dev: 180 tokens
```
