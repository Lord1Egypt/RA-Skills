#!/usr/bin/env node

const QRCode = require('qrcode');
const path = require('path');
const fs = require('fs');

async function generateQRCode(text, outputPath) {
  if (!text) {
    console.error('Usage: node generate.js <text_or_url> [output_file]');
    process.exit(1);
  }

  // Default output path
  const output = outputPath || path.join(process.cwd(), 'qrcode.png');

  try {
    // Generate QR code as PNG
    const buffer = await QRCode.toBuffer(text, {
      type: 'png',
      width: 300,
      margin: 2,
      color: {
        dark: '#000000',
        light: '#ffffff'
      }
    });

    // Ensure directory exists
    const dir = path.dirname(output);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    // Write file
    fs.writeFileSync(output, buffer);
    console.log(`QR code saved to: ${output}`);
    console.log(`Content: ${text}`);
  } catch (err) {
    console.error('Error generating QR code:', err.message);
    process.exit(1);
  }
}

// Get arguments
const args = process.argv.slice(2);
const text = args[0];
const outputFile = args[1];

generateQRCode(text, outputFile);
