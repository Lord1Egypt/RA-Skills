import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const html = fs.readFileSync(path.join(__dirname, '..', 'blog-post-wechat.html'), 'utf-8');

// Step 1: Extract
const startMarker = '<!-- ========== ARTICLE CONTENT START ========== -->';
const endMarker = '<!-- ========== ARTICLE CONTENT END ========== -->';
let content = html.substring(html.indexOf(startMarker) + startMarker.length, html.indexOf(endMarker));
content = content.replace(/<!--[\s\S]*?-->/g, '').trim();

console.log('=== Step 1: After extract ===');
console.log('Length:', content.length);
console.log('First 100 chars:', content.substring(0, 100));
console.log('');

// Step 2: Strip wrapper
let changed = true;
let strippedCount = 0;
while (changed) {
  changed = false;
  const m = content.match(/^\s*<div(?:\s+(?:class|id)="[^"]*")*\s*>\s*([\s\S]*)\s*<\/div>\s*$/);
  if (m && !content.match(/^\s*<div[^>]*style=/)) {
    const openTag = content.match(/^\s*<div[^>]*>/);
    if (openTag && !openTag[0].includes('style=')) {
      content = m[1].trim();
      changed = true;
      strippedCount++;
    }
  }
}

console.log('=== Step 2: After strip wrapper ===');
console.log('Stripped layers:', strippedCount);
console.log('Length:', content.length);
console.log('First 200 chars:', content.substring(0, 200));
console.log('');

// Check: does content still start with the styled outer div?
const startsWithStyleDiv = content.startsWith('<div style=');
console.log('Starts with <div style=:', startsWithStyleDiv);
console.log('');

// Step 3: Sanitize (simplified)
let result = content;
result = result.replace(/font-family\s*:[^;"]*(?:'[^']*'[^;"]*|"[^"]*"[^;"]*)*;?/g, '');
result = result.replace(/\s+id="[^"]*"/g, '');
result = result.replace(/\s+class="[^"]*"/g, '');
result = result.replace(/rgba\(255,\s*255,\s*255,\s*0\.12\)/g, '#FFFFFF1F');
result = result.replace(/rgba\(255,\s*255,\s*255,\s*0\.2\)/g, '#FFFFFF33');
result = result.replace(/rgba\(255,\s*255,\s*255,\s*0\.8\)/g, '#FFFFFFCC');
result = result.replace(/rgba\(255,\s*255,\s*255,\s*0\.55\)/g, '#FFFFFF8C');
result = result.replace(/rgba\(0,\s*0,\s*0,\s*[\d.]+\)/g, '#00000026');
result = result.replace(/max-width\s*:\s*578px/g, 'width:100%');
result = result.replace(/position\s*:\s*[^;]+;?/g, '');
result = result.replace(/z-index\s*:\s*[^;]+;?/g, '');
result = result.replace(/;color:#2D2A3E(?=[";}])/g, '');
result = result.replace(/color:#2D2A3E;/g, '');
result = result.replace(/;\s*;/g, ';');
result = result.replace(/style=";\s*/g, 'style="');
result = result.replace(/;\s*"/g, '"');
result = result.replace(/style="\s*"/g, '');

console.log('=== Step 3: After sanitize ===');
console.log('Length:', result.length);
console.log('First 300 chars:', result.substring(0, 300));
console.log('');

// Step 4: Compress
let compressed = result
  .replace(/<!--[\s\S]*?-->/g, '')
  .replace(/>\s+</g, '><')
  .replace(/\s{2,}/g, ' ')
  .trim();

console.log('=== Step 4: After compress ===');
console.log('Length:', compressed.length);
console.log('First 500 chars:', compressed.substring(0, 500));
console.log('');
console.log('style= count:', (compressed.match(/style=/g) || []).length);
console.log('background count:', (compressed.match(/background/g) || []).length);
console.log('border-left count:', (compressed.match(/border-left/g) || []).length);

// Critical check: save to file for inspection
fs.writeFileSync(path.join(__dirname, 'debug3-output.html'), compressed);
console.log('\nSaved to debug3-output.html for inspection');
