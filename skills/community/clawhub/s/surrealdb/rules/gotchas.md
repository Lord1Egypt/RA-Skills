# SurrealDB Gotchas — Edge Cases and Footguns

Quick reference for verified SurrealDB footguns, drawn from release notes,
GitHub issues/discussions, and upstream docs. Target: **v3.1.4+**. Each item
points to the rule file with full detail.

---

## Upgrade and migration (3.0.x → 3.1.x)

| Gotcha | What goes wrong | Fix |
|---|---|---|
| GraphQL client names | Auto-generated schema switched to Apollo-only naming | Regenerate introspection and clients; use `GRAPHQL_ALIAS` / `GRAPHQL_DEPRECATED` |
| Metrics dashboards | Scope moved to `surrealdb.*` | Update Prometheus/Grafana queries — see `rules/deployment.md` |
| HTTP `/key` bodies | Body no longer executes as SurrealQL | Treat body as inert value bound to `$data` only |
| `--allow-net` | Resolved private IPs blocked unless listed | Explicitly allow CIDRs for Surrealism/scripting hosts |
| DiskANN on 32-bit | Index type unavailable | Use HNSW on 32-bit targets; DiskANN requires 64-bit (v3.1.3+) |

Full breaking-change table: `rules/deployment.md`.

---

## Security and permissions

| Gotcha | What goes wrong | Fix |
|---|---|---|
| Array element permissions (pre-3.1.4) | `items[*]` SELECT WHERE could leak denied elements | Upgrade to **v3.1.4+** ([GHSA-8rw6-p7m8-63jp](https://github.com/surrealdb/surrealdb/security/advisories/GHSA-8rw6-p7m8-63jp)) |
| Permission subqueries (pre-3.1.3) | Nested SELECT/graph in permission WHERE re-triggered RLS recursively | Fixed in 3.1.3; upgrade if you use subqueries in table permissions |
| Bucket PERMISSIONS (pre-3.1.4) | Streaming file executor could bypass `DEFINE BUCKET … PERMISSIONS WHERE` | Upgrade to 3.1.4 for experimental buckets |
| Built-in MCP stdio | `surreal mcp` grants **owner-level** tool access with no login | Never expose stdio MCP to untrusted hosts; use HTTP `/mcp` + scoped auth in production |
| `PERMISSIONS FOR select FULL` | Unauthenticated reads on sensitive tables | Default deny; scope with `$auth` — see `rules/security.md` |
| Password fields | Accidental SELECT exposure | `PERMISSIONS FOR select NONE` on secret fields |

---

## Graph and relationships

| Gotcha | What goes wrong | Fix |
|---|---|---|
| Inline edge filter (pre-3.1.3) | `->(edge WHERE …)` returned empty | Upgrade to 3.1.3+; prefer parenthesised edge filters over post-filtering |
| `$parent` in nested graph WHERE | Wrong scope or ignored ORDER BY on traversals | Fixed 3.1.0; `$parent` = current SELECT row — see `rules/graph-queries.md` |
| RELATION + partial UNIQUE index | WHERE with partial key via `type::record()` returned 0 rows while traversal worked ([#7280](https://github.com/surrealdb/surrealdb/issues/7280)) | Verify with `EXPLAIN`; index full composite key |
| `RELATE` has no MERGE | Expecting upsert-on-edge semantics | `UPDATE` the edge record or delete + re-RELATE |
| Record link vs graph edge | Over-modeling simple FKs as edges | Use links for simple refs; edges when the relationship has properties — [official guide](https://surrealdb.com/docs/learn/data-models/graph/record-links-vs-graph-relations) |
| Unbounded recursion | Runaway traversals | Cap with `.{..N}`, `TIMEOUT`, and `LIMIT` (max depth 256) |

Deep coverage: `rules/graph-queries.md`.

---

## Vector search

| Gotcha | What goes wrong | Fix |
|---|---|---|
| JACCARD / PEARSON HNSW distance | Semantic inversion vs similarity functions in v3.0.5 catalog | Prefer `DIST COSINE` / `EUCLIDEAN` for HNSW; read inversion warning in `rules/vector-search.md` |
| Pearson constant / underflow vectors | `NaN` or `±Infinity` from f64 edge cases | Documented IEEE-754 paths in `rules/vector-search.md` — test your embedding distribution |
| `HASHED_VECTOR` | Mistaking it for quantisation | Only changes vec→docs lookup keying, not graph storage |
| `LM` vs Minkowski order | Pre-v1.5.3 docs confused HNSW `LM` with Minkowski order | Use `DIST MINKOWSKI N`, not `LM N` |
| Dimension mismatch | Silent index errors at insert | Match `DIMENSION` to embedding model exactly |
| DiskANN on WASM | Index type not supported | HNSW only in browser/WASM deployments |

Deep coverage: `rules/vector-search.md`.

---

## SurrealQL and schema

| Gotcha | What goes wrong | Fix |
|---|---|---|
| `ALTER` on 3.0.5 | Only seven ALTER targets parse | Upgrade to 3.1+ for EVENT/PARAM/BUCKET/… ALTER, or use REMOVE+DEFINE |
| `ALTER ACCESS` type change | Cannot switch record/JWT/bearer type | REMOVE + DEFINE ACCESS |
| `DEFINE INDEX … DEFER` | Does not parse in v3.x | Use `REBUILD INDEX` after bulk loads — see `rules/performance.md` |
| `<future> { … }` | Does not exist in v3.0.5+ | Use computed fields / events instead |
| `UPDATE … LIMIT` | Not valid SurrealQL | Filter in WHERE or subquery |
| Missing record SELECT | Pre-3.0.2 error vs NONE confusion | Missing record returns `NONE` since 3.0.2 |
| `encoding::json::*` | Documented in old blogs but not in v3 registry | Only `encoding::base64::*` and `encoding::cbor::*` — see `rules/surrealql.md` |
| `vector::similarity::spearman` / `mahalanobis` | Registered but return Unimplemented at runtime | Do not call — see function registry in `rules/surrealql.md` |

---

## MCP and AI agents

| Gotcha | What goes wrong | Fix |
|---|---|---|
| Two MCP surfaces | Confusion between built-in and standalone | **Built-in** (`surreal mcp`) for local IDE; **standalone** (`surrealmcp`) for extended/cloud tools |
| `cargo install surrealmcp` | Fails — not on crates.io | Source install or Docker only |
| `surrealmcp serve` | Invalid subcommand | Use `surrealmcp start` |
| LangChain `filter` kwarg | Wrong parameter name | Use `custom_filter` in `langchain-surrealdb` — `rules/langchain.md` |
| Spectron / agent-memory demo | Looks production-ready | Alpha SDK + experimental flags; reference architecture only |
| agent-memory demo flags | `--allow-funcs --allow-net --allow-experimental` | Do not copy to production without hardening |

Deep coverage: `rules/surrealmcp.md`, `rules/ecosystem-integrations.md`.

---

## SDKs and clients

| Gotcha | What goes wrong | Fix |
|---|---|---|
| Python PyPI vs main | PyPI `surrealdb` 2.0.0; main tracks 3.0.0 unreleased | Pin deliberately; check `rules/sdks.md` |
| LangChain + surrealdb SDK | Package expects v1 SDK (`~=1.0.8`) | Open connection yourself; pass to `SurrealDBVectorStore` |
| Java Maven 3.0.0 pin | Non-existent coordinate in old docs | Use **2.1.1** — `rules/sdks.md` |
| Swift / Kotlin tags | No published release tags | Pin commit/branch explicitly |
| Cold-start "Session not found" | Race on first request (pre-3.1.3) | Upgrade to 3.1.3+ or retry connect |

---

## Operational

| Gotcha | What goes wrong | Fix |
|---|---|---|
| `surreal import --conn` | Flag does not exist | Use `--endpoint` |
| In-memory in production | Data loss on restart | RocksDB / SurrealKV / TiKV for persistence |
| root/root in production | Full compromise | `DEFINE USER` with least privilege |
| `curl \| sh` installers | Supply-chain risk in audited environments | Prefer brew, apt, Docker, or `surreal upgrade` |

---

## Where to go deeper

| Topic | Rule |
|---|---|
| Graph traversal patterns | `rules/graph-queries.md` |
| Vector indexes and RAG | `rules/vector-search.md` |
| Permissions and auth | `rules/security.md` |
| Deploy and upgrade | `rules/deployment.md` |
| Language reference | `rules/surrealql.md` |
| MCP wiring | `rules/surrealmcp.md` |

Official video starting points (pre-3.1 content — cross-check against Release 3.1 docs):

- [Record IDs, Expressions and Graphs](https://www.youtube.com/watch?v=VFXXEn40GCA)
- [Graph-Style Relationships](https://www.youtube.com/watch?v=zwQwKvMa9sU)
- [Surrealist Tips: GraphQL](https://www.youtube.com/watch?v=jmFPjyiJEeI) — note 3.1 Apollo breaking changes
