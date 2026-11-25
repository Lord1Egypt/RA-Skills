/* ============================================================
 * pen.js — 笔触与图元基础层
 * 所有插图在 viewBox="0 0 100 100" 坐标系内绘制。
 * 颜色使用语义 token：INK（墨）/ ACCENT（点缀）/ MUTE（淡），
 * 渲染时统一替换为当前菜单主题的真实色值。
 * ============================================================ */

export const TOKENS = ['INK', 'ACCENT', 'MUTE'];

/** 数值取整，避免生成过长的浮点串 */
export const n = (v) => Math.round(v * 100) / 100;

/** 坐标对 */
export const xy = (x, y) => `${n(x)} ${n(y)}`;

/** 通用元素构造 */
export function el(tag, attrs) {
  let s = `<${tag}`;
  for (const k in attrs) {
    if (attrs[k] === null || attrs[k] === undefined) continue;
    s += ` ${k}="${attrs[k]}"`;
  }
  return s + '/>';
}

/** 描边路径（默认不填充、圆头圆角、线宽 2.2） */
export function path(d, o = {}) {
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

export const line = (x1, y1, x2, y2, o = {}) =>
  path(`M${xy(x1, y1)}L${xy(x2, y2)}`, o);

export const circle = (cx, cy, r0, o = {}) => {
  const { fill = 'none', sw = 2.2, c = 'INK', op = 1 } = o;
  return el('circle', {
    cx: n(cx), cy: n(cy), r: n(r0),
    fill, stroke: fill === 'none' ? c : null,
    'stroke-width': fill === 'none' ? sw : null, opacity: op === 1 ? null : op,
  });
};

export const ellipse = (cx, cy, rx, ry, o = {}) => {
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
export const solid = (tag, attrs) => el(tag, { ...attrs, fill: attrs.fill || 'ACCENT', stroke: 'none' });

/* ---------------- 确定性随机 ---------------- */

/** 字符串 → 32 位哈希 */
export function hash(str) {
  let h = 2166136261;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

/** 基于种子的伪随机数生成器（mulberry32），保证同一道菜每次画法一致 */
export function rng(seed) {
  let a = seed >>> 0;
  return function next() {
    a = (a + 0x6D2B79F5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export const pick = (rand, arr) => arr[Math.floor(rand() * arr.length) % arr.length];
export const between = (rand, a, b) => a + rand() * (b - a);

/* ---------------- 常用食物图元 ---------------- */

/** 圆盘：外圈 + 内圈，俯视微透视 */
export function plate(r = 33, y = 60) {
  return [
    ellipse(50, y, r, r * 0.3, { sw: 2.4 }),
    ellipse(50, y, r * 0.78, r * 0.225, { sw: 1.4, op: 0.55 }),
  ].join('');
}

/** 深碗：碗口椭圆 + 碗身弧线 + 底足 */
export function bowl(y = 56, r = 30) {
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
export function block(cx, cy, w, h, rot, rand, o = {}) {
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
export function leafShape(x, y, len, rot, o = {}) {
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
export const dv = (dx, dy) => `${n(dx)} ${n(dy)}`;

/**
 * 卵形叶：基部窄、中段宽、端部圆钝——用于蔬菜（油菜、菠菜、白菜）。
 * 与 leafShape 的两端尖细形成对比。
 */
export function leafOval(x, y, len, rot, w = 0.42, o = {}) {
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
export function steam(cx, cy, h = 22, count = 3) {
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
export function dots(rand, cx, cy, r0, count, size = 1.5) {
  const out = [];
  for (let i = 0; i < count; i++) {
    const a = rand() * Math.PI * 2;
    const rr = Math.sqrt(rand()) * r0;
    out.push(circle(cx + Math.cos(a) * rr, cy + Math.sin(a) * rr * 0.42, between(rand, size * 0.7, size), { sw: 1.2, op: 0.75 }));
  }
  return out.join('');
}

/** 辣椒：弯月形果实 + 柄 */
export function chili(x, y, len, rot, filled = true) {
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
export function chopsticks(x, y, len, rot) {
  return [
    path(`M${xy(x, y)}L${xy(x + Math.cos((rot * Math.PI) / 180) * len, y + Math.sin((rot * Math.PI) / 180) * len)}`, { sw: 2 }),
    path(`M${xy(x, y + 4)}L${xy(x + Math.cos((rot * Math.PI) / 180) * (len * 0.9), y + 4 + Math.sin((rot * Math.PI) / 180) * (len * 0.9))}`, { sw: 2 }),
  ].join('');
}
