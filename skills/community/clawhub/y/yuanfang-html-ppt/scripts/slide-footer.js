'use strict';

function addSlideFooter(slide, theme, dims, opts = {}) {
  if (opts.showFooter === false) return;

  const marginIn = 0.15;
  const widthIn = 1.2;
  const heightIn = 0.3;
  const x = dims.w - marginIn - widthIn;
  const y = dims.h - marginIn - heightIn;

  if (typeof slide.addText === 'function') {
    slide.addText(String(slide._slideNum || ''), {
      x, y, w: widthIn, h: heightIn,
      fontFace: theme.fontBody,
      fontSize: 9,
      color: theme.secondary,
      align: 'right',
    });
  }
}

module.exports = { addSlideFooter };
