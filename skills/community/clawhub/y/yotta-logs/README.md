<p align="center"><b>Language</b>: English · <a href="./README.zh-CN.md">中文</a></p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-logs banner" width="100%" />
</p>

<h1 align="center">yotta-logs · 元史 (Yuanshi)</h1>

<p align="center">YottaMeta's skill for retrieving and analyzing <b>historical session / memory logs across AI agents</b>: zero-dependency search over JSONL, JSON, SQLite and Markdown records to recall past conversations and parent-session context with original-log evidence.</p>
<p align="center">Activates when the user references previous content / a parent session / historical context — <b>no jq / rg needed; pure standard-library deterministic retrieval</b>.</p>
<p align="center">Pure Python 3.8+ standard library, zero external dependencies; Windows + Linux + macOS; read-only local logs, redacted by default, never uploaded.</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-logs"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-logs" /></a>
  <a href="https://github.com/YottaMeta/yotta-logs"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-logs" /></a>
  <a href="https://github.com/YottaMeta/yotta-logs/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-logs" /></a>
  <a href="https://github.com/YottaMeta/yotta-logs"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
</p>

## What it is

Agents generate a steady stream of session and memory records (JSONL / single-file JSON / SQLite / Markdown…). When tracing across sessions, the hard part is rarely "remembering that something happened" — it is finding *where the original text is, who said it, and when*. Yuanshi turns those records into a **deterministic retrieval engine**: discover every log and memory source → search by keyword / regex / date / session / role / source / kind / format → extract raw conversation → summarize messages, tokens, cost and tool usage.

It is not tied to any single platform: it is an agent-agnostic toolkit that works in any agent supporting Agent Skills. Zero dependencies, read-only local access, no network; output is redacted by default so secrets and tokens in logs never leak into context.

## Core value

- **Zero-dependency retrieval** — Python 3.8+ standard library; no jq / rg / ripgrep; works out of the box on Windows + Linux + macOS.
- **Multi-format (v0.2.0)** — not JSONL-only anymore: JSONL / single-file JSON / SQLite (opencode, Cursor state.vscdb…) / Markdown (memory + free notes) / binary (title-only) via "format family × field-alias normalization + config fallback", on a unified Record model.
- **Full source discovery** — `locate` / discover finds common local log and memory sources (Codex / Claude Code / Clawdbot / opencode / Gemini / yotta-memory / Codex notes…), filtered by the default search scope.
- **Fault-tolerant parsing** — bad lines and fields are skipped and counted, never aborting a search; binary / encrypted files degrade to titles.
- **Redacted by default** — output masks likely secrets / tokens / credentials (sk-, ghp_, AKIA, JWT, Bearer, URL passwords, key=value assignments, over-long tokens); disable with --no-redact.
- **Multi-dimensional filtering** — keyword (case-insensitive) / regex / date / session ID / sessions.json alias / role (user / assistant / tool / system / developer) / source (--source) / kind (--kind) / format (--format).
- **Structured output** — --json emits clean JSON with source, session ID, line number, timestamp and role, ideal for programmatic provenance checks.
- **Read-only & safe** — reads local logs and memory files only; never modifies, deletes or uploads; complements yotta-memory (semantic memory).

## Why use it

| Advantage | Description |
|---|---|
| **Zero dependency** | Python 3.8+ standard library; no model, database or external service; Windows + Linux + macOS |
| **Multi-format** | JSONL / JSON / SQLite / Markdown / binary; field-alias normalization + config fallback |
| **Deterministic** | Reproducible, explainable logic; hits return original fragments + line numbers, no model guessing |
| **Redacted by default** | Likely secrets / tokens / credentials masked automatically |
| **Default scope** | Session + structured memory sources on by default; free notes / binary logs off unless explicitly enabled |
| **Fault-tolerant** | Tolerates storage differences across agents; bad lines skipped without aborting; encrypted files fall back to titles |
| **Pinpoint provenance** | Hits carry source / session ID / line / timestamp / role for exact tracing |
| **Ecosystem distribution** | GitHub + npm + ClawHub synced; four install methods (npx / git clone / Download ZIP / install.sh) |

## Commands

| Command | Description |
|---|---|
| locate | Discover all local log / memory sources (source / format / kind / default on-off) |
| scan | List all sessions across sources (source / session ID / date / message count / size / alias) |
| search | Cross-source search: keyword / regex + date / session / role / source / kind / format filters; timeline hits (--json structured) |
| session | Extract one session's raw text (timeline + role + text); --role filter, --tools annotate tool calls |
| stats | Session statistics: messages / role distribution / token / cost / time range / per-source (--daily daily rollup) |
| tools | Tool-call frequency ranking |
| version | Print version |

## Quick start

On Windows use `python`; on Linux/macOS use `python3`.

```bash
# Discover all local log / memory sources
python3 scripts/yotta_logs.py locate

# Cross-source keyword search (default scope = session + structured memory; free notes off)
python3 scripts/yotta_logs.py search "deployment plan"

# Target a directory / file (format family auto-sniffed)
python3 scripts/yotta_logs.py scan --dir ~/.clawdbot/agents/<agentId>/sessions

# Regex + date + session filters
python3 scripts/yotta_logs.py search "CI failed" --regex --date 2026-08-26 --dir /path/to/sessions

# Filter by source / kind / format (source names from locate)
python3 scripts/yotta_logs.py search "remember" --kind memory
python3 scripts/yotta_logs.py search "XSS" --source opencode-db
python3 scripts/yotta_logs.py search "deploy" --format sqlite

# Explicitly enable free notes (off by default)
python3 scripts/yotta_logs.py search "push gate" --kind note

# Extract a single session's raw text
python3 scripts/yotta_logs.py session abc123 --dir /path/to/sessions

# Statistics (messages / tokens / cost / daily rollup)
python3 scripts/yotta_logs.py stats --dir /path/to/sessions --daily

# Tool-call ranking
python3 scripts/yotta_logs.py tools --dir /path/to/sessions

# JSON structured output (for programmatic checks)
python3 scripts/yotta_logs.py search "deployment plan" --dir /path/to/sessions --json
```

Exit codes (consistent with the YottaMeta family): 0 = success; 1 = no match / empty result; 4 = usage error / fatal exception.

When --dir is omitted, the engine tries $YOTTA_LOGS_DIR, then full source discovery (locate logic) filtered by the default scope; if nothing is found it exits 4 with a hint.

## Installation

Pick any of the four methods below; the order is the recommended priority. Skill files always come from **npm** (GitHub can be slow without a proxy; npm supports mirrors).

### Method 1: npm one-liner (recommended)

```text
# Optional China mirror: npm config set registry https://registry.npmmirror.com
npx -y @yottameta/yotta-logs@0.3.5 --agent <agent-name>      # install to the agent's default user-level skills dir
npx -y @yottameta/yotta-logs@0.3.5 --dir <your-skills-dir>   # point to the skills dir itself (e.g. ~/.codex/skills)
```

- `--agent <name>` installs to that agent's default user-level directory; `--list` shows each agent's default directory.
- `--dir <path>` installs to the given directory; for agents not in the preset list, point `--dir` at their skills directory.
- If the mirror has not synced the new package (404): add `--registry=https://registry.npmjs.org/` (a proxy may be needed in China), or wait for the mirror cache.

### Method 2: git clone (developers / git available)

```text
git clone https://github.com/YottaMeta/yotta-logs.git <your-skills-dir>/yotta-logs
```

### Method 3: GitHub Download ZIP (manual / no git)

On the GitHub repository `YottaMeta/yotta-logs`, click **Code → Download ZIP**, unzip it and put the `yotta-logs` folder into the agent's skills directory.

### Method 4: install.sh (multi-agent one-liner script)

```text
bash install.sh --agent <name>   # install to the agent's default user-level directory
bash install.sh --dir <path>     # install to the given directory
bash install.sh --list           # list agents -> default directories
```

> Method 1 uses the npm registry (npmmirror / npmjs) and does not depend on GitHub; Methods 2/3 use GitHub and may fail without a proxy in China.
## Usage with an AI agent

1. Wire this repo's SKILL.md into any agent's skills / rules system (see Installation above).
2. When the user asks "what was that deployment plan we discussed?", locate and search:
   ```bash
   python3 scripts/yotta_logs.py locate
   python3 scripts/yotta_logs.py search "deployment plan"
   ```
   You get a timeline of hits (source / session / time / role / raw fragment).
3. For full context, extract the session:
   ```bash
   python3 scripts/yotta_logs.py session <sessionId> --dir <logs directory>
   ```
4. For exact provenance, use --json to get source / session ID / line number / timestamp and cite it in your answer.
5. To review a session's cost or tool-use distribution, use stats / tools.

## Development & validation

- Tests: `python scripts/test_yotta_logs.py` (139 cases: 75 v0.1.0 regression + 64 v0.2.0 generalization)
- Basic validation: `python tools/validate-skill.py yotta-logs` (run from the repository root)
- Format registry: references/agent-formats.md; unified format: references/format.md; CLI protocol: references/cli.md; security boundary: references/security.md

## Changelog

- v0.3.1 (2026-09-13): Removed machine-specific hardcoded paths; discovery and config now follow environment variables and platform defaults, with regression coverage.
- v0.3.0 (2026-09-08): Evaluation-driven refinement — added FAQ, hardened installer error handling and exit codes, and added installer tests.

- v0.2.2 (2026-08-29): Install docs alignment — unified four install methods (npx -y @yottameta/yotta-logs@0.3.5 --agent/--dir, git clone, GitHub Download ZIP, install.sh --agent/--dir/--list), removed the legacy GitHub-clone installer and global-install (-g) recommendations; bilingual README install section synced to 发布规范 §3.3.1. No functional change.

- v0.2.1 (2026-08-27): Bilingual documentation — English README as the GitHub / npm / ClawHub homepage, full Chinese doc moved to README.zh-CN.md, English npm description.
- v0.2.0 (2026-08-27): Multi-format generalization — JSONL / single-file JSON / SQLite (opencode etc.) / Markdown (memory + free notes) / binary; unified Record + field-alias normalization + config fallback; discover; new --source / --kind / --format filters and default search scope (session + structured memory on, free notes / binary logs off). See CHANGELOG.md.
- v0.1.0 (2026-08-27): Initial release — zero-dependency JSONL session log search engine (locate / scan / search / session / stats / tools / version + default redaction + sessions.json alias + read-only).

## References

- references/faq.md

## License

MIT © YottaMeta — see [LICENSE](./LICENSE).
