#!/usr/bin/env node
// lint.mjs: sketch-lint. Deterministic checks of a rendered deck or page, no AI.
import {
  parseArgs, say, die, rel, requireHtmlFile, requirePlaywright, launchChromium, openPage,
  watchPage, waitReady, isDeckPage, slideCount, fileUrl, isMain, c,
} from './_lib.mjs';

const spec = {
  name: 'sketchy lint', file: 'lint.mjs', usage: '<file.html> [--json] [--strict]',
  summary: 'sketch-lint: overflow, overlap, strokes through text, type size, contrast, words, fonts, seed, placeholders, network, a11y.',
  details: [
    'Opens the file in headless Chromium in static mode (?slide=N&static for decks) and prints one line per issue:',
    '  severity  where  problem  fix: what to do',
    'Checks: text overflowing its box or the 1920x1080 slide, overlapping text, pencil strokes through text,',
    'body text under 20 px (slides) or 16 px (pages), contrast under 4.5:1 (3:1 from 28 px), more than 40 words',
    'or 6 bullets on a slide, missing data-seed, Caveat and Courier Prime not loaded, placeholder text, external',
    'or failed requests, missing <title> or lang, images without alt, charts without their hidden data table.',
    'Pages are also checked at 390 px wide for overflow and sideways scrolling.',
    'Add data-lint-ignore to an element when an overlap or crossing is intended.',
    'Severity: errors break the file, warnings are advice (words, bullets, small type, contrast between 3:1 and 4.5:1).',
    'Last line: "N errors, M warnings". Exit 1 when there are errors (or any issue with --strict).',
  ],
  options: [
    { name: 'json', type: 'boolean', help: 'print the result as JSON (stdout only carries the JSON)' },
    { name: 'strict', type: 'boolean', help: 'treat warnings as errors for the exit code' },
    { name: 'no-mobile', type: 'boolean', help: 'pages: skip the 390 px pass' },
  ],
  positionals: { min: 1, max: 1, name: '<file.html>' },
  examples: ['node lint.mjs out/deck.html', 'node lint.mjs page.html --json'],
};

/* ------------------------------------------------------------------ *
 * Runs inside the page. Must stay self-contained (it is serialized).
 * ------------------------------------------------------------------ */
async function analyzePage(opts) {
  const issues = [];
  const only = opts.only ? new Set(opts.only) : null;
  const want = (k) => !only || only.has(k);
  const IGNORE = '[data-lint-ignore]';
  const SKIP_TAGS = new Set(['SCRIPT', 'STYLE', 'NOSCRIPT', 'TEMPLATE', 'TITLE', 'OPTION', 'TEXTAREA', 'HEAD']);
  const slideMode = opts.mode === 'slide';
  const root = slideMode ? document.querySelectorAll('main.sk-deck .sk-slide')[opts.slideIndex] : document.body;
  const prefix = slideMode ? `slide ${opts.slideIndex + 1}` : 'page';
  if (!root) return { issues, error: 'no root' };
  const S = slideMode ? root.getBoundingClientRect() : null;
  const sc = slideMode ? (S.width / (root.offsetWidth || 1920)) || 1 : 1;
  const r1 = (n) => Math.round(n * 10) / 10;

  /* ----- helpers ----- */
  function describe(el) {
    if (!el || el.nodeType !== 1) return '';
    let s = el.localName;
    if (el.id) s += '#' + el.id;
    else {
      const cl = Array.from(el.classList).filter((x) => !/^is-/.test(x)).slice(0, 2);
      if (cl.length) s += '.' + cl.join('.');
    }
    const own = Array.from(el.childNodes).some((n) => n.nodeType === 3 && /\S/.test(n.nodeValue));
    const t = (el.textContent || '').replace(/\s+/g, ' ').trim().replace(/"/g, "'");
    if (t && (own || el.children.length === 0)) s += ` "${t.length > 30 ? t.slice(0, 29) + '...' : t}"`;
    return s;
  }
  const docLabel = slideMode ? 'deck' : 'page';
  const where = (el) => {
    if (!el || el === root || el === document.body) return el === root ? prefix : docLabel;
    return root.contains(el) ? `${prefix} ${describe(el)}` : `${docLabel} ${describe(el)}`;
  };
  function add(severity, el, problem, fix, check) {
    issues.push({ severity, where: where(el), problem, fix, check, slide: slideMode && (!el || root.contains(el)) ? opts.slideIndex + 1 : null });
  }
  const snippet = (el) => {
    const t = (el.textContent || '').replace(/\s+/g, ' ').trim();
    return t.length > 24 ? t.slice(0, 23) + '...' : t;
  };

  function visuallyHidden(el) {
    for (let a = el; a && a !== document.documentElement; a = a.parentElement) {
      const cs = getComputedStyle(a);
      if (cs.clip && cs.clip !== 'auto' && /rect\(\s*0(px)?[,\s]+0(px)?[,\s]+0(px)?[,\s]+0(px)?\s*\)/.test(cs.clip)) return true;
      if (cs.clipPath && /inset\(\s*(50|100)%/.test(cs.clipPath)) return true;
      if (a !== document.body) {
        const r = a.getBoundingClientRect();
        if ((r.width <= 2 || r.height <= 2) && cs.overflow !== 'visible' && cs.display !== 'inline') return true;
      }
    }
    return false;
  }
  const hiddenCache = new Map();
  function hidden(el) {
    if (hiddenCache.has(el)) return hiddenCache.get(el);
    let h = false;
    if (el.closest(IGNORE) || el.closest('.sk-notes-speaker')) h = true;
    else if (typeof el.checkVisibility === 'function' && !el.checkVisibility({ checkOpacity: true, checkVisibilityCSS: true })) h = true;
    else h = visuallyHidden(el);
    hiddenCache.set(el, h);
    return h;
  }

  /* ----- colors ----- */
  const cvs = document.createElement('canvas');
  cvs.width = cvs.height = 1;
  const cctx = cvs.getContext('2d', { willReadFrequently: true });
  function parseColor(str) {
    if (!str) return null;
    str = str.trim();
    if (str === 'transparent') return [0, 0, 0, 0];
    let m = /^rgba?\(([^)]+)\)$/.exec(str);
    if (m) {
      const p = m[1].split(/[\s,\/]+/).filter(Boolean);
      const a = p[3] !== undefined ? (p[3].endsWith('%') ? parseFloat(p[3]) / 100 : parseFloat(p[3])) : 1;
      return [parseFloat(p[0]), parseFloat(p[1]), parseFloat(p[2]), a];
    }
    m = /^color\(srgb\s+([^)]+)\)$/.exec(str);
    if (m) {
      const parts = m[1].split('/');
      const v = parts[0].trim().split(/\s+/).map(parseFloat);
      const a = parts[1] ? (parts[1].trim().endsWith('%') ? parseFloat(parts[1]) / 100 : parseFloat(parts[1])) : 1;
      return [v[0] * 255, v[1] * 255, v[2] * 255, a];
    }
    cctx.clearRect(0, 0, 1, 1);
    cctx.fillStyle = '#000';
    cctx.fillStyle = str;
    cctx.fillRect(0, 0, 1, 1);
    const d = cctx.getImageData(0, 0, 1, 1).data;
    return [d[0], d[1], d[2], d[3] / 255];
  }
  const over = (top, bottom) => {
    const a = top[3] + bottom[3] * (1 - top[3]);
    if (a <= 0) return [0, 0, 0, 0];
    return [0, 1, 2].map((i) => (top[i] * top[3] + bottom[i] * bottom[3] * (1 - top[3])) / a).concat(a);
  };
  const lin = (v) => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
  const lum = (c) => 0.2126 * lin(c[0]) + 0.7152 * lin(c[1]) + 0.0722 * lin(c[2]);
  const ratio = (a, b) => { const la = lum(a), lb = lum(b); return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05); };
  function paperBehind(el) {
    const layers = [];
    let unknown = false;
    for (let a = el; a; a = a.parentElement) {
      const cs = getComputedStyle(a);
      const bg = parseColor(cs.backgroundColor);
      const hasImg = cs.backgroundImage && cs.backgroundImage !== 'none' && /url\(/.test(cs.backgroundImage);
      if (bg && bg[3] > 0) layers.push(bg);
      if (hasImg && !(bg && bg[3] >= 0.99)) unknown = true;
      if (bg && bg[3] >= 0.99) break;
    }
    if (unknown) return null;
    let col = [255, 255, 255, 1];
    for (let i = layers.length - 1; i >= 0; i--) col = over(layers[i], col);
    return col;
  }
  function opacityChain(el) {
    let o = 1;
    for (let a = el; a && a !== document.documentElement; a = a.parentElement) o *= parseFloat(getComputedStyle(a).opacity || '1');
    return o;
  }

  /* ----- text records ----- */
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT, {
    acceptNode(n) {
      if (n.nodeType === 1) return SKIP_TAGS.has(n.tagName.toUpperCase()) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_SKIP;
      return /\S/.test(n.nodeValue) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
    },
  });
  const range = document.createRange();
  const recs = new Map();
  const allTextNodes = [];
  for (let n = walker.nextNode(); n; n = walker.nextNode()) {
    allTextNodes.push(n);
    const el = n.parentElement;
    if (!el || hidden(el)) continue;
    range.selectNodeContents(n);
    const rects = Array.from(range.getClientRects()).filter((r) => r.width > 0.5 && r.height > 0.5);
    if (!rects.length) continue;
    const cs = getComputedStyle(el);
    const svg = el instanceof SVGElement;
    let fsClient = parseFloat(cs.fontSize) * sc;
    if (svg && el.getScreenCTM) { const m = el.getScreenCTM(); if (m) fsClient = parseFloat(cs.fontSize) * Math.hypot(m.a, m.b); }
    let rec = recs.get(el);
    if (!rec) { rec = { el, svg, fsClient, fs: fsClient / sc, rects: [], band: [], cs, curved: el.localName === 'textPath' || Boolean(el.closest('textPath')) }; recs.set(el, rec); }
    const k = 0.18 * fsClient;
    for (const r of rects) {
      const box = { l: r.left, t: r.top, r: r.right, b: r.bottom };
      rec.rects.push(box);
      let bt = box.t + k, bb = box.b - k;
      if (bt >= bb) { const mid = (box.t + box.b) / 2; bt = mid - 1; bb = mid + 1; }
      rec.band.push({ l: box.l + 1, r: box.r - 1, t: bt, b: bb });
    }
  }
  const recList = Array.from(recs.values());

  /* ----- overflow: box, slide, viewport ----- */
  const flaggedOverflow = new Set();
  if (want('overflow')) {
    const seen = new Set();
    for (const rec of recList) {
      if (rec.svg || rec.curved) continue;
      const ext = {
        l: Math.min(...rec.rects.map((r) => r.l)), r: Math.max(...rec.rects.map((r) => r.r)),
        t: Math.min(...rec.band.map((r) => r.t)), b: Math.max(...rec.band.map((r) => r.b)),
      };
      let flagged = false;
      for (let a = rec.el; a && a !== root && a !== document.body; a = a.parentElement) {
        const cs = a === rec.el ? rec.cs : getComputedStyle(a);
        if (cs.display === 'inline' || cs.display === 'contents' || cs.display === 'none') continue;
        if (/auto|scroll/.test(cs.overflowX + cs.overflowY)) break;
        const A = a.getBoundingClientRect();
        if (A.width < 1 || A.height < 1) continue;
        const ex = { right: ext.r - A.right, bottom: ext.b - A.bottom, left: A.left - ext.l, top: A.top - ext.t };
        const dir = Object.keys(ex).sort((x, y) => ex[y] - ex[x])[0];
        // hanging punctuation (negative margin or indent on the start edge) may overhang by up to half an em
        const startDir = cs.direction === 'rtl' ? 'right' : 'left';
        if (ex[dir] > (dir === startDir ? Math.max(3 * sc, 0.5 * rec.fsClient) : 3 * sc)) {
          if (!seen.has(a)) {
            seen.add(a);
            add('error', a, `text overflows its box by ${r1(ex[dir] / sc)}px (${dir})`, 'shorten the text, enlarge the box, or lower the font size', 'overflow');
          }
          flagged = true;
          break;
        }
      }
      if (flagged) { flaggedOverflow.add(rec.el); continue; }
      if (slideMode) {
        const ex = { right: ext.r - S.right, bottom: ext.b - S.bottom, left: S.left - ext.l, top: S.top - ext.t };
        const dir = Object.keys(ex).sort((x, y) => ex[y] - ex[x])[0];
        if (ex[dir] > 2 * sc) {
          add('error', rec.el, `text leaves the 1920x1080 slide by ${r1(ex[dir] / sc)}px (${dir})`, 'move it inside the slide or shorten it', 'overflow');
          flaggedOverflow.add(rec.el);
        }
      } else {
        const vw = document.documentElement.clientWidth;
        if (ext.r > vw + 2) { add('error', rec.el, `text runs ${r1(ext.r - vw)}px past the right edge of the ${vw}px viewport`, 'let it wrap: remove fixed widths or white-space: nowrap', 'overflow'); flaggedOverflow.add(rec.el); }
        else if (ext.l < -2) { add('error', rec.el, `text starts ${r1(-ext.l)}px left of the viewport`, 'remove the negative offset', 'overflow'); flaggedOverflow.add(rec.el); }
      }
    }
    // pictures and drawings that leave the slide
    if (slideMode) {
      for (const g of root.querySelectorAll('img, canvas, video, svg')) {
        if (g.closest(IGNORE) || g.classList.contains('sk-deco') || g.classList.contains('sk-specks') || g.parentElement.closest('svg')) continue;
        if (hidden(g)) continue;
        const R = g.getBoundingClientRect();
        if (R.width < 2 || R.height < 2) continue;
        const ex = Math.max(R.right - S.right, R.bottom - S.bottom, S.left - R.left, S.top - R.top);
        if (ex > 4 * sc) add('warn', g, `graphic leaves the slide by ${r1(ex / sc)}px`, 'resize or move it inside 1920x1080', 'overflow');
      }
    } else if (document.documentElement.scrollWidth > document.documentElement.clientWidth + 2) {
      add('error', document.body, `page scrolls sideways (${document.documentElement.scrollWidth}px content in a ${document.documentElement.clientWidth}px viewport)`, 'use max-width: 100% and let rows wrap', 'overflow');
    }
  }

  /* ----- overlapping text boxes ----- */
  if (want('overlap')) {
    const inter = (a, b) => ({ w: Math.min(a.r, b.r) - Math.max(a.l, b.l), h: Math.min(a.b, b.b) - Math.max(a.t, b.t) });
    let count = 0;
    for (let i = 0; i < recList.length && count < 30; i++) {
      for (let j = i + 1; j < recList.length && count < 30; j++) {
        const A = recList[i], B = recList[j];
        if (A.curved || B.curved) continue;
        let hit = false;
        for (const a of A.band) {
          for (const b of B.band) {
            const x = inter(a, b);
            if (x.w < 4 * sc || x.h < 3 * sc) continue;
            const area = x.w * x.h;
            const small = Math.min((a.r - a.l) * (a.b - a.t), (b.r - b.l) * (b.b - b.t));
            if (area >= 0.2 * small) { hit = true; break; }
          }
          if (hit) break;
        }
        if (hit) { count++; add('error', A.el, `text overlaps ${describe(B.el)}`, 'move one of them or shorten the text (data-lint-ignore if intended)', 'overlap'); }
      }
    }
  }

  /* ----- pencil strokes through text ----- */
  if (want('strokes')) {
    const OWN = new Set(['underline', 'circle', 'strike', 'highlight', 'bracket']);
    const hits = new Map();
    const paths = Array.from(root.querySelectorAll('path.sk-path')).filter((p) => !p.closest(IGNORE) && p.checkVisibility && p.checkVisibility({ checkOpacity: true, checkVisibilityCSS: true }));
    for (const p of paths) {
      const bb = p.getBoundingClientRect();
      if (bb.width === 0 && bb.height === 0) continue;
      const deco = p.closest('svg.sk-deco');
      const owner = deco ? deco.parentElement : null;
      const kind = owner ? owner.getAttribute('data-sk') : null;
      const cands = recList.filter((rec) => {
        if (rec.curved) return false;
        if (owner && OWN.has(kind) && (owner.contains(rec.el) || owner.parentElement === rec.el)) return false;
        return rec.band.some((b) => b.l < bb.right + 1 && b.r > bb.left - 1 && b.t < bb.bottom + 1 && b.b > bb.top - 1);
      });
      if (!cands.length) continue;
      const len = p.getTotalLength();
      const m = p.getScreenCTM();
      if (!m || !len) continue;
      const k = Math.hypot(m.a, m.b);
      const n = Math.min(400, Math.max(8, Math.ceil((len * k) / 2.5)));
      const seg = (len * k) / n;
      const per = new Map();
      for (let i = 0; i <= n; i++) {
        const pt = p.getPointAtLength((len * i) / n);
        const x = m.a * pt.x + m.c * pt.y + m.e, y = m.b * pt.x + m.d * pt.y + m.f;
        for (const rec of cands) {
          if (rec.band.some((b) => x >= b.l && x <= b.r && y >= b.t && y <= b.b)) per.set(rec, (per.get(rec) || 0) + seg);
        }
      }
      for (const [rec, length] of per) {
        const bandH = Math.min(...rec.band.map((b) => b.b - b.t));
        if (length < Math.min(8 * sc, 0.6 * bandH)) continue;
        const h = hits.get(rec) || { length: 0, strokes: 0 };
        h.length += length; h.strokes++;
        hits.set(rec, h);
      }
    }
    for (const [rec, h] of hits) {
      const px = h.length / sc;
      add(px >= 24 ? 'error' : 'warn', rec.el, `${h.strokes} pencil stroke${h.strokes === 1 ? '' : 's'} cross the text (about ${Math.round(px)}px of line)`, 'move the drawing off the words (data-lint-ignore if intended)', 'strokes');
    }
  }

  /* ----- type size ----- */
  if (want('size')) {
    const exempt = '.sk-stamp, .sk-tape, .sk-slip-head, .sk-postmark-text, [data-lint-small-ok], sup, sub';
    const bySvg = new Map();
    const small = [];
    for (const rec of recList) {
      if (rec.svg) {
        if (rec.fs < opts.minSvg) { const s = rec.el.closest('svg'); if (s) bySvg.set(s, (bySvg.get(s) || 0) + 1); }
        continue;
      }
      if (rec.el.closest(exempt)) continue;
      if (rec.fs < opts.minFont - 0.25) small.push(rec);
    }
    small.slice(0, 8).forEach((rec) => add(rec.fs < opts.minFont * 0.75 ? 'error' : 'warn', rec.el, `body text is ${r1(rec.fs)}px, under ${opts.minFont}px`, `raise font-size to ${opts.minFont}px or cut the text`, 'size'));
    if (small.length > 8) add('warn', root, `${small.length - 8} more text elements are under ${opts.minFont}px`, `raise them to ${opts.minFont}px`, 'size');
    for (const [s, n] of bySvg) add('warn', s, `${n} drawing label${n === 1 ? '' : 's'} under ${opts.minSvg}px once scaled`, 'draw the labels larger or enlarge the drawing', 'size');
  }

  /* ----- contrast ----- */
  if (want('contrast')) {
    let n = 0;
    for (const rec of recList) {
      const cs = rec.cs;
      if (cs.mixBlendMode && cs.mixBlendMode !== 'normal') continue;
      if (rec.el.closest('.sk-stamp, .sk-postmark-text, [data-lint-contrast-ok]')) continue;
      if (cs.webkitTextFillColor === 'rgba(0, 0, 0, 0)' || /text/.test(cs.webkitBackgroundClip || cs.backgroundClip || '')) continue;
      const fg = parseColor(rec.svg ? cs.fill : cs.color);
      if (!fg || fg[3] === 0) continue;
      const bg = paperBehind(rec.svg ? (rec.el.closest('svg').parentElement || rec.el) : rec.el);
      if (!bg) continue;
      const a = fg[3] * opacityChain(rec.el);
      const text = over([fg[0], fg[1], fg[2], a], bg);
      const rr = ratio(text, bg);
      const large = rec.fs >= 28;
      const need = large ? 3 : 4.5;
      if (rr + 0.005 >= need) continue;
      if (++n > 8) continue;
      add(rr < 3 ? 'error' : 'warn', rec.el, `contrast ${rr.toFixed(2)}:1 on its paper, needs ${need}:1${large ? ' (large text)' : ''}`, 'use a darker pencil on light paper or a lighter one on dark paper (--sk-ink, --sk-graphite)', 'contrast');
    }
    if (n > 8) add('warn', root, `${n - 8} more text elements fail contrast`, 'fix the shared color token', 'contrast');
  }

  /* ----- words and bullets per slide ----- */
  if (slideMode && want('words')) {
    let words = 0;
    for (const rec of recList) {
      if (rec.svg || rec.el.closest('h1, h2, h3, h4, h5, h6, .sk-h1, .sk-h2, .sk-h3, .sk-stamp, .sk-tape, button, .sk-btn')) continue;
      for (const nd of Array.from(rec.el.childNodes)) if (nd.nodeType === 3) words += (nd.nodeValue.match(/[\p{L}\p{N}][\p{L}\p{N}'’-]*/gu) || []).length;
    }
    if (words > opts.maxWords) add('warn', root, `${words} words of body text, limit ${opts.maxWords}`, 'cut to the one idea of this slide or split it in two', 'words');
    const bullets = Array.from(root.querySelectorAll('li')).filter((li) => !hidden(li)).length;
    if (bullets > opts.maxBullets) add('warn', root, `${bullets} bullets, limit ${opts.maxBullets}`, 'keep the strongest few, or split the slide', 'words');
  }

  /* ----- placeholder text ----- */
  if (want('placeholder')) {
    const PAT = [[/\blorem\b/i, 'lorem'], [/\bipsum\b/i, 'ipsum'], [/\bTODO\b/, 'TODO'], [/\bx{3,}\b/i, 'xxx'], [/\[insert/i, '[insert'], [/\bTBD\b/, 'TBD']];
    const seen = new Set();
    const scan = (el, text, attr) => {
      for (const [re, name] of PAT) {
        const key = el.localName + name + (attr || '') + text.slice(0, 20);
        if (re.test(text) && !seen.has(key)) {
          seen.add(key);
          add('error', el, `placeholder text "${name}"${attr ? ` in ${attr}` : ''}`, 'write the real content', 'placeholder');
        }
      }
    };
    for (const nd of allTextNodes) if (nd.parentElement && !nd.parentElement.closest(IGNORE)) scan(nd.parentElement, nd.nodeValue, '');
    const attrEls = [root, ...root.querySelectorAll('[data-notes], [alt], [title], [aria-label]')];
    for (const el of attrEls) for (const a of ['data-notes', 'alt', 'title', 'aria-label']) { const v = el.getAttribute && el.getAttribute(a); if (v) scan(el, v, a); }
  }

  /* ----- accessibility: images, charts ----- */
  if (want('a11y')) {
    for (const img of root.querySelectorAll('img')) {
      if (!img.hasAttribute('alt')) add('error', img, 'image has no alt text', 'add alt="..." (alt="" when it is only decoration)', 'a11y');
    }
    for (const svg of root.querySelectorAll('svg[role="img"]')) {
      if (!svg.getAttribute('aria-label') && !svg.getAttribute('aria-labelledby') && !svg.querySelector(':scope > title')) add('error', svg, 'svg with role="img" has no name', 'add aria-label="..." describing the picture', 'a11y');
    }
    const charts = new Set([...root.querySelectorAll('figure.sk-chart, [data-chart]')]);
    for (const fig of charts) {
      if (fig.closest(IGNORE)) continue;
      const tbl = fig.querySelector('table');
      if (!tbl || !tbl.querySelector('tr')) add('error', fig, 'chart has no hidden data table', 'load sketchy-charts.js and call Sketchy.mount(), or add a visually hidden <table> with the data', 'a11y');
      else if (!fig.querySelector('svg')) add('error', fig, 'chart is not drawn', 'call SketchyCharts.render(figure) or Sketchy.mount() after the page loads', 'a11y');
    }
  }

  /* ----- sideways scrolling is covered above; document-level checks below run once ----- */
  if (opts.doc) {
    if (want('doc')) {
      if (!document.title || !document.title.trim()) add('error', null, 'missing <title>', 'add <title>Short name</title> in <head>', 'doc');
      if (!document.documentElement.getAttribute('lang')) add('error', null, 'missing lang on <html>', 'add lang="en" (or the page language) to <html>', 'doc');
      const main = document.querySelector('main.sk-deck');
      if (main) {
        if (!main.getAttribute('data-seed')) add('error', main, 'deck has no data-seed', 'add data-seed="your-deck-name" to main.sk-deck so every render draws the same lines', 'doc');
        if (!window.SketchyDeck) add('error', main, 'deck runtime is not loaded (SketchyDeck is undefined)', 'include engine/sketchy-deck.js before the page script', 'doc');
      }
    }
    if (want('fonts')) {
      const used = new Map();
      for (const rec of recList) {
        const fam = rec.cs.fontFamily.split(',')[0].replace(/["']/g, '').trim();
        const u = used.get(fam) || { specs: new Map(), text: '' };
        const key = rec.cs.fontStyle + ' ' + rec.cs.fontWeight;
        u.specs.set(key, (u.specs.get(key) || '') + ' ' + (rec.el.textContent || '').slice(0, 120));
        used.set(fam, u);
      }
      const faces = Array.from(document.fonts);
      for (const fam of ['Caveat', 'Courier Prime']) {
        if (!used.has(fam)) continue;
        const u = used.get(fam);
        const mine = faces.filter((f) => f.family.replace(/["']/g, '') === fam);
        let why = '';
        if (!mine.length) why = 'no @font-face declares it, so the browser falls back to another font';
        else if (mine.some((f) => f.status === 'error')) why = 'its font file failed to load';
        else if (!mine.some((f) => f.status === 'loaded')) why = 'its font file never loaded';
        else {
          for (const [spec, text] of u.specs) if (!document.fonts.check(`${spec} 20px "${fam}"`, text)) { why = `document.fonts.check() is false for ${spec}`; break; }
        }
        if (why) add('error', null, `font ${fam} is not loaded: ${why}`, 'link engine/sketchy.css (it loads engine/fonts) or inline everything with build.mjs', 'fonts');
      }
    }
  }
  return { issues };
}

/* ------------------------------------------------------------------ */

async function main() {
  const { values, positionals } = parseArgs(process.argv.slice(2), spec);
  const json = values.json;
  if (json) console.log = console.error; // stdout carries only the JSON
  const file = requireHtmlFile(positionals[0], 'html file');
  const pw = requirePlaywright();
  const browser = await launchChromium(pw);
  const all = [];
  const net = { errors: new Map(), failed: new Map(), external: new Map() };
  let kind = 'page', slides = 0;
  const seen = new Set();
  const push = (list, tag = '') => {
    for (const i of list) {
      const item = tag ? { ...i, where: `${i.where}${tag}` } : i;
      const key = `${item.severity}|${item.where}|${item.problem}`;
      if (seen.has(key)) continue;
      seen.add(key);
      all.push(item);
    }
  };

  try {
    // deck or page?
    {
      const { context, page } = await openPage(browser, { width: 1920, height: 1080 });
      watchPage(page, net);
      await page.goto(fileUrl(file, 'static'), { waitUntil: 'load' });
      await waitReady(page);
      if (await isDeckPage(page)) { kind = 'deck'; slides = await slideCount(page); }
      await context.close();
    }

    if (kind === 'deck') {
      if (slides === 0) all.push({ severity: 'error', where: 'deck', problem: 'main.sk-deck has no .sk-slide sections', fix: 'add <section class="sk-slide"> elements inside main.sk-deck', check: 'doc', slide: null });
      const { context, page } = await openPage(browser, { width: 1920, height: 1080 });
      watchPage(page, net);
      for (let n = 1; n <= slides; n++) {
        await page.goto(fileUrl(file, `slide=${n}&static`), { waitUntil: 'load' });
        await waitReady(page);
        const visible = await page.evaluate((i) => { const s = document.querySelectorAll('main.sk-deck .sk-slide')[i]; if (!s) return false; const r = s.getBoundingClientRect(); return r.width > 0 && r.height > 0; }, n - 1);
        if (!visible) { push([{ severity: 'error', where: `slide ${n}`, problem: 'slide is not visible with ?slide=N&static', fix: 'check the deck runtime and that the section is a direct .sk-slide of main.sk-deck', check: 'doc', slide: n }]); continue; }
        const res = await page.evaluate(analyzePage, { mode: 'slide', slideIndex: n - 1, doc: n === 1, minFont: 20, minSvg: 14, maxWords: 40, maxBullets: 6 });
        push(res.issues);
      }
      await context.close();
    } else {
      const sizes = [{ w: 1280, h: 800, tag: '', only: null }];
      if (!values.noMobile) sizes.push({ w: 390, h: 844, tag: ' (at 390px wide)', only: ['overflow', 'overlap'] });
      for (const s of sizes) {
        const { context, page } = await openPage(browser, { width: s.w, height: s.h, mobile: s.w <= 600 });
        watchPage(page, net);
        await page.goto(fileUrl(file, 'static'), { waitUntil: 'load' });
        await waitReady(page);
        const res = await page.evaluate(analyzePage, { mode: 'page', doc: !s.only, only: s.only, minFont: 16, minSvg: 11, maxWords: 1e9, maxBullets: 1e9 });
        push(res.issues, s.tag);
        await context.close();
      }
    }
  } finally {
    await browser.close();
  }

  // network and console
  for (const [url] of net.external) all.push({ severity: 'error', where: 'network', problem: `external request ${url}`, fix: 'run build.mjs and use local files only; the final file must work offline', check: 'network', slide: null });
  for (const [msg] of net.failed) all.push({ severity: 'error', where: 'network', problem: `request failed: ${msg}`, fix: 'check the path, or run build.mjs so everything is inlined', check: 'network', slide: null });
  for (const [msg] of net.errors) all.push({ severity: 'error', where: 'console', problem: msg, fix: 'open the file in a browser console and fix the script error', check: 'console', slide: null });

  const rank = { error: 0, warn: 1 };
  all.sort((a, b) => (a.slide ?? 0) - (b.slide ?? 0) || rank[a.severity] - rank[b.severity]);
  const errors = all.filter((i) => i.severity === 'error').length;
  const warnings = all.length - errors;

  if (json) {
    process.stdout.write(JSON.stringify({ file: rel(file), kind, slides, errors, warnings, issues: all }, null, 2) + '\n');
  } else {
    say.line(c.bold(`sketch-lint ${rel(file)} (${kind === 'deck' ? `deck, ${slides} slide${slides === 1 ? '' : 's'}` : 'page'})`));
    for (const i of all) {
      const label = i.severity === 'error' ? c.red('error') : c.yellow('warn ');
      say.line(`${label}  ${i.where}  ${i.problem}  fix: ${i.fix}`);
    }
    say.line(`${errors} error${errors === 1 ? '' : 's'}, ${warnings} warning${warnings === 1 ? '' : 's'}`);
  }
  process.exit(errors > 0 || (values.strict && warnings > 0) ? 1 : 0);
}

if (isMain(import.meta.url)) main().catch((e) => die(`lint failed: ${String(e && e.message ? e.message : e).split('\n')[0]}`, 'node doctor.mjs', 1));
