#!/usr/bin/env node
/**
 * 将 HTML 无缝转为 PPTX（高保真）
 * 每个 HTML 在独立 iframe 中加载，保持原始样式，不做合并/作用域
 *
 * 用法: node scripts/html-to-pptx-dom.js [filled目录] [输出文件]
 * 默认: output/filled output/presentation-dom.pptx
 */

import { readdirSync, readFileSync, writeFileSync, existsSync, mkdirSync, unlinkSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import puppeteer from 'puppeteer';

const __dirname = dirname(fileURLToPath(import.meta.url));
const SKILL_ROOT = join(__dirname, '..');

const inputDir = process.argv[2] || join(process.cwd(), 'output/filled');

function defaultOutputPath() {
  const ts = new Date().toISOString().replace(/[:T]/g, '-').replace(/\..+/, '');
  return join(process.cwd(), `output/presentation-${ts}.pptx`);
}

const outputPath = process.argv[3] || defaultOutputPath();

if (!existsSync(inputDir)) {
  console.error(`Directory not found: ${inputDir}`);
  process.exit(1);
}

const files = readdirSync(inputDir)
  .filter(f => f.endsWith('.html') && /slide-\d+/.test(f))
  .sort((a, b) => {
    const n1 = parseInt((a.match(/slide-(\d+)/) || [])[1] || '0');
    const n2 = parseInt((b.match(/slide-(\d+)/) || [])[1] || '0');
    return n1 - n2;
  });

if (files.length === 0) {
  console.error(`No slide HTML files in ${inputDir}`);
  process.exit(1);
}

// 用 srcdoc 内联每个 HTML，避免 file:// 跨域无法访问 contentDocument
function escapeForSrcdoc(html) {
  return html
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

const iframeParts = [];
for (let i = 0; i < files.length; i++) {
  const html = readFileSync(join(inputDir, files[i]), 'utf-8');
  iframeParts.push(`<iframe id="slide-${i}" srcdoc="${escapeForSrcdoc(html)}" width="1920" height="1080" style="display:block;border:none;"></iframe>`);
}

const tempDir = join(SKILL_ROOT, 'temp');
mkdirSync(tempDir, { recursive: true });
const containerPath = join(tempDir, 'pptx-container.html');
const containerContent = `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>* { margin: 0; padding: 0; } body { width: 1920px; }</style>
</head>
<body>
${iframeParts.join('\n')}
</body>
</html>`;

writeFileSync(containerPath, containerContent, 'utf-8');

const bundlePath = join(SKILL_ROOT, 'node_modules/dom-to-pptx/dist/dom-to-pptx.bundle.js');
if (!existsSync(bundlePath)) {
  console.error('dom-to-pptx bundle not found. Run: npm install dom-to-pptx');
  process.exit(1);
}

const containerUrl = `file://${containerPath}`;

console.log('Launching browser...');
const browser = await puppeteer.launch({ headless: true });
const page = await browser.newPage();

await page.setViewport({ width: 1920, height: 1080 * files.length });
try {
  await page.goto(containerUrl, { waitUntil: 'networkidle0', timeout: 30000 });
} catch (e) {
  console.warn(`Page navigation warning: ${e.message}`);
}

await new Promise((r) => setTimeout(r, 1000));
for (let i = 0; i < 20; i++) {
  const ready = await page.evaluate(() => {
    const iframes = document.querySelectorAll('iframe');
    return Array.from(iframes).every((f) => {
      try {
        return f.contentDocument?.querySelector('.slide');
      } catch (_) {
        return false;
      }
    });
  });
  if (ready) break;
  if (i === 19) console.warn('Timeout waiting for all iframes to load — proceeding anyway');
  await new Promise((r) => setTimeout(r, 300 * Math.min(i + 1, 5)));
}

// 等待所有图片加载完成，避免导出时背景/图标为空白
await page.evaluate(async () => {
  const iframes = document.querySelectorAll('iframe');
  const imgs = [];
  for (const f of iframes) {
    try {
      imgs.push(...(f.contentDocument?.querySelectorAll('img') || []));
    } catch (_) {}
  }
  await Promise.all(imgs.map((img) => {
    if (img.complete) return Promise.resolve();
    return new Promise((resolve) => {
      img.onload = img.onerror = resolve;
      setTimeout(resolve, 5000);
    });
  }));
});
await new Promise((r) => setTimeout(r, 500));

await page.addScriptTag({ path: bundlePath });

const result = await page.evaluate(async () => {
  const exportToPptx = window.domToPptx?.exportToPptx;
  if (!exportToPptx) return { error: 'exportToPptx not found' };

  const slides = [];
  const iframes = document.querySelectorAll('iframe');
  for (const iframe of iframes) {
    try {
      const doc = iframe.contentDocument;
      if (!doc) continue;
      const slide = doc.querySelector('.slide');
      if (slide) slides.push(slide);
    } catch (_) {}
  }

  if (slides.length === 0) return { error: 'No slide elements found in iframes' };

  try {
    const blob = await exportToPptx(slides, { fileName: 'export.pptx', skipDownload: true });
    const buf = await blob.arrayBuffer();
    const bytes = new Uint8Array(buf);
    let binary = '';
    const chunkSize = 8192;
    for (let i = 0; i < bytes.length; i += chunkSize) {
      binary += String.fromCharCode(...bytes.subarray(i, i + chunkSize));
    }
    return { base64: btoa(binary) };
  } catch (e) {
    return { error: String(e.message || e) };
  }
});

await browser.close();
try { unlinkSync(containerPath); } catch (_) {}

if (result.error) {
  console.error('dom-to-pptx error:', result.error);
  process.exit(1);
}

mkdirSync(dirname(outputPath), { recursive: true });
writeFileSync(outputPath, Buffer.from(result.base64, 'base64'));
console.log(`Done. ${files.length} slides saved to ${outputPath}`);
