/* ============================================================
 * store.js — 本地存档
 * 用 localStorage 保存菜单列表；写入做防抖，避免每次工具调用都落盘。
 * 内置示例不写入存档，随时可重新打开。
 * ============================================================ */

import { blankMenu, blankDish, uid } from './model.js';

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

export const store = {
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

export const PRESETS = [
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
