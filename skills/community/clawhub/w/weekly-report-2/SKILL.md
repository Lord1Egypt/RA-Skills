---
name: weekly-report
description: Generate structured weekly work reports from Git commit history and file-change statistics. Use when the user asks for a weekly report, work summary, progress review, or sprint recap based on repository activity, or when they need a Markdown report of what changed in a project over a time range.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - git
---

# Weekly Report Generator

Generates a structured Markdown weekly report from a Git repository's commit
history and file-change statistics.

## When to use

Use this skill when the user asks to:

- Create a weekly / daily / sprint work report from Git history
- Summarize what changed in a project over a date range
- Produce a Markdown progress report for a team standup

## Workflow

1. **Confirm scope**: Ask for the repository path (default: current directory),
   the number of days to cover (default: 7), and optionally an author filter.
2. **Collect commits**: Run `git log` over the time range with a stable format.
3. **Collect file changes**: Count files touched in the same range.
4. **Generate the report**: Fill in the template below and write it to
   `weekly-report.md` (or the requested output path).
5. **Review with the user**: Summarize highlights and let the user adjust
   narrative sections.

## Collecting data

Collect commits with a compact, parseable format:

```bash
git log --since="2026-08-25 00:00:00" --pretty=format:"%h|%ad|%an|%s" --date=short
```

Count changed files (excluding merge commits for cleaner stats):

```bash
git log --since="2026-08-25 00:00:00" --no-merges --name-only --pretty=format:"" | sort -u | wc -l
```

If the path is not a Git repository, fall back to listing files modified within
the time range (by `LastWriteTime`) and build the report from that, noting the
method in the report.

## Report template

```markdown
# 周报 Weekly Report

**报告周期**: 2026-08-25 ~ 2026-08-31
**提交总数**: N  |  **涉及文件**: M  |  **参与者**: 2

## 本周完成
- （按提交摘要归纳，用项目符号列出要点）

## 进行中
- （未完成/进行中的工作）

## 问题与风险
- （阻塞项或风险，无则写"无"）

## 下周计划
- （占位，由用户补充）

## 提交明细
| 提交 | 日期 | 作者 | 说明 |
|------|------|------|------|
| a1b2c3d | 08-26 | Alice | ... |
```

## Automated script (Windows)

On Windows PowerShell, an automated version is bundled:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/generate-report.ps1 -Repo . -Days 7 -Output weekly-report.md
```

Parameters:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `-Repo` | `.` | Path to the Git repository |
| `-Days` | `7` | Number of days to cover |
| `-Author` | *(all)* | Only include commits by this author |
| `-Output` | `weekly-report.md` | Output Markdown file |

The script runs `git log`, aggregates stats, and writes the filled template.

## Notes

- Keep the commit list to at most 50 rows; group or trim older items.
- Narrative sections ("本周完成" etc.) are drafted by the agent from commit
  summaries, then confirmed with the user.
- Non-Git fallback: if the folder is not a repo, list files modified in the
  range and mark the report as "based on file timestamps".

## Additional resources

- For sample reports and before/after examples, see [examples.md](examples.md)
