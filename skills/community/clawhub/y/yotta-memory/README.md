<p align="center"><b>Language</b>: English · <a href="./README.zh-CN.md">中文</a></p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-memory banner" width="100%" />
</p>

<h1 align="center">元忆 (Yuanyi / yotta-memory)</h1>

<p align="center">Boundary-aware, file-based memory for AI agents: let any agent live across sessions instead of a single conversation.</p>
<p align="center">Start work with <code>recall</code> to restore context, <code>remember</code> important facts as you go, and archive at wrap-up; memories are Markdown files in the user's own directory — <b>readable, editable, auditable, rollback-able</b>, zero-dependency and ready to use.</p>
<p align="center">FACT is shared, PREF / BOUND / COMMIT are privately isolated — <b>who may read what is decided by mechanism, not by AI self-discipline</b>; one memory store can be shared across agents, travels with the disk, and can be shared over LAN.</p>
<p align="center">"Grows smarter the more you use it" (v0.14.0): <code>context</code> builds a one-shot start-of-work package with long-term summaries first (reusing <code>consolidate</code>) + a zero-inference <code>profile</code> + a time-ordered recent corridor + high-value backfill + boundaries + commitments + a session loop contract, turning memory from "storage" into "a memory system that grows".</p>
<p align="center"><b>Mechanism-level encryption for the private zone</b>: AES-256-GCM envelope encryption + passphrase-derived master key + recovery key; <code>yotta-memory view</code> is a user-facing review platform (unlock with passphrase to see all AI memory); <code>migrate</code> converts plaintext → encrypted; <code>--no-encrypt</code> can downgrade. Cross-agent privacy upgrades from "discipline-level isolation" to "mechanism-level unreadable".</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-memory"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-memory" /></a>
  <a href="https://github.com/YottaMeta/yotta-memory"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-memory" /></a>
  <a href="https://github.com/YottaMeta/yotta-memory/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-memory" /></a>
  <a href="https://github.com/YottaMeta/yotta-memory"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
</p>

## Usage cases

**1. Stop losing context between sessions.** At the start of work the agent runs `yotta-memory context` and gets one package: identity, long-term summaries, a recent corridor, boundaries and commitments. There is no need to re-explain the project every session.

**2. Remember a decision the moment it is made.** When the user says "remember this", the agent runs `yotta-memory remember <type> <subject> <statement> --verify` and reads the entry back. Fact types go to the shared FACT zone; preference, boundary and commitment entries stay in that agent's own isolated zone.

**3. Wrap up without hand-carrying state.** Before the session ends the agent writes a COMMIT anchor; `maintain` / `consolidate` keep the store small over time, and `context --audit` checks whether anything important was dropped when the host compacted the conversation.

## Docs and release notes

> 📖 The user-facing operations manual lives in [USER_GUIDE.md](USER_GUIDE.md).
> 🆕 **v0.24.0 (structural capacity)**: `backup status` now selects valid manifest times and isolates future-dated anomalies; `index --stats` adds read-only field/byte analysis; index v5 uses gzip year shards while remaining v4-compatible; new writes use `yyyy/mm/dd` buckets with `layout plan/apply/rollback`; `doctor` adds four type-pressure indicators; `scan` supports exact rule + file + line-hash + expiry policies, while `--policy-candidates` only generates candidates.
> 🆕 **v0.24.1 (autostart profile)**: `lan enable` writes a per-user `serve-profile.json`; Windows task XML, Startup fallback, systemd and crontab reference that absolute profile. `serve --profile <file>` pins memoryHome / runtimeHome / configDir and fails closed when paths or the Windows user do not match, preventing S4U / no-profile startup from landing on `C:\Users\Default\.yottamemory` and returning remote MCP 401.
> 🆕 **v0.23.2 (ClawHub storefront)**: the ClawHub listing now ships an English-first bilingual summary and description (a dedicated `clawhub-dist/yotta-memory` publish copy), and the README gained the three usage cases above. Commands, options, output and the memory store format are unchanged.
> 🆕 **v0.18.1 (distillation provenance + absolute dates + consolidation markers + rule-promotion suggestions + write discipline)**: `distill` now emits typed extraction lists (event / lesson / todo / growth / boundary-rule / other) with per-item `[source: file#L<a>-L<b>]` anchors, measured quality metrics and a skipped/boundary list, plus structured `--json`; `consolidate` rewrites relative dates ("yesterday / last week / this month / this year") into absolute dates based on each entry's `created` date and appends a consolidation marker to archived copies (`--undo` strips it); `maintain --rules` prints read-only "repeat pitfalls → promote to a rule" suggestions (default threshold 3, never writes BOUND automatically); the Memory Doctrine gained a 6-level conflict authority order and three write-discipline rules.

> 🆕 **v0.18.0 (hit tracking + capacity water level + consolidate gate + context audit)**: `recall` / `explain` / `feedback --useful` / `context` record local hit metadata (`hit_days`, retained 90 days by default; `hit_queries` stores only an 8-hex query fingerprint, up to 12 slots, never the query text) inside the memory file, so it travels with encryption / backup / export. Disable globally with `config set usage_enabled false` or per call with `--no-usage`; read-only commands and cross-owner private entries never write hits. New read-only `maintain --capacity [--json]` reports water level, 30/90-day activity, LRU/LFU eviction candidates (30-day cooldown; immutable / BOUND / `evergreen` / `pinned` exempt) and promotion suggestions (≥3 hits across ≥3 distinct queries; commands only, nothing is changed automatically). `archive` respects cooldown and evergreen tags, with `--force` to override those two exemptions. `consolidate` now defaults to `--propose` (structured report + `--json`); `--apply` requires an interactive confirmation token, or explicit `--yes` in non-interactive runs, and shows a one-time data-lifecycle notice. `doctor` scale checks gained `scale_info_*` thresholds and per-metric `ok / info / warning` levels (`doctor.ok` still only follows critical issues). New `context --audit [--from <file|->] [--json] [--gate N]` checks whether compressed-away content was persisted, printing missing items and `remember` suggestions without writing anything. `archive --dry-run` now truly previews (no file moves, no snapshot, no audit), a no-candidate run no longer takes a whole-store snapshot, and `archive --json` emits a structured report. On the MCP side this release adds read-only / preview inputs only (`archive.dryRun`, `maintain.capacity`, `context.audit` with inline `auditText`, and a propose-only `consolidate` tool), while `archive --force` and `consolidate --apply / --undo` stay CLI-only. Previous v0.17.4: `rename` removed flat/layered same-sequence collisions (cross-layout fail-closed, destructive guard, audit).
> 🆕 **v0.17.4 (rename)**: `yotta-memory rename <id> <YYYY-MM-DD-NNNN.md>` renames a single memory entry — the minimal fix for flat/layered same-sequence collisions. Identity is type + owner + file name, checked across both layouts; an occupied target or an existing file is refused (fail-closed). Runs through the destructive guard (doctor + independent backup + snapshot), rebuilds the index and writes a `rename` audit entry; `--dry-run` previews with zero writes. CLI only — the MCP tool list is unchanged.
> 🆕 **v0.17.3 (help readability)**: the top-level `--help` no longer repeats a "做什么：" label on every command and option — each entry starts straight with its description, while "什么时候用：" and "注意：" stay as-is. Help text only: commands, arguments and exit codes are unchanged.
> 🆕 **v0.17.2 (owner gate for private maintenance)**: `explain` now refuses entries owned by another agent instead of printing their subject/statement, and `archive` / `maintain` skip private entries the caller does not own (declare your identity with `--agent <id>`; only an explicit user `--unsafe` overrides). Installer hardening: symlinked targets are refused and no whole-directory delete is performed. Previous v0.17.1: a mismatched identity-confirmation ID in `view` now shows an immediate error instead of returning silently; cancel stays silent and the server-side confirmation and destructive-operation gates are unchanged.
> 🆕 **v0.17.0 (scale: year/month layout + doctor scale check + lazy index + bench)**: new entries are written into year/month folders — public `facts/<yyyy>/<mm>/`, private `private/<owner>/<type>/<yyyy>/<mm>/`. Flat files from v0.16 and earlier stay in place and remain readable; nothing is migrated automatically. Archiving keeps the year/month path, so same-named files from different months no longer overwrite each other. `doctor` gained a scale section (entry count / largest directory / index size / index cold start) with thresholds set through `config set scale_warn_entries` / `scale_warn_files_per_dir` / `scale_warn_index_bytes` / `scale_warn_cold_start_ms`; exceeding a threshold warns only and never locks destructive writes. Large stores can read only the shards of a given year: `recall --year <yyyy>` / `context --year <yyyy>` (repeatable; omitting it loads everything exactly as before). New `bench` command: deterministic auto sampling or `--evalset <file>` (evalset v1), reporting Recall@k / MRR / nDCG@k / HitRate with bootstrap 95% CI plus store and evalset fingerprints; `--gate <metric>=<value>` fits CI, and the same store + evalset + parameters always produce the same output. `bench` is read-only: it never rebuilds the index, never touches access counters and never calls an external embedding plugin. Previous v0.16.7: interactive `yotta-memory migrate --recovery-key-out` prompt, `YOTTA_MEMORY_PASS` for automation, and a `view` memory-home fingerprint before reusing a running server.
> 🆕 **v0.17.0 (recovery probe + memory-store scan)**: `doctor --baseline [--against <store>] [--template <file>]` and `backup drill --probe` run six read-only baseline probes (identity / recent / source-only diff / CJK / operation rules / owner scope) against the target store or restored copy. Entry identity keys are layout-independent, so an old flat store migrating into the year/month layout never reports false gaps; missing items are listed and exit non-zero (`doctor` exit 2 / `drill` fails). Probes never hard-code any memory and `--template` only tightens the verdict. New `scan` command: seven classes (malicious instruction / prompt injection / credential leak / data exfiltration / guardrail bypass / behaviour manipulation / privilege escalation), five severities and `file:line` evidence; report-only by default, zero network and zero dependencies. `--gate` exits 1 at or above the given severity; `--quarantine` needs `--yes` or interactive confirmation and backs up each original file byte-for-byte into `.memory-scan/quarantine/` before redacting hit lines, with `--restore` to roll back; credential snippets are always masked.
> 🆕 **v0.16.5 (doctor JSON contract)**: `doctor --json` now exposes stable top-level `schemaVersion`, `encryption`, and `migration_required` fields while preserving the existing `checks` / `warnings` / `identity` structure.
> 🆕 **v0.16.4 (agent-key prompt scope)**: a missing `--agent-key-file` no longer prints a global `stderr` warning for public or maintenance commands. Only real private-data access fails closed, with the missing path, `view` / `key bind`, and `key status` / `key claim` guidance. `whoami --json`, `doctor --json`, and `config get --json` expose structured `identity.mode` / `identity.agentKeyStatus` fields.
> 🆕 **v0.16.2 (first-boot fixes)**: an empty encrypted store can unlock `view` with the recovery key; non-TTY hosts can use `--password-stdin`; recovery keys can be written with `--recovery-key-out <file>`; a missing `--agent-key-file` degrades to unauthenticated public-only mode; an empty plaintext store can be migrated to encryption; `view` reports port reuse/conflicts clearly.
> 🆕 **v0.16.3 (migration quick path)**: convert a plaintext store to encryption with the interactive command
> `yotta-memory migrate --recovery-key-out "%USERPROFILE%\yotta-memory-recovery.key"`.
> Then authorize agents with `yotta-memory view`; `view` and `yotta-memory key bind <id>` are equivalent, followed by `key status` / `key claim`, then `reindex` with `--agent-key-file` and a `recall` verification.
> 🆕 **v0.16.0 (identity model + stable runtime)**: identity is no longer read from environment variables. HTTP / remote MCP uses request headers `Authorization` + `X-Agent-Id` + `X-Agent-Key`; stdio MCP uses explicit `--agent-id` + `--agent-key-file`; CLI uses `--agent` + `--agent-key` / `--agent-key-file`. The new `runtime install --from-current` / `use` / `rollback` / `status` commands create a stable `<runtimeRoot>/current` launcher so managed MCP, autostart and backup tasks do not pin a version directory. `doctor --runtime` checks CLI / current / MCP config / running server / skill-copy drift, and MCP `serverInfo` returns `runtimePath` / `identityMode` / `toolProfile`.
> 🆕 **v0.15.0 (MCP tool profiles)**: `serve --tools core|full` controls the exposed MCP surface. `core` keeps `context / recall / search / remember` resident; `full` keeps the existing 16 tools for diagnostics and maintenance. Omitting the flag keeps the previous `full` behavior for compatibility.

> 🆕 **v0.14.0 (grows smarter + CLI diagnostics)**: `context` now loads long-term `consolidate` summaries first, samples a time-ordered recent corridor, keeps a deduplicated high-value backfill, and ends with a session loop contract (load at start, `remember --verify` during work, review before wrap-up). Identity, summaries, rules, profile, boundaries, commitments and the contract are not truncated by `--budget`; storage, encryption, owner isolation and permission checks are unchanged. This release also includes the CLI diagnostics work: explicit `--agent` wins over an untrusted ambient `YOTTA_AGENT_ID`; only `YOTTA_MEMORY_TRUST_ENV_AGENT=1` makes an environment identity authoritative. `key status` / `key claim` share one AI_HOME discovery rule (explicit `--to` / `--agent-key-file`, then `YOTTA_MEMORY_AGENT_HOME` / `YOTTA_MEMORY_AGENT_KEY_FILE`, then the Codex / OpenCode / generic host default) and `key status` always prints `checked` + `discovery`. The usage text now documents `remember <type> <subject> <statement>` and `recall [关键词]` directly.

> 🆕 **v0.13.2 (security)**: owner ID is not an authentication credential. Private reads/writes now require an explicit `agent_key`; the user creates it through `yotta-memory view` (or by running `yotta-memory key bind <id>`), then configures MCP with `YOTTA_AGENT_ID` + `YOTTA_MEMORY_AGENT_KEY` + `YOTTA_MEMORY_TRUST_ENV_AGENT=1` (or CLI `--agent <id> --agent-key <key>` / `--agent-key-file <file>`). Authorization also writes a temporary `keys/pending/<id>.key`; a new AI session runs `key status <id>` / `key claim <id>` to store it at `<AI_HOME>/.yotta-memory-agent-key` and delete pending, while the popup key is the user's separate backup. Legacy `keys/cache/*.key` is no longer loaded. When an owner still needs rebinding, `key list` and failed private operations print `[YTM_MIGRATION_REQUIRED]` with the affected agent IDs; the AI relays the steps and the user re-authorizes in `yotta-memory view`, which shows the one-time `agent_key` and refuses to overwrite an existing binding until it is revoked; the old key then fails validation.

> 🆕 **v0.12.2**: reliability closure — `yotta-memory doctor` checks the store, key material, index, identity registry and latest backup; `maintain --apply`, `consolidate --apply`, `merge`, `archive` and `--purge` create a transaction snapshot before writing and refuse to proceed if the snapshot fails.

> 🆕 **v0.12.1**: installation and update docs now distinguish the engine CLI (`yotta-memory`) from the skill installer (`yotta-memory-install`), with copy-ready upgrade commands.

> 🆕 **v0.12.0**: reliability baseline — `init` refuses to overwrite an existing store (`--attach` to attach); `forget` moves entries into `.trash/`; `backup create / list / doctor / restore` provides independent-volume backups with SHA-256 manifests.

> 🆕 **v0.10.0**: compression & forgetting — `consolidate` turns old low-use memories on the same topic into one **provenance-carrying periodic summary** that stays searchable (originals archived; `consolidate --undo <batch>` restores everything); near-duplicate **auto-merge with confidence** (`maintain --dedup --apply`); **per-type decay curves** (FACT slow / PREF medium / COMMIT task-like fast / BOUND never decays); batch audit via `consolidate --batches`.

> 🆕 **v0.9.0**: recall quality + context selection — optional local embedding plugin, `context --focus`, and `--explain` selection trace.

> 🆕 **v0.8.5**: security hardening — MCP `distill` no longer accepts `--model`; MCP `export` / `import` paths are restricted to the memory root; CLI `distill --model` no longer shells out (allowlist-based).

## Core value

Most memory solutions treat "remembering" as a black box: data goes into a database or the cloud, where users can see it but cannot change or audit it, let alone control "which agent sees what". Yuanyi takes a different path — restoring memory to visible, manageable files (public FACT is plaintext and auditable; the private zone is mechanically encrypted and user-unlockable with a passphrase):

- **Memory is files** — each memory is a Markdown file with YAML frontmatter in the user's own directory. Any editor can view / edit / delete; git handles versioning and rollback; team sync and handoff use the same standard toolchain.
- **Isolation is guaranteed by mechanism** — FACT goes to the public zone and is shared; PREF / BOUND / COMMIT go to the private zone, physically split per owner (`private/<owner>/<type>/`). Reads are partitioned by scope/owner; out-of-bound content is intercepted by the CLI and never returned (silently skipped by default; explicit unauthorized cross-read is denied with an error); all reads/writes go through CLI / MCP — direct shell access to library files is forbidden. Permissions are enforced by mechanism, not by AI "self-discipline".
- **Zero dependency, ready to use** — no daemon, no database, no vector store; just Node.js. Install and use; data stays on the machine; deployable anywhere.
- **Grows smarter (v0.14.0)** — `context` generates a one-shot start-of-work package (identity + long-term summaries first + zero-inference profile + time-ordered recent corridor + high-value backfill + boundaries + commitments + session loop contract); long-term summaries reuse `consolidate` output. The SKILL "memory discipline" injects rule layers (type red lines / trigger signals / know the user / bottom lines / host isolation) — rules and mechanisms only, no personality data; zero data out of the box.
- **Self-learning / self-evolving / self-improving (v0.8.0)** — `recall` semantic search (synonyms / pinyin full + initials / field weighting / fuzzy match, zero-dependency) with utility-score blended ranking; `feedback` explicit usage feedback loop (useful / useless adjusts weight / confidence / feedback_net); `maintain` rule-layer self-organization (unified utility score + age-based auto-archive / forget candidates / dedup, dry-run by default, immutable / BOUND exempt); `distill` psychological-log distillation (statistical summary / topic profile / knowledge map, optional `--model` external model enhancement).
- **Compression & forgetting (v0.10.0) — memory that never bloats** — `consolidate` summarizes old, low-use memories on the same topic into one **provenance-carrying periodic summary** that stays in active memory (every original file is listed as provenance; originals move to `.archive/`; `--undo <batch>` restores everything); `maintain --dedup` scores near-duplicates and `--apply` auto-merges high-confidence groups; the utility recency component now decays **per type** (FACT slow / PREF medium / COMMIT task-like fast / BOUND never) so durable facts are not wiped by time and stale commitments step aside quickly; every batch is auditable via `consolidate --batches`.
- **Reliability baseline (v0.12.0 / v0.12.2)** — `init` refuses to overwrite an existing store and `--attach` attaches instead; `forget` moves entries to `.trash/` with an audit record; `backup create / list / doctor / restore` backs up the store to an independent volume with a SHA-256 manifest and restores only to a new directory; `yotta-memory doctor` checks the store, key material, index, identity registry and latest backup, and destructive writes take a transaction snapshot first.
- **Milestone hook declaration** — `skill-manifest.json` declares `after_milestone` / `remember_commit`; a milestone memory write is verified only with a real file-path record.
- **Private-zone encryption (v0.7.0)** — private files AES-256-GCM envelope encrypted (passphrase-derived master key + recovery key + per-owner encrypted index); `yotta-memory view` user review platform (unlock with passphrase to see all AI memory).

### Memory types

Memory is classified into four types; the type decides visibility:

| Type | Meaning | Visibility |
|---|---|---|
| `FACT` | facts / knowledge / experience (verifiable, shareable) | public zone, readable by all agents |
| `PREF` | preferences / habits / likes | private zone, readable only by the owning agent by default |
| `BOUND` | boundaries / rules / bottom lines | private zone, readable only by the owning agent by default |
| `COMMIT` | commitments / anchors / agreements | private zone, readable only by the owning agent by default |

- **Two-level storage**: user-level `~/.yottamemory/` shares personal memory across projects; project-level `.yottamemory/` travels with the project — natural for handoff and team collaboration. recall prefers project-level.
- **Same-key auto-update**: rewriting the same subject + statement only updates `updated`, no duplicates.
- **Rich metadata**: each memory carries `confidence`, `tags`, `immutable`, `created/updated`, `access_count` and more for retrieval and lifecycle management.

### Permissions & isolation

- **Three read states**: public FACT always readable; own private always readable; other agents' private is denied by default (content not returned).
- **Physically isolated directories**: private memory lives at `private/<owner>/<type>/`; different agents' private files are physically separated; legacy flat `prefs/` `bounds/` `commits/` auto-migrate on `reindex`.
- **Three authorization gates** (any one grants reading another's private): 1. explicit grant in `grants.json`; 2. identity=user (`--agent user` / `--owner user`); 3. explicit `--unsafe` (user explicitly authorized). The caller must still present the matching `agent_key`.
- **Silent by default, explicit cross-read errors**: default recall silently skips other agents' private (no "there are N invisible private entries" leak); only explicit cross-agent reads (`--all` / `--owner <other>`) without authorization error / warn.
- **`--agent <other>` does not cross**: it only declares identity for display; reading other agents' private still needs grant / identity=user / `--unsafe`.
- **Isolation positioning**: scope: private guarantees semantic isolation between AIs; since v0.7 the private zone is mechanism-level confidentiality — files are AES-256-GCM envelope encrypted, so an AI without the owner key cannot decrypt them even if it reads the ciphertext; data sovereignty remains with the user, who can use `yotta-memory view` to unlock and view / export any memory file.
- **No direct shell reads/writes**: all memory reads/writes go through CLI / MCP tools; directly reading or editing library files with shell commands bypasses scope/owner boundaries.

### Agent identity (unique ID + self profile)

Each agent has a globally unique agent ID: it is the ownership key for private memory (PREF / BOUND / COMMIT) and the identity declaration for remote access (`X-Agent-Id`).

- **Register (must be unique)**: `yotta-memory iam <id>` writes `agents.json` at the memory root, **enforcing uniqueness** — denied if the ID is already used by another host / source (including remote token registration); `--force` only when you confirm it is the same agent.
- **Confirm identity**: `yotta-memory whoami` (remote MCP tool `agent_info`) reads the "declared identity of this session" — it never guesses or assumes.
- **Self profile (forced to disk)**: `iam` auto-writes a PREF `subject=自我接入档案` (owner=self) with `; `-separated key:value: `agent_id / host / memory_home / mcp_mode / engine_url / token` (token not stored locally). Start work with `recall "自我接入档案"` to recover identity and connection info.
- **No network token locally**: local CLI / stdio bypasses HTTP tokens, but private access still requires `agent_id + agent_key`; stdio MCP passes the key file with `--agent-id` + `--agent-key-file`, never through identity env.
- **Private memory requires an owner**: writing PREF / BOUND / COMMIT without declaring identity is rejected (public FACT is unaffected), mechanically preventing ID spoofing.

### Profile & start-of-work context (v0.6.0 + v0.9.0 + v0.14.0)

- **profile**: aggregates `private/<owner>/` PREF / BOUND / COMMIT verbatim, grouped by type + subject + tags, written to `profile.md`; the engine infers nothing — profile conclusions are formed internally by the AI per the "memory discipline", never pasted as labels.
- **context**: one-shot start-of-work package — multi-agent integration rules + identity + long-term summaries first (`consolidate` output) + user profile digest + optional task-focused memory (`--focus`) + time-ordered recent corridor + deduplicated high-value backfill + boundary reminders + commitments/anchors + session loop contract; supports `--budget` for dynamic memory and `--explain` selection trace. Optional local providers can add `memory.hook` filtering and, when `--budget` is explicit, `context.paging` ordering/paging; `context --json` returns `hook` and `paging` blocks.
- **Memory discipline**: SKILL.md embeds a rule layer (type red lines / proactive trigger capture / know-the-user three stages / psychological grounding & alignment / bottom lines / host isolation / anti-patterns).

### Retrieval: semantic search (v0.8.0 + v0.9.0 embedding)

- `remember` auto-builds the index (version 5 since v0.24.0; logical size > 4 MB or more than 5000 entries uses `index-<year>.json.gz` year shards while remaining v4-compatible; old indexes rebuild on first recall); recall defaults to semantic search — exact (field weighting: subject×3 / tags×2 / statement×1) + synonyms (built-in wordlist, extensible) + pinyin (full / initials, built-in 3755 common characters) + fuzzy (edit distance ≤ 2) + substring fallback, blended with utility score (0.65 × semantic + 0.35 × utility), zero-dependency.
- `recall --explain`: shows each hit's reason (exact / synonym / pinyin / fuzzy + field) and utility components.
- **Candidate pre-filtering (v0.8.1)**: before semantic scoring, index tokens coarsely filter the candidate set (exact / synonym / pinyin / substring / fuzzy length gate) — hit set identical to v0.8.0; the `view` platform paginates by offset, fetching only the current page.
- **Optional embedding plugin (v0.9.0)**: `recall --embedding <command>` or `config set embedding_cmd <command>` runs a local subprocess that accepts JSON on stdin and returns vectors on stdout; results are blended into the same ranking. Failures, timeouts, or malformed output automatically fall back to zero-dependency lexical recall.
- **Embedding cache**: vectors are cached under each memory root at `.embed/cache.json`, keyed by `sha256(command + text)`; only vectors are stored, not plaintext.
- The `tokens` field of `index.json` is a Chinese-tokenization term-frequency table (for TF scoring), **not** an access credential; auth tokens live at `.server/tokens.json`.
- Supports keywords, `--type` filter, `--limit` truncation, project-level priority.
- **Root de-duplication (v0.6.5)**: when project and user roots point at the same directory, recall / context uniquify roots so a file shows once.
- Hits accumulate `access_count` / `last_accessed` for lifecycle management.

### Lifecycle management (v0.8.0 rule-layer self-organization + v0.10.0 compression)

- **Per-type decay (v0.10.0)**: the recency component of the utility score is now `0.5^(days / half-life)` — FACT 730d (slow, facts do not age out), PREF 365d (medium), COMMIT 90d (task-like, fast), BOUND never decays (so boundaries are never auto-archived / forgotten). Tune with `config set maintain_decay_halflife_<TYPE> <days>`.
- `maintain`: unified utility score (confidence + usage + recency + type + structure) × weight; low-utility + over-age auto-archive candidates; extreme low value listed as forget candidates (not deleted by default; `--purge` deletes); `--dedup` now scores duplicates (≥0.85 high confidence auto-mergeable / 0.65–0.85 suggested / below ignored) and `--dedup --apply` auto-merges high-confidence groups of the same type + scope/owner (batch-audited, rollback-able; **`--dedup` is mutually exclusive with archiving** — it never silently archives); `--merge A,B` manual merge. Dry-run preview by default; immutable / BOUND exempt; audit writes `.archive/audit-<date>.jsonl`.
- `consolidate` (v0.10.0): **periodic-summary compression** — groups old (≥180d), idle (≥90d), low-utility (≤0.6) memories on the same topic into one summary entry (tags `consolidate` / `summary`, `source=consolidate`, body carries the full provenance list) that stays searchable, then archives the originals; dry-run by default; `--apply` writes a batch manifest + per-file before/after audit, `consolidate --undo <batch>` rolls the batch back (idempotent), `consolidate --batches` lists recent batches. Public summaries go to `facts/`, private to `private/<owner>/<type>/`.
- `archive`: moves low-value old memory into `.archive/` (public `.archive/facts/`, private `.archive/private/<owner>/<type>/`; immutable / BOUND exempt) by decay-blended utility + age, so the store never grows without bound.
- `feedback`: explicit usage feedback loop — useful → weight ×1.2 (cap 3.0) + confidence +0.05 + feedback_net +1; useless → weight ×0.8 (floor 0.2) + confidence −0.05 + feedback_net −1; `--undo` rolls back; audit writes `.archive/feedback-<date>.jsonl`.
- `distill`: psychological-log distillation — statistical summary (type / age / heat / feedback) + topic profile (clustered by subject) + knowledge map (type → tags); optional `--model <cmd>` external model stdin→stdout refinement (local CLI only; MCP distill does not expose `--model`); output to `private/<owner>/distills/` or `facts/distills/`.
- `explain`: view the utility components (recency shows its half-life), archive / forget / BOUND-exempt status decision of a single memory.
- `forget`: delete a single memory (by type-dir path or file name).
- `reindex`: rebuild the index after manually editing `.md` files.
- `export` / `import`: export the whole store to JSON / import from JSON; an intermediate format for migration and backup.
- git: the whole store can be version-controlled — rollback / audit / team sync.

## FAQ (quick reference)

| Question | Answer (see references/faq.md) |
|---|---|
| Wrong memory type? | Hint only; forget and rewrite; --no-hint to disable |
| Private encryption? | init encrypts by default (master password + recovery key); migrate to encrypt a plaintext store |
| Multi-agent isolation? | FACT public; PREF/BOUND/COMMIT per-owner + per-agent `agent_key`; the user binds once via `view` (or `key bind`) |
| Memory not found? | config get -> reindex -> recall/search |
| Lost master password? | reset-password with recovery key |
| LAN connect? | lan enable + token new; client url+token |
| MCP not loaded? | Check mcpServers + restart; use CLI directly |
| Version mismatch? | Run `yotta-memory doctor --runtime` and apply the repair command for each drift |
| Where is the store? | config get; project-level .yottamemory |
| Cross-session resume? | Run context + recall at session start |
| Backup / migrate? | export / import |

## Comparison with other approaches

> Compared by solution type, not product names. Criteria: data sovereignty, deployment cost, permission boundaries, auditability, cross-agent ability.

| Dimension | Yuanyi (yotta-memory) | Database / embedded storage | Vector store / semantic retrieval | Cloud-hosted memory service |
|---|---|---|---|---|
| Storage form | Public FACT plaintext files; private zone encrypted (.md.enc); git-versionable | binary / structured database files | vector index + model dependency | vendor servers |
| Data sovereignty | fully local, readable/editable/deletable (private zone via view platform) | local, but needs dedicated tools | local or self-hosted; model extra | not in user's hands; TOS-bound |
| Permission boundaries | built-in: public/private zones + scope/owner + grants | usually none, DIY | usually none, DIY | account-level only, no memory-level granularity |
| Audit / rollback | public FACT plaintext auditable; private encrypted but user-decryptable via view; git rollback | needs export toolchain; complex rollback | snapshot/export dependent | platform export dependent |
| Deployment & deps | zero-dependency, runs on Node.js | needs database runtime / embedded dep | vector store + model, heavier | online + account, data leaves local |
| Cross-agent | Agent Skills standard; write once, multiple agents read | per-agent integration, no standard | per-agent integration, costly | platform coverage dependent |

**Conclusion**: Yuanyi's core differentiator is combining "data sovereignty + permission boundaries + zero dependency" — auditable files, mechanism-level read isolation, and no heavy dependencies. For "local-first, multi-agent collaboration, long-term accumulation", it is the lightest path.

## Install

Yotta Memory ships as a **CLI + skill** pair: the `yotta-memory` command reads/writes the memory store, and the skill teaches agents the workflow. Pick any of the four methods below; the order is the recommended priority. Skill files always come from **npm** (GitHub can be slow without a proxy; npm supports mirrors).

### Method 1: npm one-liner (recommended)

```text
# Optional China mirror: npm config set registry https://registry.npmmirror.com
npx -y --package @yottameta/yotta-memory yotta-memory-install --agent <agent-name>      # install the skill to the agent's default user-level dir
npx -y --package @yottameta/yotta-memory yotta-memory-install --dir <your-skills-dir>   # point to the skills dir itself (e.g. ~/.codex/skills)
```

- `--agent <name>` installs to that agent's default user-level directory; `--list` shows each agent's default directory.
- `--dir <path>` installs to the given directory; for agents not in the preset list, point `--dir` at their skills directory.
- If the mirror has not synced the new package (404): add `--registry=https://registry.npmjs.org/` (a proxy may be needed in China), or wait for the mirror cache.
- To read/write memories, also install the CLI: `npm install -g @yottameta/yotta-memory` (see the CLI usage section below).

### Method 2: git clone (developers / git available)

```text
git clone https://github.com/YottaMeta/yotta-memory.git <your-skills-dir>/yotta-memory
```

### Method 3: GitHub Download ZIP (manual / no git)

On the GitHub repository `YottaMeta/yotta-memory`, click **Code → Download ZIP**, unzip it and put the `yotta-memory` folder into the agent's skills directory.

### Method 4: install.sh (multi-agent one-liner script)

```text
bash install.sh --agent <name>   # install to the agent's default user-level directory
bash install.sh --dir <path>     # install to the given directory
bash install.sh --list           # list agents -> default directories
```

### Two commands, two jobs

This package exposes two separate commands:

- `yotta-memory` — the engine CLI that reads and writes the memory store. `npx -y @yottameta/yotta-memory` temporarily runs only this CLI; it does **not** install the skill.
- `yotta-memory-install` — the skill installer. Install or update the skill with `npx -y --package @yottameta/yotta-memory yotta-memory-install --agent <agent-name>` (or `--dir <skills-dir>`).

> Method 1 uses the npm registry (npmmirror / npmjs) and does not depend on GitHub; Methods 2/3 use GitHub and may fail without a proxy in China.
## Example outputs

> Illustrative (actual output may vary by version) so you know what to expect on screen.

**init**:

```text
Memory store initialized: ~/.yottamemory
Master password set; recovery key: xxxx-xxxx-xxxx-xxxx (keep it safe)
```

**remember** (with verify):

```text
Recorded: ~/.yottamemory/facts/2026-09-01-0001.md
[verify] read-back OK: facts/2026-09-01-0001.md
```

**recall**:

```text
3 memories (top 3):
[FACT] subject: statement... (~/.yottamemory/facts/xxx.md)
```

**context**:

```text
# Start-of-work context (yotta-memory context)
## 1. Identity
## 2. User profile summary
## 2.5 Long-term understanding summaries
## 3. Recent corridor (time-ordered)
## 4. Recent high-value backfill
## 5. Boundaries (BOUND)
## 6. Commitments / anchors (COMMIT)
## 7. Session loop contract
```

## Upgrade

Two upgrade paths match the two install paths:

**Upgrade the CLI** (rerun the install command; no version tag defaults to latest):
```bash
npm i -g @yottameta/yotta-memory
```

**Upgrade the skill**: rerun the command that matches the way you installed it:

```text
npx -y --package @yottameta/yotta-memory yotta-memory-install --agent <agent-name>
npx -y --package @yottameta/yotta-memory yotta-memory-install --dir <skills-dir>
bash install.sh --agent <agent-name>
```

If you installed the CLI globally, `npm i -g @yottameta/yotta-memory` updates both the engine and the `yotta-memory-install` command; then run `yotta-memory-install --agent <agent-name>` to refresh the skill.

After updating, verify `yotta-memory --version` and the installed `yotta-memory/SKILL.md` frontmatter `version:`.

> **v0.17.0 upgrade note**: run `yotta-memory reindex` once with the 0.17.0 engine after upgrading. Engines 0.16.7 and earlier do not understand the new year/month layout and will drop layered entries from a rebuilt index. `doctor` now reports flat/layered same-identity duplicates: identical copies are indexed once; conflicting copies stay readable and are listed with both paths, and new writes never reuse an occupied sequence number.

**v0.10.0 upgrade notes** — upgrading touches no data: no migration, no reindex, no re-init needed. v0.10.0 does not change the memory file format, the `facts/` / `private/<owner>/<type>/` layout, or the index version, so existing stores open as-is.

Behavior changes to be aware of:

- Recall / context ranking now decays the recency component **per type** (`0.5^(days / half-life)`: FACT 730d / PREF 365d / COMMIT 90d; BOUND never decays) — durable facts rank slightly higher, stale task-like commitments step aside faster.
- BOUND is now **never auto-archived or auto-forgotten** (previously the code only exempted it from forgetting, not archiving — this release closes the gap).
- `maintain --dedup` is now **mutually exclusive with archiving**: `--dedup [--apply]` only lists / auto-merges duplicates and never silently archives old single memories.
- Archive paths changed for **future operations only**: public → `.archive/facts/`, private → `.archive/private/<owner>/<type>/`; existing `.archive/` files are left in place (not migrated, not re-indexed).
- New commands are additive: `consolidate`, `consolidate --undo <batch>`, `consolidate --batches`.

Optional post-upgrade self-check: `yotta-memory config get` (confirm `memory_home` is unchanged) and `yotta-memory recall <keyword>` still finds old memories. Tune decay with `config set maintain_decay_halflife_<TYPE> <days>`.

> Upgrades only affect commands and skill files — **they never touch your stored memories** (memory is independent of the install, kept in its own directory).

## CLI usage

| Command | What it does |
|---|---|
| `yotta-memory init [--project] [--dir <dir>]` | Initialize the store (default user-level `~/.yottamemory/`; --dir sets an explicit location) |
| `yotta-memory remember <type> <subject> <statement> [--owner <id>] [--source <src>] [--weight <0..>] [--verify] [--no-hint]` | Write a memory (same subject+statement auto-updates; --owner marks ownership; --source records origin; --weight importance, dedup takes max; --verify read-back; --no-hint disables type hints) |
| `yotta-memory recall [keywords] [--type T] [--limit N] [--year <yyyy>] [--agent <id>] [--owner <id>] [--all] [--unsafe] [--explain] [--semantic] [--embedding <cmd>] [--embedding-timeout N]` | Search memory (semantic + utility ranking; optional local embedding plugin; partitioned reads; cross-reading other agents' private is denied by default, needs grant / identity=user / `--unsafe`; project-level priority; since v0.17.0 `--year` reads only the shards of that year, repeatable) |
| `yotta-memory profile [--owner <id>]` | Generate a user profile (aggregates `private/<owner>` verbatim, zero inference, writes `profile.md`; cross-owner denied by default) |
| `yotta-memory context [--limit N] [--owner <id>] [--budget N] [--focus <text>] [--year <yyyy>] [--explain] [--embedding <cmd>]` | Generate the start-of-work package (identity + rules + profile + long-term summaries + task-focused memory + recent corridor + high-value backfill + boundaries + commitments + session loop contract; --budget caps dynamic memory, --focus adds task relevance, --year limits it to given years, --explain shows included/dropped) |
| `yotta-memory forget <file>` | Delete a memory (by type-dir path or file name) |
| `yotta-memory doctor [--json] [--runtime] [--mcp-config <file>] [--skill-dir <dir>] [--baseline [--against <store>] [--template <file>]]` | Start-of-work reliability check (store / key material / index / identity / latest backup; critical issues lock destructive writes); `--runtime` checks CLI / current / MCP config / running server / skill-copy drift; `--baseline` adds the six read-only recovery / migration probes and exits 2 with a missing-item list |
| `yotta-memory archive [--days 180] [--threshold 0.4]` | Archive old memory (decay-blended utility + age; immutable / BOUND exempt; private to `.archive/private/<owner>/<type>/`) |
| `yotta-memory reindex` | Rebuild the index (after manually editing .md) |
| `yotta-memory identity remove <id> [--dry-run] [--yes] [--keep-memories] [--keep-identity] [--password <pass> \| --recovery-key <key>]` | Permanently delete one AI identity and its private memories (v0.17.0): identity registration, owner key, agent binding, pending key, plaintext cache, the whole `private/<id>/` tree, tokens and grant references, then rebuild the index and write an audit record. Public plaintext FACTs are kept and other AIs are untouched. User-only: an encrypted store requires the master password or recovery key, a plaintext store requires an explicit `--agent user`, and the unlocked `view` session counts as the user. Destructive gate = doctor + independent backup + transaction snapshot; `--dry-run` lists the plan only |
| `yotta-memory export [--out f.json]` / `import <f.json>` | Export / import |
| `yotta-memory config set <key> <value>` / `config get` | Store location and engine tuning (`memory_home` / `embedding_cmd` / `embedding_timeout` / `maintain_archived_utility` / `maintain_decay_halflife_<TYPE>` / `consolidate_*`) |
| `yotta-memory whoami` | Show the current agent identity and registration status |
| `yotta-memory iam <id> [--name <name>] [--user <user>] [--relationship <rel>] [--force]` | Register this agent's unique identity and auto-write the self profile (`agents.json`, ID must be unique) |
| `yotta-memory token new --agent <id> [--force]` / `token list` / `token revoke --agent <id>` | Create / list / revoke access tokens for agents (registered at `.server/tokens.json`) |
| `yotta-memory serve [--host 0.0.0.0] [--port 8787] [--no-auth] [--stdio]` | Start the MCP memory engine (streamable HTTP LAN / --stdio local zero-process mode; Bearer token + X-Agent-Id + X-Agent-Key auth) |
| `yotta-memory lan enable [--onstart] / disable / status` | Autostart management (Windows: scheduled task with an S4U principal — runs silently in the background with no console window; `--onstart` starts at boot without a logon session, registration needs admin; non-admin auto-degrades to user-level silent Startup; Linux: systemd user unit, falls back to user crontab @reboot). v0.24.1 persists a per-user `serve-profile.json`; `lan status` reports drift and old tasks lacking `--profile` |
| `yotta-memory serve --profile <file>` | Read the per-user service profile, pin memory/runtime/config roots, validate absolute paths and the Windows user, and fail closed before opening the MCP port when a path is missing |
| `yotta-memory maintain [--dry-run] [--apply] [--purge] [--threshold N] [--age N] [--dedup] [--dedup --apply] [--merge A,B]` | Self-organization: archive / forget candidates / confidence-scored dedup / auto-merge high-confidence groups; dry-run by default; `--dedup` is mutually exclusive with archiving |
| `yotta-memory consolidate [--min-age N] [--min-idle N] [--max-utility N] [--min-group N] [--period N] [--type T] [--model <cmd>] [--apply] [--undo <batch>] [--batches]` | Periodic-summary compression (v0.10.0): group old idle low-value memories into one traceable summary and archive the originals; dry-run by default; `--undo <batch>` rolls a batch back; `--batches` lists batches |
| `yotta-memory feedback <file> --useful|--useless [--reason <r>] [--undo]` | Usage feedback (useful/useless adjusts weight / confidence / feedback_net; --undo rolls back the last one) |
| `yotta-memory distill [--owner <id>] [--subject <topic>] [--model <cmd>] [--out <path>]` | Psychological-log distillation (stats / topic profile / knowledge map; optional local model, local CLI only) |
| `yotta-memory explain <file>` | Show the utility breakdown and archive / forget / BOUND-exempt status of one memory |
| `yotta-memory bench [--evalset <file>] [--k N] [--seed N] [--bootstrap N] [--ablate] [--gate <metric>=<value>] [--timing] [--year <yyyy>] [--json] [--out <file>]` | Reproducible retrieval benchmark (v0.17.0): deterministic auto sampling from the store or an explicit evalset v1; reports Recall@k / MRR / nDCG@k / HitRate with bootstrap 95% CI plus store and evalset fingerprints, and writes no wall-clock data by default; `--ablate` compares lexical / semantic × fused / pure-score; `--gate` fails the run (exit 1) when a metric is below the threshold; `--timing` adds p50 / p95 and marks the report as not byte-reproducible. Read-only: no index rebuild, no access counters, no external embedding plugin |
| `yotta-memory scan [--path <dir>] [--gate <severity>] [--quarantine --yes] [--restore] [--id <batch>] [--json]` | Memory-store security scan (v0.17.0): seven classes = malicious instruction / prompt injection / credential leak / data exfiltration / guardrail bypass / behaviour manipulation / privilege escalation, five severities with `file:line` evidence and rule provenance; report-only by default, zero network and zero dependencies; `--gate` fails the run (exit 1) at or above the given severity; `--quarantine` needs `--yes` or interactive confirmation, backs each original file up byte-for-byte into `.memory-scan/quarantine/` and then redacts hit lines, and `--restore` rolls it back; credential snippets are always masked |

Types: `FACT` (fact, public shared) / `PREF` (preference) / `BOUND` (boundary) / `COMMIT` (commitment).

Example:
```bash
yotta-memory init
yotta-memory remember PREF 用户 偏好短回复，不要用表情
yotta-memory recall 偏好
yotta-memory profile
yotta-memory context --limit 10
yotta-memory recall --type FACT --limit 10
```

Environment variables:
- `YOTTA_MEMORY_HOME`: overrides the user-level store directory (default `~/.yottamemory/`).
- `YOTTA_MEMORY_AGENT_HOME` / `YOTTA_MEMORY_AGENT_KEY_FILE`: explicit AI host directory / key file overrides for `key status` and `key claim`; command-line `--to` / `--agent-key-file` take precedence.

Identity environment variables (`YOTTA_AGENT_ID`, `AGENT_ID`, `YOTTA_MEMORY_AGENT_KEY`, `YOTTA_MEMORY_TRUST_ENV_AGENT`) are no longer supported. The CLI ignores them; HTTP / stdio MCP startup rejects them so a stale host configuration cannot silently keep using the old model.

## After the agent is wired up

Once the skill is installed into an agent, SKILL.md teaches it the workflow automatically: start work with `recall` to restore context → `remember` important info as you go → archive at wrap-up. You can also just say "记住 XXX" / "上次说到哪了" in conversation.

## LAN multi-machine sharing (portable memory disk mode)

The store can live on any host or disk (= the memory engine) and be reached by agents on other LAN hosts:

- **Local direct**: CLI reads/writes directly, no token;
- **Remote**: the engine host runs `yotta-memory serve` (or registers `lan enable` autostart); remote agents connect via MCP with `url + token + agent_key`. Same-host / shared-filesystem agents use `key claim`; cross-host setups without a shared filesystem require the user to transfer the host key securely.
- **Local zero-process**: local MCP clients can use `serve --stdio --agent-id <id> --agent-key-file <path>` to launch the CLI on demand (no resident process).

```json
{
  "mcpServers": {
    "yotta-memory": {
      "command": "node",
      "args": [
        "<runtimeRoot>/current/bin/yotta-memory.js",
        "serve", "--stdio", "--tools", "core",
        "--agent-id", "<this-agent-id>",
        "--agent-key-file", "<AI_HOME>/.yotta-memory-agent-key"
      ]
    }
  }
}
```

### Engine side (the host where memory lives)

1. Initialize or attach to the store (see CLI usage).
2. Install or refresh the stable runtime entry:
   ```bash
   yotta-memory runtime install --from-current
   yotta-memory runtime status
   yotta-memory doctor --runtime
   ```
   > `lan enable` and backup scheduling call the same runtime preparation automatically and only register `<runtimeRoot>/current/bin/yotta-memory.js`.
3. Generate an independent token for each agent that needs access:
   ```bash
   yotta-memory token new --agent <agent-id>     # printed once, e.g. ytm_... (--force if the ID is taken by another source)
   yotta-memory token list                        # list registered agents
   yotta-memory token revoke --agent <agent-id>   # revoke
   ```
   > New tokens take effect immediately; no service restart needed.
4. Start the service (default listens on 0.0.0.0:8787, Bearer token + X-Agent-Id + X-Agent-Key auth) — temporary run or register autostart:
   ```bash
   yotta-memory serve                          # temporary foreground
   yotta-memory lan enable                     # register autostart (Windows: scheduled task / user-level Startup; Linux: systemd user unit / user crontab)
   yotta-memory lan status                     # autostart status
   ```
   > `lan enable` registers a silent S4U scheduled task (no console window); `--onstart` switches to start-at-boot without a logon session (registration needs admin); non-admin `lan enable` auto-degrades to user-level silent Startup; `lan disable` removes it.

> On first listen on 0.0.0.0, Windows / the system firewall may ask to allow it — allow it, or other LAN hosts cannot reach it; `--no-auth` disables auth for trusted intranets only.

### Client side (remote agent)

Before registering the connection, confirm the agent has claimed its key:

```bash
yotta-memory key status <agent-id>
yotta-memory key claim <agent-id>
```

If the engine and the agent do not share a filesystem, `key claim` cannot read the remote pending file directly; the user must transport the key through a password manager or a secure file transfer into the agent host directory. Then register the connection (`url` + three headers):

```json
{
  "mcpServers": {
    "yotta-memory": {
      "url": "http://<engine-host-ip>:8787/mcp",
      "headers": {
        "Authorization": "Bearer <TOKEN>",
        "X-Agent-Id": "<this-agent-id>",
        "X-Agent-Key": "<agent_key from this agent's host key file>"
      }
    }
  }
}
```

Once connected, MCP tools (remember / recall / search / context / doctor / forget / archive / reindex / export / import / agent_info / profile / feedback / maintain / distill / explain / consolidate) read/write memory and confirm identity; the `--tools core` profile keeps only `context / recall / search / remember`, and the full profile exposes 17 tools. Management actions (init / config / token / lan / serve) are not exposed via MCP, and token management is never exposed remotely. MCP `export` / `import` paths are restricted inside the memory root, MCP `distill` does not support `--model`, and MCP never accepts a raw embedding command from remote callers — the local embedding plugin must be configured on the engine host with `config set embedding_cmd`. `X-Agent-Id` must match the token's registered agent, and encrypted private reads/writes additionally require the matching `X-Agent-Key`; read-partition rules are the same as the CLI (FACT public-readable, PREF / BOUND / COMMIT private).

### Location persistence

The CLI persists the store location (`~/.yottamemory/config.json`), so agents on the same host use the right location on later `recall` without re-specifying:

```bash
yotta-memory config set memory_home <store-dir>
yotta-memory config get
```

Resolution priority: `YOTTA_MEMORY_HOME` (temporary override) > `config.json#memory_home` (persistent) > default `~/.yottamemory`. Put the store on a disk, plug it into any host, run `config set memory_home` once (or `yotta-memory init --dir <dir>` to initialize directly to a location) and all memory is restored on that host.

## Development & validation

- Run at the project root: python tools/validate-skill.py yotta-memory
- Engine self-test: node --check bin/yotta-memory.js; node bin/yotta-memory.js --version

Keep tests green and bump the version before releasing changes.

## Changelog

See [CHANGELOG.md](./CHANGELOG.md).

## License

[MIT](./LICENSE) © YottaMeta. "Yuanyi" / "yotta-memory" and the YottaMeta family names (yotta-* prefix) are YottaMeta brand identifiers; derived works must not reuse them, see [NOTICE](./NOTICE).
