---
name: wechat-collect
description: Fetch a public WeChat article URL, archive the raw HTML, and convert the article into a stage-1 compatible brief in `content-production/inbox/`. Use when Codex needs to collect公众号文章素材 or start the Stage 2 collect-to-create pipeline from a public `mp.weixin.qq.com` URL.
---

# WeChat Collect

Collect a public WeChat article and transform it into a brief that can be passed directly to `case-writer-hybrid`.

## Quick Start

Run the default command:

```bash
.venv/bin/python -m skill_runtime.cli run-skill wechat-collect --input content-production/inbox/20260403-wechat-collect-url.txt
```

## Prepare Input

Pass a text file containing at least one URL. The first detected URL is used.

Example input file:

```text
content-production/inbox/20260403-wechat-collect-url.txt
```

## Follow Collection Workflow

1. Fetch the public article HTML from the first detected URL.
2. Extract title, author, date, and candidate正文段落 from the page.
3. Build a stage-1 compatible brief that downstream writing steps can reuse.
4. Archive the raw HTML for traceability and later extraction tuning.

## Write Output

Write the brief to:

```text
content-production/inbox/<date>-<slug>-gzh-brief.md
```

Write the raw archive to:

```text
content-production/inbox/raw/wechat/<date>-<slug>.html
```

## Respect Constraints

- Only works for publicly reachable article URLs
- Deleted articles or anti-crawl variants may produce reduced-quality extraction or fail explicitly
- Current extraction is usable for pipeline intake, but still needs quality tuning for cleaner argument mining

## Read Related Files

- Shared runtime: `skills/wechat-collect/runtime.py`
- Pipeline entry: `skill_runtime/engine.py`
- Stage 2 workflow: `workflows/stage2-wechat-pipeline.json`
- Planning reference: `docs/content-skills-implementation-plan.md`
