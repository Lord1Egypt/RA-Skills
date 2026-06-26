#!/usr/bin/env node
/**
 * generate-carousel.js — Create Instagram carousel slides from video frames + text
 * 
 * Usage: node generate-carousel.js <content-plan.json> <frames-dir> <output-dir> [brand-config.json]
 * 
 * Generates 1080x1350 (4:5 portrait) carousel slides with:
 * - Video frame as background
 * - Semi-transparent overlay for text readability
 * - Quote/takeaway text overlay
 * - Consistent branding
 * 
 * Requires: npm install canvas (node-canvas)
 */

const fs = require('fs');
const path = require('path');

// Parse args
const contentPlanPath = process.argv[2];
const framesDir = process.argv[3];
const outputDir = process.argv[4];
const brandConfigPath = process.argv[5];

if (!contentPlanPath || !framesDir || !outputDir) {
  console.error('Usage: node generate-carousel.js <content-plan.json> <frames-dir> <output-dir> [brand-config.json]');
  process.exit(1);
}

// Default brand config
let brand = {
  primaryColor: '#000000',
  secondaryColor: '#FFFFFF',
  accentColor: '#8B5CF6',
  overlayOpacity: 0.55,
  width: 1080,
  height: 1350,
  seriesName: '',
  accountHandle: '',
  fontSizeTitle: 64,
  fontSizeBody: 48,
  fontSizeCTA: 40,
  padding: 80
};

if (brandConfigPath && fs.existsSync(brandConfigPath)) {
  const custom = JSON.parse(fs.readFileSync(brandConfigPath, 'utf8'));
  brand = { ...brand, ...custom };
}

async function main() {
  // Dynamic import for canvas (ESM/CJS compatibility)
  let createCanvas, loadImage;
  try {
    const canvasModule = require('canvas');
    createCanvas = canvasModule.createCanvas;
    loadImage = canvasModule.loadImage;
  } catch (e) {
    console.error('Error: canvas module not found. Install with: npm install canvas');
    console.error('Falling back to metadata-only mode (no image generation).');
    await generateMetadataOnly();
    return;
  }

  const contentPlan = JSON.parse(fs.readFileSync(contentPlanPath, 'utf8'));
  const slidesDir = path.join(outputDir, 'slides');
  fs.mkdirSync(slidesDir, { recursive: true });

  const carousels = contentPlan.carousels || [];
  
  for (const carousel of carousels) {
    const carouselDir = path.join(slidesDir, carousel.id);
    fs.mkdirSync(carouselDir, { recursive: true });

    for (let i = 0; i < carousel.slides.length; i++) {
      const slide = carousel.slides[i];
      const canvas = createCanvas(brand.width, brand.height);
      const ctx = canvas.getContext('2d');

      // Load and draw background frame
      if (slide.framePath && fs.existsSync(slide.framePath)) {
        try {
          const img = await loadImage(slide.framePath);
          // Cover-fit the image
          const scale = Math.max(brand.width / img.width, brand.height / img.height);
          const w = img.width * scale;
          const h = img.height * scale;
          const x = (brand.width - w) / 2;
          const y = (brand.height - h) / 2;
          ctx.drawImage(img, x, y, w, h);
        } catch (e) {
          // Fallback to solid color
          ctx.fillStyle = brand.primaryColor;
          ctx.fillRect(0, 0, brand.width, brand.height);
        }
      } else {
        ctx.fillStyle = brand.primaryColor;
        ctx.fillRect(0, 0, brand.width, brand.height);
      }

      // Draw overlay
      ctx.fillStyle = `rgba(0, 0, 0, ${brand.overlayOpacity})`;
      ctx.fillRect(0, 0, brand.width, brand.height);

      // Optional accent bar at top
      if (slide.type === 'hook' || i === 0) {
        ctx.fillStyle = brand.accentColor;
        ctx.fillRect(0, 0, brand.width, 6);
      }

      // Draw text
      ctx.fillStyle = brand.secondaryColor;
      ctx.textAlign = 'left';
      ctx.textBaseline = 'top';

      const padding = brand.padding;
      const maxWidth = brand.width - (padding * 2);

      if (slide.type === 'hook') {
        // Hook slide: large bold text
        ctx.font = `bold ${brand.fontSizeTitle}px "Helvetica Neue", Helvetica, Arial, sans-serif`;
        wrapText(ctx, slide.text, padding, brand.height * 0.35, maxWidth, brand.fontSizeTitle * 1.3);
      } else if (slide.type === 'cta') {
        // CTA slide
        ctx.font = `bold ${brand.fontSizeCTA}px "Helvetica Neue", Helvetica, Arial, sans-serif`;
        ctx.textAlign = 'center';
        wrapText(ctx, slide.text, brand.width / 2, brand.height * 0.4, maxWidth, brand.fontSizeCTA * 1.4);
        
        // Account handle
        if (brand.accountHandle) {
          ctx.font = `${brand.fontSizeCTA * 0.8}px "Helvetica Neue", Helvetica, Arial, sans-serif`;
          ctx.fillStyle = brand.accentColor;
          ctx.fillText(brand.accountHandle, brand.width / 2, brand.height * 0.6);
        }
      } else {
        // Quote/takeaway slides
        ctx.font = `${brand.fontSizeBody}px "Helvetica Neue", Helvetica, Arial, sans-serif`;
        wrapText(ctx, slide.text, padding, brand.height * 0.3, maxWidth, brand.fontSizeBody * 1.4);

        // Attribution
        if (slide.attribution) {
          ctx.font = `italic ${brand.fontSizeBody * 0.7}px "Helvetica Neue", Helvetica, Arial, sans-serif`;
          ctx.fillStyle = brand.accentColor;
          ctx.fillText(`— ${slide.attribution}`, padding, brand.height * 0.82);
        }
      }

      // Series name watermark (bottom)
      if (brand.seriesName) {
        ctx.font = `${24}px "Helvetica Neue", Helvetica, Arial, sans-serif`;
        ctx.fillStyle = `rgba(255, 255, 255, 0.4)`;
        ctx.textAlign = 'right';
        ctx.fillText(brand.seriesName, brand.width - padding, brand.height - 40);
      }

      // Slide counter
      ctx.font = `${20}px "Helvetica Neue", Helvetica, Arial, sans-serif`;
      ctx.fillStyle = `rgba(255, 255, 255, 0.5)`;
      ctx.textAlign = 'left';
      ctx.fillText(`${i + 1}/${carousel.slides.length}`, padding, brand.height - 40);

      // Save
      const outPath = path.join(carouselDir, `slide_${String(i + 1).padStart(2, '0')}.png`);
      const buffer = canvas.toBuffer('image/png');
      fs.writeFileSync(outPath, buffer);
      console.log(`  Generated: ${outPath}`);
    }

    console.log(`==> Carousel "${carousel.id}": ${carousel.slides.length} slides generated`);
  }

  // Save slide manifest
  const manifest = carousels.map(c => ({
    id: c.id,
    slideCount: c.slides.length,
    dir: path.join(slidesDir, c.id),
    slides: c.slides.map((s, i) => path.join(slidesDir, c.id, `slide_${String(i + 1).padStart(2, '0')}.png`))
  }));
  
  fs.writeFileSync(path.join(outputDir, 'slides-manifest.json'), JSON.stringify(manifest, null, 2));
  console.log(`\n==> All carousels generated. Manifest: ${path.join(outputDir, 'slides-manifest.json')}`);
}

function wrapText(ctx, text, x, y, maxWidth, lineHeight) {
  const words = text.split(' ');
  let line = '';
  let currentY = y;

  for (const word of words) {
    const testLine = line + word + ' ';
    const metrics = ctx.measureText(testLine);
    if (metrics.width > maxWidth && line !== '') {
      ctx.fillText(line.trim(), x, currentY);
      line = word + ' ';
      currentY += lineHeight;
    } else {
      line = testLine;
    }
  }
  ctx.fillText(line.trim(), x, currentY);
}

async function generateMetadataOnly() {
  const contentPlan = JSON.parse(fs.readFileSync(contentPlanPath, 'utf8'));
  const slidesDir = path.join(outputDir, 'slides');
  fs.mkdirSync(slidesDir, { recursive: true });

  const manifest = (contentPlan.carousels || []).map(c => ({
    id: c.id,
    slideCount: c.slides.length,
    dir: path.join(slidesDir, c.id),
    slides: c.slides.map((s, i) => ({
      index: i + 1,
      type: s.type,
      text: s.text,
      framePath: s.framePath || null,
      note: 'Image not generated — install canvas module'
    }))
  }));

  fs.writeFileSync(path.join(outputDir, 'slides-manifest.json'), JSON.stringify(manifest, null, 2));
  console.log('==> Metadata-only manifest saved (install canvas for image generation)');
}

main().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
