/**
 * generate_pdf.js — Markdown to PDF converter
 * Uses pdfkit (installed at workspace/.tmp-report)
 * Supports Chinese fonts, A4 layout, headers/footers, page numbers
 *
 * Usage:
 *   node generate_pdf.js input.md output.pdf "Report Title"
 *
 * Module usage:
 *   const { generatePDF } = require('./generate_pdf.js');
 *   await generatePDF(markdownString, 'output.pdf', 'My Report');
 */

const PDFDocument = require('pdfkit');
const fs = require('fs');
const path = require('path');

// === CONFIG ===
const WORKSPACE = process.env.OPENCLAW_WORKSPACE || '.';

// Try to find pdfkit
const PDFKIT_PATH = process.env.PDFKIT_PATH ||
  path.join(WORKSPACE, '.tmp-report', 'node_modules', 'pdfkit');

// Font paths (try assets first, then system font)
const ASSETS_DIR = path.join(__dirname, '..', 'assets');
const FONT_PATHS = [
  path.join(ASSETS_DIR, 'NotoSansSC-Regular.ttf'),
  path.join(ASSETS_DIR, 'NotoSansSC-Bold.ttf'),
  'C:/Windows/Fonts/msyh.ttc',
  'C:/Windows/Fonts/msyhbd.ttc',
];

const PAGE_WIDTH = 595.28;   // A4
const PAGE_HEIGHT = 841.89;  // A4
const MARGIN = 72;           // 1 inch
const HEADER_Y = 40;
const FOOTER_Y = PAGE_HEIGHT - 30;
const CONTENT_TOP = 72;
const CONTENT_BOTTOM = PAGE_HEIGHT - 72;

// === Helpers ===

function addHeader(doc, title) {
  doc.save();
  doc.fontSize(8).fillColor('#666666');
  doc.text(title || '市场报告', MARGIN, HEADER_Y, { align: 'left' });
  doc.moveTo(MARGIN, HEADER_Y + 14)
     .lineTo(PAGE_WIDTH - MARGIN, HEADER_Y + 14)
     .stroke('#cccccc');
  doc.restore();
}

function addFooter(doc, pageNum) {
  doc.save();
  doc.fontSize(8).fillColor('#999999');
  doc.text(`第 ${pageNum} 页`, MARGIN, FOOTER_Y, { align: 'center' });
  doc.restore();
}

function checkPageBreak(doc, y, title) {
  if (y > CONTENT_BOTTOM - 30) {
    doc.addPage();
    doc.pageNum = (doc.pageNum || 1) + 1;
    addHeader(doc, title);
    addFooter(doc, doc.pageNum);
    return CONTENT_TOP;
  }
  return y;
}

// === Main PDF Generator ===

async function generatePDF(markdownContent, outputPath, title) {
  title = title || '市场报告';

  // Resolve fonts
  const regularFont = FONT_PATHS.slice(0, 2).find(f => fs.existsSync(f)) || FONT_PATHS[2];
  const boldFont = FONT_PATHS.slice(1, 3).find(f => fs.existsSync(f)) || regularFont;

  const doc = new PDFDocument({
    size: 'A4',
    margins: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN },
    info: {
      Title: title,
      Author: 'OpenClaw 虾哥',
      Producer: 'pdf-report-generator',
      Creator: 'OpenClaw',
    }
  });

  const stream = fs.createWriteStream(outputPath);
  doc.pipe(stream);

  doc.pageNum = 1;
  addHeader(doc, title);
  addFooter(doc, 1);

  const lines = markdownContent.split('\n');
  let y = CONTENT_TOP;

  for (const line of lines) {
    y = checkPageBreak(doc, y, title);

    if (line.startsWith('# ')) {
      // H1
      doc.fontSize(18).fillColor('#1a1a2e');
      y = doc.text(line.slice(2).trim(), MARGIN, y + 16).y + 6;
    } else if (line.startsWith('## ')) {
      // H2
      doc.fontSize(14).fillColor('#16213e');
      y = doc.text(line.slice(3).trim(), MARGIN, y + 12).y + 4;
    } else if (line.startsWith('### ')) {
      // H3
      doc.fontSize(12).fillColor('#0f3460');
      y = doc.text(line.slice(4).trim(), MARGIN, y + 10).y + 2;
    } else if (line.startsWith('---')) {
      // Horizontal rule
      doc.moveTo(MARGIN, y + 4)
         .lineTo(PAGE_WIDTH - MARGIN, y + 4)
         .stroke('#cccccc');
      y += 12;
    } else if (line.trim() === '') {
      y += 8;
    } else if (line.startsWith('|') && line.endsWith('|')) {
      // Simple table row — print as-is with monospace-ish treatment
      doc.fontSize(9).fillColor('#333333');
      const text = line.replace(/\|/g, ' ').trim();
      y = doc.text(text, MARGIN, y + 2, {
        width: PAGE_WIDTH - 2 * MARGIN
      }).y + 2;
    } else {
      // Regular text / bullet
      doc.fontSize(10).fillColor('#333333');
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

// CLI
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length < 1) {
    console.error('Usage: node generate_pdf.js <input.md> [output.pdf] [title]');
    process.exit(1);
  }

  const mdFile = args[0];
  const outFile = args[1] || 'report.pdf';
  const reportTitle = args[2] || '市场报告';

  if (!fs.existsSync(mdFile)) {
    console.error(`File not found: ${mdFile}`);
    process.exit(1);
  }

  const md = fs.readFileSync(mdFile, 'utf-8');
  generatePDF(md, outFile, reportTitle).then((out) => {
    console.log(`✅ PDF generated: ${out}`);
  }).catch(err => {
    console.error('❌ PDF generation failed:', err.message);
    process.exit(1);
  });
}

module.exports = { generatePDF };
