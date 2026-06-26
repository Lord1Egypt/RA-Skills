---
name: visual-qa
description: Visual regression testing pipeline for web applications. Capture baseline screenshots, compare against new builds using pixel-level diffing, and gate deployments based on visual similarity thresholds. Use when: visual QA, visual regression testing, screenshot comparison, UI verification, visual diff, pre-deploy check, or validating UI changes before merge.
---

# Visual QA

A visual regression testing pipeline for web applications. Capture baseline screenshots of your app, compare new screenshots against baselines using pixel-level diffing, and pass/fail based on configurable similarity thresholds.

## When to Use

- **Pre-deploy visual verification** — gate merges/deploys until UI changes are approved
- **Regression testing** — catch unintended visual changes in CI
- **UI review workflow** — generate diff images for design/code review
- **Cross-browser/viewport testing** — verify responsive layouts
- **Component library QA** — ensure design system changes don't break consumers

## Quick Start

### 1. Capture Baselines

```bash
# Capture single URL
python scripts/capture.py http://localhost:3000 --output .visual-qa/baselines

# Capture multiple viewports
python scripts/capture.py http://localhost:3000 --viewports desktop mobile tablet --output .visual-qa/baselines

# Capture multiple pages from config
python scripts/capture.py --config .visual-qa.json --output .visual-qa/baselines
```

### 2. Compare Against Baselines

```bash
# Compare new screenshots
python scripts/diff.py --baseline .visual-qa/baselines --current .visual-qa/current --threshold 99
```

### 3. All-in-One Gate

```bash
# Capture + diff in one command
python scripts/gate.py --baseline .visual-qa/baselines --url http://localhost:3000 --threshold 99

# With local dev server
python scripts/gate.py --baseline .visual-qa/baselines --server "npm run dev" --port 3000 --threshold 99

# Using config file
python scripts/gate.py --config .visual-qa.json
```

## Config File Pattern

Create `.visual-qa.json` in your project root:

```json
{
  "urls": ["/", "/about", "/pricing"],
  "baseUrl": "http://localhost:3000",
  "viewports": ["desktop", "mobile"],
  "threshold": 99,
  "server": "npm run dev",
  "port": 3000,
  "baselineDir": ".visual-qa/baselines",
  "ignore": [".visual-qa/diffs", ".visual-qa/current"]
}
```

## Scripts

All scripts support `--help` for detailed usage.

### capture.py

Capture screenshots using Playwright (headless Chromium).

**Features:**
- Multiple viewport sizes: desktop (1280x800), tablet (768x1024), mobile (375x812)
- Waits for networkidle before capture
- Optional local server start/stop
- Configurable output directory
- Descriptive filenames: `{url-slug}_{viewport}.png`

**Usage:**
```bash
python scripts/capture.py <url> --output <dir> [options]
python scripts/capture.py --config <config.json> --output <dir>
```

### diff.py

Compare screenshots using pixel-level diffing (Pillow).

**Features:**
- Pixel-by-pixel comparison
- Diff images with red/magenta overlay highlighting changes
- Similarity percentage per image pair
- Pass/fail based on threshold (default 99%)
- Summary report with pass/fail status
- Saves diff images to output directory

**Usage:**
```bash
python scripts/diff.py --baseline <dir> --current <dir> --output <diff-dir> --threshold <percent>
```

### gate.py

All-in-one gate: capture + diff in a single command.

**Features:**
- Combines capture and diff steps
- Starts/stops local server automatically if needed
- Returns exit code 0 (pass) or 1 (fail)
- Human-readable summary output
- Can use config file or CLI args

**Usage:**
```bash
python scripts/gate.py --baseline <dir> --url <url> --threshold <percent>
python scripts/gate.py --baseline <dir> --server <command> --port <port> --threshold <percent>
python scripts/gate.py --config <config.json>
```

## Workflow Examples

### Initial Baseline Capture

```bash
# Start your app
npm run dev

# Capture baselines (desktop + mobile)
python scripts/capture.py http://localhost:3000 --viewports desktop mobile --output .visual-qa/baselines
```

### CI/CD Integration

```bash
# In your CI pipeline after build
python scripts/gate.py --baseline .visual-qa/baselines --server "npm start" --port 3000 --threshold 99

# Exit code 0 = pass, 1 = fail
if [ $? -eq 0 ]; then
  echo "Visual QA passed ✓"
else
  echo "Visual QA failed ✗"
  exit 1
fi
```

### Review Workflow

```bash
# 1. Developer makes UI changes
# 2. Capture new screenshots
python scripts/capture.py http://localhost:3000 --output .visual-qa/current

# 3. Generate diff images
python scripts/diff.py --baseline .visual-qa/baselines --current .visual-qa/current --output .visual-qa/diffs

# 4. Review diff images in .visual-qa/diffs/
# 5. If changes are intentional, update baselines:
rm -rf .visual-qa/baselines
mv .visual-qa/current .visual-qa/baselines
```

### Multi-Page Testing

Create `.visual-qa.json`:

```json
{
  "urls": ["/", "/products", "/about", "/contact"],
  "baseUrl": "http://localhost:3000",
  "viewports": ["desktop", "mobile"],
  "threshold": 99,
  "baselineDir": ".visual-qa/baselines"
}
```

```bash
# Capture all pages
python scripts/capture.py --config .visual-qa.json --output .visual-qa/baselines

# Gate all pages
python scripts/gate.py --config .visual-qa.json
```

## Dependencies

Scripts require Playwright and Pillow:

```bash
pip install playwright pillow
python -m playwright install chromium
```

Scripts will check for dependencies and print install instructions if missing.

## Thresholds

The `--threshold` parameter controls similarity percentage (0-100):

- **99%** (default) — strict, catches most visual changes
- **95%** — moderate, allows minor rendering differences (anti-aliasing, fonts)
- **90%** — loose, allows more variation (use for dynamic content)

Experiment to find the right threshold for your app. Start strict (99%) and loosen if you get false positives.

## Ignoring Dynamic Content

For pages with dynamic content (dates, user-specific data):

1. **Use data attributes** to hide dynamic elements during testing:
   ```css
   [data-test-hide] { visibility: hidden !important; }
   ```

2. **Capture specific viewport regions** (future enhancement)

3. **Loosen threshold** for pages with acceptable dynamic content

## Troubleshooting

**"Command not found: python"**
- Use `python3` instead of `python`

**"Playwright not installed"**
- Run: `pip install playwright && python -m playwright install chromium`

**"Similarity below threshold but images look the same"**
- Font rendering, anti-aliasing, or sub-pixel differences. Lower threshold to 98-95%.

**"Server not starting"**
- Check that `--port` matches your server's port
- Ensure server command is correct (`npm run dev`, `npm start`, etc.)
- Increase wait time in gate.py (default 5s)

**"Images not found"**
- Check that baseline directory exists and contains PNGs
- Ensure current screenshots were captured to the correct directory
- Verify filenames match pattern: `{url-slug}_{viewport}.png`

## Tips

- **Commit baselines** to Git so your team shares the same reference
- **Add `.visual-qa/diffs` and `.visual-qa/current` to `.gitignore`**
- **Run in CI** as a required check before merge
- **Update baselines** when intentional UI changes are made
- **Use multiple viewports** to catch responsive layout issues
- **Test empty/error/loading states** by capturing those URLs explicitly

## Integration with Other Skills

- **ux-qa-gate** — Use visual-qa as part of the UX QA checklist
- **webapp-testing** — Combine with Playwright functional tests
- **coding-agent** — Sub-agents building UI must pass visual-qa before completion

---

For detailed script options, run:
```bash
python scripts/capture.py --help
python scripts/diff.py --help
python scripts/gate.py --help
```
