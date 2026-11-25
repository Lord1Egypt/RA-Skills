/* 生动菜单 · 单文件包
 * 由 tools/build.js 生成，请勿直接修改。
 * 改源码请编辑 js/ 下的模块，然后执行：npm run build
 */
(function () {
'use strict';

/* ==================== js/art/pen.js ==================== */
/* ============================================================
 * pen.js — 笔触与图元基础层
 * 所有插图在 viewBox="0 0 100 100" 坐标系内绘制。
 * 颜色使用语义 token：INK（墨）/ ACCENT（点缀）/ MUTE（淡），
 * 渲染时统一替换为当前菜单主题的真实色值。
 * ============================================================ */

const TOKENS = ['INK', 'ACCENT', 'MUTE'];

/** 数值取整，避免生成过长的浮点串 */
const n = (v) => Math.round(v * 100) / 100;

/** 坐标对 */
const xy = (x, y) => `${n(x)} ${n(y)}`;

/** 通用元素构造 */
function el(tag, attrs) {
  let s = `<${tag}`;
  for (const k in attrs) {
    if (attrs[k] === null || attrs[k] === undefined) continue;
    s += ` ${k}="${attrs[k]}"`;
  }
  return s + '/>';
}

/** 描边路径（默认不填充、圆头圆角、线宽 2.2） */
function path(d, o = {}) {
  const {
    fill = 'none', sw = 2.2, c = 'INK', op = 1,
    dash = null, cap = 'round', join = 'round', extra = '',
  } = o;
  return el('path', {
    d, fill, stroke: fill === 'none' ? c : null,
    'stroke-width': fill === 'none' ? sw : null,
    'stroke-linecap': cap, 'stroke-linejoin': join,
    'stroke-opacity': op === 1 ? null : op,
    'stroke-dasharray': dash, opacity: op === 1 ? null : op,
    ...(extra ? JSON.parse(extra) : {}),
  });
}

const line = (x1, y1, x2, y2, o = {}) =>
  path(`M${xy(x1, y1)}L${xy(x2, y2)}`, o);

const circle = (cx, cy, r0, o = {}) => {
  const { fill = 'none', sw = 2.2, c = 'INK', op = 1 } = o;
  return el('circle', {
    cx: n(cx), cy: n(cy), r: n(r0),
    fill, stroke: fill === 'none' ? c : null,
    'stroke-width': fill === 'none' ? sw : null, opacity: op === 1 ? null : op,
  });
};

const ellipse = (cx, cy, rx, ry, o = {}) => {
  const { fill = 'none', sw = 2.2, c = 'INK', op = 1, rot = null } = o;
  return el('ellipse', {
    cx: n(cx), cy: n(cy), rx: n(rx), ry: n(ry),
    fill, stroke: fill === 'none' ? c : null,
    'stroke-width': fill === 'none' ? sw : null,
    opacity: op === 1 ? null : op,
    transform: rot !== null ? `rotate(${n(rot)} ${xy(cx, cy)})` : null,
  });
};

/** 实心色块（用于点缀色小元素） */
const solid = (tag, attrs) => el(tag, { ...attrs, fill: attrs.fill || 'ACCENT', stroke: 'none' });

/* ---------------- 确定性随机 ---------------- */

/** 字符串 → 32 位哈希 */
function hash(str) {
  let h = 2166136261;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

/** 基于种子的伪随机数生成器（mulberry32），保证同一道菜每次画法一致 */
function rng(seed) {
  let a = seed >>> 0;
  return function next() {
    a = (a + 0x6D2B79F5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const pick = (rand, arr) => arr[Math.floor(rand() * arr.length) % arr.length];
const between = (rand, a, b) => a + rand() * (b - a);

/* ---------------- 常用食物图元 ---------------- */

/** 圆盘：外圈 + 内圈，俯视微透视 */
function plate(r = 33, y = 60) {
  return [
    ellipse(50, y, r, r * 0.3, { sw: 2.4 }),
    ellipse(50, y, r * 0.78, r * 0.225, { sw: 1.4, op: 0.55 }),
  ].join('');
}

/** 深碗：碗口椭圆 + 碗身弧线 + 底足 */
function bowl(y = 56, r = 30) {
  const ry = r * 0.28;
  return [
    path(
      `M${xy(50 - r, y)}A${n(r)} ${n(ry)} 0 0 1 ${xy(50 + r, y)}`,
      { sw: 2.4 },
    ),
    path(
      `M${xy(50 - r, y)}C${xy(50 - r * 0.86, y + 26)} ${xy(50 + r * 0.86, y + 26)} ${xy(50 + r, y)}`,
      { sw: 2.4 },
    ),
    path(
      `M${xy(50 - r * 0.34, y + 24)}L${xy(50 - r * 0.26, y + 29)}L${xy(50 + r * 0.26, y + 29)}L${xy(50 + r * 0.34, y + 24)}`,
      { sw: 2 },
    ),
    ellipse(50, y, r, ry, { sw: 1.4, op: 0.45 }),
  ].join('');
}

/** 一个食物块：不规则四边形 + 内部高光 */
function block(cx, cy, w, h, rot, rand, o = {}) {
  const { sw = 2.2, highlight = true } = o;
  const j = () => between(rand, -0.09, 0.09);
  const hw = w / 2, hh = h / 2;
  const p = [
    [cx - hw * (1 + j()), cy - hh * (1 + j())],
    [cx + hw * (1 + j()), cy - hh * (1 + j())],
    [cx + hw * (1 + j()), cy + hh * (1 + j())],
    [cx - hw * (1 + j()), cy + hh * (1 + j())],
  ];
  const a = (rot * Math.PI) / 180;
  const cos = Math.cos(a), sin = Math.sin(a);
  const pts = p.map(([px, py]) => {
    const dx = px - cx, dy = py - cy;
    return xy(cx + dx * cos - dy * sin, cy + dx * sin + dy * cos);
  });
  const d = `M${pts[0]}L${pts[1]}L${pts[2]}L${pts[3]}Z`;
  const out = [path(d, { sw, join: 'round' })];
  if (highlight) {
    const hy = cy - hh * 0.34;
    out.push(
      path(
        `M${xy(cx - hw * 0.52, hy + 1.2)}Q${xy(cx, hy - 1.8)} ${xy(cx + hw * 0.5, hy + 0.6)}`,
        { sw: 1.5, op: 0.5 },
      ),
    );
  }
  return out.join('');
}

/** 弧线叶片：从 (x,y) 起，朝 rot 方向长出。w 控制叶片饱满度 */
function leafShape(x, y, len, rot, o = {}) {
  const { sw = 2, vein = true, w = 0.32 } = o;
  const a = (rot * Math.PI) / 180;
  const tx = x + Math.cos(a) * len;
  const ty = y + Math.sin(a) * len;
  const nx = Math.cos(a + Math.PI / 2) * len * w;
  const ny = Math.sin(a + Math.PI / 2) * len * w;
  const d = `M${xy(x, y)}Q${xy((x + tx) / 2 + nx, (y + ty) / 2 + ny)} ${xy(tx, ty)}Q${xy((x + tx) / 2 - nx, (y + ty) / 2 - ny)} ${xy(x, y)}`;
  const out = [path(d, { sw })];
  if (vein) out.push(path(`M${xy(x, y)}L${xy(tx, ty)}`, { sw: 1.1, op: 0.45 }));
  return out.join('');
}

/** 偏移动画字符串（用于相对指令 q/c 的控制点） */
const dv = (dx, dy) => `${n(dx)} ${n(dy)}`;

/**
 * 卵形叶：基部窄、中段宽、端部圆钝——用于蔬菜（油菜、菠菜、白菜）。
 * 与 leafShape 的两端尖细形成对比。
 */
function leafOval(x, y, len, rot, w = 0.42, o = {}) {
  const { sw = 1.9, vein = true } = o;
  const a = (rot * Math.PI) / 180;
  const dx = Math.cos(a), dy = Math.sin(a);
  const px = -dy, py = dx;
  const P = (along, side) => [
    x + dx * len * along + px * len * side,
    y + dy * len * along + py * len * side,
  ];
  const b0 = P(0.02, -0.1 * w * 4);
  const b1 = P(0.02, 0.1 * w * 4);
  const c1 = P(0.42, -w * 1.5);
  const c2 = P(0.82, -w * 1.05);
  const c3 = P(0.8, w * 1.05);
  const c4 = P(0.42, w * 1.5);
  const tip = P(1, 0);
  const d = `M${xy(b0[0], b0[1])}C${xy(c1[0], c1[1])} ${xy(c2[0], c2[1])} ${xy(tip[0], tip[1])}C${xy(c3[0], c3[1])} ${xy(c4[0], c4[1])} ${xy(b1[0], b1[1])}Z`;
  const out = [path(d, { sw, join: 'round' })];
  if (vein) {
    const v1 = P(0.75, 0), v2 = P(0.5, -0.22), v3 = P(0.5, 0.22);
    out.push(path(`M${xy(b0[0], b0[1])}L${xy(v1[0], v1[1])}`, { sw: 1, op: 0.4 }));
    out.push(path(`M${xy(P(0.42, 0)[0], P(0.42, 0)[1])}L${xy(v2[0], v2[1])}`, { sw: 0.9, op: 0.32 }));
    out.push(path(`M${xy(P(0.42, 0)[0], P(0.42, 0)[1])}L${xy(v3[0], v3[1])}`, { sw: 0.9, op: 0.32 }));
  }
  return out.join('');
}

/** 蒸汽：三条上升的波浪线 */
function steam(cx, cy, h = 22, count = 3) {
  const out = [];
  for (let i = 0; i < count; i++) {
    const x = cx + (i - (count - 1) / 2) * 8;
    out.push(
      path(
        `M${xy(x, cy)}c${xy(3.4, -h * 0.28)} ${xy(-3.4, -h * 0.46)} ${xy(0.6, -h * 0.72)}`,
        { sw: 1.5, op: 0.4, c: 'MUTE' },
      ),
    );
  }
  return out.join('');
}

/** 葱花 / 芝麻 / 花椒点 */
function dots(rand, cx, cy, r0, count, size = 1.5) {
  const out = [];
  for (let i = 0; i < count; i++) {
    const a = rand() * Math.PI * 2;
    const rr = Math.sqrt(rand()) * r0;
    out.push(circle(cx + Math.cos(a) * rr, cy + Math.sin(a) * rr * 0.42, between(rand, size * 0.7, size), { sw: 1.2, op: 0.75 }));
  }
  return out.join('');
}

/** 辣椒：弯月形果实 + 柄 */
function chili(x, y, len, rot, filled = true) {
  const a = (rot * Math.PI) / 180;
  const cos = Math.cos(a), sin = Math.sin(a);
  const T = (px, py) => xy(x + px * cos - py * sin, y + px * sin + py * cos);
  const d = `M${T(0, 0)}C${T(len * 0.42, -len * 0.3)} ${T(len * 0.86, -len * 0.16)} ${T(len, len * 0.16)}C${T(len * 0.7, len * 0.14)} ${T(len * 0.36, len * 0.1)} ${T(0, 0)}Z`;
  return [
    path(d, { fill: filled ? 'ACCENT' : 'none', c: 'INK', sw: filled ? 1.5 : 2 }),
    path(`M${T(0, 0)}L${T(-len * 0.14, -len * 0.1)}`, { sw: 1.8, c: 'INK' }),
  ].join('');
}

/** 筷子：两根细长条 */
function chopsticks(x, y, len, rot) {
  return [
    path(`M${xy(x, y)}L${xy(x + Math.cos((rot * Math.PI) / 180) * len, y + Math.sin((rot * Math.PI) / 180) * len)}`, { sw: 2 }),
    path(`M${xy(x, y + 4)}L${xy(x + Math.cos((rot * Math.PI) / 180) * (len * 0.9), y + 4 + Math.sin((rot * Math.PI) / 180) * (len * 0.9))}`, { sw: 2 }),
  ].join('');
}


/* ==================== js/art/kinds.js ==================== */
/* ============================================================
 * kinds.js — 食材类别画法库
 * 每个画法都是 (rand, variant) => svg 片段，绘制在 0 0 100 100 内。
 * variant 用于在同类别内产生不同构图，避免整页插图雷同。
 * ============================================================ */



/* ---------- 肉类 ---------- */

// 猪肉：方块塔（红烧）/ 厚方绑绳（东坡）/ 切片覆梅菜（扣肉）
function pork(rand) {
  const mode = Math.floor(rand() * 3);
  const out = [plate(33, 62)];

  if (mode === 0) {
    // 红烧肉：三块方肉垒成小塔，肥瘦分层
    for (const [x, y, w, h, r] of [[38, 55, 15, 11, -6], [62, 55, 15, 11, 5], [50, 45, 16, 11, 0]]) {
      out.push(block(x, y, w, h, r, rand));
      out.push(path(`M${xy(x - w * 0.42, y - 1.4)}q${xy(w * 0.42, -2.4)} ${xy(w * 0.84, 0.6)}`, { sw: 1.3, op: 0.55 }));
    }
    out.push(
      leafShape(31, 67, 12, -30, { sw: 1.8, vein: false, w: 0.36 }),
      leafShape(69, 67, 11, 210, { sw: 1.8, vein: false, w: 0.36 }),
      path(`M${xy(34, 62)}q${xy(16, 6)} ${xy(32, 0)}`, { sw: 1.3, op: 0.4 }),
    );
  } else if (mode === 1) {
    // 东坡肉：两块厚方，十字草绳捆绑
    for (const [x, y, s] of [[42, 54, 1], [60, 57, 0.86]]) {
      const w = 24 * s, h = 17 * s;
      out.push(path(`M${xy(x - w / 2, y - h / 2)}L${xy(x + w / 2, y - h / 2)}L${xy(x + w / 2, y + h / 2)}L${xy(x - w / 2, y + h / 2)}Z`, { sw: 2.4 }));
      // 肥皮
      out.push(path(`M${xy(x - w / 2, y - h / 2 + 2.6)}L${xy(x + w / 2, y - h / 2 + 2.6)}`, { sw: 1.4, op: 0.6 }));
      // 草绳
      out.push(
        path(`M${xy(x - w * 0.18, y - h / 2 - 1)}L${xy(x - w * 0.18, y + h / 2 + 1)}`, { sw: 1.4, op: 0.7, dash: '2 1.6' }),
        path(`M${xy(x - w / 2 - 1, y + 1)}L${xy(x + w / 2 + 1, y + 1)}`, { sw: 1.4, op: 0.7, dash: '2 1.6' }),
      );
    }
    out.push(path(`M${xy(34, 64)}q${xy(16, 5)} ${xy(32, 0)}`, { sw: 1.3, op: 0.4 }));
  } else {
    // 梅菜扣肉：肉片呈扇形层叠，顶上覆梅菜
    for (let i = 0; i < 5; i++) {
      const y = 50 + i * 4.2;
      out.push(path(`M${xy(36 + i * 0.7, y)}L${xy(64 - i * 0.7, y)}`, { sw: 2.2 - i * 0.1 }));
    }
    out.push(path(`M${xy(35, 48)}q${xy(15, -9)} ${xy(30, 0)}`, { sw: 2.4 }));
    // 梅菜碎
    for (let i = 0; i < 7; i++) {
      const x = 39 + i * 3.6;
      out.push(path(`M${xy(x, 47 - Math.sin(i) * 1.5)}q${xy(1.6, -2)} ${xy(3, 0.4)}`, { sw: 1.1, op: 0.6 }));
    }
  }
  return out.join('');
}

// 牛肉：块烧 / 牛排格纹 / 薄片扇形
function beef(rand, v, name) {
  // 菜名决定构图：水煮/麻辣 → 汤碗肉片，牛排/烤 → 肉排，丝/片/炒 → 薄片，其余 → 肉块
  const n = String(name || '');
  let mode;
  if (/牛排|西冷|肋眼|菲力|烤牛|煎牛|战斧/.test(n)) mode = 1;
  else if (/水煮|麻辣|香辣|沸腾|汤|煲|锅/.test(n)) mode = 2;
  else if (/丝|片|炒|爆|柳|铁板/.test(n)) mode = 3;
  else if (/红烧|炖|焖|萝卜|土豆|番茄|咖喱|块/.test(n)) mode = 0;
  else mode = Math.floor(rand() * 4);

  const out = [];

  if (mode === 0) {
    /* 红烧牛肉：三块厚肉叠成小堆，块内有肥筋线 */
    out.push(plate(33, 65));
    const chunks = [
      [40, 56, 22, 16, -7],
      [61, 58, 21, 15, 6],
      [51, 45, 23, 16, 1],
    ];
    for (const [x, y, w, h, r] of chunks) {
      out.push(block(x, y, w, h, r, rand, { highlight: false }));
      out.push(
        path(`M${xy(x - w * 0.32, y + 1)}q${xy(w * 0.2, -2.4)} ${xy(w * 0.44, 0)}`, { sw: 1.1, op: 0.45 }),
        path(`M${xy(x - w * 0.28, y + 4.4)}q${xy(w * 0.2, -2)} ${xy(w * 0.38, 0)}`, { sw: 1, op: 0.3 }),
      );
    }
    out.push(leafShape(31, 70, 12, -24, { sw: 1.6, vein: false, w: 0.34 }));
    out.push(dots(rand, 50, 62, 12, 3, 1));
  } else if (mode === 1) {
    /* 牛排：厚切肉排（带侧面厚度）+ 烤格纹 + 平放迷迭香 */
    out.push(plate(34, 71));
    out.push(path(
      `M${xy(33, 57)}Q${xy(31, 46)} ${xy(45, 45)}L${xy(60, 45)}Q${xy(72, 47)} ${xy(68, 58)}Q${xy(66, 66)} ${xy(50, 66)}Q${xy(35, 66)} ${xy(33, 57)}Z`,
      { sw: 2.6 },
    ));
    // 厚度：下缘一条平行弧
    out.push(path(`M${xy(35, 60)}Q${xy(38, 65)} ${xy(50, 65.4)}Q${xy(63, 65)} ${xy(66.4, 59)}`, { sw: 1.5, op: 0.55 }));
    // 烤格纹（斜向，落在肉面中部）
    for (let i = 0; i < 3; i++) {
      out.push(path(`M${xy(40 + i * 6, 49)}L${xy(48 + i * 6, 61)}`, { sw: 2, op: 0.5 }));
    }
    // 边缘油脂
    out.push(path(`M${xy(45, 45.6)}q${xy(8, -0.6)} ${xy(13, 1.6)}`, { sw: 1.2, op: 0.4 }));
    for (const [dx, dy] of [[0, 0], [2.4, 1.7], [4.8, 3.4]]) {
      out.push(leafShape(60 + dx, 47 + dy, 8, 22, { sw: 1.2, vein: false, w: 0.3 }));
    }
  } else if (mode === 2) {
    /* 水煮牛肉：汤碗 + 红油 + 牛肉片 + 干辣椒 + 花椒 + 蒸汽 */
    out.push(bowl(54, 28));
    out.push(ellipse(50, 54, 23, 6.5, { sw: 1.6, op: 0.7 }));
    for (const [x, y, r] of [[42, 53, -12], [55, 55, 9], [48, 50, 3], [61, 52, -7]]) {
      out.push(path(
        `M${xy(x - 7, y)}q${xy(3.6, -4)} ${xy(7, -0.6)}q${xy(1.4, 3.4)} ${xy(-3, 4)}q${xy(-3, 1.4)} ${xy(-4, -3.4)}Z`,
        { sw: 1.8, extra: JSON.stringify({ transform: `rotate(${r} ${xy(x, y)})` }) },
      ));
    }
    out.push(chili(33, 51, 8, 190, true), chili(66, 55, 7, 12, true));
    out.push(dots(rand, 50, 53, 15, 5, 1));
    out.push(steam(50, 44, 20, 3));
  } else {
    /* 牛柳/小炒：细长肉条交错 + 葱段 + 辣椒 */
    out.push(plate(33, 63));
    const strips = [
      [50, 55, -8], [50, 50, 6], [50, 60, 3], [46, 45, -14], [54, 65, 12],
    ];
    for (const [x, y, r] of strips) {
      out.push(block(x, y, 27, 4.6, r, rand, { highlight: false, sw: 1.9 }));
    }
    out.push(chili(30, 57, 11, 200, true), chili(71, 52, 10, 12, true));
    out.push(dots(rand, 50, 56, 13, 4, 1));
  }
  return out.join('');
}

// 禽类：鸡块带辣椒 / 整只鸡腿带骨（两种都经得起放大）
function chicken(rand, v, name) {
  // 菜名决定构图：白切/口水 → 切片，辣子/宫保/鸡丁 → 鸡块，鸡腿/翅/烤 → 带骨整只
  const n = String(name || '');
  let mode;
  if (/白切|口水|盐焗|盐水|醉鸡|切鸡|凉拌/.test(n)) mode = 2;
  else if (/辣子|宫保|鸡丁|鸡块|炒鸡|爆鸡|大盘鸡/.test(n)) mode = 0;
  else if (/腿|翅|琵琶|烤鸡|炸鸡|烧鸡|叫花/.test(n)) mode = 1;
  else mode = Math.floor(rand() * 3);
  const out = [];

  if (mode === 0) {
    /* 鸡块：三块带棱的肉 + 双椒 + 花椒 + 葱段 */
    out.push(plate(33, 62));
    out.push(block(41, 54, 15, 13, -12, rand), block(60, 57, 14, 12, 9, rand), block(50, 45, 13, 11, 3, rand));
    out.push(dots(rand, 50, 57, 15, 6, 1.1));
    out.push(chili(28, 60, 13, 198, true), chili(72, 52, 11, 14, true));
    out.push(leafShape(36, 66, 12, -22, { sw: 1.6, vein: false, w: 0.34 }));
    out.push(path(`M${xy(34, 63)}q${xy(16, 6)} ${xy(32, -1)}`, { sw: 1.3, op: 0.42 }));
  } else if (mode === 1) {
    /* 整只鸡腿：梨形腿肉 + 一根骨头 + 骨节 */
    out.push(plate(35, 70));
    out.push(path(
      `M${xy(60, 50)}C${xy(67, 56)} ${xy(65, 68)} ${xy(53, 73)}C${xy(39, 78)} ${xy(29, 68)} ${xy(31, 57)}C${xy(33, 47)} ${xy(48, 43)} ${xy(60, 50)}Z`,
      { sw: 2.4 },
    ));
    // 骨头从肉的上端伸出，末端有两个骨节
    out.push(path(`M${xy(59, 51)}L${xy(71, 40)}`, { sw: 3.2 }));
    out.push(circle(73, 38, 3.4, { sw: 1.9 }), circle(69, 42, 2.6, { sw: 1.7 }));
    // 皮纹
    out.push(path(`M${xy(40, 58)}q${xy(8, -4)} ${xy(14, -1)}`, { sw: 1.2, op: 0.45 }));
    out.push(path(`M${xy(43, 64)}q${xy(7, -3)} ${xy(12, -1)}`, { sw: 1.1, op: 0.35 }));
    // 椒盐
    out.push(dots(rand, 46, 60, 11, 4, 1));
  } else {
    /* 白切鸡：并排码放的四片，带皮线，边片略矮 */
    out.push(plate(36, 71));
    for (let i = 0; i < 4; i++) {
      const x = 32 + i * 6.6;
      const top = 50 + (i === 0 || i === 3 ? 2.5 : 0);
      out.push(path(
        `M${xy(x, 69)}Q${xy(x + 0.6, top + 2)} ${xy(x + 3.7, top)}Q${xy(x + 6.8, top + 2)} ${xy(x + 7.4, 69)}Z`,
        { sw: 1.9 },
      ));
      // 皮线
      out.push(path(`M${xy(x + 0.5, 64)}Q${xy(x + 3.7, 62.2)} ${xy(x + 6.9, 64)}`, { sw: 1, op: 0.45 }));
    }
    // 姜葱蘸料小碟 + 葱花
    out.push(circle(50, 71, 4.4, { sw: 1.5, op: 0.65 }));
    out.push(dots(rand, 50, 71, 2.4, 3, 0.9));
    out.push(leafShape(70, 60, 10, -38, { sw: 1.4, vein: false, w: 0.34 }));
  }
  return out.join('');
}

/* ---------- 水产 ---------- */

// 整鱼：清蒸整条 / 汤碗鱼片 / 花刀松鼠鱼
function fish(rand, v, name) {
  const n = String(name || '');
  let mode;
  if (/水煮|酸菜|番茄鱼|鱼片|汆|滑|冷锅/.test(n)) mode = 1;
  else if (/松鼠|糖醋|菊花|花刀/.test(n)) mode = 2;
  else if (/清蒸|红烧|烤|干烧|香煎/.test(n)) mode = 0;
  else mode = Math.floor(rand() * 3);

  if (mode === 1) {
    // 汤碗鱼片：三片梭形鱼片浮在汤面，红油辣椒点缀
    const out = [bowl(50, 28)];
    out.push(ellipse(50, 50, 23, 6.2, { sw: 1.5, op: 0.65 }));
    const slice = (cx, cy, rot, s = 1) => {
      const w = 9.5 * s, h = 4.2 * s;
      return path(
        `M${xy(cx - w, cy)}Q${xy(cx, cy - h * 1.5)} ${xy(cx + w, cy)}Q${xy(cx, cy + h * 1.5)} ${xy(cx - w, cy)}Z`,
        { sw: 1.6, extra: JSON.stringify({ transform: `rotate(${rot} ${xy(cx, cy)})` }) },
      );
    };
    out.push(slice(42, 49, -14), slice(56, 52, 10), slice(49, 45, 2, 0.85));
    // 酸菜叶压在碗沿两侧，避免与鱼片缠在一起
    out.push(
      leafOval(35, 53, 7.5, -155, 0.5, { sw: 1.2, vein: false }),
      leafOval(64, 54, 7, -25, 0.5, { sw: 1.2, vein: false }),
    );
    out.push(chili(31, 47, 8.5, 200, true), chili(66, 48, 7.5, 10, true));
    out.push(dots(rand, 50, 50, 14, 4, 1));
    out.push(steam(50, 40, 20, 3));
    return out.join('');
  }

  const out = [ellipse(50, 62, 38, 9, { sw: 2.2 })];
  const body = `M20 58C26 44 ${xy(48, 40)} 66 52Q${xy(70, 48)} 72 47Q${xy(74, 52)} 72.5 58Q${xy(74, 64)} 72 69Q70 68 66 64C48 76 26 72 20 58Z`;
  out.push(path(body, { sw: 2.4 }));
  out.push(
    circle(28, 57, 1.9, { fill: 'INK', sw: 0 }),
    circle(28, 57, 3.4, { sw: 1.2, op: 0.6 }),
    path(`M35 53q${xy(4, 5)} ${xy(0, 10)}`, { sw: 1.4, op: 0.7 }),
    path(`M72 47q${xy(10, 2)} ${xy(11, 11)}q${xy(-7, -1)} ${xy(-11, 11)}`, { sw: 2 }),
    path(`M42 45q${xy(9, -6)} ${xy(18, 1)}`, { sw: 1.8 }),
  );

  if (mode === 2) {
    // 松鼠鳜鱼：菱形花刀 + 浇汁
    for (let i = 0; i < 3; i++) {
      for (let j = 0; j < 2; j++) {
        out.push(path(`M${xy(40 + i * 9, 49 + j * 6)}l${xy(4, 4)}l${xy(-4, 4)}l${xy(-4, -4)}Z`, { sw: 1.2, op: 0.55 }));
      }
    }
    out.push(path(`M${xy(34, 66)}q${xy(16, 5)} ${xy(32, -1)}`, { sw: 1.6, op: 0.5 }));
  } else {
    // 清蒸：鳞片 + 葱丝
    for (let i = 0; i < 3; i++) {
      out.push(path(`M${xy(40 + i * 8, 50)}q${xy(4, 6)} ${xy(0, 12)}`, { sw: 1.1, op: 0.4 }));
    }
    out.push(
      path(`M${xy(44, 44)}q${xy(6, -3)} ${xy(13, -1)}`, { sw: 1.5, op: 0.6 }),
      path(`M${xy(48, 41)}q${xy(7, -2)} ${xy(13, 1)}`, { sw: 1.5, op: 0.6 }),
    );
  }
  return out.join('');
}

// 虾：C 形身体 + 分节 + 尾扇 + 触须
function shrimp(rand) {
  const out = [plate(31, 62)];
  out.push(path('M30 46C24 58 30 72 46 74C60 76 70 66 68 54', { sw: 2.4 }));
  out.push(path('M36 44C32 56 37 66 48 68C58 70 64 62 62 52', { sw: 2 }));
  // 分节
  for (let i = 0; i < 4; i++) {
    const t = i / 4;
    out.push(path(`M${xy(33 + t * 4, 50 + t * 18)}l${xy(7, 1.5)}`, { sw: 1.2, op: 0.55 }));
  }
  // 尾扇
  out.push(path('M68 54l8 -6l-1 8l7 -2l-6 8z', { sw: 1.8 }));
  // 头与眼
  out.push(circle(31, 44, 2, { fill: 'INK', sw: 0 }));
  // 触须
  out.push(path('M30 44q-10 -6 -14 -1', { sw: 1.2, op: 0.65 }), path('M30 47q-11 0 -13 6', { sw: 1.2, op: 0.5 }));
  return out.join('');
}

// 蟹：壳 + 双钳 + 六足
function crab(rand) {
  const out = [plate(33, 64)];
  out.push(ellipse(50, 56, 19, 14, { sw: 2.4 }));
  out.push(path(`M36 50q${xy(14, -7)} ${xy(28, 0)}`, { sw: 1.3, op: 0.5 }));
  // 眼柄
  out.push(circle(44, 41, 1.6, { fill: 'INK', sw: 0 }), circle(56, 41, 1.6, { fill: 'INK', sw: 0 }));
  // 钳
  out.push(
    path('M31 52q-11 -8 -15 -2q-3 6 5 7q-6 2 -3 6q4 4 12 -3', { sw: 2.2 }),
    path('M69 52q11 -8 15 -2q3 6 -5 7q6 2 3 6q-4 4 -12 -3', { sw: 2.2 }),
  );
  // 腿
  for (let i = 0; i < 3; i++) {
    const y = 58 + i * 5;
    out.push(path(`M${xy(34, y)}q${xy(-10, 3)} ${xy(-12, 9)}`, { sw: 1.7 }));
    out.push(path(`M${xy(66, y)}q${xy(10, 3)} ${xy(12, 9)}`, { sw: 1.7 }));
  }
  return out.join('');
}

// 贝类：铰链在下的扇形壳 + 放射纹
function shellfish(rand) {
  const out = [plate(33, 63)];
  const shell = (cx, cy, s) => {
    const hx = cx, hy = cy + 5 * s;
    const R = 13.5 * s;
    const a1 = -158, a2 = -22;
    const P = (ang, r) => [hx + Math.cos((ang * Math.PI) / 180) * r, hy + Math.sin((ang * Math.PI) / 180) * r];
    const p1 = P(a1, R), p2 = P(a2, R);
    let g = path(`M${xy(hx, hy)}L${xy(p1[0], p1[1])}A${R} ${R} 0 0 1 ${xy(p2[0], p2[1])}Z`, { sw: 2.2 });
    for (let i = 1; i < 7; i++) {
      const ang = a1 + ((a2 - a1) * i) / 7;
      const pp = P(ang, R * 0.94);
      g += path(`M${xy(hx, hy)}L${xy(pp[0], pp[1])}`, { sw: 1, op: 0.42 });
    }
    // 铰链小弧
    g += path(`M${xy(hx - 3.4 * s, hy)}q${xy(3.4 * s, 2.6 * s)} ${xy(6.8 * s, 0)}`, { sw: 1.6 });
    return g;
  };
  out.push(shell(40, 58, 1.05), shell(61, 60, 0.88));
  return out.join('');
}

/* ---------- 蔬食 ---------- */

// 青菜：整棵油菜（白帮 + 宽叶），或一丛炒叶菜
function veg(rand) {
  const mode = Math.floor(rand() * 2);
  const out = [plate(33, 63)];

  if (mode === 0) {
    // 整棵油菜：底部菜帮，上面五片宽叶重叠成菜心
    const cabbage = (cx, cy, s, tilt) => {
      let g = path(
        `M${xy(cx - 3.4 * s, cy)}q${xy(0.2 * s, 6.2 * s)} ${xy(3.4 * s, 6.6 * s)}q${xy(3.2 * s, -0.4 * s)} ${xy(3.4 * s, -6.6 * s)}Z`,
        { sw: 1.9 },
      );
      const angles = [[-130, 1], [-88, 1.16], [-46, 1], [-108, 0.84]];
      for (const [ang, k] of angles) {
        g += leafOval(cx, cy - 2 * s, 16.5 * s * k, ang + tilt, 0.44, { sw: 1.8 });
      }
      return g;
    };
    out.push(cabbage(38, 56, 1.05, -9), cabbage(64, 60, 0.92, 11));
  } else {
    // 炒叶菜：叶片围绕中心放射，稍短
    for (let i = 0; i < 6; i++) {
      const ang = -155 + i * 25;
      out.push(leafOval(50 + (i % 3 - 1) * 3, 61, between(rand, 12, 16), ang, 0.36, { sw: 1.7 }));
    }
    out.push(dots(rand, 50, 58, 11, 3, 1.2));
  }
  return out.join('');
}

// 菌菇：伞盖 + 柄 + 斑点
function mushroom(rand) {
  const out = [plate(32, 63)];
  const one = (cx, cy, s) => {
    let g = path(`M${xy(cx - 13 * s, cy + 2 * s)}Q${xy(cx - 12 * s, cy - 11 * s)} ${xy(cx, cy - 11 * s)}Q${xy(cx + 12 * s, cy - 11 * s)} ${xy(cx + 13 * s, cy + 2 * s)}Z`, { sw: 2.2 });
    g += path(`M${xy(cx - 4 * s, cy + 2 * s)}l${xy(-1.5 * s, 8 * s)}q${xy(5.5 * s, 2 * s)} ${xy(11 * s, 0)}l${xy(-1.5 * s, -8 * s)}`, { sw: 2 });
    g += path(`M${xy(cx - 8 * s, cy - 4 * s)}q${xy(4, -3)} ${xy(8, 0)}`, { sw: 1.1, op: 0.5 });
    return g;
  };
  out.push(one(42, 56, 0.9), one(58, 58, 1.05));
  return out.join('');
}

// 豆腐：立方体（顶面菱形 + 双侧面）
function tofu(rand) {
  const out = [plate(33, 63)];
  const cube = (cx, cy, s) => {
    const w = 11 * s, h = 7 * s, d = 5 * s;
    return [
      path(`M${xy(cx, cy - h)}L${xy(cx + w, cy - h + d)}L${xy(cx, cy - h + 2 * d)}L${xy(cx - w, cy - h + d)}Z`, { sw: 2 }),
      path(`M${xy(cx - w, cy - h + d)}L${xy(cx - w, cy + h)}L${xy(cx, cy + h + d)}L${xy(cx, cy - h + 2 * d)}`, { sw: 2 }),
      path(`M${xy(cx + w, cy - h + d)}L${xy(cx + w, cy + h)}L${xy(cx, cy + h + d)}`, { sw: 2 }),
    ].join('');
  };
  out.push(cube(42, 56, 1), cube(60, 58, 0.85));
  return out.join('');
}

// 蛋：荷包蛋 / 番茄炒蛋
function egg(rand, v) {
  const out = [plate(33, 62)];
  if (v % 2 === 0) {
    out.push(
      path('M32 58q-3 -13 9 -15q6 -8 14 -2q11 -3 12 7q6 6 0 11q-4 8 -13 5q-8 5 -14 -1q-8 -1 -8 -5Z', { sw: 2.2 }),
      circle(50, 55, 6.5, { sw: 2 }),
      circle(48, 53, 1.6, { sw: 1, op: 0.4 }),
    );
  } else {
    // 番茄炒蛋：红黄块交错
    const reds = [[37, 55, 6.5, 5, -12], [61, 61, 6, 4.6, 10], [48, 64, 5.5, 4.2, -4], [64, 50, 5.5, 4.2, 8]];
    const yellows = [[50, 52, 11, 8, 6], [64, 52, 9, 7, -8], [34, 63, 8, 6, 14]];
    for (const [x, y, w, h, r] of yellows) out.push(block(x, y, w, h, r, rand));
    for (const [x, y, w, h, r] of reds) out.push(path(`M${xy(x - w / 2, y - h / 2)}L${xy(x + w / 2, y - h / 2)}L${xy(x + w / 2, y + h / 2)}L${xy(x - w / 2, y + h / 2)}Z`, { fill: 'ACCENT', c: 'INK', sw: 1.5 }));
  }
  return out.join('');
}

// 凉菜：盘 + 两堆细丝（成束而非散落）
function salad(rand) {
  const out = [plate(33, 62)];
  const heap = (cx, cy, s) => {
    let g = '';
    for (let i = 0; i < 6; i++) {
      const dy = (i - 2.5) * 2.3 * s;
      g += path(`M${xy(cx - 11 * s, cy + dy)}q${xy(11 * s, dy * 0.45 - 3.4 * s)} ${xy(22 * s, 0)}`, { sw: 1.6, op: 0.78 });
    }
    return g;
  };
  out.push(heap(43, 56, 0.92), heap(59, 60, 0.8));
  out.push(dots(rand, 50, 55, 12, 4, 1.3));
  return out.join('');
}

/* ---------- 主食 ---------- */

// 面：碗 + 面条 + 筷
function noodle(rand, v) {
  const out = [bowl(54, 29)];
  for (let i = 0; i < 4; i++) {
    const x = 34 + i * 6.4;
    out.push(path(`M${xy(x, 46)}c${xy(4, -8)} ${xy(-4, -13)} ${xy(1, -21)}`, { sw: 1.8, op: 0.85 }));
  }
  // 浇头
  out.push(block(44, 40, 11, 7, -8, rand), block(59, 42, 10, 7, 10, rand), dots(rand, 50, 38, 10, 4, 1.1));
  if (v % 2 === 0) out.push(chopsticks(58, 20, 30, 62));
  out.push(steam(50, 30, 14, 2));
  return out.join('');
}

// 米饭：碗 + 饭堆
function rice(rand) {
  const out = [bowl(56, 28)];
  out.push(path('M30 54q3 -16 20 -16q17 0 20 16', { sw: 2.2 }));
  for (let i = 0; i < 12; i++) {
    out.push(circle(between(rand, 33, 67), between(rand, 42, 53), between(rand, 0.7, 1.3), { sw: 1, op: 0.55 }));
  }
  out.push(steam(50, 36, 13, 3));
  return out.join('');
}

// 汤：碗 + 液面 + 浮料 + 蒸汽
function soup(rand) {
  const out = [bowl(52, 30)];
  out.push(ellipse(50, 52, 24, 6.5, { sw: 1.6, op: 0.7 }));
  out.push(dots(rand, 44, 52, 9, 3, 2.2), dots(rand, 58, 53, 7, 2, 1.8));
  out.push(leafShape(53, 50, 8, -18, { sw: 1.4, vein: false }));
  out.push(steam(50, 42, 22, 3));
  return out.join('');
}

// 饺子：盘 + 三只月牙，顶部褶子
function dumpling(rand) {
  const out = [plate(33, 63)];
  const jiao = (cx, cy, s) => {
    const w = 11 * s, h = 8 * s;
    let g = path(
      `M${xy(cx - w, cy + 1.5 * s)}Q${xy(cx, cy - h * 1.75)} ${xy(cx + w, cy + 1.5 * s)}Q${xy(cx, cy + h * 1.15)} ${xy(cx - w, cy + 1.5 * s)}Z`,
      { sw: 2.2 },
    );
    // 顶部褶：四道小弧，位置沿上弧抬升
    for (let i = 0; i < 4; i++) {
      const x0 = cx - w * 0.6 + i * (w * 1.2 / 4);
      const lift = (Math.abs(i - 1.5) ** 2) * 0.55 * s;
      g += path(`M${xy(x0, cy - h * 0.72 + lift)}q${dv(1.5 * s, -2.7 * s)} ${dv(3 * s, 0.1 * s)}`, { sw: 1.2, op: 0.7 });
    }
    // 下腹弧
    g += path(`M${xy(cx - w * 0.68, cy + 3.6 * s)}q${xy(w * 0.68, 2.5 * s)} ${xy(w * 1.36, 0)}`, { sw: 1.2, op: 0.4 });
    return g;
  };
  out.push(jiao(42, 58, 0.95), jiao(60, 61, 0.86), jiao(51, 49, 0.78));
  return out.join('');
}

// 饼：两层圆饼 + 厚度边 + 焦斑 + 芝麻
function pancake(rand) {
  const out = [plate(33, 63)];
  // 下层饼（带厚度）
  out.push(
    ellipse(50, 56, 24, 10, { sw: 2.4 }),
    path(`M${xy(26, 56)}q${xy(24, 9)} ${xy(48, 0)}`, { sw: 1.3, op: 0.35 }),
  );
  // 上层饼
  out.push(ellipse(50, 50, 21.5, 9, { sw: 2 }));
  // 焦斑
  for (let i = 0; i < 5; i++) {
    const a = rand() * Math.PI * 2, r0 = Math.sqrt(rand()) * 13;
    out.push(ellipse(50 + Math.cos(a) * r0, 50 + Math.sin(a) * r0 * 0.42, between(rand, 1.6, 3), between(rand, 0.9, 1.5), { sw: 1.1, op: 0.45 }));
  }
  // 芝麻
  out.push(dots(rand, 50, 50, 15, 5, 1.1));
  return out.join('');
}

// 烧烤串：斜签 + 串肉
function skewer(rand) {
  const out = [plate(30, 66)];
  out.push(path('M26 78L74 24', { sw: 2 }));
  const pos = [[36, 68], [45, 58], [54, 48], [63, 38]];
  for (const [x, y] of pos) out.push(block(x, y, 9, 8, -45, rand, { sw: 1.9, highlight: false }));
  out.push(dots(rand, 50, 52, 16, 5, 1.1));
  return out.join('');
}

// 火锅 / 干锅：锅体 + 烟囱 + 周围食材
function hotpot(rand, v) {
  const out = [];
  out.push(ellipse(50, 66, 34, 8, { sw: 2.2 }));
  out.push(
    path('M18 56q1 16 32 16q31 0 32 -16', { sw: 2.4 }),
    ellipse(50, 56, 32, 10, { sw: 2.4 }),
    ellipse(50, 56, 22, 6.5, { sw: 1.4, op: 0.5 }),
  );
  // 烟囱
  out.push(
    path('M44 50L42 30h16l-2 20', { sw: 2 }),
    ellipse(50, 30, 8, 3, { sw: 1.8 }),
    steam(50, 26, 12, 2),
  );
  // 把手
  out.push(path('M16 54q-8 0 -8 6', { sw: 1.8 }), path('M84 54q8 0 8 6', { sw: 1.8 }));
  // 食材
  const items = v % 2 === 0 ? 4 : 3;
  for (let i = 0; i < items; i++) {
    const a = (i / items) * Math.PI * 2 + 0.6;
    out.push(block(50 + Math.cos(a) * 19, 54 + Math.sin(a) * 5.5, 7, 5, 0, rand, { sw: 1.6, highlight: false }));
  }
  out.push(chili(68, 50, 9, 20), chili(32, 52, 8, 200));
  return out.join('');
}

// 甜点：小碟 + 圆形糕 + 装饰
function dessert(rand, v) {
  const out = [plate(29, 66)];
  if (v % 2 === 0) {
    out.push(circle(50, 54, 15, { sw: 2.3 }), circle(50, 54, 9, { sw: 1.3, op: 0.5 }));
    out.push(circle(50, 44, 4.2, { fill: 'ACCENT', c: 'INK', sw: 1.4 }));
    out.push(path('M50 40q4 -5 8 -4', { sw: 1.4 }));
    for (let i = 0; i < 6; i++) {
      const a = (i / 6) * Math.PI * 2;
      out.push(circle(50 + Math.cos(a) * 12, 54 + Math.sin(a) * 12, 1.5, { sw: 1, op: 0.5 }));
    }
  } else {
    // 切块蛋糕
    out.push(path('M34 60L50 66L66 58L50 52Z', { sw: 2.2 }), path('M34 60L34 48L50 42L50 52Z', { sw: 2.2 }), path('M66 58L66 46L50 40L50 52Z', { sw: 2.2 }));
    out.push(path('M34 48L50 42L66 46L50 40Z', { fill: 'ACCENT', c: 'INK', sw: 1.4 }));
    out.push(circle(50, 36, 3.6, { fill: 'ACCENT', c: 'INK', sw: 1.4 }));
  }
  return out.join('');
}

// 饮品：杯 / 壶
function drink(rand, v) {
  const out = [];
  if (v % 2 === 0) {
    out.push(ellipse(50, 70, 20, 5, { sw: 2 }));
    out.push(path('M36 34L38 68q12 5 24 0L64 34', { sw: 2.3 }), ellipse(50, 34, 14, 4, { sw: 2 }));
    out.push(ellipse(50, 46, 12.5, 3.4, { sw: 1.3, op: 0.5 }));
    out.push(path('M58 24q4 -6 10 -4', { sw: 1.4, op: 0.6 }));
    for (let i = 0; i < 4; i++) out.push(circle(between(rand, 42, 58), between(rand, 52, 64), between(rand, 1, 1.8), { sw: 1, op: 0.5 }));
  } else {
    // 酒壶
    out.push(ellipse(50, 72, 18, 4.5, { sw: 2 }));
    out.push(path('M40 66q-8 -10 -2 -22q4 -8 12 -8q8 0 12 8q6 12 -2 22q-10 4 -20 0Z', { sw: 2.3 }));
    out.push(path('M46 36l1 -7h6l1 7', { sw: 2 }), ellipse(50, 29, 4, 1.6, { sw: 1.6 }));
    out.push(path('M44 48q6 -3 12 0', { sw: 1.3, op: 0.5 }));
    out.push(path('M66 46q9 -4 7 6q-2 8 -8 6', { sw: 2 }));
  }
  return out.join('');
}

// 通配：盘 + 一块主料 + 点缀
function generic(rand) {
  const out = [plate(33, 62)];
  out.push(block(50, 56, 22, 15, -6, rand), block(40, 64, 12, 8, 10, rand), block(62, 64, 11, 7, -12, rand));
  out.push(leafShape(64, 50, 11, -40, { sw: 1.6, vein: false }), dots(rand, 50, 58, 15, 4, 1.2));
  return out.join('');
}

const KINDS = {
  pork, beef, chicken, fish, shrimp, crab, shellfish,
  veg, mushroom, tofu, egg, salad,
  noodle, rice, soup, dumpling, pancake, skewer, hotpot,
  dessert, drink, generic,
};

const KINDS_VARIANTS = { fish: 2, veg: 2, noodle: 2, egg: 2, hotpot: 2, dessert: 2, drink: 2 };


/* ==================== js/art/index.js ==================== */
/* ============================================================
 * art/index.js — 插图引擎分发层
 *  1. inferKind()  菜名 → 食材类别
 *  2. buildArt()   类别 + 种子 → 内联 svg 片段
 *  3. sanitizeArt() 外部传入 SVG 的白名单清洗
 *  4. applyTokens() 颜色 token → 主题真实色值
 * ============================================================ */




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

// 煲类菜里出现这些字时，说明是主料而非清汤
const MAIN_INGREDIENT = /牛|羊|猪|鸡|鸭|鹅|鱼|虾|蟹|排骨|五花|腩|肠/;

// 按优先级排列：形态类先于食材类，避免「牛肉面」被判成牛肉
const RULES = [
  ['drink', /酒|茶|醋饮|汁|露|咖啡|奶茶|可乐|酸梅|柠檬水|气泡|苏打|豆浆|米浆|酸奶|汽水|啤酒|米酒|白酒|黄酒/],
  ['hotpot', /火锅|干锅|麻辣香锅|冒菜|麻辣烫|锅底|毛血旺|涮/],
  ['noodle', /面|粉|米线|河粉|粉丝|馄饨面|乌冬|意面|拉条|拌面|炒面|焖面|凉皮|凉面/],
  ['soup', /汤|羹|粥|煲$|例汤|炖盅/],
  ['rice', /饭|煲仔|盖浇|米$|寿司|饭团/],
  ['dumpling', /饺|包$|包子|馄饨|抄手|烧麦|云吞|汤圆|元宵|烧卖/],
  ['pancake', /饼|馍|粑|锅贴|煎包|酥|油条|春卷/],
  ['skewer', /串|烧烤|烤羊肉|烤鸡翅|烤蔬/],
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

function inferKind(name = '', tags = []) {
  const clean = String(name).replace(/[\s（）()【】\-—_]/g, '');
  for (const key in EXACT) {
    if (clean.includes(key)) return EXACT[key];
  }
  for (const [kind, re] of RULES) {
    if (!re.test(clean)) continue;
    // 「牛腩煲」「鸡煲」这类砂锅菜，主料优先于器皿，否则会被判成清汤
    if (kind === 'soup' && /煲$/.test(clean) && MAIN_INGREDIENT.test(clean)) continue;
    return kind;
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
function artInner(kind, seedStr) {
  const draw = KINDS[kind] || KINDS.generic;
  const h = hash(seedStr || kind);
  const rand = rng(h);
  const variants = KINDS_VARIANTS[kind] || 1;
  const variant = h % variants;
  try {
    return draw(rand, variant, seedStr);
  } catch (e) {
    console.warn('[art] 画法失败，回退通用图形：', kind, e);
    return KINDS.generic(rng(1), 0);
  }
}

/** 颜色 token 替换为真实色值 */
function applyTokens(fragment, theme) {
  const map = { INK: theme.ink, ACCENT: theme.accent, MUTE: theme.ink };
  return fragment
    .replace(/\bINK\b/g, map.INK)
    .replace(/\bACCENT\b/g, map.ACCENT)
    .replace(/\bMUTE\b/g, map.MUTE);
}

/** 输出可独立使用的完整 <svg> 字符串 */
function buildArt(dish, theme) {
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
function sanitizeArt(svg) {
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




/* ==================== js/measure.js ==================== */
/* ============================================================
 * measure.js — 文本测量与折行
 * SVG 没有自动折行，必须在排版阶段自己算。这里用字符宽度模型：
 * CJK 按 1 个字宽，西文按 0.55 左右，并对窄字符单独处理。
 * ============================================================ */

const NARROW = /[iIlj.,:;'!|']/;
const WIDE = /[mwMW@%]/;

/** 单字符相对字号的宽度系数 */
function charRatio(ch) {
  const code = ch.codePointAt(0);
  // CJK、全角标点、假名、谚文
  if (
    (code >= 0x4e00 && code <= 0x9fff) ||
    (code >= 0x3000 && code <= 0x303f) ||
    (code >= 0xff00 && code <= 0xffef) ||
    (code >= 0x3040 && code <= 0x30ff) ||
    (code >= 0xac00 && code <= 0xd7af)
  ) return 1;
  if (ch === ' ') return 0.3;
  if (NARROW.test(ch)) return 0.3;
  if (WIDE.test(ch)) return 0.85;
  if (/[0-9]/.test(ch)) return 0.55;
  if (/[a-zA-Z]/.test(ch)) return 0.56;
  return 0.5;
}

/** 估算一行文本宽度 */
function measureText(str, fontSize) {
  if (!str) return 0;
  let w = 0;
  for (const ch of String(str)) w += charRatio(ch) * fontSize;
  return w;
}

/** 切成排版 token：CJK 单字、西文单词、空格 */
function tokenize(str) {
  const tokens = [];
  let buf = '';
  for (const ch of str) {
    const code = ch.codePointAt(0);
    const isCJK =
      (code >= 0x4e00 && code <= 0x9fff) ||
      (code >= 0x3000 && code <= 0x303f) ||
      (code >= 0xff00 && code <= 0xffef) ||
      (code >= 0x3040 && code <= 0x30ff);
    if (isCJK) {
      if (buf) { tokens.push(buf); buf = ''; }
      tokens.push(ch);
    } else if (ch === ' ') {
      if (buf) { tokens.push(buf); buf = ''; }
      tokens.push(' ');
    } else {
      buf += ch;
    }
  }
  if (buf) tokens.push(buf);
  return tokens;
}

/** 贪心折行 */
function wrapText(str, maxWidth, fontSize) {
  const s = String(str || '').trim();
  if (!s) return [];
  if (maxWidth <= 0) return [s];
  const lines = [];
  let line = '';
  let w = 0;
  for (const t of tokenize(s)) {
    const tw = measureText(t, fontSize);
    if (w + tw > maxWidth + 0.01 && line.trim()) {
      lines.push(line.replace(/\s+$/, ''));
      line = t === ' ' ? '' : t;
      w = measureText(line, fontSize);
    } else {
      line += t;
      w += tw;
    }
  }
  if (line.trim()) lines.push(line.replace(/\s+$/, ''));
  return lines;
}

/** 折行并限制行数，超出部分以省略号收尾 */
function wrapClamp(str, maxWidth, fontSize, maxLines) {
  const all = wrapText(str, maxWidth, fontSize);
  if (all.length <= maxLines) return { lines: all, truncated: false };
  const kept = all.slice(0, maxLines);
  let last = kept[maxLines - 1];
  while (last.length > 1 && measureText(`${last}…`, fontSize) > maxWidth) {
    last = last.slice(0, -1);
  }
  kept[maxLines - 1] = `${last.replace(/[，、。；：,.;:]$/, '')}…`;
  return { lines: kept, truncated: true };
}

/** 金额/价格的显示宽度（用于右侧对齐） */
const priceWidth = (price, fontSize) => measureText(String(price || ''), fontSize);


/* ==================== js/model.js ==================== */
/* ============================================================
 * model.js — 菜单数据模型
 * 菜品是结构化数据，SVG 只是渲染结果。这一层不碰任何 DOM。
 * ============================================================ */

/** 纸张与版心尺寸（单位与 SVG viewBox 一致） */
const PAPER = {
  width: 880,
  marginX: 76,
  padTop: 96,
  padBottom: 108,
  maxHeight: 4200,
};

/** 尺寸令牌 */
const SZ = {
  artNormal: 88,
  artSignature: 216,
  artTextGap: 20,
  priceW: 92,
  rowGap: 26,
  sectionGap: 34,
  signatureGap: 40,
};

/** 字体阶梯 */
const FS = {
  shopName: 44,
  shopNameAlt: 15,
  sectionTitle: 20,
  dishName: 21,
  dishNameSig: 34,
  blurb: 13.5,
  tags: 12,
  price: 19,
  priceSig: 22,
  footer: 12.5,
  seal: 15,
};

/** 主题预设：纸 / 墨 / 点缀 */
const THEMES = {
  rice: {
    id: 'rice', label: '米白宣纸',
    paper: '#faf6ec', ink: '#2b2622', accent: '#b4472f',
    edge: '#e6ddc9', noise: 0.5,
  },
  kraft: {
    id: 'kraft', label: '牛皮纸',
    paper: '#e8d9bd', ink: '#3a2d1e', accent: '#7a5c2e',
    edge: '#d3bf9a', noise: 0.75,
  },
  moss: {
    id: 'moss', label: '松烟墨绿',
    paper: '#eef0e6', ink: '#1f2a22', accent: '#4a6b46',
    edge: '#d6dbcb', noise: 0.4,
  },
  indigo: {
    id: 'indigo', label: '靛青',
    paper: '#f2f4f7', ink: '#1c2b3a', accent: '#2f5d8c',
    edge: '#dbe2ea', noise: 0.35,
  },
  clay: {
    id: 'clay', label: '陶土',
    paper: '#f6ece2', ink: '#33231c', accent: '#a85434',
    edge: '#e4d3c4', noise: 0.6,
  },
};

const THEME_LIST = Object.values(THEMES);

let seq = 1;
const uid = (prefix = 'd') => `${prefix}${(seq++).toString(36)}${Math.random().toString(36).slice(2, 5)}`;

/** 空白菜品 */
function blankDish(patch = {}) {
  return {
    id: uid('d'),
    section: '主菜',
    name: '',
    name_original: '',
    romanization: '',
    price: '',
    blurb: '',
    tags: [],
    signature: false,
    signature_note: '',
    kind: '',
    art: '',
    ...patch,
  };
}

/** 空白菜单 */
function blankMenu(patch = {}) {
  return {
    schema: 1,
    id: uid('m'),
    name: '',
    name_original: '',
    subtitle: '',
    footer: '',
    seal: '',
    theme: 'rice',
    dishes: [],
    createdAt: Date.now(),
    updatedAt: Date.now(),
    ...patch,
  };
}

/** 取主题，未命中回落到米白 */
const themeOf = (menu) => THEMES[menu?.theme] || THEMES.rice;

/* ---------------- 菜单操作（纯函数，返回新对象） ---------------- */

function addDish(menu, dish) {
  const d = blankDish(dish);
  // 没有指定分节时，沿用最后一道菜的分节
  if (!dish.section && menu.dishes.length) {
    d.section = menu.dishes[menu.dishes.length - 1].section;
  }
  return touch({ ...menu, dishes: [...menu.dishes, d] });
}

function updateDish(menu, id, patch) {
  const i = menu.dishes.findIndex((d) => d.id === id);
  if (i < 0) return menu;
  const next = menu.dishes.slice();
  next[i] = { ...next[i], ...patch, id };
  return touch({ ...menu, dishes: next });
}

function removeDish(menu, id) {
  return touch({ ...menu, dishes: menu.dishes.filter((d) => d.id !== id) });
}

function moveDish(menu, id, delta) {
  const i = menu.dishes.findIndex((d) => d.id === id);
  const j = i + delta;
  if (i < 0 || j < 0 || j >= menu.dishes.length) return menu;
  const next = menu.dishes.slice();
  [next[i], next[j]] = [next[j], next[i]];
  return touch({ ...menu, dishes: next });
}

const touch = (menu) => ({ ...menu, updatedAt: Date.now() });

/** 菜品统计 */
function stats(menu) {
  const dishes = menu.dishes || [];
  const sigs = dishes.filter((d) => d.signature);
  const prices = dishes
    .map((d) => parseFloat(String(d.price).replace(/[^\d.]/g, '')))
    .filter((v) => !Number.isNaN(v));
  return {
    count: dishes.length,
    signatureCount: sigs.length,
    minPrice: prices.length ? Math.min(...prices) : null,
    maxPrice: prices.length ? Math.max(...prices) : null,
    sections: [...new Set(dishes.map((d) => d.section).filter(Boolean))],
  };
}


/* ==================== js/layout.js ==================== */
/* ============================================================
 * layout.js — 排版计算
 * 输入菜单数据，输出一份带绝对坐标的绘图指令表（blocks）。
 * 这一层只算不动手画，渲染层照着 coordinates 画就行。
 * ============================================================ */




/**
 * @typedef {{type:string}} Block
 * @returns {{width:number, height:number, blocks:Block[], theme:object}}
 */
function layoutMenu(menu) {
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


/* ==================== js/render.js ==================== */
/* ============================================================
 * render.js — SVG 渲染
 * 拿着 layout 给出的坐标表逐条绘制。没有布局逻辑在这里。
 * ============================================================ */





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
function renderMenu(menu, opt = {}) {
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
function exportSvg(menu) {
  return renderMenu(menu).svg;
}


/* ==================== js/inspect.js ==================== */
/* ============================================================
 * inspect.js — 自动质检
 * 把「看起来对不对」翻译成可计算的检查：包围盒、元素数、
 * 行数、对比度、色距、重复度。返回 error / warn 两级问题。
 * ============================================================ */






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
function contrastRatio(a, b) {
  const l1 = luminance(a), l2 = luminance(b);
  const [hi, lo] = l1 > l2 ? [l1, l2] : [l2, l1];
  return (hi + 0.05) / (lo + 0.05);
}

/** 色差（RGB 欧氏距离，0-441） */
function colorDistance(a, b) {
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

function inspectMenu(menu) {
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


/* ==================== js/parse.js ==================== */
/* ============================================================
 * parse.js — 文字菜单解析 + 内置菜品词典
 * 用途：不依赖任何 AI 服务，把用户粘贴的一段文字菜单
 * 变成结构化菜品，并自动补上口味标签与一句话说明。
 * ============================================================ */

const D = (kind, tags, blurb) => ({ kind, tags: tags ? tags.split(',') : [], blurb });

/**
 * 常用菜词典。key 为菜名，值是类别 / 标签 / 默认说明。
 * 说明文案刻意写成「食材 + 做法 + 口感」，避免空话。
 */
const DICT = {
  /* --- 凉菜 --- */
  拍黄瓜: D('salad', '爽脆,清口', '黄瓜拍裂更入味，蒜末香醋一拌，最先上桌也最先光盘。'),
  口水鸡: D('chicken', '麻辣,凉菜', '鸡肉浸得嫩，红油浮着一层芝麻，麻在前辣在后。'),
  夫妻肺片: D('beef', '麻辣,凉菜', '牛肉牛杂切得薄，红油拌得透，嚼起来有韧劲。'),
  凉拌木耳: D('mushroom', '爽脆,素', '木耳焯过水，拌上小米辣和香菜，脆得响。'),
  皮蛋豆腐: D('tofu', '凉菜,清淡', '嫩豆腐托着皮蛋，淋一勺酱油膏，凉着吃最舒服。'),
  酱牛肉: D('beef', '卤味,下酒', '牛腱子卤足一夜，切片带筋，越嚼越香。'),
  拌三丝: D('salad', '清爽,素', '土豆丝、胡萝卜丝、青椒丝，酸辣开胃。'),
  卤味拼盘: D('pork', '卤味,下酒', '豆干、鸡蛋、鸭胗一锅卤，越泡越入味。'),

  /* --- 猪肉 --- */
  红烧肉: D('pork', '肥而不腻,家常', '五花肉慢炖两小时，糖色收得透亮，筷子一夹就颤。'),
  东坡肉: D('pork', '酥烂,浓香', '整块方肉以草绳捆住，黄酒代水焖到酥，肥处透明。'),
  回锅肉: D('pork', '咸香,微辣', '二刀肉先煮后炒，豆瓣酱煸出红油，配蒜苗段。'),
  梅菜扣肉: D('pork', '咸香,软糯', '梅干菜吸饱肉汁，肉片铺成扇形，倒扣上桌。'),
  糖醋里脊: D('pork', '酸甜,外脆', '里脊挂糊炸两遍，糖醋汁裹得亮，咬开还有声。'),
  锅包肉: D('pork', '酸甜,酥', '肉片薄而大，炸到金黄起泡，酸甜汁一浇滋啦响。'),
  鱼香肉丝: D('pork', '酸甜微辣,下饭', '泡椒、姜蒜、糖醋调成鱼香汁，肉丝滑嫩带汁。'),
  小炒肉: D('pork', '香辣,下饭', '五花肉片煸出油，螺丝椒猛火快炒，锅气足。'),
  京酱肉丝: D('pork', '咸甜,包着吃', '甜面酱炒肉丝，配葱丝用豆腐皮卷起来吃。'),
  咕噜肉: D('pork', '酸甜,酥', '肉块炸脆裹糖醋，配菠萝青椒，酸甜里带果香。'),
  蒜泥白肉: D('pork', '蒜香,微辣', '白煮肉切得极薄，蒜泥红油一浇，肥而不腻。'),
  粉蒸肉: D('pork', '软糯,咸香', '肉片裹米粉上笼蒸，底下垫着红薯，甜咸交融。'),
  排骨: D('pork', '家常', '带骨带肉，炖到脱骨，汤汁拌饭最好。'),
  红烧排骨: D('pork', '咸甜,家常', '排骨焯水后炒糖色，收汁到油亮，啃起来带甜。'),
  椒盐排骨: D('pork', '咸香,酥', '排骨炸到外壳酥，椒盐一撒，越嚼越香。'),
  腊肉炒蒜苗: D('pork', '咸香,烟熏', '腊肉切薄片煸出油，蒜苗下锅一翻就好。'),

  /* --- 牛羊肉 --- */
  小炒黄牛肉: D('beef', '鲜辣,下饭', '黄牛肉逆纹切薄，小米辣猛火快炒，嫩得能掐出水。'),
  黑椒牛柳: D('beef', '黑椒,嫩', '牛柳滑油，黑椒汁裹匀，配洋葱丝。'),
  水煮牛肉: D('beef', '麻辣,重口', '牛肉片滑嫩，铺在豆芽上，热油泼辣椒面。'),
  番茄牛腩: D('beef', '酸甜,软烂', '牛腩炖到用勺就能断，番茄熬成浓汤。'),
  孜然羊肉: D('beef', '孜然,香', '羊肉片大火爆炒，孜然辣椒面裹满，一点不膻。'),
  烤羊排: D('beef', '炭香,外焦', '羊排腌足味，烤到边缘焦脆，撒一把孜然。'),
  牛排: D('beef', '西式,嫩', '厚切煎至表面焦褐，切面粉红，配黑椒汁。'),

  /* --- 禽类 --- */
  宫保鸡丁: D('chicken', '酸甜微辣,经典', '鸡丁滑嫩，花生米还脆，荔枝口的汁挂得住。'),
  辣子鸡: D('chicken', '麻辣,干香', '鸡块炸到干香，藏在满盘辣椒里，越翻越有。'),
  白切鸡: D('chicken', '原味,嫩', '整鸡浸熟过冰水，皮爽肉滑，蘸姜葱蓉。'),
  三杯鸡: D('chicken', '酱香,微甜', '一杯酒一杯酱油一杯麻油，收汁到浓稠。'),
  黄焖鸡: D('chicken', '酱香,下饭', '鸡块焖到酥，汤汁浓，拌米饭吃最实在。'),
  可乐鸡翅: D('chicken', '甜咸,家常', '鸡翅煎出油，可乐收汁，甜得讨小孩喜欢。'),
  烤鸭: D('chicken', '皮脆,经典', '片皮鸭皮脆如纸，配葱丝黄瓜条卷饼。'),
  啤酒鸭: D('chicken', '浓香,微辣', '鸭块爆炒后用啤酒焖，酒气散尽只留香。'),
  口水鸭: D('chicken', '麻辣,凉菜', '鸭肉紧实，红油浸透，越嚼越出味。'),

  /* --- 水产 --- */
  清蒸鲈鱼: D('fish', '鲜,清淡', '鲈鱼打刀上锅八分钟，淋豉油泼热油，肉一瓣一瓣。'),
  酸菜鱼: D('fish', '酸辣,开胃', '鱼片滑嫩，酸菜熬出白汤，汤比鱼还抢手。'),
  水煮鱼: D('fish', '麻辣,重口', '鱼片铺满热油辣椒，捞起来还在滴红油。'),
  松鼠鳜鱼: D('fish', '酸甜,宴客', '鱼身切花刀炸成松鼠形，浇汁时滋滋作响。'),
  红烧鱼: D('fish', '咸鲜,家常', '鱼两面煎黄，酱油糖收汁，最家常的做法。'),
  剁椒鱼头: D('fish', '鲜辣,湘菜', '胖头鱼头铺满剁椒蒸透，肉嫩，汤汁拌面一流。'),
  烤鱼: D('fish', '香辣,聚餐', '整鱼烤到皮焦，垫底配菜吸满汤汁。'),
  小龙虾: D('shrimp', '麻辣,宵夜', '虾壳红亮，肉弹，剥起来手上全是料汁。'),
  白灼虾: D('shrimp', '鲜甜,清淡', '活虾下锅变色即捞，蘸姜醋，吃的就是甜。'),
  油焖大虾: D('shrimp', '咸甜,浓', '虾壳煎出红油，糖醋汁收到发亮，壳都能嚼。'),
  蒜蓉粉丝蒸扇贝: D('shellfish', '蒜香,鲜', '扇贝铺粉丝，蒜蓉一浇蒸六分钟，粉丝比贝好吃。'),
  爆炒花蛤: D('shellfish', '鲜辣,下酒', '花蛤吐净沙，猛火爆炒到开口，汤汁咸鲜。'),
  香辣蟹: D('crab', '香辣,宴客', '蟹块炸过再炒，壳脆肉甜，配年糕吸汁。'),
  清蒸大闸蟹: D('crab', '原味,时令', '蟹肚朝上蒸，配姜醋，拆开满是黄。'),

  /* --- 蔬菜 --- */
  干煸四季豆: D('veg', '干香,微辣', '四季豆煸到起皱，肉末芽菜一并炒香。'),
  清炒时蔬: D('veg', '清淡,当季', '当日绿叶菜大火快炒，只放盐，吃个脆嫩。'),
  蒜蓉菠菜: D('veg', '蒜香,素', '菠菜焯水去涩，蒜末爆香一拌，绿得发亮。'),
  上汤娃娃菜: D('veg', '鲜甜,清淡', '娃娃菜浸在上汤里，配皮蛋咸蛋，汤鲜菜甜。'),
  手撕包菜: D('veg', '干香,微辣', '包菜手撕更挂汁，五花肉煸油，干辣椒提味。'),
  地三鲜: D('veg', '咸香,下饭', '土豆茄子青椒过油再烧，酱汁浓得裹住每一块。'),
  鱼香茄子: D('veg', '酸甜微辣,下饭', '茄子先炸后烧，鱼香汁收浓，拌饭一绝。'),
  干锅花菜: D('veg', '干香,微辣', '花菜煸到边缘焦，配腊肉片，越吃越香。'),
  醋溜土豆丝: D('veg', '酸辣,爽脆', '土豆丝过水去淀粉，白醋一激，脆得响。'),
  蚝油生菜: D('veg', '鲜,快炒', '生菜下锅十秒即起，蚝油汁淋上，脆生生。'),
  麻婆豆腐: D('tofu', '麻辣,下饭', '嫩豆腐不碎，牛肉末炒香，花椒面撒在最后。'),
  家常豆腐: D('tofu', '咸香,家常', '豆腐煎至两面金黄，配青蒜木耳烧透。'),

  /* --- 菌菇蛋 --- */
  香菇滑鸡: D('mushroom', '鲜香,嫩', '香菇泡发留汁，鸡块同蒸，菌香渗进肉里。'),
  干锅茶树菇: D('mushroom', '干香,微辣', '茶树菇撕条煸干，配五花肉，越嚼越有味。'),
  番茄炒蛋: D('egg', '酸甜,家常', '番茄炒出沙，蛋块裹上汁，糖要比盐多一点。'),
  韭菜炒蛋: D('egg', '鲜香,快炒', '韭菜断生即起，鸡蛋滑嫩，香气冲。'),
  蒸水蛋: D('egg', '嫩滑,清淡', '蛋液过筛，温水比例一比一五，蒸出镜面。'),

  /* --- 主食 --- */
  蛋炒饭: D('rice', '干香,经典', '隔夜饭粒粒分明，蛋液裹住每颗米，锅气足。'),
  扬州炒饭: D('rice', '鲜,料足', '虾仁叉烧青豆一并下锅，米粒金黄不黏。'),
  煲仔饭: D('rice', '锅巴,香', '腊味铺在米上焖熟，底下一层焦脆锅巴。'),
  卤肉饭: D('rice', '咸甜,下饭', '五花肉丁卤到起胶，浇在热饭上，配半颗卤蛋。'),
  牛肉面: D('noodle', '浓汤,饱腹', '牛骨汤熬足六小时，面条筋道，牛肉切厚片。'),
  酸辣粉: D('noodle', '酸辣,开胃', '红薯粉滑弹，酸辣汤底，花生碎和香菜盖顶。'),
  热干面: D('noodle', '芝麻酱,干香', '碱水面拌芝麻酱，萝卜丁酸豆角，越拌越香。'),
  炸酱面: D('noodle', '酱香,家常', '黄酱甜面酱炒肉丁，配黄瓜丝豆芽，自己拌。'),
  葱油拌面: D('noodle', '葱香,简单', '小葱熬到焦，葱油拌面，一勺酱油就够。'),
  小笼包: D('dumpling', '汤汁,鲜', '皮薄能看见汤，提起来不破，先咬一个小口。'),
  猪肉白菜饺: D('dumpling', '家常,鲜', '白菜挤干水，猪肉打上劲，煮到浮起来。'),
  生煎包: D('dumpling', '底脆,汤汁', '底部煎成金黄脆壳，上面撒芝麻葱花。'),
  葱油饼: D('pancake', '酥,葱香', '面团抹油卷起再擀，煎到层层起酥。'),
  肉夹馍: D('pancake', '酥脆,扎实', '白吉馍烤到边脆，腊汁肉剁碎塞满。'),
  烤串: D('skewer', '炭香,孜然', '羊肉肥瘦相间，炭火烤到滴油，孜然辣椒面撒满。'),

  /* --- 汤羹 --- */
  番茄蛋汤: D('soup', '酸甜,家常', '番茄炒出红汁加水，蛋液拉成蛋花，撒葱花。'),
  紫菜蛋花汤: D('soup', '清淡,快', '水开下紫菜，蛋液转圈淋入，滴两滴香油。'),
  冬瓜排骨汤: D('soup', '清甜,去火', '排骨焯水慢炖，冬瓜后放，汤清不腻。'),
  酸辣汤: D('soup', '酸辣,开胃', '豆腐丝木耳笋丝，胡椒和醋在最后调。'),
  佛跳墙: D('soup', '浓,宴客', '鲍鱼海参花胶同煨，汤浓得挂勺。'),

  /* --- 甜品饮品 --- */
  杨枝甘露: D('dessert', '芒果,冰凉', '芒果西柚椰浆，底下藏着西米，甜而不腻。'),
  双皮奶: D('dessert', '奶香,嫩', '水牛奶结两层皮，勺子挖下去会颤。'),
  红豆沙: D('dessert', '绵密,温', '红豆煮到起沙，加陈皮解腻，热吃最舒服。'),
  红糖糍粑: D('dessert', '软糯,甜', '糍粑煎到外脆，红糖浆一浇，撒黄豆粉。'),
  酸梅汤: D('drink', '解腻,冰', '乌梅山楂陈皮熬煮，冰镇后酸甜生津。'),
  柠檬水: D('drink', '清爽,酸', '鲜柠檬片泡冷水，微酸带回甘。'),
  精酿啤酒: D('drink', '麦香,微苦', '麦芽香重，苦度适中，配肉最合适。'),
  桂花米酒: D('drink', '甜,微醺', '糯米酿的甜酒，撒一把干桂花，冰着喝。'),

  /* --- 家常补充：面饭、蛋、小吃、西式 --- */
  番茄鸡蛋面: D('noodle', '家常,酸甜', '番茄炒出沙，鸡蛋滑成块，汤头酸甜带蛋香。'),
  卤蛋: D('egg', '卤香,入味', '鸡蛋卤到蛋白发褐，切开蛋黄还溏着。'),
  蒜蓉粉丝扇贝: D('shellfish', '蒜香,鲜', '扇贝上铺粉丝，蒜蓉一勺，蒸到汤汁冒泡。'),
  可乐: D('drink', '冰,甜', '冰镇过的可乐，气足，解辣最好用。'),
  雪碧: D('drink', '冰,柠檬', '柠檬味汽水，冰到挂霜，喝完打个嗝。'),
  米饭: D('rice', '白口,配菜', '新米现焖，颗粒分明，配汤汁最合适。'),
  例汤: D('soup', '当日,清', '当天现煲的一锅，配餐送，喝完再添。'),
  炸鸡: D('chicken', '酥,多汁', '裹粉炸到外壳起鳞，咬开还冒汁。'),
  意面: D('noodle', '西式,番茄', '面条煮到有嚼劲，番茄肉酱裹匀。'),
  披萨: D('pancake', '西式,芝士', '薄底烤到边脆，芝士拉丝，趁热吃。'),
  沙拉: D('salad', '清爽,生', '生菜番茄现拌，油醋汁轻薄不糊口。'),
  三明治: D('pancake', '西式,便携', '面包夹肉和菜，压紧切开，一手能拿。'),
  咖喱饭: D('rice', '咖喱,浓', '咖喱块熬到稠，浇在热饭上，微辣回甜。'),
  牛肉粉: D('noodle', '鲜,汤好', '牛骨汤打底，粉滑汤清，撒一把香菜。'),
  羊肉串: D('skewer', '孜然,炭火', '肥瘦相间穿串，炭火上撒孜然辣椒面。'),
  毛血旺: D('hotpot', '麻辣,重口', '鸭血毛肚黄喉同煮，红油翻滚，越吃越辣。'),
  啤酒: D('drink', '冰,麦香', '冰镇到冒水珠，配烧烤最痛快。'),
  豆浆: D('drink', '豆香,温', '现磨黄豆煮开，微甜，配油条正好。'),
  布丁: D('dessert', '滑,奶香', '勺子一碰就颤，入口即化，焦糖微苦。'),
  蛋挞: D('dessert', '酥皮,蛋香', '酥皮层层起片，蛋液烤到表面带焦斑。'),
  麻辣牛肉: D('beef', '麻辣,干香', '牛肉片过油煸干，辣椒花椒炒香，越嚼越有味。'),
  铁板豆腐: D('tofu', '烫,香辣', '铁板烧到冒烟，豆腐贴上去滋滋响，浇汁上桌。'),
};

const dictLookup = (name) => {
  const key = String(name || '').replace(/[\s·・]/g, '');
  if (DICT[key]) return DICT[key];
  // 宽松匹配：菜名包含词典键（长出的部分不超过 3 字，避免「鸡」命中「宫保鸡丁」）
  for (const k in DICT) {
    if (key.length >= 2 && key.includes(k) && key.length - k.length <= 3) return DICT[k];
  }
  return null;
};

/* ---------------- 文字解析 ---------------- */

const PRICE_TAIL = /(?:[¥￥$]\s*)?(\d+(?:\.\d{1,2})?)\s*(元|块|份|例|位|两|斤|只|串|杯|壶)?\s*$/;
const SECTION_RE = /^(?:[【\[（(]\s*([^】\]）)]{1,8})\s*[】\]）)]|#{1,3}\s*(.+)|(.{1,8})(?:系列|菜单|类)\s*[:：]?)\s*$/;

/**
 * 解析一段文字菜单。
 * 支持：菜名 价格 / 菜名 ¥价格 / 菜名....价格 / 【分节】 / 菜名 价格 描述
 */
function parseTextMenu(text) {
  const lines = String(text || '').split(/\r?\n/);
  const dishes = [];
  let section = '';
  let shopName = '';

  for (const rawLine of lines) {
    let line = rawLine.trim();
    if (!line) continue;

    // 分节标题
    const sm = line.match(SECTION_RE);
    if (sm && !/\d/.test(sm[1] || sm[2] || '')) {
      section = (sm[1] || sm[2] || sm[3] || '').trim();
      continue;
    }

    // 店铺名：以「店/馆/楼/记/家/轩」结尾且很短，且不在行首带价格
    if (!dishes.length && !shopName && line.length <= 14 && /[店馆楼记家轩坊园居]$/.test(line)) {
      shopName = line;
      continue;
    }

    // 点多号 / 破折号当分隔
    line = line.replace(/[.．。·•\-—_…]{2,}/g, ' ').replace(/\s+/g, ' ').trim();

    const pm = line.match(PRICE_TAIL);
    let namePart = line;
    let price = '';
    let blurbHint = '';
    if (pm) {
      const num = pm[1];
      const unit = pm[2] || '';
      price = unit && !/[元块]/.test(unit) ? `${num}${unit}` : `${num}`;
      namePart = line.slice(0, pm.index).trim();
    } else {
      // 价格夹在中间：「菜名 48 描述」
      const mid = line.match(/^(.{2,22}?)\s+[¥￥]?(\d{1,4}(?:\.\d{1,2})?)\s*(?:元|块|份|例|位)?\s+(\S.{0,60})$/);
      if (mid) {
        namePart = mid[1].trim();
        price = mid[2];
        blurbHint = mid[3].trim();
      }
    }

    if (!namePart) continue;

    // 拆分菜名与描述
    let name = namePart;
    let blurb = '';
    const parts = namePart.split(/\s+/);
    if (parts.length > 1) {
      // 前半部分能在词典里命中，就当作菜名，其余当描述
      for (let k = Math.min(parts.length - 1, 3); k >= 1; k--) {
        const cand = parts.slice(0, k).join('');
        if (dictLookup(cand)) { name = cand; blurb = parts.slice(k).join(' '); break; }
      }
      if (name === namePart) {
        // 没命中词典：以第一个空格为界
        name = parts[0];
        blurb = parts.slice(1).join(' ');
      }
    }

    // 一行里塞了多道菜：按「数字+空格」再切
    if (!pm && /\d{1,4}\s+\S/.test(namePart) && namePart.split(/\s+/).length > 3) {
      const chunks = namePart.split(/(?<=\d)\s+(?=[\u4e00-\u9fa5])/);
      if (chunks.length > 1) {
        for (const c of chunks) {
          const sub = parseTextMenu(c);
          dishes.push(...sub.dishes.map((d) => ({ ...d, section })));
        }
        continue;
      }
    }

    name = name.replace(/^[、,，:：\-]+|[、,，:：]+$/g, '').trim();
    if (!name) continue;

    const hit = dictLookup(name);
    dishes.push({
      section,
      name,
      price,
      blurb: blurb || blurbHint || (hit ? hit.blurb : ''),
      tags: hit ? hit.tags : [],
      kind: hit ? hit.kind : '',
      signature: false,
      signature_note: '',
      name_original: '',
    });
  }

  return { shopName, dishes, sections: [...new Set(dishes.map((d) => d.section).filter(Boolean))] };
}

/** 从一段文字里嗅出可能的店名（首行不以价格结尾、不含数字） */
function sniffShopName(text) {
  const first = String(text || '').split(/\r?\n/).map((s) => s.trim()).find(Boolean);
  if (!first) return '';
  if (/\d/.test(first)) return '';
  if (first.length > 16) return '';
  return first;
}


/* ==================== js/store.js ==================== */
/* ============================================================
 * store.js — 本地存档
 * 用 localStorage 保存菜单列表；写入做防抖，避免每次工具调用都落盘。
 * 内置示例不写入存档，随时可重新打开。
 * ============================================================ */



const KEY = 'vivid-menu.v1';
const DEBOUNCE = 1500;

let saveTimer = null;
let lastPayload = null;

function read() {
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return { menus: [], activeId: null };
    const data = JSON.parse(raw);
    return { menus: Array.isArray(data.menus) ? data.menus : [], activeId: data.activeId || null };
  } catch (e) {
    console.warn('[store] 读取失败，按空存档处理', e);
    return { menus: [], activeId: null };
  }
}

function write(data) {
  try {
    localStorage.setItem(KEY, JSON.stringify(data));
    return true;
  } catch (e) {
    // 配额超限：丢掉图片再试一次
    console.warn('[store] 写入失败，尝试剥离图片后重试', e);
    try {
      const slim = {
        ...data,
        menus: data.menus.map((m) => ({ ...m, sourceImage: '' })),
      };
      localStorage.setItem(KEY, JSON.stringify(slim));
      return true;
    } catch (e2) {
      console.error('[store] 存档空间不足，本次不持久化', e2);
      return false;
    }
  }
}

const store = {
  list() {
    return read().menus;
  },

  get(id) {
    return read().menus.find((m) => m.id === id) || null;
  },

  activeId() {
    return read().activeId;
  },

  /** 写入或更新一条菜单（防抖） */
  save(menu, { immediate = false } = {}) {
    const payload = JSON.parse(JSON.stringify(menu));
    lastPayload = payload;
    const commit = () => {
      const data = read();
      const i = data.menus.findIndex((m) => m.id === payload.id);
      if (i >= 0) data.menus[i] = payload;
      else data.menus.unshift(payload);
      data.activeId = payload.id;
      write(data);
      saveTimer = null;
    };
    if (immediate) {
      if (saveTimer) { clearTimeout(saveTimer); saveTimer = null; }
      commit();
      return true;
    }
    if (saveTimer) clearTimeout(saveTimer);
    saveTimer = setTimeout(commit, DEBOUNCE);
    return true;
  },

  setActive(id) {
    const data = read();
    data.activeId = id;
    write(data);
  },

  remove(id) {
    const data = read();
    data.menus = data.menus.filter((m) => m.id !== id);
    if (data.activeId === id) data.activeId = data.menus[0]?.id || null;
    write(data);
  },

  clear() {
    try { localStorage.removeItem(KEY); } catch (e) { /* ignore */ }
  },

  /** 立即冲刷未落盘的改动 */
  flush() {
    if (saveTimer) { clearTimeout(saveTimer); saveTimer = null; if (lastPayload) this.save(lastPayload, { immediate: true }); }
  },
};

/* ============================================================
 * 内置示例：不打标记为"已保存"，只作为展示
 * ============================================================ */

const dish = (section, name, price, blurb, tags, kind, extra = {}) =>
  blankDish({ id: uid('s'), section, name, price, blurb, tags, kind, ...extra });

const PRESETS = [
  (() => {
    const m = blankMenu({
      id: uid('preset'),
      name: '巷子口·川味小馆',
      name_original: "XIANGZIKOU SICHUAN",
      subtitle: '二十年的老灶，辣得有分寸',
      footer: '本店所有菜品均使用当日现采食材 · 微辣可调 · 提供免费茶水',
      seal: '巷子口',
      theme: 'rice',
      dishes: [],
    });
    m.dishes = [
      dish('凉菜', '口水鸡', '38', '鸡肉浸得嫩，红油浮着一层芝麻，麻在前辣在后。', ['麻辣', '凉菜'], 'chicken'),
      dish('凉菜', '夫妻肺片', '48', '牛肉牛杂切得薄，红油拌得透，嚼起来有韧劲。', ['麻辣', '下酒'], 'beef'),
      dish('凉菜', '拍黄瓜', '18', '黄瓜拍裂更入味，蒜末香醋一拌，最先上桌也最先光盘。', ['爽脆', '清口'], 'salad'),
      dish('热菜', '水煮鱼', '98', '两斤半的草鱼现杀，鱼片滑嫩，热油泼在辣椒面上还在响。', ['麻辣', '镇店'], 'fish', {
        signature: true, signature_note: '开店二十年销量第一，几乎每桌必点',
      }),
      dish('热菜', '回锅肉', '56', '二刀肉先煮后炒，豆瓣酱煸出红油，配蒜苗段。', ['咸香', '微辣'], 'pork'),
      dish('热菜', '麻婆豆腐', '32', '嫩豆腐不碎，牛肉末炒香，花椒面撒在最后一道。', ['麻辣', '下饭'], 'tofu'),
      dish('热菜', '干煸四季豆', '28', '四季豆煸到起皱，肉末芽菜一并炒香。', ['干香'], 'veg'),
      dish('热菜', '辣子鸡', '68', '鸡块炸到干香，藏在满盘辣椒里，越翻越有。', ['麻辣', '干香'], 'chicken'),
      dish('主食', '酸辣粉', '22', '红薯粉滑弹，酸辣汤底，花生碎和香菜盖顶。', ['酸辣'], 'noodle'),
      dish('主食', '蛋炒饭', '26', '隔夜饭粒粒分明，蛋液裹住每颗米，锅气足。', ['干香'], 'rice'),
      dish('汤羹', '番茄蛋汤', '18', '番茄炒出红汁加水，蛋液拉成蛋花，撒葱花。', ['酸甜'], 'soup'),
    ];
    return m;
  })(),

  (() => {
    const m = blankMenu({
      id: uid('preset'),
      name: '夜灯小食堂',
      name_original: 'YODENG SHOKUDO',
      subtitle: '只做夜里十点以后的那一餐',
      footer: '深夜营业至凌晨两点 · 单人套餐可点半份 · 谢绝外带酒水',
      seal: '夜灯',
      theme: 'kraft',
      dishes: [],
    });
    m.dishes = [
      dish('先付', '枝豆', '16', '海盐搓过表皮的毛豆，焯三分钟，配冰啤酒。', ['清淡', '下酒'], 'veg'),
      dish('先付', '冷奴', '18', '嫩豆腐上放柴鱼片与姜末，淋一圈淡酱油。', ['清淡'], 'tofu'),
      dish('烤物', '炙烤鸡腿肉', '42', '备长炭直火烤，皮脆肉汁锁在里面，撒七味粉。', ['炭香', '招牌'], 'chicken', {
        signature: true, signature_note: '每晚最早卖完的一道，常客默认必点',
      }),
      dish('烤物', '盐烤鲭鱼', '46', '整条鲭鱼撒粗盐烤到皮起泡，配白萝卜泥。', ['炭香', '鲜'], 'fish'),
      dish('烤物', '酱烤鸡皮串', '22', '鸡皮刷三遍酱汁，烤到边缘微焦，越嚼越香。', ['酱香', '下酒'], 'skewer'),
      dish('煮物', '关东煮五品', '38', '萝卜、昆布、鱼豆腐、竹轮、鸡蛋，一锅清汤里煨着。', ['温', '清淡'], 'hotpot'),
      dish('主食', '茶泡饭', '24', '冷饭浇上煎茶，放一颗梅干和少许海苔丝。', ['清爽'], 'rice'),
      dish('酒水', '生啤', '26', '冰到起霜的杯子，泡沫三指厚。', ['冰', '麦香'], 'drink'),
      dish('酒水', '梅酒苏打', '32', '青梅酒兑苏打水，加一颗冰球，甜里带气泡。', ['甜', '微醺'], 'drink'),
      dish('甘味', '黑糖蕨饼', '20', '蕨饼裹黄豆粉，淋黑糖蜜，凉着吃。', ['软糯', '甜'], 'dessert'),
    ];
    return m;
  })(),

  (() => {
    const m = blankMenu({
      id: uid('preset'),
      name: '山间茶事',
      name_original: 'SHANJIAN TEAHOUSE',
      subtitle: '一席六味，随季节换单',
      footer: '每季仅设十二席 · 需提前一日预订 · 茶点随主茶搭配',
      seal: '山间',
      theme: 'moss',
      dishes: [],
    });
    m.dishes = [
      dish('茶点', '桂花米糕', '28', '新米磨浆蒸成，桂花糖浆淋面，凉透后切块。', ['软糯', '清甜'], 'dessert'),
      dish('茶点', '陈皮红豆酥', '32', '酥皮十六层，红豆沙里藏着陈皮丝，解腻。', ['酥', '甜'], 'dessert'),
      dish('茶', '炭焙乌龙', '68', '武夷山炭焙三道，汤色琥珀，回甘长。', ['炭焙', '回甘'], 'drink', {
        signature: true, signature_note: '主理人每年亲赴武夷山选料，仅存四十斤',
      }),
      dish('茶点', '咸蛋黄酥', '26', '咸蛋黄现磕，油润起沙，配浓茶正好。', ['咸香', '酥'], 'dessert'),
      dish('茶点', '青梅煮酒', '38', '青梅与黄酒小火煮开，姜片两片，微醺不上头。', ['温', '微醺'], 'drink'),
      dish('时令', '春笋腌笃鲜', '58', '春笋、咸肉、鲜五花同炖，汤白味厚。', ['鲜', '时令'], 'soup'),
    ];
    return m;
  })(),
];


/* ==================== js/protocol.js ==================== */
/* ============================================================
 * protocol.js — 9 个网页工具
 *
 * 设计要点：这一层只定义「能力」，不关心谁来调用。
 * 外部 Agent（WebMCP）和内置生成器调的是同一批 handler，
 * 所以两条路径不会出现逻辑分叉。
 * ============================================================ */







/* ---------------- 工具说明（给 Agent 看的画法规范） ---------------- */

const BRIEF = `# 生动菜单 · 绘制说明

你在为一个网页菜单应用工作。你的产出不是一张图片，而是**结构化菜品数据 + 每道菜的 SVG 线条插图**，由页面负责排版、质检和导出。

## 工作顺序
1. \`get_source\` 看有没有原图或文字；有原图就 \`zoom_source\` 局部放大，逐字辨认菜名和价格。
2. \`begin_menu\` 建一张纸，确定店名、纸张质感与点缀色。
3. 逐道 \`add_dish\`。**一次只加一道**，加完可以继续。
4. \`inspect_menu\` 检查，按返回的 issues 逐条 \`update_dish\` 修。
5. \`wait_for_user\` 等用户提新要求（换图、改文案、加菜）。

## 插图规范（art 字段）
- 视口固定 \`0 0 100 100\`，纯线条画，\`stroke-linecap="round"\`。
- 主描边 \`stroke-width\` 2~2.4，细节 1~1.3，不要用 fill 铺大面积。
- 颜色只允许三种 token：\`INK\`（墨）、\`ACCENT\`（点缀，仅用于辣椒/印章等小面积）、\`MUTE\`（淡）。
- 不要写 \`<svg>\` 外壳，只给内部图元。
- 一道菜 8~45 个图元为宜，太少了认不出，太多了缩到 88px 会糊。
- **留白**：四周至少留 8 单位，别顶到边。
- 如果没把握，可以不传 art，页面会自动用内置图形引擎按菜名生成。

## 内容规范
- 价格**照抄原图**。看不清就留空，绝不编造。
- 招牌菜必须给 \`signature_note\`，写明判断依据（销量、口碑、菜单上的标记）。
- 描述一句话，讲食材和口感，不要写"美味可口"这类空话。
- 菜名太长会被截断，超过 12 字要拆。

## 配色
${THEME_LIST.map((t) => `- \`${t.id}\` ${t.label}：纸 ${t.paper} / 墨 ${t.ink} / 点缀 ${t.accent}`).join('\n')}
`;

/* ---------------- 工具实现 ---------------- */

/**
 * @param {object} ctx 会话上下文
 * @param {() => object} ctx.getMenu 取当前菜单
 * @param {(m:object) => void} ctx.setMenu 写回菜单
 * @param {() => object} ctx.getSource 取原图/文字源
 * @param {(p:object) => void} ctx.pushEvent 记录一条用户事件
 */
function createToolset(ctx) {
  const ok = (data = {}) => ({ ok: true, ...data });
  const fail = (error, hint = '') => ({ ok: false, error, hint });

  const findDish = (menu, { id, name }) => {
    if (id) return menu.dishes.find((d) => d.id === id) || null;
    if (name) return menu.dishes.find((d) => d.name === name) || null;
    return null;
  };

  return {
    /* 1. 画法说明 */
    read_brief: {
      description: '读取绘制规范：插图怎么画、文案怎么写、有哪些配色可选。开工前先调用一次。',
      inputSchema: { type: 'object', properties: {} },
      handler: async () => ok({ brief: BRIEF }),
    },

    /* 2. 原图状态 */
    get_source: {
      description: '获取当前原始菜单的状态：是否有照片、尺寸、以及当前放大区域。',
      inputSchema: { type: 'object', properties: {} },
      handler: async () => {
        const s = ctx.getSource();
        return ok({
          hasPhoto: !!s.dataUrl,
          width: s.width || 0,
          height: s.height || 0,
          zoom: s.zoom || null,
          textHint: s.text ? s.text.slice(0, 2000) : '',
          note: s.dataUrl
            ? '照片在左侧显示。需要辨认细节时用 zoom_source 按归一化坐标放大。'
            : '还没有照片。可以请用户上传图片，或直接粘贴文字菜单。',
        });
      },
    },

    /* 3. 局部放大 */
    zoom_source: {
      description: '按归一化坐标（0~1）放大原图某一块，用于辨认菜名和价格。返回放大后的图片与区域。',
      inputSchema: {
        type: 'object',
        properties: {
          x: { type: 'number', description: '左边界，0~1' },
          y: { type: 'number', description: '上边界，0~1' },
          w: { type: 'number', description: '宽度，0~1' },
          h: { type: 'number', description: '高度，0~1' },
        },
        required: ['x', 'y', 'w', 'h'],
      },
      handler: async ({ x, y, w, h }) => {
        const s = ctx.getSource();
        if (!s.dataUrl) return fail('还没有上传照片', '请用户上传原菜单图片，或改用文字输入。');
        const clamp01 = (v) => Math.max(0, Math.min(1, Number(v) || 0));
        const box = {
          x: clamp01(x), y: clamp01(y),
          w: Math.max(0.02, Math.min(1 - clamp01(x), clamp01(w))),
          h: Math.max(0.02, Math.min(1 - clamp01(y), clamp01(h))),
        };
        const crop = await ctx.cropSource(box);
        return ok({ box, image: crop.dataUrl, pixelWidth: crop.width, pixelHeight: crop.height });
      },
    },

    /* 4. 新建菜单 */
    begin_menu: {
      description: '创建一张新菜单纸，确定店名与配色。会清空已有菜品。',
      inputSchema: {
        type: 'object',
        properties: {
          name: { type: 'string', description: '店名' },
          name_original: { type: 'string', description: '原文店名/罗马音，可留空' },
          subtitle: { type: 'string', description: '一句话副标题' },
          footer: { type: 'string', description: '页脚说明（营业时间、备注）' },
          seal: { type: 'string', description: '印章文字，2~4 字' },
          theme: { type: 'string', enum: THEME_LIST.map((t) => t.id), description: '纸张配色' },
        },
        required: ['name'],
      },
      handler: async (args) => {
        const menu = blankMenu({
          name: args.name || '未命名小馆',
          name_original: args.name_original || '',
          subtitle: args.subtitle || '',
          footer: args.footer || '',
          seal: (args.seal || '').slice(0, 4),
          theme: THEME_LIST.some((t) => t.id === args.theme) ? args.theme : 'rice',
        });
        ctx.setMenu(menu);
        return ok({ menuId: menu.id, theme: menu.theme, note: '纸张已建好，接下来用 add_dish 逐道加菜。' });
      },
    },

    /* 5. 加菜 */
    add_dish: {
      description: '添加一道菜。art 可选，不传则按菜名自动生成线条插图。',
      inputSchema: {
        type: 'object',
        properties: {
          section: { type: 'string', description: '分节，如「凉菜」「热菜」；留空则沿用上一道' },
          name: { type: 'string', description: '菜名' },
          name_original: { type: 'string', description: '原文菜名，可留空' },
          price: { type: 'string', description: '价格，照抄原图，别编造' },
          blurb: { type: 'string', description: '一句话说明，讲食材和口感' },
          tags: { type: 'array', items: { type: 'string' }, description: '口味标签，2 个以内' },
          signature: { type: 'boolean', description: '是否招牌菜' },
          signature_note: { type: 'string', description: '招牌依据' },
          kind: { type: 'string', description: '食材类别，不传则自动推断' },
          art: { type: 'string', description: 'SVG 内部图元，0 0 100 100 坐标系' },
        },
        required: ['name'],
      },
      handler: async (args) => {
        if (!args.name) return fail('缺少菜名');
        const menu = ctx.getMenu();
        const dish = blankDish({
          section: args.section ?? '',
          name: String(args.name).slice(0, 40),
          name_original: args.name_original || '',
          price: args.price == null ? '' : String(args.price),
          blurb: args.blurb || '',
          tags: Array.isArray(args.tags) ? args.tags.slice(0, 3) : [],
          signature: !!args.signature,
          signature_note: args.signature_note || '',
          kind: args.kind || inferKind(args.name, args.tags || []),
          art: args.art ? sanitizeArt(args.art) : '',
        });
        ctx.setMenu(addDish(menu, dish));
        return ok({ dishId: dish.id, kind: dish.kind, count: ctx.getMenu().dishes.length });
      },
    },

    /* 6. 改菜 */
    update_dish: {
      description: '按 id 或菜名修改某道菜。只传要改的字段。',
      inputSchema: {
        type: 'object',
        properties: {
          id: { type: 'string' },
          name: { type: 'string', description: '用于定位的菜名' },
          patch: {
            type: 'object',
            description: '要修改的字段：name/price/blurb/tags/section/signature/signature_note/kind/art',
          },
        },
        required: ['patch'],
      },
      handler: async ({ id, name, patch }) => {
        const menu = ctx.getMenu();
        const d = findDish(menu, { id, name });
        if (!d) return fail('找不到这道菜', '先用 get_source 或 inspect_menu 确认菜品列表。');
        const clean = { ...patch };
        if (clean.art) clean.art = sanitizeArt(clean.art);
        if (clean.name) clean.name = String(clean.name).slice(0, 40);
        if (Array.isArray(clean.tags)) clean.tags = clean.tags.slice(0, 3);
        ctx.setMenu(updateDish(menu, d.id, clean));
        return ok({ dishId: d.id, changed: Object.keys(clean) });
      },
    },

    /* 7. 删菜 */
    remove_dish: {
      description: '删除一道菜。',
      inputSchema: {
        type: 'object',
        properties: { id: { type: 'string' }, name: { type: 'string' } },
      },
      handler: async ({ id, name }) => {
        const menu = ctx.getMenu();
        const d = findDish(menu, { id, name });
        if (!d) return fail('找不到这道菜');
        ctx.setMenu(removeDish(menu, d.id));
        return ok({ removed: d.name, count: ctx.getMenu().dishes.length });
      },
    },

    /* 8. 质检 */
    inspect_menu: {
      description: '检查整张菜单：排版、插图、内容一致性。返回 error 和 warn 两级问题清单。',
      inputSchema: { type: 'object', properties: {} },
      handler: async () => {
        const report = inspectMenu(ctx.getMenu());
        return ok({
          passed: report.ok,
          errors: report.errors,
          warns: report.warns,
          metrics: report.metrics,
          issues: report.issues,
          hint: report.ok ? '没有 error 级问题。' : '按 issues 里的 dishId 逐条 update_dish 修复。',
        });
      },
    },

    /* 9. 等用户 */
    wait_for_user: {
      description: '暂停，等待用户的下一个动作（换图、文字要求、导出）。返回用户事件类型。',
      inputSchema: { type: 'object', properties: {} },
      handler: async () => {
        const ev = ctx.takeEvent();
        return ok({
          event: ev ? ev.type : 'idle',
          payload: ev ? ev.payload : null,
          hint: ev ? '按事件内容继续处理。' : '暂时没有新事件，可以让用户提要求。',
        });
      },
    },
  };
}

/* ---------------- 一次性批量导入（内置生成器专用） ---------------- */

/**
 * 从文字一次性填充菜单。内置生成器走这条路，等价于
 * 连续调用 begin_menu + N 次 add_dish，但不需要逐个 await。
 */
function fillFromText(menu, text) {
  const parsed = parseTextMenu(text);
  let m = menu;
  const created = [];

  for (const p of parsed.dishes) {
    const hit = dictLookup(p.name);
    const d = blankDish({
      section: p.section || '',
      name: p.name,
      price: p.price || '',
      blurb: p.blurb || (hit ? hit.blurb : ''),
      tags: p.tags || (hit ? hit.tags : []),
      kind: p.kind || inferKind(p.name, p.tags || []),
    });
    m = addDish(m, d);
    created.push(d);
  }
  return { menu: m, parsed, created };
}


/* ==================== js/driver.js ==================== */
/* ============================================================
 * driver.js — 双驱动
 *  A. 内置生成器：不依赖任何外部服务，规则解析 + 参数化插图
 *  B. WebMCP 桥：把同一套工具暴露给外部 Agent
 * 两者的差别只在「谁来决策」，执行路径完全一致。
 * ============================================================ */







const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const toNum = (v) => {
  const n = parseFloat(String(v).replace(/[^\d.]/g, ''));
  return Number.isNaN(n) ? -1 : n;
};

/* ---------------- 挑招牌 ---------------- */

const NOT_SIGNATURE_KIND = /^(drink|dessert|soup)$/;
const SIGN_WORDS = /招牌|特色|镇店|必点|推荐|招牌菜|拿手/;

function autoPickSignature(menu) {
  if (!menu.dishes.length) return menu;
  if (menu.dishes.some((d) => d.signature)) return menu;

  const pool = menu.dishes.filter((d) => !NOT_SIGNATURE_KIND.test(d.kind || ''));
  if (!pool.length) return menu;

  let pick = pool.find((d) => SIGN_WORDS.test(d.name));
  let note = '菜名带「招牌/特色」字样，据此标为主推';
  if (!pick) {
    pick = pool.slice().sort((a, b) => toNum(b.price) - toNum(a.price))[0];
    note = '按价位在该品类中最高，暂定为主推；可改为实际销量最高的一道';
  }
  return updateDish(menu, pick.id, { signature: true, signature_note: note });
}

/* ---------------- 自动修复闭环 ---------------- */

/**
 * 按质检结果修可以机器修的问题。
 * 明确不修：价格缺失（不编造）、菜名重复（要人判断）、菜名过长（要人删字）。
 */
function autoFix(menu, rounds = 3) {
  let m = menu;
  const log = [];

  for (let r = 0; r < rounds; r++) {
    const report = inspectMenu(m);
    if (!report.issues.length) break;
    let changed = false;

    for (const issue of report.issues) {
      const d = issue.dishId ? m.dishes.find((x) => x.id === issue.dishId) : null;

      switch (issue.code) {
        case 'no-blurb': {
          const hit = dictLookup(d?.name);
          if (d && hit?.blurb) {
            m = updateDish(m, d.id, { blurb: hit.blurb });
            log.push(`补全「${d.name}」的描述`);
            changed = true;
          }
          break;
        }
        case 'sig-no-evidence': {
          if (d) {
            m = updateDish(m, d.id, { signature_note: '人工标记为主推菜，未记录具体依据' });
            log.push(`为「${d.name}」补上招牌依据说明`);
            changed = true;
          }
          break;
        }
        case 'art-thin':
        case 'art-tiny': {
          if (d) {
            // 丢掉不够用的外部图，交回引擎重画
            m = updateDish(m, d.id, { art: '', kind: d.kind || inferKind(d.name, d.tags) });
            log.push(`重新绘制「${d.name}」的插图`);
            changed = true;
          }
          break;
        }
        case 'mixed-section': {
          const fix = m.dishes.map((x) => ({ ...x, section: x.section || '热菜' }));
          m = { ...m, dishes: fix };
          log.push('把未分类的菜品统一归到「热菜」');
          changed = true;
          break;
        }
        case 'multi-signature': {
          const sigs = m.dishes.filter((x) => x.signature);
          for (const s of sigs.slice(1)) {
            m = updateDish(m, s.id, { signature: false, signature_note: '' });
          }
          log.push(`只保留第一道招牌，取消另外 ${sigs.length - 1} 道的标记`);
          changed = true;
          break;
        }
        case 'price-format': {
          const fixed = m.dishes.map((x) =>
            String(x.price || '').trim() && !/^[¥￥$]/.test(String(x.price).trim())
              ? { ...x, price: `¥${String(x.price).trim()}` }
              : x,
          );
          m = { ...m, dishes: fixed };
          log.push('统一价格写法，全部加上货币符号');
          changed = true;
          break;
        }
        default:
          break;
      }
    }
    if (!changed) break;
  }
  return { menu: m, log };
}

/* ---------------- 内置生成器 ---------------- */

/**
 * 从文字菜单跑完整流程。走的是 toolset 的同一批 handler。
 * @param {object} ctx 会话上下文
 * @param {object} toolset protocol.createToolset() 的产物
 * @param {{onStep?:(s:object)=>void, pace?:number}} opts
 */
async function runLocal(ctx, toolset, opts = {}) {
  const { onStep = () => {}, pace = 55 } = opts;
  const src = ctx.getSource();
  const text = String(src.text || '');
  const cur = ctx.getMenu();

  const parsed = parseTextMenu(text);
  if (!parsed.dishes.length) {
    return {
      ok: false,
      error: '没能从文字里解析出菜品',
      hint: '每行一道菜，格式如「红烧肉 68」，或用【热菜】这样的分节标题。',
    };
  }

  const total = parsed.dishes.length + 2;
  let done = 0;
  const step = (label, phase = 'work') => {
    done += 1;
    onStep({ label, phase, done, total });
  };

  // 1) 铺纸
  const shopName = parsed.shopName || cur.name || '未命名小馆';
  await toolset.begin_menu.handler({
    name: shopName,
    name_original: cur.name_original || '',
    subtitle: cur.subtitle || '',
    footer: cur.footer || '',
    seal: cur.seal || (shopName.length >= 2 ? shopName.slice(0, 2) : ''),
    theme: cur.theme || 'rice',
  });
  step('铺好菜单纸', 'paper');

  // 2) 逐道落笔
  for (const p of parsed.dishes) {
    await toolset.add_dish.handler({
      section: p.section || '',
      name: p.name,
      price: p.price || '',
      blurb: p.blurb || '',
      tags: p.tags || [],
      kind: p.kind || inferKind(p.name, p.tags || []),
    });
    step(`写下「${p.name}」`, 'dish');
    if (pace) await sleep(pace);
  }

  // 3) 挑招牌 → 自动修复 → 复检
  let menu = ctx.getMenu();
  menu = autoPickSignature(menu);
  ctx.setMenu(menu);
  step('挑出主推菜', 'sign');

  const fixed = autoFix(ctx.getMenu());
  ctx.setMenu(fixed.menu);
  const report = inspectMenu(fixed.menu);
  step('质检完成', 'inspect');

  return {
    ok: true,
    shopName,
    parsed: { dishes: parsed.dishes.length, sections: parsed.sections },
    fixed: fixed.log,
    report,
  };
}

/** 对已有菜单做一次「重画全部插图」——换掉外部 art，回到引擎 */
function redrawAll(menu) {
  return {
    ...menu,
    dishes: menu.dishes.map((d) => ({
      ...d,
      art: '',
      kind: d.kind || inferKind(d.name, d.tags),
    })),
  };
}

/* ---------------- WebMCP 桥 ---------------- */

/**
 * 把工具注册到页面的 WebMCP。不支持的浏览器返回 unsupported，
 * 此时应用仍可用内置生成器工作。
 */
function mountWebMCP(toolset, meta = {}) {
  const mc = globalThis.document?.modelContext;
  if (!mc || typeof mc.provideContext !== 'function') {
    return { supported: false, reason: '当前浏览器未提供 WebMCP（document.modelContext）' };
  }
  try {
    const tools = Object.entries(toolset).map(([name, def]) => ({
      name,
      description: def.description,
      inputSchema: def.inputSchema,
      execute: async (args) => {
        const r = await def.handler(args || {});
        return { content: [{ type: 'text', text: JSON.stringify(r) }] };
      },
    }));
    mc.provideContext({
      name: meta.name || 'vivid-menu',
      description: meta.description || '把网页变成 Agent 的画布：逐道菜绘制菜单',
      tools,
    });
    return { supported: true, count: tools.length };
  } catch (e) {
    return { supported: false, reason: `注册失败：${e.message}` };
  }
}

/** 当前主题是否是已知预设 */
const isValidTheme = (id) => !!THEMES[id];


/* ==================== js/photo.js ==================== */
/* ============================================================
 * photo.js — 照片输入、压缩与局部放大
 * 原图只存在浏览器里，不上传。压缩后再进存档，避免撑爆 localStorage。
 * ============================================================ */

/** 读取文件为 dataURL */
function readAsDataUrl(file) {
  return new Promise((resolve, reject) => {
    const r = new FileReader();
    r.onload = () => resolve(r.result);
    r.onerror = () => reject(new Error('读取文件失败'));
    r.readAsDataURL(file);
  });
}

function loadImage(src) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = () => reject(new Error('图片解码失败'));
    img.src = src;
  });
}

/**
 * 读入图片并压缩。长边超过 maxEdge 时等比缩小。
 * @returns {{dataUrl:string,width:number,height:number,name:string}}
 */
async function readImageFile(file, maxEdge = 1400, quality = 0.82) {
  if (!file.type.startsWith('image/')) throw new Error('这不是图片文件');
  const raw = await readAsDataUrl(file);
  const img = await loadImage(raw);
  const scale = Math.min(1, maxEdge / Math.max(img.width, img.height));
  const w = Math.round(img.width * scale);
  const h = Math.round(img.height * scale);

  const c = document.createElement('canvas');
  c.width = w;
  c.height = h;
  const g = c.getContext('2d');
  g.imageSmoothingQuality = 'high';
  g.drawImage(img, 0, 0, w, h);

  return {
    dataUrl: c.toDataURL('image/jpeg', quality),
    width: w,
    height: h,
    name: file.name || 'menu.jpg',
  };
}

/**
 * 按归一化区域裁切放大，用于辨认细节。
 * @param {{dataUrl:string}} source
 * @param {{x:number,y:number,w:number,h:number}} box 0~1
 */
async function cropRegion(source, box, outWidth = 1000) {
  const img = await loadImage(source.dataUrl);
  const sx = box.x * img.width;
  const sy = box.y * img.height;
  const sw = Math.max(8, box.w * img.width);
  const sh = Math.max(8, box.h * img.height);
  const scale = Math.min(3, outWidth / sw);
  const w = Math.round(sw * scale);
  const h = Math.round(sh * scale);

  const c = document.createElement('canvas');
  c.width = w;
  c.height = h;
  const g = c.getContext('2d');
  g.imageSmoothingQuality = 'high';
  g.drawImage(img, sx, sy, sw, sh, 0, 0, w, h);

  return { dataUrl: c.toDataURL('image/png'), width: w, height: h };
}

/** 从粘贴事件里取图片文件 */
function fileFromPaste(e) {
  const items = e.clipboardData?.items || [];
  for (const it of items) {
    if (it.type && it.type.startsWith('image/')) return it.getAsFile();
  }
  return null;
}


/* ==================== js/export.js ==================== */
/* ============================================================
 * export.js — 导出 SVG / PNG
 * SVG 是矢量母版；PNG 用于直接发微信、发朋友圈。
 * ============================================================ */



/** 生成 SVG 文本（导出用，剔除点击热区） */
const toSvgText = (menu) => renderMenu(menu, { hitAreas: false }).svg;

function saveBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 2000);
}

const safeName = (s) => String(s || '菜单').replace(/[\\/:*?"<>|]/g, '_').slice(0, 30);

/** 下载 SVG */
function downloadSvg(menu) {
  const svg = toSvgText(menu);
  saveBlob(new Blob([svg], { type: 'image/svg+xml;charset=utf-8' }), `${safeName(menu.name)}.svg`);
}

/** SVG → PNG Blob */
async function svgToPngBlob(menu, scale = 2) {
  const svg = toSvgText(menu);
  const { width, height } = renderMenu(menu).layout;
  const url = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`;

  const img = await new Promise((resolve, reject) => {
    const i = new Image();
    i.onload = () => resolve(i);
    i.onerror = () => reject(new Error('SVG 渲染失败'));
    i.src = url;
  });

  const c = document.createElement('canvas');
  c.width = Math.round(width * scale);
  c.height = Math.round(height * scale);
  const g = c.getContext('2d');
  g.fillStyle = '#ffffff';
  g.fillRect(0, 0, c.width, c.height);
  g.imageSmoothingQuality = 'high';
  g.drawImage(img, 0, 0, c.width, c.height);

  return new Promise((resolve) => {
    c.toBlob((b) => resolve(b), 'image/png');
  });
}

/** 下载 PNG */
async function downloadPng(menu, scale = 2) {
  const blob = await svgToPngBlob(menu, scale);
  saveBlob(blob, `${safeName(menu.name)}.png`);
}

/**
 * 复制 PNG 到剪贴板。不支持时回落为下载，并返回状态说明。
 * @returns {Promise<'copied'|'downloaded'|'failed'>}
 */
async function copyPng(menu, scale = 2) {
  try {
    const blob = await svgToPngBlob(menu, scale);
    if (!blob) throw new Error('生成图片失败');
    if (!navigator.clipboard || !window.ClipboardItem) throw new Error('浏览器不支持图片剪贴板');
    await navigator.clipboard.write([new ClipboardItem({ 'image/png': blob })]);
    return 'copied';
  } catch (e) {
    console.warn('[export] 复制失败，改为下载', e);
    try {
      await downloadPng(menu, scale);
      return 'downloaded';
    } catch (e2) {
      console.error('[export] 下载也失败', e2);
      return 'failed';
    }
  }
}


/* ==================== js/main.js ==================== */
/* ============================================================
 * main.js — 界面编排
 * 只做三件事：把状态画到屏幕上、把用户动作翻译成工具调用、
 * 在两条驱动路径之间做切换。
 * ============================================================ */












/* ---------------- DOM ---------------- */

const $ = (id) => document.getElementById(id);
const dom = {
  stage: $('stage'),
  leftPane: $('leftPane'),
  sourceView: $('sourceView'),
  paperHolder: $('paperHolder'),
  cmdInput: $('cmdInput'),
  btnRun: $('btnRun'),
  dishCount: $('dishCount'),
  engineStatus: $('engineStatus'),
  engineText: $('engineText'),
  themeSwatch: $('themeSwatch'),
  intro: $('intro'),
  progress: $('progress'),
  toast: $('toast'),
  fileInput: $('fileInput'),
  sheetMask: $('sheetMask'),
  drawerMask: $('drawerMask'),
  drawerBody: $('drawerBody'),
  briefMask: $('briefMask'),
  briefBody: $('briefBody'),
  mcpHint: $('mcpHint'),
};

/* ---------------- 状态 ---------------- */

const state = {
  menu: blankMenu({ name: '' }),
  source: { dataUrl: '', width: 0, height: 0, text: '', zoom: null },
  editingId: null,
  busy: false,
  focus: false,
  events: [],
  dirty: false,
};

let rafId = 0;
const scheduleRender = () => {
  if (rafId) return;
  rafId = requestAnimationFrame(() => {
    rafId = 0;
    paintPaper();
    paintMeta();
  });
};

/* ---------------- 轻提示 ---------------- */

let toastTimer = null;
function toast(msg, isErr = false) {
  dom.toast.textContent = msg;
  dom.toast.classList.toggle('err', isErr);
  dom.toast.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => dom.toast.classList.remove('show'), 2600);
}

/* ---------------- 会话上下文（供工具调用） ---------------- */

const ctx = {
  getMenu: () => state.menu,
  setMenu: (m) => {
    state.menu = { ...m, sourceImage: state.source.dataUrl || '' };
    store.save(state.menu);
    scheduleRender();
  },
  getSource: () => state.source,
  pushEvent: (type, payload) => state.events.push({ type, payload }),
  takeEvent: () => state.events.shift() || null,
  cropSource: (box) => cropRegion(state.source, box),
};

const toolset = createToolset(ctx);

/* ---------------- 绘制屏幕 ---------------- */

function paintPaper() {
  const { svg } = renderMenu(state.menu);
  dom.paperHolder.innerHTML = svg;
  dom.paperHolder.style.background = themeOf(state.menu).paper;
}

function paintMeta() {
  const s = stats(state.menu);
  dom.dishCount.textContent = `${s.count} 道菜${s.signatureCount ? ` · ${s.signatureCount} 招牌` : ''}`;
  dom.themeSwatch.style.background = themeOf(state.menu).paper;
  dom.btnRun.disabled = state.busy;
}

function paintSource() {
  const box = dom.sourceView;
  const s = state.source;

  if (s.dataUrl) {
    box.innerHTML = `
      <div class="photo-box">
        <img src="${s.dataUrl}" alt="原始菜单">
        ${state.busy ? '<div class="scan"></div>' : ''}
      </div>
      ${s.zoom ? `
        <div class="zoom-box">
          <div class="zb-head"><span>局部放大</span><span>${Math.round(s.zoom.w * 100)}% 区域</span></div>
          <img src="${s.zoom.dataUrl}" alt="放大区域">
        </div>` : ''}
      <div class="source-empty">
        <b>照片只在本机，不上传</b>
        浏览器本地读不出图上的字。把菜名和价格粘到下面的框里，就能开始画。
      </div>`;
    return;
  }

  if (s.text.trim()) {
    const st = stats(state.menu);
    box.innerHTML = `<div class="text-box">${escapeHtml(s.text)}</div>` + (st.count ? miniStat(st) : '');
    return;
  }

  if (state.menu.dishes.length) {
    const st = stats(state.menu);
    box.innerHTML = `
      <div class="source-empty">
        <b>这张已经画好了</b>
        右边是成品。点任意一道菜可以改名字、价格和说明；<br>也可以把文字粘到下面的框里，重新生成一张。
      </div>` + miniStat(st);
    return;
  }

  box.innerHTML = `<div class="source-empty">
      <b>还没有素材</b>
      上传一张菜单照片，或把你的菜单文字粘进来。<br>一行一道菜就行。
    </div>`;
}

function miniStat(st) {
  return `<div class="mini-stat">
    <div><span>菜品</span><b>${st.count}</b></div>
    <div><span>分节</span><b>${st.sections.length}</b></div>
    <div><span>招牌</span><b>${st.signatureCount}</b></div>
  </div>`;
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
}

/* ---------------- 进度 ---------------- */

function showProgress(ratio, label) {
  dom.progress.hidden = false;
  dom.progress.querySelector('.bar i').style.width = `${Math.round(ratio * 100)}%`;
  dom.progress.querySelector('.label').textContent = label;
}
function hideProgress() {
  dom.progress.hidden = true;
  dom.progress.querySelector('.bar i').style.width = '0%';
}

/* ---------------- 开场 ---------------- */

function hideIntro() {
  dom.intro.classList.add('hidden');
}
function showIntro() {
  dom.intro.classList.remove('hidden');
}

/* ---------------- 生成 ---------------- */

async function generate() {
  if (state.busy) return;

  const text = (dom.cmdInput.value || '').trim() || state.source.text;
  if (!text.trim()) {
    if (state.source.dataUrl) {
      toast('照片里有字，但浏览器认不出来。请把菜名粘到下面的框里。', true);
      dom.cmdInput.focus();
    } else {
      toast('先粘一段菜单文字，或上传一张照片', true);
    }
    return;
  }

  state.source.text = text;
  state.busy = true;
  dom.btnRun.textContent = '绘制中…';
  dom.btnRun.disabled = true;
  paintSource();
  showProgress(0.04, '铺纸…');
  hideIntro();

  try {
    const res = await runLocal(ctx, toolset, {
      pace: 58,
      onStep: (s) => showProgress(0.08 + (s.done / s.total) * 0.9, s.label),
    });

    if (!res.ok) {
      toast(res.error + (res.hint ? '：' + res.hint : ''), true);
      return;
    }

    store.save(state.menu, { immediate: true });
    // 文字已经落到素材区，输入框腾出来当指令区
    dom.cmdInput.value = '';
    dom.cmdInput.placeholder = '继续说要改什么，例如：把招牌换成酸辣粉 / 价格都加个 ¥';
    paintSource();
    scheduleRender();

    const rep = res.report;
    const parts = [`画好了 ${res.parsed.dishes} 道菜`];
    if (rep.errors) parts.push(`${rep.errors} 处要修`);
    else if (rep.warns) parts.push(`${rep.warns} 处可优化`);
    else parts.push('质检通过');
    if (res.fixed.length) parts.push(`自动修了 ${res.fixed.length} 项`);
    showProgress(1, parts.join('，'));
    toast(parts.join('，'));
  } catch (e) {
    console.error(e);
    toast('绘制出错：' + e.message, true);
  } finally {
    state.busy = false;
    dom.btnRun.textContent = '开始绘制';
    dom.btnRun.disabled = false;
    paintMeta();
    paintSource();
    setTimeout(hideProgress, 1000);
  }
}

/* ---------------- 素材输入 ---------------- */

async function loadPhoto(file) {
  if (!file) return;
  try {
    const img = await readImageFile(file);
    state.source = { ...state.source, dataUrl: img.dataUrl, width: img.width, height: img.height, zoom: null };
    state.menu = { ...state.menu, sourceImage: img.dataUrl };
    store.save(state.menu);
    hideIntro();
    paintSource();
    toast('照片已就位。把菜名粘到下面的框里，就能开始画。');
  } catch (e) {
    toast(e.message, true);
  }
}

function loadText(text) {
  state.source.text = text;
  dom.cmdInput.value = text;
  hideIntro();
  paintSource();
  dom.cmdInput.focus();
}

/* ---------------- 打开菜单 ---------------- */

function openMenu(menu) {
  state.menu = { ...menu };
  state.source = {
    dataUrl: menu.sourceImage || '',
    width: 0, height: 0,
    text: '',
    zoom: null,
  };
  hideIntro();
  paintSource();
  scheduleRender();
  paintMeta();
}

/* ---------------- 菜品编辑 ---------------- */

function bindPaperClicks() {
  dom.paperHolder.addEventListener('click', (e) => {
    const hit = e.target.closest('.vm-hit');
    if (!hit) return;
    const id = hit.getAttribute('data-dish');
    if (id) openSheet(id);
  });
}

function openSheet(dishId) {
  const d = state.menu.dishes.find((x) => x.id === dishId);
  if (!d) return;
  state.editingId = dishId;

  $('fName').value = d.name || '';
  $('fPrice').value = d.price || '';
  $('fSection').value = d.section || '';
  $('fBlurb').value = d.blurb || '';
  $('fTags').value = (d.tags || []).join(',');
  $('fSig').checked = !!d.signature;
  $('fSigNote').value = d.signature_note || '';
  $('sigNoteWrap').hidden = !d.signature;
  $('artKind').textContent = d.kind || inferKind(d.name, d.tags) || '—';

  dom.sheetMask.hidden = false;
  $('fName').focus();
}

function closeSheet() {
  dom.sheetMask.hidden = true;
  state.editingId = null;
}

function saveSheet() {
  const id = state.editingId;
  if (!id) return;
  const patch = {
    name: $('fName').value.trim(),
    price: $('fPrice').value.trim(),
    section: $('fSection').value.trim(),
    blurb: $('fBlurb').value.trim(),
    tags: $('fTags').value.split(/[,，、]/).map((s) => s.trim()).filter(Boolean).slice(0, 3),
    signature: $('fSig').checked,
    signature_note: $('fSigNote').value.trim(),
  };
  if (!patch.name) { toast('菜名不能为空', true); return; }
  ctx.setMenu(updateDish(state.menu, id, patch));
  store.save(state.menu, { immediate: true });
  closeSheet();
  scheduleRender();
}

/* ---------------- 合集 ---------------- */

function openDrawer() {
  const saved = store.list();
  const items = [
    ...saved.map((m) => ({ menu: m, saved: true })),
    ...PRESETS.map((m) => ({ menu: m, saved: false })),
  ];

  if (!items.length) {
    dom.drawerBody.innerHTML = '<div class="gal-empty">还没有存过菜单。<br>画完一张就会自动出现在这里。</div>';
  } else {
    dom.drawerBody.innerHTML = items.map(({ menu, saved }, i) => {
      const { svg } = renderMenu(menu, { hitAreas: false });
      const s = stats(menu);
      return `<div class="gal-item" data-idx="${i}">
        <div class="thumb">${svg}</div>
        <div class="meta">
          <b>${escapeHtml(menu.name || '未命名')}</b>
          <span>${s.count} 道菜 · ${saved ? '我存的' : '示例'}</span>
        </div>
        ${saved ? '<button class="del" data-del="' + menu.id + '" title="删除">×</button>' : ''}
      </div>`;
    }).join('');

    dom.drawerBody.querySelectorAll('.gal-item').forEach((node) => {
      node.addEventListener('click', (e) => {
        if (e.target.closest('.del')) return;
        const idx = Number(node.getAttribute('data-idx'));
        openMenu(items[idx].menu);
        dom.drawerMask.hidden = true;
        toast('已打开「' + (items[idx].menu.name || '未命名') + '」');
      });
    });

    dom.drawerBody.querySelectorAll('.del').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        store.remove(btn.getAttribute('data-del'));
        openDrawer();
      });
    });
  }
  dom.drawerMask.hidden = false;
}

/* ---------------- 主题面板 ---------------- */

let themePanel = null;
function toggleThemePanel() {
  if (themePanel) { closeThemePanel(); return; }

  themePanel = document.createElement('div');
  themePanel.className = 'theme-panel';
  themePanel.innerHTML = THEME_LIST.map((t) => `
    <button data-theme="${t.id}" class="${state.menu.theme === t.id ? 'on' : ''}">
      <span class="chip" style="background:${t.paper};border-color:${t.edge}">
        <i style="background:${t.ink}"></i><i style="background:${t.accent}"></i>
      </span>
      <span class="tn">${t.label}</span>
    </button>`).join('');

  document.body.appendChild(themePanel);
  const r = $('btnTheme').getBoundingClientRect();
  themePanel.style.top = `${r.bottom + 8}px`;
  themePanel.style.left = `${Math.max(12, Math.min(r.left - 60, window.innerWidth - 230))}px`;

  themePanel.querySelectorAll('button').forEach((b) => {
    b.addEventListener('click', () => {
      ctx.setMenu({ ...state.menu, theme: b.getAttribute('data-theme') });
      store.save(state.menu, { immediate: true });
      closeThemePanel();
      toast('换成「' + THEMES[b.getAttribute('data-theme')].label + '」');
    });
  });

  setTimeout(() => document.addEventListener('click', outsideTheme), 0);
}

function outsideTheme(e) {
  if (themePanel && !themePanel.contains(e.target) && e.target.id !== 'btnTheme') closeThemePanel();
}

function closeThemePanel() {
  if (themePanel) { themePanel.remove(); themePanel = null; }
  document.removeEventListener('click', outsideTheme);
}

/* ---------------- 绑定 ---------------- */

function bind() {
  // 开场三个入口
  dom.intro.querySelectorAll('.choice').forEach((b) => {
    b.addEventListener('click', () => {
      const act = b.getAttribute('data-act');
      if (act === 'photo') dom.fileInput.click();
      if (act === 'text') { hideIntro(); dom.cmdInput.focus(); }
      if (act === 'demo') { openMenu(PRESETS[0]); toast('已打开示例菜单，可以直接改'); }
    });
  });

  $('btnPick').addEventListener('click', () => dom.fileInput.click());
  $('btnText').addEventListener('click', () => { hideIntro(); dom.cmdInput.focus(); dom.cmdInput.select(); });
  $('btnReset').addEventListener('click', () => {
    if (state.menu.dishes.length && !confirm('清空当前菜单，重新开始？')) return;
    state.menu = blankMenu({ theme: state.menu.theme });
    state.source = { dataUrl: '', width: 0, height: 0, text: '', zoom: null };
    dom.cmdInput.value = '';
    store.save(state.menu, { immediate: true });
    paintSource();
    scheduleRender();
    paintMeta();
    showIntro();
  });

  dom.fileInput.addEventListener('change', (e) => {
    const f = e.target.files?.[0];
    dom.fileInput.value = '';
    loadPhoto(f);
  });

  dom.btnRun.addEventListener('click', generate);

  // 粘贴：图片优先进素材，纯文字进输入框
  document.addEventListener('paste', (e) => {
    const f = fileFromPaste(e);
    if (f) {
      e.preventDefault();
      loadPhoto(f);
      return;
    }
    const t = e.clipboardData?.getData('text/plain') || '';
    if (t && /[\u4e00-\u9fa5]/.test(t) && /\d/.test(t) && document.activeElement !== dom.cmdInput) {
      e.preventDefault();
      loadText(t);
      toast('文字已接住，点「开始绘制」试试');
    }
  });

  // 拖入
  let dragDepth = 0;
  window.addEventListener('dragenter', (e) => {
    if (!e.dataTransfer?.types?.includes('Files')) return;
    dragDepth += 1;
    document.body.classList.add('drag-over');
  });
  window.addEventListener('dragleave', () => {
    dragDepth = Math.max(0, dragDepth - 1);
    if (!dragDepth) document.body.classList.remove('drag-over');
  });
  window.addEventListener('dragover', (e) => e.preventDefault());
  window.addEventListener('drop', (e) => {
    e.preventDefault();
    dragDepth = 0;
    document.body.classList.remove('drag-over');
    const f = e.dataTransfer?.files?.[0];
    if (f && f.type.startsWith('image/')) loadPhoto(f);
  });

  // 顶栏
  $('btnTheme').addEventListener('click', toggleThemePanel);
  $('btnGallery').addEventListener('click', openDrawer);
  $('btnBrief').addEventListener('click', () => {
    dom.briefBody.textContent = BRIEF;
    dom.briefMask.hidden = false;
  });
  $('briefClose').addEventListener('click', () => { dom.briefMask.hidden = true; });
  dom.briefMask.addEventListener('click', (e) => { if (e.target === dom.briefMask) dom.briefMask.hidden = true; });

  // 底部工具
  $('btnFocus').addEventListener('click', () => {
    state.focus = !state.focus;
    dom.stage.classList.toggle('focus', state.focus);
    $('btnFocus').classList.toggle('on', state.focus);
  });
  $('btnSvg').addEventListener('click', () => {
    if (!state.menu.dishes.length) return toast('还没有菜可导出', true);
    downloadSvg(state.menu);
    toast('SVG 已下载');
  });
  $('btnPng').addEventListener('click', async () => {
    if (!state.menu.dishes.length) return toast('还没有菜可导出', true);
    const r = await copyPng(state.menu, 2);
    toast(r === 'copied' ? '图片已复制，去微信里粘贴' : r === 'downloaded' ? '已下载 PNG' : '导出失败', r === 'failed');
  });

  // 编辑浮层
  $('sheetClose').addEventListener('click', closeSheet);
  dom.sheetMask.addEventListener('click', (e) => { if (e.target === dom.sheetMask) closeSheet(); });
  $('btnSaveDish').addEventListener('click', saveSheet);
  $('btnDel').addEventListener('click', () => {
    const id = state.editingId;
    if (!id) return;
    ctx.setMenu(removeDish(state.menu, id));
    store.save(state.menu, { immediate: true });
    closeSheet();
    scheduleRender();
    toast('已删除');
  });
  $('fSig').addEventListener('change', (e) => { $('sigNoteWrap').hidden = !e.target.checked; });
  $('btnRedraw').addEventListener('click', () => {
    const id = state.editingId;
    if (!id) return;
    const d = state.menu.dishes.find((x) => x.id === id);
    if (!d) return;
    // 用一个新种子重画：换掉 art 并微调 id 参与哈希
    const next = updateDish(state.menu, id, { art: '', kind: d.kind || inferKind(d.name, d.tags) });
    next.dishes = next.dishes.map((x) =>
      x.id === id ? { ...x, _seed: Math.random().toString(36).slice(2) } : x,
    );
    ctx.setMenu(next);
    scheduleRender();
    toast('换了一幅');
  });

  // 抽屉
  $('drawerClose').addEventListener('click', () => { dom.drawerMask.hidden = true; });
  dom.drawerMask.addEventListener('click', (e) => { if (e.target === dom.drawerMask) dom.drawerMask.hidden = true; });

  // 快捷键
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeSheet();
      dom.drawerMask.hidden = true;
      dom.briefMask.hidden = true;
      closeThemePanel();
    }
    if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') generate();
    if ((e.metaKey || e.ctrlKey) && e.key === 's') {
      e.preventDefault();
      store.save(state.menu, { immediate: true });
      toast('已保存到合集');
    }
  });

  window.addEventListener('beforeunload', () => store.flush());
  bindPaperClicks();
}

/* ---------------- 引擎状态 ---------------- */

function initEngineBadge() {
  const mcp = mountWebMCP(toolset, {
    name: 'vivid-menu',
    description: '生动菜单：逐道菜绘制餐厅菜单',
  });
  if (mcp.supported) {
    dom.engineStatus.setAttribute('data-state', 'mcp');
    dom.engineText.textContent = `Agent 已接入 · ${mcp.count} 个工具`;
    dom.mcpHint.innerHTML = `<span style="color:#4a6b46">WebMCP 已就绪，${mcp.count} 个工具可供外部 Agent 调用</span>`;
  } else {
    dom.engineStatus.setAttribute('data-state', 'local');
    dom.engineText.textContent = '内置引擎';
    dom.mcpHint.textContent = '当前浏览器无 WebMCP，使用内置引擎（不影响使用）';
  }
}

/* ---------------- 启动 ---------------- */

function boot() {
  bind();
  initEngineBadge();
  paintSource();
  paintMeta();

  // 恢复上次的菜单
  const activeId = store.activeId();
  const saved = activeId ? store.get(activeId) : null;
  if (saved && saved.dishes?.length) {
    openMenu(saved);
  } else {
    paintPaper();
  }

  // 提示当前能力边界
  console.info('%c生动菜单', 'color:#b4472f;font-weight:600', '就绪。9 个工具已挂到 window.vividMenu');
  window.vividMenu = { state, ctx, toolset, renderMenu, inspectMenu, parseTextMenu };

  // 分享/演示入口：?demo=0|1|2 直接打开内置示例
  const q = new URLSearchParams(location.search);
  if (q.has('demo')) {
    const i = Math.max(0, Math.min(PRESETS.length - 1, Number(q.get('demo')) || 0));
    openMenu(PRESETS[i]);
  }
  if (q.has('text')) {
    const t = q.get('text');
    dom.cmdInput.value = t;
    loadText(t);
    // ?text=...&run=1 可做一键演示链接
    if (q.has('run')) setTimeout(generate, 260);
  }
  // 调试用：?sheet=1 打开第一道菜的编辑浮层
  if (q.has('sheet') && state.menu.dishes[0]) {
    setTimeout(() => openSheet(state.menu.dishes[0].id), 500);
  }
}

boot();


})();
