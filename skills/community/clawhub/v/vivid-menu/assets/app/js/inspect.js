/* ============================================================
 * inspect.js — 自动质检
 * 把「看起来对不对」翻译成可计算的检查：包围盒、元素数、
 * 行数、对比度、色距、重复度。返回 error / warn 两级问题。
 * ============================================================ */

import { layoutMenu } from './layout.js';
import { PAPER, SZ, FS, themeOf } from './model.js';
import { wrapText, measureText } from './measure.js';
import { artInner, buildArt, applyTokens } from './art/index.js';

/* ---------------- 颜色工具 ---------------- */

function hexToRgb(hex) {
  const h = String(hex).replace('#', '');
  const v = h.length === 3 ? h.split('').map((c) => c + c).join('') : h;
  return [parseInt(v.slice(0, 2), 16), parseInt(v.slice(2, 4), 16), parseInt(v.slice(4, 6), 16)];
}

function luminance(hex) {
  const [r, g, b] = hexToRgb(hex).map((c) => {
    const s = c / 255;
    return s <= 0.03928 ? s / 12.92 : ((s + 0.055) / 1.055) ** 2.4;
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

/** WCAG 对比度 */
export function contrastRatio(a, b) {
  const l1 = luminance(a), l2 = luminance(b);
  const [hi, lo] = l1 > l2 ? [l1, l2] : [l2, l1];
  return (hi + 0.05) / (lo + 0.05);
}

/** 色差（RGB 欧氏距离，0-441） */
export function colorDistance(a, b) {
  const [r1, g1, b1] = hexToRgb(a);
  const [r2, g2, b2] = hexToRgb(b);
  return Math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2);
}

/* ---------------- 插图结构统计 ---------------- */

const SHAPE_RE = /<(path|line|circle|ellipse|rect|polygon|polyline)\b/g;

function artStats(dish, theme) {
  const inner = dish.art && dish.art.trim()
    ? buildArt(dish, theme).replace(/^<svg[^>]*>/, '').replace(/<\/svg>$/, '')
    : applyTokens(artInner(dish.kind || 'generic', dish._seed || dish.name || dish.id || 'x'), theme);
  const shapes = (inner.match(SHAPE_RE) || []).length;
  // 笔画密度：路径指令数量，粗略代表"画得细不细"
  const cmds = (inner.match(/[MLQCSTAZmlqcstaz]/g) || []).length;
  return { shapes, cmds, bytes: inner.length };
}

/* ---------------- 主检查 ---------------- */

export function inspectMenu(menu) {
  const issues = [];
  const theme = themeOf(menu);
  const dishes = menu.dishes || [];
  const add = (level, code, msg, extra = {}) => issues.push({ level, code, msg, ...extra });

  /* ===== 数据层 ===== */

  if (!dishes.length) {
    add('warn', 'empty', '菜单还没有任何菜品');
  }

  const nameCount = new Map();
  const seenIds = new Set();

  for (const d of dishes) {
    const name = (d.name || '').trim();
    if (!name) {
      add('error', 'no-name', '有一道菜没有菜名', { dishId: d.id });
    } else {
      nameCount.set(name, (nameCount.get(name) || 0) + 1);
    }
    if (seenIds.has(d.id)) add('error', 'dup-id', `菜品 id 重复：${d.id}`, { dishId: d.id });
    seenIds.add(d.id);

    if (!String(d.price || '').trim()) {
      add('warn', 'no-price', `「${name || '未命名'}」没有标价`, { dishId: d.id });
    }
    if (d.signature && !String(d.signature_note || '').trim()) {
      add('warn', 'sig-no-evidence', `招牌菜「${name}」缺少判断依据（signature_note）`, { dishId: d.id });
    }
    if (!String(d.blurb || '').trim()) {
      add('warn', 'no-blurb', `「${name || '未命名'}」没有一句话说明`, { dishId: d.id });
    }
  }

  for (const [k, v] of nameCount) {
    if (v > 1) add('error', 'dup-name', `菜名「${k}」重复了 ${v} 次`, { name: k });
  }

  // 价格符号一致性
  const priced = dishes.filter((d) => String(d.price || '').trim());
  if (priced.length > 1) {
    const withSym = priced.filter((d) => /^[¥￥$]/.test(String(d.price).trim())).length;
    if (withSym > 0 && withSym < priced.length) {
      add('warn', 'price-format', `价格写法不统一：${withSym}/${priced.length} 道带货币符号`);
    }
    const withUnit = priced.filter((d) => /份|例|位|两|斤|只/.test(String(d.price))).length;
    if (withUnit > 0 && withUnit < priced.length) {
      add('warn', 'price-unit', '部分价格带计价单位，部分没有，建议统一');
    }
  }

  // 分节
  const sections = dishes.map((d) => (d.section || '').trim());
  if (sections.some((s) => !s) && sections.some((s) => s)) {
    add('warn', 'mixed-section', '有些菜品归了类，有些没有归类');
  }

  /* ===== 插图层 ===== */

  for (const d of dishes) {
    const s = artStats(d, theme);
    const label = (d.name || '未命名').trim();
    if (s.shapes < 4) {
      add('error', 'art-thin', `「${label}」的插图笔画太少（${s.shapes} 个图元），辨识度不足`, { dishId: d.id });
    } else if (s.shapes > 70) {
      add('warn', 'art-busy', `「${label}」的插图元素过多（${s.shapes} 个），缩到小尺寸会糊成一团`, { dishId: d.id });
    }
    if (s.bytes < 120) {
      add('warn', 'art-tiny', `「${label}」的插图内容过少，可能是空图形`, { dishId: d.id });
    }
  }

  /* ===== 排版层 ===== */

  const L = layoutMenu(menu);
  const contentW = PAPER.width - PAPER.marginX * 2;
  const textW = contentW - SZ.artNormal - SZ.artTextGap - SZ.priceW;

  for (const d of dishes) {
    const label = (d.name || '未命名').trim();
    if (wrapText(d.name || '', textW, FS.dishName).length > 2) {
      add('error', 'name-overflow', `菜名「${label}」太长，两行放不下会被截断`, { dishId: d.id });
    }
    if (wrapText(d.blurb || '', textW, FS.blurb).length > 2) {
      add('warn', 'blurb-truncate', `「${label}」的描述会被截断，建议压到 60 字以内`, { dishId: d.id });
    }
    const pw = measureText(String(d.price || ''), FS.price);
    if (pw > SZ.priceW - 6) {
      add('warn', 'price-wide', `「${label}」的价格文字过宽，会挤压文字区`, { dishId: d.id });
    }
  }

  if (L.height > PAPER.maxHeight) {
    add('warn', 'too-long', `菜单总高 ${Math.round(L.height)} 超过建议上限 ${PAPER.maxHeight}，打印会分页`);
  }
  if (dishes.length > 0 && dishes.length < 4) {
    add('warn', 'too-few', `只有 ${dishes.length} 道菜，菜单会显得空`);
  }
  const sigs = dishes.filter((d) => d.signature).length;
  if (sigs > 1) {
    add('warn', 'multi-signature', `标记了 ${sigs} 道招牌菜，只有第一道会放大展示`); 
  }

  /* ===== 主题层 ===== */

  const cr = contrastRatio(theme.paper, theme.ink);
  if (cr < 7) {
    add('warn', 'contrast-low', `纸墨对比度 ${cr.toFixed(1)}:1 偏低，远看会发灰`);
  }
  const cd = colorDistance(theme.accent, theme.ink);
  if (cd < 28) {
    add('warn', 'accent-close', '点缀色与墨色过于接近，招牌菜看不出区别');
  }

  const errors = issues.filter((i) => i.level === 'error').length;
  const warns = issues.filter((i) => i.level === 'warn').length;

  return {
    ok: errors === 0,
    errors,
    warns,
    issues,
    metrics: {
      height: Math.round(L.height),
      maxHeight: PAPER.maxHeight,
      dishCount: dishes.length,
      signatureCount: sigs,
      contrast: Number(cr.toFixed(2)),
    },
  };
}
