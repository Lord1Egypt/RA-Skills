---
name: repo-explainer
description: |
  Decode a GitHub repository **or a local code directory** into a
  non-developer-friendly report, delivered as BOTH a polished HTML page
  AND a Markdown document. Given either a GitHub repo URL or a local
  directory path, this skill prepares the source (shallow-clone for URLs,
  in-place for local paths), scans the ACTUAL source code (not just
  README), and produces two synchronized reports containing: project
  overview, tech stack table, architecture diagram, key module table,
  main user-flow sequence diagram, API/CLI surface table, third-party
  dependency table, and a "what this project actually does in plain
  language" section. The HTML is themed and print-ready; the Markdown
  embeds native Mermaid blocks and pastes cleanly into Feishu / Notion /
  GitHub. Every conclusion is backed by `path:line` references — for
  GitHub URLs (and local clones with a github remote), references render
  as clickable permalinks anchored to the commit SHA; for non-git local
  dirs they render as monospace text.

  TRIGGER WHEN the user gives a `github.com/<owner>/<repo>` URL **OR**
  a local directory path (absolute / relative / `~`-prefixed) AND asks
  any of: "解读这个项目"、"分析这个仓库"、"分析这个目录"、"讲讲这个 GitHub 项目"、
  "帮我看下这个 repo / 这个文件夹做什么"、"explain this repo"、
  "analyze this github project"、"analyze this folder"、
  "what does this repository do"、"understand this codebase"、
  "画一下这个项目的架构"。

  DO NOT TRIGGER for: private/internal GitLab URLs, single-file gists,
  or when the user only wants to run/install the project (not understand
  it). Local-directory mode IS in-scope — including monorepos
  (use `--subpath`) and not-yet-pushed work-in-progress checkouts.
---

# repo-explainer

## Mission

Turn a GitHub repo URL into a self-contained HTML report that a
**non-developer** (PM, designer, manager) can read and walk away
understanding:

1. What the project does (in plain language)
2. Who it is for and what problem it solves
3. How it is built (tech stack + architecture)
4. What the key modules are and how they interact
5. What the main user flow looks like
6. What external dependencies it relies on

**Hard rule**: every claim must be grounded in actual source code, not
just the README. Cite `path:line` for each non-trivial conclusion.

## Inputs

The skill accepts **either** of two source forms:

1. **GitHub URL** — `https://github.com/<owner>/<repo>` (with optional
   `/tree/<branch>` suffix). The repo is shallow-cloned into
   `./workspace/<owner>__<repo>/`.
2. **Local directory path** — absolute, relative, or `~`-prefixed.
   Analyzed in-place; nothing is cloned or copied. If the directory is a
   git checkout whose `origin` (or first available remote) points at
   github.com, the owner / repo / branch / commit SHA are auto-recovered
   so `path:line` evidence still renders as clickable permalinks. If
   not, evidence renders as monospace text and the report still works.

Optional:

- **`--subpath`** — focus on a sub-directory (for monorepos), e.g.
  `packages/core`. Applies to both modes.
- Audience hint — `pm` | `designer` | `engineer` (default `pm`).

If the user gives a non-GitHub URL (and not a local path), refuse
politely and point at the scope limitation.

## Workflow

Execute the following 6 stages **in order**. Each stage has a dedicated
script under `scripts/`. Do NOT skip stages.

### Stage 1 — Fetch

```bash
# Remote mode — shallow-clone a public GitHub repo
python3 scripts/fetch_repo.py <github_url> [--subpath <path>]

# Local mode — analyze a directory in-place (auto-detected when the
# argument is an existing path; force with --local for ambiguous cases)
python3 scripts/fetch_repo.py <local_dir> [--subpath <path>] [--local]
```

The script auto-detects the mode:

- Argument starts with `http://` / `https://` and contains `github.com`
  → **remote mode** (clone)
- Argument is an existing local directory → **local mode** (in-place)
- Otherwise → fall back to URL parser (which will refuse non-GitHub URLs)

**Remote mode** behavior:

- Shallow-clone (`--depth=1`) to `./workspace/<owner>__<repo>/`
- Hard cap repo size at **500 MB**; if exceeded, abort and ask the user
  to pick a sub-path
- Capture default branch, latest commit SHA, repo description, star
  count, primary language (via GitHub REST API, no auth needed for public
  repos but works with `GH_TOKEN` if set)

**Local mode** behavior:

- Resolve the path (absolute / relative / `~`-prefixed); reject if not a
  directory
- Apply the same 500 MB size cap (excluding `.git`, `node_modules`,
  `venv`, `__pycache__`, `dist`, `build`, `target`)
- Try `git -C <path>` for: `HEAD` SHA, current branch, `origin` remote.
  If the remote URL matches `github.com/<owner>/<repo>(.git)?`, owner /
  repo / branch / commit_sha are populated so downstream `path:line`
  evidence becomes clickable permalinks identical to remote mode.
- If the directory is not a git repo, all four GitHub coordinates are
  left null — the renderers degrade evidence to monospace text and the
  hero shows a 📁 `<local-path>` badge instead of a repo link.

The output `meta.json` schema is identical across both modes; only the
`mode` field (`"remote"` / `"local"`) and the optional null-ness of
owner / repo / branch / commit_sha distinguish them.

### Stage 2 — Scan

```bash
python3 scripts/scan_structure.py ./workspace/<owner>__<repo>/
```

Produces `scan.json` containing:

- Directory tree (depth ≤ 4, files counted per dir)
- Language breakdown (lines of code per language, via simple extension map)
- Manifest files detected (`package.json`, `pyproject.toml`, `go.mod`,
  `pom.xml`, `Cargo.toml`, `Gemfile`, `composer.json`, `requirements.txt`,
  `Dockerfile`, `docker-compose.yml`, CI YAMLs)
- Parsed dependencies from each manifest
- Entry-point candidates (`main.*`, `index.*`, `app.*`, `cmd/`, `bin/`,
  `cli.*`, plus framework-specific routes like `routes/`, `pages/`,
  `controllers/`)
- README excerpts (first 300 lines)

### Stage 3 — Analyze

```bash
python3 scripts/analyze_modules.py ./workspace/<owner>__<repo>/ scan.json
```

Produces `analysis.json` containing:

- **Top-N modules**: ranked by (a) inbound import count, (b) LOC,
  (c) presence in entry-point graph
- For each top module: file paths, exported symbols (best-effort regex
  per language), one-line "what it does" guess from docstring/comment
- **API surface**: HTTP routes, CLI commands, exported public functions
- **Data models**: classes/structs that look like entities (heuristic:
  fields-only, named like nouns)
- **External calls**: detected SDK usage (e.g. `boto3`, `openai`, `redis`,
  `kafka`, `axios`, `fetch`) with `path:line` evidence

### Stage 4 — Synthesize

```bash
python3 scripts/synthesize_summary.py analysis.json scan.json > summary.json
```

Calls the LLM (via Mira's built-in capability — **the orchestrating agent
performs this step in-context**, the script just prepares a structured
prompt payload). The agent must produce JSON conforming to
`templates/summary.schema.json`:

```json
{
  "project_name": "...",
  "one_liner": "≤30 字白话定位",
  "who_for": "目标用户群体",
  "problem_solved": "...",
  "core_value": "...",
  "tech_stack": [{"layer": "前端|后端|数据|基础设施", "items": ["..."]}],
  "key_models": [{"name": "PolicyAST", "path": "src/core/types", "purpose": "...", "key_fields": "id, rules[], snapshot_id", "evidence": "path:line"}],
  "key_modules": [{"name": "...", "path": "...", "responsibility": "...", "principle": "实现原理一句话", "subflow": ["步骤1","步骤2"], "evidence_list": ["path:line", "path:line"]}],
  "limitations": [{"title": "...", "detail": "...", "category": "performance|security|scalability|usability|compatibility|documentation|test_coverage|architecture|other", "severity": "low|medium|high", "evidence": "path:line 或 issue 链接,可空"}],
  "main_flow": [{"step": 1, "actor": "用户|系统", "action": "...", "evidence": "path:line"}],
  "api_surface": [{"type": "HTTP|CLI|SDK", "signature": "...", "purpose": "...", "evidence": "path:line"}],
  "dependencies": [{"name": "...", "purpose": "...", "criticality": "核心|辅助"}],
  "highlights": ["特色 1", "特色 2", "..."],
  "architecture_mermaid": "graph TD\n  ...",
  "sequence_mermaid": "sequenceDiagram\n  ...",
  "glossary": [{"term": "...", "plain": "白话解释"}]
}
```

**Rules for the agent during synthesis**:

- Every `evidence` field MUST be a real `path:line` from the scanned repo
- Mermaid node labels MUST use business language ("登录请求"),
  NOT class names ("AuthController")
- **Mermaid safety (HARD RULE — violating this breaks rendering on Feishu /
  GitHub / Notion / Mermaid Live)**. Both `architecture_mermaid` and
  `sequence_mermaid` MUST follow:
  - **No HTML-confusable chars** in node labels or sequence message text:
    forbid `<` `>` `"` `'` (use full-width 「」 or remove); replace
    `path/file.ts` style with `path file.ts` or `file 文件`.
  - **No code-fence-confusable chars**: forbid backticks ` ` `, pipes `|`
    inside labels (Markdown table parser eats them).
  - **No `rect rgb(...)` colour blocks inside `sequenceDiagram`** — Feishu /
    Notion Mermaid renderers commonly fail on them. Use `Note over X,Y:
    阶段 N 描述` to mark phases instead.
  - **Quote labels with non-ASCII**: in `graph TD`, wrap labels containing
    Chinese / spaces in double quotes — `A["登录请求"]`, not `A[登录请求]`.
    In `sequenceDiagram`, use `participant ALIAS as 显示名` (NO quotes).
  - **Replace these symbols inside labels / messages**: `<` `>` → 全角
    `〈 〉` or remove; `&` → `加`; em-dash `—` → space; slash `/` inside
    message text → space (slash in `participant alias` is fine).
  - **One statement per line**, no inline `;`. Indent body by 2-4 spaces.
  - **Self-check before emitting**: paste your mermaid into
    https://mermaid.live mentally — if any line contains the forbidden
    chars above, rewrite it.
- `glossary` MUST contain every technical term that appears in
  `one_liner` / `core_value` / `highlights`
- **`key_models`**: extract core domain/data structs/classes/protobuf/schemas
  (e.g. `Alert`, `PolicyAST`, `Snapshot`, `User`). These are the nouns the
  project moves around. Render BEFORE `key_modules` so readers learn the
  "what" before the "how". Keep 5-12 entries.
- **`key_modules`**: keep `principle` (核心原理 1-2 句) and `subflow`
  (3-6 步关键流程) for each module — readers should leave understanding
  not just what each module does but HOW it works.
- **`limitations`**: MUST include 4-8 entries. Sources allowed:
  (a) TODO/FIXME/XXX/HACK comments grep'd from source,
  (b) open issues / known issues in README,
  (c) obvious architectural gaps (e.g. no rate limiting on public API,
      single-node only, no auth on /metrics, hardcoded secrets in tests,
      missing test coverage, deprecated dependency).
  Be honest and specific — generic items like "需要更多测试" are forbidden.
  If evidence cannot be cited, leave `evidence` empty rather than fake.
- If a field cannot be confidently filled, leave empty string —
  never fabricate

### Stage 5 — Render (BOTH formats, in parallel)

The pipeline MUST produce **both** an HTML report and a Markdown report
from the same `summary.json` — never just one. Markdown is for embedding
in Feishu / Notion / GitHub READMEs / chat; HTML is for sharing /
printing / standalone viewing.

```bash
# 5a · HTML (themed, single-file, interactive)
python3 scripts/render_html.py summary.json \
    --meta_json meta.json \
    --file_count "$(jq '.structure.total_files' scan.json)" \
    --theme midnight \
    > report.html

# 5b · Markdown (Mermaid-native, GitHub/Feishu-friendly)
python3 scripts/render_markdown.py summary.json \
    --meta_json meta.json \
    --file_count "$(jq '.structure.total_files' scan.json)" \
    > report.md
```

Both renderers share the same section order and the same evidence-link
contract:

- Sections (identical in both formats): Hero (one_liner + project_name +
  repo link) → TL;DR (who_for / problem / value) → Tech Stack table →
  Architecture diagram (Mermaid) → **Key Models table** → Key Modules
  detail cards → Main Flow (sequence diagram) → API Surface table →
  Dependencies table → Highlights → **Limitations / 待优化点** → Glossary
- Every `evidence: path:line` rendered as a clickable link to
  `https://github.com/<owner>/<repo>/blob/<sha>/<path>#L<line>`
- HTML extras: 3 themes (midnight / light / terminal), `@media print`
  rules, drop-shadow + auto-classified subgraph colors + legend,
  localStorage theme persistence
- Markdown extras: ```` ```mermaid ```` fenced blocks (rendered natively
  by GitHub / GitLab / Obsidian / Typora / Bear / VS Code preview),
  shields.io badges in the hero, severity emoji (🔴 high / 🟠 medium /
  🟢 low) in the limitations section

### Stage 6 — Deliver

- Upload **both** `report.html` AND `report.md` via
  `mcp__runtime__upload_file` — never just one
- Return to user: ① uploaded HTML URL ② uploaded Markdown URL ③ brief
  3-line summary (project name, one-liner, top-3 highlights) ④ note
  that they can click any `path:line` link to verify, and that the
  Markdown version can be pasted directly into Feishu / Notion / GitHub
  issues

## Failure Modes

| Symptom | Action |
|---|---|
| 404 from GitHub API | Tell user repo is private/non-existent; stop |
| Clone >500 MB | Ask user to pick a sub-path; offer top-3 sub-dirs by size |
| Zero recognized manifests AND zero code files | Report "not a code repo" and stop |
| LLM synthesis returns invalid JSON | Retry once with schema reminder; if still fails, fall back to a degraded report (skip the broken section, mark it `[未能可靠生成]`) |
| Mermaid render error in HTML | The HTML uses Mermaid 10+; on parse error the diagram block shows the raw text instead — DO NOT block the rest of the report. The Markdown report is unaffected since GitHub/Feishu render Mermaid independently. |
| Markdown render error | The Markdown renderer is pure Python with no runtime deps and emits raw fenced ```mermaid blocks — only fails on invalid summary.json. If `render_markdown.py` fails, still deliver the HTML; report markdown error to the user. |

## Non-Goals (explicit)

- Not a security auditor
- Not a code review tool
- Not a runner/installer
- Not a comparison-with-other-projects tool (use `competitive-analysis`)
- Not a deep call-graph tracer (out of MVP scope)

## Examples

**Trigger — GitHub URL**:
> 帮我解读一下 https://github.com/tiangolo/fastapi 这个项目

**Trigger — local directory**:
> 帮我分析下 ~/code/my-side-project 这个目录在做什么

> explain this folder /Users/me/work/checkout-service

**Not a trigger** (private/internal GitLab, out of scope):
> 帮我分析下 https://code.byted.org/some/private/repo

**Not a trigger** (only wants to run, not understand):
> 这个 github 项目怎么跑起来
