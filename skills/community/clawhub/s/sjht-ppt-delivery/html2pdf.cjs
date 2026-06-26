#!/usr/bin/env node
/**
 * html2pdf.cjs — Convert HTML slide deck to multi-page PDF via screenshots.
 *
 * Usage: node html2pdf.cjs <input.html> <output.pdf> [--width 1920] [--height 1080]
 *
 * Dependencies: puppeteer-core (global), pdf-lib (global)
 * Browser: chromium-browser
 */
const puppeteer = require('puppeteer-core');
const { PDFDocument } = require('pdf-lib/cjs/index.js');
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
let inputFile = null;
let outputFile = null;
let width = 1920;
let height = 1080;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--width' && args[i + 1]) width = parseInt(args[++i]);
  else if (args[i] === '--height' && args[i + 1]) height = parseInt(args[++i]);
  else if (!inputFile) inputFile = args[i];
  else if (!outputFile) outputFile = args[i];
}

if (!inputFile || !outputFile) {
  console.error('Usage: node html2pdf.cjs <input.html> <output.pdf> [--width 1920] [--height 1080]');
  process.exit(1);
}

inputFile = path.resolve(inputFile);
outputFile = path.resolve(outputFile);

if (!fs.existsSync(inputFile)) {
  console.error(`File not found: ${inputFile}`);
  process.exit(1);
}

(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/usr/bin/chromium-browser',
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
  });

  const page = await browser.newPage();
  await page.setViewport({ width, height });
  await page.goto(`file://${inputFile}`, { waitUntil: 'networkidle0', timeout: 30000 });

  // Wait for fonts and animations
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 3000));

  const slideCount = await page.evaluate(() => document.querySelectorAll('.slide').length);
  if (slideCount === 0) {
    console.error('No .slide elements found in HTML');
    await browser.close();
    process.exit(1);
  }

  const pdfDoc = await PDFDocument.create();

  for (let i = 0; i < slideCount; i++) {
    await page.evaluate((idx) => {
      const slides = document.querySelectorAll('.slide');
      slides[idx].scrollIntoView({ block: 'start' });
      slides[idx].classList.add('visible');
    }, i);
    await new Promise(r => setTimeout(r, 800));

    const buf = await page.screenshot({ type: 'png', fullPage: false });
    const img = await pdfDoc.embedPng(buf);
    const pg = pdfDoc.addPage([width, height]);
    pg.drawImage(img, { x: 0, y: 0, width, height });
    console.log(`Page ${i + 1}/${slideCount} done`);
  }

  const pdfBytes = await pdfDoc.save();
  fs.writeFileSync(outputFile, pdfBytes);

  await browser.close();
  console.log(`PDF generated: ${outputFile} (${slideCount} pages, ${(pdfBytes.length / 1024).toFixed(0)} KB)`);
})();
