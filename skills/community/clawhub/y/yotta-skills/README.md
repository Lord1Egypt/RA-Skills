<p align="center"><b>Language</b>: English · <a href="./README.zh-CN.md">中文</a></p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-skills banner" width="100%" />
</p>

<h1 align="center">yotta-skills · 元阁 (YuanGe)</h1>

<p align="center">YottaMeta's skill-family <b>orchestration router, inventory, and one-command installer</b>: route which skills to combine for a task, then one <code>npx</code> line installs the published <code>yotta-*</code> skills (currently <b>27</b>) into any agent or directory.</p>
<p align="center">List the family, route a task, install everything, incrementally update, preview with <code>--dry-run</code>, pin exact versions - idempotent and zero-dependency (Node.js 18+), pure npm ecosystem.</p>
<p align="center">This package contains <b>no skill bodies</b> — only a manifest, a downloader, a placer and a summary. Each skill still comes from its own npm package.</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-skills"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-skills" /></a>
  <a href="https://github.com/YottaMeta/yotta-skills"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-skills" /></a>
  <a href="https://github.com/YottaMeta/yotta-skills/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-skills" /></a>
  <a href="https://github.com/YottaMeta/yotta-skills"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
</p>

## What it is

Installing the whole YottaMeta family used to mean running <code>npx</code> for each skill one by one. 元阁 turns it into a single command: it reads a built-in manifest (27 published skills), downloads each from its own npm package, places it into the target skills directory, and prints a summary (success / skipped / failed).

元阁 is also the **family orchestration planner**: given a task, check the orchestration table first — which skills to combine, in what order, and why — then install exactly those. The decision table ships in the package as <code>references/orchestration.md</code> and is summarized in <code>SKILL.md</code>.

- **List** - see the whole family: slug, Chinese name, package, version and a one-line description.
- **Orchestration routing** - <code>--route</code> turns a task summary into a candidate combination, call order, per-skill roles, confidence, evidence, installed/missing status, and an install command; it only suggests installation and never installs automatically. An optional local provider may add or re-order installed skills within the allow-list and return <code>confidence</code> / <code>reasons</code> / <code>summary</code> / <code>alternatives</code> (no behavior change when unconfigured; see <code>references/provider-protocol.md</code>).
- **M1 memory adjudication** - <code>decide-memory</code> returns read-only <code>promote / hold / demote</code> suggestions, scores and signal details. Scoring is performed by a user-configured local provider (capability <code>m1.adjudicate</code>). It is read-only by default; <code>--promote</code> writes only a local recommendation file and never writes memory or deletes anything. <code>usage</code> is off by default and records only structured signals after the user enables it.
- **Install** — install everything (or a subset) into an agent's default user-level directory or any directory.
- **Update** — incremental update: add missing skills, upgrade version-skewed ones.
- **Update check / auto-update** — <code>update --check</code> compares installed skill versions against the npm registry and reports; <code>update --check --scheduled</code> is the weekly background entry with a local cache and jitter, so it stays offline until due; <code>update --auto</code> upgrades the installed YottaMeta family to the latest (non-family skills are never auto-updated).
- **Works without npm** — fetching and extraction default to built-in Node channels (npm / system tar are fallbacks only); <code>update --installed-only</code> adopts only skills already installed on the machine and never backfills or errors on missing ones.
- **Doctor / rollback** — <code>doctor</code> checks the installed skill directory, version, manifest, registry and custom doctor script without modifying it; <code>--dir</code> may point to a skills container or directly to a single skill package. <code>rollback</code> validates a snapshot and restores the latest install or update.
- **Runtime hook adapter** — manifests declare six lifecycle requirements; <code>hook capabilities / evaluate / bind / unbind</code> probe host support, apply deterministic decisions, record evidence, and never overstate audit-only hosts as enforced.
- **Idempotent** — a skill already at the manifest version is skipped; re-running is safe.
- **Pre-install gate** — family installs read the package manifest, bootstrap yotta-verify (元信) when it is missing, then scan each package. <code>DO NOT INSTALL</code> blocks; caution/review continue with visible risk. Old versions are snapshotted before replacement.
- **Inventory / re-index** - scan the skill directories on this machine and keep a local registry (<code>~/.yottaskills/registry.json</code>); set <code>YOTTA_SKILLS_REGISTRY_FILE</code> to isolate the registry per agent; self-contained, no other skills required. Newly installed skills are discovered automatically: <code>install</code> / <code>update</code> re-index the registry afterwards, and <code>--reindex</code> re-scans on demand. An optional <code>yotta-skills</code> MCP (on-demand, not resident) exposes <code>list_installed_skills</code> / <code>describe_skill</code> / <code>reindex</code> / <code>route_request</code> / <code>decide_memory</code>; see <code>SKILL.md</code> for the config.
- **No silent writes** - 元阁 only suggests. Installing skills, adding a client <code>mcpServers</code> entry, and writing an agent's global memory each require explicit user confirmation beforehand; declining never blocks the plain CLI workflow.

Boundaries: it only downloads, places, gates and summarizes — it does **not** develop skill content, does **not** bundle any skill body, does **not** use <code>-g</code> global installs, and does **not** silently write host configuration or agent global memory. Besides the target directory, it keeps its registry, snapshots, install evidence and update-check cache under <code>~/.yottaskills</code>.

## Usage cases

**1. Put the whole family into one agent.** `npx -y @yottameta/yotta-skills install --agent codex` resolves the manifest, scans each package with the pre-install gate, places every skill (already-current ones are skipped) and re-indexes the registry afterwards.

**2. Keep one source of truth and fan it out.** `hub install` places the family into a single local Hub directory; `hub link --all` then distributes it to every verified host as a junction or symlink, and `hub status` / `doctor` show where each copy points and whether anything drifted.

**3. See what is already installed, and what a task needs.** `--inventory` / `--reindex` scan the skill directories on this machine into a local registry, while `--route "<task>"` returns a candidate combination, call order, per-skill role, confidence, evidence, installed/missing status and the install command. Routing only suggests; it never installs on its own.

## Quick start

Primary flow (Hub as the main path; the installation itself is agent-agnostic):

```bash
# 1) See the hosts and skill directories on this machine (states: available / orphan / missing / marker-only)
npx -y @yottameta/yotta-skills hub hosts

# 2) Install into the Hub source of truth (default ~/.yottaskills/hub; no agent needed)
npx -y @yottameta/yotta-skills hub install

# 3) Distribute to every verified host (Windows junction / macOS·Linux symlink)
npx -y @yottameta/yotta-skills hub link --all

# 4) Manage from the local panel (host matrix / links & health / adoption / rollback)
npx -y @yottameta/yotta-skills view
```

Standalone install (run the engine as an independent CLI, no agent required):

```bash
npx -y @yottameta/yotta-skills install-self                    # default: ~/.yottaskills/yotta-skills
npx -y @yottameta/yotta-skills install-self --dir ~/tools/yotta-skills
npx -y @yottameta/yotta-skills where                           # running CLI / standalone installs / Hub location
```

Direct install into a specific agent (compatibility path):

```bash
# List the whole family (no network, no changes)
npx -y @yottameta/yotta-skills --list

# Install everything into an agent's default user-level skills dir
npx -y @yottameta/yotta-skills install --agent codex

# Install everything into any directory (each skill lands in <dir>/<slug>)
npx -y @yottameta/yotta-skills install --dir ~/my-skills

# Install only selected skills
npx -y @yottameta/yotta-skills install yotta-memory yotta-verify --dir ~/my-skills

# Incrementally update installed skills
npx -y @yottameta/yotta-skills update --agent codex

# Check for updates manually (read-only, no changes)
npx -y @yottameta/yotta-skills update --check

# Weekly background entry (stays offline until due; writes ~/.yottaskills/update-check.json)
npx -y @yottameta/yotta-skills update --check --scheduled

# Check and auto-update the installed YottaMeta family (pre-install gate applies; non-family skills untouched)
npx -y @yottameta/yotta-skills update --auto

# Adopt only the family skills already installed on this machine (no backfill)
npx -y @yottameta/yotta-skills update --installed-only --dir ~/my-skills

# Read-only health check (optionally with --slug / --json)
npx -y @yottameta/yotta-skills doctor --dir ~/my-skills --slug yotta-memory

# List snapshots; restore the latest install or update
npx -y @yottameta/yotta-skills rollback --list --dir ~/my-skills
npx -y @yottameta/yotta-skills rollback --slug yotta-memory --dir ~/my-skills

# Inspect host hook capability and evaluate one manifest event
npx -y @yottameta/yotta-skills hook capabilities --host codex --json
npx -y @yottameta/yotta-skills hook evaluate --host codex --event before_send --manifest ./skill-manifest.json --json

# Preview what would be installed (no network, no changes)
npx -y @yottameta/yotta-skills --dry-run

# Route a task to a combination, call order, and missing-skill install suggestion
npx -y @yottameta/yotta-skills --route "Review this code carefully before release"

# Inspect / enable local structured usage signals (off by default)
npx -y @yottameta/yotta-skills usage status
npx -y @yottameta/yotta-skills usage enable

# Read-only M1 memory adjudication; --promote writes only a local recommendation file
npx -y @yottameta/yotta-skills decide-memory --explain
npx -y @yottameta/yotta-skills decide-memory --promote --json

# Inventory installed skills on this machine (self-contained scan, no other skills needed)
npx -y @yottameta/yotta-skills --inventory

# Re-index the registry (on demand; install / update re-index automatically)
npx -y @yottameta/yotta-skills --reindex

# Discover installed agents and their skill directories (filesystem-first; no memory registry)
npx -y @yottameta/yotta-skills hub hosts

# Install once into the local Hub, then link to every verified host (default scope)
npx -y @yottameta/yotta-skills hub install
npx -y @yottameta/yotta-skills hub adopt --scan
npx -y @yottameta/yotta-skills hub adopt --apply
npx -y @yottameta/yotta-skills hub link --all
# Opt in to auto-discovered directories (lock / data bridges are never linked)
npx -y @yottameta/yotta-skills hub link --all --include-discovered
npx -y @yottameta/yotta-skills hub status
npx -y @yottameta/yotta-skills hub doctor
```

Requirements: Node.js 18+, npm, and system <code>tar</code> (built into Windows 10+ / macOS / most Linux distributions).

## Commands & options

| Command / option | Description |
|---|---|
| `--list` (`-l`) | List the whole family with versions and descriptions; add a skill name to filter |
| `install-self [--dir <path>] [--dry-run] [--force]` | Standalone install: place the engine at an independent location (default `~/.yottaskills/yotta-skills`); no host config, no global shim |
| `where [--json]` | Show the YottaSkills location: running CLI / standalone installs (current one marked) / Hub source |
| `install --agent <name>` | Install everything into the agent's default user-level skills dir (compatibility path) |
| `install --dir <path>` | Install everything into a directory; each skill lands in `<path>/<slug>` |
| `install <skill>... [--agent <name> \| --dir <path>]` | Install only the given skills |
| `update [--agent <name> \| --dir <path>]` | Incremental update: add missing, upgrade version-skewed |
| `update --check` | Read-only update check: compare installed versions against the npm registry and report (exit 0 = up to date, 3 = updates available, 1 = could not check; run with `--registry <url>` to target a mirror); no changes |
| `update --check --scheduled` | Weekly background entry: no network until due, then one check and a local cache write; text mode stays quiet on failure, `--json` keeps diagnostics; always exits 0 |
| `update --auto` | Check and automatically update the installed YottaMeta family to the latest (runs the pre-install gate; never auto-updates non-family skills) |
| `doctor [--agent <name> \| --dir <path>] [--slug <slug>]` | Read-only self-check: SKILL / version / manifest / registry / custom doctor; `--dir` may point to a skills container or a single skill package; exit 0 = pass, 4 = no checkable target, 1 = check failed, 6 = manifest identity failure |
| `rollback [--agent <name> \| --dir <path>] [--slug <slug>]` | Validate and restore the latest snapshot; `--list` lists snapshots; `--json` returns machine-readable output |
| `hook capabilities --host <name>` | Show the six-event host capability matrix; unknown hosts stay <code>unsupported</code> |
| `hook evaluate --host <name> --event <event> --manifest <file> --context <json>` | Evaluate a manifest hook event, return allow / block / warn / unverified, and append structured evidence |
| `hook bind --host <name> --manifest <file>` / `hook unbind <id>` | Idempotently register or remove hook declarations |
| `--registry <url>` | npm registry to check against (default https://registry.npmjs.org/; `YOTTA_SKILLS_REGISTRY` overrides) |
| `--inventory` | Inventory installed skills: scan skill directories and update the local registry (self-contained); `--json` for JSON, `--project` adds project-level dirs |
| `--reindex` | Re-index the registry: re-scan skill directories and merge changes incrementally (on demand; `install` / `update` re-index automatically; `--rescan` is a synonym); `--json` for JSON |
| `hub hosts [--json] [--state <state>]` | Discover hosts and their skill directories (filesystem + environment; never reads the memory registry); lifecycle states (available / orphan / missing / marker-only); `--state` filter; `--json` for JSON |
| `hub hosts add <dir> [--label <name>] [--id <agentId>]` | Register a custom host directory (registration only: never creates directories or edits host config; Hub / bridge dirs are fail-closed) |
| `hub hosts remove <dir \| --id <agentId>> [--purge [--yes]]` | Remove a registration (never deletes the directory); `--purge` cleans an orphan directory (preview by default, `--yes` to execute; only Hub-pointing links are removed, the directory goes to trash for 7 days) |
| `hub hosts list` / `hub hosts mark <dir> --state <available\|orphan\|ignored>` | Show the registry / manually mark a host state (shares the registry store) |
| `hub config get \| set --hub <path> [--move] \| clear` | Persist the Hub location in `config.json` (priority `--hub` > `YOTTA_SKILLS_HUB` > config > default); `--move` copies + verifies the old Hub, relinks hosts and trashes the old one (7 days), fail-closed |
| `hub install [skill...]` | Install family skills into the local Hub (`~/.yottaskills/hub` by default; override with `--hub` / `YOTTA_SKILLS_HUB`) |
| `hub adopt --scan` | Read-only preview: scan existing host skills and report adoption candidates, duplicate conflicts and Hub state |
| `hub adopt --apply [--include <a,b>] [--force] [--in-place]` | Adopt selected skills into the Hub; copy-preserving by default and keep the original directory; non-YottaMeta sources are marked "no update source" |
| `hub refresh <slug> --from <path>` | Manually re-sync a non-YottaMeta skill (re-adopt, refresh hash and ledger) |
| `hub link --all [--include-discovered]` | Link Hub skills into every verified host (default scope; `--include-discovered` opts in to auto-discovered directories); target a single agent with `hub link <skill> --agent <id>`; Windows junction / POSIX symlink |
| `hub unlink --all` | Remove links only; never touches Hub sources (fail-closed for real directories or foreign links); per-agent removal with `hub unlink <skill> --agent <id>`; clean out-of-scope links with `--dir <dir>` |
| `hub remove <slug> [--dry-run] [--include-discovered]` | Delete a Hub skill: clean links on every host (including broken links), move the Hub directory to trash (7 days), clear Hub / link ledgers and write an audit record; fail-closed (real copies / foreign links are kept and reported; a link error aborts before the Hub entry is touched); narrowed `--agent` / `--dir` is only for cleaning dead links |
| `hub status` | Show Hub sources, versions, link hosts and drift; `--json` for JSON |
| `hub doctor` | Check broken links, missing Hub targets, slug mismatches, link scope (`link_scope`) and directory permissions; exit 1 on errors; `--json` for JSON |
| `--route <task-summary>` | Orchestration routing: return a combination, call order, per-skill roles, confidence, evidence, installed/missing status, and an install suggestion; also lists other installed (non-YottaMeta) skills as candidates matched mechanically against their frontmatter description, tagged "not scanned", read-only and never auto-invoked; an optional local provider may add or re-order installed skills within the allow-list and return <code>confidence</code> / <code>reasons</code> / <code>summary</code> / <code>alternatives</code> (see <code>references/provider-protocol.md</code>); `--json` for JSON plus a `dynamic` status block, `--project` adds project-level dirs |
| `usage status` / `usage enable` / `usage disable` | Inspect / enable / disable local structured usage signals; off by default and limited to slug, time, signal type, playbook / confidence and skill pairs |
| `usage mark --skill <slug> --signal used\|named\|accepted` | Record one explicit usage signal; no prior enable required |
| `usage reset --yes` | Clear the local usage record |
| `decide-memory [--dry-run\|--promote] [--explain]` | Read-only M1 memory adjudication; `--promote` writes only a local recommendation file and never writes memory or deletes anything; `--json` for stable JSON |
| `--no-reindex` | Do not re-index the registry automatically after `install` / `update` |
| `--dry-run` | Preview the install / update list; no network, no changes |
| `--pin` | Lock the exact manifest versions (default) |
| `--range` | Follow the latest patch of the same major (opt-in; the default stays pinned) |
| `--force` | Reinstall even when already at the latest version |
| `--skip-scan` | Manual escape hatch: skip the verifier gate and mark the result `explicit-unverified`; never used by `update --auto` |
| `--npm <path>` | Specify the npm executable |
| `--python <path>` | Specify the python executable (used for yotta-verify scan) |
| `--verify <path>` | Specify the yotta_verify.py path |
| `-h, --help` / `-v, --version` | Help / version |

Calling `npx -y @yottameta/yotta-skills <skill>` without a subcommand is equivalent to `install <skill>`.

Supported agent keys (17): `claude` `cursor` `codex` `gemini` `goose` `amp` `opencode` `windsurf` `workbuddy` `kiro` `trae` `trae-cn` `qwen` `comate` `codebuddy` `kimi` `agents`. For agents not in the preset list, point `--dir` at their skills directory (`.agents/skills` is not a universal directory).

## Version strategy

- Default `pin`: `npm pack <pkg>@<exact manifest version>` — fully reproducible, no silent drift onto a floating version.
- `--range` (opt-in): `npm pack <pkg>@<major>.x` — the latest patch of the same major, for users who explicitly want to follow patch releases.
- "Already at the latest" is determined by comparing the frontmatter `version` in `<dir>/<slug>/SKILL.md` with the manifest; matching versions are skipped.

## Installation

> **Two layers first**: `yotta-skills` (元阁) is a **family installer**, not a skill itself — it ships no skill bodies. It pulls each of the 27 published `yotta-*` skills from its own npm package into your target directory, so **getting 元阁 is not the same as having the skills**. After you have the installer, run `install` once to actually place the whole family. A single skill (e.g. `@yottameta/yotta-memory`) is its own npm package and installs by itself; 元阁 is the **install everything at once** manager, so its install path is different.

Pick any of the four methods below; the order is the recommended priority. The package always comes from **npm** (GitHub can be slow without a proxy; npm supports mirrors). Methods 2/3 only fetch the **installer**; method 4 places only the **installer skill** into an agent's skills directory — in each case you still run `install` to bring the whole family.

### Method 1: npm one-liner (recommended)

```text
# Optional China mirror: npm config set registry https://registry.npmmirror.com
npx -y @yottameta/yotta-skills install --agent <agent-name>      # install the whole family to the agent's default user-level skills dir
npx -y @yottameta/yotta-skills install --dir <your-skills-dir>   # install the whole family to a directory (e.g. ~/.codex/skills)
```

- `npx` fetches the latest `yotta-skills` automatically, so there is no separate installation step; this is the only method that both gets the installer and installs the family in one command.
- `--agent <name>` installs to that agent's default user-level directory; `--list` shows each agent's default directory.
- `--dir <path>` installs to the given directory; for agents not in the preset list, point `--dir` at their skills directory.
- If the mirror has not synced the new package (404): add `--registry=https://registry.npmjs.org/` (a proxy may be needed in China), or wait for the mirror cache.

### Method 2: git clone (developers / git available)

```text
git clone https://github.com/YottaMeta/yotta-skills.git <your-skills-dir>/yotta-skills
cd <your-skills-dir>/yotta-skills
node bin/yotta-skills.js install --dir <your-skills-dir>
```

- Cloning only fetches the **installer**; `--list` only prints the manifest and installs nothing. Run `install` to place the whole family into the target directory.

### Method 3: GitHub Download ZIP (manual / no git)

On the GitHub repository `YottaMeta/yotta-skills`, click **Code → Download ZIP**, unzip it, then run `node bin/yotta-skills.js install --dir <your-skills-dir>`. Copying the `yotta-skills` folder into an agent's skills directory only makes the **installer skill** itself callable (it has its own `SKILL.md`) — it does not bring the 27 skills; run `install` for that.

### Method 4: install.sh (multi-agent one-liner script)

```text
bash install.sh --agent <name>   # install the master installer skill to the agent's default user-level directory
bash install.sh --dir <path>     # install the master installer skill to the given directory
bash install.sh --list           # list agents -> default directories
```

- `install.sh` places the **元阁 installer skill** itself so an agent can invoke the family installer. To install the 27 skills, run `node bin/yotta-skills.js install --agent <name>` (or `--dir <path>`).

### Method 5: OpenClaw (host-native commands)

```text
openclaw skills install @yottameta/yotta-skills   # install (with ClawHub security audit)
openclaw skills update @yottameta/yotta-skills    # update
```

- OpenClaw uses the `~/.openclaw/skills` directory, which `--inventory` / `--reindex` recognize (including the `OPENCLAW_STATE_DIR` override).
- Host-native commands keep ClawHub's security-audit card and update tracking (`openclaw skills update` only covers ClawHub-tracked installs).

> Method 1 uses the npm registry (npmmirror / npmjs) and does not depend on GitHub; Methods 2/3 use GitHub and may fail without a proxy in China.

## Included skills

The full 27-skill manifest with Chinese names, package names, versions and descriptions is in `references/skill-list.md` (the machine-readable source is `skills.json`). Family coverage: Security & Guardrails (12), Quality & Engineering (4), Memory & Context (3), Writing & Expression (1), Workflow (1), Entry & Guidance (1), Compliance & Trust (1), Education & Learning (4).

## How it works

For each skill in the manifest: `npm pack <pkg>@<spec>` into a temp directory → `tar -xzf` → read the package manifest → run the yotta-verify pre-install gate (bootstrap yotta-verify first when missing) → snapshot the old version and stage the new one → atomically replace `<dest>/<slug>` → summary report. After `install` / `update` finishes, the local skill registry is re-indexed automatically so newly installed skills show up in `--inventory` / `--reindex` (disable with `--no-reindex`). Details: `references/install-flow.md`; beginner tutorial (Chinese): `references/tutorial.md`.

## Development & validation

```bash
# Run the test suite from the skill directory
npm test
```

The tests cover `--list`, install into a temp directory with assertions, idempotency, `--pin`, `update`, error paths, and yotta-verify scan integration (with a fake npm).

## 参考文档

- 常见问题：`references/faq.md`
- 复杂场景走查：`references/walkthroughs.md`

## License

MIT © YottaMeta — see [LICENSE](./LICENSE).
