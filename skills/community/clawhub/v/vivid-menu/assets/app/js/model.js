/* ============================================================
 * model.js — 菜单数据模型
 * 菜品是结构化数据，SVG 只是渲染结果。这一层不碰任何 DOM。
 * ============================================================ */

/** 纸张与版心尺寸（单位与 SVG viewBox 一致） */
export const PAPER = {
  width: 880,
  marginX: 76,
  padTop: 96,
  padBottom: 108,
  maxHeight: 4200,
};

/** 尺寸令牌 */
export const SZ = {
  artNormal: 88,
  artSignature: 216,
  artTextGap: 20,
  priceW: 92,
  rowGap: 26,
  sectionGap: 34,
  signatureGap: 40,
};

/** 字体阶梯 */
export const FS = {
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
export const THEMES = {
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

export const THEME_LIST = Object.values(THEMES);

let seq = 1;
export const uid = (prefix = 'd') => `${prefix}${(seq++).toString(36)}${Math.random().toString(36).slice(2, 5)}`;

/** 空白菜品 */
export function blankDish(patch = {}) {
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
export function blankMenu(patch = {}) {
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
export const themeOf = (menu) => THEMES[menu?.theme] || THEMES.rice;

/* ---------------- 菜单操作（纯函数，返回新对象） ---------------- */

export function addDish(menu, dish) {
  const d = blankDish(dish);
  // 没有指定分节时，沿用最后一道菜的分节
  if (!dish.section && menu.dishes.length) {
    d.section = menu.dishes[menu.dishes.length - 1].section;
  }
  return touch({ ...menu, dishes: [...menu.dishes, d] });
}

export function updateDish(menu, id, patch) {
  const i = menu.dishes.findIndex((d) => d.id === id);
  if (i < 0) return menu;
  const next = menu.dishes.slice();
  next[i] = { ...next[i], ...patch, id };
  return touch({ ...menu, dishes: next });
}

export function removeDish(menu, id) {
  return touch({ ...menu, dishes: menu.dishes.filter((d) => d.id !== id) });
}

export function moveDish(menu, id, delta) {
  const i = menu.dishes.findIndex((d) => d.id === id);
  const j = i + delta;
  if (i < 0 || j < 0 || j >= menu.dishes.length) return menu;
  const next = menu.dishes.slice();
  [next[i], next[j]] = [next[j], next[i]];
  return touch({ ...menu, dishes: next });
}

export const touch = (menu) => ({ ...menu, updatedAt: Date.now() });

/** 菜品统计 */
export function stats(menu) {
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
