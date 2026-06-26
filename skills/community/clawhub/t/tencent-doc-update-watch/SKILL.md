---
name: tencent-doc-update-watch
description: Privacy-first re-crawl and diff workflow for Tencent Docs (docs.qq.com) update checks. Use when asked to re-crawl Tencent Docs links, verify whether content changed since last snapshot, and produce a structured update report. Supports sheet/doc/aio links and snapshot comparison.
---

# Tencent Doc Update Watch

## Overview

Use this skill to re-crawl Tencent Docs links and detect updates with snapshot diffing.
The workflow outputs:
- `manifest.json` (structured machine-readable result)
- `report.md` (human-readable diff summary)

## Quick Run

Run with default doc list:

```bash
python scripts/check-qq-doc-updates.py \
  --config references/default-docs.json \
  --workspace /tmp/tencent-doc-watch
```

Run with explicit baseline:

```bash
python scripts/check-qq-doc-updates.py \
  --config /abs/path/my-docs.json \
  --workspace /tmp/tencent-doc-watch \
  --compare /tmp/tencent-doc-watch/snapshots/20260305_101500/manifest.json
```

## Privacy Defaults

Default behavior is privacy-first:
- Raw HTML/opendoc/cookie files are removed after parsing.
- URL query values are redacted in `opendoc_url` fields.
- Public URL in manifest removes query strings to avoid leaking tokens.

Keep raw files only when explicitly needed for debugging:

```bash
python scripts/check-qq-doc-updates.py \
  --config references/default-docs.json \
  --workspace /tmp/tencent-doc-watch \
  --keep-raw
```

## Config Format

Use JSON:

```json
{
  "docs": [
    {
      "name": "Example Sheet",
      "url": "https://docs.qq.com/sheet/DEXAMPLE_SHEET_001?tab=sample"
    },
    {
      "name": "Example Doc",
      "url": "https://docs.qq.com/doc/DEXAMPLE_DOC_001"
    }
  ]
}
```

Optional field:
- `id`: Tencent doc ID (auto-parsed from URL when omitted)

## Output and Status

Generated under `<workspace>/snapshots/<label>/`:
- `manifest.json`
- `report.md`
- `raw/` only when `--keep-raw` is enabled

Report status values:
- `UNCHANGED`
- `CHANGED`
- `NEW`
- `FIRST_RUN`

## Key Detection Signals

Comparison currently checks:
- `last_modify_ms`
- `rev`
- `cgi_code`
- `title`
- `pad_type`

## 中文补充

此 Skill 固化“腾讯文档重新抓取 + 与历史快照对比”的流程。默认开启隐私最小化策略：
- 不持久化原始抓取内容（除非加 `--keep-raw`）
- 脱敏 `opendoc_url` 查询参数
- 在 `manifest.json` 中移除页面 URL 的查询参数
