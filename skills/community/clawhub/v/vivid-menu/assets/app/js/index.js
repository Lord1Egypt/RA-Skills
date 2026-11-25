/* ============================================================
 * art/index.js — 插图引擎分发层
 *  1. inferKind()  菜名 → 食材类别
 *  2. buildArt()   类别 + 种子 → 内联 svg 片段
 *  3. sanitizeArt() 外部传入 SVG 的白名单清洗
 *  4. applyTokens() 颜色 token → 主题真实色值
 * ============================================================ */

import { KINDS, KINDS_VARIANTS } from './kinds.js';
import { hash, rng } from './pen.js';

/* ---------------- 菜名 → 类别 ---------------- */

// 精确表优先：这些菜名含歧义关键词（如「鱼香肉丝」并非鱼）
const EXACT = {
  鱼香肉丝: 'pork', 鱼香茄子: 'veg', 蚂蚁上树: 'noodle', 夫妻肺片: 'beef',
  宫保鸡丁: 'chicken', 辣子鸡: 'chicken', 白切鸡: 'chicken', 口水鸡: 'chicken',
  小炒肉: 'pork', 红烧肉: 'pork', 东坡肉: 'pork', 梅菜扣肉: 'pork',
  麻婆豆腐: 'tofu', 家常豆腐: 'tofu', 皮蛋豆腐: 'tofu',
  酸辣粉: 'noodle', 螺蛳粉: 'noodle', 热干面: 'noodle',
  佛跳墙: 'soup', 腌笃鲜: 'soup',
  糖醋里脊: 'pork', 锅包肉: 'pork', 咕噜肉: 'pork',
  酸菜鱼: 'fish', 水煮鱼: 'fish', 烤鱼: 'fish', 松鼠鳜鱼: 'fish',
  小龙虾: 'shrimp', 蒜蓉小龙虾: 'shrimp', 十三香小龙虾: 'shrimp',
  干煸四季豆: 'veg', 清炒时蔬: 'veg', 上汤娃娃菜: 'veg',
  毛血旺: 'hotpot', 麻辣香锅: 'hotpot',
  蛋炒饭: 'rice', 扬州炒饭: 'rice', 煲仔饭: 'rice',
  小笼包: 'dumpling', 生煎包: 'dumpling', 灌汤包: 'dumpling',
  葱油饼: 'pancake', 肉夹馍: 'pancake',
  杨枝甘露: 'dessert', 双皮奶: 'dessert', 红豆沙: 'dessert',
  酸梅汤: 'drink', 大麦茶: 'drink', 柠檬水: 'drink',
};

// 按优先级排列：形态类先于食材类，避免「牛肉面」被判成牛肉
const RULES = [
  ['drink', /酒|茶|醋饮|汁|露|咖啡|奶茶|可乐|酸梅|柠檬水|气泡|苏打|豆浆|米浆|酸奶|汽水|啤酒|米酒|白酒|黄酒/],
  ['hotpot', /火锅|干锅|麻辣香锅|冒菜|麻辣烫|锅底|毛血旺|涮/],
  ['noodle', /面|粉|米线|河粉|粉丝|馄饨面|乌冬|意面|拉条|拌面|炒面|焖面|凉皮|凉面/],
  ['soup', /汤|羹|粥|煲$|例汤|炖盅/],
  ['rice', /饭|煲仔|盖浇|米$|寿司|饭团/],
  ['dumpling', /饺|包$|包子|馄饨|抄手|烧麦|云吞|汤圆|元宵|烧卖/],
  ['pancake', /饼|馍|粑|锅贴|煎包|酥|油条|春卷/],
  ['skewer', /串|烧烤|烤羊肉|烤鸡翅|铁板|烤蔬/],
  ['dessert', /甜|糕|布丁|慕斯|奶冻|冰淇淋|冰激凌|糖水|豆花|芋圆|雪媚娘|蛋挞|芝士/],
  ['crab', /蟹/],
  ['shrimp', /虾|龙虾|虾仁|基围虾/],
  ['fish', /鱼|鲈|鳜|鳝|三文鱼|巴沙|龙利|带鱼|黄花鱼|鱼头/],
  ['shellfish', /贝|螺|蛤|蚝|扇贝|牡蛎|蛏|蚬/],
  ['beef', /牛|肥牛|牛排|牛腩|牛柳|和牛|牛舌/],
  ['pork', /肉|猪|排骨|五花|里脊|肘|叉烧|腊|培根|香肠|腊肠|火腿/],
  ['chicken', /鸡|鸭|鹅|鸽|翅|掌|鸭掌|凤爪/],
  ['mushroom', /菇|菌|木耳|松茸|竹荪|银耳|香菇/],
  ['tofu', /豆腐|豆干|腐竹|豆皮|千张|豆泡|臭豆腐/],
  ['egg', /蛋|番茄炒|韭黄/],
  ['salad', /凉拌|拌|沙拉|爽口|卤味|凉菜|泡菜|腌/],
  ['veg', /菜|笋|茄|豆|瓜|椒|菠|生菜|芥兰|西兰花|花菜|土豆|萝卜|藕|山药|秋葵|芹|苔|苗|芽|菌菇|玉米|南瓜|冬瓜|丝瓜|苦瓜|白菜|紫甘蓝/],
];

export function inferKind(name = '', tags = []) {
  const clean = String(name).replace(/[\s（）()【】\-—_]/g, '');
  for (const key in EXACT) {
    if (clean.includes(key)) return EXACT[key];
  }
  for (const [kind, re] of RULES) {
    if (re.test(clean)) return kind;
  }
  // 菜名没命中时，退回看标签
  const t = tags.join('');
  for (const [kind, re] of RULES) {
    if (re.test(t)) return kind;
  }
  return 'generic';
}

/* ---------------- 生成插图 ---------------- */

/**
 * 生成插图内部片段（不含 <svg> 外壳）
 * @param {string} kind 类别
 * @param {string} seedStr 种子字符串（一般用菜名+id）
 */
export function artInner(kind, seedStr) {
  const draw = KINDS[kind] || KINDS.generic;
  const h = hash(seedStr || kind);
  const rand = rng(h);
  const variants = KINDS_VARIANTS[kind] || 1;
  const variant = h % variants;
  try {
    return draw(rand, variant);
  } catch (e) {
    console.warn('[art] 画法失败，回退通用图形：', kind, e);
    return KINDS.generic(rng(1), 0);
  }
}

/** 颜色 token 替换为真实色值 */
export function applyTokens(fragment, theme) {
  const map = { INK: theme.ink, ACCENT: theme.accent, MUTE: theme.ink };
  return fragment
    .replace(/\bINK\b/g, map.INK)
    .replace(/\bACCENT\b/g, map.ACCENT)
    .replace(/\bMUTE\b/g, map.MUTE);
}

/** 输出可独立使用的完整 <svg> 字符串 */
export function buildArt(dish, theme) {
  const kind = dish.kind || inferKind(dish.name, dish.tags);
  // 种子优先用菜名：同一菜名在任何设备、任何会话都画出同一幅图。
  // _seed 用于「换一幅插图」，显式覆盖；id 是随机会话生成，只在无名时兜底。
  const seed = dish._seed || dish.name || dish.id;
  const inner = dish.art && dish.art.trim()
    ? sanitizeArt(dish.art)
    : artInner(kind, seed);
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100%" height="100%">${applyTokens(inner, theme)}</svg>`;
}

/* ---------------- 外部 SVG 白名单清洗 ---------------- */

const ALLOWED_TAGS = new Set([
  'svg', 'g', 'path', 'line', 'polyline', 'polygon', 'rect', 'circle', 'ellipse',
  'text', 'tspan', 'defs', 'linearGradient', 'radialGradient', 'stop', 'clipPath', 'use',
]);

const ALLOWED_ATTR = /^(d|x|y|x1|y1|x2|y2|cx|cy|r|rx|ry|width|height|points|fill|stroke|stroke-width|stroke-linecap|stroke-linejoin|stroke-dasharray|stroke-opacity|fill-opacity|opacity|transform|viewBox|gradientUnits|offset|stop-color|stop-opacity|clip-path|id|text-anchor|font-size|font-family|font-weight|xmlns)$/;

/**
 * 清洗外部 SVG：只保留绘图相关标签与属性，剔除 script / foreignObject / on* / href 等。
 * 与原版 art 白名单机制对应。
 */
export function sanitizeArt(svg) {
  let s = String(svg);
  // 干掉危险容器及其内容
  s = s.replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/<style[\s\S]*?<\/style>/gi, '')
    .replace(/<foreignObject[\s\S]*?<\/foreignObject>/gi, '')
    .replace(/<iframe[\s\S]*?<\/iframe>/gi, '')
    .replace(/<!--[\s\S]*?-->/g, '')
    .replace(/<\?xml[\s\S]*?\?>/g, '')
    .replace(/<!DOCTYPE[\s\S]*?>/gi, '');

  // 逐标签过滤
  s = s.replace(/<(\/?)([a-zA-Z][\w:-]*)([^>]*?)(\/?)>/g, (m, close, tag, attrs, selfClose) => {
    if (!ALLOWED_TAGS.has(tag)) return '';
    if (close) return `</${tag}>`;
    let out = '';
    const attrRe = /([a-zA-Z_:][\w:.-]*)\s*=\s*"([^"]*)"|([a-zA-Z_:][\w:.-]*)\s*=\s*'([^']*)'/g;
    let a;
    while ((a = attrRe.exec(attrs))) {
      const name = a[1] || a[3];
      const val = a[2] !== undefined ? a[2] : a[4];
      if (!ALLOWED_ATTR.test(name)) continue;
      if (/^(href|xlink:href)$/i.test(name) && !val.startsWith('#')) continue;
      if (/javascript:/i.test(val)) continue;
      out += ` ${name}="${val.replace(/"/g, '&quot;')}"`;
    }
    return `<${tag}${out}${selfClose ? '/' : ''}>`;
  });

  // 去掉 <svg> 外壳，只留内部，由外层统一包 viewBox
  const m = s.match(/<svg[^>]*>([\s\S]*)<\/svg>/i);
  if (m) s = m[1];
  return s;
}

export { KINDS };
