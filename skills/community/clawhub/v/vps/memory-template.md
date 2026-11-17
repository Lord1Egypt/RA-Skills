# Working File Templates — VPS

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — Configuration table keys and preference areas alike | `~/Clawic/data/vps/config.yaml` | Key by key, read-modify-write |
| Current fleet summary, provider accounts, exposure, spend, due dates, box index | `~/Clawic/data/vps/memory.md` | Rewritten in place; stays small |
| Hosts and machines themselves | `~/Clawic/data/servers/servers.md` (**shared**) | One row per host, every provider in one inventory |
| VPS-only attributes of a host that `servers.md` has no column for — image, snapshot policy, private-network membership, what it serves, PTR | `## Hosts` in `memory.md`; `~/Clawic/data/vps/hosts.md` after the split | One row per host, keyed by the same `Name` |
| Provider accounts: login owner, billing, API-token pointer, support tier | `## Provider Accounts` in `memory.md` while there is one; `~/Clawic/data/vps/provider-accounts.md` from the second | One row per account |
| Which ports are open on which host and why | `## Exposure` in `memory.md`; `~/Clawic/data/vps/exposure.md` after the split | One row per open port |
| Domains pointing at a host: registrar, expiry, target | `~/Clawic/data/domains/domains.md` (**shared**) | One row per domain |
| What this infrastructure costs per month, as a subscription line | `~/Clawic/data/finances/subscriptions.md` (**shared**) | One row per provider account, never per host |
| Things you produced that get re-read — recovery runbooks, cutover plans, provider-choice decisions, hardening baselines, incident write-ups | `~/Clawic/data/vps/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| Things that happened to a host — created, rebuilt, resized, restored, migrated, destroyed; and timed restore drills | `~/Clawic/data/vps/changes/<year>.md` | Append-only, cut by year |
| **Anything durable this table does not name** | `~/Clawic/data/vps/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials of any kind | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| A host was created, rebuilt, discovered, or destroyed | Its row in `servers.md`, its VPS attributes in `## Hosts`, and the event in `changes/<year>.md` |
| A host was resized, or its disk grew | The row in `servers.md` (type, monthly), `## Hosts`, and `changes/<year>.md` — disk growth is irreversible and belongs in the log |
| A port was opened or closed, or an exposure sweep ran | `## Exposure` |
| A provider account was added, or its billing or owner named | The provider accounts table, plus its row in `~/Clawic/data/finances/subscriptions.md` |
| A domain was pointed at a host, or its TTL changed for a cutover | `~/Clawic/data/domains/domains.md` |
| A backup policy was set, or a restore was actually timed | `## Due` for the cadence, `changes/<year>.md` for the drill and its measured time |
| A bill was reviewed, or a saving landed | `## Spend` |
| A recovery runbook, cutover plan, incident write-up, or provider decision came out of the session | `artifacts/` |
| The user declared a preference | Its key in `config.yaml` |
| Recurring work was scheduled or run | `## Due` |

## Start flat, split only when it hurts

Everything except artifacts, the change log, and the shared boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings, and comments do not count — then, in the same turn: create the new file in `~/Clawic/data/vps/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, so the split is a copy-paste and never a rewrite.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

Artifacts are the exception: a runbook or a decision is born as its own file whatever its size, because it is read whole and only when its subject comes up.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. A pasted runbook, `.env`, or terminal log is the densest source of secrets in this domain: replace each value **before** writing, and say in one line that you did. Store the pointer in place of the value, in this shape: `<kind>:<locator>`.

`file:~/.ssh/id_ed25519` · `keychain:hetzner-api` · `1password:Infra/vps-root` · `bitwarden:Infra/backup-passphrase` · `env:RESTIC_PASSWORD` · `vault:secret/infra/wireguard` · `profile:prod`

In a document the pointer goes exactly where the value was: `root_password: <1password:Infra/vps-root>`.

In this domain — **not secrets, keep them**: hostnames, IPv4 and IPv6 addresses, provider and region names, datacenter and instance ids, plan names, disk and RAM sizes, SSH port numbers, usernames, **public** keys and their fingerprints, PTR records, domain names, prices and invoice totals. **Secrets, strip them**: SSH private keys and their passphrases, root and user passwords, provider API tokens and their secrets, console/VNC and rescue-mode passwords, backup repository passphrases and repo keys, WireGuard and VPN private keys, database passwords inside a runbook or connection string, SMTP relay credentials, control-panel admin passwords, and 2FA recovery codes.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [shared servers inventory](#shared-servers-inventory) · [shared domains box](#shared-domains-box) · [shared finances box](#shared-finances-box) · [artifacts/](#artifacts) · [changes/](#changes) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/vps/` if it does not exist.

```yaml
provider: hetzner
default_distro: debian
cpu_arch: arm64
monthly_budget: 25
admin_user: ivan
ssh_port: 22
firewall_layer: both
backup_target: object-storage
patch_window: "sunday 03:00"

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
tooling:
  firewall_frontend: ufw
  backup_tool: restic
  provisioning: cloud-init
conventions:
  hostname_scheme: "<role>-<env>-<n>"
  project_root: /srv
isolation_model: docker-compose-per-project
safety_posture:
  destructive_commands: confirm-each
data_residency: EU
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# VPS Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Per-host VPS attributes (18 hosts) → `hosts.md`; read before any change to a specific host
- Open ports and why (22 rows) → `exposure.md`; read before opening a port or auditing exposure
- Rescue procedure for web-prod-1 → `artifacts/runbook-lockout-web-prod-1.md`; read the moment SSH refuses on that host
- Provider move Contabo → Hetzner → `artifacts/cutover-2026-contabo-hetzner.md`; read before any further migration
- Change log 2026 → `changes/2026.md`; read when "why is this box like this" comes up, or before a restore drill

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| Restore drill (timed) | quarter | 2026-04-14 | 2026-07-14 |
| Reboot for kernel updates | month, Sunday 03:00 | 2026-07-06 | 2026-08-02 |
| Snapshot pruning | month | 2026-07-01 | 2026-08-01 |
| Spend review | quarter | 2026-04-02 | 2026-07-02 |
| Provider-account 2FA and API-token review | year | 2025-11-10 | 2026-11-10 |

## Hosts
| Name | Image | Serves | Snapshot policy | Private net | PTR | Notes |
|------|-------|--------|-----------------|-------------|-----|-------|
| web-prod-1 | debian 13 | 3 sites behind Caddy | daily, keep 7 | 10.0.0.2 | mail.example.com | disk grown to 80 GB 2026-05, cannot shrink |
| build-1 | ubuntu 24.04 | CI runner | none — rebuildable | 10.0.0.3 | — | destroyed nightly |

## Provider Accounts
| Provider | Account / project | Login owner | 2FA | Billing | API token | Support tier |
|----------|-------------------|-------------|-----|---------|-----------|--------------|
| hetzner | infra-main | user | yes | card, monthly | keychain:hetzner-api | standard |

## Exposure
| Host | Port | Service | Open to | Why | Layer |
|------|------|---------|---------|-----|-------|
| web-prod-1 | 443 | caddy | 0.0.0.0/0 | public sites | both |
| web-prod-1 | 22 | sshd | office IP + provider console | admin | provider |
| web-prod-1 | 5432 | postgres | 127.0.0.1 only | app-local | host |

## Spend
### Monthly
| Month | Provider | Actual | As of | Budget | Breakdown | Notes |
|-------|----------|--------|-------|--------|-----------|-------|
| 2026-06 | hetzner | 41 EUR | 2026-06-30 | 25 EUR | 3 servers 28 · snapshots 7 · IPv4 3 · traffic 3 | closed; over budget since build-1 |
| 2026-07 | hetzner | 12 EUR | 2026-07-09 | 25 EUR | servers 9 · snapshots 2 · IPv4 1 | month-to-date |

### Optimization Log
| Date | Change | Monthly saving |
|------|--------|----------------|
| 2026-05-20 | Destroyed two stopped boxes still billing for disk | 9 EUR |

## Pain Points
March 2026: locked out of web-prod-1 for 6 hours, no console access configured. Fallback path is now checked first, always.

## How They Work
Comfortable in a shell, does not want provider-console clicking. Wants the irreversible steps flagged before they are run.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Every recurring thing this skill schedules belongs here, and the restore drill is the one that must never sit overdue quietly.
- **`## Hosts`**: keyed by the same `Name` as `servers.md`, and it carries **only** what that inventory has no column for. If a field exists in both, the shared inventory wins and the copy here is deleted. Delete the row when the host is destroyed, in the same turn as the inventory row.
- **`## Exposure`**: one row per open port, per host, with the reason. `Layer` says where the rule lives (`provider`, `host`, or `both`) — a rule the user believes exists at a layer where it does not is the whole point of this table.
- **`## Spend`**: `As of` is the day the number was read. A row whose `As of` is not the last day of the month is month-to-date and must never be compared against a closed month. Re-checking the current month **overwrites** its row; never a second row for the same month. Amounts always carry their currency. `Breakdown` splits the plan price from the add-ons, because the add-ons are what moves (`costs.md`).
- These headings are exactly the ones the split-out files get, so any split stays a copy-paste.

| Status | Meaning |
|-------|---------|
| `ongoing` | Still learning their fleet and their provider |
| `complete` | Fleet, accounts, and recovery paths all known |

## Shared servers inventory

Lives at `~/Clawic/data/servers/servers.md` and is shared with every other infrastructure skill — the user may have none of them installed, so the format travels with this skill.

```markdown
# Servers

| Name | Provider | Account / Project | Region | Type | Role | Monthly | Access reference |
|------|----------|-------------------|--------|------|------|---------|------------------|
| web-prod-1 | hetzner | infra-main | fsn1 | CAX21 | web + db | 8 EUR | file:~/.ssh/id_ed25519 |
```

- **Identity is `Name` + `Provider`.** Read the file before adding. If that pair is already there, update the row in place — it is yours. Rows whose `Provider` is not one this session touched belong to another source: never edit them.
- **Retirement is part of the inventory.** When a host is destroyed, delete its row, delete its `## Hosts` row, and note the date in `changes/<year>.md`. An inventory that only grows stops being an inventory.
- **Amounts carry their currency in the value** (`8 EUR`), because rows from US providers sit next to yours in USD and someone will add the column up.
- **`Monthly` is a planning estimate, not an invoice.** The provider's billing page is the source of truth; after a spend review, refresh any row whose real cost moved more than ~20%, and put the add-ons in `## Spend`, not in this column.
- **Scale cut**: one row per host while there are ≤15. Past that, one file per host at `~/Clawic/data/servers/<name>.md` with the same fields, and `servers.md` becomes the index (`Name | Provider | Role | → file`). If you arrive and the folder already looks like that, follow it — do not start a parallel `servers.md`.
- **Foreign columns win.** If `servers.md` already exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- `Access reference` is a pointer only — never a key, password, or token.
- If a host belongs to a client, the client goes in `~/Clawic/data/contacts/contacts.md` and is referenced here **by name only**. Never duplicate a person's record inside an infrastructure box.

## Shared domains box

Lives at `~/Clawic/data/domains/domains.md`, shared with the DNS and domain skills. Write here whenever a domain starts or stops pointing at a host, and before a migration, because the TTL sets the cutover window.

```markdown
# Domains

| Domain | Registrar | Expires | DNS host | Points at | TTL | Auto-renew | Notes |
|--------|-----------|---------|----------|-----------|-----|------------|-------|
| example.com | porkbun | 2027-03-14 | cloudflare | web-prod-1 (hetzner) | 300 | yes | TTL lowered 2026-07-24 for cutover |
```

- **Identity is `Domain`.** Read before adding; if the row exists, update in place — never a second row for the same name.
- `Points at` names the host using the same `Name` as `servers.md`, not an IP address: addresses change during a migration and the name does not.
- Only touch `Points at`, `TTL`, and `Notes` for domains this skill moved. Registrar, expiry, and auto-renew belong to whoever manages the registration; if those columns are empty, leave them empty rather than guessing.
- **Scale cut**: a single `domains.md` table holds them all; past ~40 hostnames, group by apex domain into `~/Clawic/data/domains/<apex>.md` with the same fields and leave `domains.md` as the index. If you arrive and the folder already looks like that, follow it — do not start a parallel `domains.md`.
- **Foreign columns win**: match an existing header, add what is missing as a trailing note, never rewrite it.
- Raise the TTL back after a successful cutover and update the row — a permanently low TTL is a permanent extra query cost and someone will wonder why.

## Shared finances box

Lives at `~/Clawic/data/finances/subscriptions.md`, shared with the money and subscription skills. One row **per provider account**, never per host: the per-host breakdown is in `servers.md` and duplicating it here is how two skills start contradicting each other.

```markdown
# Subscriptions

| Service | Category | Amount | Cycle | Next charge | Paid with | Notes |
|---------|----------|--------|-------|-------------|-----------|-------|
| Hetzner (infra-main) | infrastructure | 41 EUR | monthly | 2026-08-01 | card ••4471 | 3 servers + snapshots; breakdown in servers.md |
```

- **Identity is `Service`** including the account name in parentheses — one provider can hold two accounts with separate billing.
- Amounts carry their currency in the value, and estimated amounts carry the date of the estimate in `Notes`.
- Update in place after each spend review. Delete the row when the last server on that account is destroyed and the account is closed — and note the closure in `changes/<year>.md`.
- **Foreign columns win**; match the header that is already there.
- Never record a card number beyond the last four digits, and never a billing portal password.

## artifacts/

One file per thing, at `~/Clawic/data/vps/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **recovery runbook** (how to get back into this specific host), **cutover plan**, **incident write-up**, **provider decision**, **hardening baseline**. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Runbook — locked out of web-prod-1
*Read when: SSH to web-prod-1 refuses or times out. Written 2026-07-26.*

Fallback order: provider console (Hetzner Cloud → Servers → web-prod-1 → Console) →
rescue mode → mount /dev/sda1 → chroot. Root password for rescue: <1password:Infra/vps-root>.
Known cause history: fail2ban banned the office address twice; unban list is at /etc/fail2ban/.
```

```markdown
# Provider decision — Hetzner over DigitalOcean for the app fleet
*Read before adding a server or re-opening the provider question. 2026-07-26.*

Decision: Hetzner CAX (arm64), fsn1.
Why: same RAM for roughly a third of the price, and included traffic covers our egress with headroom.
Rejected: DigitalOcean — better managed add-ons, but the egress allowance made the real bill ~2× ours.
Accepted downsides: EU/US locations only; arm64 forces a compatibility check on every new image.
Revisit when: users outside EU/US exceed a fifth of traffic, or arm64 blocks a dependency we need.
```

If the user tracks this infrastructure as a project, the decision summary also belongs in the shared `~/Clawic/data/projects/<project>.md`, with the full artifact staying here and referenced by name.

## changes/

```markdown
# Changes — 2026

| Date | Host | What changed | Reversible? | Notes |
|------|------|--------------|-------------|-------|
| 2026-05-11 | web-prod-1 | Disk 40 → 80 GB | no | Growth is one-way; monthly went 6 → 8 EUR |
| 2026-06-02 | build-1 | Created, cloud-init v3 | yes | Destroyed and recreated nightly |
| 2026-07-18 | old-vps | Destroyed; address released, 2 snapshots deleted | no | Teardown list completed, billing confirmed stopped |

## Restore Drills
| Date | What was restored | Restored to | Measured RTO | What was missing |
|------|-------------------|-------------|--------------|------------------|
| 2026-04-14 | Nightly restic snapshot of /srv | scratch box, same region | 38 min | Backup passphrase was only in one person's head; now `1password:Infra/backup-passphrase` |
```

The `Reversible?` column exists because disk growth, address release, and snapshot deletion cannot be undone, and six months later nobody remembers which of them happened. The drill table is the only honest source of a recovery-time number.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside `memory.md`.

`hosts.md` — the `## Hosts` table, same columns. Created when the fleet passes ~15 hosts, which is also when `servers.md` hits its own scale cut; do both in the same turn so the two stay keyed alike.

`exposure.md` — the `## Exposure` table, same columns, one `## <host>` heading per host once more than one host has rules worth listing.

`provider-accounts.md` — the provider accounts table, same columns, from the second account onward.

`spend-log.md` — `## Monthly` and `## Optimization Log`. The optimization log is the reason this file exists: without it the same forgotten stopped server gets rediscovered every year and nobody can say what the last cleanup was worth.
