#!/usr/bin/env node
'use strict';

/**
 * render-html-pptx.js  — PoC: content.json → HTML (html-ppt-skill layouts) → PPTX (dom-to-pptx)
 *
 * Usage:
 *   node yuanfang-html-ppt/scripts/render-html-pptx.js \
 *     --file content-multipage.json --theme pitch-deck-vc --output /tmp/deck.pptx
 *
 * Requires: playwright, dom-to-pptx (already installed)
 */

const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright');
const { loadContent } = require('./load-content');

const ROOT = path.resolve(__dirname, '..', '..');
const DESIGN_DIR = path.join(ROOT, 'yuanfang-design');

// ── Helpers ──────────────────────────────────────────────────────────

function readFile(p) {
  try { return fs.readFileSync(p, 'utf8'); } catch { return ''; }
}

function px(n) { return `${n}px`; }

// ── Layout generators ──────────────────────────────────────────────────
// Each returns the <section> inner HTML matching html-ppt-skill patterns.

function coverLayout(slide) {
  const { title, subtitle, tags } = slide;
  const tagsHtml = tags?.length
    ? `<div class="row wrap mt-l">${tags.map(t => `<span class="pill">${escHtml(t)}</span>`).join('')}</div>`
    : '';
  return `
    <div class="deck-header">
      <span class="eyebrow" style="display:inline-block;min-width:400px">${escHtml(slide.brand || 'Keynote')} · 2026</span>
      ${slide.logo ? `<img src="${slide.logo}" style="height:44px;width:auto"/>` : `<span class="eyebrow">html-ppt × dom-to-pptx</span>`}
    </div>
    <div style="max-width:100%">
      ${slide.kicker ? `<p class="kicker">${escHtml(slide.kicker)}</p>` : ''}
      <h1 class="h1">${title || 'Title'}</h1>
      ${subtitle ? `<p class="lede">${escHtml(subtitle)}</p>` : ''}
      ${tagsHtml}
    </div>`;
}

function sectionLayout(slide) {
  return `
    <div style="text-align:center">
      ${slide.kicker ? `<p class="kicker">${escHtml(slide.kicker)}</p>` : ''}
      <h1 class="h1" style="font-size:96px;display:inline-block;min-width:600px">${slide.title || ''}</h1>
      <div class="divider-accent" style="margin:28px auto"></div>
      ${slide.subtitle ? `<p class="lede" style="margin:0 auto;max-width:1000px">${escHtml(slide.subtitle)}</p>` : ''}
    </div>
  `;
}

function contentLayout(slide) {
  const { title, points } = slide;
  // Use <div> not <ul>/<li>: dom-to-pptx collapses <ul> wrapping cards into
  // one shape, losing card backgrounds. <div> preserves the card structure.
  // Use a separate <div class="card-line"> for the accent stripe: dom-to-pptx
  // drops borders when both `border` and `border-top` are declared together.
  const list = points?.length
    ? `<div class="grid g1" style="gap:14px">
        ${points.map((p, i) => {
          const num = String(i + 1).padStart(2, '0');
          return `<div class="card"><div class="card-line"></div><div class="row" style="gap:18px;align-items:baseline;padding:0 28px">
            <div style="font-size:40px;font-weight:800;color:var(--accent);min-width:90px">${num}</div>
            <div style="font-size:32px;font-weight:500;color:var(--text-1);flex:1">${escHtml(p)}</div>
          </div></div>`;
        }).join('')}
      </div>`
    : '';
  return `
    ${slide.kicker ? `<p class="kicker">${escHtml(slide.kicker)}</p>` : ''}
    <h2 class="h2">${escHtml(title)}</h2>
    ${slide.lede ? `<p class="lede mb-l">${escHtml(slide.lede)}</p>` : ''}
    ${list}`;
}

function twoColumnLayout(slide) {
  const { title, leftTitle, leftPoints, rightTitle, rightPoints } = slide;
  return `
    ${slide.kicker ? `<p class="kicker">${escHtml(slide.kicker)}</p>` : ''}
    <h2 class="h2">${escHtml(title)}</h2>
    <div class="grid g2 mt-l" style="align-items:start">
      <div class="card">
        <h3 class="h3">${escHtml(leftTitle)}</h3>
        <ul class="mt-m">${(leftPoints||[]).map(p => `<li style="margin-bottom:10px;font-size:34px;color:var(--text-2)">${escHtml(p)}</li>`).join('')}</ul>
      </div>
      <div class="card">
        <div class="card-line"></div>
        <h3 class="h3">${escHtml(rightTitle)}</h3>
        <ul class="mt-m">${(rightPoints||[]).map(p => `<li style="margin-bottom:10px;font-size:34px;color:var(--text-2)">${escHtml(p)}</li>`).join('')}</ul>
      </div>
    </div>`;
}

function dataLayout(slide) {
  const { title, metrics } = slide;
  const count = metrics?.length || 3;
  const cols = count <= 3 ? `g${count}` : 'g4';
  return `
    <p class="kicker">Metrics · 关键数字</p>
    <h2 class="h2">${escHtml(title)}</h2>
    <div class="grid ${cols} mt-l anim-stagger-list">
      ${(metrics||[]).map(m => `
        <div class="card">
          <p class="eyebrow" style="font-size:28px">${escHtml(m.label)}</p>
          <div style="font-size:64px;font-weight:800;line-height:1.1">${escHtml(m.value)}</div>
          ${m.change ? `<p style="margin:8px 0 0;font-size:34px;color:${m.change.startsWith('↑') ? 'var(--good)' : 'var(--warn)'}">${escHtml(m.change)}</p>` : ''}
        </div>`).join('')}
    </div>`;
}

function quoteLayout(slide) {
  const { quote, attribution, title } = slide;
  return `
    ${slide.kicker ? `<p class="kicker">${escHtml(slide.kicker)}</p>` : ''}
    <h2 class="h2">${escHtml(title)}</h2>
    <div class="card" style="margin-top:24px;padding:40px;text-align:center">
      <div style="font-size:64px;line-height:1;color:var(--accent);opacity:0.3;margin-bottom:8px">"</div>
      <p style="font-size:40px;line-height:1.6;font-weight:500;max-width:1000px;margin:0 auto">${escHtml(quote)}</p>
      <div style="margin-top:24px;padding-top:16px;border-top:1px solid var(--border)">
        <span class="pill-accent">${escHtml(attribution)}</span>
      </div>
    </div>`;
}

function summaryLayout(slide) {
  const { title, points } = slide;
  return `
    <p class="kicker">Next · 下一步</p>
    <h2 class="h2" style="margin-bottom:32px">${escHtml(title)}</h2>
    <div class="grid g1" style="gap:20px;max-width:1100px">
      ${(points||[]).map(p => `
        <div style="display:grid;grid-template-columns:auto 1fr;gap:20px;align-items:center">
          <div style="width:16px;height:16px;border-radius:50%;background:var(--accent)"></div>
          <div style="font-size:36px;font-weight:500;line-height:1.3">${escHtml(p)}</div>
        </div>`).join('')}
    </div>`;
}

// Table of contents — grid of numbered sections
function tocLayout(slide) {
  const { items } = slide;
  const list = (items || []).map((item, i) => {
    const num = String(i + 1).padStart(2, '0');
    return `<div class="card">
      <div class="row" style="gap:24px;align-items:flex-start">
        <div class="h3" style="color:var(--text-3);width:64px;flex-shrink:0">${num}</div>
        <div style="flex:1;min-width:0">
          <h4 style="margin:0 0 8px;font-size:28px;font-weight:700">${escHtml(item.title || '')}</h4>
          ${item.desc ? `<p class="dim" style="font-size:20px;line-height:1.4;margin:0">${escHtml(item.desc)}</p>` : ''}
        </div>
      </div>
    </div>`;
  }).join('');
  return `
    ${slide.kicker ? `<p class="kicker">${escHtml(slide.kicker)}</p>` : ''}
    <h2 class="h2">${slide.title || 'Contents'}</h2>
    <div class="grid g2" style="margin-top:24px;gap:18px">${list}</div>`;
}

// Three-column feature grid (icon + title + description)
function threeColumnLayout(slide) {
  const { items } = slide;
  const list = (items || []).map(item => `
    <div class="card card-accent">
      <div class="card-line"></div>
      <div style="font-size:64px;line-height:1;margin-bottom:18px">${escHtml(item.icon || '✦')}</div>
      <h4 class="h3" style="margin:0 0 12px">${escHtml(item.title || '')}</h4>
      <p class="dim" style="font-size:22px;line-height:1.5;margin:0">${escHtml(item.desc || '')}</p>
    </div>`).join('');
  return `
    ${slide.kicker ? `<p class="kicker">${escHtml(slide.kicker)}</p>` : ''}
    <h2 class="h2">${slide.title || ''}</h2>
    ${slide.lede ? `<p class="lede mb-l">${escHtml(slide.lede)}</p>` : ''}
    <div class="grid g3" style="margin-top:24px;gap:22px">${list}</div>`;
}

// Numbered process steps (horizontal flow with circular numbers)
function processStepsLayout(slide) {
  const { steps } = slide;
  const list = (steps || []).map((s, i) => `
    <div class="step">
      <div class="num">${i + 1}</div>
      <h4 style="margin:18px 0 8px;font-size:26px;font-weight:700">${escHtml(s.title || '')}</h4>
      <p class="dim" style="font-size:20px;line-height:1.5;margin:0">${escHtml(s.desc || '')}</p>
      ${s.tag ? `<span class="pill" style="margin-top:12px">${escHtml(s.tag)}</span>` : ''}
    </div>`).join('');
  return `
    ${slide.kicker ? `<p class="kicker">${escHtml(slide.kicker)}</p>` : ''}
    <h2 class="h2">${slide.title || ''}</h2>
    ${slide.lede ? `<p class="lede mb-l">${escHtml(slide.lede)}</p>` : ''}
    <div class="steps">${list}</div>`;
}

// Horizontal timeline with dot connectors
function timelineLayout(slide) {
  const { items } = slide;
  const list = (items || []).map(item => `
    <div class="tl-item">
      <div class="tl-year">${escHtml(item.year || '')}</div>
      <div class="tl-dot"></div>
      <h4 style="margin:16px 0 6px;font-size:26px;font-weight:700">${escHtml(item.title || '')}</h4>
      <p class="dim" style="font-size:20px;line-height:1.4;margin:0">${escHtml(item.desc || '')}</p>
    </div>`).join('');
  return `
    ${slide.kicker ? `<p class="kicker">${escHtml(slide.kicker)}</p>` : ''}
    <h2 class="h2">${slide.title || ''}</h2>
    <div class="tl">${list}</div>`;
}

// Big quote — centered, oversized serif, accent quote mark
function bigQuoteLayout(slide) {
  return `
    <div style="max-width:1100px;margin:0 auto;text-align:center">
      <div class="serif" style="font-size:160px;line-height:.85;color:var(--accent);opacity:.55;margin-bottom:-30px">"</div>
      <blockquote class="serif" style="font-size:54px;line-height:1.3;font-style:italic;font-weight:600;margin:0 0 36px">${slide.quote || ''}</blockquote>
      <div class="row" style="justify-content:center;gap:16px;align-items:center">
        ${slide.avatar ? `<div style="width:48px;height:48px;border-radius:50%;background:var(--grad)"></div>` : ''}
        <span style="font-size:22px;font-weight:600;letter-spacing:.04em">${escHtml(slide.attribution || '')}</span>
        ${slide.role ? `<span class="dim" style="font-size:20px">· ${escHtml(slide.role)}</span>` : ''}
      </div>
    </div>`;
}

// Stat highlight — single huge number, minimal supporting text
// Common in pitch decks for "headline metric" slides
function statLayout(slide) {
  const { stats } = slide;
  const list = (stats || []).map(s => `
    <div class="stat-item">
      <div class="stat-num gradient-text">${escHtml(s.value || '')}</div>
      <div class="stat-label">${escHtml(s.label || '')}</div>
      ${s.context ? `<div class="stat-context dim">${escHtml(s.context)}</div>` : ''}
    </div>`).join('');
  return `
    ${slide.kicker ? `<p class="kicker">${escHtml(slide.kicker)}</p>` : ''}
    <h2 class="h2" style="margin-bottom:24px">${escHtml(slide.title || '')}</h2>
    <div class="stat-grid">${list}</div>
    ${slide.caption ? `<p class="lede" style="text-align:center;margin-top:32px">${escHtml(slide.caption)}</p>` : ''}`;
}

// Comparison — side-by-side with checkmarks/dots
function comparisonLayout(slide) {
  const { items, leftLabel, rightLabel, leftColor, rightColor } = slide;
  const list = (items || []).map(item => `
    <div class="comparison-row">
      <div class="comparison-cell" style="color:${leftColor || 'var(--bad)'}">
        ${item.left ? '<span class="comparison-mark bad">✗</span>' : '<span class="comparison-mark ok">✓</span>'}
        <span>${escHtml(item.left || item.label || '')}</span>
      </div>
      <div class="comparison-divider"></div>
      <div class="comparison-cell" style="color:${rightColor || 'var(--good)'}">
        ${item.right ? '<span class="comparison-mark good">✓</span>' : '<span class="comparison-mark bad">✗</span>'}
        <span>${escHtml(item.right || '')}</span>
      </div>
    </div>`).join('');
  return `
    ${slide.kicker ? `<p class="kicker">${escHtml(slide.kicker)}</p>` : ''}
    <h2 class="h2">${slide.title || 'Comparison'}</h2>
    <div style="max-width:1400px;margin:0 auto;width:100%">
      <div class="comparison-header" style="margin-top:24px;margin-bottom:16px">
        <div style="font-size:24px;font-weight:700;color:${leftColor || 'var(--bad)'};padding-left:46px">${escHtml(leftLabel || 'Before')}</div>
        <div></div>
        <div style="font-size:24px;font-weight:700;color:${rightColor || 'var(--good)'};padding-left:46px">${escHtml(rightLabel || 'After')}</div>
      </div>
      <div class="comparison-list">${list}</div>
    </div>`;
}

// ── HTML generators map ──────────────────────────────────────────────

const LAYOUTS = {
  cover:        coverLayout,
  section:      sectionLayout,
  content:      contentLayout,
  'two-column':  twoColumnLayout,
  data:         dataLayout,
  quote:        quoteLayout,
  summary:      summaryLayout,
  // New layouts (aesthetic-rich, ported from html-ppt-skill 31-template system)
  toc:          tocLayout,
  'three-column': threeColumnLayout,
  process:      processStepsLayout,
  timeline:     timelineLayout,
  'big-quote':  bigQuoteLayout,
  stat:         statLayout,
  comparison:   comparisonLayout,
  // aliases
  bullets:      contentLayout,
  'kpi-grid':   dataLayout,
  'section-divider': sectionLayout,
  thanks:      (s) => ` <div style="text-align:center;padding:40px 0">
    <h1 class="h1" style="font-size:120px;line-height:1"><span class="gradient-text" style="display:inline-block;min-width:400px">Thanks</span></h1>
    ${s.subtitle ? `<p class="lede" style="margin:24px auto 0">${escHtml(s.subtitle)}</p>` : ''}
    <div class="row mt-l" style="justify-content:center;gap:40px">
      ${(s.points||[]).map(p => `<span class="dim2" style="font-size:36px">${escHtml(p)}</span>`).join('')}
    </div>
  </div>`,
};

function escHtml(s) {
  if (typeof s !== 'string') return String(s ?? '');
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

// ── HTML document generator ──────────────────────────────────────────

function buildHtml(slides, theme, themeCss) {
  const slidesHtml = slides.map((slide, i) => {
    const gen = LAYOUTS[slide.layout];
    if (!gen) return '';
    const inner = gen(slide);
    const isCenter = ['section', 'thanks'].includes(slide.layout);
    const extraClass = isCenter ? ' tc center' : '';
    // Per-slide class (Mar p-style metadata) for layout variants. e.g.
    // { layout: "content", class: "compact" } → section gets class="slide content-compact"
    const variantClass = slide.class ? ` ${escHtml(slide.layout)}-${escHtml(slide.class)}` : '';
    // Speaker notes embedded as hidden aside; post-processor extracts these
    // and writes them into notesSlideN.xml inside the PPTX zip.
    const notesHtml = slide.notes
      ? `<aside class="notes" data-notes="${escHtml(slide.notes)}" style="display:none">${escHtml(slide.notes)}</aside>`
      : '';
    const footerLabel = slide.footer || '';
    return `<section class="slide${extraClass}${variantClass}" data-title="${escHtml(slide.title || '')}" data-index="${i}">
  ${inner}
  <div class="deck-footer">
    <span class="dim2">${escHtml(footerLabel)}</span>
    <span class="dim2">${i + 1} / ${slides.length}</span>
  </div>
  ${notesHtml}
</section>`;
  }).join('\n\n');

  // html-ppt-skill base styles (subset needed for dom-to-pptx, no runtime.js)
  const baseStyles = `
@font-face{font-family:"Arial";src:local("Liberation Sans"),local("DejaVu Sans")}
@font-face{font-family:"PingFang SC";src:local("Liberation Sans"),local("DejaVu Sans")}
:root {
  --space-1:8px;--space-2:16px;--space-3:24px;--space-4:48px;
  --letter-tight:-.03em;--letter-normal:-.01em;
  --ease:cubic-bezier(.4,0,.2,1);
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:100%;background:#1a1a1a;font-family:var(--font-sans)}
/* Slides stack vertically — no transform on any ancestor (dom-to-pptx constraint) */
#deck{display:flex;flex-direction:column;align-items:center;gap:24px;padding:24px 0}
.slide{
  width:1920px;height:1080px;position:relative;overflow:hidden;
  display:flex;flex-direction:column;justify-content:center;
  padding:88px 120px;background:var(--bg);color:var(--text-1);
  font-family:var(--font-sans);flex-shrink:0
}
.slide.tc{text-align:center}
.slide.center{align-items:center;justify-content:center}
.deck-header{
  position:absolute;top:24px;left:40px;right:40px;
  display:flex;justify-content:space-between;pointer-events:none;
  z-index:10
}
.deck-footer{
  position:absolute;bottom:28px;left:40px;right:40px;
  display:flex;justify-content:space-between;font-size:28px;color:var(--text-3);
  z-index:10
}
/* Nav bar — fixed, NOT an ancestor of .slide (safe for dom-to-pptx) */
#nav{position:fixed;bottom:24px;left:50%;margin-left:-180px;width:360px;
  display:flex;align-items:center;justify-content:space-between;z-index:100;
  background:rgba(0,0,0,.6);padding:10px 20px;border-radius:40px;box-sizing:border-box}
#nav .dots{display:flex;gap:6px;flex:1;justify-content:center}
#nav .dot{width:10px;height:10px;border-radius:50%;background:rgba(255,255,255,.3);cursor:pointer;flex-shrink:0}
#nav .dot.active{background:#fff;width:14px;height:14px}
#nav .counter{color:rgba(255,255,255,.6);font-size:14px;min-width:50px;text-align:center}
#nav .arrow{color:rgba(255,255,255,.7);font-size:22px;cursor:pointer;padding:0 6px;user-select:none;flex-shrink:0}
#nav .arrow:hover{color:#fff}
/* PPTX-optimized sizes (dom-to-pptx maps 1920px→10in, ratio 192px/in)
 * Target min body: 14pt → need 14/0.375 = 37px HTML */
.eyebrow{font-size:30px;font-weight:500;letter-spacing:.16em;text-transform:uppercase;color:var(--text-3)}
.kicker{font-size:32px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;margin-bottom:16px;color:var(--accent)}
.h1{font-family:var(--font-display);font-size:80px;line-height:1.05;font-weight:800;letter-spacing:var(--letter-tight);color:var(--text-1);margin-bottom:20px}
.h2{font-size:54px;line-height:1.1;font-weight:700;letter-spacing:var(--letter-tight);margin-bottom:12px}
.h3{font-size:38px;line-height:1.2;font-weight:600;margin-bottom:8px}
.lede{font-size:36px;line-height:1.5;color:var(--text-2);max-width:1500px}
.dim{color:var(--text-2)}
.dim2{color:var(--text-3)}
.gradient-text{background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;color:var(--accent)}
.row{display:flex;gap:14px;align-items:center;flex-wrap:wrap}
.grid{display:grid;gap:24px}
.g1{grid-template-columns:1fr}
.g2{grid-template-columns:repeat(2,1fr)}
.g3{grid-template-columns:repeat(3,1fr)}
.g4{grid-template-columns:repeat(4,1fr)}
.card{background:var(--surface);border:1px solid var(--border-strong);border-radius:var(--radius);padding:32px 28px;box-shadow:var(--shadow);position:relative;overflow:hidden}
/* Layout variants — Marp-style class metadata, e.g. slide.class="compact" */
.content-compact .card{padding:20px 22px}
.content-compact .grid.g1{gap:10px}
.content-detailed .card{padding:40px 32px}
.content-detailed .grid.g1{gap:22px}
.data-grid .grid{grid-template-columns:repeat(2,1fr)}
.data-list .card{display:flex;flex-direction:row;align-items:center;gap:24px;padding:20px 28px}
.cover-minimal .kicker,.cover-minimal .lede{display:none}
.cover-minimal .h1{margin-bottom:0}
.thanks-contact .row{flex-direction:column;gap:12px}
.card-line{position:absolute;top:0;left:0;right:0;height:4px;background:var(--accent)}
.pill{display:inline-block;padding:6px 20px;border-radius:999px;font-size:26px;font-weight:500;background:var(--surface-2);color:var(--text-2);border:1px solid var(--border);white-space:nowrap}
/* Process steps — circular number badge, lifted card */
.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;margin-top:40px}
.step{position:relative;padding:36px 26px 24px;border:1px solid var(--border-strong);border-radius:var(--radius);background:var(--surface);box-shadow:var(--shadow)}
.step .num{position:absolute;top:-26px;left:22px;width:52px;height:52px;border-radius:50%;background:var(--accent);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:22px;box-shadow:var(--shadow)}
.step h4{margin:0 0 8px}
.step p{font-size:18px;color:var(--text-2);line-height:1.5}
/* Timeline — horizontal flow with year + dot + content */
.tl{position:relative;margin-top:48px;padding-top:64px}
.tl::before{content:"";position:absolute;left:0;right:0;top:48px;height:2px;background:var(--border);z-index:0}
.tl{display:grid;grid-template-columns:repeat(5,1fr);gap:24px;margin-top:48px}
.tl-item{position:relative;padding-top:60px;text-align:center}
.tl-year{font-size:18px;color:var(--text-3);letter-spacing:.12em;text-transform:uppercase;font-weight:600;position:absolute;top:-32px;left:0;right:0}
.tl-dot{position:absolute;top:36px;left:50%;transform:translateX(-50%);width:24px;height:24px;border-radius:50%;background:var(--accent);border:4px solid var(--bg);box-shadow:0 0 0 2px var(--accent);z-index:1}
/* Cover decoration — gradient bg + soft gradient blob (top-right) */

/* Stat highlight — single huge gradient number */
.stat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:48px;margin-top:40px}
.stat-item{text-align:center;display:flex;flex-direction:column;gap:14px}
.stat-num{font-size:180px;font-weight:900;line-height:.95;letter-spacing:-.05em}
.stat-label{font-size:24px;font-weight:700;letter-spacing:.02em}
.stat-context{font-size:18px;line-height:1.4}
/* Comparison — 2-col rows with checkmark markers */
.comparison-list{display:flex;flex-direction:column;gap:0;max-width:1400px;margin:0 auto}
.comparison-header,.comparison-row{display:grid;grid-template-columns:1fr 60px 1fr;gap:24px;align-items:center;padding:18px 0}
.comparison-cell{display:flex;align-items:center;gap:14px;font-size:24px;font-weight:500}
.comparison-mark{font-size:20px;font-weight:800;width:32px;height:32px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;flex-shrink:0}
.comparison-mark.bad{background:color-mix(in srgb,var(--bad) 15%,transparent);color:var(--bad)}
.comparison-mark.ok{background:color-mix(in srgb,var(--good) 15%,transparent);color:var(--good)}
.comparison-divider{height:1px;background:var(--border)}
.pill-accent{background:color-mix(in srgb,var(--accent) 12%,transparent);color:var(--accent);border-color:color-mix(in srgb,var(--accent) 28%,transparent)}
.divider-accent{height:3px;width:72px;background:var(--accent);border-radius:2px;margin:var(--space-2) 0}
.tc .divider-accent{margin-left:auto;margin-right:auto}
.mt-m{margin-top:var(--space-2)}
.mt-l{margin-top:var(--space-3)}
.mb-l{margin-bottom:var(--space-3)}
.ml-m{margin-left:var(--space-2)}
`;

  // Slide viewer — scroll-based nav, no transform (preserves dom-to-pptx compatibility)
  const viewerJs = `
(function(){
  var slides = document.querySelectorAll('.slide');
  var total = slides.length, current = 0;
  function goTo(n){
    if (n < 0 || n >= total) return;
    current = n;
    slides[n].scrollIntoView({behavior:'smooth', block:'start'});
    document.querySelectorAll('.dot').forEach(function(d,i){d.classList.toggle('active',i===n)});
    document.getElementById('counter').textContent = (n+1)+' / '+total;
  }
  function build(){
    var nav = document.createElement('div'); nav.id = 'nav';
    var left = document.createElement('span'); left.className = 'arrow'; left.textContent = '\u25C0';
    left.onclick = function(){goTo(current-1)};
    nav.appendChild(left);
    var dd = document.createElement('div'); dd.className = 'dots';
    for (var i=0;i<total;i++){
      var d = document.createElement('span'); d.className = 'dot'+(i===0?' active':'');
      d.onclick = (function(idx){return function(){goTo(idx)}})(i);
      dd.appendChild(d);
    }
    nav.appendChild(dd);
    var c = document.createElement('span'); c.className = 'counter'; c.id = 'counter';
    c.textContent = '1 / '+total; nav.appendChild(c);
    var r = document.createElement('span'); r.className = 'arrow'; r.textContent = '\u25B6';
    r.onclick = function(){goTo(current+1)}; nav.appendChild(r);
    document.body.appendChild(nav);
  }
  build();
  document.addEventListener('keydown',function(e){
    if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {e.preventDefault(); goTo(current-1);}
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') {e.preventDefault(); goTo(current+1);}
  });
})();
`;

  return `<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="utf-8"><meta name="viewport" content="width=1920">
<title>Slide Deck</title>
<style>
${themeCss}
${baseStyles}
</style>
</head>
<body>
<div id="deck">
${slidesHtml}
</div>
<script>${viewerJs}</script>
</body></html>`;
}

// ── Theme loader ─────────────────────────────────────────────────────

function loadThemeCss(themeName) {
  const base = readFile(path.join(DESIGN_DIR, 'base.css'));
  const theme = readFile(path.join(DESIGN_DIR, 'themes', `${themeName}.css`));
  if (!theme) {
    const avail = fs.readdirSync(path.join(DESIGN_DIR, 'themes'))
      .filter(f => f.endsWith('.css')).map(f => f.replace('.css',''));
    throw new Error(`Theme '${themeName}' not found. Available: ${avail.join(', ')}`);
  }
  // Strip [data-theme="xxx"] wrapper → :root for dom-to-pptx
  let css = theme.replace(/\[data-theme="[^"]*"\]\s*\{/g, ':root {').replace(/\}\s*$/, '}');
  return base + '\n' + css;
}

function adjustColor(hex, amount) {
  hex = hex.replace('#','');
  const r = Math.max(0, Math.min(255, parseInt(hex.substring(0,2),16) + amount));
  const g = Math.max(0, Math.min(255, parseInt(hex.substring(2,4),16) + amount));
  const b = Math.max(0, Math.min(255, parseInt(hex.substring(4,6),16) + amount));
  return `#${r.toString(16).padStart(2,'0')}${g.toString(16).padStart(2,'0')}${b.toString(16).padStart(2,'0')}`;
}

function fixPptxFonts(buf) {
  const { execSync } = require('child_process');
  const tmpDir = path.join(require('os').tmpdir(), 'pptx-fontfix-' + Date.now());
  const inPath = path.join(tmpDir, 'in.pptx');
  const scriptPath = path.join(tmpDir, 'fixfonts.py');
  fs.mkdirSync(tmpDir, { recursive: true });
  fs.writeFileSync(inPath, buf);
  fs.writeFileSync(scriptPath, `
import zipfile, os, re
inpath = "${inPath.replace(/"/g, '\\"')}"
outpath = inpath.replace('.pptx', '-fixed.pptx')
with zipfile.ZipFile(inpath, 'r') as zin:
    with zipfile.ZipFile(outpath, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename.endswith('.xml'):
                text = data.decode('utf-8', errors='replace')
                if 'typeface=\"Inter\"' in text:
                    text = text.replace('typeface=\"Inter\"', 'typeface=\"Microsoft YaHei\"')
                data = text.encode('utf-8')
            zout.writestr(item, data)
print(outpath)
`);
  const outPath = execSync(`python3 "${scriptPath}"`, { stdio: 'pipe' }).toString().trim();
  const result = fs.readFileSync(outPath);
  fs.rmSync(tmpDir, { recursive: true, force: true });
  return result;
}

// ── Main ─────────────────────────────────────────────────────────────

async function main() {
  // Parse args
  const args = {};
  for (let i = 2; i < process.argv.length; i += 2) {
    const key = process.argv[i].replace(/^--/, '');
    args[key] = process.argv[i + 1];
  }

  const contentPath = args.file || path.join(ROOT, 'yuanfang-html-ppt', 'tests', 'fixtures', 'content-multipage.yaml');
  const themeName = args.theme || 'pitch-deck-vc';
  const outputPath = args.output || '/tmp/poc-deck.pptx';
  const format = (args.format || 'pptx').toLowerCase();

  // 1. Read content (auto-detect .json/.yaml/.yml)
  const content = loadContent(contentPath);
  if (!content) throw new Error(`File not found: ${contentPath}`);

  const slides = content.slides || [{ layout: 'cover', title: content.title, subtitle: content.subtitle, points: content.points }];

  console.log(`📄 Slides: ${slides.length}`);
  console.log(`🎨 Theme:  ${themeName}`);
  console.log(`📦 Format: ${format}`);

  // 2. Load theme CSS
  let themeCss = loadThemeCss(themeName);

  // 2a. Brand color override
  if (args['brand-color']) {
    const color = args['brand-color'];
    const darker = adjustColor(color, -20);
    themeCss += `\n:root{--accent:${color};--accent-dark:${darker};--grad:linear-gradient(135deg,${color},#7C3AED)}`;
    console.log(`🎨 Brand color: ${color}`);
    // Propagate to cover slide for brand tag
    if (slides.length > 0 && !slides[0].brand) {
      slides[0].brand = 'Brand';
    }
  }

  // 3. Generate HTML
  const html = buildHtml(slides, themeName, themeCss);
  // Save HTML alongside output for side-by-side comparison
  const htmlPath = outputPath.replace(/\.(pptx|pdf|png)$/i, '.html');
  fs.writeFileSync(htmlPath, html);
  console.log(`📝 HTML:   ${htmlPath} (${(Buffer.byteLength(html)/1024).toFixed(0)} KB)`);

  // 4. Render based on format
  if (format === 'png') {
    await renderPng(htmlPath, outputPath, slides.length);
  } else if (format === 'pdf') {
    await renderPdf(htmlPath, outputPath, slides.length);
  } else {
    await renderPptx(htmlPath, outputPath, slides, themeName);
  }
}

// Render each slide to a PNG screenshot via Playwright
async function renderPng(htmlPath, outputPath, slideCount) {
  console.log('🚀 Launching Playwright for PNG export...');
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto(`file://${path.resolve(htmlPath)}`, { waitUntil: 'networkidle' });

  const base = outputPath.replace(/\.png$/i, '');
  for (let i = 0; i < slideCount; i++) {
    await page.evaluate((idx) => {
      const slides = document.querySelectorAll('.slide');
      if (slides[idx]) slides[idx].scrollIntoView({ block: 'start' });
    }, i);
    await new Promise(r => setTimeout(r, 200));
    const out = `${base}-${String(i + 1).padStart(2, '0')}.png`;
    await page.screenshot({ path: out, fullPage: false });
    console.log(`  📸 ${out}`);
  }
  await browser.close();
  console.log(`✅ PNGs:   ${base}-*.png (${slideCount} files)`);
}

// Render all slides to a single multi-page PDF via Playwright
async function renderPdf(htmlPath, outputPath, slideCount) {
  console.log('🚀 Launching Playwright for PDF export...');
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto(`file://${path.resolve(htmlPath)}`, { waitUntil: 'networkidle' });
  await page.pdf({
    path: outputPath,
    width: '1920px',
    height: '1080px',
    printBackground: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 },
  });
  await browser.close();
  const size = fs.statSync(outputPath).size;
  console.log(`✅ PDF:    ${outputPath} (${(size/1024).toFixed(0)} KB)`);
}

// Render via Playwright + dom-to-pptx (the original pipeline)
async function renderPptx(htmlPath, outputPath, slides, _themeName) {
  console.log('🚀 Launching Playwright for PPTX export...');
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

  // Load the dom-to-pptx bundle
  await page.goto(`file://${path.resolve(htmlPath)}`, { waitUntil: 'networkidle' });
  await page.addScriptTag({ path: path.join(ROOT, 'node_modules', 'dom-to-pptx', 'dist', 'dom-to-pptx.bundle.js') });

  // Export to PPTX — pass array of <section> elements for multi-slide
  const uint8 = await page.evaluate(async () => {
    const slides = Array.from(document.querySelectorAll('.slide'));
    if (!slides.length) throw new Error('No .slide elements found');
    const blob = await domToPptx.exportToPptx(slides, {
      returnBuffer: true,
      width: 10,
      height: 5.625,
    });
    const ab = await blob.arrayBuffer();
    return Array.from(new Uint8Array(ab));
  });

  await browser.close();

  // Post-process: inject speaker notes into the dom-to-pptx output
  // (dom-to-pptx creates empty notes slides; we fill them from slide.notes)
  const { injectNotes } = require('./notes-injector');
  const notesBySlide = {};
  slides.forEach((slide, i) => {
    if (slide.notes && String(slide.notes).trim()) {
      notesBySlide[String(i + 1)] = String(slide.notes);
    }
  });
  let finalBuffer = await injectNotes(Buffer.from(uint8), notesBySlide);
  finalBuffer = fixPptxFonts(finalBuffer);

  // Save
  fs.writeFileSync(outputPath, finalBuffer);
  const noteCount = Object.keys(notesBySlide).length;
  console.log(`✅ PPTX:   ${outputPath} (${(finalBuffer.length/1024).toFixed(0)} KB${noteCount ? `, ${noteCount} with notes` : ''})`);
}

main().catch(err => {
  console.error('❌', err.message);
  process.exit(1);
});
