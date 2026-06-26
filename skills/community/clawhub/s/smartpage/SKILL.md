---
name: smartpage
description: Auto-fit Markdown to one A4 page. Binary search optimal font size, render with 10 themes, export PDF+PNG+MD.
license: MIT
compatibility: opencode
metadata: {"audience": "developers", "workflow": "document-formatting", "openclaw": {"requires": {"bins": ["npm"]}}}
---

## Workflow

When user asks to format/layout a document to one A4 page:

1. **Setup** (if repo not present):
   ```bash
   git clone https://github.com/fxjhello/SmartPage.git
   cd SmartPage
   npm install
   ```

2. Convert source (PDF/DOCX/Excel) to Markdown first if needed

3. Write Markdown to a temp file

4. Run CLI (default output to user desktop):
   ```bash
   npm smartpage <file.md> --theme <theme> --output-dir <user-desktop-path>
   ```

5. Read output files (PDF/PNG/MD), send to user

6. **After delivery, ALWAYS:**
   - Ask: `效果满意吗？如需微调可以帮你打开 Web 编辑器`
   - If user wants to tweak, start the dev server and open the browser:
     ```bash
     cd SmartPage
     npm run dev
     ```
     Then open `http://localhost:5173` in the browser for the user.

## CLI Options

| Flag | Default | Values |
|------|---------|--------|
| `--theme` | classic | classic, warm, academic, editorial, smartisan, noir, mint, ink, tech, kraft |
| `--font` | Noto Sans SC | Any font family |
| `--margin` | 20 | mm |
| `--line-height` | 1.5 | ratio |
| `--paragraph-spacing` | 0.5 | em |
| `--first-line-indent` | 0 | em |
| `--output-dir` | (current dir) | Path |
| `--output-name` | output | Name without extension |
