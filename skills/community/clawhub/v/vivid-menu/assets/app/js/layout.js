/* ============================================================
 * layout.js — 排版计算
 * 输入菜单数据，输出一份带绝对坐标的绘图指令表（blocks）。
 * 这一层只算不动手画，渲染层照着 coordinates 画就行。
 * ============================================================ */

import { PAPER, SZ, FS, themeOf } from './model.js';
import { wrapText, wrapClamp, measureText } from './measure.js';

/**
 * @typedef {{type:string}} Block
 * @returns {{width:number, height:number, blocks:Block[], theme:object}}
 */
export function layoutMenu(menu) {
  const theme = themeOf(menu);
  const W = PAPER.width;
  const mx = PAPER.marginX;
  const contentW = W - mx * 2;
  const cx = W / 2;
  const blocks = [];
  let y = PAPER.padTop;

  /* ---------- 页眉 ---------- */
  blocks.push({ type: 'rule', y, x1: cx - 44, x2: cx + 44, sw: 1.2, op: 0.45 });
  y += 32;

  const nameStr = (menu.name || '未命名小馆').trim();
  const nameLines = wrapText(nameStr, contentW - 40, FS.shopName).slice(0, 2);
  const nameLH = FS.shopName * 1.14;
  blocks.push({
    type: 'lines', lines: nameLines, x: cx, y,
    size: FS.shopName, weight: 700, align: 'middle', lh: nameLH, tracking: 2, color: 'ink',
  });
  y += nameLines.length * nameLH;

  if (menu.name_original) {
    blocks.push({
      type: 'text', text: menu.name_original, x: cx, y: y + 8,
      size: FS.shopNameAlt, align: 'middle', tracking: 3.2, op: 0.6, italic: true,
    });
    y += 30;
  }
  if (menu.subtitle) {
    blocks.push({
      type: 'text', text: menu.subtitle, x: cx, y: y + 10,
      size: 12.5, align: 'middle', tracking: 4, op: 0.5,
    });
    y += 30;
  }

  y += 12;
  blocks.push({ type: 'rule', y, x1: mx, x2: mx + contentW, sw: 1.5, op: 0.7 });
  blocks.push({ type: 'rule', y: y + 3.5, x1: mx, x2: mx + contentW, sw: 0.7, op: 0.35 });
  y += 34;

  /* ---------- 菜品 ---------- */
  let lastSection = null;
  let sigDrawn = false;
  const dishes = menu.dishes || [];
  const rows = [];

  for (const dish of dishes) {
    const yStart = y;
    const hasSection = dish.section && dish.section.trim();
    if (hasSection && dish.section !== lastSection) {
      if (y > PAPER.padTop + 60) y += SZ.sectionGap;
      blocks.push({
        type: 'section', title: dish.section.trim(), x: mx, y,
        right: mx + contentW, size: FS.sectionTitle,
      });
      y += 40;
      lastSection = dish.section;
    }

    if (dish.signature && !sigDrawn) {
      y += SZ.signatureGap;
      const b = layoutSignature(dish, cx, y, contentW, theme);
      blocks.push(...b.blocks);
      y += b.height;
      y += SZ.signatureGap;
      sigDrawn = true;
    } else {
      const b = layoutRow(dish, mx, y, contentW, theme);
      blocks.push(...b.blocks);
      y += b.height + SZ.rowGap;
    }
    rows.push({ dishId: dish.id, y1: yStart, y2: y });
  }

  if (!dishes.length) {
    y += 60;
    blocks.push({
      type: 'text', text: '暂无菜品', x: cx, y, size: 15,
      align: 'middle', op: 0.35, tracking: 3,
    });
    y += 40;
  }

  /* ---------- 页脚 ---------- */
  y += 12;
  blocks.push({ type: 'rule', y, x1: cx - 26, x2: cx + 26, sw: 1, op: 0.4 });
  y += 26;

  if (menu.footer) {
    const lines = wrapClamp(menu.footer, contentW - 120, FS.footer, 2);
    blocks.push({
      type: 'lines', lines: lines.lines, x: cx, y,
      size: FS.footer, align: 'middle', lh: FS.footer * 1.7, op: 0.5, tracking: 1.2,
    });
    y += lines.lines.length * FS.footer * 1.7;
  }

  if (menu.seal) {
    // 印章放在页脚右下，红底白字
    const sealSize = 44;
    blocks.push({
      type: 'seal', text: menu.seal.slice(0, 4), x: mx + contentW - sealSize,
      y: y + 6, size: sealSize,
    });
    y += sealSize * 0.6;
  }

  const height = Math.max(y + PAPER.padBottom, 680);
  return { width: W, height, blocks, rows, theme, menu };
}

/* ---------------- 普通菜行 ---------------- */

function layoutRow(dish, x, y, contentW, theme) {
  const artSize = SZ.artNormal;
  const textX = x + artSize + SZ.artTextGap;
  const priceRight = x + contentW;
  const textW = contentW - artSize - SZ.artTextGap - SZ.priceW;

  const nameLines = wrapText(dish.name || '未命名', textW, FS.dishName).slice(0, 2);
  const blurb = wrapClamp(dish.blurb || '', textW, FS.blurb, 2);
  const tagsStr = (dish.tags || []).filter(Boolean).join(' · ');

  let textH = nameLines.length * FS.dishName * 1.24;
  if (blurb.lines.length) textH += 5 + blurb.lines.length * FS.blurb * 1.55;
  if (tagsStr) textH += 5 + FS.tags * 1.4;

  const rowH = Math.max(artSize, textH);
  const blocks = [];
  const artTop = y + (rowH - artSize) / 2;
  const textTop = y + (rowH - textH) / 2;

  blocks.push({ type: 'art', x, y: artTop, size: artSize, dish });

  let ty = textTop + FS.dishName * 1.02;
  blocks.push({
    type: 'lines', lines: nameLines, x: textX, y: ty,
    size: FS.dishName, weight: 600, align: 'start', lh: FS.dishName * 1.24,
    tracking: 0.6, color: dish.signature ? 'accent' : 'ink',
  });
  ty += nameLines.length * FS.dishName * 1.24;

  if (blurb.lines.length) {
    ty += 5 + FS.blurb * 0.9;
    blocks.push({
      type: 'lines', lines: blurb.lines, x: textX, y: ty,
      size: FS.blurb, align: 'start', lh: FS.blurb * 1.55, op: 0.62,
    });
    ty += blurb.lines.length * FS.blurb * 1.55;
  }

  if (tagsStr) {
    ty += 5 + FS.tags * 0.95;
    blocks.push({
      type: 'text', text: tagsStr, x: textX, y: ty,
      size: FS.tags, align: 'start', op: 0.5, tracking: 1,
    });
  }

  if (dish.price) {
    blocks.push({
      type: 'price', text: dish.price, x: priceRight, y: y + rowH / 2 + FS.price * 0.35,
      size: FS.price, align: 'end', weight: 500,
    });
  }

  if (dish.signature) {
    // 非首位的招牌菜加一个小标记
    blocks.push({
      type: 'mark', x: priceRight, y: y + rowH / 2 - FS.price * 0.9,
      text: '招牌', size: 9.5,
    });
  }

  return { blocks, height: rowH };
}

/* ---------------- 招牌大卡 ---------------- */

function layoutSignature(dish, cx, y, contentW, theme) {
  const blocks = [];
  const artSize = SZ.artSignature;
  const startY = y;

  blocks.push({
    // 招牌依据（signature_note）是给人和 Agent 核对的信息，不印在纸面上
    type: 'badge', text: '招牌',
    x: cx, y, size: 10.5,
  });
  y += 28;

  const nameLines = wrapText(dish.name || '招牌菜', contentW - 80, FS.dishNameSig).slice(0, 2);
  const lh = FS.dishNameSig * 1.18;
  blocks.push({
    type: 'lines', lines: nameLines, x: cx, y: y + FS.dishNameSig * 0.9,
    size: FS.dishNameSig, weight: 700, align: 'middle', lh, tracking: 3, color: 'accent',
  });
  y += nameLines.length * lh + 10;

  // 淡圆底 + 细圆环，把大图托住
  blocks.push({ type: 'halo', cx, cy: y + artSize / 2, r: Math.round(artSize * 0.44) });
  blocks.push({ type: 'art', x: cx - artSize / 2, y, size: artSize, dish });
  y += artSize + 16;

  if (dish.blurb) {
    const blurb = wrapClamp(dish.blurb, contentW - 160, 14.5, 2);
    blocks.push({
      type: 'lines', lines: blurb.lines, x: cx, y,
      size: 14.5, align: 'middle', lh: 14.5 * 1.7, op: 0.66,
    });
    y += blurb.lines.length * 14.5 * 1.7;
    y += 8;
  }

  if (dish.price) {
    blocks.push({
      type: 'price', text: dish.price, x: cx, y: y + 12,
      size: FS.priceSig, align: 'middle', weight: 500,
    });
    y += 30;
  }

  return { blocks, height: y - startY };
}
