---
name: topic-research
description: Run a second-hop deep research pass through the Tavily CLI after an initial scan, then normalize the result into a local `research.md` contract. Use when Codex needs cited follow-up research for a chosen topic from `news-collect`, or wants a reusable research report saved into `content-production/inbox/`.
---

# Topic Research

This skill deepens a selected topic after `news-collect` or any manually chosen theme. It does not replace first-pass collection. The report now also produces a local writing decision layer.

## Quick Start

Run the default command:

```bash
.venv/bin/python -m skill_runtime.cli run-skill topic-research --input content-production/inbox/20260405-agent-topic-research.md
```

## Prepare Input

Pass a markdown request file with YAML frontmatter.

Supported fields:

- `topic`
- `question`
- `model`: `mini` / `pro` / `auto`
- `source_file`: optional path to a prior `news-report.md`
- `seed_urls`: optional list or comma-separated URLs

Example:

```markdown
---
topic: AI coding agents
question: 这些产品近一周的产品化方向和商业化信号是什么？
model: pro
source_file: content-production/inbox/20260405-ai-news-report.md
seed_urls:
  - https://example.com/a
  - https://example.com/b
---

补充说明：优先输出能转成中文公众号选题判断的结论。
```

## Follow Research Workflow

1. Validate that `tvly` is installed and available on PATH.
2. Combine the request fields into a single research query.
3. Call `tvly research ... --json`.
4. Save the raw JSON and rewrite the result into a normalized markdown research report.
5. Add a writing-decision section covering whether the topic is worth writing, recommended structure, opening hooks, title directions, and evidence risks.

## Write Output

Write the report to:

```text
content-production/inbox/YYYYMMDD-<slug>-research.md
```

Write the raw JSON to:

```text
content-production/inbox/raw/research/YYYY-MM-DD/<slug>.json
```

## Respect Constraints

- Only use the repo-local dependency marker `skills/tavily-research/` for this integration
- Do not silently fall back if `tvly` is missing or not logged in
- Keep the output contract stable even if Tavily CLI changes its JSON schema

## Read Related Files

- Runtime entry: `skill_runtime/engine.py`
- Wrapper runtime: `skills/topic-research/runtime.py`
- Vendor dependency marker: `skills/tavily-research/`
- Data contract: `docs/data-contracts.md`
