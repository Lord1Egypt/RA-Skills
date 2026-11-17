# Working File Templates — Server

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — table keys and preference areas alike | `~/Clawic/data/server/config.yaml` | Key by key, read-modify-write |
| Stack in use, pain points, how they work, due dates, box index | `~/Clawic/data/server/memory.md` | Rewritten in place; stays small |
| Machines the services run on | `~/Clawic/data/servers/servers.md` (**shared**) | One row per host, every provider in one inventory |
| Hostnames, vhosts, registrar and expiry | `~/Clawic/data/domains/domains.md` (**shared**) | One row per domain |
| Running services: what, where, port, supervisor, vhost | `## Services` in `memory.md`; `~/Clawic/data/server/services.md` past the split threshold | One row per service |
| Measured numbers — worker counts, RSS per worker, req/s, p95, timeout ladder in force | `## Baselines` in `memory.md`; `~/Clawic/data/server/baselines.md` past the threshold | One row per service per measurement date |
| Releases and rollbacks | `~/Clawic/data/server/deploys/<year>.md` | Append-only, cut by year |
| Outages: symptom, real cause, fix, duration | `~/Clawic/data/server/incidents/<year>.md` | Append-only, cut by year |
| Things you produced that get re-read — runbooks, a unit file or vhost that finally worked, topology decisions and diagrams, load-test reports, cutover plans | `~/Clawic/data/server/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| The project this work belongs to, and the decisions it produced | `~/Clawic/data/projects/<project>.md` (**shared**) | One file per project; decisions appended |
| People named in this work — client, teammate, provider contact | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person, identity is the address |
| **Anything durable this table does not name** | `~/Clawic/data/server/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line, with its read condition, in the same turn |
| Credentials of any kind | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| A service was deployed, moved, renamed, or retired | Its row in `## Services` |
| A machine was discovered, provisioned, or decommissioned | Its row in `servers.md` (shared) |
| A hostname was pointed at a service, or a certificate wired | Its row in `domains.md` (shared) + the vhost column of `## Services` |
| Workers, threads, pool size, or a timeout was derived or measured | `## Baselines` |
| A release shipped, or a rollback happened | `deploys/<year>.md` |
| Something was down and the cause was found | `incidents/<year>.md` |
| A runbook, a working unit or vhost, a topology decision, or a load-test report came out of the session | `artifacts/` |
| That decision belongs to a project the user tracks | Its summary in `projects/<project>.md` (shared), pointing at the artifact |
| A client, teammate, or provider contact was named | Their row in `contacts.md` (shared) |
| A recurring check was scheduled or run — renewal, restore drill, upgrade, disk sweep | `## Due` |
| The user declared a preference | Its key in `config.yaml` |

## Start flat, split only when it hurts

Everything except artifacts, deploy records, incident records and the shared boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — then, in the same turn: create the new file in `~/Clawic/data/server/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, so the split is a copy-paste and never a rewrite. `## Services` becomes `services.md` with the same table columns; `## Baselines` becomes `baselines.md` with the same columns.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

Artifacts are the exception: a runbook, a working config, or a decision is born as its own file whatever its size, because it is read whole and only when its subject comes up.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. This matters most for the files nobody planned: a runbook carries the connection string, a "config that finally worked" carries the token, a pasted `.env` is nothing but secrets. Store the pointer in its place, in this shape: `<kind>:<locator>`.

`env:DATABASE_URL` · `file:/etc/myapp/env` · `file:~/.ssh/id_ed25519` · `keychain:deploy-key` · `1password:Infra/prod-db` · `bitwarden:servers/api-token` · `vault:secret/prod/api` · `profile:deploy`

When the user pastes something to save, replace each secret value before writing and leave the pointer visible: `DATABASE_URL=<env:DATABASE_URL>`, `ssl_certificate_key <file:/etc/letsencrypt/live/example.com/privkey.pem>;`. Say in one line that you did it.

In this domain — **not secrets, keep them**: hostnames and domain names, public IP addresses, ports and socket paths, unit and container names, image tags and digests, the user and group a service runs as, config file paths, certificate paths, issuers, fingerprints and expiry dates, upstream addresses, log paths. **Secrets, strip them**: private key material of any kind and its passphrase, `.env` contents, connection strings carrying a password, basic-auth files and password hashes, API and registry tokens, DNS-provider tokens used for ACME challenges, ACME account keys, session and cookie signing secrets, webhook signing secrets, admin panel passwords, SSH private keys and their contents.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [shared servers inventory](#shared-servers-inventory) · [shared domains inventory](#shared-domains-inventory) · [artifacts/](#artifacts) · [shared projects box](#shared-projects-box) · [shared contacts box](#shared-contacts-box) · [deploys/](#deploys) · [incidents/](#incidents) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/server/` if it does not exist.

```yaml
proxy: caddy
process_manager: systemd
os_family: debian
app_root: /srv
tls_issuer: caddy-auto
confirm_restarts: true
maintenance_window: "Sun 02:00-04:00 Europe/Madrid"
health_path: /healthz

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
conventions:
  port_range: "8000-8099 for apps, 9000-9099 for admin UIs"
  release_layout: "/srv/<app>/releases/<sha>, current symlink"
delivery:
  method: rsync-releases
  migrations: before-restart
constraints:
  no_docker_on: [db-1]
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Server Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Services (19) → `services.md`; read before any deploy, port assignment or "what runs here" question
- Baselines (11) → `baselines.md`; read before sizing, tuning or a capacity claim
- Releases 2026 → `deploys/2026.md`; read before a rollback, or when "what changed" is the question
- Outages 2026 → `incidents/2026.md`; read when a symptom looks familiar, and before any post-mortem
- Checkout 502 runbook → `artifacts/runbook-checkout-502.md`; read the moment checkout returns 502
- Proxy topology decision → `artifacts/decision-caddy-over-nginx.md`; read before changing the edge

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| Certificate expiry sweep | month | 2026-07-02 | 2026-08-02 |
| Restore drill from backup | quarter | 2026-05-18 | 2026-08-18 |
| OS and runtime security updates | month | 2026-07-06 | 2026-08-06 |
| Log disk and rotation check | month | 2026-07-06 | 2026-08-06 |

## Stack
Debian 12 · Caddy on the host, TLS auto · apps under /srv, systemd units · Postgres 16 on the same box · backups to object storage nightly.

## Services
| Service | Host | Runtime | Listens | Supervisor | Public vhost | Restart | Data path |
|---------|------|---------|---------|------------|--------------|---------|-----------|
| api | web-1 | node 22 | 127.0.0.1:8000 | systemd api.service | api.example.com | on-failure | — |
| jellyfin | media-1 | container | 127.0.0.1:8096 | compose jellyfin | media.example.com | unless-stopped | /srv/jellyfin |

## Baselines
| Date | Service | Config measured | Result | Saturated by |
|------|---------|-----------------|--------|--------------|
| 2026-07-14 | api | 3 gunicorn workers, pool 8 | 240 req/s, p95 180ms | CPU at 340 req/s |

## Pain Points
May 2026: four-hour outage after a certificate renewed without a proxy reload. Wants expiry checked monthly, not trusted.

## How They Work
One person, one box, no on-call. Prefers a unit file over a container. Wants the reload command with every config change.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Every recurring thing this skill schedules belongs here (`maintenance.md`).
- **`## Services`**: identity is `Service` + `Host`. Update the row in place; a service that moved host keeps one row. When it is retired, delete the row and note the date here — an inventory that only grows stops being one. `Listens` records the interface too (`127.0.0.1:8000` and `0.0.0.0:8000` are different facts, Rule 7).
- **`## Baselines`**: one row per measurement, never overwritten — the point is the comparison. Always record what was measured *with* (worker count, pool size), not only the result, or the number cannot be reproduced. Full load-test output goes to `artifacts/`, and this table keeps the headline.
- These are exactly the headings and columns `services.md` and `baselines.md` get when they split out, so the split stays a copy-paste.

| Status | Meaning |
|-------|---------|
| `ongoing` | Still learning their stack and boxes |
| `complete` | Know every service, host, and how they deploy |

## Shared servers inventory

Lives at `~/Clawic/data/servers/servers.md` and is shared with every other infrastructure skill — the user may not have any of them installed, so the format travels with this skill.

```markdown
# Servers

| Name | Provider | Account / Project | Region | Type | Role | Monthly | Access reference |
|------|----------|-------------------|--------|------|------|---------|------------------|
| web-1 | hetzner | personal | fsn1 | cpx31 | web + proxy | 15 EUR | file:~/.ssh/id_ed25519 |
```

- **Identity is `Name` + `Provider`.** Read the file before adding. If that pair is already there, update the row in place — never append a second one. Rows whose `Provider` is one you did not write are someone else's; never touch them.
- **Retirement is part of the inventory.** When a host is decommissioned, delete its row and note the date in `memory.md`.
- **Amounts carry their currency in the value** (`15 EUR`), because rows from other providers are in other currencies and someone will add the column up. An estimate carries the date it was estimated.
- **Scale cut**: one row per host while there are ≤15. Past that, one file per host at `~/Clawic/data/servers/<name>.md` with the same fields, and `servers.md` becomes the index (`Name | Provider | Role | → file`). If you arrive and the folder already looks like that, follow it — do not start a parallel `servers.md`.
- **Foreign columns win.** If `servers.md` already exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- `Role` is what the box *does* (`web + proxy`, `db`, `media`); the services themselves stay in `## Services` here. Do not duplicate the service list into the host row.
- Access reference is a pointer only. Never a key, token, or password.

## Shared domains inventory

Lives at `~/Clawic/data/domains/domains.md`, shared with the DNS and hosting skills. Write here whenever a hostname starts pointing at a service.

```markdown
# Domains

| Domain | Registrar | Expires | DNS | Points to | Certificate | Notes |
|--------|-----------|---------|-----|-----------|-------------|-------|
| example.com | porkbun | 2027-03-11 | cloudflare | web-1 (api, www) | caddy-auto, renews 30d out | proxied |
```

- **Identity is `Domain`** (the registrable name; subdomains are rows in `Points to`, not new rows). Read before adding; if it exists, update in place.
- Record the **registrar expiry and the certificate expiry separately** — they are different failures with the same symptom, and a domain expiry is the one nobody has a renewal hook for.
- **Retirement**: a domain let go or moved away gets its row deleted and the date noted in `memory.md`.
- **Scale cut**: one table while there are ≤40 hostnames. Past that, group by apex — one `~/Clawic/data/domains/<apex>.md` per registrable name with the same columns, and `domains.md` becomes the index (`Domain | Registrar | Expires | → file`). If you arrive and it is already grouped that way, follow it rather than rebuilding the table.
- **Foreign columns win** — match the header you find, add anything missing as a trailing note.
- Never write a DNS-provider API token here; the token that renews the certificate is a pointer in the service's notes (`env:CF_API_TOKEN`).

## artifacts/

One file per thing, at `~/Clawic/data/server/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **runbook** for a recurring failure, **config that finally worked** (unit file, vhost, compose stack), **topology decision** with its diagram, **load-test report**, **cutover plan**. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Runbook — checkout 502s
*Read when: checkout returns 502. Written 2026-07-26.*

Cause seen three times: app keepAliveTimeout below the proxy's.
1. Confirm from the box: curl the upstream socket directly.
2. ...steps, with every secret replaced by its pointer...
Rollback: flip /srv/api/current to the previous release directory, reload.
```

```markdown
# Working config — api.service
*Read before editing api.service or moving the app to another host. 2026-07-26.*

Why these values: LimitNOFILE raised because the default 1024 capped concurrent
connections at ~500; Type=notify because ordered units started too early with simple.
...the unit, with Environment values as pointers, never literals...
```

Two things inside an artifact belong to other boxes: the project it is part of, and the people named in it. Write them there, keep only the name here — a person or a project described in two places is how two skills end up contradicting each other. Protocols below.

## Shared projects box

Lives at `~/Clawic/data/projects/<project>.md`, shared with the planning and product skills. Write here when the user tracks this work as a project and a decision came out of the session: the summary and its consequence go there, the diagram and the full reasoning stay in `artifacts/` and are referenced by file name.

```markdown
# Migration to Caddy

## Decisions
- 2026-07-26 — Caddy over nginx at the edge: automatic TLS removes the renewal hook that caused the May outage. Detail: `~/Clawic/data/server/artifacts/decision-caddy-over-nginx.md`.
```

- **Identity is the file name**, kebab-cased from the project name — one file per project from the first one, never a table and never a second file for the same project. Read the folder before creating: a near-match (`web-migration.md` vs `migration.md`) is the same project.
- **If the file exists, append under the heading you find** (`## Decisions`, `## Log`, whatever it uses) and never rewrite its structure. Only if it has no such heading do you add one.
- **No scale cut**: files accumulate, one per project. A finished project keeps its file with the outcome noted, and is never deleted — the decision is why the box exists.
- Only the summary and the pointer, never the artifact's content copied over.

## Shared contacts box

Lives at `~/Clawic/data/contacts/contacts.md`, shared with the people and client skills. Write here when a client, teammate or provider contact is named as part of this work — who to reach when the box breaks is operational data.

```markdown
# Contacts

| Name | Email or handle | Role | Preferred channel | Context |
|------|-----------------|------|-------------------|---------|
| Marta Ruiz | marta@acme.example | client, acme | email | Owns the acme.example DNS zone; approves maintenance windows |
```

- **Identity is the email or handle**, not the name — two people share a name, nobody shares an address. Read the file before adding; if the identity is there, update the row in place and never append a second one.
- **Rows you did not write are someone else's**: add to the `Context` cell, never rewrite another skill's row, and never delete it.
- **Retirement**: when the relationship ends, delete the row you own and note the date in `~/Clawic/data/server/memory.md`.
- **Scale cut**: one table while there are ≤15 people. Past that, one file per person at `~/Clawic/data/contacts/<name-slug>.md` with the same fields, and `contacts.md` becomes the index (`Name | Role | → file`). If you arrive and it already looks like that, follow it.
- **Foreign columns win** — match the header you find and add anything missing as a trailing note.
- Keep `Context` operational — what they own, what they approve, which maintenance window they accept. Access a person holds is a pointer in `## Services`, never a value here.

## deploys/

```markdown
# Deploys — 2026

| Date | Service | Version / commit | Migration | Rollback target | Result |
|------|---------|------------------|-----------|-----------------|--------|
| 2026-07-24 | api | a41b7e | 2 up, expand-only | releases/9f2c1d | ok |
| 2026-07-25 | api | 7c02bb | none | releases/a41b7e | rolled back, 11 min |
```

`Rollback target` is the release directory or image digest that was actually there before — the reason this file exists is that at 3am nobody remembers it.

## incidents/

```markdown
# Incidents — 2026

| Date | Service | Symptom | Real cause | Fix | Down for |
|------|---------|---------|------------|-----|----------|
| 2026-05-03 | www | Browser cert warning | Renewal ran, proxy never reloaded | Deploy hook + monthly expiry check | 4h10m |
```

Write the *real* cause, not the first hypothesis. Two entries with the same real cause mean the fix belongs in `artifacts/` as a runbook, and the recurring check belongs in `## Due`.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings and columns it had inside `memory.md`.

`services.md` — the `## Services` table, one `## <host>` heading per host once more than one machine is in play.

`baselines.md` — the `## Baselines` table. It exists so that "it used to handle more" is a claim someone can check.
