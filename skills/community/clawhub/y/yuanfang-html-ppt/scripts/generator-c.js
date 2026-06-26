'use strict';

const { addSlideFooter } = require('./slide-footer');
const { ptInch } = require('./units');
const { applyBackground } = require('./background');

const DEFAULT_DIMS = { w: 13.333, h: 7.5 };

function applyNotes(slide, text) {
  if (typeof text === 'string' && text.trim() !== '' && typeof slide.addNotes === 'function') {
    slide.addNotes(text);
  }
}

function metricCardHtml(m) {
  const esc = (s) => String(s || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
  return `<div class="metric-card"><div class="metric-label">${esc(m.label)}</div><div class="metric-value">${esc(m.value)}</div><div class="metric-change">${esc(m.change)}</div></div>`;
}

function cssShadowToProps(shadowStr) {
  if (!shadowStr || shadowStr === 'none' || shadowStr === '') return undefined;
  const m = shadowStr.match(/(-?\d+)px\s+(-?\d+)px\s+(-?\d+)px\s+rgba?\(([^)]+)\)/);
  if (!m) return undefined;
  const offsetY = parseInt(m[2], 10);
  const blur = Math.max(0, parseInt(m[3], 10));
  const rgba = m[4].split(',').map(s => parseFloat(s.trim()));
  const r = Math.round(rgba[0] || 0);
  const g = Math.round(rgba[1] || 0);
  const b = Math.round(rgba[2] || 0);
  const alpha = rgba[3] !== undefined ? rgba[3] : 1;
  const color = `${[r, g, b].map(n => n.toString(16).padStart(2, '0')).join('').toUpperCase()}`;
  return {
    type: 'outer',
    color,
    opacity: Math.round(alpha * 100) / 100,
    blur: Math.min(100, blur / 4),
    angle: 90,
    offset: Math.min(200, Math.abs(offsetY) / 4),
  };
}

function applyFeatureFlags(slide, theme, dims) {
  if (theme.accentLine && theme.accentLine !== 'none' && theme.accentLine !== '') {
    slide.addShape('rect', {
      x: 0, y: 0, w: dims.w, h: 0.05,
      fill: { color: theme.accent },
      line: { color: theme.accent, width: 0 },
    });
  }
  if (theme.accentBlock && theme.accentBlock !== 'none' && theme.accentBlock !== '') {
    slide.addShape('rect', {
      x: dims.w * 0.85, y: 0, w: dims.w * 0.15, h: dims.h,
      fill: { color: theme.accent },
      line: { color: theme.accent, width: 0 },
    });
  }
  if (theme.terminalBar && theme.terminalBar !== 'none' && theme.terminalBar !== '') {
    const barH = 0.4;
    const dotR = 0.12;
    const dotY = barH / 2;
    slide.addShape('rect', {
      x: 0, y: 0, w: dims.w, h: barH,
      fill: { color: theme.secondary },
      line: { color: theme.secondary, width: 0 },
    });
    for (let i = 0; i < 3; i++) {
      const colors = ['#FF5F56', '#FFBD2E', '#27C93F'];
      slide.addShape('ellipse', {
        x: 0.2 + i * (dotR * 2 + 0.1), y: dotY - dotR, w: dotR * 2, h: dotR * 2,
        fill: { color: colors[i] },
        line: { color: colors[i], width: 0 },
      });
    }
  }
}

function buildSection(pres, slide, theme, dims = DEFAULT_DIMS) {
  const s = pres.addSlide();
  if (!applyBackground(s, slide)) s.background = { color: theme.bg };
  const usableW = dims.w - ptInch(theme.spacing) * 2;
  s.addText(slide.title || '', {
    x: ptInch(theme.spacing), y: dims.h * 0.32, w: usableW, h: 1.5,
    fontFace: theme.fontTitle, fontSize: theme.sizeH1,
    color: theme.accent, bold: true, align: 'center', opacity: 0.5,
  });
  s.addText(slide.title || '', {
    x: ptInch(theme.spacing), y: dims.h * 0.50, w: usableW, h: 0.8,
    fontFace: theme.fontTitle, fontSize: theme.sizeH1,
    color: theme.text, bold: true, align: 'center',
  });
  s.addShape('line', {
    x: dims.w * 0.40, y: dims.h * 0.68, w: dims.w * 0.20, h: 0,
    line: { color: theme.accent, width: 4 },
  });
  applyFeatureFlags(s, theme, dims);
  applyNotes(s, slide.notes);
  addSlideFooter(s, theme, dims, slide);
  return s;
}

function buildTwoColumn(pres, slide, theme, dims = DEFAULT_DIMS) {
  const s = pres.addSlide();
  if (!applyBackground(s, slide)) s.background = { color: theme.bg };
  const usableW = dims.w - ptInch(theme.spacing) * 2;
  s.addText(slide.title || '', {
    x: ptInch(theme.spacing), y: ptInch(theme.spacing), w: usableW, h: 0.8,
    fontFace: theme.fontTitle, fontSize: theme.sizeH2,
    color: theme.text, bold: true,
  });
  const colGap = ptInch(theme.space3);
  const colW = (dims.w - ptInch(theme.spacing) * 2 - colGap) / 2;
  const colY = dims.h * 0.22;
  const colH = dims.h * 0.70;
  const cardPad = ptInch(theme.space3);
  s.addShape('roundRect', {
    x: ptInch(theme.spacing), y: colY, w: colW, h: colH,
    fill: { color: theme.bgAlt },
    line: { color: theme.bgAlt, width: 0 },
    rectRadius: theme.rectRadius,
    shadow: cssShadowToProps(theme.shadow) || undefined,
  });
  s.addText(slide.leftTitle || '', {
    x: ptInch(theme.spacing) + cardPad, y: colY + cardPad, w: colW - cardPad * 2, h: 0.6,
    fontFace: theme.fontTitle, fontSize: theme.sizeH3,
    color: theme.accent, bold: true,
  });
  const leftBody = (slide.leftPoints || []).map(p => '• ' + p).join('\n');
  if (leftBody) {
    s.addText(leftBody, {
      x: ptInch(theme.spacing) + cardPad, y: colY + 1.1, w: colW - cardPad * 2, h: colH - 1.4,
      fontFace: theme.fontBody, fontSize: theme.sizeBase,
      color: theme.text, valign: 'top', paraSpaceAfter: theme.space1,
    });
  }
  s.addShape('roundRect', {
    x: ptInch(theme.spacing) + colW + colGap, y: colY, w: colW, h: colH,
    fill: { color: theme.bgAlt },
    line: { color: theme.bgAlt, width: 0 },
    rectRadius: theme.rectRadius,
    shadow: cssShadowToProps(theme.shadow) || undefined,
  });
  s.addText(slide.rightTitle || '', {
    x: ptInch(theme.spacing) + colW + colGap + cardPad, y: colY + cardPad, w: colW - cardPad * 2, h: 0.6,
    fontFace: theme.fontTitle, fontSize: theme.sizeH3,
    color: theme.accent, bold: true,
  });
  const rightBody = (slide.rightPoints || []).map(p => '• ' + p).join('\n');
  if (rightBody) {
    s.addText(rightBody, {
      x: ptInch(theme.spacing) + colW + colGap + cardPad, y: colY + 1.1, w: colW - cardPad * 2, h: colH - 1.4,
      fontFace: theme.fontBody, fontSize: theme.sizeBase,
      color: theme.text, valign: 'top', paraSpaceAfter: 8,
    });
  }
  applyFeatureFlags(s, theme, dims);
  applyNotes(s, slide.notes);
  addSlideFooter(s, theme, dims, slide);
  return s;
}

function buildData(pres, slide, theme, dims = DEFAULT_DIMS) {
  const s = pres.addSlide();
  if (!applyBackground(s, slide)) s.background = { color: theme.bg };
  const usableW = dims.w - ptInch(theme.spacing) * 2;
  s.addText(slide.title || '', {
    x: ptInch(theme.spacing), y: ptInch(theme.spacing), w: usableW, h: 0.8,
    fontFace: theme.fontTitle, fontSize: theme.sizeH2,
    color: theme.text, bold: true,
  });
  const metrics = slide.metrics || [];
  if (metrics.length === 0) return s;
  const cols = Math.min(3, metrics.length);
  const interCardGap = ptInch(theme.space3);
  const cardW = (dims.w - ptInch(theme.spacing) * 2 - interCardGap * (cols - 1)) / cols;
  const cardH = dims.h * 0.32;
  const cardY = dims.h * 0.22;
  const cardPad = ptInch(theme.space1);
  metrics.forEach((m, i) => {
    const col = i % cols;
    const row = Math.floor(i / cols);
    const x = ptInch(theme.spacing) + col * (cardW + interCardGap);
    const y = cardY + row * (cardH + ptInch(theme.spacing));
    s.addShape('roundRect', {
      x, y, w: cardW, h: cardH,
      fill: { color: theme.bgAlt },
      line: { color: theme.bgAlt, width: 0 },
      rectRadius: theme.rectRadius,
      shadow: cssShadowToProps(theme.shadow) || undefined,
    });
    s.addText(m.label || '', {
      x: x + cardPad, y: y + cardPad, w: cardW - cardPad * 2, h: 0.4,
      fontFace: theme.fontBody, fontSize: theme.sizeSm,
      color: theme.secondary, align: 'center',
    });
    s.addText(m.value || '', {
      x: x + cardPad, y: y + 0.6, w: cardW - cardPad * 2, h: cardH * 0.45,
      fontFace: theme.fontTitle, fontSize: theme.sizeH1,
      color: theme.text, bold: true, align: 'center',
    });
    s.addText(m.change || '', {
      x: x + cardPad, y: y + cardH - 0.55, w: cardW - cardPad * 2, h: 0.4,
      fontFace: theme.fontBody, fontSize: theme.sizeSm,
      color: theme.accent, bold: true, align: 'center',
    });
  });
  applyFeatureFlags(s, theme, dims);
  applyNotes(s, slide.notes);
  addSlideFooter(s, theme, dims, slide);
  return s;
}

function buildQuote(pres, slide, theme, dims = DEFAULT_DIMS) {
  const s = pres.addSlide();
  if (!applyBackground(s, slide)) s.background = { color: theme.bg };
  s.addText('"', {
    x: 0, y: dims.h * 0.18, w: dims.w, h: dims.h * 0.30,
    fontFace: theme.fontTitle, fontSize: 200,
    color: theme.accent, align: 'center', valign: 'middle', opacity: 0.3,
  });
  s.addText(slide.quote || '', {
    x: dims.w * 0.15, y: dims.h * 0.40, w: dims.w * 0.70, h: dims.h * 0.30,
    fontFace: theme.fontBody, fontSize: theme.sizeH2,
    color: theme.text, italic: true, align: 'center', valign: 'middle',
  });
  s.addText('— ' + (slide.attribution || ''), {
    x: dims.w * 0.15, y: dims.h * 0.72, w: dims.w * 0.70, h: 0.5,
    fontFace: theme.fontBody, fontSize: theme.sizeSm,
    color: theme.secondary, align: 'center',
  });
  applyFeatureFlags(s, theme, dims);
  applyNotes(s, slide.notes);
  addSlideFooter(s, theme, dims, slide);
  return s;
}

async function renderSection(pres, slide, theme, dims = DEFAULT_DIMS) {
  return buildSection(pres, slide, theme, dims);
}
async function renderTwoColumn(pres, slide, theme, dims = DEFAULT_DIMS) {
  return buildTwoColumn(pres, slide, theme, dims);
}
async function renderData(pres, slide, theme, dims = DEFAULT_DIMS) {
  return buildData(pres, slide, theme, dims);
}
async function renderQuote(pres, slide, theme, dims = DEFAULT_DIMS) {
  return buildQuote(pres, slide, theme, dims);
}

module.exports = {
  renderSection, renderTwoColumn, renderData, renderQuote,
  buildSection, buildTwoColumn, buildData, buildQuote,
  applyFeatureFlags, applyNotes, metricCardHtml, DEFAULT_DIMS,
};
