/**
 * PDF Generator Script
 * Usage: node generate-pdf.js <url> <outputPath> [title]
 * 
 * Prerequisites:
 *   npm install playwright
 *   npx playwright install chromium
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const url = process.argv[2];
const outputPath = process.argv[3];
const title = process.argv[4] || 'document';

if (!url || !outputPath) {
  console.error('Usage: node generate-pdf.js <url> <outputPath> [title]');
  process.exit(1);
}

async function generatePDF() {
  console.log('Launching browser...');
  const browser = await chromium.launch({
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
  });
  
  try {
    const page = await browser.newPage();
    console.log('Loading page:', url);
    await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
    
    // Set page title
    await page.evaluate((t) => { document.title = t; }, title);
    
    console.log('Generating PDF...');
    await page.pdf({
      path: outputPath,
      format: 'A4',
      landscape: false,
      printBackground: true,
      margin: { top: '1cm', bottom: '1cm', left: '1cm', right: '1cm' }
    });
    
    const stats = fs.statSync(outputPath);
    console.log('PDF saved:', outputPath, 'Size:', (stats.size / 1024 / 1024).toFixed(2), 'MB');
  } finally {
    await browser.close();
  }
}

generatePDF().catch(e => {
  console.error('Error:', e.message);
  process.exit(1);
});
