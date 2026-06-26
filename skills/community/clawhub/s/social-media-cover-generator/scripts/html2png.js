/**
 * HTML to PNG Converter
 * Uses Puppeteer + snapdom to convert HTML files to PNG images
 * 
 * Usage: node html2png.js <input.html> [output.png]
 */

const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

async function htmlToPng(inputPath, outputPath) {
  const absoluteInputPath = path.resolve(inputPath);
  
  if (!fs.existsSync(absoluteInputPath)) {
    console.error(`Error: File does not exist ${absoluteInputPath}`);
    process.exit(1);
  }
  
  // Default output path
  if (!outputPath) {
    outputPath = absoluteInputPath.replace(/\.html?$/i, '.png');
  }
  
  const absoluteOutputPath = path.resolve(outputPath);
  
  console.log(`Converting: ${absoluteInputPath}`);
  console.log(`Output to: ${absoluteOutputPath}`);
  
  const browser = await puppeteer.launch({
    headless: 'new',
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox'
    ]
  });
  
  try {
    const page = await browser.newPage();
    
    // Set a large viewport to accommodate various sizes
    await page.setViewport({
      width: 2560,
      height: 2560,
      deviceScaleFactor: 1
    });
    
    // Load the HTML file
    await page.goto(`file:///${absoluteInputPath.replace(/\\/g, '/')}`, {
      waitUntil: 'networkidle0',
      timeout: 30000
    });
    
    // Wait for snapdom to load
    await page.waitForFunction(() => typeof snapdom !== 'undefined', { timeout: 10000 });
    
    // Get the cover element
    const cover = await page.$('#cover');
    if (!cover) {
      throw new Error('#cover element not found');
    }
    
    // Use snapdom to convert to canvas
    const canvas = await page.evaluate(async () => {
      const coverEl = document.getElementById('cover');
      const canvasEl = await snapdom.toCanvas(coverEl);
      return canvasEl.toDataURL('image/png');
    });
    
    // Save the image
    const base64Data = canvas.replace(/^data:image\/png;base64,/, '');
    fs.writeFileSync(absoluteOutputPath, Buffer.from(base64Data, 'base64'));
    
    console.log(`✓ Successfully generated: ${absoluteOutputPath}`);
    
  } catch (error) {
    console.error(`Conversion failed: ${error.message}`);
    process.exit(1);
  } finally {
    await browser.close();
  }
}

// Command line arguments
const args = process.argv.slice(2);
if (args.length < 1) {
  console.log('Usage: node html2png.js <input.html> [output.png]');
  console.log('');
  console.log('Examples:');
  console.log('  node html2png.js cover.html');
  console.log('  node html2png.js cover.html output.png');
  process.exit(0);
}

htmlToPng(args[0], args[1]);