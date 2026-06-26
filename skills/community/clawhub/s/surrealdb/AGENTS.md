# Agent Briefing: surrealdb

Structured reference for AI agents. Minimal prose, maximum signal.

## Quick Start

```bash
# Check if configured
uv run {baseDir}/scripts/onboard.py --check

# Get full capabilities manifest (JSON)
uv run {baseDir}/scripts/onboard.py --agent
```

## Capabilities

| Command | Script | What It Does | When to Use |
|---------|--------|-------------|-------------|
| `doctor` | `scripts/doctor.py` | Health check: CLI, connectivity, version, storage | First run, troubleshooting, verifying environment |
| `doctor --check` | `scripts/doctor.py` | Quick pass/fail (exit code only) | CI pipelines, pre-flight checks |
| `schema introspect` | `scripts/schema.py` | Full schema dump (tables, fields, indexes, events) | Understanding existing database structure |
| `schema tables` | `scripts/schema.py` | List tables with field counts and indexes | Quick overview of database contents |
| `schema table <name>` | `scripts/schema.py` | Inspect a single table in detail | Debugging a specific table definition |
| `schema export` | `scripts/schema.py` | Export schema as SurrealQL or JSON | Reproducible deployments, version control |
| `onboard --agent` | `scripts/onboard.py` | JSON capabilities manifest | Agent self-discovery, integration setup |
| `onboard --check` | `scripts/onboard.py` | Verify prerequisites | First run, CI |

## Decision Trees

### "User wants to create a SurrealDB project"

```
1. Run doctor to verify environment:
   uv run {baseDir}/scripts/doctor.py

2. Is surreal CLI installed?
   NO  -> brew install surrealdb/tap/surreal (or see https://surrealdb.com/install)
   YES -> Continue

3. Choose storage engine (LOCAL DEV -- use scoped credentials in production):
   Development     -> surreal start memory --user root --pass root
   Single-node     -> surreal start rocksdb://data/mydb.db --user root --pass root
   Time-travel     -> surreal start surrealkv://data/mydb --user root --pass root
   Distributed     -> surreal start tikv://... --user root --pass root

4. Design schema:
   -> Reference rules/data-modeling.md for table/field patterns
   -> Reference rules/graph-queries.md if domain has relationships
   -> Reference rules/vector-search.md if semantic search needed

5. Apply schema (local dev credentials -- use scoped users in production):
   surreal import --endpoint $SURREAL_ENDPOINT --user root --pass root \
     --ns <ns> --db <db> schema.surql

6. Verify:
   uv run {baseDir}/scripts/schema.py introspect
```

### "User has a data modeling question"

```
What kind of data?
  Documents/records    -> rules/data-modeling.md (record IDs, field types, schema modes)
  Relationships/graphs -> rules/graph-queries.md (RELATE, edge tables, traversal)
  Vector embeddings    -> rules/vector-search.md (vector fields, HNSW indexes, similarity)
  Time-series          -> rules/data-modeling.md (datetime fields, range queries, aggregations)
  Geospatial           -> rules/data-modeling.md (geometry types, geo functions, spatial indexes)
  Mixed/multi-model    -> rules/data-modeling.md + relevant specialized rules

Need schema validation?
  YES -> DEFINE TABLE ... SCHEMAFULL (strict, all fields must be defined)
  PARTIAL -> DEFINE TABLE ... SCHEMALESS (flexible, defined fields are validated)
```

### "User needs to optimize performance"

```
1. Check current schema and indexes:
   uv run {baseDir}/scripts/schema.py introspect

2. Identify bottleneck type:
   Slow queries        -> rules/performance.md (EXPLAIN, index strategies)
   High write latency  -> rules/performance.md (batch operations, storage engine)
   Memory pressure     -> rules/deployment.md (resource limits, storage engine selection)
   Connection issues   -> rules/sdks.md (connection pooling, WebSocket vs HTTP)

3. Index audit:
   Missing index on filtered field  -> DEFINE INDEX ... ON TABLE ... FIELDS ...
   Full-text search slow             -> DEFINE INDEX ... SEARCH ANALYZER ...
   Vector search slow                -> DEFINE INDEX ... HNSW DIMENSION ... DIST ...

4. Storage engine review:
   Memory       -> Fast but volatile, development only
   RocksDB      -> General purpose, good read/write balance
   SurrealKV    -> Time-travel queries, versioned data
   TiKV         -> Distributed, horizontal scaling
```

### "User wants to write WASM extensions"

```
1. Reference rules/surrealism.md for Surrealism module system
2. Prerequisites: Rust toolchain, wasm32-unknown-unknown target
3. Workflow:
   a. Create Rust project with surrealism SDK
   b. Implement custom functions/analyzers
   c. Compile to WASM
   d. Deploy to SurrealDB instance
   e. Use in SurrealQL queries via custom function syntax
```

### "User wants to deploy / serve an ML model"

```
1. Reference rules/surrealml.md
2. Prerequisites: `surrealml` PyPI package 0.0.4 (extras: [sklearn] / [torch] /
   [tensorflow]); SurrealML is preview-stage and the SurrealQL invocation
   surface is unstable as of 2026-06-17.
3. The v1.4.0 documentation for `DEFINE MODEL`, `INFO FOR MODEL`,
   `ml::name<version>(...)`, `surreal ml import`, `db.upload_ml(...)`, and
   `SurMlFile.from_<framework>(...)` was retracted in v1.4.1 -- those
   surfaces were not present in current upstream. Treat anything beyond the
   `.surml` artifact format and the supported pip extras as pending
   verification; pin to a specific surrealml commit and consult the upstream
   `clients/python` source before writing code.
4. Stable patterns that don't depend on the unstable ML surface:
   - DEFINE INDEX ... HNSW DIMENSION ... DIST COSINE for vector storage
   - Compute embeddings client-side, persist with UPDATE in the same
     transaction
```

### "User hit a surprising SurrealDB behavior / gotcha"

```
1. Reference rules/gotchas.md first — cross-domain footgun catalog (v3.1.4+)
2. Narrow by domain:
   Graph / RELATE / traversal     -> rules/graph-queries.md
   Vector / HNSW / DiskANN        -> rules/vector-search.md
   Permissions / auth             -> rules/security.md
   Upgrade / deploy / metrics     -> rules/deployment.md
   MCP / agent tooling            -> rules/surrealmcp.md
   Language / schema DDL          -> rules/surrealql.md
3. Confirm server version — many gotchas are version-gated (3.0.5 vs 3.1.x)
4. Recommend v3.1.4+ minimum for production when security fixes apply
```

### "User wants AI agents to talk to SurrealDB"

```
1. Reference rules/surrealmcp.md
2. Choose MCP surface:
   Built-in (SurrealDB 3.1+) -> `surreal mcp` stdio or HTTP POST /mcp on a running server
   Standalone surrealmcp     -> extended tool catalog, cloud helpers, multi-endpoint switching
3. Built-in stdio (local IDE hosts — Cursor, Claude Desktop, Copilot in VS Code, Zed):
   surreal mcp --endpoint ws://localhost:8000/rpc --ns ... --db ... --user ... --pass ...
   WARNING: stdio MCP grants owner-level tool access with no login step — do not expose to untrusted hosts.
4. Standalone install (when built-in tools are insufficient):
   `cargo install --path .` from github.com/surrealdb/surrealmcp,
   OR `docker run --rm -i --pull always surrealdb/surrealmcp:latest start`.
   `surrealmcp` is NOT published to crates.io or npm.
5. Add to host MCP config — consult each host's own MCP docs for path/key shape.
6. Standalone binary requires `start` subcommand: `surrealmcp start --ns ... --db ...`.
   Connection env vars: SURREALDB_URL / SURREALDB_NS / SURREALDB_DB /
   SURREALDB_USER / SURREALDB_PASS. Server-side env vars use SURREAL_MCP_* prefix.
7. Production: scoped DB user (DEFINE USER ... ON DATABASE ROLES VIEWER),
   TLS, JWT bearer auth, `--rate-limit-rps` / `--rate-limit-burst` (standalone),
   RUST_LOG for structured logging, GET /health for health checks (standalone HTTP).
```

### "User wants editor / IDE support"

```
1. Reference rules/editor-tooling.md
2. Prerequisites: an LSP binary on $PATH. First-party baseline:
   `surrealql-language-server` v0.1.6. `surql-lsp` v0.1.1 is a separate
   community crate.
3. Pick the editor:
   VS Code / Cursor / Windsurf -> "SurrealQL" extension (Marketplace + OpenVSX)
   JetBrains                    -> "SurrealQL" plugin (JetBrains Marketplace)
   Neovim                       -> surrealdb/surrealql-neovim + nvim-treesitter
   Helix                        -> wire via languages.toml once LSP is on $PATH
   Zed                          -> Zed extensions panel
4. Custom web editors -> `@surrealdb/codemirror` / `@surrealdb/lezer` v1.0.6
5. Per-extension command palettes, settings catalogs, and config-file
   schemas must still be verified against each extension's own README.
```

### "User wants LangChain / RAG"

```
1. Reference rules/langchain.md + rules/vector-search.md
2. Python (verified package: langchain-surrealdb 0.2.1, deps
   langchain-core ~= 1.1.0 and surrealdb ~= 1.0.8 -- v1 SurrealDB SDK,
   not v2):
   pip install -U langchain-surrealdb surrealdb
   # Open the connection yourself, then pass it to the constructor:
   conn = Surreal("ws://localhost:8000/rpc")
   conn.signin({"username": "root", "password": "root"})
   conn.use("ns", "db")
   store = SurrealDBVectorStore(embeddings, conn)
   # Note: kwarg is `custom_filter`, not `filter`
   store.similarity_search_with_score(query=..., k=..., custom_filter={...})
3. JS/TS: NO official `@langchain/surrealdb` npm package as of 2026-06-17;
   the v1.4.0 documentation for it was retracted in v1.4.1. Use the v2
   JavaScript SurrealDB SDK directly until an official integration ships.
4. For multi-tenant:
   DEFINE TABLE document PERMISSIONS FOR select WHERE tenant_id = $auth.tenant_id;
   Then signin with DEFINE ACCESS record-level user before constructing the store
5. For server-side embeddings: SurrealML's invocation surface is unstable
   (rules/surrealml.md). Compute embeddings in Python with the embedding
   provider of your choice and persist via the vector store, OR via your
   own DEFINE FUNCTION wrapping a Surrealism extension.
```

### "User wants n8n / AI framework / ecosystem integration"

```
1. Reference rules/ecosystem-integrations.md.
2. n8n:
   - Use scoped npm package `@surrealdb/n8n-nodes-surrealdb` v0.6.0.
   - Self-hosted n8n only; community nodes do not run in n8n Cloud.
   - HTTP/HTTPS only; do not configure ws:// or wss:// endpoints.
   - Set N8N_COMMUNITY_PACKAGES_ALLOW_TOOL_USAGE=true only if exposing the
     node as an AI tool.
   - Use scoped SurrealDB users and parameterized query inputs.
3. AI framework docs:
   - LangChain has a verified local rule (`rules/langchain.md`).
   - Agno, Camel, CrewAI, Dagster, Google Agent, Kreuzberg, LlamaIndex,
     Pydantic AI, and SmolAgents are docs-index pointers. Verify package,
     import path, constructor/API shape, and SDK dependency before coding.
4. Spectron / Agent Memory Context:
   - Treat as roadmap-only until upstream publishes installable packages,
     schema/API docs, and operational guidance.
5. Official agent skills:
   - `npx skills add surrealdb/agent-skills` installs upstream narrow skills;
     this repo remains the broader SurrealDB 3 rule set.
```

### "User migrating from another database"

```
Source database?
  PostgreSQL/MySQL/SQL -> rules/data-modeling.md (relational mapping to SurrealDB)
                          rules/surreal-sync.md (CDC migration with Surreal-Sync)
  MongoDB/CouchDB      -> rules/data-modeling.md (document model, record IDs)
                          rules/surreal-sync.md (CDC migration)
  Neo4j/graph DB       -> rules/graph-queries.md (edge table mapping, traversal equivalents)
  SurrealDB v2         -> rules/surrealql.md (v2->v3 breaking changes)
                          surreal export/import for data migration
  Redis/key-value      -> rules/data-modeling.md (record ID patterns, schemaless mode)

Migration steps:
  1. Map source schema to SurrealDB tables/fields
  2. Use Surreal-Sync for CDC if available (rules/surreal-sync.md)
  3. Or export -> transform -> import with surreal CLI
  4. Verify with schema introspection
```

## Common Workflows

### 1. Verify environment and connect

```bash
# Health check
uv run {baseDir}/scripts/doctor.py

# Start dev server (LOCAL DEV ONLY -- use scoped credentials in production)
surreal start memory --user root --pass root --bind 127.0.0.1:8000

# Connect (local dev)
surreal sql --endpoint http://localhost:8000 --user root --pass root --ns test --db test
```

### 2. Design and apply a schema

```surql
-- Define namespace and database context
USE NS myapp DB production;

-- Define a schemafull table with fields and indexes
DEFINE TABLE user SCHEMAFULL;
DEFINE FIELD name ON TABLE user TYPE string;
DEFINE FIELD email ON TABLE user TYPE string ASSERT string::is::email($value);
DEFINE FIELD created ON TABLE user TYPE datetime DEFAULT time::now();
DEFINE INDEX idx_user_email ON TABLE user FIELDS email UNIQUE;

-- Define a graph edge table
DEFINE TABLE follows SCHEMAFULL TYPE RELATION IN user OUT user;
DEFINE FIELD since ON TABLE follows TYPE datetime DEFAULT time::now();

-- Define permissions
DEFINE TABLE post SCHEMALESS
  PERMISSIONS
    FOR select WHERE published = true OR author = $auth.id
    FOR create, update WHERE author = $auth.id
    FOR delete WHERE author = $auth.id OR $auth.role = 'admin';
```

```bash
surreal import --endpoint http://localhost:8000 --user root --pass root \
  --ns myapp --db production schema.surql

uv run {baseDir}/scripts/schema.py introspect
```

### 3. Set up vector search

```surql
-- Define table with vector field
DEFINE TABLE document SCHEMALESS;
DEFINE FIELD content ON TABLE document TYPE string;
DEFINE FIELD embedding ON TABLE document TYPE array<float> ASSERT array::len($value) = 1536;

-- Create HNSW vector index
DEFINE INDEX idx_doc_embedding ON TABLE document FIELDS embedding
  HNSW DIMENSION 1536 DIST COSINE;

-- Query by similarity
SELECT *, vector::similarity::cosine(embedding, $query_vec) AS score
  FROM document
  WHERE embedding <|10,40|> $query_vec
  ORDER BY score DESC
  LIMIT 10;
```

### 4. Graph traversal queries

```surql
-- Create records and relationships
CREATE person:alice SET name = 'Alice', role = 'engineer';
CREATE person:bob SET name = 'Bob', role = 'manager';
CREATE project:atlas SET name = 'Atlas', status = 'active';

RELATE person:alice->works_on->project:atlas SET since = d'2025-01-15';
RELATE person:bob->manages->project:atlas;
RELATE person:bob->mentors->person:alice SET topic = 'architecture';

-- Traverse outgoing edges
SELECT ->works_on->project.name AS projects FROM person:alice;

-- Traverse incoming edges
SELECT <-works_on<-person.name AS engineers FROM project:atlas;

-- Multi-hop traversal
SELECT ->mentors->person->works_on->project.name AS mentee_projects FROM person:bob;

-- Bidirectional traversal
SELECT <->mentors<->person.name AS mentorship_peers FROM person:alice;
```

### 5. Production deployment checklist

```bash
# 1. Choose storage engine (see rules/deployment.md)
# NOTE: 0.0.0.0 is correct for production servers behind a firewall/load balancer.
# For local dev, use 127.0.0.1 instead.
surreal start rocksdb://data/production.db \
  --user $SURREAL_USER --pass $SURREAL_PASS \
  --bind 0.0.0.0:8000 \
  --log info

# 2. Apply schema
surreal import --endpoint $SURREAL_ENDPOINT \
  --user $SURREAL_USER --pass $SURREAL_PASS \
  --ns production --db main schema.surql

# 3. Set up access control (see rules/security.md)
# 4. Configure backups
surreal export --endpoint $SURREAL_ENDPOINT \
  --user $SURREAL_USER --pass $SURREAL_PASS \
  --ns production --db main backup-$(date +%Y%m%d).surql

# 5. Verify
uv run {baseDir}/scripts/doctor.py --endpoint $SURREAL_ENDPOINT
uv run {baseDir}/scripts/schema.py introspect --endpoint $SURREAL_ENDPOINT
```

## Rules Manifest

| Rule | Description |
|------|-------------|
| `rules/surrealql.md` | Complete SurrealQL language reference: statements, functions, operators, idioms, v2-to-v3 migration notes |
| `rules/data-modeling.md` | Schema design patterns: record IDs, field types, schemafull vs schemaless, normalization, multi-model strategies, time-series, geospatial |
| `rules/graph-queries.md` | Graph edge creation with RELATE, traversal operators (-> <- <->), path expressions, recursive queries, filtering edges, aggregation |
| `rules/vector-search.md` | Vector field definitions, HNSW indexes (the v3 vector index type; brute-force is a fallback during index build/rebuild), distance metrics, similarity functions, RAG pipeline patterns, hybrid search |
| `rules/security.md` | Row-level permissions, DEFINE ACCESS (JWT, record), DEFINE USER, namespace/database/table scoping, $auth/$session variables, authentication flows |
| `rules/deployment.md` | Installation methods, storage engines (memory, RocksDB, SurrealKV, TiKV), Docker, Kubernetes Helm charts, production hardening, backup/restore, monitoring; `surrealdb/setup-surreal@v2` GitHub Action for CI (the v1.4.0 documentation that described setup-surreal as a CLI bootstrap was retracted in v1.4.2) |
| `rules/performance.md` | Index strategies (unique, search, HNSW), EXPLAIN for query analysis, batch operations, connection pooling, storage engine trade-offs, resource limits |
| `rules/sdks.md` | Official SDK usage for JS/TS, Python, Go, Rust, Java, Kotlin, .NET, C, PHP, Swift, Ruby plus source-only C boundary: connection setup, authentication, CRUD, live queries, typed records |
| `rules/surrealism.md` | Surrealism WASM extension system (new in v3): Rust SDK, custom functions, custom analyzers, module lifecycle, deployment |
| `rules/surrealml.md` | SurrealML scope summary (preview/unstable as of 2026-06-17); `.surml` artifact format, supported pip extras, GitHub v0.1.2 vs PyPI 0.0.4 boundary, setup-time native-library download warning |
| `rules/surrealmcp.md` | Model Context Protocol server (`surrealdb/surrealmcp` v0.4.0): verified install (Cargo from source / Docker; not on crates.io or npm), `surrealmcp start` CLI shape, `SURREALDB_*` env-var conventions, snake_case tool catalog grouped per upstream README, host-config pointers for Claude Desktop / Cursor / Copilot in VS Code / Zed / n8n, JWT bearer auth for HTTP mode |
| `rules/editor-tooling.md` | First-party `surrealql-language-server` v0.1.3, community `surql-lsp` boundary, `surrealql-tree-sitter`, CodeMirror packages, and discoverability pointers for VS Code / Cursor / Windsurf / VSCodium / JetBrains / Neovim / Helix / Sublime / Zed / Emacs extensions |
| `rules/langchain.md` | LangChain integration: `langchain-surrealdb` 0.2.1 (Python only) -- verified deps (`langchain-core ~= 1.1.0`, `surrealdb ~= 1.0.8` v1 SDK), constructor-based `SurrealDBVectorStore(embeddings, conn)` API, `custom_filter` kwarg. JS package, async class, chat history, and hybrid retriever from v1.4.0 were retracted in v1.4.1 |
| `rules/ecosystem-integrations.md` | n8n community node (`@surrealdb/n8n-nodes-surrealdb` v0.6.0), official AI framework docs index, Spectron roadmap boundary, CodeMirror, official Agent Skills repo |
| `rules/surrealist.md` | Surrealist IDE/GUI: schema designer, query editor, graph visualizer, table explorer, connection management |
| `rules/surreal-sync.md` | Surreal-Sync CDC tool: source connectors, target connectors, migration workflows, incremental sync, schema translation |
| `rules/surrealfs.md` | SurrealFS AI agent filesystem: file storage and retrieval, metadata management, directory structures, agent integration patterns |
| `rules/surrealkit.md` | SurrealKit schema sync, rollout-based migrations, seeding, and declarative schema/API tests |
| `rules/gotchas.md` | Cross-domain edge cases, footguns, and verified gotchas (upgrade, graph, vector, security, MCP, SDKs) |

## Configuration Requirements

| Requirement | How to Check | How to Fix |
|-------------|-------------|------------|
| surreal CLI | `surreal version` | `brew install surrealdb/tap/surreal` or see [install docs](https://surrealdb.com/install) |
| Python 3.10+ | `python3 --version` | Install from python.org or use system package manager |
| uv runtime | `which uv` | `brew install uv` or `pip install uv` |
| SurrealDB server | `uv run {baseDir}/scripts/doctor.py` | `surreal start memory --user root --pass root` |

Environment variables (optional, all have defaults):

| Variable | Default | Description |
|----------|---------|-------------|
| `SURREAL_ENDPOINT` | `http://localhost:8000` | SurrealDB server URL |
| `SURREAL_USER` | `root` | Authentication username |
| `SURREAL_PASS` | `root` | Authentication password |
| `SURREAL_NS` | `test` | Default namespace |
| `SURREAL_DB` | `test` | Default database |

## Output Contracts

All scripts: **stderr** = human-readable (Rich), **stdout** = JSON.

### `doctor.py`

```json
{
  "status": "healthy",
  "checks": {
    "cli_installed": true,
    "cli_version": "3.0.0",
    "server_reachable": true,
    "auth_valid": true,
    "namespace_exists": true,
    "database_exists": true,
    "storage_engine": "rocksdb"
  },
  "issues": []
}
```

### `doctor.py` (with issues)

```json
{
  "status": "unhealthy",
  "checks": {
    "cli_installed": true,
    "cli_version": "3.0.0",
    "server_reachable": false,
    "auth_valid": false,
    "namespace_exists": false,
    "database_exists": false,
    "storage_engine": null
  },
  "issues": ["Server not reachable at http://localhost:8000"]
}
```

### `schema.py introspect`

```json
{
  "namespace": "test",
  "database": "test",
  "tables": [
    {
      "name": "user",
      "type": "normal",
      "schema_mode": "schemafull",
      "fields": [
        {"name": "name", "type": "string", "default": null, "assert": null},
        {"name": "email", "type": "string", "default": null, "assert": "string::is::email($value)"}
      ],
      "indexes": [
        {"name": "idx_user_email", "fields": ["email"], "unique": true, "search": false, "vector": false}
      ],
      "events": [],
      "permissions": {"select": "FULL", "create": "FULL", "update": "FULL", "delete": "FULL"}
    }
  ],
  "accesses": [],
  "users": []
}
```

### `schema.py tables`

```json
{
  "tables": [
    {"name": "user", "type": "normal", "fields": 5, "indexes": 2, "events": 0},
    {"name": "follows", "type": "relation", "fields": 1, "indexes": 0, "events": 0},
    {"name": "post", "type": "normal", "fields": 8, "indexes": 3, "events": 1}
  ]
}
```

### `onboard.py --agent`

```json
{
  "skill": "surrealdb",
  "version": "1.7.1",
  "capabilities": ["surrealql", "data-modeling", "graph-queries", "vector-search", "security", "deployment", "performance", "sdks", "surrealism", "surrealml", "surrealmcp", "editor-tooling", "langchain", "ecosystem-integrations", "surrealist", "surreal-sync", "surrealfs", "surrealkit", "gotchas"],
  "scripts": ["doctor.py", "schema.py", "onboard.py", "check_upstream.py"],
  "rules": ["surrealql.md", "data-modeling.md", "graph-queries.md", "vector-search.md", "security.md", "deployment.md", "performance.md", "sdks.md", "surrealism.md", "surrealml.md", "surrealmcp.md", "editor-tooling.md", "langchain.md", "ecosystem-integrations.md", "surrealist.md", "surreal-sync.md", "surrealfs.md", "surrealkit.md", "gotchas.md"],
  "prerequisites": {
    "surreal_cli": true,
    "python": true,
    "uv": true,
    "server_reachable": true
  }
}
```

## Error Handling

| Exit Code | Meaning | Recovery |
|-----------|---------|----------|
| 0 | Success | N/A |
| 1 | Error | Check stderr for details |

Common errors:

- **surreal CLI not found**: Install with `brew install surrealdb/tap/surreal` or see https://surrealdb.com/install
- **Server not reachable**: Start a server with `surreal start memory --user root --pass root`
- **Authentication failed**: Verify `SURREAL_USER` and `SURREAL_PASS` environment variables
- **Namespace/database not found**: Create with `DEFINE NAMESPACE ...` / `DEFINE DATABASE ...` or use `USE NS ... DB ...` in SurrealQL
- **Schema import failed**: Check SurrealQL syntax; run `surreal sql` to test queries interactively
- **Permission denied**: Check table-level permissions in `rules/security.md`

## Version Information

| Component | Version |
|-----------|---------|
| SurrealDB target | 3.1.4+ (recommend minimum for production) |
| Skill version | 1.7.1 |
| SurrealQL compat | SurrealDB 3.x |
| Python requirement | 3.10+ |

## Source Provenance

This skill was built from the following upstream sources. Use `check_upstream.py`
to detect what changed since this snapshot for incremental updates.

```bash
uv run {baseDir}/scripts/check_upstream.py          # full diff report
uv run {baseDir}/scripts/check_upstream.py --stale   # only changed repos
```

| Repository | Release | SHA (short) | Snapshot Date | Rules Affected |
|------------|---------|-------------|---------------|----------------|
| surrealdb/surrealdb | v3.1.4 | `c9e039542e85` | 2026-06-10 | surrealql, data-modeling, security, performance, deployment, surrealism, surrealml, surrealmcp, vector-search, graph-queries |
| surrealdb/surrealist | surrealist-v3.9.0 | `b0f4b03b3c6e` | 2026-06-16 | surrealist |
| surrealdb/surrealdb.js | v2.0.3 | `c25ccbd12864` | 2026-06-17 | sdks |
| surrealdb/surrealdb.py | v2.0.0 (PyPI); main 3.0.0 unreleased | `616cc6eb65e7` | 2026-06-17 | sdks |
| surrealdb/surrealdb.go | v1.4.0 (main) | `82ed1db52c9e` | 2026-06-17 | sdks |
| surrealdb/surrealdb.java | v2.1.1 | `175bf2584fb3` | 2026-06-10 | sdks |
| surrealdb/surrealdb.net | v0.10.2 | `ab079d855b6f` | 2026-06-17 | sdks |
| surrealdb/surrealdb.php | v1.0.1 | `2f8f7ade9c47` | 2026-03-02 | sdks |
| surrealdb/surrealdb.c | -- | `039481e0c46f` | 2026-03-06 | sdks |
| surrealdb/surrealdb.swift | -- | `046f7d5f2405` | 2026-04-29 | sdks |
| surrealdb/surrealdb.kotlin | -- | `1d91ee969664` | 2026-05-13 | sdks |
| surrealdb/surrealdb.rb | v0.7.0 | `5a98c3464b1f` | 2026-04-01 | sdks |
| surrealdb/surreal-sync | v0.3.4 | `59b3166910f0` | 2026-03-11 | surreal-sync |
| surrealdb/surrealfs | -- | `0008a3a94dbe` | 2026-01-29 | surrealfs |
| surrealdb/surrealkit | v0.7.0 | `8b83dd867338` | 2026-06-11 | surrealkit |
| surrealdb/surrealmcp | v0.4.0 (standalone; built-in MCP in server 3.1+) | `6b82d699ece8` | 2026-01-14 | surrealmcp |
| surrealdb/surrealml | v0.1.2 GitHub; 0.0.4 PyPI | `152ac2d508f1` | 2025-09-17 | surrealml |
| surrealdb/surrealql-language-server | v0.1.6 | `02706f9c6c98` | 2026-05-28 | editor-tooling |
| surrealdb/surrealql-tree-sitter | -- | `5db387281bcc` | 2026-05-07 | editor-tooling |
| surrealdb/codemirror | v1.0.6 | `f88011f3ac07` | 2026-05-19 | editor-tooling, ecosystem-integrations |
| surrealdb/langchain-surrealdb | v0.2.1 | `4cfecc53efbc` | 2026-03-16 | langchain |
| surrealdb/n8n-nodes-surrealdb | v0.6.0 | `a14db7def6e2` | 2026-04-24 | ecosystem-integrations |
| surrealdb/agent-skills | -- | `95628976c277` | 2026-06-17 | ecosystem-integrations |

Documentation: [surrealdb.com/docs](https://surrealdb.com/docs) snapshot 2026-06-17.

Full provenance data: `SOURCES.json` (machine-readable).
