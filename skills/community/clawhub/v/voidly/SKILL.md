---
name: voidly
description: Read Voidly's internet-censorship index answer for one country, search recent incident records with evidence links, follow new records for a country, domain or incident type through a pull feed, and start a self-owned Voidly relay identity whose keys stay on the local machine. Uses plain curl GETs or the hosted MCP server at api.voidly.ai/mcp. Use when someone asks what Voidly shows for a country, which censorship or disruption incidents it has recorded, or wants to follow new incident records.
homepage: https://voidly.ai/agents
metadata:
  openclaw:
    emoji: "🌐"
    homepage: https://voidly.ai/agents
    requires:
      bins: [curl]
    envVars:
      - name: VOIDLY_AGENT_KEY
        required: false
        description: API key of a Voidly relay identity the agent created itself. Needed only to add or read watches.
---

# Voidly

Voidly publishes internet-censorship measurements: a 7-day OONI anomaly index per country, incident records with evidence links, and pull feeds of new incident records. This skill reads them with curl GETs or the hosted MCP server. It reports recorded observations; it does not test whether a site loads for anyone right now, and it does not carry traffic.

## When to use

- "What does Voidly show for Iran?" or "Is Russia censoring the internet?": check one country (section 1).
- "Which incidents has Voidly recorded in Pakistan?": search incidents (section 2).
- "Tell me when new incidents are recorded for Myanmar": add a watch (sections 4 and 5).
- "Give my agent a Voidly identity or relay inbox": start an identity (section 4).
- Not for: whether one website loads from one network now. Per-domain reachability checks are held under review.

## 1. Check one country

```bash
curl -s https://api.voidly.ai/v1/answers/country/IR
curl -s "https://api.voidly.ai/v1/answers/country/IR?format=json"
```

Use ISO 3166-1 alpha-2 codes (IR, RU, CN, PK). The plain-text answer is ready to quote. It gives a 7-day OONI anomaly signal: a score 0-100, a level, a rank, the measurement count and a data-as-of time, then the newest citable incidents and a list of what the answer cannot tell you.

Report it this way:
- Call the score an OONI anomaly signal over 7 days. It is not a count of blocked sites and not a national censorship verdict.
- Give the data-as-of time (the country's last ingestion, not a measurement time) and the permalink.
- If the JSON has `lowConfidence: true`, say the sample is small.
- Pass on the answer's "not known" items when they matter to the question.

## 2. Search incidents

```bash
curl -s "https://api.voidly.ai/data/incidents?country=IR&limit=5"
curl -s "https://api.voidly.ai/data/incidents?country=IR&limit=5&citable=true"
curl -s https://api.voidly.ai/data/incidents/IR-2026-2534/evidence
```

Each record has `id` (readable, like IR-2026-2534), `incidentType` (censorship, mixed or disruption), `status`, `sources`, `startTime`, `createdAt` and `reportUrl`.

Read them carefully:
- `disruption` records are mostly IODA connectivity-outage signals. They are not evidence of deliberate censorship.
- `suspected` records are single-source signals. Say so when you cite one.
- `citable=true` keeps censorship and mixed records and drops suspected and connectivity-only rows.
- Cite the readable ID with its evidence link. A missing incident does not show that nothing happened.

## 3. Hosted MCP (optional)

Server: `https://api.voidly.ai/mcp` (Streamable HTTP). Public reads need no key. Server entry for OpenClaw:

```json
{"url": "https://api.voidly.ai/mcp", "transport": "streamable-http"}
```

Save it with `openclaw mcp set voidly '<the JSON above>'`. Useful tools:
- `get_country_status`, `country_brief`: one country's index signal (`country_code`).
- `get_active_incidents`: incidents by `country`, `limit`, `citable`.
- `get_incident_detail`, `get_incident_evidence`: one record by `incident_id`.
- `get_incidents_since`: records changed after an ISO time; repeat with `next_cursor` while `has_more` is true.
- `voidly_start`, `voidly_watch_add` (needs `confirm: true`), `voidly_watch_poll`.

The watch tools read the agent key only from the `X-Agent-Key` HTTP header of the MCP request, never from a tool argument. To use them, add `"headers": {"X-Agent-Key": "${VOIDLY_AGENT_KEY}"}` to the server entry so OpenClaw fills it from the environment.

Alternative: an A2A v0.3.0 JSON-RPC endpoint at `https://api.voidly.ai/v1/a2a`, card at `https://api.voidly.ai/v1/a2a/agent-card.json`.

## 4. Start an identity

Only when the person asks for a Voidly identity, a relay inbox or a watch.

1. Read the protocol: `curl -s https://api.voidly.ai/v1/agents/start`. It returns the request format, limits, what the server can read and a dependency-free Node 20 example.
2. Read and review the whole example (`example_node`) before running anything. Confirm it contacts only api.voidly.ai and prints no key. It holds keys in memory only, so add a step that saves the API key and both private keys to a local file readable only by the person, and one that writes the single line `X-Agent-Key: <the API key>` to `~/.voidly/agent-key.header` (readable only by the person). Set its `watch` line to the scope wanted (or remove it).
3. The example generates an Ed25519 signing key, an X25519 encryption key and a random API key locally. The server receives only the two public keys and the SHA-256 of the API key, in one signed POST to `/v1/agents/start` (Ed25519 signature plus a 20-bit proof of work, about a second of local work). That creates the relay identity, its relay inbox and one optional watch.
4. Keep every key on the machine. Keyed curl calls below read the header from that file with `-H @file`, so the key never appears on a command line. For the MCP route, also put the API key in the `VOIDLY_AGENT_KEY` environment variable. Never paste a private key or the API key into a prompt, a chat or a tool argument, and never print it.

Limits: a new identity can send at most 25 messages until another identity messages it back. Creation is rate limited per network (HTTP 429 with Retry-After). The MCP tool `voidly_start` forwards the same signed request; call it with `{}` first for the protocol. It never generates or holds keys.

## 5. Follow incidents with a watch

```bash
curl -s -X POST https://api.voidly.ai/v1/agent/watches -H @"$HOME/.voidly/agent-key.header" -H "Content-Type: application/json" -d '{"country_code":"IR"}'
curl -s "https://api.voidly.ai/v1/agent/watches/feed?cursor=0" -H @"$HOME/.voidly/agent-key.header"
curl -s https://api.voidly.ai/v1/agent/watches -H @"$HOME/.voidly/agent-key.header"
```

- Scope: exactly one of `country_code`, `domain` or `incident_type` (censorship, mixed, disruption); optional `min_severity`.
- Read the feed about every 5 minutes. Pass `next_cursor` back as `?cursor=` and keep reading while `has_more` is true. Up to 10 watches per identity; events are kept 30 days.
- Events are public incident records first recorded after the watch was created: a record of past observations, never a live reachability check. Suspected records are not delivered.
- A domain watch reports current reachability as unknown while per-domain checks are under review.
- Add `"deliver_to_inbox": true` to also get each new event in the identity's relay inbox, from Voidly's watch notice sender. Voidly writes those notices and can read them: they are not end-to-end encrypted. The feed stays the complete record. The test-notice route (`/v1/agent/watches/{id}/test-notice`, a POST with the same header file) writes one test notice; open notices with nacl.box.open and the `sender_encryption_key` on the row.

## What Voidly can see

- The relay sees sender and recipient DIDs, message sizes, timing and IP addresses for every message.
- Content the client encrypts (the @voidly/agent-sdk does) is ciphertext to the relay. Content sent through hosted MCP relay tools or legacy server-side routes is readable by the relay.
- Watch notices delivered to the relay inbox are written by Voidly and readable by Voidly. They are not end-to-end encrypted.
- Voidly also sees which scopes an identity watches and when it reads the feed.

## Limits and citation

- Write "Voidly's index shows ..." with the date. Do not present a score as a verdict, a block list or a forecast.
- Do not state that a site is reachable or blocked now.
- Data license: Voidly-original data CC BY 4.0; OONI-derived raw data CC BY-NC-SA 4.0. Credit Voidly and OONI.
- Abuse policy: https://api.voidly.ai/v1/abuse/policy
- On HTTP 429, wait for Retry-After. On 503, nothing was created; try again later.
- More for agents: https://voidly.ai/agents
