# OpenClaw Cross-Tool Commander 🎛️

> Drive your XiaoyaoClaw/OpenClaw gateway from any Agent Skills tool — Claude Code, Codex, OpenCode, Trae, DSH and more.

<p align="center">
  <img src="./assets/readme/hero.svg" width="100%" alt="OpenClaw Cross-Tool Commander — drive XiaoyaoClaw/OpenClaw gateway from any Agent Skills tool (Claude Code/Codex/OpenCode/Trae/DSH) via openclaw CLI">
</p>

> Command your local XiaoyaoClaw / OpenClaw multi-agent system from any Agent Skills-compatible tool.
> Cross-tool command layer — drive the OpenClaw gateway from Claude Code, Codex, OpenCode, Trae, DSH.

![license](https://img.shields.io/badge/license-MIT-green)
[![ClawHub downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fclawhub.ai%2Fapi%2Fv1%2Fskills%2Fxiaoyaoclaw-commander&query=skill.stats.downloads&label=ClawHub%20downloads&color=blue)](https://clawhub.ai/dtsola/skills/xiaoyaoclaw-commander)

## Why you need it

Claude Code, Codex, OpenCode, Trae, DSH and other agent tools help you write code and run tasks — while your OpenClaw / XiaoyaoClaw hosts a fleet of agents (tiantong, xiaoguang, xiaozhi...) and multiple channels (Feishu, Telegram...). **When you want an external agent to command OpenClaw directly**, you run into:

- ❌ **Command not found** — openclaw is not on PATH (desktop app embeds it), plain `openclaw` errors out
- ❌ **Real agents invisible** — env vars missing, `agents list` shows only `main`
- ❌ **Task goes to the wrong agent** — without `--agent`, it falls back to the default agent
- ❌ **Hardcoded paths** — break when the install location or platform changes

This skill provides a **standardized command channel**: dynamic detection + env-var filling + explicit-agent enforcement + cross-tool universality — any Agent Skills tool can command OpenClaw / XiaoyaoClaw in one go.

## Features

- 🔍 **Dynamic detection** — multi-level probing for the openclaw binary on Windows / macOS / Linux (XiaoyaoClaw desktop → PATH → vanilla desktop → local prefixes), no hardcoded paths
- 🧩 **Auto env-var filling** — derives `OPENCLAW_STATE_DIR` / `OPENCLAW_CONFIG_PATH` for desktop installs, so external tools see all real agents
- 🎯 **Explicit agent required** — `--agent` is mandatory; if the user doesn't name one, ask first — never fall back to a default
- 🌐 **Agent name mapping** — Chinese/English/emoji names ↔ ids resolved via the `Identity` field of `agents list`; if no match, ask — never guess
- 🧰 **Cross-tool universal** — works in any tool supporting Agent Skills (Claude Code / Codex / OpenCode / Trae / DSH), commands are fully generic
- 🔌 **Version-agnostic** — works on older openclaw (v2026.3.x) without `mcp`/`migrate`; defers to `--help`
- 🛡️ **No stored credentials** — no tokens/keys in the skill; gateway credentials come from the environment

## Install

```bash
# Manually from GitHub
git clone https://github.com/dtsola/xiaoyaoclaw-commander
# Copy the SKILL.md folder into your tool's skills directory:
#   Claude Code → ~/.claude/skills/
#   Codex       → ~/.codex/skills/
#   Others      → corresponding Agent Skills directory
```

> No need to install into OpenClaw's skills directory — this skill is for **external tools** commanding OpenClaw.
> 
> 🔒 **No persistence**: no cron jobs, no daemons, no startup scripts, no cross-session state files; env vars are set for the current shell only and no configuration file is touched.
> 
> 🌐 **Language is optional**: docs default to Chinese — ask in English (or any language) and the skill answers in it.
> 
> ⚠️ **Real-world side effects**: this is not a read-only tool — `agent` makes a real agent work (it may change files or send messages), and `message send` **delivers to real recipients** (Feishu, Telegram, ...). So 🟢 read-only commands (`health` / `agents list` / `sessions`) run directly, while 🟠 task dispatch and 🔴 channel sends **restate the exact target and content and wait for your confirmation first**. Check for sensitive content before sending.

## Usage

1. Put the skill in your tool's skills directory (Claude Code / Codex / OpenCode / Trae / DSH...)
2. Tell the tool "**have tiantong research X**" or "**send a Feishu message via OpenClaw**" (name the target agent or channel — it asks when that is unclear) — the skill will:
   - Detect the openclaw binary + fill in env vars
   - Map the agent name to its id via `agents list`
   - Run tasks / send messages / check status through the Gateway
3. Query commands: "list the OpenClaw agents", "is the gateway healthy?"

**When it should not fire**: chatting about OpenClaw without asking it to act; asking about OpenClaw docs, config format or internals (answer directly); a session that already runs inside OpenClaw; or a vague "send a message" / "research X" that neither routes through OpenClaw nor names a target.

## 🚀 Quick Start (3 steps, 5 minutes)

### Step 1: Install the skill

```bash
git clone https://github.com/dtsola/xiaoyaoclaw-commander
# Windows: copy to %USERPROFILE%\.claude\skills\xiaoyaoclaw-commander\
# macOS:   copy to ~/.claude/skills/xiaoyaoclaw-commander/
```

### Step 2: Delegate a task

Tell your Claude Code / Codex:

> Have tiantong research the release workflow of the xiaoyaoclaw ecosystem

The tool will: detect openclaw → fill env vars → map "天桐" via `agents list` → tiantong → `openclaw agent -m "..." --agent tiantong --json` → return the result.

### Step 3: Verify + more capabilities

- List agents: "which OpenClaw agents exist?" → `openclaw agents list` (with Chinese identities)
- Send a channel message: "send a Feishu message: xxx" → `openclaw message send --channel feishu -t <id> -m "..."`
- Check status: "is the OpenClaw gateway healthy?" → `openclaw health`

### Daily habits

| Scenario | Action |
|---|---|
| Delegate to a specific agent | "Have <name> do X" → auto-mapped id |
| Cross-channel notifications | "send via Feishu/Telegram" → `message send` |
| Team collaboration | `agents list` first to see who's available |
| Unknown agent name | The skill checks Identity and confirms — never guesses |

## How it compares

| | Raw terminal | openclaw mcp serve | **OpenClaw Cross-Tool Commander** |
|---|---|---|---|
| Binary location | manual, error-prone | needs new runtime | ✅ dynamic detection |
| Env vars | manual | needs setup | ✅ auto-filled |
| Runtime version | any | needs v2026.8+ | ✅ any version |
| Agent selection | default fallback risk | DIY | ✅ explicit + name mapping |
| Tool support | terminal only | MCP clients only | ✅ any Agent Skills tool |
| Skill standard | — | — | ✅ Agent Skills open standard |

## Directory structure

```
xiaoyaoclaw-commander/
├── SKILL.md                    # the skill itself (detection + env vars + command reference)
├── docs/
│   ├── DESIGN.md               # design document
│   ├── research-report-claude-code-openclaw.md   # research report
│   └── research-00-problem-decomposition.md      # problem decomposition
├── README.md
└── LICENSE
```

## License

MIT — use it freely, attribution optional.

---

## 🛠️ Need customization?

**Agent & Skills customization, from ¥800 (≈$110).**

- WeChat: `dtsola` (note: **openclaw custom**)
- Services: OpenClaw multi-agent deployment / workspace standardization / custom Skill development / agent memory system setup

## 💬 Join the community

Xiaoyao product family user group — feedback · exchange · suggestions:

<p align="center">
  <img src="./assets/readme/community-qr.png" width="280" alt="XiaoyaoAI user group QR: scan to join, or add WeChat dtsola (note: 加群)">
</p>

<p align="center">Scan to join, or add WeChat <code>dtsola</code> (note: <b>加群</b>)</p>

## Sister projects

- 🏠 **xiaoyaoclaw-workspace-initializer** (workspace initializer): gives every agent a "home" — standard directory structure + WORKSPACE.md rules + multi-agent config safety. <https://github.com/dtsola/xiaoyaoclaw-workspace-initializer>
- 🧠 **xiaoyaoclaw-memory-distill** (memory distill): distill conversations into structured memory — semantic classification (core → MEMORY.md / daily → logs) + first-run building + incremental dedup + sensitive-info skip. <https://github.com/dtsola/xiaoyaoclaw-memory-distill>
- 🗂️ **xiaoyaoclaw-task-progress-tracker** (task progress tracker): directory as container, PROGRESS.md as progress — lifecycle management for tasks/ and projects/ (status + progress log + document index). <https://github.com/dtsola/xiaoyaoclaw-task-progress-tracker>
- 📚 **xiaoyaoclaw-kb-retriever** (knowledge base retriever): local KB retrieval — hierarchical data_structure.md index navigation + progressive retrieval over md/pdf/xlsx, zero dependencies, Windows & macOS ready. <https://github.com/dtsola/xiaoyaoclaw-kb-retriever>
- 🩹 **xiaoyaoclaw-workspace-auditor** (workspace auditor): read-only health check — 5 categories, graded report with fix suggestions, zero-dependency, never modifies files. <https://github.com/dtsola/xiaoyaoclaw-workspace-auditor>
- 📎 **xiaoyaoclaw-web-clipper** (web clipper): save any web page as clean local Markdown with frontmatter — dual-engine extraction (readability + trafilatura fallback), Chinese-safe filenames, batch clipping with dedup; output lands in knowledge/clippings/ ready for kb-retriever indexing. <https://github.com/dtsola/xiaoyaoclaw-web-clipper>
- 🤝 **xiaoyaoclaw-agent-orchestrator** (agent orchestrator, **collaboration layer**): split, dispatch, track, aggregate, retry.<https://github.com/dtsola/xiaoyaoclaw-agent-orchestrator>
- 📊 **xiaoyaoclaw-usage-report** (usage report): parse session JSONL to answer how long each task took, which tools/skills/models were used, and how many tokens were consumed — zero dependency, local only, token is the primary metric. <https://github.com/dtsola/xiaoyaoclaw-usage-report>
- 🎛️ **xiaoyaoclaw-commander** (OpenClaw Cross-Tool Commander, **command layer**): this skill — command your XiaoyaoClaw/OpenClaw multi-agent system from any Agent Skills tool. <https://github.com/dtsola/xiaoyaoclaw-commander>
- 🔍 **xiaoyaoclaw-seo-skill** (SEO skill): analyze & optimize website search visibility — audit (technical SEO) / page / content / schema / geo (AI search, AEO/GEO) workflows + zero-dependency audit script, cross-tool ready. <https://github.com/dtsola/xiaoyaoclaw-seo-skill>

## 