# Slidev Export

PDF, PNG, PPTX export and SPA builds.

## PDF Export

Export to PDF via CLI:
```bash
slidev export
```

Output: `slides-export.pdf` in project root.

### PDF Options
```bash
slidev export --output my-slides.pdf
slidev export --with-clicks          # Include click animations as pages
slidev export --with-toc             # Include table of contents
slidev export --dark                 # Force dark theme
slidev export --timeout 60000        # Increase timeout (ms)
```

### Configure in Headmatter
```yaml
---
export:
  format: pdf
  timeout: 30000
  dark: false
  withClicks: false
  withToc: false
---
```

### Custom Export Filename
```yaml
---
exportFilename: my-presentation
---
```

## PNG Export

Export slides as PNG images:
```bash
slidev export --format png
```

Output: Folder with numbered PNG files.

### PNG Options
```bash
slidev export --format png --output ./images
slidev export --format png --with-clicks
```

## PPTX Export

Export to PowerPoint format:
```bash
slidev export --format pptx
```

Note: PPTX export has limitations. Animations and some styles may not transfer perfectly.

## Build as SPA

Build a static single-page application:
```bash
slidev build
```

Output: `dist/` folder with static files.

### Build Options
```bash
slidev build --base /my-slides/     # Set base path for deployment
slidev build --out my-build         # Custom output directory
slidev build --without-notes        # Exclude speaker notes
```

### Base Path

For deployment to a subdirectory, base path MUST start and end with `/`:
```bash
# ✅ CORRECT
slidev build --base /talks/my-talk/

# ❌ WRONG
slidev build --base talks/my-talk
```

## PDF Download Button

Enable PDF download in the built SPA:
```yaml
---
download: true
---
```

Or provide a custom URL:
```yaml
---
download: /my-slides.pdf
---
```

## Generate PDF During Build

Build SPA with PDF included:
```yaml
---
export:
  format: pdf
  withClicks: true
download: true
---
```

Then run:
```bash
slidev build
```

The PDF is generated and linked automatically.

## Browser Executable

If export fails due to browser issues, specify Chromium path:
```bash
slidev export --executable-path /path/to/chromium
```

Or in config:
```yaml
---
export:
  executablePath: /path/to/chromium
---
```

## Hosting

### GitHub Pages

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 'lts/*'
      - run: npm install
      - run: npm run build -- --base /${{ github.event.repository.name }}/
      - uses: actions/upload-pages-artifact@v3
        with:
          path: dist

  deploy:
    needs: build
    runs-on: ubuntu-latest
    permissions:
      pages: write
      id-token: write
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/deploy-pages@v4
        id: deployment
```

### Netlify

Create `netlify.toml`:
```toml
[build]
publish = 'dist'
command = 'npm run build'

[[redirects]]
from = '/*'
to = '/index.html'
status = 200
```

### Vercel

Create `vercel.json`:
```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```