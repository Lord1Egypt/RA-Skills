---
name: pdf-report-generator
description: Convert Markdown reports to professionally formatted PDF documents using pdfkit. Supports Chinese fonts, A4 layout, auto headers/footers, page numbers. Designed primarily for daily-market-report output but usable for any Markdown-to-PDF conversion.
emoji: 📄
metadata:
  openclaw:
    requires:
      bins:
        - node
    envVars:
      - name: PDFKIT_PATH
        required: false
        description: Path to pdfkit node_modules (defaults to workspace/.tmp-report)
---

# PDF Report Generator — Markdown转PDF

Convert structured Markdown reports into print-ready A4 PDF documents with Chinese font support, automatic headers/footers, and page numbers. Designed to work hand-in-hand with the `daily-market-report` skill.

## When to Use

| Scenario | Trigger |
|:---------|:--------|
| End-of-day market report → PDF | After `daily-market-report` generates a Markdown summary |
| Trade journal / weekly review export | Convert structured notes to PDF |
| Investment memo generation | Produce clean A4 printouts for offline review |
| Any Markdown → formatted PDF | General-purpose conversion |

## Prerequisites

The pdfkit library is already installed at:

```
C:\Users\Tania\.openclaw\workspace\.tmp-report\node_modules\pdfkit
```

No additional installs needed. The skill uses this existing dependency.

### Chinese Font

For Chinese text rendering, pdfkit requires a TrueType font file. Recommended:

- **Noto Sans SC** (free, open-source): Download from [Google Fonts](https://fonts.google.com/noto/specimen/Noto+Sans+SC)
- **Source Han Sans** (思源黑体): Another good open-source option
- **Microsoft YaHei** (微软雅黑): Available on Windows at `C:\Windows\Fonts\msyh.ttc`

Place the font file in the skill's `assets/` directory or reference it from a known path. Example:

```bash
# Option 1: Place in assets/
cp /path/to/NotoSansSC-Regular.ttf skills/pdf-report-generator/assets/

# Option 2: Use Windows system font (no copy needed)
# Just reference C:\Windows\Fonts\msyh.ttc in the script
```

## Workflow: Markdown → PDF

### Step 1: Parse Markdown content

The input is a Markdown string. Key structural elements to handle:

| Markdown Element | PDF Rendering |
|:-----------------|:--------------|
| `# H1` | Large bold header |
| `## H2` | Medium bold header |
| `### H3` | Small bold header |
| Plain text | Body paragraph |
| `| table |` | Table with borders |
| `**bold**` | Bold text |
| `- list` | Bullet point |
| `> quote` | Indented italic |
| `---` | Horizontal rule |
| `` `code` `` | Monospace |
| `🟢` / `🔴` | Color markers |

### Step 2: Generate PDF via Node.js script

Create and run a Node.js script that uses pdfkit. Script location: `skills/pdf-report-generator/scripts/generate_pdf.js`

#### Core Script Template

```javascript
const PDFDocument = require('pdfkit');
const fs = require('fs');

// === CONFIG ===
const FONT_PATH = 'C:/Windows/Fonts/msyh.ttc';     // Chinese font
const FONT_BOLD_PATH = 'C:/Windows/Fonts/msyhbd.ttc'; // Bold variant (optional)
const PAGE_WIDTH = 595.28;   // A4 width (points)
const PAGE_HEIGHT = 841.89;  // A4 height (points)
const MARGIN = 72;           // 1 inch margins
const HEADER_Y = 40;
const FOOTER_Y = PAGE_HEIGHT - 30;
const CONTENT_TOP = 72;
const CONTENT_BOTTOM = PAGE_HEIGHT - 72;

// === HELPERS ===
function addHeader(doc, text) {
  doc.fontSize(8).font(FONT_PATH)
     .text(text, MARGIN, HEADER_Y, { align: 'left' });
  doc.moveTo(MARGIN, HEADER_Y + 14)
     .lineTo(PAGE_WIDTH - MARGIN, HEADER_Y + 14)
     .stroke('#cccccc');
}

function addFooter(doc, pageNum) {
  doc.fontSize(8).font(FONT_PATH)
     .text(`第 ${pageNum} 页`, MARGIN, FOOTER_Y, { align: 'center' });
}

function renderTable(doc, headers, rows, startY) {
  // Column widths: equal distribution
  const colCount = headers.length;
  const colWidth = (PAGE_WIDTH - 2 * MARGIN) / colCount;
  let y = startY;

  // Header row
  doc.fontSize(9).font(FONT_BOLD_PATH || FONT_PATH);
  headers.forEach((h, i) => {
    doc.text(h, MARGIN + i * colWidth + 2, y + 2, {
      width: colWidth - 4, align: 'center'
    });
  });
  y += 20;

  // Draw header line
  doc.moveTo(MARGIN, y).lineTo(PAGE_WIDTH - MARGIN, y).stroke();

  // Data rows
  doc.fontSize(9).font(FONT_PATH);
  for (const row of rows) {
    row.forEach((cell, i) => {
      doc.text(String(cell), MARGIN + i * colWidth + 2, y + 2, {
        width: colWidth - 4, align: 'center'
      });
    });
    y += 18;

    doc.moveTo(MARGIN, y).lineTo(PAGE_WIDTH - MARGIN, y)
       .stroke('#eeeeee');
  }

  return y; // Return next Y position
}

// === MAIN ===
function generatePDF(markdownContent, outputPath, title) {
  const doc = new PDFDocument({
    size: 'A4',
    margins: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN },
    info: {
      Title: title || 'Market Report',
      Author: 'OpenClaw 虾哥',
      Producer: 'OpenClaw pdf-report-generator',
    }
  });

  const stream = fs.createWriteStream(outputPath);
  doc.pipe(stream);

  let pageNum = 1;
  addHeader(doc, title || '市场报告');
  addFooter(doc, pageNum);

  // --- Parse and render markdown ---
  const lines = markdownContent.split('\n');
  let y = CONTENT_TOP;

  for (const line of lines) {
    // Check if we need a new page
    if (y > CONTENT_BOTTOM - 30) {
      doc.addPage();
      pageNum++;
      addHeader(doc, title || '市场报告');
      addFooter(doc, pageNum);
      y = CONTENT_TOP;
    }

    // H1
    if (line.startsWith('# ')) {
      doc.fontSize(18).font(FONT_BOLD_PATH || FONT_PATH)
         .fillColor('#1a1a2e');
      y = doc.text(line.slice(2), MARGIN, y + 16, {
        continued: false
      }).y + 6;
    }
    // H2
    else if (line.startsWith('## ')) {
      doc.fontSize(14).font(FONT_BOLD_PATH || FONT_PATH)
         .fillColor('#16213e');
      y = doc.text(line.slice(3), MARGIN, y + 12, {
        continued: false
      }).y + 4;
    }
    // H3
    else if (line.startsWith('### ')) {
      doc.fontSize(12).font(FONT_BOLD_PATH || FONT_PATH)
         .fillColor('#0f3460');
      y = doc.text(line.slice(4), MARGIN, y + 10, {
        continued: false
      }).y + 2;
    }
    // Horizontal rule
    else if (line.startsWith('---')) {
      doc.moveTo(MARGIN, y + 4)
         .lineTo(PAGE_WIDTH - MARGIN, y + 4)
         .stroke('#cccccc');
      y += 12;
    }
    // Empty line
    else if (line.trim() === '') {
      y += 8;
    }
    // Regular text / bullet / table row
    else {
      doc.fontSize(10).font(FONT_PATH).fillColor('#333333');
      y = doc.text(line, MARGIN, y + 2, {
        width: PAGE_WIDTH - 2 * MARGIN,
        lineGap: 2
      }).y + 2;
    }

    doc.fillColor('#000000');
  }

  doc.end();

  return new Promise((resolve, reject) => {
    stream.on('finish', () => resolve(outputPath));
    stream.on('error', reject);
  });
}

// Export for use as module
module.exports = { generatePDF };

// CLI usage
if (require.main === module) {
  const args = process.argv.slice(2);
  const mdFile = args[0];
  const outFile = args[1] || 'report.pdf';
  const title = args[2] || '市场报告';

  const md = fs.readFileSync(mdFile, 'utf-8');
  generatePDF(md, outFile, title).then(() => {
    console.log(`PDF generated: ${outFile}`);
  });
}
```

#### CLI Usage

```bash
# From workspace root:
node skills/pdf-report-generator/scripts/generate_pdf.js input.md output.pdf "市场日报"
```

### Step 3: Verify output

- Open generated PDF and check:
  - Chinese characters render correctly
  - Headers/footers appear on every page
  - Page numbers increment properly
  - Tables align correctly
  - Color markers (🟢🔴) display
  - No content overflow at page boundaries

## Integration with daily-market-report

After `daily-market-report` produces a Markdown string, call this skill:

1. Save the Markdown to a temp file (e.g., `.tmp-report/latest.md`)
2. Run the Node.js script with the file
3. Delete the temp Markdown file
4. Return the PDF file path to the user

### Quick Function (Python → Node bridge)

```python
import subprocess
import tempfile
import os

def markdown_to_pdf(markdown_content, output_path, title="市场报告"):
    """Convert Markdown string to PDF file."""
    # Write temp markdown
    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.md', delete=False, encoding='utf-8'
    ) as f:
        f.write(markdown_content)
        md_path = f.name

    try:
        # Call Node.js generator
        subprocess.run([
            'node',
            'skills/pdf-report-generator/scripts/generate_pdf.js',
            md_path, output_path, title
        ], check=True, cwd=os.getenv('OPENCLAW_WORKSPACE', '.'))
        return output_path
    finally:
        os.unlink(md_path)
```

## Resources

### assets/
Place Chinese TrueType font files here for portable use:
- `NotoSansSC-Regular.ttf` — Main Chinese font
- `NotoSansSC-Bold.ttf` — Bold variant (optional)
- `NotoSansSC-Light.ttf` — Light variant (optional)

If no font file is in assets/, the script falls back to `C:\Windows\Fonts\msyh.ttc`.

### scripts/
- `generate_pdf.js` — Main PDF generation script (see template above)

## Notes

- A4 size: 210mm × 297mm (595.28 × 841.89 points)
- Standard margin: 72pt (1 inch) all sides
- Chinese font rendering requires a TTF/TTC with CJK glyphs
- pdfkit doesn't support CSS — all styling is programmatic
- For table-heavy reports, consider reducing font size to 8-9pt
- The script handles page breaks automatically by tracking Y position
- Color markers: 🟢↔green, 🔴↔red, can be mapped to fill colors
