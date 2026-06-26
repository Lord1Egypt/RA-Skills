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

// Strip wrapper divs (no style)
let changed = true;
while (changed) {
  changed = false;
  const m = content.match(/^\s*<div(?:\s+(?:class|id)="[^"]*")*\s*>\s*([\s\S]*)\s*<\/div>\s*$/);
  if (m && !content.match(/^\s*<div[^>]*style=/)) {
    const openTag = content.match(/^\s*<div[^>]*>/);
    if (openTag && !openTag[0].includes('style=')) {
      content = m[1].trim();
      changed = true;
    }
  }
}

// Step 2: Sanitize (with div → section)
let result = content;

// KEY: div → section
result = result.replace(/<div(\s)/g, '<section$1');
result = result.replace(/<div>/g, '<section>');
result = result.replace(/<\/div>/g, '</section>');

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

// Step 3: Compress
let compressed = result
  .replace(/<!--[\s\S]*?-->/g, '')
  .replace(/>\s+</g, '><')
  .replace(/\s{2,}/g, ' ')
  .trim();

console.log('=== Final stats ===');
console.log('Length:', compressed.length);
console.log('Within 20K limit:', compressed.length <= 20000);
console.log('<section count:', (compressed.match(/<section/g) || []).length);
console.log('</section> count:', (compressed.match(/<\/section>/g) || []).length);
console.log('<div count:', (compressed.match(/<div/g) || []).length);
console.log('style= count:', (compressed.match(/style=/g) || []).length);
console.log('background count:', (compressed.match(/background/g) || []).length);
console.log('border-left count:', (compressed.match(/border-left/g) || []).length);
console.log('');
console.log('First 300 chars:', compressed.substring(0, 300));
console.log('');

// Save for inspection
fs.writeFileSync(path.join(__dirname, 'debug4-output.html'), compressed);
console.log('Saved to debug4-output.html');
