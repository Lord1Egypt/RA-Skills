---
name: ux-usability-auditor
description: Automated UX/usability audit for web applications. Use when the user wants to evaluate usability, accessibility, or UI consistency of a web app; mentions "usability audit", "UX review", "UI inspection", "易用性巡检", "体验巡检", or wants to generate a structured usability report. Works by navigating through target app pages via Playwright, capturing screenshots and UI metadata, then evaluating against a configurable checklist. Supports both Chinese and English usability standards.
---

# UX Usability Auditor

Automated usability and UX inspection for web applications. Navigates target app pages, captures screenshots and UI element metadata, then generates a structured audit report mapped to a usability checklist.

## Quick Start

Minimal workflow — 4 steps:

1. **Prepare config** — create a `config.json` (see [Configuration](#configuration))
2. **Run inspection** — `node scripts/inspect.js config.json`
3. **Review results** — check `results/inspection_results.json` and screenshots
4. **Generate report** — `node scripts/generate_report.js config.json`

## Configuration

Create a `config.json` in the working directory:

```json
{
  "name": "My App Usability Audit",
  "targetUrl": "https://example.com/#/login",
  "login": {
    "username": "admin",
    "password": "123456",
    "usernameSelector": "input[type='text'], input[placeholder*='账号'], input[placeholder*='用户名']",
    "passwordSelector": "input[type='password'], input[placeholder*='密码']",
    "submitSelector": "button:has-text('登录'), button:has-text('Login'), .login-btn"
  },
  "pages": [],
  "checklist": "references/checklist-default.md",
  "outputDir": "./results",
  "screenshotDir": "./results/screenshots",
  "headless": false
}
```

**`pages` field** (auto-discovery if empty):

- `[]` — auto-discover pages by clicking through sidebar/menu after login
- explicit list — provide known page URLs:

```json
{
  "pages": [
    { "name": "Dashboard", "url": "/#/dashboard" },
    { "name": "User List", "url": "/#/users" }
  ]
}
```

**Login selectors** — customize if the target app uses non-standard login form. Default works for most Element UI / Ant Design apps.

## Scripts

### `scripts/inspect.js` — Main Inspection Runner

Navigates pages, captures screenshots and UI metadata.

```bash
node scripts/inspect.js path/to/config.json
```

Output: `results/inspection_results.json` + `results/screenshots/*.png`

The script:
1. Launches Chromium via Playwright
2. Logs in using credentials from config
3. Discovers pages (auto from sidebar, or from config)
4. For each page: waits for load, screenshots, extracts UI stats (button/input/table counts, empty states, breadcrumbs, action buttons)
5. Writes results to JSON

### `scripts/generate_report.js` — Report Generator

Generates a markdown audit report from inspection results + checklist.

```bash
node scripts/generate_report.js path/to/config.json
```

Output: `results/usability_audit_report.md`

The script:
1. Loads `inspection_results.json`
2. Parses the checklist (markdown file, supports the standard 6-category format)
3. Evaluates each checklist item against inspection data
4. Generates a structured report with: summary table, detailed findings per category, evidence screenshots, priority-ranked issue list

## Checklist Format

The default checklist is at `references/checklist-default.md`. It follows this format (compatible with the 易用性专项检查项清单 Excel):

```markdown
# Usability Checklist

## Category 1: Navigation & Layout
### 1.1 Menu Hierarchy
- **Standard**: menu depth ≤ 3 levels, high-frequency entries prioritized
- **Applicable to**: All modules
```

To use a custom checklist, point `checklist` in config.json to your own markdown file, or pass a path to `generate_report.js`:

```bash
node scripts/generate_report.js config.json --checklist my_checklist.md
```

## Advanced: Tuning Page Discovery

If auto-discovery misses pages, manually list them in config.json `pages` field. The inspector will navigate to each URL and capture data.

For single-page apps (SPA) with hash routing (like the one we audited), make sure URLs include the `#/` fragment.

## Output Structure

```
results/
├── inspection_results.json      # Raw inspection data per page
├── usability_audit_report.md   # Final report (markdown)
├── screenshots/
│   ├── 01_dashboard.png
│   ├── 02_user_list.png
│   └── ...
└── report_assets/              # Copied screenshots for report embedding
```

## Notes

- **Playwright required**: `npm install playwright` before first run
- **Chromium bundled**: Playwright downloads its own Chromium; no local Chrome needed
- **Headless mode**: Set `"headless": true` in config for CI/batch runs
- **Chinese UI**: Default selectors and checklist support Chinese enterprise web apps (Element UI, Ant Design)
- **SPA support**: Handles hash-based routing (`#/`) and pushState routing
