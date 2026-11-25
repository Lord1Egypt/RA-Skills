/* ============================================================
 * render.js — SVG 渲染
 * 拿着 layout 给出的坐标表逐条绘制。没有布局逻辑在这里。
 * ============================================================ */

import { layoutMenu } from './layout.js';
import { measureText } from './measure.js';
import { buildArt } from './art/index.js';

const FONT_SERIF = "'Noto Serif SC','Source Han Serif SC','Songti SC','SimSun',Georgia,serif";
const FONT_SANS = "'PingFang SC','Microsoft YaHei','Hiragino Sans GB',system-ui,sans-serif";

const esc = (s) => String(s ?? '')
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;');

const anchor = (a) => (a === 'middle' ? 'middle' : a === 'end' ? 'end' : 'start');
const colorOf = (c, t) => (c === 'accent' ? t.accent : t.ink);

/**
 * 渲染整张菜单
 * @param {object} menu
 * @param {{bare?:boolean}} opt bare=true 时不加纸张底色（用于嵌入预览）
 */
export function renderMenu(menu, opt = {}) {
  const L = layoutMenu(menu);
  const t = L.theme;
  const W = L.width;
  const H = L.height;

  const parts = [];
  parts.push(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" class="menu-svg" font-family="${FONT_SERIF}">`);

  // 纸张
  parts.push(`<rect x="0" y="0" width="${W}" height="${H}" fill="${t.paper}"/>`);
  // 内侧细边框
  parts.push(`<rect x="20" y="20" width="${W - 40}" height="${H - 40}" fill="none" stroke="${t.edge}" stroke-width="1" opacity="0.85"/>`);

  for (const b of L.blocks) parts.push(renderBlock(b, t, W));

  // 菜品点击热区（导出时剔除）
  if (opt.hitAreas !== false) {
    for (const r of L.rows || []) {
      const h = Math.max(1, r.y2 - r.y1);
      parts.push(
        `<rect class="vm-hit" data-dish="${r.dishId}" x="0" y="${r.y1}" width="${W}" height="${h}" fill="#000000" fill-opacity="0" pointer-events="all"/>`,
      );
    }
  }

  parts.push('</svg>');
  return { svg: parts.join(''), layout: L };
}

function renderBlock(b, t, W) {
  switch (b.type) {
    /* ---- 分隔线 ---- */
    case 'rule':
      return `<line x1="${b.x1}" y1="${b.y}" x2="${b.x2}" y2="${b.y}" stroke="${t.ink}" stroke-width="${b.sw || 1}" opacity="${b.op ?? 0.6}" stroke-linecap="round"/>`;

    /* ---- 单行文字 ---- */
    case 'text':
      return textEl(b, t);

    /* ---- 多行文字 ---- */
    case 'lines': {
      const lh = b.lh || b.size * 1.4;
      return b.lines.map((ln, i) =>
        textEl({ ...b, text: ln, y: b.y + i * lh }, t),
      ).join('');
    }

    /* ---- 招牌图的托底：淡圆 + 细环 ---- */
    case 'halo':
      return [
        `<circle cx="${b.cx}" cy="${b.cy}" r="${b.r}" fill="${t.ink}" opacity="0.035"/>`,
        `<circle cx="${b.cx}" cy="${b.cy}" r="${b.r}" fill="none" stroke="${t.accent}" stroke-width="0.8" opacity="0.28"/>`,
      ].join('');

    /* ---- 插图 ---- */
    case 'art': {
      const art = buildArt(b.dish, t);
      const inner = art.replace(/^<svg[^>]*>/, '').replace(/<\/svg>$/, '');
      return `<svg x="${b.x}" y="${b.y}" width="${b.size}" height="${b.size}" viewBox="0 0 100 100">${inner}</svg>`;
    }

    /* ---- 价格 ---- */
    case 'price':
      return textEl({ ...b, align: 'middle' === b.align ? 'middle' : 'end' }, t, true);

    /* ---- 招牌标签（圆角胶囊） ---- */
    case 'badge': {
      const w = measureText(b.text, b.size) + b.text.length * 2.4 + 26;
      const h = 22;
      const x = b.x - w / 2;
      return [
        `<rect x="${x}" y="${b.y}" width="${w}" height="${h}" rx="${h / 2}" fill="none" stroke="${t.accent}" stroke-width="1" opacity="0.8"/>`,
        `<text x="${b.x}" y="${b.y + 15}" font-size="${b.size}" fill="${t.accent}" text-anchor="middle" letter-spacing="1.6" font-family="${FONT_SANS}">${esc(b.text)}</text>`,
      ].join('');
    }

    /* ---- 分节标题 ---- */
    case 'section': {
      const tw = measureText(b.title, b.size) + b.title.length * 1.6;
      const lineStart = b.x + tw + 18;
      return [
        `<text x="${b.x}" y="${b.y + b.size}" font-size="${b.size}" font-weight="600" fill="${t.ink}" letter-spacing="2.4">${esc(b.title)}</text>`,
        `<line x1="${lineStart}" y1="${b.y + b.size - 6}" x2="${b.right}" y2="${b.y + b.size - 6}" stroke="${t.ink}" stroke-width="0.8" opacity="0.28"/>`,
      ].join('');
    }

    /* ---- 印章 ---- */
    case 'seal': {
      const s = b.size;
      const chars = [...b.text];
      const cols = chars.length >= 3 ? 2 : 1;
      const rows = Math.ceil(chars.length / cols);
      const fs = Math.min(s / (cols + 0.4), s / (rows + 0.3));
      let out = `<rect x="${b.x}" y="${b.y}" width="${s}" height="${s}" rx="3" fill="${t.accent}" opacity="0.92"/>`;
      chars.forEach((ch, i) => {
        const c = i % cols;
        const r = Math.floor(i / cols);
        out += `<text x="${b.x + (c + 0.5) * (s / cols)}" y="${b.y + (r + 0.5) * (s / rows) + fs * 0.36}" font-size="${fs}" fill="${t.paper}" text-anchor="middle" font-weight="700" letter-spacing="0">${esc(ch)}</text>`;
      });
      return out;
    }

    /* ---- 招牌小标记 ---- */
    case 'mark':
      return `<text x="${b.x}" y="${b.y}" font-size="${b.size}" fill="${t.accent}" text-anchor="end" letter-spacing="1.2" font-family="${FONT_SANS}" opacity="0.9">${esc(b.text)}</text>`;

    default:
      return '';
  }
}

function textEl(b, t, mono) {
  const weight = b.weight ? ` font-weight="${b.weight}"` : '';
  const style = b.italic ? ' font-style="italic"' : '';
  const tracking = b.tracking ? ` letter-spacing="${b.tracking}"` : '';
  const op = b.op !== undefined ? ` opacity="${b.op}"` : '';
  const fill = colorOf(b.color, t);
  const fam = mono ? FONT_SANS : FONT_SERIF;
  return `<text x="${b.x}" y="${b.y}" font-size="${b.size}"${weight}${style}${tracking}${op} fill="${fill}" text-anchor="${anchor(b.align)}" font-family="${fam}">${esc(b.text)}</text>`;
}

/** 导出为可独立打开的 SVG 文件内容 */
export function exportSvg(menu) {
  return renderMenu(menu).svg;
}
