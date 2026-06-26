# LangChain Integration

> **v1.4.1 status note:** the v1.4.0 version of this rule documented a
> JS package (`@langchain/surrealdb`), several Python classes
> (`AsyncSurrealDBVectorStore`, `SurrealChatMessageHistory`,
> `SurrealHybridRetriever`), factory methods (`from_endpoint`,
> `from_client`), and pip extras (`[openai]`, `[huggingface]`) that do
> not exist upstream. Those sections have been removed. The content
> below is grounded in the upstream `surrealdb/langchain-surrealdb`
> README and the v0.2.1 PyPI metadata. Anything not covered here is
> deferred until a manual upstream pass.

`langchain-surrealdb` is the official LangChain integration for
SurrealDB. It exposes SurrealDB as a LangChain **vector store** so
RAG and agent chains can persist documents + embeddings + structured
metadata + graph edges in a single SurrealDB instance.

- Upstream: `https://github.com/surrealdb/langchain-surrealdb`
- PyPI: `https://pypi.org/project/langchain-surrealdb/` (status: stable)
- Verified version at v1.4.1 cut: `0.2.1`
- Verified deps: `langchain-core ~= 1.1.0`, `surrealdb ~= 1.0.8`
- Verified Python: `>= 3.10, < 4.0`
- Declared extras at v0.2.1: **none** (the upstream `pyproject.toml` has no `[project.optional-dependencies]` block; PyPI `provides_extras` is null). The README mentions a `[graph-qa]` extra that depends on `langchain-classic`, but that extra is not shipped in the v0.2.1 package metadata -- pip will silently no-op `pip install "langchain-surrealdb[graph-qa]"` rather than installing `langchain-classic`. If you need the graph helpers, install `langchain-classic` explicitly until the upstream extra ships.

> **JS / TypeScript:** there is no published `@langchain/surrealdb`
> npm package as of the v1.4.1 cut. Use the v2 JavaScript SurrealDB
> SDK directly (`rules/sdks.md`) until an official LangChain JS
> integration ships.

---

## When to Use

| Goal | Why this integration fits |
|------|---------------------------|
| RAG over content with structured metadata + graph relationships | Vector + graph in one SurrealDB instance, no separate metadata store |
| Pipelines that already persist domain data in SurrealDB | Avoid moving embeddings to a second database |
| Multi-tenant SaaS where embeddings must stay scoped to a tenant | DEFINE ACCESS / per-tenant namespaces enforce isolation server-side |

If you only need a pure vector store with no metadata, no permissions,
and no graph -- pick a dedicated vector DB. If your data already has
structure, this integration is the path of least resistance.

---

## Installation

```bash
# Core install
pip install -U langchain-surrealdb surrealdb

# uv (preferred for contributors)
uv add langchain-surrealdb surrealdb

# If you want the graph QA helpers (the upstream README mentions a
# `[graph-qa]` extra, but the v0.2.1 PyPI package does not ship it as a
# declared extra -- install langchain-classic explicitly):
pip install -U langchain-classic
```

The package targets `langchain-core ~= 1.1.0` and the v1 SurrealDB
Python SDK (`surrealdb ~= 1.0.8`). It is **not** pinned to the v2
Python SDK series; check the upstream `pyproject.toml` before bumping
your project's `surrealdb` dependency.

---

## Vector Store (verified API)

The constructor takes an `Embeddings` instance and an existing
`Surreal` connection. There is no `from_endpoint` or `from_client`
class method.

```python
from langchain_core.documents import Document
from langchain_surrealdb.vectorstores import SurrealDBVectorStore
from langchain_ollama import OllamaEmbeddings
from surrealdb import Surreal

# 1. Open the connection yourself
conn = Surreal("ws://localhost:8000/rpc")
conn.signin({"username": "root", "password": "root"})  # local dev only
conn.use("langchain", "demo")

# 2. Hand it to the vector store
vector_store = SurrealDBVectorStore(
    OllamaEmbeddings(model="llama3.2"),
    conn,
)

doc_1 = Document(page_content="foo", metadata={"source": "https://surrealdb.com"})
doc_2 = Document(page_content="SurrealDB", metadata={"source": "https://surrealdb.com"})

vector_store.add_documents(documents=[doc_1, doc_2], ids=["1", "2"])

# Similarity search with metadata filter -- note: keyword is `custom_filter`,
# not `filter`
results = vector_store.similarity_search_with_score(
    query="surreal",
    k=1,
    custom_filter={"source": "https://surrealdb.com"},
)
for doc, score in results:
    print(f"[SIM={score:.3f}] {doc.page_content} {doc.metadata}")
```

> The exact filter shape, async-method surface, and retriever options
> beyond the LangChain `VectorStore.as_retriever()` base behavior are
> not redocumented here. Check the upstream `vectorstores.py` and the
> `examples/` directory in the upstream repo. Examples worth reading:
>
> - `examples/basic/main.py`
> - `examples/graph/graph.py`
> - `docs/vectorstores.ipynb`

---

## Multi-Tenant + Permissioned Stores

Use SurrealDB's `DEFINE ACCESS` / `DEFINE TABLE ... PERMISSIONS`
machinery to enforce per-tenant isolation server-side instead of
filtering only in Python:

```surql
DEFINE TABLE document SCHEMAFULL
  PERMISSIONS
    FOR select WHERE tenant_id = $auth.tenant_id
    FOR create, update, delete WHERE tenant_id = $auth.tenant_id;

DEFINE FIELD tenant_id ON TABLE document TYPE string;
```

Sign in with the tenant-scoped record user before constructing the
vector store; the v1 Python SDK signin shape is verified in
`rules/sdks.md`. Row-level permissions filter both writes and
similarity-search reads.

---

## Performance Notes

- **Vector index choice:** SurrealDB v3 supports HNSW for vector
  indexes; MTREE was removed in v3. See `rules/vector-search.md` for
  the supported index types and trade-offs at the v3.x line.
- **Pre-create indexes** for production: auto-create-on-first-write
  incurs build cost on the first query.
- **Batch embeddings** by passing lists of documents to
  `add_documents`; the integration batches embedding calls and DB
  inserts.
- **Use record IDs as document IDs** when stable, to avoid a
  secondary unique-index lookup.

---

## Cross-References

- `rules/vector-search.md` -- HNSW and DiskANN index types in v3.1+
- `rules/data-modeling.md` -- record IDs, schemafull definitions, edges
- `rules/security.md` -- DEFINE ACCESS, row-level permissions
- `rules/sdks.md` -- Python v1/v2 SurrealDB SDK details
- `rules/surrealmcp.md` -- agent-side access (complements LangChain's app-side use)
- Upstream README: `https://github.com/surrealdb/langchain-surrealdb`
- Upstream docs portal: `https://surrealdb.com/docs/integrations/frameworks/langchain`
