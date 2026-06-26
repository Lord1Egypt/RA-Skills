# SurrealDB Ecosystem Integrations

This rule captures first-party or official-docs ecosystem surfaces that do not
yet justify a full dedicated rule, or whose exact API should be re-verified
before implementation. Use this as an ecosystem map, not as a substitute for
the focused rules (`rules/sdks.md`, `rules/langchain.md`,
`rules/editor-tooling.md`, `rules/surrealmcp.md`).

Verified snapshot: 2026-06-17.

---

## New Ecosystem Surfaces (since v1.6.6)

| Project | Status | Skill pointer |
|---|---|---|
| [surqlize](https://github.com/surrealdb/surqlize) | Active development | Type-safe TypeScript ORM with graph support — verify API before examples |
| [datasets](https://github.com/surrealdb/datasets) | Official sample data | Browse in Surrealist v3.9+ datasets panel |
| [agent-memory](https://github.com/surrealdb/agent-memory) | Demo only | KG + vector agent memory reference; requires `--allow-experimental` |
| [kaig](https://github.com/surrealdb/kaig) | Demo | Graph RAG knowledge AI sample |
| Built-in MCP (`surreal mcp`) | GA in SurrealDB 3.1+ | `rules/surrealmcp.md` — prefer over standalone for local IDE hosts |

---

## n8n Community Node

The official n8n node lives at `surrealdb/n8n-nodes-surrealdb` and publishes
the scoped npm package `@surrealdb/n8n-nodes-surrealdb`.

Current verified release: `v0.6.0` / npm `0.6.0` (2026-04-24). v0.6.0 adds
SurrealDB server v3 support by upgrading to the JavaScript SDK `surrealdb`
`^2.0.3`, and the release workflow uses trusted publishing.

Install in a self-hosted n8n instance:

```text
Settings -> Community Nodes -> Install -> @surrealdb/n8n-nodes-surrealdb
```

Important boundaries:

- Self-hosted n8n only. Community nodes do not run in n8n Cloud.
- HTTP/HTTPS only. The node does not support `ws://` or `wss://` connection
  strings because of n8n's execution model.
- To expose the node as an AI tool, set
  `N8N_COMMUNITY_PACKAGES_ALLOW_TOOL_USAGE=true`.
- Credential scopes are root, namespace, or database. Use scoped SurrealDB
  users for production workflows instead of root credentials.
- Prefer the node's parameter fields for query variables; don't concatenate
  untrusted user input into raw SurrealQL strings.

Operations covered by the upstream README and docs include record CRUD, table
operations, field/index operations, relationship operations, raw query
execution, visual SELECT-query building, health check, version, and connection
pool statistics.

---

## AI Framework Docs Index

The official docs index now lists multiple AI framework integrations:

- Agno
- Camel
- CrewAI
- Dagster
- Google Agent
- Kreuzberg
- LangChain
- LlamaIndex
- Pydantic AI
- SmolAgents

Only LangChain has a fully verified local rule in this skill
(`rules/langchain.md`). For every other framework, treat the docs page as a
pointer and verify the package, import path, constructor/API shape, and current
SurrealDB SDK dependency before writing code.

Default production pattern across these frameworks:

1. Compute embeddings or agent memory artifacts in the framework runtime.
2. Persist structured data, graph edges, and vectors through an official
   SurrealDB SDK.
3. Enforce tenant/user isolation in SurrealDB with `DEFINE ACCESS` and table
   permissions instead of trusting framework-side filters only.

---

## Spectron / Agent Memory Context

Spectron remains **preview/alpha** — not a generally available runtime API.
However, upstream SDK main branches now expose Spectron-related endpoints:

- **surrealdb.js** main: Spectron package at `1.0.0-alpha.4` (unreleased on npm)
- **surrealdb.py** main: Spectron SDK endpoints added (unreleased on PyPI)

Do not present Spectron as stable. Pin to explicit commits and audit before
production. The [`surrealdb/agent-memory`](https://github.com/surrealdb/agent-memory)
demo shows a reference architecture combining graph + vectors; it requires
experimental server flags and is not a production template.

Stable building blocks available today:

- `rules/vector-search.md` for HNSW and DiskANN vector storage and retrieval
- `rules/graph-queries.md` for graph edges and traversal
- `rules/security.md` for access control and tenant isolation
- `rules/langchain.md` for the currently verified Python LangChain vector store
- `rules/surrealmcp.md` for agent tool access to SurrealDB

---

## CodeMirror

The official CodeMirror packages are tracked in `rules/editor-tooling.md`:
`@surrealdb/codemirror` and `@surrealdb/lezer` v1.0.6. Use them when building a
custom web editor that needs SurrealQL syntax support. They are not database
clients and do not replace the language server for schema-aware diagnostics.

---

## Official Agent Skills Repo

SurrealDB also maintains `surrealdb/agent-skills`, a separate Agent Skills
standard repository. Current verified commit: `95628976c277` (2026-06-17).
Four additional upstream skills shipped since the v1.6.6 snapshot.

Install all official upstream skills:

```bash
npx skills add surrealdb/agent-skills
```

Install a specific upstream skill:

```bash
npx skills add surrealdb/agent-skills --skill surrealql
npx skills add surrealdb/agent-skills --skill surrealdb-vector
npx skills add surrealdb/agent-skills --skill surrealdb-python
```

Those upstream skills are narrower and are not a drop-in replacement for this
package. This repo tracks a broader, adversarially corrected rule set across
SurrealDB 3, SDKs, tooling, deployment, security, and AI-agent surfaces.

---

## Cross-References

- Official docs overview: `https://surrealdb.com/docs`
- Official integrations docs: `https://surrealdb.com/docs/integrations`
- n8n docs: `https://surrealdb.com/docs/integrations/data-management/n8n/`
- n8n repo: `https://github.com/surrealdb/n8n-nodes-surrealdb`
- CodeMirror repo: `https://github.com/surrealdb/codemirror`
- Agent Skills repo: `https://github.com/surrealdb/agent-skills`
