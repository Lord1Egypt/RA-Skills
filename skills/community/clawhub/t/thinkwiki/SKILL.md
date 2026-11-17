---
name: "ThinkWiki"
description: "Use this skill when the user wants to create, maintain, query, or visualize a local Markdown knowledge base. ThinkWiki can initialize a wiki, import files or webpages, collect inbox items, answer from existing knowledge, save higher-value outputs, and generate HTML viewer and graph artifacts."
license: "MIT"
compatibility: "Requires Python 3 with venv support. ThinkWiki bootstraps its own .venv, installs runtime dependencies from requirements.txt, and supports macOS, Linux, and Windows."
---

# ThinkWiki

ThinkWiki is a single public skill for working with a local Markdown knowledge base.

## Role

- Act as the end-user-facing knowledge base assistant.
- Translate user intent into stable ThinkWiki actions.
- Prefer natural conversation over exposing raw subcommands.
- Treat existing wiki pages as the primary evidence base for answers.
- Escalate to page creation only when the output is valuable enough to preserve.

## Operating Principles

- Keep ThinkWiki as the only visible skill entry point.
- Resolve the wiki root before running any read, write, or generation task.
- Prefer evidence-first answers from existing pages.
- Prefer HTML deliverables such as inbox, viewer, graph, and governance pages when the user asks to inspect or browse the workspace.
- Surface ambiguity explicitly when confidence is low, sources conflict, or entity identity is unclear.

## When To Use This Skill

- The user wants to create or maintain a local knowledge base.
- The user wants to import Markdown, PDF, DOCX, XLSX, XLS, PPTX, webpages, or plain text.
- The user wants to collect content into an inbox before formal ingest.
- The user wants to ask questions against an existing wiki.
- The user wants to save results as `query`, `synthesis`, `decision`, or `concept` pages.
- The user wants to generate a viewer, a graph, or a governance report.
- The user wants to review entity alias collisions or perform deterministic entity merges.

## When Not To Use This Skill

- The task is unrelated to a local Markdown knowledge base.
- The user only wants general chat without knowledge capture, lookup, or maintenance.
- The task belongs to a different productivity domain such as spreadsheets, slides, or unrelated code work.

## Required Environment Variables

Remote AI features are **disabled by default**. Configure only what you need.

### Content generation (`crystallize`, `digest`)

Requires all three variables. Any OpenAI-compatible chat completion endpoint works.

| Variable | Required | Used By | Notes |
|----------|----------|---------|-------|
| `THINKWIKI_LLM_API_KEY` | Yes, to enable | `llm_client.py` | API key for the configured LLM provider |
| `THINKWIKI_LLM_BASE_URL` | Yes, to enable | `llm_client.py` | Chat completions URL |
| `THINKWIKI_LLM_MODEL` | Yes, to enable | `llm_client.py` | Model name |
| `THINKWIKI_LLM_TEMPERATURE` | No | `llm_client.py` | Optional temperature override |

Without a complete LLM configuration, `crystallize` and `digest` use local heuristics only.

### Entity embedding (`entity-merge-review`, `graph-report`, `health`)

Enabled when `THINKWIKI_EMBED_API_KEY` is set. Defaults to SiliconFlow BGE-M3.

| Variable | Required | Used By | Notes |
|----------|----------|---------|-------|
| `THINKWIKI_EMBED_API_KEY` | Yes, to enable | `embed_client.py` | API key for the embedding provider |
| `THINKWIKI_EMBED_BASE_URL` | No | `embed_client.py` | Default `https://api.siliconflow.cn/v1/embeddings` |
| `THINKWIKI_EMBED_MODEL` | No | `embed_client.py` | Default `BAAI/bge-m3` |

## Root Resolution

- If the user provides a wiki path, use it directly.
- If the working directory already contains `.wiki-schema.md`, treat that directory as the wiki root.
- If the user wants a new workspace, run `init`.
- If no wiki root can be found, ask the user where the wiki should live before making changes.

## Execution Entry

When you need to invoke ThinkWiki, use the unified entry:

```bash
<python-command> scripts/thinkwiki <command> ...
```

Platform note:

- On macOS and Linux, `<python-command>` is usually `python3`.
- On Windows, `<python-command>` is usually `python`.

## Intent Mapping

- Create a wiki -> `init`
- Warm up the runtime -> `bootstrap`
- Convert a file or webpage to Markdown -> `convert`
- Import a file or webpage into the wiki -> `ingest`
- Collect content into inbox first -> `clip`
- Build or refresh inbox review -> `inbox`
- Ask from existing wiki knowledge -> `ask`
- Save a correction or lesson learned -> `correct`
- Save a valuable answer -> `query`
- Create a concept, decision, or synthesis artifact -> `crystallize` or `digest`
- Build the graph explorer -> `graph`
- Build the graph governance report -> `graph-report`
- Review entity merge candidates -> `entity-merge-review`
- Preview or apply entity merges -> `entity-merge-apply`
- Browse HTML outputs in a browser -> `serve`
- Check workspace health -> `health`
- Check a compact workspace snapshot -> `status`
- Validate environment capabilities -> `doctor`

## Browsing HTML Outputs

ThinkWiki HTML pages are static files under `<wiki-root>/output/`. Agent chat UIs usually cannot render them inline, so prefer the loopback HTTP server when the user wants to inspect or browse outputs.

Default workflow:

```bash
<python-command> scripts/thinkwiki serve --root <wiki-root>
```

This serves `<wiki-root>/output/` at `http://127.0.0.1:8765/` by default.

Useful URLs:

- Workspace home: `http://127.0.0.1:8765/index.html`
- Inbox review: `http://127.0.0.1:8765/inbox/index.html`
- Local viewer: `http://127.0.0.1:8765/viewer/index.html`
- Knowledge graph: `http://127.0.0.1:8765/graph/index.html`
- Graph report: `http://127.0.0.1:8765/graph/report.html`

OpenClaw integration:

- After `viewer`, `graph`, `inbox`, or `graph-report`, run `serve` when the user wants to browse the results.
- If the OpenClaw browser tool is available, open the workspace home URL in the `openclaw` browser profile.
- If a long-running `serve` process is not practical in the current session, run `serve --print-urls` and tell the user to start `serve` locally, then open the printed workspace URL.

## Completion Criteria

- After initialization, report where the wiki was created.
- After import or capture, explain what was ingested or clipped and which artifacts were refreshed.
- After answer tasks, cite the relevant wiki pages and call out confidence or conflict where needed.
- After graph or viewer tasks, report the HTML artifact locations, especially `output/index.html`.
- When the user wants to browse inbox, viewer, graph, or governance pages, prefer `serve` and return the loopback HTTP URLs instead of only `file://` paths.
- After starting `serve`, give the user the workspace home URL first (`http://127.0.0.1:8765/index.html` by default) and, in OpenClaw, offer to open it with `openclaw browser --browser-profile openclaw open <url>`.
- If the host cannot keep a long-running process alive, run `serve --print-urls` to show the URLs and ask the user to start `serve` in a local terminal or background job.
- After graph governance tasks, report the relevant governance outputs such as `output/graph/report.html`.
- After entity merge review, report how many ambiguous groups need manual confirmation and point to `output/graph/entity-merge-review.html`.
- After entity merge dry-runs, make it explicit that no entity pages were modified and point to `output/graph/entity-merge-plan.html`.
- After entity merge apply, report the canonical entity page, the merged pages, and the refreshed outputs.
- When execution fails, explain the missing input, root cause, or capability gap instead of only returning raw command errors.
