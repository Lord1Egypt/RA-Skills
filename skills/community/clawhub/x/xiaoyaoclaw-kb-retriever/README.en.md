# OpenClaw Knowledge Base Retriever 📚

<div align="center">
  <a href="README.md">🇨🇳 中文</a> | <strong>🌐 English</strong>
</div>

<p align="center">
  <img src="./assets/readme/hero.svg" width="100%" alt="OpenClaw Knowledge Base Retriever — local knowledge-base retrieval over md/pdf/xlsx: hierarchical data_structure.md index navigation + progressive search, core retrieval zero-dependency">
</p>

> Local knowledge-base retrieval & QA over a local directory (md/pdf/xlsx) — hierarchical index navigation + progressive search, core retrieval zero-dependency (PDF/Excel need on-demand pip packages), Windows & macOS ready.
> 本地知识库检索器——分层索引导航 + 渐进式检索，核心检索零依赖零 API key，Windows / macOS 双平台（PDF/Excel 处理按需安装 Python 包）。

![license](https://img.shields.io/badge/license-MIT-green)
[![ClawHub downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fclawhub.ai%2Fapi%2Fv1%2Fskills%2Fxiaoyaoclaw-kb-retriever&query=skill.stats.downloads&label=ClawHub%20downloads&color=blue)](https://clawhub.ai/dtsola/skills/xiaoyaoclaw-kb-retriever)

## Why you need it

When an OpenClaw agent faces a local knowledge base (docs / reports / data directories), common pain points:
- ❌ **Whole-file reads**: huge PDFs/Excels dumped into context, token explosion
- ❌ **Blind searching**: no index navigation, full-tree scans are slow and noisy
- ❌ **Wrong format handling**: PDF/Excel processed with the wrong tools
- ❌ **Cloud dependency**: RAG solutions need embedding models or external API keys, privacy at risk

This skill solves all of it: **hierarchical index navigation + progressive retrieval + learn-before-process + fully local, no cloud API.**

## Features

- 🗂️ **Hierarchical index navigation**: each directory carries a `data_structure.md`; navigate the index tree instead of scanning everything
- 🔍 **Progressive retrieval**: grep/Select-String to locate → windowed reads (offset/limit) → up to 5 bounded rounds, never whole-file loads
- 📖 **Learn-before-process**: PDF/Excel handling is gated on reading the right references first
- 🐍 **Unified Python pipeline**: PDF via pdfplumber — identical behavior on Windows & macOS
- 🔒 **Fully local, no cloud API**: no vector index, no cloud API, sensitive data never leaves your machine (PDF/Excel use on-demand pip packages from an allowlist)
- 🏗️ **One-command index build**: `python build_index.py <kb>` auto-generates the index skeleton
- 🧭 **Sourced answers**: every answer cites file + location, verifiable

## Install

```bash
# ClawHub (recommended)
clawhub install xiaoyaoclaw-kb-retriever

# Or manual from GitHub
git clone https://github.com/dtsola/xiaoyaoclaw-kb-retriever
# Put SKILL.md, references/, scripts/ into your skills directory
```

## Usage

1. Put the skill into OpenClaw's skills directory
2. Prepare your knowledge base: put files into `knowledge/` in your workspace (or point to any path in conversation)
3. Build the index (optional — this writes files):

> ⚠️ **This step writes to disk**: `build_index.py` creates or overwrites `data_structure.md` inside your knowledge base (with `--force` it overwrites existing indexes). It is a maintenance action, not retrieval — run it only when you actually want an index, and every write target is real-path checked so a symlink cannot push a write outside the knowledge base.

> 🛡️ **Bounded both ways**: reads are confined the same way — search/listing resolves each entry's real path and **skips and counts** anything that escapes the knowledge-base root, so no file outside it is ever read. Source documents handed to the PDF helpers must be **real paths**: any symlink in the path is refused outright rather than followed.

```bash
python scripts/build_index.py knowledge
```

4. Ask your agent: "**query xxx from the knowledge base**" — it will locate the KB, navigate the index, retrieve progressively, and answer with sources.

## 🚀 Quick start (3 steps, 5 minutes)

### Step 1: Install the skill

```bash
clawhub install xiaoyaoclaw-kb-retriever
```

Done — it's now in your agent's skill list. No API keys, no services to configure.

### Step 2: Drop in your files + build the index

Put your documents into a `knowledge/` directory in your workspace (create it if missing). md / pdf / xlsx all work:

```
your-workspace/
└── knowledge/          ← your files live here
    ├── product-docs/
    ├── sales-reports/
    └── meeting-notes/
```

Then run one command to generate the "directory map" (index — optional; **it writes files**):

```bash
python scripts/build_index.py knowledge
```

> It works without the index too, but with it the agent finds things much faster and more accurately.

### Step 3: Ask with your knowledge-base path

No commands to memorize — but always name the knowledge base so the skill knows what to search:

> "From the knowledge base `knowledge/`, what are the key numbers in the 2024 sales report?"
> "Look up our pricing strategy in `knowledge/`."

> Requests that never name a knowledge base are **not** handled by this skill — it asks for the path first instead of guessing.

The agent will: **read the index → locate relevant files → read only what's needed → answer with sources**.

## When this skill triggers (and when it does not)

**Triggers** — the user names a knowledge base **and** a retrieval/maintenance intent:
- "query xxx from the knowledge base `<path>`" / "does `<path>` have anything about xxx"
- "retrieve / look up / answer from my local knowledge base `<path>`"
- "build (or refresh) the index for `<path>`", "convert `xxx.pdf` under `<path>` to text" (write actions — confirm first)

**Does not trigger** — examples:
- A vague "look something up for me" **without** a knowledge-base path or a clear retrieval intent → ask for the path first; never pick a directory on your own
- General chat, coding, summarizing this conversation, explaining concepts
- Web scraping or internet search (this skill is offline; use `xiaoyaoclaw-web-clipper` for pages)
- Memory distillation or workspace restructuring (use `xiaoyaoclaw-memory-distill` / `xiaoyaoclaw-workspace-initializer`)
- "See what's on my computer" style open-ended browsing → not supported; only the KB root the user names explicitly

**Language**: the skill is language-optional — it answers in Chinese by default and follows the user's language
otherwise. Example text, the index template and the README artwork contain Chinese as sample/brand material;
index section headings (Purpose / Files / Coverage) are English either way.


### Daily habits

| Scenario | Action |
|---|---|
| First-time setup | `python build_index.py knowledge` |
| New files added | re-run build_index (skips existing, `--force` to rebuild) |
| Custom directory | say "use ./docs as the knowledge base" |
| Large PDFs | auto page-range extraction (extract_pdf_text.py), never whole-file |
## Why not a vector RAG?

| | Vector RAG (qmd / boof / hk101) | **xiaoyaoclaw-kb-retriever** |
|---|---|---|
| Dependencies | embedding models / cloud API keys / local ML | ✅ No cloud services (grep + read + pdfplumber + pandas, on-demand pip) |
| Index | vector index build required | ✅ Lightweight text index, one command |
| Privacy | some upload to cloud | ✅ Fully local |
| Platforms | mostly Unix-oriented | ✅ Windows & macOS first-class |
| Language | English-first | ✅ Bilingual (中文 / English) |
| Context cost | loads index/vectors | ✅ Progressive retrieval, only matched windows |

## Directory structure

```
xiaoyaoclaw-kb-retriever/
├── SKILL.md                    # main skill (OpenClaw-adapted)
├── manifest.json               # compat: openclaw / claude-code / cursor / ...
├── references/
│   ├── pdf_reading.md          # PDF handling (unified Python pipeline)
│   ├── excel_reading.md        # Excel reading
│   └── excel_analysis.md       # Excel analysis
├── scripts/
│   ├── build_index.py          # [highlight] one-command data_structure.md generator
│   └── extract_pdf_text.py     # cross-platform PDF text extraction
├── templates/
│   └── data_structure.md       # index template
├── docs/
│   └── DESIGN.md               # design doc
├── README.md / README.en.md
└── LICENSE
```

## Upstream credit

Forked & adapted from [ConardLi/garden-skills](https://github.com/ConardLi/garden-skills) kb-retriever (MIT):
- **Kept**: hierarchical index navigation, learn-before-process, progressive retrieval, sourced answers
- **Adapted**: OpenClaw tool mapping (read / exec dual-platform commands), unified Python PDF pipeline, one-command index builder, bilingual docs

## License

MIT — use freely, attribution optional.

---

## 🛠️ Custom development?

**Agent & Skills customization, from ¥800.**

- WeChat: `dtsola` (note: **openclaw定制**)
- Scope: OpenClaw multi-agent deployment / workspace standardization / custom Skill development / agent memory systems / knowledge-base setup

## 💬 Join the community

Xiaoyao product family user group — feedback · exchange · suggestions:

<p align="center">
  <img src="./assets/readme/community-qr.png" width="280" alt="XiaoyaoAI user group QR: scan to join, or add WeChat dtsola (note: 加群)">
</p>

<p align="center">Scan to join, or add WeChat <code>dtsola</code> (note: <b>加群</b>)</p>

## Sister projectss

- 🏠 **xiaoyaoclaw-workspace-initializer**: give every agent a "home" — standard directory structure + WORKSPACE.md rules + multi-agent config safety. <https://github.com/dtsola/xiaoyaoclaw-workspace-initializer>
- 🧠 **xiaoyaoclaw-memory-distill**: distill conversations into MEMORY.md + daily logs, solve context overflow. <https://github.com/dtsola/xiaoyaoclaw-memory-distill>
- 🗂️ **xiaoyaoclaw-task-progress-tracker**: directory-as-container, PROGRESS.md-as-card — tasks/ & projects/ lifecycle management. <https://github.com/dtsola/xiaoyaoclaw-task-progress-tracker>
- 🩹 **xiaoyaoclaw-workspace-auditor**: read-only workspace health check — 5 categories, graded report with fix suggestions, zero-dependency, never modifies files. <https://github.com/dtsola/xiaoyaoclaw-workspace-auditor>
- 📎 **xiaoyaoclaw-web-clipper**: save any web page as clean local Markdown with frontmatter — dual-engine extraction (readability + trafilatura fallback), Chinese-safe filenames, batch clipping with dedup; output lands in knowledge/clippings/ ready for kb-retriever indexing. <https://github.com/dtsola/xiaoyaoclaw-web-clipper>
- 🤝 **xiaoyaoclaw-agent-orchestrator** (collaboration layer): on top of the ecosystem — split, dispatch, track, aggregate, retry.<https://github.com/dtsola/xiaoyaoclaw-agent-orchestrator>
- 📊 **xiaoyaoclaw-usage-report**: parse session JSONL to answer how long each task took, which tools/skills/models were used, and how many tokens were consumed — zero dependency, local only, token is the primary metric. <https://github.com/dtsola/xiaoyaoclaw-usage-report>
- 🎛️ **xiaoyaoclaw-commander** (cross-tool commander, **command layer**): command your XiaoyaoClaw/OpenClaw multi-agent system from any Agent Skills tool (Claude Code / Codex / OpenCode / Trae / DSH). <https://github.com/dtsola/xiaoyaoclaw-commander>
- 🔍 **xiaoyaoclaw-seo-skill** (SEO skill): analyze & optimize website search visibility — audit (technical SEO) / page / content / schema / geo (AI search, AEO/GEO) workflows + zero-dependency audit script, cross-tool ready. <https://github.com/dtsola/xiaoyaoclaw-seo-skill>

## 