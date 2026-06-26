#!/usr/bin/env node
const PptxGenJS = require('/root/.openclaw/workspace/node_modules/pptxgenjs');
const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

const C = {
  navy: '13293D', navy2: '1B3A57', blue: '2A628F', teal: '2CA6A4', gold: 'D5A44A',
  mint: 'DDF4F1', light: 'F5F8FC', white: 'FFFFFF', dark: '18222D', mid: '5C6773',
  line: 'D6E1EB', gold_bg: 'FBF7EE', gold2: 'ECD7A4'
};

const FONT = 'Microsoft YaHei';
const FONT_HEAD = 'Microsoft YaHei';
const SIZE = {
  headerTitle: 25,
  headerSubtitle: 10.5,
  pageNum: 10,
  titleZh: 27,
  titleEn: 17,
  titleMeta: 17.5,
  titleAuthors: 14.5,
  smallLabel: 12,
  smallText: 11,
  agendaIndex: 14,
  agendaTitle: 21,
  sectionHeading: 17.5,
  body: 16.5,
  bodyDense: 15,
  resultLabel: 19,
  resultCaption: 14,
  resultFigRef: 10.5,
  mechanismLabel: 18,
  mechanismNode: 14,
  mechanismExplain: 14,
  takeaway: 18,
  closingTitle: 30,
  closingSubtitle: 21,
  closingNote: 14.5,
  badge: 13
};

function softShadow() { return { type: 'outer', color: '000000', blur: 2, offset: 1, angle: 45, opacity: 0.12 }; }
function sanitize(name) {
  return String(name || 'output').replace(/[\\/:*?"<>|]/g, '').replace(/\s+/g, ' ').trim();
}
function parseArgs(argv) {
  const out = {};
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) out[a.slice(2)] = argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[++i] : true;
  }
  return out;
}
function addBg(slide, dark = false) {
  if (dark) {
    slide.addShape('rect', { x: 0, y: 0, w: 13.333, h: 7.5, fill: { color: C.navy } });
    slide.addShape('rect', { x: 8.7, y: 0, w: 4.633, h: 7.5, fill: { color: C.navy2 } });
  } else {
    slide.addShape('rect', { x: 0, y: 0, w: 13.333, h: 7.5, fill: { color: C.light } });
    slide.addShape('rect', { x: 0, y: 0, w: 13.333, h: 0.78, fill: { color: C.navy } });
    slide.addShape('rect', { x: 0, y: 7.18, w: 13.333, h: 0.32, fill: { color: 'E8EEF4' } });
  }
}
function addHeader(slide, title, subtitle='') {
  slide.addText(title, { x: 0.3, y: 0.16, w: 10.5, h: 0.42, fontFace: FONT_HEAD, fontSize: SIZE.headerTitle, bold: true, color: C.white, margin: 0, fit: 'shrink' });
  if (subtitle) slide.addText(subtitle, { x: 8.8, y: 0.2, w: 3.9, h: 0.24, fontFace: FONT, fontSize: SIZE.headerSubtitle, color: 'DCE7F1', align: 'right', margin: 0, fit: 'shrink' });
}
function addPageNum(slide, n) { slide.addText(String(n), { x: 12.4, y: 7.02, w: 0.28, h: 0.14, fontFace: FONT, fontSize: SIZE.pageNum, color: '6B7280', align: 'right', margin: 0, fit: 'shrink' }); }
function addLeftAccent(slide, x, y, h, color) { slide.addShape('rect', { x, y, w: 0.12, h, fill: { color }, line: { color } }); }
function addBulletText(slide, text, opts={}) {
  slide.addText('• ' + text, { x: opts.x, y: opts.y, w: opts.w, h: opts.h, fontFace: FONT, fontSize: opts.fontSize || SIZE.body, color: opts.color || C.dark, margin: 0.03, valign: 'top', fit: 'shrink' });
}
function download(url, outPath) {
  return new Promise((resolve, reject) => {
    const lib = url.startsWith('https') ? https : http;
    lib.get(url, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) return resolve(download(res.headers.location, outPath));
      if (res.statusCode !== 200) return reject(new Error('HTTP ' + res.statusCode));
      const f = fs.createWriteStream(outPath);
      res.pipe(f);
      f.on('finish', () => f.close(() => resolve(outPath)));
      f.on('error', reject);
    }).on('error', reject);
  });
}
async function ensureAsset(url, cacheDir) {
  if (!url) return null;
  if (fs.existsSync(url)) return url;
  const ext = path.extname(new URL(url).pathname) || '.jpg';
  const crypto = require('crypto');
  const base = crypto.createHash('sha1').update(String(url)).digest('hex');
  const out = path.join(cacheDir, base + ext);
  if (fs.existsSync(out) && fs.statSync(out).size > 0) return out;
  try { await download(url, out); return out; } catch { return null; }
}
function titleSlide(pptx, deck, page) {
  const s = pptx.addSlide(); addBg(s, true);
  s.addShape('rect', { x: 0.65, y: 0.8, w: 0.18, h: 5.2, fill: { color: C.gold }, line: { color: C.gold } });
  s.addText(deck.paper_meta.title_zh || deck.paper_meta.title_en, { x: 1.06, y: 1.02, w: 7.05, h: 1.55, fontFace: FONT_HEAD, fontSize: SIZE.titleZh, bold: true, color: C.white, margin: 0, fit: 'shrink' });
  s.addText(deck.paper_meta.title_en, { x: 1.08, y: 2.82, w: 6.95, h: 1.05, fontFace: FONT, fontSize: SIZE.titleEn, italic: true, color: 'D5E4F0', margin: 0, fit: 'shrink' });
  s.addText(`${deck.paper_meta.journal || ''}  ${deck.paper_meta.year || ''}`.trim(), { x: 1.1, y: 4.15, w: 4.8, h: 0.25, fontFace: FONT, fontSize: SIZE.titleMeta, bold: true, color: 'C9DBEA', margin: 0, fit: 'shrink' });
  s.addText(deck.paper_meta.author_display || (deck.paper_meta.first_author ? `${deck.paper_meta.first_author} et al.` : (deck.paper_meta.authors || []).join('、')), { x: 1.1, y: 4.72, w: 7.0, h: 0.7, fontFace: FONT, fontSize: SIZE.titleAuthors, color: C.white, margin: 0, valign: 'top', fit: 'shrink' });
  s.addShape('rect', { x: 8.95, y: 1.15, w: 3.45, h: 1.05, fill: { color: '1D405D' }, line: { color: C.gold, width: 1 } });
  s.addText('研究主线', { x: 9.1, y: 1.24, w: 1.2, h: 0.2, fontFace: FONT, fontSize: SIZE.smallLabel, bold: true, color: C.gold, margin: 0, fit: 'shrink' });
  s.addText('免疫调节 → 神经炎症↓ → Aβ/Tau↓ → 神经保护↑', { x: 9.1, y: 1.55, w: 3.0, h: 0.42, fontFace: FONT, fontSize: 10.6, color: 'C9DBEA', margin: 0, fit: 'shrink' });
  s.addShape('rect', { x: 8.95, y: 2.62, w: 3.45, h: 2.4, fill: { color: '1D405D' }, line: { color: C.teal, width: 1 } });
  s.addText('关键词', { x: 9.1, y: 2.72, w: 1, h: 0.22, fontFace: FONT, fontSize: SIZE.smallLabel, bold: true, color: C.teal, margin: 0, fit: 'shrink' });
  s.addText('Fingolimod\nAPP/PS1\nAβ\nTau\nLymphocyte\nNeurodegeneration', { x: 9.1, y: 3.05, w: 3.0, h: 1.8, fontFace: FONT, fontSize: SIZE.smallText, color: 'C9DBEA', margin: 0, fit: 'shrink' });
  addPageNum(s, page);
}
function agendaSlide(pptx, page) {
  const s = pptx.addSlide(); addBg(s); addHeader(s, '目录'); addPageNum(s, page);
  s.addShape('rect', { x: 0.7, y: 1.2, w: 12.0, h: 5.55, fill: { color: C.white }, shadow: softShadow() });
  const items = ['全文概述','研究背景与科学问题','研究设计与技术路线','关键结果','机制主线总结','优点与局限','Take-home message'];
  items.forEach((t, i) => {
    const y = 1.48 + i * 0.72;
    s.addShape('ellipse', { x: 1.05, y, w: 0.5, h: 0.5, fill: { color: i >= 3 && i <=4 ? C.gold : C.teal } });
    s.addText(String(i+1).padStart(2,'0'), { x: 1.05, y, w: 0.5, h: 0.5, fontFace: FONT, fontSize: SIZE.agendaIndex, bold: true, color: C.white, align: 'center', valign: 'middle', margin: 0, fit: 'shrink' });
    s.addText(t, { x: 1.82, y: y+0.02, w: 9.8, h: 0.3, fontFace: FONT, fontSize: SIZE.agendaTitle, bold: true, color: C.dark, margin: 0, fit: 'shrink' });
    if (i < items.length - 1) s.addShape('line', { x: 1.82, y: y+0.58, w: 9.8, h: 0, line: { color: 'E8EEF4', width: 1 } });
  });
}
function genericTextSlide(pptx, slideData, page) {
  const s = pptx.addSlide(); addBg(s); addHeader(s, slideData.title, slideData.subtitle || ''); addPageNum(s, page);
  s.addShape('rect', { x: 0.7, y: 1.18, w: 12.0, h: 5.56, fill: { color: C.white }, shadow: softShadow() });
  addLeftAccent(s, 0.7, 1.18, 5.56, slideData.slide_type === 'limitations' ? C.gold : C.teal);
  if (slideData.sections?.length) {
    const cols = slideData.sections.length >= 3 ? 3 : Math.min(2, slideData.sections.length);
    const colW = cols === 3 ? 3.55 : 5.5; const gap = cols === 3 ? 0.28 : 0.45;
    slideData.sections.forEach((sec, i) => {
      const col = i % cols; const row = Math.floor(i / cols); const x = 1.05 + col * (colW + gap); const y = 1.4 + row * 2.5;
      s.addText(sec.heading, { x, y, w: colW, h: 0.28, fontFace: FONT, fontSize: SIZE.sectionHeading, bold: true, color: slideData.slide_type === 'limitations' ? C.gold : C.teal, margin: 0, fit: 'shrink' });
      s.addShape('line', { x, y: y+0.34, w: colW, h: 0, line: { color: C.line, width: 1 } });
      (sec.points || []).forEach((p, j) => addBulletText(s, p, { x, y: y+0.5 + j*0.78, w: colW, h: 0.7, fontSize: SIZE.bodyDense }));
    });
  } else if (slideData.bullets?.length) {
    slideData.bullets.forEach((b, i) => addBulletText(s, b, { x: 1.0, y: 1.55 + i*0.9, w: 11.1, h: 0.75, fontSize: slideData.slide_type === 'takeaway' ? SIZE.takeaway : SIZE.body }));
  }
}
function resultSlide(pptx, slideData, page) {
  const s = pptx.addSlide(); addBg(s); addHeader(s, slideData.title, slideData.subtitle || ''); addPageNum(s, page);
  const hasImage = !!(slideData.localImagePath && fs.existsSync(slideData.localImagePath) && fs.statSync(slideData.localImagePath).size > 0);
  if (hasImage) {
    s.addShape('rect', { x: 0.48, y: 1.03, w: 4.04, h: 5.9, fill: { color: C.white }, shadow: softShadow() });
    addLeftAccent(s, 0.48, 1.03, 5.9, C.gold);
    s.addText('核心结论', { x: 0.82, y: 1.22, w: 3.2, h: 0.28, fontFace: FONT, fontSize: SIZE.resultLabel, bold: true, color: C.navy, margin: 0, fit: 'shrink' });
    (slideData.bullets || []).slice(0,4).forEach((b, i) => addBulletText(s, b, { x: 0.78, y: 1.62 + i*1.05, w: 3.42, h: 0.92, fontSize: SIZE.body }));
    s.addShape('rect', { x: 4.82, y: 1.03, w: 8.02, h: 3.98, fill: { color: 'F4F7FA' }, line: { color: 'C8D5E1', width: 1 } });
    s.addImage({ path: slideData.localImagePath, x: 4.91, y: 1.12, w: 7.84, h: 3.8, sizing: { type: 'contain', w: 7.84, h: 3.8 } });
    s.addShape('rect', { x: 4.82, y: 5.2, w: 8.02, h: 1.55, fill: { color: C.white }, line: { color: 'C8D5E1', width: 1 } });
    s.addShape('rect', { x: 5.0, y: 5.34, w: 0.72, h: 0.26, fill: { color: C.mint }, line: { color: C.mint } });
    s.addText('图解', { x: 5.0, y: 5.34, w: 0.72, h: 0.26, fontFace: FONT, fontSize: SIZE.smallLabel, bold: true, color: C.teal, align: 'center', valign: 'middle', margin: 0, fit: 'shrink' });
    const figRef = (slideData.figure_refs || [])[0] || '';
    s.addText(figRef, { x: 11.0, y: 5.38, w: 1.4, h: 0.18, fontFace: FONT, fontSize: SIZE.resultFigRef, color: C.mid, align: 'right', margin: 0, fit: 'shrink' });
    const exp = slideData.figure_explanations?.[0]?.explanation || '';
    s.addText(exp, { x: 5.08, y: 5.68, w: 7.1, h: 0.9, fontFace: FONT, fontSize: SIZE.resultCaption, color: C.dark, margin: 0, valign: 'top', fit: 'shrink' });
  } else {
    s.addShape('rect', { x: 0.72, y: 1.18, w: 12.0, h: 5.56, fill: { color: C.white }, shadow: softShadow() });
    addLeftAccent(s, 0.72, 1.18, 5.56, C.gold);
    s.addText('关键内容', { x: 1.02, y: 1.42, w: 2.2, h: 0.3, fontFace: FONT, fontSize: SIZE.resultLabel, bold: true, color: C.navy, margin: 0, fit: 'shrink' });
    (slideData.bullets || []).slice(0,5).forEach((b, i) => {
      s.addShape('roundRect', { x: 1.0, y: 1.95 + i*0.83, w: 11.2, h: 0.66, rectRadius: 0.05, fill: { color: i % 2 === 0 ? 'EEF7F6' : 'F8FBFD' }, line: { color: i % 2 === 0 ? 'EEF7F6' : 'F8FBFD' } });
      s.addText(String(i+1).padStart(2,'0'), { x: 1.22, y: 2.08 + i*0.83, w: 0.5, h: 0.22, fontFace: FONT, fontSize: 18, bold: true, color: i % 2 === 0 ? C.teal : C.gold, margin: 0, fit: 'shrink' });
      s.addText(b, { x: 1.9, y: 2.03 + i*0.83, w: 9.9, h: 0.34, fontFace: FONT, fontSize: SIZE.takeaway, color: C.dark, margin: 0, fit: 'shrink' });
    });
  }
}
function mechanismSlide(pptx, slideData, page) {
  const s = pptx.addSlide(); addBg(s); addHeader(s, slideData.title); addPageNum(s, page);
  const hasImage = !!(slideData.localImagePath && fs.existsSync(slideData.localImagePath) && fs.statSync(slideData.localImagePath).size > 0);
  s.addShape('rect', { x: 0.62, y: 1.16, w: hasImage ? 5.0 : 12.0, h: 5.55, fill: { color: C.white }, shadow: softShadow() });
  addLeftAccent(s, 0.62, 1.16, 5.55, C.teal);
  s.addText('路径主线', { x: 0.95, y: 1.35, w: 1.6, h: 0.25, fontFace: FONT, fontSize: SIZE.mechanismLabel, bold: true, color: C.teal, margin: 0, fit: 'shrink' });
  const bullets = slideData.bullets || [];
  bullets.forEach((b, i) => {
    const y = 1.82 + i * 1.03; const fill = i === 0 ? C.teal : (i === bullets.length -1 ? C.gold : 'EEF5FB'); const txtColor = i === 0 ? C.white : C.dark;
    s.addShape('roundRect', { x: 1.0, y, w: hasImage ? 4.1 : 10.8, h: 0.55, rectRadius: 0.05, fill: { color: fill }, line: { color: fill } });
    s.addText(b, { x: 1.12, y: y+0.08, w: hasImage ? 3.86 : 10.5, h: 0.36, fontFace: FONT, fontSize: hasImage ? SIZE.mechanismNode : 15.5, bold: i===0 || i===bullets.length-1, color: txtColor, align: hasImage ? 'center' : 'left', valign: 'middle', margin: 0, fit: 'shrink' });
    if (i < bullets.length -1) s.addText('↓', { x: hasImage ? 2.85 : 5.9, y: y+0.56, w: 0.4, h: 0.24, fontFace: FONT, fontSize: 18, bold: true, color: 'B7CBDC', align: 'center', margin: 0, fit: 'shrink' });
  });
  if (hasImage) {
    s.addShape('rect', { x: 5.95, y: 1.16, w: 6.6, h: 3.6, fill: { color: 'F4F7FA' }, line: { color: 'C8D5E1', width: 1 } });
    s.addImage({ path: slideData.localImagePath, x: 6.05, y: 1.28, w: 6.4, h: 3.35, sizing: { type: 'contain', w: 6.4, h: 3.35 } });
    s.addShape('rect', { x: 5.95, y: 5.0, w: 6.6, h: 1.7, fill: { color: C.gold_bg }, shadow: softShadow() });
    addLeftAccent(s, 5.95, 5.0, 1.7, C.gold);
    s.addText('机制解读', { x: 6.2, y: 5.22, w: 1.2, h: 0.22, fontFace: FONT, fontSize: 16, bold: true, color: 'A2721D', margin: 0, fit: 'shrink' });
    const exp = slideData.figure_explanations?.[0]?.explanation || '';
    s.addText(exp, { x: 6.2, y: 5.55, w: 5.9, h: 0.85, fontFace: FONT, fontSize: SIZE.mechanismExplain, color: C.dark, margin: 0, valign: 'top', fit: 'shrink' });
  }
}
function closingSlide(pptx, page) {
  const s = pptx.addSlide(); addBg(s, true);
  s.addShape('roundRect', { x: 1.1, y: 1.45, w: 5.5, h: 3.7, rectRadius: 0.08, fill: { color: '1D405D' } });
  s.addText('谢谢！', { x: 1.55, y: 2.1, w: 3.2, h: 0.7, fontFace: FONT_HEAD, fontSize: SIZE.closingTitle, bold: true, color: C.white, margin: 0, fit: 'shrink' });
  s.addText('感谢批评指正！', { x: 1.58, y: 3.0, w: 4.3, h: 0.42, fontFace: FONT, fontSize: SIZE.closingSubtitle, color: 'DDE9F2', margin: 0, fit: 'shrink' });
  s.addText('Questions & Discussion', { x: 1.58, y: 3.72, w: 3.5, h: 0.3, fontFace: FONT, fontSize: SIZE.closingNote, italic: true, color: 'BDD2E3', margin: 0, fit: 'shrink' });
  s.addShape('rect', { x: 9.2, y: 1.75, w: 2.65, h: 2.65, fill: { color: '274967' } });
  s.addShape('line', { x: 9.52, y: 3.08, w: 2.0, h: 0, line: { color: C.gold, width: 2 } });
  s.addShape('line', { x: 10.52, y: 2.08, w: 0, h: 2.0, line: { color: C.gold, width: 2 } });
  s.addText('AD Journal Club', { x: 9.46, y: 4.7, w: 2.6, h: 0.22, fontFace: FONT, fontSize: SIZE.badge, color: 'D0DFEB', margin: 0, fit: 'shrink' });
  addPageNum(s, page);
}
(async function main() {
  const args = parseArgs(process.argv);
  if (!args['slides-json']) { console.error('missing --slides-json'); process.exit(1); }
  const deck = JSON.parse(fs.readFileSync(args['slides-json'], 'utf8'));
  const cacheDir = args['assets-dir'] || path.join(path.dirname(args['slides-json']), 'assets');
  fs.mkdirSync(cacheDir, { recursive: true });
  for (const s of deck.slides) {
    if (s.image_paths_or_urls?.length) s.localImagePath = await ensureAsset(s.image_paths_or_urls[0], cacheDir);
  }
  const pptx = new PptxGenJS();
  pptx.layout = 'LAYOUT_WIDE';
  pptx.author = 'OpenClaw';
  pptx.title = deck.paper_meta.title_en;
  pptx.subject = deck.paper_meta.title_en;
  pptx.lang = 'zh-CN';
  pptx.theme = { headFontFace: FONT_HEAD, bodyFontFace: FONT, lang: 'zh-CN' };
  let page = 1;
  titleSlide(pptx, deck, page++);
  agendaSlide(pptx, page++);
  for (const slideData of deck.slides.slice(1, -1)) {
    if (slideData.slide_type === 'result') resultSlide(pptx, slideData, page++);
    else if (slideData.slide_type === 'mechanism') mechanismSlide(pptx, slideData, page++);
    else genericTextSlide(pptx, slideData, page++);
  }
  closingSlide(pptx, page++);
  const outPath = args['output'] || path.join(process.cwd(), sanitize(deck.paper_meta.title_en) + '.pptx');
  await pptx.writeFile({ fileName: outPath });
  console.log(outPath);
})().catch(err => { console.error(err?.stack || String(err)); process.exit(1); });
