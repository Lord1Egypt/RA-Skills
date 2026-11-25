---
name: synapcores-memory
description: "Give the agent long-term memory that survives restarts — store facts, recall them semantically, and forget them on request — backed by a self-hosted SynapCores database. Use when the user asks you to remember something, asks what you remember, wants to correct or delete a stored fact, or wants persistent memory across sessions."
homepage: https://github.com/SynapCores/synapcores-openclaw-memory
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "requires":
          { "bins": ["curl", "jq"], "env": ["SYNAPCORES_API_KEY"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "jq",
              "bins": ["jq"],
              "label": "Install jq (brew)",
            },
          ],
      },
  }
---

# SynapCores Memory

Long-term memory for the agent, stored in a database you run yourself. Memories
are embedded on write and retrieved by meaning, not keywords — "what coffee does
he like" finds "prefers dark roast" without sharing a single word.

Your data stays in the SynapCores gateway you run, which is on this machine unless you
point `SYNAPCORES_URL` at a server of your own. Embeddings are computed inside the engine;
there is no external API key and no third-party service in the path.

## When to use this

- The user says "remember that…", "don't forget…", "for future reference…"
- The user asks "what do you remember about…", "what did I tell you about…"
- The user corrects or retracts something you stored
- You need context from an earlier session

## Setup

**1. Run a SynapCores gateway** (once). Bind it to loopback so your personal
memory database stays local to this machine, and pin the image **by digest** so
the published tag can never be swapped under you:

```bash
docker run -d --name synapcores -p 127.0.0.1:8080:8080 \
  -v synapcores-data:/var/lib/synapcores \
  ghcr.io/synapcores/community:v2.5.1-ce@sha256:c2a583fef157b3d6afab1844641d95185d4893ac5a8f1268aa56f7af40707f1a
```

SynapCores sends an anonymous install/heartbeat ping (version, OS, a random install id; never data, queries or prompts); add `-e SYNAPCORES_TELEMETRY=off` to turn it off.

On first boot the gateway prints **your own** admin login and a starter API key
to its own startup console. Read that startup output on your machine and copy
the `aidb_…` API key it shows. It is your credential — the
plugin only ever sends it to your own gateway, never anywhere else.

**2. Export the key and the gateway URL:**

```bash
export SYNAPCORES_API_KEY="aidb_…"
export SYNAPCORES_URL="http://127.0.0.1:8080"
```

For a gateway on another machine, use its `https://` address instead, so the
key and your memories stay encrypted on the network. The helper below checks
this for you: it accepts `https://` anywhere and plain `http://` on this machine
(`localhost`, `127.0.0.1`, `[::1]`). For a gateway on a private network you
trust, `export SYNAPCORES_ALLOW_INSECURE_HTTP=1` lets it use plain `http://`.

The first `MEMORY_STORE` below doubles as your connectivity check — a `401`
means the key is wrong, and a connection error means the gateway is not up yet.

## Usage

Every operation is one SQL statement over HTTP. Define this helper once per
shell session:

```bash
sc() {
  # The API key rides on every request: keep it on this machine or on TLS.
  case "$SYNAPCORES_URL" in
    *@*) echo "sc: SYNAPCORES_URL must not contain '@'" >&2; return 1 ;;
    https://*|http://localhost|http://localhost[:/]*|http://127.0.0.1|http://127.0.0.1[:/]*|http://\[::1\]|http://\[::1\][:/]*) ;;
    *) [ "$SYNAPCORES_ALLOW_INSECURE_HTTP" = 1 ] || {
         echo "sc: use an https:// SYNAPCORES_URL for a gateway on another machine" \
              "(or set SYNAPCORES_ALLOW_INSECURE_HTTP=1 for a private network you trust)" >&2
         return 1; } ;;
  esac
  curl -s -m 120 -X POST "$SYNAPCORES_URL/v1/query/execute" \
    -H 'Content-Type: application/json' \
    -H "Authorization: Bearer $SYNAPCORES_API_KEY" \
    -d "$(jq -nc --arg sql "$1" '{sql:$sql}')"
}
```

Using `jq -nc` to build the body matters: memory text routinely contains quotes
and apostrophes, and hand-built JSON breaks on them.

### Remember something

```bash
sc "SELECT MEMORY_STORE('default', 'Luis prefers dark roast and takes calls after 10am') AS id" \
  | jq -r '.data.rows[0][0]'
# mem_1kzv0fkzy_AK7TUf
```

Note the SQL string quoting: **single quotes are strings, double quotes are
identifiers.** A double-quoted value is read as a column name and will error.
Escape an apostrophe by doubling it — `'Luis''s laptop'`.

Optional metadata for later filtering:

```bash
sc "SELECT MEMORY_STORE('default', 'Renewal call scheduled for March',
      json_object('category','decision')) AS id" | jq -r '.data.rows[0][0]'
```

### Recall

```bash
sc "SELECT content, similarity FROM MEMORY_RECALL('default', 'what coffee does he like', 5)" \
  | jq -r '.data.rows[] | "\(.[1] | tonumber | .*100 | round)%  \(.[0])"'
# 39%  Luis prefers dark roast and takes calls after 10am
```

That is the whole point: the stored sentence never says "coffee", and it is
still the top hit. Keyword search returns nothing here.

`MEMORY_RECALL(namespace, query [, top_k])` is table-valued — it goes in `FROM`,
not `SELECT`. It returns `(id, content, similarity, metadata, created_at)`,
ordered by similarity, `top_k` defaulting to 10 and capped at 100. An unknown
namespace returns zero rows rather than an error.

**Read the similarity before you trust a hit.** These are cosine scores, and a
genuine match on this embedding model often sits around 0.5 rather than near
1.0. A low score across every row means nothing relevant is stored — say so
instead of presenting the closest row as fact.

### Forget

```bash
ID=$(sc "SELECT id FROM MEMORY_RECALL('default', 'renewal call', 1)" | jq -r '.data.rows[0][0]')
sc "SELECT MEMORY_FORGET('default', '$ID') AS deleted" | jq -r '.data.rows[0][0]'
# true
```

Returns `true` if a row was deleted, `false` if the id did not exist. This is a
hard delete — use it when the user asks you to forget something.

### Namespaces

The first argument is a namespace, stored as `_memory_<namespace>`. Use one per
person or project to keep memories apart. It must match
`^[A-Za-z_][A-Za-z0-9_]*$` — no hyphens.

## Good practice

- **Store the fact, not the transcript.** "Prefers dark roast" beats a
  paragraph of chat — short, self-contained statements retrieve far better.
- **Recall before you answer** anything personal, rather than guessing.
- **Ask before storing** anything sensitive, and never store credentials,
  payment details, or regulated data.
- **Recall before storing** to avoid near-duplicates piling up.

## Want this to happen automatically?

This skill is manual: you call it when it is relevant. The companion **plugin**
wires the same store into OpenClaw's memory slot so capture and recall happen on
their own, and adds SQL-filtered recall, graph relations between memories, and
AutoML relevance scoring:

```bash
openclaw plugins install clawhub:@synapcores/openclaw-memory
```

It reads the same `SYNAPCORES_API_KEY` and talks to the same gateway.

**Whether it reads the same memories depends on the engine version.** From
plugin v0.7.0 on a gateway running **v1.14.3-ce or newer**, the plugin uses the
`CREATE MEMORY` object — `REMEMBER` / `RECALL` / `CURRENT` / `FORGET` / `TRACE`,
backed by `_mem_<name>_*` tables — which is a *different* store from the
`_memory_<namespace>` table this skill writes to. On older gateways, and
whenever the plugin is configured with `memory.backend: "legacy"`, both write
the same table and everything here is shared. Check which one is live:

```bash
curl -s -H "Authorization: Bearer $SYNAPCORES_API_KEY" "$SYNAPCORES_URL/v1/memory"
# a JSON array  => the plugin will use the CREATE MEMORY object
# HTTP 404      => the plugin stays on the MEMORY_* functions this skill uses
```

## Troubleshooting

| symptom | cause |
|---|---|
| `Cannot reach the SynapCores gateway` | container not running — `docker ps`, then `docker logs synapcores` |
| `401` / rejected key | `SYNAPCORES_API_KEY` unset, stale, or has a trailing newline (store it clean) |
| `Unknown function: memory_store` | gateway older than v1.8.5-ce — `curl -s "$SYNAPCORES_URL/version"` |
| recall returns nothing | wrong namespace, or nothing stored yet — `sc "SELECT COUNT(*) FROM _memory_default"` |
| SQL error naming your text as a column | double quotes used for a string — use single quotes |

Verified against SynapCores v2.5.1-ce.
