#!/usr/bin/env node
// export-pptx.mjs: PowerPoint file from a sketchy deck, 16:9 (13.333 x 7.5 in).
//   faithful  one full-bleed picture per slide (2x), speaker notes, the visible text as alt text
//   editable  the same picture with its text hidden, plus real text boxes placed over the art
// The writer is pptxgenjs 3.12.0 (MIT), vendored in scripts/vendor/. No network is needed.
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import zlib from 'node:zlib';
import { spawnSync } from 'node:child_process';
import {
  parseArgs, say, die, rel, baseName, fmtBytes, requireHtmlFile, requirePlaywright, launchChromium,
  openPage, watchPage, waitReady, isDeckPage, slideCount, fileUrl, isMain, SCRIPT_DIR,
} from './_lib.mjs';

const VENDOR = path.join(SCRIPT_DIR, 'vendor', 'pptxgenjs-3.12.0', 'pptxgen.bundle.js');
const EMU_W = 12192000, EMU_H = 6858000;   // 13.333 x 7.5 in
const IN_W = EMU_W / 914400, IN_H = EMU_H / 914400;
const PX_PER_IN = 1920 / IN_W;             // 144 stage px per inch
const PT_PER_PX = 72 / PX_PER_IN;          // 0.5 pt per stage px

const spec = {
  name: 'sketchy export-pptx', file: 'export-pptx.mjs', usage: '<deck.html> [-o out.pptx] [--mode faithful|editable]',
  summary: 'PowerPoint file (16:9) from a deck: slide art as a picture, notes, and optionally real text boxes.',
  details: [
    'faithful (default): one full-bleed picture per slide captured at 2x with ?static&clean&slide=N,',
    '  speaker notes from data-notes or .sk-notes-speaker, the slide\'s visible text as alt text.',
    'editable: the same picture with its text hidden, plus a real text box over each text block',
    '  (Calibri for prose, Courier New for figures and mono), sized and colored from the page.',
    '  Text that is rotated more than 3 degrees stays in the picture.',
    'The handwriting font and the boil animation cannot live in a .pptx. After writing, the file is reopened',
    'and checked (parts, slide and notes counts, alt text); with LibreOffice installed it is also converted to PDF.',
  ],
  options: [
    { name: 'out', short: 'o', type: 'string', arg: 'file', help: 'output file (default: out/<name>.pptx next to the input)' },
    { name: 'mode', type: 'string', arg: 'faithful|editable', default: 'faithful', help: 'faithful: picture + notes. editable: picture without text + real text boxes' },
    { name: 'scale', type: 'number', default: 2, help: 'picture scale: 1 gives 1920x1080, 2 gives 3840x2160 (default 2)' },
    { name: 'image', type: 'string', arg: 'jpeg|png', default: 'jpeg', help: 'picture format: jpeg (quality 90, the default, mail-friendly) or png (sharpest, about five times larger)' },
    { name: 'no-fit', type: 'boolean', help: 'editable: keep the page font size in pt even when Calibri runs wider than the handwriting' },
  ],
  positionals: { min: 1, max: 1, name: '<deck.html>' },
  examples: ['node export-pptx.mjs out/deck.html', 'node export-pptx.mjs out/deck.html --mode editable -o deck-editable.pptx', 'node export-pptx.mjs out/deck.html --image png'],
};

/* ---------- the writer (vendored pptxgenjs) ---------- */
function loadPptxGenJS() {
  if (!fs.existsSync(VENDOR)) die('the vendored pptxgenjs is missing', [`expected ${rel(VENDOR)}`, 'restore scripts/vendor/ from the sketchy repository']);
  const src = fs.readFileSync(VENDOR, 'utf8');
  // The browser bundle defines `var PptxGenJS` and expects window.JSZip; give it a private window.
  const win = {}; win.window = win;
  try {
    return new Function('win', `var PptxGenJS; with (win) {\n${src}\n}\nreturn PptxGenJS;`)(win);
  } catch (e) {
    return die(`the vendored pptxgenjs did not load: ${String(e.message).split('\n')[0]}`, 'reinstall the skill (scripts/vendor/ is damaged)');
  }
}

/* ---------- in the page: notes, alt text, text blocks ---------- */
/** Runs inside the deck page. Returns plain data; marks the text it takes over with data-pptx-hide. */
function extractSlide(opts) {
  const slide = document.querySelector('.sk-slide.is-current') || document.querySelector('main.sk-deck .sk-slide');
  const out = { notes: '', title: '', alt: '', blocks: [], kept: 0 };
  if (!slide) return out;
  const stage = slide.closest('.sk-stage') || slide.parentElement;
  const sr = stage.getBoundingClientRect();
  const K = sr.width / 1920 || 1;

  const sp = slide.querySelector('.sk-notes-speaker');
  const rawNotes = slide.getAttribute('data-notes') || (sp ? sp.textContent : '') || '';
  out.notes = rawNotes.split(/\r?\n/).map((l) => l.replace(/[ \t]+/g, ' ').trim()).filter(Boolean).join('\n');
  const titleEl = slide.querySelector('h1, h2, .sk-corner-title, .sk-label-title, blockquote');
  out.title = titleEl ? titleEl.textContent.replace(/\s+/g, ' ').trim().slice(0, 100) : '';
  const lines = String(slide.innerText || '').split(/\n+/).map((s) => s.replace(/\s+/g, ' ').trim()).filter(Boolean);
  out.alt = lines.map((l) => (/[.!?:;\u2026]$/.test(l) ? l : `${l}.`)).join(' ').slice(0, 1500);
  if (!opts.blocks) return out;

  /* ---- helpers ---- */
  const cache = new Map();
  const cs = (el) => { let s = cache.get(el); if (!s) { s = getComputedStyle(el); cache.set(el, s); } return s; };
  const opacityCache = new Map();
  const opacityOf = (el) => {
    if (!el || el === document.documentElement) return 1;
    if (opacityCache.has(el)) return opacityCache.get(el);
    const v = parseFloat(cs(el).opacity);
    const o = (Number.isNaN(v) ? 1 : v) * opacityOf(el.parentElement);
    opacityCache.set(el, o);
    return o;
  };
  const cv = document.createElement('canvas'); cv.width = cv.height = 1;
  const cx = cv.getContext('2d', { willReadFrequently: true });
  const colorCache = new Map();
  const rgba = (css) => {
    if (colorCache.has(css)) return colorCache.get(css);
    let r = null;
    const m = /^rgba?\(\s*([\d.]+)[ ,]+([\d.]+)[ ,]+([\d.]+)(?:\s*[,/]\s*([\d.]+%?))?\s*\)$/.exec(css);
    if (m) r = { r: +m[1], g: +m[2], b: +m[3], a: m[4] === undefined ? 1 : (m[4].endsWith('%') ? parseFloat(m[4]) / 100 : +m[4]) };
    else {
      cx.clearRect(0, 0, 1, 1); cx.fillStyle = '#000'; cx.fillStyle = css; cx.fillRect(0, 0, 1, 1);
      const d = cx.getImageData(0, 0, 1, 1).data; r = { r: d[0], g: d[1], b: d[2], a: d[3] / 255 };
    }
    colorCache.set(css, r);
    return r;
  };
  const hex = (c) => [c.r, c.g, c.b].map((v) => Math.round(v).toString(16).padStart(2, '0')).join('').toUpperCase();
  // Calibri advance widths (em), used only to decide how far to shrink a size when Calibri runs wider than the handwriting
  const CAL = { a: .479, b: .525, c: .423, d: .525, e: .498, f: .305, g: .471, h: .525, i: .229, j: .239, k: .455, l: .229, m: .799, n: .525, o: .527, p: .525, q: .525, r: .349, s: .391, t: .335, u: .525, v: .452, w: .715, x: .433, y: .453, z: .395,
    A: .579, B: .544, C: .533, D: .615, E: .488, F: .459, G: .631, H: .623, I: .252, J: .319, K: .52, L: .42, M: .855, N: .646, O: .662, P: .517, Q: .673, R: .543, S: .459, T: .487, U: .642, V: .567, W: .89, X: .519, Y: .487, Z: .468,
    ' ': .226, '.': .252, ',': .25, ':': .268, ';': .268, '-': .306, '(': .303, ')': .303, '!': .326, '?': .463, '%': .715, '+': .498, '/': .386, '&': .682, '\u00b7': .252, '\u2019': .227, '"': .401 };
  const calWidth = (ch, em, bold) => ((/[0-9\u20ac$]/.test(ch) ? .507 : (CAL[ch] !== undefined ? CAL[ch] : .5)) * em) * (bold ? 1.04 : 1);

  const hiddenBox = (el) => {
    for (let e = el; e && e !== slide.parentElement; e = e.parentElement) {
      const s = cs(e);
      if (s.display === 'none' || s.visibility === 'collapse') return true;
      if (e !== el && s.overflow !== 'visible') { const r = e.getBoundingClientRect(); if (r.width <= 2 || r.height <= 2) return true; }
      if (s.clip && s.clip !== 'auto' && /rect\(\s*0/.test(s.clip)) return true;
      if (s.clipPath && /inset\(\s*(50|100)%/.test(s.clipPath)) return true;
      if (e === slide) break;
    }
    return false;
  };

  /* ---- group the slide's text nodes by block ---- */
  const walker = document.createTreeWalker(slide, NodeFilter.SHOW_TEXT);
  const groups = new Map();
  for (let n = walker.nextNode(); n; n = walker.nextNode()) {
    const p = n.parentElement; // whitespace-only nodes stay: the space between two inline elements is real text
    if (!p || p.closest('script, style, noscript, template, .sk-notes-speaker, [hidden]')) continue;
    let owner = null, svg = false;
    if (p instanceof SVGElement) {
      owner = p.closest('text');
      svg = true;
      if (!owner) continue;
      if (p.closest('textPath')) { out.kept++; continue; }
    } else {
      owner = p;
      while (owner && owner !== slide) { const d = cs(owner).display; if (d !== 'inline' && d !== 'contents') break; owner = owner.parentElement; }
      if (!owner) owner = slide;
    }
    if (!groups.has(owner)) groups.set(owner, { svg, nodes: [] });
    groups.get(owner).nodes.push(n);
  }

  const range = document.createRange();
  const markHide = [];
  for (const [owner, g] of groups) {
    if (!g.nodes.some((n) => /\S/.test(n.nodeValue))) continue;
    if (hiddenBox(owner) || cs(owner).visibility !== 'visible' || opacityOf(owner) < 0.03) continue;

    // geometry and rotation
    let angle = 0, unit = 1;
    if (g.svg) {
      const m = owner.getScreenCTM();
      if (m) { angle = Math.atan2(m.b, m.a) * 180 / Math.PI; unit = Math.hypot(m.a, m.b) / K; }
    } else {
      let m = new DOMMatrix();
      const chain = [];
      for (let e = owner; e && e !== document.documentElement; e = e.parentElement) chain.push(e);
      for (const e of chain.reverse()) { const t = cs(e).transform; if (t && t !== 'none') { try { m = m.multiply(new DOMMatrix(t)); } catch (err) { /* ignore */ } } }
      angle = Math.atan2(m.b, m.a) * 180 / Math.PI;
    }
    if (Math.abs(angle) < 0.25) angle = 0;
    const textParents = [...new Set(g.nodes.map((n) => n.parentElement))];
    if (Math.abs(angle) > 3) { out.kept++; textParents.forEach((el) => markHide.push({ el, keep: true })); continue; }

    // characters with their rectangles, in reading order
    const chars = [];
    for (const n of g.nodes) {
      const s = n.nodeValue, el = n.parentElement;
      for (let i = 0; i < s.length; i++) {
        range.setStart(n, i); range.setEnd(n, i + 1);
        const rects = range.getClientRects();
        if (!rects.length) continue;
        const q = rects[0];
        if (q.width === 0 && /\s/.test(s[i])) continue;
        chars.push({ ch: s[i], l: (q.left - sr.left) / K, t: (q.top - sr.top) / K, r: (q.right - sr.left) / K, b: (q.bottom - sr.top) / K, el });
      }
    }
    if (!chars.length) continue;

    // lines: a new line starts when x steps back or y jumps
    const ls = [[chars[0]]];
    for (let i = 1; i < chars.length; i++) {
      const a = chars[i - 1], c = chars[i];
      const hmin = Math.min(a.b - a.t, c.b - c.t) || 1;
      const newLine = c.l < a.l - 1 || Math.abs((c.t + c.b) / 2 - (a.t + a.b) / 2) > 0.8 * hmin;
      if (newLine) ls.push([c]); else ls[ls.length - 1].push(c);
    }
    for (const L of ls) { while (L.length && /\s/.test(L[0].ch)) L.shift(); while (L.length && /\s/.test(L[L.length - 1].ch)) L.pop(); }
    const lineList = ls.filter((L) => L.length);
    if (!lineList.length) continue;

    // style per element
    const style = (el) => {
      const s = cs(el);
      let size = parseFloat(s.fontSize) || 16;
      let colorCss = g.svg && s.fill && s.fill !== 'none' && !/^url/.test(s.fill) ? s.fill : s.color;
      const c = rgba(colorCss);
      const ls0 = parseFloat(s.letterSpacing);
      if (g.svg) size *= unit;
      return {
        size, color: hex(c), alpha: Math.min(1, c.a * opacityOf(el) * (g.svg ? (parseFloat(s.fillOpacity) || 1) : 1)),
        bold: s.fontWeight === 'bold' || parseInt(s.fontWeight, 10) >= 600, italic: /italic|oblique/.test(s.fontStyle),
        mono: /courier|mono|consolas/i.test(s.fontFamily),
        underline: /underline/.test(s.textDecorationLine || ''), strike: /line-through/.test(s.textDecorationLine || ''),
        spacing: Number.isFinite(ls0) ? ls0 * (g.svg ? unit : 1) : 0, transform: s.textTransform,
      };
    };
    const styles = new Map();
    const styleOf = (el) => { if (!styles.has(el)) styles.set(el, style(el)); return styles.get(el); };
    const transformChar = (ch, st, prev) => {
      if (st.transform === 'uppercase') return ch.toUpperCase();
      if (st.transform === 'lowercase') return ch.toLowerCase();
      if (st.transform === 'capitalize') return !prev || /[\s(\-]/.test(prev) ? ch.toUpperCase() : ch;
      return ch;
    };
    const key = (st) => [st.size.toFixed(1), st.color, st.alpha.toFixed(2), st.bold, st.italic, st.mono, st.underline, st.strike, st.spacing.toFixed(2)].join('|');

    const outLines = [];
    let fit = 1;
    for (const L of lineList) {
      const runs = [];
      let est = 0, prev = '';
      for (const c of L) {
        const st = styleOf(c.el);
        const ch = transformChar(c.ch, st, prev);
        prev = c.ch;
        est += st.mono ? 0.6 * st.size : calWidth(ch, st.size, st.bold);
        const k = key(st);
        const last = runs[runs.length - 1];
        if (last && last.k === k) last.text += ch;
        else runs.push({ k, text: ch, size: st.size, color: st.color, alpha: st.alpha, bold: st.bold, italic: st.italic, mono: st.mono, underline: st.underline, strike: st.strike, spacing: st.spacing });
      }
      const width = Math.max(...L.map((c) => c.r)) - Math.min(...L.map((c) => c.l));
      if (opts.fit && est > 0 && width > 0) fit = Math.min(fit, width / est);
      outLines.push({ runs, l: Math.min(...L.map((c) => c.l)), r: Math.max(...L.map((c) => c.r)), t: Math.min(...L.map((c) => c.t)), b: Math.max(...L.map((c) => c.b)) });
    }
    fit = Math.max(0.62, Math.min(1, fit));

    // box, alignment, line pitch
    const x0 = Math.min(...outLines.map((l) => l.l)), x1 = Math.max(...outLines.map((l) => l.r));
    const centers = outLines.map((l) => (l.t + l.b) / 2);
    let pitch;
    if (centers.length > 1) { const d = centers.slice(1).map((c, i) => c - centers[i]).sort((a, b) => a - b); pitch = d[Math.floor(d.length / 2)]; }
    else pitch = Math.max(...outLines.map((l) => l.b - l.t));
    const s0 = cs(owner);
    let align = 'left';
    if (g.svg) align = s0.textAnchor === 'middle' ? 'center' : s0.textAnchor === 'end' ? 'right' : 'left';
    else { const ta = s0.textAlign; align = ta === 'center' ? 'center' : (ta === 'right' || ta === 'end') ? 'right' : 'left'; }
    const top = centers[0] - pitch / 2;
    out.blocks.push({
      x: x0, y: top, w: x1 - x0, h: pitch * outLines.length, pitch, align, rotate: Math.round(angle * 100) / 100, fit,
      lines: outLines.map((l) => l.runs.map((r) => ({ text: r.text, size: r.size * fit, color: r.color, alpha: r.alpha, bold: r.bold, italic: r.italic, mono: r.mono, underline: r.underline, strike: r.strike, spacing: r.spacing }))),
    });
    textParents.forEach((el) => markHide.push({ el, keep: false }));
  }

  /* ---- hide what became real text; keep what stays in the art ---- */
  const kept = new Set(markHide.filter((m) => m.keep).map((m) => m.el));
  for (const { el, keep } of markHide) {
    if (keep) continue;
    el.setAttribute('data-pptx-hide', '');
    for (const pseudo of ['::before', '::after']) {
      const c = getComputedStyle(el, pseudo).content;
      if (c && c !== 'none' && c !== 'normal') el.style.setProperty('--pptx-pc', getComputedStyle(el).color);
    }
  }
  for (const el of kept) {
    if (el.hasAttribute('data-pptx-hide')) continue;
    const col = getComputedStyle(el).color;
    el.style.setProperty('color', col, 'important');
    el.style.setProperty('-webkit-text-fill-color', col, 'important');
  }
  return out;
}

const HIDE_CSS = [
  '.sk-notes-speaker { display: none !important; }',
  '[data-pptx-hide] { color: transparent !important; -webkit-text-fill-color: transparent !important; text-shadow: none !important; fill: transparent !important; stroke: transparent !important; }',
  '[data-pptx-hide]::before, [data-pptx-hide]::after { color: var(--pptx-pc, currentColor) !important; -webkit-text-fill-color: var(--pptx-pc, currentColor) !important; }',
].join('\n');

/* ---------- zip reader and writer (to check and tidy what pptxgenjs wrote) ---------- */
export function readZip(buf) {
  let i = buf.length - 22;
  while (i >= 0 && buf.readUInt32LE(i) !== 0x06054b50) i--;
  if (i < 0) throw new Error('not a zip file (no end record)');
  const count = buf.readUInt16LE(i + 10);
  let p = buf.readUInt32LE(i + 16);
  const entries = new Map();
  for (let n = 0; n < count; n++) {
    if (buf.readUInt32LE(p) !== 0x02014b50) throw new Error('damaged zip directory');
    const nlen = buf.readUInt16LE(p + 28), elen = buf.readUInt16LE(p + 30), clen = buf.readUInt16LE(p + 32);
    entries.set(buf.toString('utf8', p + 46, p + 46 + nlen), {
      method: buf.readUInt16LE(p + 10), crc: buf.readUInt32LE(p + 16), csize: buf.readUInt32LE(p + 20), usize: buf.readUInt32LE(p + 24), lho: buf.readUInt32LE(p + 42),
    });
    p += 46 + nlen + elen + clen;
  }
  const raw = (name) => {
    const e = entries.get(name);
    if (!e) throw new Error(`missing part ${name}`);
    const nl = buf.readUInt16LE(e.lho + 26), el = buf.readUInt16LE(e.lho + 28);
    return buf.subarray(e.lho + 30 + nl + el, e.lho + 30 + nl + el + e.csize);
  };
  const read = (name) => { const e = entries.get(name); const data = raw(name); return e.method === 0 ? data : zlib.inflateRawSync(data); };
  return { names: [...entries.keys()], read, raw, entry: (name) => entries.get(name) };
}

const CRC_TABLE = (() => { const t = new Uint32Array(256); for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; } return t; })();
export function crc32(data) { let c = 0xffffffff; for (let i = 0; i < data.length; i++) c = CRC_TABLE[(c ^ data[i]) & 0xff] ^ (c >>> 8); return (c ^ 0xffffffff) >>> 0; }

/** parts: [{ name, method (0 or 8), crc, usize, data (the bytes as stored) }] in the order they should appear. */
export function writeZip(parts) {
  const chunks = [], central = [];
  let offset = 0;
  for (const p of parts) {
    const name = Buffer.from(p.name, 'utf8');
    const local = Buffer.alloc(30);
    local.writeUInt32LE(0x04034b50, 0); local.writeUInt16LE(20, 4); local.writeUInt16LE(0x0800, 6); local.writeUInt16LE(p.method, 8);
    local.writeUInt16LE(0, 10); local.writeUInt16LE(0x0021, 12); // 1980-01-01, so the same input gives the same file
    local.writeUInt32LE(p.crc, 14); local.writeUInt32LE(p.data.length, 18); local.writeUInt32LE(p.usize, 22); local.writeUInt16LE(name.length, 26); local.writeUInt16LE(0, 28);
    const cd = Buffer.alloc(46);
    cd.writeUInt32LE(0x02014b50, 0); cd.writeUInt16LE(20, 4); cd.writeUInt16LE(20, 6); cd.writeUInt16LE(0x0800, 8); cd.writeUInt16LE(p.method, 10);
    cd.writeUInt16LE(0, 12); cd.writeUInt16LE(0x0021, 14); cd.writeUInt32LE(p.crc, 16); cd.writeUInt32LE(p.data.length, 20); cd.writeUInt32LE(p.usize, 24);
    cd.writeUInt16LE(name.length, 28); cd.writeUInt32LE(offset, 42);
    central.push(cd, name);
    chunks.push(local, name, p.data);
    offset += 30 + name.length + p.data.length;
  }
  const cdBuf = Buffer.concat(central);
  const end = Buffer.alloc(22);
  end.writeUInt32LE(0x06054b50, 0); end.writeUInt16LE(parts.length, 8); end.writeUInt16LE(parts.length, 10); end.writeUInt32LE(cdBuf.length, 12); end.writeUInt32LE(offset, 16);
  return Buffer.concat([...chunks, cdBuf, end]);
}

/**
 * pptxgenjs writes a paragraph-properties element before every text run, so a paragraph with two styles has
 * two of them; the schema allows one, at the start. Keep the first, drop the rest, and leave every other part as stored.
 */
export function tidyParagraphs(buf) {
  const zip = readZip(buf);
  let changed = 0;
  const parts = zip.names.map((name) => {
    const e = zip.entry(name);
    if (/^ppt\/slides\/slide\d+\.xml$/.test(name)) {
      const xml = zip.read(name).toString('utf8');
      const out = xml.replace(/<a:p>([\s\S]*?)<\/a:p>/g, (m, inner) => {
        let seen = false;
        return `<a:p>${inner.replace(/<a:pPr\b[^>]*?(?:\/>|>[\s\S]*?<\/a:pPr>)/g, (pp) => { if (!seen) { seen = true; return pp; } changed++; return ''; })}</a:p>`;
      });
      if (out !== xml) { const data = Buffer.from(out, 'utf8'); return { name, method: 8, crc: crc32(data), usize: data.length, data: zlib.deflateRawSync(data) }; }
    }
    return { name, method: e.method, crc: e.crc, usize: e.usize, data: zip.raw(name) };
  });
  return { buf: changed ? writeZip(parts) : buf, changed };
}

const unescapeXml = (s) => s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&apos;/g, "'").replace(/&amp;/g, '&');
const textsOf = (xml) => [...xml.matchAll(/<a:t>([\s\S]*?)<\/a:t>/g)].map((m) => unescapeXml(m[1]));

/** Reopen the file and compare it with what was meant to go in. Returns { facts, problems }. */
export function validatePptx(file, expected) {
  const problems = [];
  const facts = {};
  let zip;
  try { zip = readZip(fs.readFileSync(file)); } catch (e) { return { facts, problems: [`cannot reopen the file: ${e.message}`] }; }
  const names = new Set(zip.names);
  const need = (n) => { if (!names.has(n)) problems.push(`missing part ${n}`); return names.has(n); };
  if (need('[Content_Types].xml')) {
    const ct = zip.read('[Content_Types].xml').toString('utf8');
    facts.contentTypes = (ct.match(/<(Default|Override)\b/g) || []).length;
    for (const n of zip.names.filter((x) => /^ppt\/slides\/slide\d+\.xml$/.test(x))) if (!ct.includes(`/${n}`)) problems.push(`[Content_Types].xml does not list /${n}`);
    if (!/Extension="(png|jpe?g)"/i.test(ct)) problems.push('[Content_Types].xml has no picture type');
  }
  const slides = zip.names.filter((x) => /^ppt\/slides\/slide\d+\.xml$/.test(x)).sort((a, b) => parseInt(a.replace(/\D/g, ''), 10) - parseInt(b.replace(/\D/g, ''), 10));
  const notes = zip.names.filter((x) => /^ppt\/notesSlides\/notesSlide\d+\.xml$/.test(x));
  facts.slides = slides.length; facts.notesParts = notes.length;
  facts.media = zip.names.filter((x) => /^ppt\/media\/[^/]+$/.test(x)).length;
  if (slides.length !== expected.slides.length) problems.push(`${slides.length} slides in the file, ${expected.slides.length} in the deck`);
  if (need('ppt/presentation.xml')) {
    const pres = zip.read('ppt/presentation.xml').toString('utf8');
    const sz = /<p:sldSz cx="(\d+)" cy="(\d+)"/.exec(pres);
    facts.size = sz ? `${sz[1]}x${sz[2]}` : '?';
    if (!sz || +sz[1] !== EMU_W || +sz[2] !== EMU_H) problems.push(`slide size is ${facts.size}, expected ${EMU_W}x${EMU_H} (16:9)`);
    if ((pres.match(/<p:sldId\b/g) || []).length !== slides.length) problems.push('presentation.xml lists a different number of slides');
  }
  let withNotes = 0, boxes = 0, alts = 0;
  slides.forEach((name, i) => {
    const xml = zip.read(name).toString('utf8');
    const exp = expected.slides[i] || {};
    const relsName = name.replace('slides/', 'slides/_rels/') + '.rels';
    if (names.has(relsName)) {
      for (const m of zip.read(relsName).toString('utf8').matchAll(/Target="([^"]+)"/g)) {
        if (/^https?:/i.test(m[1])) continue;
        const target = path.posix.normalize(path.posix.join('ppt/slides', m[1])).replace(/^\//, '');
        if (!names.has(target) && !names.has(m[1].replace(/^\//, ''))) problems.push(`slide ${i + 1} points at ${m[1]}, which is not in the file`);
      }
    } else problems.push(`slide ${i + 1} has no relationships part`);
    const pic = /<p:pic>[\s\S]*?<\/p:pic>/.exec(xml);
    if (!pic) problems.push(`slide ${i + 1} has no picture`);
    else if (/descr="[^"]+"/.test(pic[0])) alts++;
    else problems.push(`slide ${i + 1}: the picture has no alt text`);
    const sps = (xml.match(/<p:sp>[\s\S]*?<\/p:sp>/g) || []).filter((s) => /<a:t>/.test(s));
    boxes += sps.length;
    if (exp.boxes !== undefined && sps.length !== exp.boxes) problems.push(`slide ${i + 1} has ${sps.length} text boxes, expected ${exp.boxes}`);
    const nName = `ppt/notesSlides/notesSlide${parseInt(name.replace(/\D/g, ''), 10)}.xml`;
    if (exp.notes) {
      if (!names.has(nName)) problems.push(`slide ${i + 1} should have notes but ${nName} is missing`);
      else {
        const joined = textsOf(zip.read(nName).toString('utf8')).join('\n').replace(/\s+/g, ' ');
        const want = exp.notes.replace(/\s+/g, ' ').trim();
        if (!joined.includes(want)) problems.push(`slide ${i + 1}: the notes in the file differ from the deck`);
        else withNotes++;
      }
    }
  });
  facts.notesWithText = withNotes; facts.textBoxes = boxes; facts.altText = alts;
  const wantNotes = expected.slides.filter((s) => s.notes).length;
  if (withNotes !== wantNotes) problems.push(`${withNotes} slides carry notes, the deck has ${wantNotes}`);
  return { facts, problems };
}

/* ---------- LibreOffice (optional second check) ---------- */
function findSoffice() {
  const cands = ['soffice', 'libreoffice'];
  if (process.platform === 'win32') cands.push('C:\\Program Files\\LibreOffice\\program\\soffice.exe', 'C:\\Program Files (x86)\\LibreOffice\\program\\soffice.exe');
  if (process.platform === 'darwin') cands.push('/Applications/LibreOffice.app/Contents/MacOS/soffice');
  for (const c of cands) {
    const r = spawnSync(c, ['--version'], { encoding: 'utf8', windowsHide: true, timeout: 30000 });
    if (!r.error && r.status === 0) return c;
  }
  return null;
}

function pdfPages(file) {
  const text = fs.readFileSync(file).toString('latin1');
  return (text.match(/\/Type\s*\/Page(?![s\w])/g) || []).length;
}

function checkWithSoffice(soffice, pptx) {
  const work = fs.mkdtempSync(path.join(os.tmpdir(), 'sketchy-soffice-'));
  try {
    const r = spawnSync(soffice, ['--headless', `-env:UserInstallation=file:///${path.join(work, 'profile').replace(/\\/g, '/')}`, '--convert-to', 'pdf', '--outdir', work, pptx], { encoding: 'utf8', windowsHide: true, timeout: 180000 });
    const pdf = path.join(work, `${baseName(pptx)}.pdf`);
    if (r.error || !fs.existsSync(pdf)) return { error: r.error ? String(r.error.message) : `no PDF written${r.stderr ? `: ${r.stderr.trim().split('\n')[0]}` : ''}` };
    return { pages: pdfPages(pdf) };
  } finally { fs.rmSync(work, { recursive: true, force: true }); }
}

/* ---------- build ---------- */
const round = (n, d = 1) => Math.round(n * 10 ** d) / 10 ** d;

function addBlocks(slide, blocks) {
  blocks.forEach((b, i) => {
    const runs = [];
    b.lines.forEach((line, li) => line.forEach((r, ri) => {
      const o = {
        fontFace: r.mono ? 'Courier New' : 'Calibri', fontSize: Math.max(1, round(r.size * PT_PER_PX)), color: r.color,
      };
      if (r.bold) o.bold = true;
      if (r.italic) o.italic = true;
      if (r.underline) o.underline = { style: 'sng' };
      if (r.strike) o.strike = 'sngStrike';
      if (r.spacing) o.charSpacing = round(r.spacing * PT_PER_PX, 2);
      if (r.alpha < 0.99) o.transparency = Math.min(100, Math.max(0, Math.round((1 - r.alpha) * 100)));
      if (li > 0 && ri === 0) o.softBreakBefore = true;
      runs.push({ text: r.text, options: o });
    }));
    const box = {
      x: round(b.x / PX_PER_IN, 4), y: round(b.y / PX_PER_IN, 4), w: Math.max(0.05, round(b.w / PX_PER_IN, 4)), h: Math.max(0.05, round(b.h / PX_PER_IN, 4)),
      margin: 0, valign: 'top', wrap: false, fit: 'none', align: b.align, lineSpacing: Math.max(1, round(b.pitch * PT_PER_PX)),
      objectName: `Text ${i + 1}`,
    };
    if (b.rotate) box.rotate = b.rotate;
    slide.addText(runs, box);
  });
}

async function main() {
  const { values, positionals } = parseArgs(process.argv.slice(2), spec);
  const file = requireHtmlFile(positionals[0], 'deck html file');
  if (!/^(faithful|editable)$/.test(values.mode)) die(`--mode must be faithful or editable, got "${values.mode}"`, 'for example --mode editable');
  if (!/^(png|jpeg)$/.test(values.image)) die(`--image must be png or jpeg, got "${values.image}"`, 'for example --image jpeg');
  if (!(values.scale >= 1 && values.scale <= 3)) die(`--scale must be from 1 to 3, got ${values.scale}`, 'for example --scale 2');
  const editable = values.mode === 'editable';
  let out;
  if (values.out) out = path.resolve(values.out);
  else if (path.basename(path.dirname(file)) === 'out') out = path.join(path.dirname(file), `${baseName(file)}.pptx`);
  else out = path.join(path.dirname(file), 'out', `${baseName(file)}.pptx`);
  fs.mkdirSync(path.dirname(out), { recursive: true });

  const PptxGenJS = loadPptxGenJS();
  const pw = requirePlaywright();
  const browser = await launchChromium(pw);
  const state = { errors: new Map(), failed: new Map(), external: new Map() };
  const shots = [];
  let docTitle = '';
  const started = Date.now();
  try {
    const { context, page } = await openPage(browser, { width: 1920, height: 1080, scale: values.scale });
    watchPage(page, state);
    await page.goto(fileUrl(file, 'static&clean&slide=1'), { waitUntil: 'load' });
    if (!(await waitReady(page))) say.warn('page was not ready after 15 s; exporting anyway');
    if (!(await isDeckPage(page))) die('this file is not a sketchy deck', ['PPTX export needs <main class="sk-deck"> with <section class="sk-slide"> pages', 'make one with: node new.mjs deck <folder>']);
    const count = await slideCount(page);
    if (!count) die('the deck has no slides', 'add <section class="sk-slide"> elements inside main.sk-deck', 1);
    docTitle = await page.title();
    for (let n = 1; n <= count; n++) {
      if (n > 1) {
        await page.goto(fileUrl(file, `static&clean&slide=${n}`), { waitUntil: 'load' });
        if (!(await waitReady(page))) say.warn(`slide ${n} was not ready after 15 s`);
      }
      await page.addStyleTag({ content: HIDE_CSS });
      const info = await page.evaluate(extractSlide, { blocks: editable, fit: !values.noFit });
      if (editable) await page.evaluate(() => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r))));
      const png = await page.screenshot(values.image === 'png' ? { type: 'png' } : { type: 'jpeg', quality: 90 });
      shots.push({ n, ...info, image: png });
    }
    await context.close();
  } finally {
    await browser.close();
  }

  const pptx = new PptxGenJS();
  pptx.layout = 'LAYOUT_WIDE';
  pptx.title = docTitle || baseName(file);
  pptx.subject = 'Made with sketchy';
  pptx.author = 'sketchy';
  pptx.company = '';
  const mime = values.image === 'png' ? 'image/png' : 'image/jpeg';
  for (const s of shots) {
    const slide = pptx.addSlide();
    const alt = editable
      ? `Slide ${s.n}${s.title ? `: ${s.title}` : ''}. Hand-drawn art; the text is in separate text boxes.${s.kept ? ' Some rotated text is part of the picture: ' + s.alt : ''}`
      : (s.alt || `Slide ${s.n}${s.title ? `: ${s.title}` : ''}`);
    slide.addImage({ data: `${mime};base64,${s.image.toString('base64')}`, x: 0, y: 0, w: IN_W, h: IN_H, altText: alt, objectName: `Slide ${s.n} art` });
    if (editable) addBlocks(slide, s.blocks);
    if (s.notes) slide.addNotes(s.notes);
  }
  const buf = tidyParagraphs(await pptx.write({ outputType: 'nodebuffer' })).buf;
  const tmp = `${out}.partial`;
  fs.writeFileSync(tmp, buf);
  fs.rmSync(out, { force: true });
  fs.renameSync(tmp, out);

  const { facts, problems } = validatePptx(out, { slides: shots.map((s) => ({ notes: s.notes, boxes: editable ? s.blocks.length : undefined })) });
  const size = fs.statSync(out).size;
  say.ok(`pptx  ${rel(out)}  ${values.mode}, ${facts.slides} slides at 13.333 x 7.5 in, ${fmtBytes(size)}, ${((Date.now() - started) / 1000).toFixed(0)} s`);
  say.ok(`check  [Content_Types].xml ${facts.contentTypes || '?'} entries, ${facts.slides} slides, ${facts.notesWithText} with notes (${facts.notesParts} notes parts), ${facts.media} pictures, ${facts.altText} with alt text${editable ? `, ${facts.textBoxes} text boxes` : ''}`);
  if (editable) {
    const kept = shots.reduce((a, s) => a + s.kept, 0);
    if (kept) say.info(`${kept} rotated or curved text block${kept === 1 ? '' : 's'} stay in the picture`);
  }
  if (size > 40 * 1024 * 1024 && values.image === 'png') say.warn(`${fmtBytes(size)} is large for mail`), say.fix('add --image jpeg (about a fifth of the size) or --scale 1');
  let bad = 0;
  for (const p of problems) { say.error(p); bad++; }

  const soffice = findSoffice();
  if (!soffice) say.info('LibreOffice check skipped (soffice not found); open the file in PowerPoint or Keynote to be sure');
  else {
    const r = checkWithSoffice(soffice, out);
    if (r.error) say.warn(`LibreOffice could not convert the file: ${r.error}`);
    else if (r.pages !== facts.slides) { say.error(`LibreOffice made a PDF of ${r.pages} pages from ${facts.slides} slides`); bad++; }
    else say.ok(`LibreOffice opened it: PDF of ${r.pages} pages`);
  }
  for (const [msg] of state.errors) say.warn(`console: ${msg}`);
  for (const [msg] of state.failed) say.warn(`request failed: ${msg}`);
  for (const [url] of state.external) say.warn(`external request: ${url}`);
  if (state.errors.size || state.failed.size || state.external.size) say.fix('run lint.mjs and shoot.mjs, fix the deck, export again');
  if (bad) process.exit(1);
}

if (isMain(import.meta.url)) main().catch((e) => die(`export failed: ${String(e && e.message ? e.message : e).split('\n')[0]}`, 'node doctor.mjs', 1));
