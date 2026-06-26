'use strict';

const { addSlideFooter } = require('./slide-footer');
const { ptInch, usableWidth, leftEdge } = require('./units');
const { applyDecorCorners } = require('./decor');
const { applyBackground } = require('./background');

const DEFAULT_DIMS = { w: 13.333, h: 7.5 };

function applyNotes(slide, text) {
  if (typeof text === 'string' && text.trim() !== '' && typeof slide.addNotes === 'function') {
    slide.addNotes(text);
  }
}

function renderCover(pres, slide, theme, dims = DEFAULT_DIMS) {
  const s = pres.addSlide();
  if (!applyBackground(s, slide)) s.background = { color: theme.bg };
  const titleY = dims.h * 0.30;
  const subtitleY = dims.h * 0.50;
  const authorY = dims.h * 0.86;
  const usableW = dims.w - ptInch(theme.spacing) * 2;

  s.addText(slide.title || '', {
    x: ptInch(theme.spacing), y: titleY, w: usableW, h: 1.2,
    fontFace: theme.fontTitle, fontSize: theme.sizeH1,
    color: theme.text, bold: true, align: 'center',
  });

  if (slide.subtitle) {
    s.addText(slide.subtitle, {
      x: ptInch(theme.spacing), y: subtitleY, w: usableW, h: 0.6,
      fontFace: theme.fontBody, fontSize: theme.sizeH2,
      color: theme.textSecondary, align: 'center',
    });
  }

  if (slide.author || slide.date) {
    const authorLine = [slide.author, slide.date].filter(Boolean).join(' · ');
    s.addText(authorLine, {
      x: ptInch(theme.spacing), y: authorY, w: usableW, h: 0.4,
      fontFace: theme.fontBody, fontSize: theme.sizeSm,
      color: theme.textSecondary, align: 'center',
    });
  }

  if (slide.logo) {
    const logoSize = 0.55;
    s.addImage({
      path: slide.logo,
      x: dims.w - theme.spacing - logoSize,
      y: ptInch(theme.spacing),
      w: logoSize, h: logoSize,
    });
  }

  if (theme.seal && theme.seal !== '""' && theme.seal !== 'none' && theme.seal !== '') {
    const sealText = theme.seal.replace(/^["']|["']$/g, '');
    if (sealText) {
      const sealSize = 0.8;
      s.addShape('ellipse', {
        x: ptInch(theme.spacing), y: ptInch(theme.spacing), w: sealSize, h: sealSize,
        fill: { color: theme.accent },
        line: { color: theme.accent, width: 0 },
      });
      s.addText(sealText, {
        x: ptInch(theme.spacing), y: ptInch(theme.spacing), w: sealSize, h: sealSize,
        fontFace: theme.fontTitle, fontSize: 28, bold: true,
        color: theme.bg, align: 'center', valign: 'middle',
      });
    }
  }

  applyNotes(s, slide.notes);
  addSlideFooter(s, theme, dims, slide);
  applyDecorCorners(s, theme, dims);
  return s;
}

function renderContent(pres, slide, theme, dims = DEFAULT_DIMS) {
  const s = pres.addSlide();
  if (!applyBackground(s, slide)) s.background = { color: theme.bg };
  const usableW = dims.w - ptInch(theme.spacing) * 2;
  const titleY = ptInch(theme.spacing);
  const bodyY = dims.h * 0.22;
  const bodyH = dims.h * 0.70;

  s.addText(slide.title || '', {
    x: ptInch(theme.spacing), y: titleY, w: usableW, h: 0.8,
    fontFace: theme.fontTitle, fontSize: theme.sizeH2,
    color: theme.text, bold: true, align: 'left',
  });

  const body = (slide.points || (slide.body ? [slide.body] : [])).join('\n');
  s.addText(body, {
    x: ptInch(theme.spacing), y: bodyY, w: usableW, h: bodyH,
    fontFace: theme.fontBody, fontSize: theme.sizeBase,
      color: theme.text, valign: 'top', paraSpaceAfter: theme.space1,
    bullet: slide.points ? { code: '25CF' } : false,
  });

  applyNotes(s, slide.notes);
  addSlideFooter(s, theme, dims, slide);
  return s;
}

function renderSummary(pres, slide, theme, dims = DEFAULT_DIMS) {
  const s = pres.addSlide();
  if (!applyBackground(s, slide)) s.background = { color: theme.bg };
  const usableW = dims.w - ptInch(theme.spacing) * 2;
  const closing = slide.closing || '谢谢 · Thank You';

  s.addText(slide.title || '', {
    x: ptInch(theme.spacing), y: ptInch(theme.spacing), w: usableW, h: 0.8,
    fontFace: theme.fontTitle, fontSize: theme.sizeH2,
    color: theme.text, bold: true, align: 'left',
  });

  const body = (slide.points || []).join('\n');
  if (body) {
    s.addText(body, {
      x: ptInch(theme.spacing), y: dims.h * 0.22, w: usableW, h: dims.h * 0.50,
      fontFace: theme.fontBody, fontSize: theme.sizeBase,
      color: theme.text, valign: 'top', paraSpaceAfter: theme.space1,
      bullet: { code: '25CF' },
    });
  }

  s.addText(closing, {
    x: ptInch(theme.spacing), y: dims.h * 0.80, w: usableW, h: 0.6,
    fontFace: theme.fontTitle, fontSize: theme.sizeH1,
    color: theme.accent, bold: true, align: 'center',
  });

  applyNotes(s, slide.notes);
  addSlideFooter(s, theme, dims, slide);
  return s;
}

module.exports = { renderCover, renderContent, renderSummary, DEFAULT_DIMS, applyNotes };
