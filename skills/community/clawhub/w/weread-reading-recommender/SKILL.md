---
name: weread-reading-recommender
description: Use this skill when the user wants to export local WeRead records, normalize WeRead data, analyze reading preferences from WeRead history, or get book recommendations grounded in WeRead reading behavior and a current learning goal.
---

# WeRead Reading Recommender

## Overview

This is a local-first skill for exporting 微信读书 (WeRead) records from a cookie stored on the user's machine, normalizing those records into a recommendation-friendly JSON file, and using that data to analyze reading preferences or recommend what to read next.

Use this skill when the user wants to:
- 根据微信读书记录推荐书
- 分析自己的阅读偏好或阅读画像
- 结合“最近想学的主题”与微信读书历史一起做推荐
- 导出、刷新、归一化本地微信读书数据

## Trigger Cases

Activate this skill for requests like:
- “根据我的微信读书记录推荐书”
- “分析我的阅读偏好”
- “我最近想系统学 AI Agent，结合微信读书记录推荐 5 本书”
- “帮我导出 / 刷新 / 归一化微信读书数据”
- “基于我的阅读历史，推荐下一本最适合现在读的书”
- “分析我的阅读偏好，并给我 3 本稳妥推荐 + 2 本探索推荐”

## Workflow

Follow this sequence:

1. Check whether a normalized JSON file already exists.
2. If normalized data is missing, or the user explicitly wants fresh data, check whether a local WeRead cookie is already available.
3. Look for a local cookie source in this order:
   - a cookie file path explicitly provided by the user
   - `WEREAD_COOKIE`
   - another env var name passed through `--env-var`
4. If no local cookie source exists, ask the user to set one locally and stop there. Do not tell the user to edit `SKILL.md`.
5. If a local cookie source exists, run the export script.
6. Run the normalize script on the raw export.
7. Read the normalized JSON and identify strong signals:
   - high-engagement books
   - recent books
   - unfinished books with momentum
   - repeated categories or lists
8. If the user provides a current goal, weight goal fit first.
9. If the user does not provide a goal, produce a reading-profile summary plus safe and exploratory recommendations.

## Recommendation Guidance

When the user provides a current goal, weight approximately:
- 60% goal fit
- 40% history fit

When the user provides no goal, weight approximately:
- 70% history fit
- 20% recency
- 10% exploration/diversity

For each recommendation, explain:
- why it fits the user's current goal or history
- which past books it resembles
- what gap it fills
- whether it is a safe pick or an exploration pick
- whether it is a good fit right now

Suggested response structure:
- 阅读画像 / Reading profile
- 推荐结果 / Recommendations
- 为什么适合现在 / Why now
- 暂缓推荐 / Skip for now (optional)

## Local Data Workflow

### 1. Check local cookie availability first

Before asking the user to set anything, first check whether a local cookie is already available through:
- a cookie file path the user provided
- `WEREAD_COOKIE`
- another env var name passed through `--env-var`

If none of these exist, ask the user to set the cookie locally, then continue.

### 2. Export raw WeRead data

If a local cookie is already available, export directly:

```bash
python3 scripts/export_weread.py --out data/weread-raw.json
```

Optional variants:

```bash
python3 scripts/export_weread.py --cookie-file ~/.config/weread.cookie --out data/weread-raw.json
python3 scripts/export_weread.py --env-var WEREAD_COOKIE --include-book-info --detail-limit 50 --out data/weread-raw.json
```

If the user does need to set one manually, keep it local. For example:

```bash
export WEREAD_COOKIE='wr_skey=...; wr_vid=...; ...'
```

### 3. Normalize the raw export

```bash
python3 scripts/normalize_weread.py --input data/weread-raw.json --output data/weread-normalized.json
```

### 4. Use the normalized file for recommendation turns

After normalization, this skill should reason primarily from the normalized JSON, not from a live cookie session, unless the user explicitly asks for a refresh.

## Security Boundary

This skill is local-first. Enforce these rules:

- Cookie is for local use only.
- Never write the cookie into `SKILL.md`, scripts, assets, logs, or exported JSON.
- Never echo the cookie back in responses.
- Prefer checking existing local cookie sources before asking the user to set one again.
- Do not rely on CookieCloud or any third-party cookie sync service by default.
- Do not suggest remote cookie hosting as the normal path.
- Recommendation work should use the normalized JSON whenever possible.

## Files

Use these project files as the main references:
- `scripts/export_weread.py`
- `scripts/normalize_weread.py`
- `references/data-schema.md`
- `references/privacy-model.md`
- `references/recommendation-rubric.md`
- `assets/sample-weread-raw.json`
- `assets/sample-weread-normalized.json`

## Example Requests

- 结合我的微信读书记录，我最近想系统学 AI Agent，推荐 5 本书
- 基于我的阅读历史，推荐下一本最适合现在读的书
- 分析我的阅读偏好，并给我 3 本稳妥推荐 + 2 本探索推荐
- 帮我刷新微信读书数据，然后按最近在读主题推荐下一批书
