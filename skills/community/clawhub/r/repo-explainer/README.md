# repo-explainer

**Languages** &nbsp;·&nbsp; **English** &nbsp;·&nbsp; [简体中文](README.zh-CN.md)

> Turn any public GitHub repository **or local code directory** into a beautiful, evidence-backed report — readable by non-developers, trusted by engineers. One run produces an HTML page **and** a Markdown document side-by-side.

`repo-explainer` is a 6-stage command-line pipeline that ingests **either a public GitHub repo URL or a local directory path** and produces two synchronized reports answering:

- What does the project actually do, in plain language?
- Who is it for and what problem does it solve?
- What's the tech stack, architecture, and the key data models?
- What is the main user flow?
- What are the honest limitations and trade-offs?

Every claim is grounded in real source code with `path:line` citations. Every code reference — file paths, directory paths, and `path:line` evidence — is a clickable link that jumps straight to the commit-pinned source on GitHub. For local directories that are git checkouts of a github.com remote, links are auto-anchored to the working-tree commit SHA; for non-git local dirs, evidence renders as monospace text and the report still works.

---

## Table of Contents

- [Features](#features)
- [Demo Gallery](#demo-gallery)
- [Quick Start](#quick-start)
- [Themes](#themes)
- [Configuration](#configuration)
- [Output Examples](#output-examples)
- [Design Principles](#design-principles)
- [Repository Layout](#repository-layout)
- [Roadmap](#roadmap)
- [Known Limitations](#known-limitations)
- [Non-Goals](#non-goals)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Dual output — HTML + Markdown side-by-side.** Every run produces a themed single-file HTML and a portable Markdown document. The Markdown uses native ` ```mermaid ` fenced blocks and renders cleanly on GitHub, GitLab, Feishu, Notion, Obsidian, Typora, and VS Code preview.
- **Every code path is a clickable link.** `path/to/file.ts` jumps to the file; `dir/` jumps to the directory tree; `path/to/file.ts:91` jumps to line 91. URLs are pinned to the commit SHA so they don't rot.
- **Source-grounded.** Scans the actual repo (not just the README). The LLM in Stage 4 receives real paths, real LOC counts, and real SDK import line numbers — never the project's marketing copy.
- **Non-developer friendly.** Mermaid node labels use business language (`登录请求`) rather than class names (`AuthController`). A built-in glossary translates every technical term.
- **3 built-in themes.** Midnight (dark), Light (print-friendly), Terminal (monospace green). One-click switch with `localStorage` persistence.
- **Auto-styled architecture diagrams.** Subgraphs are heuristically grouped and colored, with a matching legend rendered below each diagram.
- **Phased sequence diagrams.** Mermaid sequence with `autonumber` and `Note over` phase markers. Strict safety rules avoid characters that break Feishu / Notion Mermaid renderers.
- **Key Models table.** Extracts the project's core domain types (structs / classes / protobuf) before diving into module internals — readers learn the "what" before the "how".
- **Honest limitations.** Every report includes 4–8 limitation cards tagged with severity (high / medium / low) and category. Generic platitudes like "needs more tests" are forbidden in the prompt.
- **Single-file HTML.** Inline CSS, Mermaid via CDN, print-friendly (`@media print`), no build server required. A small JS click-handler guarantees every code-path link opens in a new tab even inside strict sandboxed iframes (Mira / Lark / Notion preview), without ever stealing the current window.
- **Theme override system.** Drop in a JSON file with just the variables you want to change; it is deep-merged on top of the base theme.

---

## Demo Gallery

The same `summary.json` was rendered into all three HTML themes **and** the portable Markdown — below is what each looks like for [`NousResearch/hermes-agent`](https://github.com/NousResearch/hermes-agent).

> Screenshots are full-width crops of the top of each report (hero + TL;DR + tech stack + architecture diagram). Click any thumbnail to view full size.

### HTML — Midnight (default)

Deep purple ⇄ cyan gradient, intended for on-screen reading.

![Midnight theme preview](https://p-mira-img-sign-sgnontt.byteintl.net/tos-mya-i-xobrcjvdq7/83771931c97a4206b7a0e09e8ae19847.png~tplv-xobrcjvdq7-image-jpeg.jpeg?lk3s=3523e930&x-orig-authkey=miraorigin&x-orig-expires=1781532000&x-orig-sign=F3QPAqxkTz7GCfyGwb5QK8zQapc%3D)

### HTML — Light

White background, blue accent, print-friendly. Best for embedding in business reports or exporting to PDF.

![Light theme preview](https://p-mira-img-sign-sgnontt.byteintl.net/tos-mya-i-xobrcjvdq7/c9c398f8c7ac4223854a92efcd26b516.png~tplv-xobrcjvdq7-image-jpeg.jpeg?lk3s=3523e930&x-orig-authkey=miraorigin&x-orig-expires=1781532000&x-orig-sign=845VzIlqktSCuSQ1LQau4WibNlI%3D)

### HTML — Terminal

Black background, neon-green monospace. Hacker aesthetic; pairs well with dark-mode IDE themes.

![Terminal theme preview](https://p-mira-img-sign-sgnontt.byteintl.net/tos-mya-i-xobrcjvdq7/f473b19c3caa436487d1ae3662788358.png~tplv-xobrcjvdq7-image-jpeg.jpeg?lk3s=3523e930&x-orig-authkey=miraorigin&x-orig-expires=1781532000&x-orig-sign=tzFdGGvCrCJkK4YPiPWe%2F2hgNk8%3D)

### Markdown — rendered on GitHub

The exact same content, generated by `render_markdown.py`, rendered with GitHub-flavored styling and live Mermaid diagrams. Paste it into Feishu / Notion / Obsidian and it renders identically.

![Markdown rendered preview](https://p-mira-img-sign-sgnontt.byteintl.net/tos-mya-i-xobrcjvdq7/6bddd00cd39d4597924ce04d9d2f6d18.png~tplv-xobrcjvdq7-image-jpeg.jpeg?lk3s=3523e930&x-orig-authkey=miraorigin&x-orig-expires=1781532000&x-orig-sign=BRJIUtLNlsf20pFZgqzbgh52PPc%3D)

Every code-path and `path:line` reference in all four outputs is a clickable link anchored to the commit SHA, so readers can verify any claim in one click.

---

## Quick Start

`repo-explainer` is shipped as a portable **Agent Skill package** (`repo-explainer.zip`) — the layout (`SKILL.md` at root, scripts/ and templates/ alongside) is compatible with Mira, Claude Code, Codex, and any other agent host that follows the Anthropic-style skills convention. Pick whichever you already use, or fall back to the local CLI.

### Option A — Install as an Agent Skill (recommended)

Download the latest skill package: **`repo-explainer.zip`** (released alongside this repo). Then install it into your agent of choice:

#### A1. Mira

- **UI**: open any chat → `/find-skills` → **Install from file** → select `repo-explainer.zip`.
- **Programmatic** (from inside another agent run):
  ```text
  skill_write(action="enable", skill_type="custom",
              file_uri="<URL-or-tos-uri-of-the-zip>",
              confirmed=false)
  # review the preview, then call again with confirmed=true
  ```

#### A2. Claude Code

Claude Code auto-discovers any skill folder under `~/.claude/skills/`. Unpack the zip there and the skill is live on the next session:

```bash
mkdir -p ~/.claude/skills
unzip -d ~/.claude/skills/ repo-explainer.zip
# verify the layout
ls ~/.claude/skills/repo-explainer/          # → SKILL.md  scripts/  templates/
```

Then start a Claude Code session and trigger it:

> /skills                                   # list to confirm "repo-explainer" appears
> explain this repo https://github.com/tiangolo/fastapi

For project-scoped install instead of user-global, drop the folder into `<project>/.claude/skills/repo-explainer/` — same layout, just visible only inside that repo.

#### A3. Codex CLI

Codex follows the same on-disk convention. Unpack into the Codex skills directory:

```bash
mkdir -p ~/.codex/skills
unzip -d ~/.codex/skills/ repo-explainer.zip
# (or, for repo-local: <project>/.codex/skills/repo-explainer/)
```

Then in any Codex chat:

> @repo-explainer https://github.com/NousResearch/hermes-agent

#### A4. Try it

Once installed in any of the hosts above, trigger from chat with **a GitHub URL or a local directory path**:

> 解读这个项目 https://github.com/tiangolo/fastapi
>
> explain this repo https://github.com/NousResearch/hermes-agent
>
> 分析下这个目录 ~/code/my-side-project
>
> explain this folder /Users/me/work/checkout-service

The skill auto-runs all 6 stages and returns two artifacts: the polished HTML report and the paste-anywhere Markdown report. No local Python setup needed — the agent's sandbox provides `python3`, `git`, `jq`, and an LLM in-context.

### Option B — Run the pipeline locally (CLI)

Useful for batch jobs, CI integration, or if you don't have Mira.

> Prerequisites: **Python 3.9+** (stdlib only), **git**, **jq**, and an LLM you can prompt via the command line.

```bash
# 1. Get the package
unzip repo-explainer.zip            # or: git clone <this-repo>
cd repo-explainer/

# 2. Run the 6-stage pipeline against any public GitHub URL …
TARGET="https://github.com/tiangolo/fastapi"

#    … OR against a local directory (auto-detected; force with --local
#    if the path is ambiguous). Owner / repo / branch / commit SHA are
#    auto-recovered from .git/config when the dir is a git checkout, so
#    path:line evidence stays clickable.
# TARGET="/home/me/code/my-side-project"
# TARGET="~/work/checkout-service"

# Stages 1–3 are deterministic Python — no LLM, stdlib only
python3 scripts/fetch_repo.py      "$TARGET"                                > meta.json
python3 scripts/scan_structure.py  "$(jq -r .local_path meta.json)"         > scan.json
python3 scripts/analyze_modules.py "$(jq -r .local_path meta.json)" scan.json > analysis.json

# Stage 4 — synthesis (the only step that needs an LLM)
#   Feed analysis.json + scan.json to your LLM using
#   templates/summary.schema.json as the strict output contract.
#   Save the result as summary.json.

# Stage 5a — themed HTML (single self-contained file)
python3 scripts/render_html.py summary.json \
        --meta_json   meta.json \
        --file_count  "$(jq '.structure.total_files' scan.json)" \
        --theme       midnight \
        > report.html

# Stage 5b — portable Markdown (Mermaid-native, paste-anywhere)
python3 scripts/render_markdown.py summary.json \
        --meta_json   meta.json \
        --file_count  "$(jq '.structure.total_files' scan.json)" \
        > report.md
```

Open `report.html` in any browser, or paste `report.md` directly into GitHub, GitLab, Feishu, Notion, or Obsidian.

> **Tip** — only Stage 4 needs an LLM. The other five stages are deterministic Python and run offline. There are no `pip` dependencies — the entire pipeline uses only the Python standard library.

---

## Themes

Three themes ship in `templates/themes.json`. Each carries:

- 30+ CSS variables (background, foreground, accent, hero gradient, diagram bg/border/shadow, etc.)
- A full set of Mermaid `themeVariables` (primaryColor, clusterBkg, actorBkg, loopTextColor, edgeLabelBackground, …)
- A 5-color palette for architecture nodes: `user / core / module / kernel / store`

| Theme | When to use | Vibe |
|---|---|---|
| `midnight` | Default; on-screen reading | Deep purple ⇄ cyan gradient |
| `light` | Print / business documents | White background, blue accent |
| `terminal` | Hacker aesthetic | Black background, neon green monospace |

Switch at render time:

```bash
python3 scripts/render_html.py summary.json --meta_json meta.json --theme light > report.html
```

Or click the theme toggle in the top-right corner of the report — Mermaid re-renders live and the choice is remembered via `localStorage`.

---

## Configuration

### Custom theme override

Want your brand color without rewriting all 30 variables? Drop the deltas in a JSON file:

```json
{
  "css_vars": {
    "--bg": "#fdf6e3",
    "--fg": "#073642",
    "--accent": "#268bd2",
    "--hero-grad": "linear-gradient(135deg, #268bd2 0%, #2aa198 100%)"
  },
  "fonts": {
    "primary": "'Source Sans Pro', sans-serif"
  },
  "mermaid": {
    "themeVariables": { "primaryColor": "#eee8d5", "lineColor": "#586e75" }
  },
  "diagram_class_palette": {
    "user":   { "fill": "#eee8d5", "stroke": "#268bd2", "color": "#073642" },
    "core":   { "fill": "#fdf6e3", "stroke": "#6c71c4", "color": "#073642" },
    "module": { "fill": "#eee8d5", "stroke": "#2aa198", "color": "#073642" },
    "kernel": { "fill": "#fdf6e3", "stroke": "#dc322f", "color": "#073642" },
    "store":  { "fill": "#eee8d5", "stroke": "#859900", "color": "#073642" }
  }
}
```

Then apply on top of the base theme of your choice (here Midnight):

```bash
python3 scripts/render_html.py summary.json \
        --meta_json meta.json \
        --theme midnight \
        --theme-override my-brand.json \
        > report.html
```

The override is deep-merged onto the base theme, so you never have to copy the whole file.

### CLI reference

**HTML renderer** (`render_html.py`)

```text
python3 scripts/render_html.py <summary.json> [OPTIONS]

  --meta_json <path>          (required) The meta.json from Stage 1
  --file_count <int>          Total file count, shown in the hero
  --theme <name>              midnight (default) | light | terminal
  --theme-override <path>     JSON file with overrides to deep-merge
```

**Markdown renderer** (`render_markdown.py`)

```text
python3 scripts/render_markdown.py <summary.json> [OPTIONS]

  --meta_json <path>          (required) The meta.json from Stage 1
  --file_count <int>          Total file count, shown in the hero badge
```

The Markdown renderer is pure Python stdlib — no external dependencies, no themes (rendering colors are left to the host). Output is paste-ready for any platform that supports GitHub-flavored Markdown plus ` ```mermaid ` fenced blocks.

---

## Output Examples

A single run produces two synchronized artifacts from the same `summary.json`:

| Format | When to use | Renders best on |
|---|---|---|
| **`report.html`** | Sharing a polished link, printing, embedding in a dashboard, archiving | Any modern browser (offline-capable, single file) |
| **`report.md`** | Pasting into a wiki / chat / issue tracker, code-reviewing the report in a PR, version-controlling alongside source | GitHub, GitLab, Feishu, Notion, Obsidian, Typora, VS Code preview |

Both share the same section order, the same `path:line` evidence links, and the same Mermaid source.

### What's in a report

Hero (project name + one-liner + repo metadata) → TL;DR cards → tech stack table → architecture diagram → **key models** table → **per-module detail** (responsibility / principle / sub-flow / evidence) → main-flow sequence diagram → API surface → dependencies → highlights → **limitations overview + details** → glossary.

### Link conventions

| Reference shape | Resolves to | Example URL |
|---|---|---|
| `src/cli.ts` | `/blob/<sha>/src/cli.ts` | Jumps to the file |
| `src/ingest/` | `/tree/<sha>/src/ingest` | Jumps to the directory listing |
| `src/cli.ts:91` | `/blob/<sha>/src/cli.ts#L91` | Jumps to line 91 |

In Markdown the visible text is the path itself (no inline-code backticks inside the link text — they break paste behavior in some hosts). In HTML, every code reference carries a small `↗` icon and underlines on hover so it's visually obvious it's a link.

---

## Design Principles

### 1. Source-grounded, never marketing-driven

Stages 2 and 3 read the actual source files; the LLM in Stage 4 receives real paths, real LOC counts, and real SDK import line numbers — never the repository's README copy. Every conclusion ships with a clickable `path:line` link to the commit-pinned source.

### 2. Readable by non-developers, trusted by engineers

Mermaid node labels enforce business language (`告警事件` over `AlertEventDto`). The glossary translates every jargon term. Engineers retain the option to drill in via the principle + evidence list on each module card.

### 3. Beauty is trust

Three layers of visual polish make readers want to open the second report:

- Mermaid `themeVariables` cover 30+ fine-grained colors per theme
- Subgraph nodes are auto-classified into 5 colored groups with a matching legend
- The diagram container uses a radial gradient background, a 3px top brand bar, an SVG drop-shadow filter, rounded node corners, and dashed cluster borders

### 4. Every reference is clickable, every click survives

Code paths and `path:line` evidence are all anchored to the commit SHA so links never rot. The HTML uses a JavaScript click-handler that calls `window.open(href, '_blank')` (with `top.location` and same-frame fallbacks) so every link opens cleanly in a new tab, even inside Mira / Lark / Notion preview iframes where a plain `target="_blank"` would be silently blocked — and never replaces the current page. The Markdown drops backticks inside link text so Feishu / Notion paste handlers render the visible label correctly instead of leaking the raw URL.

### 5. Honest limitations are mandatory

The Stage 4 schema requires 4–8 `limitations` per report. Sources allowed: TODO/FIXME/XXX comments grepped from source, known issues in README, or obvious architectural gaps. Generic platitudes like "needs more tests" are explicitly forbidden in the prompt.

---

## Repository Layout

```
repo-explainer/
├── README.md                     # This file
├── SKILL.md                      # Agent-skill manifest + workflow contract
├── scripts/
│   ├── fetch_repo.py             # Stage 1 — shallow clone (or in-place local dir) + GitHub REST metadata
│   ├── scan_structure.py         # Stage 2 — tree / LOC / manifests
│   ├── analyze_modules.py        # Stage 3 — module ranking / SDK / routes
│   ├── render_html.py            # Stage 5a — themed single-file HTML
│   └── render_markdown.py        # Stage 5b — paste-anywhere Markdown
└── templates/
    ├── summary.schema.json       # Stage 4 LLM output contract (JSON Schema draft-07)
    └── themes.json               # 3 built-in themes + 5-class diagram palette
```

---

## Roadmap

- **Monorepo deep-scan** — when the root contains a single `src/`, drill one level deeper instead of collapsing `top_modules`
- **GitLab / Bitbucket adapters** — currently GitHub only
- **`--subpath` auto-suggest** — when a repo exceeds 500 MB, suggest the top-3 largest sub-directories
- **SDK dictionary expansion** — `analyze_modules.py:SDK_HINTS` is hardcoded; missing entries (eBPF, MCP, Qwen, …) silently drop
- **PDF / PNG export** — bundle a headless renderer
- **i18n** — currently the prompt and schema fields favor Chinese output; English / Japanese / Korean variants planned

---

## Known Limitations

| # | Limitation | Workaround |
|---|---|---|
| 1 | SDK identification is dictionary-based; rare SDKs slip through | Extend `analyze_modules.py:SDK_HINTS` or let the LLM catch them in Stage 4 |
| 2 | Top-level single-`src/` monorepos collapse into one entry | Manual `--subpath packages/<name>` |
| 3 | Repos over 500 MB are rejected outright | Pass `--subpath` to focus the clone |
| 4 | Public GitHub only — no GitLab / Bitbucket / private repos | Fork `fetch_repo.py` and add the adapter |
| 5 | No call-graph tracing or security auditing | Out of scope; use dedicated tools |

---

## Non-Goals

This project deliberately does **not** try to be:

- A security scanner or vulnerability auditor
- A code reviewer or refactoring suggestion engine
- A run-the-project guide or installation helper
- A multi-repo comparison / benchmarking tool
- A deep call-graph tracer

It does one thing: explain a repository.

---

## Contributing

PRs are welcome. The simplest contribution is a new theme — drop a JSON object into `templates/themes.json` following the existing schema. For pipeline changes:

1. Fork and create a feature branch
2. Run the pipeline end-to-end against at least one real repo (`tiangolo/fastapi` is a good smoke test)
3. Open a PR with a screenshot of the generated report
4. Include a one-line entry in the roadmap if the change introduces a new capability

For bigger ideas (new stages, new diagram types, new exporters), open an issue first so we can discuss the design.

---

## Acknowledgements

- [Mermaid.js](https://mermaid.js.org/) — flowcharts and sequence diagrams
- [Inter](https://rsms.me/inter/), [JetBrains Mono](https://www.jetbrains.com/lp/mono/), and [Fira Code](https://github.com/tonsky/FiraCode) — typography
- [GitHub REST API v3](https://docs.github.com/en/rest) — repository metadata
- Inspired by `deepwiki`, `gitingest`, and `gitsummary`; this project focuses specifically on **readability for non-engineers**.

---

## License

MIT — see [LICENSE](LICENSE) for details.
