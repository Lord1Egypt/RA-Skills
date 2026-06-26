const sharp = require('sharp');
const path = require('path');
const fs = require('fs');

const args = process.argv.slice(2);
const svgPath = args[0] || path.join(__dirname, 'icon.svg');
const pngPath = args[1] || svgPath.replace('.svg', '.png');
const size = parseInt(args[2]) || 1024;

async function convertSvgToPng() {
  try {
    if (!fs.existsSync(svgPath)) {
      console.error(`❌ Error: File not found: ${svgPath}`);
      process.exit(1);
    }

    await sharp(svgPath)
      .resize(size, size)
      .png()
      .toFile(pngPath);

    console.log(`✅ Successfully converted ${path.basename(svgPath)} to ${path.basename(pngPath)} (${size}x${size})`);
  } catch (error) {
    console.error(`❌ Error: ${error.message}`);
    process.exit(1);
  }
}

convertSvgToPng();