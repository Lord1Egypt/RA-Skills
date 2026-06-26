---
name: screenshot-visual
description: Takes screenshots of targets using Playwright and performs visual/contextual analysis for potential vulnerabilities.
version: 1.0.0
author: NyetNighy
tags: [bugbounty, screenshots, visual-analysis, reconnaissance]
metadata:
  {"openclaw":{"emoji":"📸","os":["linux","darwin","win32"],"requires":{"bins":["playwright-mcp","npx"]},"install":[{"id":"npm-playwright-mcp","kind":"npm","package":"@playwright/mcp","bins":["playwright-mcp"],"label":"Install Playwright MCP"}]}}
---

# Screenshot + Visual Analysis Skill

Uses browser automation to capture screenshots and analyze pages for interesting security indicators.

## When to Use

Use this skill when you need to:
- Capture screenshots of target pages for visual bug bounty recon
- Find exposed panels, debug interfaces, or login pages
- Detect weak security headers visually
- Build a visual inventory of a target's web surface

## Workflow

1. **Navigate** to target URL and capture screenshot
2. **Collect** page source, security headers, and JavaScript endpoints
3. **Analyze** for security-relevant indicators
4. **Report** findings with severity and evidence

## Quick Start

```bash
node scripts/screenshot.js https://example.com
```

## Configuration

Default output dir: `screenshots/` (created in workspace)
Default viewport: 1280x720
Full page screenshot: yes

## Example Prompts

- "Take screenshots and analyze visually for example.com"
- "Visual recon with screenshots on target.com"
- "Check login pages for issues"

## Requirements

- Requires `playwright-mcp` or equivalent browser automation
- Node.js environment with `@playwright/mcp` installed
- `playwright` browser binaries (`npx playwright install chromium`)

## Output

Each run produces:
- `screenshots/<domain>/<path>-<timestamp>.png` — screenshot file
- `screenshots/<domain>/<path>-<timestamp>.json` — metadata + headers

## Security Notes

- Screenshots are saved locally only
- No data leaves the machine except browser requests to the target
- Respect target scope and rate limits