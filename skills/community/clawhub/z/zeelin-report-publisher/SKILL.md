---
name: zeelin-report-publisher
description: Publish reports to the ZeeLin reports website ("智灵报告网站") by copying report assets, inserting a new top entry into public/reports_config.json for any category, running build checks, and preparing PR-ready branches.
metadata:
  openclaw:
    emoji: "🗂️"
    requires:
      bins:
        - python3
        - git
        - npm
      anyBins:
        - gh
---

# ZeeLin Report Publisher

## When To Use

Use this skill when the user asks to publish, upload, or add a report to the **智灵报告网站**.

Trigger intent should include both:

- the site phrase: `智灵报告网站`
- an action phrase: `发布` / `上架` / `新增报告`

This skill supports multiple categories (not only OpenClaw).

## Inputs

Collect these fields before running:

- `report_file` (required)
- `title` (required)
- `category` (required)
- `date` (optional, auto-infer if omitted)
- `abstract` (optional, auto-generate if omitted)
- `version` (optional, default `1.0`)
- `id` (optional)
- `cover_url` (optional)
- `category_dir` (optional)

Field details: see [report-metadata.md](references/report-metadata.md).

## Workflow

1. On a new machine, run GitHub bootstrap first (section below).
2. Confirm target repo path and that it contains `public/reports_config.json`.
3. Run the publisher script (below).
4. Verify build result.
5. Confirm branch push and PR URL.

## Bootstrap (New Machine)

Run this once per user machine to set git identity, authenticate GitHub, upload SSH key, and validate repo push permission:

```bash
bash {baseDir}/scripts/bootstrap_github.sh \
  --name "Your Name" \
  --email "you@example.com" \
  --repo "<repo_root>"
```

`<repo_root>` should point to your local report-site repository (for example `THU-ZeeLin-Reports`).

Fork workflow setup (recommended for team members without write access on main repo):

```bash
bash {baseDir}/scripts/bootstrap_github.sh \
  --name "Your Name" \
  --email "you@example.com" \
  --clone-url "git@github.com:<your-user>/THU-ZeeLin-Reports.git" \
  --upstream-url "git@github.com:thu-nmrc/THU-ZeeLin-Reports.git"
```

`--clone-dir` is optional. If omitted, repo is cloned to current workspace as `<workspace>/THU-ZeeLin-Reports`.

## Script

Primary command:

```bash
python3 {baseDir}/scripts/publish_report.py \
  --repo "<repo_root>" \
  --report-file "<report_file>" \
  --title "Report Title" \
  --category "OpenClaw" \
  --date "2026" \
  --version "1.0" \
  --abstract "Short summary text."
```

Default behavior:

- Copies file into `public/<category_dir>/`.
- Inserts new entry at index `0` in `public/reports_config.json`.
- Auto-detects `date` from file name/title (`YYYY-MM`/`YYYY`) and falls back to current year.
- Auto-generates `abstract` when omitted.
- Runs `npm run build`.
- Creates feature branch `codex/report-<id>`.
- Commits and pushes to `origin` (fork).
- Uses `upstream` as PR base remote when available (otherwise `origin`).
- Creates PR with `gh` if available; otherwise prints manual compare URL.

Remote options:

- `--push-remote` controls where branches are pushed (default `origin`).
- `--base-remote` controls PR base remote (default auto: `upstream` if exists, else `origin`).

## Abstract Generation Standard

When `abstract` is omitted, generate a concise, neutral summary by these rules:

- Use one sentence in Chinese, around 40-90 characters.
- Mention scope + value (for example: "核心进展、关键问题、落地路径").
- Avoid unverifiable claims and marketing tone.
- If content context is limited, use title/category-based generic summary.

## Guardrails

- Do not push directly to `main` as final delivery; use PR workflow.
- If working tree is dirty, stop unless user explicitly allows mixed changes.
- Validate git identity and push remote access before mutating files.
- Keep existing entry format compatible with site fields: `id/title/version/date/category/abstract/coverUrl/pdfUrl`.
