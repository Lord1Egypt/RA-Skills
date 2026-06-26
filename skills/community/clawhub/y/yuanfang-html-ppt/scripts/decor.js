'use strict';

const { ptInch } = require('./units');

function parseColorValue(value, fallback) {
  if (typeof value !== 'string') return fallback;
  const v = value.trim();
  if (v === 'none' || v === '' || v === 'block' || v === 'flex' || v === 'inherit' || v === 'initial') return null;
  if (v.startsWith('#')) return v;
  if (v.startsWith('rgb')) {
    const m = v.match(/rgba?\(([^)]+)\)/);
    if (m) {
      const parts = m[1].split(',').map(s => parseInt(s.trim(), 10));
      if (parts.length >= 3) {
        const r = parts[0].toString(16).padStart(2, '0');
        const g = parts[1].toString(16).padStart(2, '0');
        const b = parts[2].toString(16).padStart(2, '0');
        return `#${r}${g}${b}`.toUpperCase();
      }
    }
  }
  if (v.startsWith('linear-gradient') || v.startsWith('radial-gradient')) {
    return fallback;
  }
  return v;
}

function applyDecorCorners(slide, theme, dims) {
  if (typeof slide.addShape !== 'function') return;
  const cornerSize = 0.5;
  const margin = ptInch(theme.space4 || 48);

  const corners = [
    { token: theme.decorTL, x: 0, y: 0 },
    { token: theme.decorTR, x: dims.w - cornerSize, y: 0 },
    { token: theme.decorBL, x: 0, y: dims.h - cornerSize },
    { token: theme.decorBR, x: dims.w - cornerSize, y: dims.h - cornerSize },
  ];

  for (const c of corners) {
    const color = parseColorValue(c.token, theme.accent);
    if (color) {
      slide.addShape('rect', {
        x: c.x, y: c.y, w: cornerSize, h: cornerSize,
        fill: { color },
        line: { color, width: 0 },
      });
    }
  }
  void margin;
}

module.exports = { applyDecorCorners, parseColorValue };
