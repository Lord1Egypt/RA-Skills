# OpenClaw Memory Distill 🧠

> Distill conversations into structured memory — fix context overflow, so your agent never forgets.

<p align="center">
  <img src="./assets/readme/hero.svg" width="100%" alt="OpenClaw Memory Distill — distill conversations into structured memory: semantic classification into core (MEMORY.md), daily (memory/YYYY-MM-DD.md), with dedup and sensitive-info skip">
</p>

> Turn conversations into structured memory to solve session context overflow.
> OpenClaw memory distillation & organization — distill conversations into MEMORY.md + daily logs, so your agent never forgets.

![license](https://img.shields.io/badge/license-MIT-green)
[![ClawHub downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fclawhub.ai%2Fapi%2Fv1%2Fskills%2Fxiaoyaoclaw-memory-distill&query=skill.stats.downloads&label=ClawHub%20downloads&color=blue)](https://clawhub.ai/dtsola/skills/xiaoyaoclaw-memory-distill)

## Why you need it

Every OpenClaw agent session starts fresh. Without memory organization, your agent will:
- ❌ **Context overflow** — long conversations push out important info, forcing a memory-wiping /reset
- ❌ **Fragmented memory** — decisions and project state scattered across daily logs, impossible to find
- ❌ **Missing MEMORY.md** — no long-term memory file, every session feels like a first meeting
- ❌ **Duplicate bloat** — the same content written over and over, memory files growing out of control

This skill solves it all in one go: **semantic classification + first-run memory building + incremental dedup + sensitive-info protection**.

## Features

> ⚠️ **This skill writes workspace files** (by default only after your confirmation): distillation
> organizes conversation content into the root `MEMORY.md` and `memory/YYYY-MM-DD.md` (archiving the
> previous MEMORY.md to `memory/archive/` first), and the first-time setup creates `distill-config.json`.
> Scheduled (cron) runs **report only** by default — unattended writing requires explicitly setting
> `autoWrite: true`.
> 🌐 **Language is optional**: docs are equivalent in Chinese and English, and answers follow the user's language.

- 🧪 **Semantic classification** — Core → root `MEMORY.md`; Daily → `memory/YYYY-MM-DD.md`; Temporary → current day only (semantic understanding, not keyword matching)
- 🏗️ **First-run memory building** — if `MEMORY.md` is missing, auto-generate it from historical logs — no empty skeleton
- 🔁 **Incremental dedup** — checks existing content before writing; appends only new entries, merges duplicates
- 🔒 **Sensitive-info skip** — tokens/passwords/keys auto-detected, never written to disk by default
- 🗄️ **Archive, never delete** — expired logs move to `archive/`, deletion requires human confirmation
- 🕐 **Three trigger modes** — one-phrase manual, daily Cron, HEARTBEAT dynamic
- 🧍 **Per-agent isolation** — each agent only organizes its own workspace memory
- 🏠 **Pairs with initializer** — it manages the "home" of your memory system; this skill manages the "content"

## Install

```bash
# From ClawHub (recommended)
clawhub install xiaoyaoclaw-memory-distill

# Or manually from GitHub
git clone https://github.com/dtsola/xiaoyaoclaw-memory-distill
# Put SKILL.md and templates/ into your skills directory
```

## Usage

1. Put the skill in your OpenClaw skills directory
2. **Ask explicitly** — "**distill memory**" / 「蒸馏记忆」/ "tidy up my memory" — then it will:
   - Check `memory/` and `MEMORY.md` (if missing, **build memory from historical logs**)
   - Scan the session → classify semantically → show a distill report (with sensitive-info notices)
   - Write incrementally with dedup → report results
3. Optional: say "schedule memory distill at 22:00 daily" to enable Cron automation

## 🚀 Quick Start (3 steps, 5 minutes)

### Step 1: Install the skill

```bash
clawhub install xiaoyaoclaw-memory-distill
```

### Step 2: Trigger your first distill

Tell your agent:

> distill memory

It will: check memory state → (build MEMORY.md from history if missing) → scan the session → classify → show report → write after confirmation → report back.

### Step 3: Verify + enable automation (optional)

Open your workspace and verify:

```
workspace root/
├── MEMORY.md               ← long-term memory (core) is ready
├── distill-config.json     ← distill configuration
└── memory/
    └── YYYY-MM-DD.md       ← today's distill log
```

Want daily automation? Tell your agent:

> schedule memory distill at 22:00 daily

When context is nearly full: "distill memory" first, then `/reset` — nothing is lost.

### Daily habits

| Scenario | Action |
|---|---|
| Session ends / context nearly full | Say "distill memory", then /reset |
| Long-term use | Schedule daily Cron at 22:00 |
| Weekly consolidation | Say "consolidate memory" → merge the last 7 days into MEMORY.md |
| Sensitive conversations | Auto-skipped by the report, nothing to do |

## How it compares

| | systiger/memory-distill | **xiaoyaoclaw-memory-distill** |
|---|---|---|
| Classification | keyword matching | ✅ semantic (core/daily/temporary) |
| Missing MEMORY.md | empty skeleton only | ✅ first-run build from history logs |
| Duplicate writes | no protection, bloats | ✅ incremental dedup & merge |
| Sensitive info | a one-line note | ✅ auto-detected and skipped |
| Expired cleanup | auto-delete (retentionDays) | ✅ archive only; delete needs confirmation |
| Auto /reset | config option exists | ✅ not provided (user decides) |
| Multi-agent memory | not distinguished | ✅ each agent handles its own |
| Workspace conventions | unrelated | ✅ paths follow WORKSPACE.md, config safety inherited from initializer |

## Directory structure

```
xiaoyaoclaw-memory-distill/
├── SKILL.md                    # the skill itself (workflow Steps 1-7)
├── templates/
│   ├── distill-config.json     # distill config template
│   ├── MEMORY.md               # long-term memory structure template
│   └── AGENTS-memory-safety.md # memory safety rules (append to AGENTS.md)
├── docs/
│   └── DESIGN.md               # design document
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
- 📚 **xiaoyaoclaw-kb-retriever** (knowledge base retriever): local KB retrieval — hierarchical data_structure.md index navigation + progressive retrieval over md/pdf/xlsx, zero dependencies, Windows & macOS ready. <https://github.com/dtsola/xiaoyaoclaw-kb-retriever>
- 🩹 **xiaoyaoclaw-workspace-auditor**: read-only workspace health check — 5 categories, graded report with fix suggestions, zero-dependency, never modifies files. <https://github.com/dtsola/xiaoyaoclaw-workspace-auditor>
- 🗂️ **xiaoyaoclaw-task-progress-tracker** (task progress tracker): directory as container, PROGRESS.md as progress — lifecycle management for tasks/ and projects/ (status + progress log + document index). <https://github.com/dtsola/xiaoyaoclaw-task-progress-tracker>
- 📎 **xiaoyaoclaw-web-clipper**: save any web page as clean local Markdown with frontmatter — dual-engine extraction (readability + trafilatura fallback), Chinese-safe filenames, batch clipping with dedup; output lands in knowledge/clippings/ ready for kb-retriever indexing. <https://github.com/dtsola/xiaoyaoclaw-web-clipper>
- 🤝 **xiaoyaoclaw-agent-orchestrator** (collaboration layer): on top of the ecosystem — split, dispatch, track, aggregate, retry.<https://github.com/dtsola/xiaoyaoclaw-agent-orchestrator>
- 📊 **xiaoyaoclaw-usage-report**: parse session JSONL to answer how long each task took, which tools/skills/models were used, and how many tokens were consumed — zero dependency, local only, token is the primary metric. <https://github.com/dtsola/xiaoyaoclaw-usage-report>
- 🎛️ **xiaoyaoclaw-commander** (cross-tool commander, **command layer**): command your XiaoyaoClaw/OpenClaw multi-agent system from any Agent Skills tool (Claude Code / Codex / OpenCode / Trae / DSH). <https://github.com/dtsola/xiaoyaoclaw-commander>
- 🔍 **xiaoyaoclaw-seo-skill** (SEO skill): analyze & optimize website search visibility — audit (technical SEO) / page / content / schema / geo (AI search, AEO/GEO) workflows + zero-dependency audit script, cross-tool ready. <https://github.com/dtsola/xiaoyaoclaw-seo-skill>

## 