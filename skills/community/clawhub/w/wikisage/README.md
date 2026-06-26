# wikisage

A **Karpathy-style LLM Wiki** packaged as an [AgentSkill](https://github.com/openclaw/openclaw) for
[OpenClaw](https://openclaw.ai) / Claude Code / any skill-aware agent.

> Persistent, plain-markdown knowledge base where **the LLM writes and maintains all content**,
> and the user supplies sources, exploration direction, and questions.
> No vector database — an `index.md` plus Obsidian-style `[[wikilinks]]` is enough.

Inspired by Andrej Karpathy's "LLM wiki" pattern.

---

## ✨ Features

- **Three-layer structure**: `raw/` (sources) → `pages/` (LLM-maintained knowledge) → `index.md` (navigation)
- **Confidence tagging**: every page declares `EXTRACTED` / `INFERRED` / `AMBIGUOUS` / `UNVERIFIED` at both frontmatter and paragraph level — the LLM must surface this in answers
- **SHA256 dedup** for ingest sources (files / URLs), so you never re-index the same PDF twice
- **Two-layer lint**:
  - *Layer 1* — `lint.py` (mechanical scan: orphans, missing concept pages, stale pages, missing cross-refs, missing confidence tags, index consistency)
  - *Layer 2* — LLM walks the report and fixes issues interactively via MCP
- **Obsidian MCP first**: all reads/writes prefer the filesystem-sandboxed Obsidian MCP server, with `read`/`write`/`edit` fallback
- **Logged everything**: `log.md` is an append-only timeline of every ingest / query / lint operation
- **Cross-platform**: Linux, macOS, Windows — pure `pathlib`, no POSIX-only calls

---

## 🖥️ Platform support

Works on **Linux, macOS, and Windows**. All scripts use `pathlib` + `os.path.expanduser("~")`,
so `~` resolves correctly everywhere (`/home/you` on Linux, `/Users/you` on macOS,
`C:\Users\you` on Windows). There are no POSIX-only syscalls.

Only the *shell one-liners* in this README differ per OS — see platform-specific blocks below.

> **Heads-up**: this skill relies on an **Obsidian filesystem MCP server** as its primary
> read/write channel. It falls back to `read`/`write`/`edit` tools if MCP isn't wired up, but
> you get meaningfully better behavior (sandboxing, structured errors) with it. See
> [Dependencies](#-dependencies) below.

## 📦 Install

### As an OpenClaw skill

**Linux / macOS:**
```bash
git clone https://github.com/harryzsh/wikisage \
  ~/.openclaw/workspace/skills/wikisage
```

**Windows (PowerShell):**
```powershell
git clone https://github.com/harryzsh/wikisage `
  "$HOME\.openclaw\workspace\skills\wikisage"
```

That's it — OpenClaw auto-discovers skills at startup.

### As a Claude Code skill

**Linux / macOS:**
```bash
git clone https://github.com/harryzsh/wikisage ~/.claude/skills/wikisage
```

**Windows (PowerShell):**
```powershell
git clone https://github.com/harryzsh/wikisage "$HOME\.claude\skills\wikisage"
```

### As a generic agent skill

Copy the folder into whatever directory your agent scans for skills, or point the agent at
`SKILL.md` directly.

---

## ⚙️ Configuration

All paths are driven by environment variables with safe defaults:

| Variable | Default | Purpose |
|----------|---------|---------|
| `WIKI_ROOT` | `$HOME/.openclaw/workspace/wiki` | Where the markdown wiki lives |
| `WIKI_SKILL_DIR` | `$HOME/.openclaw/workspace/skills/wikisage` | Where this skill is installed (scripts referenced by SKILL.md) |
| `MCPORTER_CONFIG` | `$HOME/.openclaw/workspace/config/mcporter.json` | Optional — path to your [mcporter](https://github.com/CrazyPython/mcporter) config (for the Obsidian MCP server) |
| `AWS_REGION` / `WIKI_EMBED_SECRET` | `us-east-1` / `wikisage/opensearch` | Only used by the optional `embed.py` (see below) |

> The skill itself is **channel-agnostic**. It does not push notifications anywhere. If you
> want weekly lint reports delivered to chat/email/a webhook, pipe `lint.py --summary` from
> your scheduler — see [Weekly lint schedule](#-weekly-lint-schedule) for examples.

Set them once in your shell profile, agent env, or cron line.

**Linux / macOS (bash/zsh):**
```bash
export WIKI_ROOT="$HOME/my-wiki"
export WIKI_SKILL_DIR="$HOME/.openclaw/workspace/skills/wikisage"
```

**Windows (PowerShell, current session):**
```powershell
$env:WIKI_ROOT = "$HOME\my-wiki"
$env:WIKI_SKILL_DIR = "$HOME\.openclaw\workspace\skills\wikisage"
```

**Windows (persistent, user-level):**
```powershell
[Environment]::SetEnvironmentVariable("WIKI_ROOT", "$HOME\my-wiki", "User")
[Environment]::SetEnvironmentVariable("WIKI_SKILL_DIR", "$HOME\.openclaw\workspace\skills\wikisage", "User")
```

> **Note for Windows users**: defaults like `~/.openclaw/workspace/wiki` resolve to
> `C:\Users\<you>\.openclaw\workspace\wiki`. If you prefer a more Windows-native location
> (e.g. `%USERPROFILE%\Documents\wiki`), just set `WIKI_ROOT` explicitly.

---

## 🗂 Initial wiki layout

After install, create the empty skeleton (or let the first ingest create it).

**Linux / macOS:**
```bash
mkdir -p "$WIKI_ROOT"/{raw,pages/{aws,ai,clients,projects,ops},.lint-history}
cat > "$WIKI_ROOT/index.md" <<'EOF'
# Wiki Index

_Pages auto-listed here by the LLM after each ingest._
EOF
touch "$WIKI_ROOT/log.md"
```

**Windows (PowerShell):**
```powershell
$root = $env:WIKI_ROOT
"raw","pages\aws","pages\ai","pages\clients","pages\projects","pages\ops",".lint-history" |
  ForEach-Object { New-Item -ItemType Directory -Force -Path "$root\$_" | Out-Null }
"# Wiki Index`n`n_Pages auto-listed here by the LLM after each ingest._" |
  Set-Content -Path "$root\index.md" -Encoding UTF8
New-Item -ItemType File -Force -Path "$root\log.md" | Out-Null
```

---

## 🔌 Dependencies

### Required
- **Python ≥ 3.9** (stdlib only for `lint.py` / `dedup.py` — no `pip install` needed)
- **Git** (to clone this repo)

### Strongly recommended: Obsidian filesystem MCP server

This skill is **designed around an Obsidian-style filesystem MCP server** as its primary
read/write channel. All operating rules in [`SKILL.md`](./SKILL.md) assume the LLM can call
`obsidian.read_text_file`, `obsidian.write_file`, `obsidian.edit_file`, `obsidian.list_directory`,
`obsidian.search_files`, and `obsidian.list_allowed_directories`.

**Why it matters:**
- Sandboxes all writes inside `$WIKI_ROOT` (allowed-dir enforcement) — the LLM can't accidentally
  touch files outside the wiki.
- Gives structured errors the LLM can reason about, instead of raw shell failures.
- Matches the Obsidian editor's view if you also open the same directory in Obsidian desktop
  (with any filesystem-based sync plugin) — works fine on Windows, macOS, Linux.

**How to wire it up via [mcporter](https://github.com/CrazyPython/mcporter):**

Add this to your `mcporter.json` (path defaults to `~/.openclaw/workspace/config/mcporter.json`,
or wherever `$MCPORTER_CONFIG` points):

```json
{
  "servers": {
    "obsidian": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "<absolute path to $WIKI_ROOT>"]
    }
  }
}
```

Replace `<absolute path to $WIKI_ROOT>` with the real path — most MCP launchers don't expand
environment variables inside the `args` array. Examples:
- Linux/macOS: `/home/you/.openclaw/workspace/wiki` or `/Users/you/wiki`
- Windows:     `C:\\Users\\you\\.openclaw\\workspace\\wiki` (escape the backslashes in JSON)

Alternative MCP servers that work the same way:
- [`@modelcontextprotocol/server-filesystem`](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) (vanilla, used above)
- Any other filesystem-style MCP server that exposes `read_text_file` / `write_file` / `edit_file` / `list_directory`

**Fallback without MCP:** the skill still works — `SKILL.md` explicitly tells the LLM to fall
back to plain `read` / `write` / `edit` tools and log that MCP is offline. You lose the sandbox
guarantee but everything else keeps running.

### Optional / experimental
- `embed.py` — Bedrock Titan embeddings → OpenSearch indexing. Requires AWS creds, a secret named
  `$WIKI_EMBED_SECRET` containing `{endpoint, username, password}`, and
  `pip install boto3 opensearch-py requests-aws4auth`. Skip unless you want semantic search on
  top of the wiki.

---

## 🚀 Usage

Once the skill is loaded, talk to your agent naturally:

| You say | Skill does |
|---------|-----------|
| "加进 wiki" / "ingest this" | Reads `index.md`, decides new-vs-update, writes page + updates index + logs |
| "查 wiki" / "what do we have on X" | Reads `index.md` + relevant pages, answers with `> 参考：[[page]]` citations |
| "整理 wiki" / "lint the wiki" | Runs `lint.py`, then LLM walks the report interactively to fix issues |

Under the hood the agent follows the flows in `scripts/ingest.md`, `scripts/query.md`, `scripts/lint.md`.

---

## 🗓 Weekly lint schedule

`lint.py` only *scans* and writes a report to `$WIKI_ROOT/.lint-history/YYYY-MM-DD.md`. It
does not push notifications anywhere — **delivery is your scheduler's job**. Use
`--summary` to get a single-line status suitable for piping into mail/chat/webhooks.

### Linux / macOS (cron)

```cron
# every Monday 02:00 local time: run full lint, write report to .lint-history/
0 2 * * 1 WIKI_ROOT=$HOME/.openclaw/workspace/wiki \
  python3 $HOME/.openclaw/workspace/skills/wikisage/scripts/lint.py \
  >> $HOME/.openclaw/workspace/wiki/.lint-history/cron.log 2>&1
```

**Pipe the one-line summary to whatever you use:**

```bash
# email
python3 .../lint.py --summary | mail -s 'wiki lint' you@example.com

# Slack incoming webhook
python3 .../lint.py --summary | \
  xargs -I{} curl -s -X POST -H 'Content-type: application/json' \
    --data '{"text":"{}"}' https://hooks.slack.com/services/XXX/YYY/ZZZ

# Any chat via openclaw CLI (Feishu / Discord / Telegram / Slack / ...)
python3 .../lint.py --summary | \
  xargs -I{} openclaw message send --channel feishu --target user:ou_xxx --message {}

# Discord webhook
python3 .../lint.py --summary | \
  xargs -I{} curl -s -X POST -H 'Content-type: application/json' \
    --data '{"content":"{}"}' https://discord.com/api/webhooks/XXX/YYY
```

### Windows (Task Scheduler, PowerShell)

Register a weekly task that runs Monday 02:00:

```powershell
$wikiRoot  = "$HOME\.openclaw\workspace\wiki"
$skillDir  = "$HOME\.openclaw\workspace\skills\wikisage"
$action    = New-ScheduledTaskAction -Execute "python" `
    -Argument "`"$skillDir\scripts\lint.py`""
$trigger   = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 2am
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive
$settings  = New-ScheduledTaskSettingsSet -StartWhenAvailable

Register-ScheduledTask -TaskName "wikisage-weekly-lint" `
  -Action $action -Trigger $trigger -Principal $principal -Settings $settings

[Environment]::SetEnvironmentVariable("WIKI_ROOT", $wikiRoot, "User")
```

To deliver a summary to chat/email, wrap it in a small script that pipes `lint.py --summary`
into your tool of choice, then point the scheduled task at that wrapper.

---

## 🧭 Why this pattern?

Plain markdown + Obsidian-style links gives you:

- **Zero lock-in** — it's just `.md` files; any editor works
- **Version-control friendly** — your wiki content belongs in a separate (private) git repo
- **Grep-able forever** — no ORM, no schema migrations, no embeddings to rebuild
- **LLM-native** — every page fits in context, and the whole `index.md` is an agent's cognitive map

The LLM is responsible for *curation* (deduping, cross-referencing, contradiction detection),
not just bulk-dumping. Hence the confidence tags, the lint flow, and the append-only `log.md`.

---

## 📁 Repository layout

```
wikisage/
├── SKILL.md              # skill manifest + operating rules (what the LLM reads)
├── scripts/
│   ├── ingest.md         # ingest flow spec
│   ├── query.md          # query flow spec
│   ├── lint.md           # lint flow spec (Layer 1 + Layer 2)
│   ├── lint.py           # Layer 1 mechanical scanner
│   ├── dedup.py          # SHA256 dedup cache for sources
│   └── embed.py          # optional: Bedrock Titan → OpenSearch
├── README.md             # you are here
└── LICENSE               # MIT
```

---

## 🔐 Separate your wiki content from this skill

**Do not commit your actual wiki (`$WIKI_ROOT`) to this public repo.**

This repo contains only the *skill definition*. Your wiki content — clients, account IDs,
decisions — should live in:

- a **separate private repo** (recommended), or
- a local Mutagen/rclone mount, or
- AWS S3 / any blob store

That separation is the whole point: the skill is reusable across machines; the knowledge is yours.

---

## 📝 License

MIT — see [LICENSE](./LICENSE).

## 🙏 Credits

Pattern inspired by [Andrej Karpathy](https://x.com/karpathy)'s "LLM wiki" idea.
Built for / battle-tested on [OpenClaw](https://openclaw.ai).
