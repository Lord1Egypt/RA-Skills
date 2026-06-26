const { marked } = require('marked');
const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

// Find Chrome/Edge executable
function findBrowser() {
  // Check environment variables first
  if (process.env.CHROME_PATH && fs.existsSync(process.env.CHROME_PATH)) {
    return process.env.CHROME_PATH;
  }
  if (process.env.EDGE_PATH && fs.existsSync(process.env.EDGE_PATH)) {
    return process.env.EDGE_PATH;
  }

  // Default paths - try Edge first (often has fewer permission issues)
  const paths = [
    'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
  ];

  for (const p of paths) {
    if (fs.existsSync(p)) return p;
  }
  throw new Error('No Chrome/Edge browser found');
}

async function mdToPdf(inputFile, outputFile, options = {}) {
  const browserPath = findBrowser();
  console.log(`Using browser: ${browserPath}`);

  const mdContent = fs.readFileSync(inputFile, 'utf-8');
  const htmlContent = marked(mdContent);

  const fullHtml = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif;
      line-height: 1.6;
      max-width: 900px;
      margin: 0 auto;
      padding: 40px;
      color: #333;
    }
    h1 { font-size: 2em; border-bottom: 2px solid #eee; padding-bottom: 10px; }
    h2 { font-size: 1.5em; border-bottom: 1px solid #eee; padding-bottom: 8px; }
    h3 { font-size: 1.25em; }
    code {
      background: #f4f4f4;
      padding: 2px 6px;
      border-radius: 3px;
      font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
    }
    pre {
      background: #f8f8f8;
      padding: 16px;
      border-radius: 6px;
      overflow-x: auto;
      border: 1px solid #ddd;
    }
    pre code {
      background: none;
      padding: 0;
    }
    table {
      border-collapse: collapse;
      width: 100%;
      margin: 16px 0;
    }
    th, td {
      border: 1px solid #ddd;
      padding: 8px 12px;
      text-align: left;
    }
    th {
      background: #f4f4f4;
      font-weight: 600;
    }
    tr:nth-child(even) {
      background: #f9f9f9;
    }
    blockquote {
      border-left: 4px solid #ddd;
      margin: 0;
      padding: 8px 16px;
      color: #666;
    }
    img {
      max-width: 100%;
      height: auto;
    }
    a {
      color: #0366d6;
      text-decoration: none;
    }
    hr {
      border: none;
      border-top: 2px solid #eee;
      margin: 24px 0;
    }
  </style>
</head>
<body>
${htmlContent}
</body>
</html>`;

  const browser = await puppeteer.launch({
    executablePath: browserPath,
    headless: 'new',
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-gpu',
      '--no-first-run',
      '--no-default-browser-check',
      '--disable-extensions'
    ]
  });

  const page = await browser.newPage();
  await page.setContent(fullHtml, { waitUntil: 'networkidle0' });

  await page.pdf({
    path: outputFile,
    format: 'A4',
    margin: {
      top: options.marginTop || '20mm',
      bottom: options.marginBottom || '20mm',
      left: options.marginLeft || '15mm',
      right: options.marginRight || '15mm'
    },
    printBackground: true,
    displayHeaderFooter: options.showPageNumbers !== false,
    headerTemplate: options.headerTemplate || '<div></div>',
    footerTemplate: options.footerTemplate || `
      <div style="font-size: 10px; text-align: center; width: 100%;">
        <span class="pageNumber"></span> / <span class="totalPages"></span>
      </div>
    `
  });

  await browser.close();
  console.log(`PDF generated: ${outputFile}`);
}

// CLI
const args = process.argv.slice(2);
if (args.length < 1) {
  console.log('Usage: node convert.js <input.md> [output.pdf] [--no-page-numbers]');
  process.exit(1);
}

const inputFile = path.resolve(args[0]);
const outputFile = path.resolve(args[1] || inputFile.replace(/\.md$/, '.pdf'));
const showPageNumbers = !args.includes('--no-page-numbers');

if (!fs.existsSync(inputFile)) {
  console.error(`Error: File not found: ${inputFile}`);
  process.exit(1);
}

mdToPdf(inputFile, outputFile, { showPageNumbers })
  .then(() => console.log('Done!'))
  .catch(err => {
    console.error('Error:', err.message);
    process.exit(1);
  });
