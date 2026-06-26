# HTML to PDF - Setup Guide

## Prerequisites

- Node.js installed

## 1. Install Dependencies

```bash
cd ~/.claude/skills/html-to-pdf
npm install
```

This installs Puppeteer which includes Chromium for rendering.

## 2. Test

```bash
# Create test HTML
echo "<h1>Test</h1>" > /tmp/test.html

# Convert to PDF
node scripts/html-to-pdf.js /tmp/test.html /tmp/test.pdf

# Check output
ls -la /tmp/test.pdf
```

If PDF is created, setup is complete!

## 3. Mark Setup Complete

Edit `SKILL.md` and change:
```yaml
setup_complete: true
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Chromium download fails | Set `PUPPETEER_SKIP_DOWNLOAD=true` and install Chrome manually |
| Permission denied | Check write permissions on output path |
| Hebrew/RTL issues | The script handles RTL automatically |
| Missing fonts | Install system fonts for the language |
