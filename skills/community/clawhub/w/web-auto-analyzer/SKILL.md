---
name: Chrome DevTools Auto Analyzer
slug: chrome-devtools-auto-analyzer
version: 1.1.1
homepage: https://github.com/user/chrome-devtools-auto-analyzer
description: Automatically analyze websites for performance metrics and audit issues using Lighthouse.
metadata: {"clawic":{"emoji":"🤖","requires":{"bins":["node","npm"],"npm":["lighthouse","chrome-launcher"]},"os":["linux","darwin","win32"]}}
---

## When to Use

User wants to automatically analyze a website URL for performance metrics, accessibility, SEO, or best practices without manual Chrome DevTools interaction.

## Core Rules

1. **Verify prerequisites** — Check Node.js (v18+) and packages installed: `node --version && npm list lighthouse chrome-launcher`

2. **Run Lighthouse audit** — Execute `node automation-script.js <URL> [--mobile] [--output=DIR]` to collect all metrics.

3. **Extract and present metrics** — Use tables for scores (0-100) and metrics with status indicators (⚪ Good, 🟡 Warning, 🔴 Critical).

4. **Identify critical issues** — Flag metrics outside thresholds: LCP>2.5s, CLS>0.1, INP>200ms, TBT>200ms, Performance<50.

5. **Provide actionable fixes** — For each issue, include specific code fixes from `audit-checklist.md` and `metrics-reference.md`.

6. **Save results** — Store JSON and HTML reports in `./results/`. Ask user before saving to memory for tracking.

7. **Handle errors gracefully** — If audit fails, check `troubleshooting.md` for common solutions (Chrome not found, ES module errors, memory issues).

## Quick Reference

| Topic | File |
|-------|------|
| Automation script | `automation-script.js` |
| Metrics & thresholds | `metrics-reference.md` |
| Fix checklists | `audit-checklist.md` |
| Setup guide | `setup.md` |
| Quick start | `quick-start.md` |
| Troubleshooting | `troubleshooting.md` |
| Memory tracking | `memory-template.md` |

## Data Storage

After analysis, offer to save: URL, timestamp, scores, critical issues, report path. Always ask before saving to memory.

## Security & Privacy

- Runs locally in headless Chrome — no external data transmission
- Warn before analyzing authenticated URLs
- JSON reports contain URL structure — handle sensitive paths carefully

## Common Commands

```bash
# Quick audit (desktop)
node automation-script.js https://example.com

# Mobile emulation
node automation-script.js https://example.com --mobile

# Custom output directory
node automation-script.js https://example.com --output=./reports

# Lighthouse CLI directly
lighthouse https://example.com --output=json --output-path=report.json
```

## Troubleshooting Quick Reference

| Error | Solution |
|-------|----------|
| "lighthouse is not a function" | Add `"type": "module"` to package.json |
| "Chrome not found" | Install Chrome or use `npm install puppeteer` |
| "JavaScript heap out of memory" | Run with `node --max-old-space-size=4096` |
| "Port already in use" | Specify different port in script config |
