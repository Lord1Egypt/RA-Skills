#!/usr/bin/env node
/**
 * 根据 slides.json 填充 HTML 模板，输出到 output/filled/
 * 用法: node scripts/fill-template.js [slides.json路径]
 * 默认: output/slides.json
 * 模板路径自动解析为脚本所在 skill 目录
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync, rmSync } from 'fs';
import { dirname, join, resolve } from 'path';
import { fileURLToPath } from 'url';
import { JSDOM } from 'jsdom';

const __dirname = dirname(fileURLToPath(import.meta.url));
const SKILL_ROOT = join(__dirname, '..');

const slidesPath = process.argv[2] || 'output/slides.json';
const manifestPath = join(SKILL_ROOT, 'templates/manifest.json');
const templatesDir = join(SKILL_ROOT, 'templates');
const outputDir = 'output/filled';

const manifest = JSON.parse(readFileSync(manifestPath, 'utf-8'));
if (!existsSync(slidesPath)) {
  console.error(`slides.json not found: ${slidesPath}`);
  process.exit(1);
}
const slides = JSON.parse(readFileSync(slidesPath, 'utf-8'));

const templateMap = new Map(manifest.templates.map(t => [t.id, t]));

// 清理上次生成的残留文件，避免旧 slide 混入新一次输出
try { rmSync(outputDir, { recursive: true, force: true }); } catch (_) {}
mkdirSync(outputDir, { recursive: true });

const lucideCache = new Map();
const LUCIDE_ICONS_DIR = join(SKILL_ROOT, 'node_modules/lucide-static/icons');

function normalizeLucideName(name) {
  return String(name || '')
    .trim()
    .replace(/^lucide:/i, '')
    .replace(/\s+/g, '-')
    .replace(/_/g, '-')
    .toLowerCase();
}

/** 优先从本地 lucide-static 读取，无网络依赖 */
function lucideSvgToDataUrl(iconName) {
  const n = normalizeLucideName(iconName);
  if (!n) return null;
  if (lucideCache.has(n)) return lucideCache.get(n);
  const localPath = join(LUCIDE_ICONS_DIR, `${n}.svg`);
  if (existsSync(localPath)) {
    const svg = readFileSync(localPath, 'utf-8');
    const dataUrl = `data:image/svg+xml;base64,${Buffer.from(svg, 'utf-8').toString('base64')}`;
    lucideCache.set(n, dataUrl);
    return dataUrl;
  }
  return null;
}

/** 本地图片路径转 data URL，供 srcdoc 内联使用 */
function localImageToDataUrl(value) {
  const cwd = process.cwd();
  const path = resolve(cwd, value.trim());
  if (!existsSync(path)) return null;
  const buf = readFileSync(path);
  const ext = (value.split('.').pop() || 'png').toLowerCase();
  const mime = ext === 'jpg' || ext === 'jpeg' ? 'image/jpeg' : ext === 'gif' ? 'image/gif' : ext === 'webp' ? 'image/webp' : 'image/png';
  return `data:${mime};base64,${buf.toString('base64')}`;
}

const urlToDataUrlCache = new Map();
/** 将 http(s) 图片转为 data URL，避免 srcdoc 内联时跨域/网络导致导出空白 */
async function urlToDataUrl(url) {
  if (urlToDataUrlCache.has(url)) return urlToDataUrlCache.get(url);
  try {
    const res = await fetch(url);
    if (!res.ok) return null;
    const buf = Buffer.from(await res.arrayBuffer());
    const ct = res.headers.get('content-type') || 'image/png';
    const mime = ct.split(';')[0].trim();
    const dataUrl = `data:${mime};base64,${buf.toString('base64')}`;
    urlToDataUrlCache.set(url, dataUrl);
    return dataUrl;
  } catch (e) {
    console.warn(`Failed to fetch image ${url}: ${e.message}`);
    return null;
  }
}

for (let i = 0; i < slides.length; i++) {
  const slide = slides[i];
  const template = templateMap.get(slide.templateId);
  if (!template) {
    console.error(`Slide ${i + 1}: Unknown templateId '${slide.templateId}'`);
    process.exit(1);
  }

  const htmlPath = join(templatesDir, template.file);
  const html = readFileSync(htmlPath, 'utf-8');
  const dom = new JSDOM(html);
  const document = dom.window.document;

  for (const slot of template.slots) {
    const value = slide.slots?.[slot.id];
    if (value === undefined || value === null || value === '') continue;

    const el = document.querySelector(slot.selector);
    if (!el) continue;

    if (slot.type === 'image') {
      let finalSrc = value;
      // 任意 image 槽位：支持 lucide:<icon-name>，从 unpkg 拉取 SVG 转 data URL
      const isLucide =
        typeof value === 'string' && value.trim().toLowerCase().startsWith('lucide:');
      if (isLucide) {
        finalSrc = lucideSvgToDataUrl(value);
        if (!finalSrc) {
          console.warn(`Lucide icon not found: ${value} (run npm install in skill dir)`);
          continue;
        }
      } else if (typeof value === 'string' && !value.trim().startsWith('http') && !value.trim().startsWith('data:')) {
        // 本地路径（如 output/images/slide-4.png）：转为 data URL 以支持 srcdoc 内联
        const dataUrl = localImageToDataUrl(value);
        if (!dataUrl) {
          console.warn(`Image not found: ${value} — keeping template default`);
          continue;
        }
        finalSrc = dataUrl;
      }
      if (el.tagName === 'IMG') {
        el.setAttribute('src', finalSrc);
      } else {
        const img = el.querySelector('img');
        if (img) img.setAttribute('src', finalSrc);
      }
    } else {
      if (slot.type === 'richtext') {
        el.innerHTML = value.replace(/\n/g, '<br>');
      } else {
        el.textContent = value;
      }
    }
  }

  // 将所有 http(s) 图片转为 data URL，确保 srcdoc 导出时背景/占位图不因网络问题变空白
  const imgs = document.querySelectorAll('img[src^="http://"], img[src^="https://"]');
  for (const img of imgs) {
    const src = img.getAttribute('src');
    if (!src) continue;
    const dataUrl = await urlToDataUrl(src);
    if (dataUrl) img.setAttribute('src', dataUrl);
  }

  const outPath = join(outputDir, `slide-${String(i + 1).padStart(2, '0')}-${template.id}.html`);
  writeFileSync(outPath, dom.serialize(), 'utf-8');
  console.log(`Wrote ${outPath}`);
}

console.log(`Done. Filled ${slides.length} slides to ${outputDir}/`);
