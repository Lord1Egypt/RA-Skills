---
name: tavily-arxiv-paper-fetech
description: "Resolve one or more paper titles to reliable arXiv papers using Tavily search, then fetch compact arXiv metadata and abstracts with a local helper script. Use when the user provides paper titles and wants canonical arXiv URLs, title-author-year metadata, abstracts, or a reusable title-to-paper lookup workflow."
argument-hint: [paper-titles --workdir path]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, call_mcp_tool, WebFetch
---

# Tavily arXiv Paper Fetech Pipeline

Orchestrate a title-to-arXiv metadata workflow for: **$ARGUMENTS**

## Overview

This skill turns a list of paper titles into a reproducible arXiv lookup result:

```text
paper titles
-> Tavily search only
-> canonical arXiv abs URL
-> local arXiv metadata fetch
-> JSONL process log
-> markdown report
```

The goal is not just to answer once. The goal is to leave behind a reusable work folder that can be resumed or consumed by another workflow.

## Inputs

Extract or ask for:

- **TITLE_LIST**: one or more paper titles
- **WORKDIR**: optional working folder

If `WORKDIR` is omitted, default to:

- `0_docs/tavily_arxiv_paper_fetech`

Accepted title formats:

- a single title
- multiple titles separated by newlines
- markdown bullet lists

## Constants

- **TAVILY_ONLY = true** — Tavily is the only allowed search mechanism
- **SEQUENTIAL_MODE = true** — process titles one by one to reduce rate limits
- **NO_FALLBACK_SEARCH = true** — never switch to arXiv API search, guessed arXiv URLs, or another provider
- **LOW_CONTEXT_MODE = true** — append one JSON line per title, then render markdown from JSONL

## Work Folder Layout

Write all outputs under `WORKDIR`:

| Artifact | Purpose |
|----------|---------|
| `input_titles.md` | normalized input title list |
| `paper_fetches.jsonl` | one JSON line per processed title |
| `paper_fetch_report.md` | rendered report from the JSONL |

## Execution Rule

Process titles in order. Do not parallelize Tavily calls.

If Tavily rate limits:

- wait briefly
- retry Tavily only
- if it still fails, record the error and continue

## Phase 0: Initialize

1. Normalize the input title list.
2. Create `WORKDIR`.
3. Write the normalized title list to `WORKDIR/input_titles.md`.

## Phase 1: Tavily resolution

For each title:

1. Search Tavily with:

```text
"<paper title>" arXiv
```

2. Prefer results in this order:
   - `https://arxiv.org/abs/...`
   - `https://arxiv.org/html/...`
   - `https://arxiv.org/pdf/...`

3. Accept a result only when the match is reliable:
   - exact title match after minor normalization
   - same title with only punctuation, Unicode, or math-formatting differences
   - arXiv page clearly shows the same paper title

4. If uncertain, record `no_match` instead of guessing.

## Phase 2: Local arXiv fetch

Once a reliable arXiv URL is known, run:

```bash
python3 ".cursor/skills/tavily-arxiv-paper-fetech/scripts/fetch_arxiv_abs.py" "<arxiv-url>"
```

This returns compact JSON with:

- canonical abs URL
- arXiv id
- title
- authors
- abstract

## Phase 3: Low-context JSONL logging

For each title, immediately append one JSON line to:

- `WORKDIR/paper_fetches.jsonl`

Each line should include at least:

- `index`
- `input_title`
- `tavily_status`
- `tavily_error`
- `arxiv_url`
- `fetch`

Status values:

- `ok`
- `no_match`
- `error`

## Phase 4: Render markdown report

After all titles are processed, run:

```bash
python3 ".cursor/skills/tavily-arxiv-paper-fetech/scripts/jsonl_to_paper_fetch_md.py" \
  "WORKDIR/paper_fetches.jsonl" \
  "WORKDIR/paper_fetch_report.md"
```

## Output Format

The rendered report should look like:

```markdown
# Tavily arXiv Paper Fetech Report

## Results

### 1. Original Title
- Status: ok
- arXiv URL: https://arxiv.org/abs/xxxx.xxxxx
- arXiv ID: xxxx.xxxxx
- Resolved Title: ...
- Authors: ...
- Abstract: ...
```

## Key Rules

- Never fabricate a paper match.
- Never use non-Tavily search for title resolution.
- Keep all outputs inside `WORKDIR`.
- Prefer the local helper script over bringing full arXiv page content into context.

## Utility Scripts

- `scripts/fetch_arxiv_abs.py` — fetch compact metadata from a known arXiv URL
- `scripts/jsonl_to_paper_fetch_md.py` — render JSONL to markdown

## Additional Resources

- For copy-paste invocations and expected outputs, see [examples.md](examples.md)

## Example Invocation

```text
/tavily-arxiv-paper-fetech "RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control\nOpenVLA: An Open-Source Vision-Language-Action Model --workdir 0_docs/tavily_arxiv_lookup_run_01"
```
