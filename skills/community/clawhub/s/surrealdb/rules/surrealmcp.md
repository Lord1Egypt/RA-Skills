# SurrealMCP -- Model Context Protocol Server for SurrealDB

> **v1.7.0 status note:** SurrealDB **v3.1.0+** ships a **built-in MCP
> server** (`surreal mcp` stdio, HTTP `POST /mcp`) inside the main `surreal`
> binary. The standalone `surrealdb/surrealmcp` repo (v0.4.0) remains for
> extended tool catalogs, cloud helpers, and multi-endpoint switching. Prefer
> built-in MCP for local IDE hosts; use standalone surrealmcp when you need
> its extra tools or HTTP deployment patterns from the separate repo.

---

## Built-in MCP (SurrealDB v3.1.0+)

Since v3.1.0, every `surreal` binary includes MCP without a separate install.

```bash
# stdio — typical MCP host config (Cursor, Claude Desktop, VS Code Copilot)
surreal mcp --endpoint ws://127.0.0.1:8000/rpc --ns myns --db mydb \
  --user root --pass root

# Or attach to an already-running server (stdio transport)
surreal mcp --endpoint http://127.0.0.1:8000 --ns myns --db mydb
```

HTTP mode is exposed at `POST /mcp` on a running server (requires normal
SurrealDB authentication — unlike stdio, which grants owner-level tool access
with no login step). **Do not expose stdio MCP to untrusted hosts.**

Server-side tuning env vars (verified in [MCP docs](https://surrealdb.com/docs/build/ai-agents/mcp)):

| Variable | Default | Purpose |
|---|---|---|
| `SURREAL_HTTP_MAX_MCP_BODY_SIZE` | 4 MiB | Max MCP request body |
| `SURREAL_MCP_QUERY_TIMEOUT_SECS` | 60 | Query timeout for tool calls |
| `SURREAL_MCP_MAX_RESULT_BYTES` | 256 KiB | Max tool result size |
| `SURREAL_MCP_RUN_MAX_ARGS` | 64 | Max args for `run`-style tools |
| `SURREAL_MCP_PARAMS_MAX_KEYS` | 256 | Max keys in tool param objects |

Built-in tools include schema introspection resources and CRUD/query tools with
`read_only_hint` / `destructive_hint` / `idempotent_hint` annotations for MCP
clients. For the full standalone catalog (cloud tools, endpoint switching), see
the **SurrealMCP (standalone)** section below.

---

## SurrealMCP (standalone repo)

> **v1.4.1 status note:** v1.4.1 retracted the v1.4.0 install path, CLI
> shape, env-var names, and tool catalog (none matched
> `surrealdb/surrealmcp` upstream). This rule keeps the full tool
> argument schema by inspecting `surrealdb/surrealmcp` at tag `v0.4.0`
> directly (`src/tools/mod.rs`). Pin to that tag if you want the
> schemas below to match exactly; later upstream commits may add or
> rename tools.

SurrealMCP is the official Model Context Protocol (MCP) server published
under `surrealdb/surrealmcp`. It exposes a SurrealDB connection (local or
SurrealDB Cloud) to MCP-compatible clients (Claude Desktop, Cursor,
GitHub Copilot in VS Code, Zed, n8n, etc.) so an agent can read and
write a SurrealDB instance without bespoke per-host glue.

- Upstream: `https://github.com/surrealdb/surrealmcp`
- Status: preview
- Source-of-truth README: pin to upstream HEAD; consult for every
  install/CLI/tool detail not duplicated here

---

## When to Use SurrealMCP

| Use case | Why MCP fits |
|----------|--------------|
| Long-running agent loops over a project DB | One-shot connection setup, structured tool surface |
| Multi-host agent deployments (Claude + Cursor + Copilot on the same DB) | Single MCP config, identical tools across clients |
| Unattended automation (autoplan, /loop, scheduled agents) | Tool calls fail loudly; raw SDK calls get swallowed by streaming output |

Reach for SurrealMCP when an agent needs *programmatic* access that
survives across turns. Reach for the SDK (`rules/sdks.md`) when
application code is the consumer, not an agent.

---

## Installation (verified)

The upstream README documents two install paths:

```bash
# From source
git clone https://github.com/surrealdb/surrealmcp
cd surrealmcp
cargo install --path .

# Docker (preferred for unattended hosts)
docker run --rm -i --pull always surrealdb/surrealmcp:latest start
```

`cargo install surrealmcp` does **not** work -- the crate is not
published to crates.io. There is no published `npm` package either.
Use the source or Docker paths only.

---

## CLI Shape (verified)

The binary requires the `start` subcommand for every mode:

```bash
# stdio (default; what most MCP hosts launch)
surrealmcp start

# HTTP server
surrealmcp start --bind-address 127.0.0.1:8000

# Unix socket
surrealmcp start --socket-path /tmp/surrealmcp.sock
```

Connection flags (verified against upstream README):

| Flag | Purpose |
|------|---------|
| `--endpoint <URL>` | SurrealDB endpoint (e.g. `ws://localhost:8000/rpc`) |
| `--ns <name>` | Namespace |
| `--db <name>` | Database |
| `--user <name>` / `--pass <secret>` | DB credentials |
| `--bind-address <host:port>` | HTTP bind |
| `--server-url <url>` | Public-facing server URL |
| `--cloud-auth-server <url>` | SurrealDB Cloud auth server |
| `--expected-audience <aud>` | JWT audience validation |
| `--rate-limit-rps <n>` / `--rate-limit-burst <n>` | Rate limiting |
| `--auth-disabled` | Disable auth (dev only) |
| `--access-token <token>` / `--refresh-token <token>` | Pre-configured SurrealDB Cloud auth tokens (env-var equivalents: `SURREAL_MCP_CLOUD_ACCESS_TOKEN` / `SURREAL_MCP_CLOUD_REFRESH_TOKEN`) |
| `--socket-path <path>` | Listen on a Unix socket instead of HTTP |

Health check is HTTP, not a CLI subcommand:

```bash
curl http://localhost:8000/health
```

There is no `surrealmcp ping`, `surrealmcp serve`, `--transport`,
`--bind` (use `--bind-address`), `--auth-token` (use
`--access-token` / `--refresh-token`), `--max-concurrent-tools`,
`--namespace` (use `--ns`), `--database` (use `--db`), or
`--log-format json` flag in current upstream. Logging is configured via
`RUST_LOG` env var (`tracing-subscriber`).

---

## Environment Variables (verified)

```bash
# Connection
SURREALDB_URL=ws://localhost:8000/rpc
SURREALDB_NS=mynamespace
SURREALDB_DB=mydatabase
SURREALDB_USER=root
SURREALDB_PASS=root

# Server (HTTP mode)
SURREAL_MCP_BIND_ADDRESS=127.0.0.1:8000
SURREAL_MCP_SERVER_URL=https://mcp.surrealdb.com
SURREAL_CLOUD_AUTH_SERVER=https://auth.surrealdb.com
SURREAL_MCP_EXPECTED_AUDIENCE=https://custom.audience.com/
SURREAL_MCP_RATE_LIMIT_RPS=100
SURREAL_MCP_RATE_LIMIT_BURST=200
SURREAL_MCP_AUTH_REQUIRED=false
SURREAL_MCP_CLOUD_ACCESS_TOKEN=...
SURREAL_MCP_CLOUD_REFRESH_TOKEN=...
```

Note the `SURREALDB_*` prefix for connection vars and the
`SURREAL_MCP_*` prefix for server-side configuration. The
surreal-skills-wide `SURREAL_USER` / `SURREAL_PASS` convention used
in other rules is **not** what surrealmcp reads -- map your env
explicitly when wiring host configs.

---

## Configuring MCP Hosts

The upstream README includes installation walk-throughs for Cursor,
Claude Desktop, GitHub Copilot in VS Code, Zed, and n8n. Use those as
the source-of-truth for each host's exact JSON path and key shape; the
example below is the common skeleton.

```json
{
  "mcpServers": {
    "SurrealDB": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i", "--pull", "always",
        "surrealdb/surrealmcp:latest",
        "start"
      ]
    }
  }
}
```

For a non-Docker invocation, swap to `"command": "surrealmcp"` with
`"args": ["start"]` and pass connection details via the `env` block
using the verified env-var names above.

> **Cross-host config drift:** different hosts use different top-level
> keys (`mcpServers` vs `servers` vs `mcp.servers`). Always consult the
> host's own MCP docs for the exact path and shape.

---

## Available Tools (verified at `surrealdb/surrealmcp@v0.4.0`)

Tool wire-names are the snake-case method names on `SurrealService` in
`src/tools/mod.rs`. Argument types come from the `#[derive(schemars::
JsonSchema)]` `*Params` structs in the same file -- the schemas below
mirror what `tools/list` returns from a running v0.4.0 server.

### Database operations

| Tool | Required args | Optional args |
|------|---------------|---------------|
| `query` | `query: string` | `parameters: object` |
| `select` | `targets: string[]` | `where_clause`, `split_clause`, `group_clause`, `order_clause`, `limit_clause`, `start_clause` (all `string`); `parameters: object` |
| `insert` | `target: string`, `values: object[]` | `ignore: bool`, `relation: bool` |
| `create` | `target: string`, `data: object` | -- |
| `upsert` | `targets: string[]` | one of `patch_data: object[]` / `merge_data: object` / `content_data: object` / `replace_data: object`; `where_clause: string`; `parameters: object` |
| `update` | `targets: string[]` | one of `patch_data` / `merge_data` / `content_data` / `replace_data` (same shapes as `upsert`); `where_clause`; `parameters` |
| `delete` | `targets: string[]` | `where_clause: string`, `parameters: object` |
| `relate` | `from: string[]`, `with: string[]`, `table: string` | `content_data: object`, `parameters: object` |

Notes:

- For `upsert` / `update`, only one of the four data variants is
  meaningful per call -- the server applies whichever is provided in
  the order `patch → merge → content → replace`. Don't combine.
- `targets` entries may be plain table names (`user`) or fully-qualified
  record IDs (`user:abc`). Mixing both in one call is allowed.
- Every CRUD tool surfaces a `parameters` map that becomes bound
  variables in the underlying SurrealQL -- prefer this over inlining
  user-controlled strings into clause text.

### Connection management

| Tool | Required args | Optional args |
|------|---------------|---------------|
| `connect_endpoint` | `endpoint: string` | `namespace`, `database`, `username`, `password` (all `string`) |
| `use_namespace` | `namespace: string` | -- |
| `use_database` | `database: string` | -- |
| `list_namespaces` | -- | -- |
| `list_databases` | -- | -- |
| `disconnect_endpoint` | -- | -- |

`connect_endpoint.endpoint` accepts the same scheme set as the
SurrealDB SDK: `memory`, `file:/path`, `rocksdb:/path`,
`ws://host:port[/rpc]`, `wss://host:port[/rpc]`, `http://host:port`,
`https://host:port`, or `cloud:<instance_id>`.

### Cloud operations

| Tool | Required args |
|------|---------------|
| `list_cloud_organizations` | -- |
| `list_cloud_instances` | `organization_id: string` |
| `pause_cloud_instance` | `instance_id: string` |
| `resume_cloud_instance` | `instance_id: string` |
| `get_cloud_instance_status` | `instance_id: string` |
| `create_cloud_instance` | `name: string`, `organization_id: string` |

Cloud tools require the server to be configured with
`SURREAL_MCP_CLOUD_ACCESS_TOKEN` + `SURREAL_MCP_CLOUD_REFRESH_TOKEN` (or
their `--access-token` / `--refresh-token` CLI equivalents). Without
them the cloud client is constructed in unauthenticated mode and the
tools fail at call time.

### Schema-drift policy

Pin to `v0.4.0` if you depend on the table above. To verify a different
tag, dump the live tool surface from a running server:

```bash
# After starting `surrealmcp start` somewhere, hit /tools/list over the
# wire (HTTP transport shown; for stdio use the host's MCP inspector).
curl -s -X POST http://localhost:8000/tools/list \
  -H 'content-type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | jq
```

Compare the returned `inputSchema` JSON-Schemas against the table above
and update your call sites if anything diverges.

---

## Production Posture

| Concern | Posture |
|---------|---------|
| Network exposure | HTTP behind TLS termination + auth required; never expose stdio over a TCP forwarder |
| Auth | Bearer JWT with JWKS validation against the configured auth server; `--auth-disabled` is dev-only |
| Rate limiting | `--rate-limit-rps` / `--rate-limit-burst` flags |
| Health | `GET /health` endpoint |
| Audit logging | Configure `RUST_LOG`; SurrealMCP uses `tracing-subscriber` |
| Permission posture | Run with scoped DB credentials (`DEFINE USER ... ON DATABASE ROLES VIEWER`); see `rules/security.md` |

---

## Cross-References

- `rules/sdks.md` -- direct SDK use for application code
- `rules/security.md` -- DEFINE USER / DEFINE ACCESS for scoped credentials
- `rules/editor-tooling.md` -- editor LSP tooling (complements MCP)
- `rules/deployment.md` -- production hardening for the SurrealDB instance
- Upstream README: `https://github.com/surrealdb/surrealmcp/blob/main/README.md`
- Source-of-truth docs: `https://surrealdb.com/docs/integrations/`
