# Connections and credentials

A **Connection** turns Tokenrip into a general **API / inference router**: a named place (base URL, rules, default headers) where you, or any current member of the owning team, call an upstream through `rip connection call` (REST `POST /v0/connections/call`; this generic call is never an MCP tool). Calls saved on a connection as named **operations** run by name with `rip connection run`, and every agent that may call the connection, on a chat host too, sees each one as its own MCP tool (see [Operations](#operations--named-calls-and-the-tools-chat-hosts-see)). The key it sends lives in a **credential**: encrypted on the server, injected **server-side** on every call, and never shown to the caller. One credential can serve many connections, and rotating it reaches all of them. Return to [SKILL.md](../SKILL.md) for decision trees and workflows. For the full model (proxy safeguards, SSRF defense, failure codes, REST endpoints) read `docs/architecture/connections.md`.

## Why a Connection instead of a per-service tool

Point one Connection at any provider whose key you hold and the caller supplies only `--method` + `--path` (+ body). No backend change per integration. To reach the same provider from a chat host, save the calls agents need as operations: each is a tool with a fixed path, which the chat directories accept where they reject a tool that takes any method and path. The key stays encrypted at rest and is injected on every call, so a shared key can be *used* by people who never *see* it — the basis for team-owned connections and credentials.

## Ownership: personal vs team

Connections and credentials are each owned by a personal account **or** a team (`--team <slug>`), never both. A connection uses a credential of the same owner.

| Scope | Who can read / list / invoke | Who can create | Who can manage |
|---|---|---|---|
| Personal (default) | The owning account | The owning account | The owning account |
| Team (`--team <slug>`) | Any current team member | Any current team member | A connection: its creator or the team owner (update, disable, delete). A credential: its creator or the team owner (rename, rotate, restrict, delete, and attach it to a connection) |

Changing an attached connection's base URL, rules, default headers or default query also needs the credential's management right.

## Credentials

```bash
# A plain key (bearer, header or basic placement is chosen on the connection)
export POSTHOG_KEY=phx_...
rip credential create --team quintel --name posthog --secret-env POSTHOG_KEY

# A Google service account: the key file's JSON text, plus 1-20 scope URLs
rip credential create --team quintel --name google --kind google_service_account \
  --key-file ./service-account.json \
  --scope https://www.googleapis.com/auth/analytics.readonly \
  --scope https://www.googleapis.com/auth/webmasters.readonly

rip credential list --team quintel           # each credential and the connections using it
rip credential get posthog --team quintel    # by name in its team, or by id alone: rip credential get <id>

# Replace the key: every connection using it sends the new one from its next call
rip credential rotate posthog --team quintel --secret-env POSTHOG_KEY
rip credential rotate <id> --key-file ./new-key.json

# Rename, or change a Google credential's scopes (--scope replaces the list)
rip credential update posthog --team quintel --name posthog-prod

# Only named team members may call through it (an empty list refuses everyone, the team owner included)
rip credential update posthog-prod --team quintel --restrict --user simon --user alek
rip credential update <id> --unrestrict

# Delete: refused (CREDENTIAL_IN_USE) while any connection, disabled ones included, uses it
rip credential rm <id>
```

- **The key is write-only.** Give it with exactly one of `--secret <value>` (avoid; it lands in shell history), `--secret-env <VAR>` (preferred), `--secret-stdin` (piped from a secret manager) or `--key-file <path>` (the file's text, verbatim). No read ever returns it.
- **Kinds:** `secret` (default) is sent as is. `google_service_account` holds a Google key file and its scopes; the server trades it for short-lived tokens itself. Its connections must use `bearer` and an `https` base URL on `googleapis.com` (for example `https://analyticsdata.googleapis.com` or `https://searchconsole.googleapis.com`), so a Google token only goes to Google. Rotating does not revoke the old key at Google: delete it in Google Cloud.
- **Names** are lowercase and unique per owner. Commands take the credential's **id** alone (from `list`; a team's too, no `--team` needed) or its **name**: with `--team <slug>` for a team's, without for your personal one. `--team` beside an id is refused (`INVALID_FIELD`). `rip connection create --credential` takes either, under the new connection's owner.
- **Named users** apply to team credentials only. `--user` takes an account alias or id, each a current member; it replaces the list and needs the credential to be restricted after the update. `--unrestrict` clears the list. A member who leaves the team is dropped from every list.

## Connections

```bash
# Attach an existing credential (authType defaults to bearer)
rip connection create --team quintel --name ga4 --credential google \
  --base-url https://analyticsdata.googleapis.com \
  --allowed-paths 'POST /v1beta/properties/*:runReport'

# Or create the key inline: it becomes a credential named after the connection
export OPENAI_KEY=sk-...
rip connection create --name openai \
  --base-url https://api.openai.com --auth-type bearer \
  --secret-env OPENAI_KEY --allowed-paths 'GET /v1/models,POST /v1/chat/completions'

# Team-owned, custom auth header, static default header
export MINIMAX_KEY=sk-...
rip connection create --team quintel --name minimax \
  --base-url https://api.minimax.io/anthropic --auth-type header \
  --auth-header-name x-api-key --secret-env MINIMAX_KEY \
  --allowed-paths 'POST /v1/messages' --header anthropic-version=2023-06-01

# List / inspect (keys never shown; each shows its credential, its rules and "can call")
rip connection list
rip connection list --team quintel --include-disabled
rip connection get minimax --team quintel    # by name in its team, or by id alone: rip connection get <id>

# Disable (soft — frees the connection's name; it keeps its credential) or delete (hard; the credential stays)
rip connection disable <id>
rip connection rm minimax --team quintel
```

A connection is named the same way as a credential: its id alone, or its name (with `--team <slug>` for a team's). To replace a key, rotate its credential: `rip credential rotate <credential>`; every connection using it sends the new key.

### Create flags

| Flag | Meaning |
|---|---|
| `--name <name>` | Connection name, unique per owner. This is the handle `call` targets. |
| `--base-url <url>` | Upstream API origin (SSRF-checked; private/loopback addresses are rejected). Calls stay under its path. |
| `--credential <name\|id>` | Use an existing credential of the same owner (needs its management right). Without it, give `--auth-type` and a secret flag. |
| `--auth-type <type>` | `bearer` (Authorization: Bearer), `header` (custom header — needs `--auth-header-name`) or `basic`. Required without `--credential`; defaults to `bearer` with it. |
| `--auth-header-name <name>` | Header the key is injected into when `--auth-type header` (e.g. `x-api-key`). |
| `--secret`, `--secret-env`, `--secret-stdin` | Without `--credential`: the key, kept as a new credential named after the connection (409 `CREDENTIAL_NAME_TAKEN` if that name exists: attach it with `--credential` instead). |
| `--allowed-paths <csv>` | Comma-separated rules (below). Omit to allow any method and path. |
| `--header k=v` | Static **default header**, always sent (repeatable). This is how required provider statics like `anthropic-version` reach upstream — they bypass the caller header allowlist. Must not name the auth header. |
| `--query k=v` | Static **default query** param, always sent (repeatable). |
| `--rate-limit-per-min <n>` | Per-minute call cap (default 60). |
| `--daily-quota <n>` | 24h call cap (default 1000). |
| `--team <slug>` | Make it team-owned (member-invokable; creator or team owner manages it). |

### Rules (`--allowed-paths`)

Each rule is `[METHOD[|METHOD…] ]/path`: optional methods from `GET POST PUT PATCH DELETE` joined by `|`, one space, then a pattern starting with `/`. No method means any method.

- `*` matches within one path segment (never `/`); `**` matches any run, `/` included. Every other character is literal.
- Rules judge the path as sent, minus the base URL's path, still percent-encoded and without the query: write them as sent (`/webmasters/v3/sites/*/searchAnalytics/query` matches `…/sites/https%3A%2F%2Ftokenrip.com%2F/…`).
- A call passes when any rule allows it; otherwise `403 PATH_NOT_ALLOWED`. A path with `.` or `..` segments (encoded or not), a backslash, or bad percent-encoding is refused with `400 PATH_NOT_CANONICAL` and nothing is sent.
- Examples: `POST /v1/messages`, `GET|POST /api/**`, `POST /v1beta/properties/*:runReport`.

There is no CLI update for non-secret connection fields — disable + recreate, or use the REST `PATCH /v0/connections/:connection` documented in `docs/architecture/connections.md`.

## `rip connection call` — invoking an upstream

Call one of your own personal connections, or a team connection of a team you currently belong to, by name, or any of them by its id alone. The call goes straight to the connection; nothing else needs to be set up first. Auth and default headers/query are injected server-side; you provide the method, path, and body. Every call is audited with the calling account (metadata only, never bodies).

```bash
# Team connection (you must be a current member of the team)
rip connection call --team <slug> --connection <name> \
  --method <M> --path <path> [--body <json>] [--query <json>] [--header k=v]

# Personal connection (you own it)
rip connection call --connection <name> --method <M> --path <path>
```

| Flag | Meaning |
|---|---|
| `--team <slug>` | Call the team's connection by name. A non-member, or a member not named on a restricted credential, gets `403 CONNECTION_FORBIDDEN`. Omit for a personal connection or an id. |
| `--connection <id\|name>` | The connection's id, or its name. A missing or disabled one, or an id you cannot reach, is `404 CONNECTION_NOT_FOUND`. |
| `--method <M>` | `GET` / `POST` / `PUT` / `PATCH` / `DELETE`. |
| `--path <path>` | Path under the connection's base URL; the method and path must pass the connection's rules. |
| `--body <json>` | JSON request body (parsed and re-serialized; invalid JSON errors locally). |
| `--query <json>` | JSON object of query params (merged with the connection's `--query` defaults; caller wins on conflict). |
| `--header k=v` | Extra request header (repeatable). Only `Content-Type` / `Accept` / `Accept-Language` / `User-Agent` are forwarded; the connection's defaults and injected auth win. |

### Worked example — MiniMax (Anthropic-compatible)

Using the team `minimax` connection created above (`--auth-header-name x-api-key`, `--header anthropic-version=2023-06-01`, `--allowed-paths 'POST /v1/messages'`):

```bash
rip connection call --team quintel --connection minimax \
  --method POST --path /v1/messages \
  --body '{"model":"MiniMax-M2.5","max_tokens":64,"messages":[{"role":"user","content":"hi"}]}'
```

The x-api-key auth and the `anthropic-version` header are added server-side. **Output in human mode is the bare upstream response** `{ status, headers, body, bodyIsJson, latencyMs }` printed as JSON on stdout — so a skill can `JSON.parse(stdout)` directly. `--json` wraps that same object in the standard `{ ok, data }` envelope. Non-streaming responses only; a 30s timeout and a 5MB response cap apply.

## Operations — named calls, and the tools chat hosts see

An **operation** is one call saved on a connection under a name: a fixed method and path, a described input, and what it changes at the provider. Every agent that may call the connection can run it by name here, and on MCP sees it as its own tool named `<connection>_<operation>` (a team's: `<team>_<connection>_<operation>`, lowercased, `-` as `_`), for example `quintel_posthog_query`. Declaring, changing and removing take the connection's write right (its personal owner, or a team connection's creator or the team owner); any member may list and read them, and run them unless the credential is restricted to named members they are not among. The person can do the same from the connection's Operations section on the dashboard. MCP has no tool to declare one.

```bash
# Declare: POST to PostHog's query endpoint, the agent supplies only the query text
rip connection operation add posthog --team quintel --name query \
  --title 'Query PostHog' --description 'Runs a HogQL query and returns the result rows.' \
  --method POST --path /api/projects/434992/query/ \
  --input-schema '{"type":"object","properties":{"query":{"type":"string"}},"required":["query"]}' \
  --fixed-body '{"query":{"kind":"HogQLQuery"}}' --place query=/query/query --response /results

# An operation that changes something at the provider says so (here: Write)
rip connection operation add minimax-image --team quintel --name generate \
  --title 'Generate an image' --description 'Generates an image from a prompt and returns its URLs.' \
  --method POST --path /v1/image_generation \
  --input-schema '{"type":"object","properties":{"prompt":{"type":"string"}},"required":["prompt"]}' \
  --fixed-body '{"model":"image-01","response_format":"url"}' --response /data/image_urls --kind adds

rip connection operation list posthog --team quintel          # each with its toolName and class
rip connection operation get posthog query --team quintel
rip connection operation update posthog query --team quintel --title 'Query PostHog with HogQL'
rip connection operation update minimax-image generate --team quintel --title 'Generate an image from a prompt'   # still a Write: its --kind adds is kept
rip connection operation rm posthog query --team quintel      # the tool leaves every agent's list
```

| Flag (`add`; all optional on `update`) | Meaning |
|---|---|
| `--name <name>` | Lowercase letters, digits and `_`, starting with a letter, at most 40; unique on the connection |
| `--title`, `--description` | What hosts show in approval prompts (≤ 60 characters) and what the call does and returns (≤ 1,000) |
| `--method`, `--path` | Fixed, under the base URL, and inside the connection's rules (`INVALID_OPERATION` `outside_rules` otherwise). A fixed query string is allowed; no path placeholders |
| `--input-schema <json>` / `--input-schema-file <path>` | A JSON Schema object: fields of type `string`, `number`, `integer`, `boolean`, `array`, `object`, with `description`, `enum` and bounds; no `pattern`. At most 32 fields at the root and 4 levels below. Every object refuses unknown keys. A field whose name says it holds a secret (`api_key`, `token`, `password`, `secret`, `session`, `code`, `otp` and the like) is refused; `why` is reserved |
| `--fixed-body <json>` | POST/PUT/PATCH: the body the inputs are placed into (≤ 16 KiB stored, as the schema) |
| `--place <field=/pointer>` | Repeatable: where an input goes in the body; a field without one goes to the top level under its own name. GET and DELETE send inputs as query parameters instead |
| `--response </pointer>` | The part of the provider's JSON answer to return; the whole answer by default |
| `--kind <kind>` | Repeatable: `adds`, `modifies`, `destroys`, `widens`, `publishes`, `sends`. None means it only reads |
| `--no-fixed-body`, `--no-place`, `--no-response`, `--no-kind` | `update` only: clear that part. `--no-kind` makes it a read, so use it only when the call truly changes nothing at the provider; an update that keeps the same call keeps its kinds |

**The class follows from the kinds**, and hosts use it to decide when to ask the person: none is **Read**; `adds`, `modifies` or `publishes` is **Write** (a change at the outside service); `destroys`, `widens` or `sends` is **Sensitive** (cannot be undone; hosts ask every time). The kinds are the declarer's honest statement: declare what the call does at the provider. Spending money is not a kind.

**Run one by name:**

```bash
rip connection run posthog query --team quintel --input '{"query":"select count() from events"}'
rip connection run minimax-image generate --team quintel --input-file ./prompt.json
```

The input is checked against the schema first (`400 INVALID_FIELD` on `input.<field>`, nothing sent), then the call goes through the connection's rules, limits and key injection like any other. Human mode prints the bare `{ status, body }` as JSON (`status` the provider's, inside a 200; `body` the part `--response` selects); `--json` wraps it in `{ ok, data }`. REST: `POST /v0/connections/:connection/operations/:operation/call` `{ team?, input? }`. Up to 5 MB; nothing from the answer is stored, and the audit names the operation.

**On MCP.** A host sees a new, changed or removed operation on its next tool list (a reconnect, a refresh of the connector's tools or a new conversation, by host); Tokenrip sends no notice. A tool answers `{ status, body }` within about 31 KiB (larger is `RESPONSE_TOO_LARGE`: narrow the query or the response pointer); a provider error is `UPSTREAM_STATUS` with the status and the start of its answer. A writing operation also takes `why`. Agents without the `connections:execute` scope, or not named on a restricted credential, see none of these tools, and a disabled connection's operations are hidden.

**Keeping them callable.** Changing the connection's base URL or rules so an operation falls outside them, renaming it so a tool name breaks, or giving it a default query key that a GET or DELETE operation's input already uses, is refused with `409 OPERATIONS_WOULD_BREAK` naming the operations: change or remove them first. Refusals on declare: `400 INVALID_OPERATION` with a `reason` (and `field`), `409 OPERATION_NAME_TAKEN` (on the connection, or the tool name among the owner's operations), `404 OPERATION_NOT_FOUND`.

## Related

- Concept + safety model (proxy safeguards, SSRF, failure codes, REST endpoints): `docs/architecture/connections.md`
- MiniMax / Anthropic / generic provider configs: the "verified provider configs" table in `docs/architecture/connections.md`
