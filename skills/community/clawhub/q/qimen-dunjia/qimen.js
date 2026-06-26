#!/usr/bin/env node
/**
 * 奇门遁甲排盘系统 - 命令行版本
 * 直接输出盘面解读，无需浏览器
 */

const TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
const DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];

const PALACE_MAP = {
  1: { name: '坎', gua: '☵', element: '水', zhi: [0], dir: '正北' },
  2: { name: '坤', gua: '☷', element: '土', zhi: [5, 6], dir: '西南' },
  3: { name: '震', gua: '☳', element: '木', zhi: [3], dir: '正东' },
  4: { name: '巽', gua: '☴', element: '木', zhi: [4, 5], dir: '东南' },
  5: { name: '中', gua: '', element: '土', zhi: [], dir: '中宫' },
  6: { name: '乾', gua: '☰', element: '金', zhi: [10, 11], dir: '西北' },
  7: { name: '兑', gua: '☱', element: '金', zhi: [9], dir: '正西' },
  8: { name: '艮', gua: '☶', element: '土', zhi: [1, 2], dir: '东北' },
  9: { name: '离', gua: '☲', element: '火', zhi: [6], dir: '正南' },
};

const NINE_STARS = {
  1: { name: '天蓬', type: '凶', weight: 30 },
  2: { name: '天芮', type: '凶', weight: 20 },
  3: { name: '天冲', type: '吉', weight: 80 },
  4: { name: '天辅', type: '吉', weight: 90 },
  5: { name: '天禽', type: '吉', weight: 100 },
  6: { name: '天心', type: '吉', weight: 90 },
  7: { name: '天柱', type: '凶', weight: 40 },
  8: { name: '天任', type: '吉', weight: 85 },
  9: { name: '天英', type: '平', weight: 60 },
};

const EIGHT_DOORS = {
  1: { name: '休门', element: '水', type: '吉', weight: 90 },
  2: { name: '死门', element: '土', type: '凶', weight: 10 },
  3: { name: '伤门', element: '木', type: '凶', weight: 30 },
  4: { name: '杜门', element: '木', type: '平', weight: 50 },
  6: { name: '开门', element: '金', type: '吉', weight: 95 },
  7: { name: '惊门', element: '金', type: '凶', weight: 40 },
  8: { name: '生门', element: '土', type: '吉', weight: 100 },
  9: { name: '景门', element: '火', type: '平', weight: 65 },
};

const EIGHT_GODS = ['值符', '腾蛇', '太阴', '六合', '白虎', '玄武', '九地', '九天'];
const GOD_WEIGHTS = { '值符': 100, '腾蛇': 20, '太阴': 80, '六合': 85, '白虎': 10, '玄武': 20, '九地': 75, '九天': 90 };

const SOLAR_TERMS_JU = {
  '冬至': [1, 7, 4], '小寒': [2, 8, 5], '大寒': [3, 9, 6], '立春': [8, 5, 2], '雨水': [9, 6, 3], '惊蛰': [1, 7, 4],
  '春分': [3, 9, 6], '清明': [4, 1, 7], '谷雨': [5, 2, 8], '立夏': [4, 1, 7], '小满': [5, 2, 8], '芒种': [6, 3, 9],
  '夏至': [9, 3, 6], '小暑': [8, 2, 5], '大暑': [7, 1, 4], '立秋': [2, 5, 8], '处暑': [1, 4, 7], '白露': [9, 3, 6],
  '秋分': [7, 1, 4], '寒露': [6, 9, 3], '霜降': [5, 8, 2], '立冬': [6, 9, 3], '小雪': [5, 8, 2], '大雪': [4, 7, 1],
};

const SOLAR_TERMS_C = [5.4055, 20.12, 3.87, 18.73, 5.63, 20.646, 4.81, 20.1, 5.52, 21.04, 5.678, 21.37, 7.108, 22.83, 7.5, 23.13, 7.646, 23.042, 8.318, 23.438, 7.438, 22.36, 7.18, 21.94];
const SOLAR_TERM_NAMES = ['小寒', '大寒', '立春', '雨水', '惊蛰', '春分', '清明', '谷雨', '立夏', '小满', '芒种', '夏至', '小暑', '大暑', '立秋', '处暑', '白露', '秋分', '寒露', '霜降', '立冬', '小雪', '大雪', '冬至'];

// 获取节气日期
function getTermDay(year, termIndex) {
  const y = year % 100, d = 0.2422, l = Math.floor(y / 4);
  return Math.floor(y * d + SOLAR_TERMS_C[termIndex]) - l;
}

// 获取当前节气
function getSolarTerm(date) {
  const y = date.getFullYear(), m = date.getMonth(), d = date.getDate();
  const base = m * 2;
  const d1 = getTermDay(y, base), d2 = getTermDay(y, base + 1);
  const idx = d < d1 ? (base - 1 + 24) % 24 : (d >= d1 && d < d2 ? base : base + 1);
  return { idx, name: SOLAR_TERM_NAMES[idx] };
}

// 获取干支
function getGanZhi(date) {
  const y = date.getFullYear(), m = date.getMonth(), d = date.getDate(), h = date.getHours();
  const term = getSolarTerm(date);
  const liChun = new Date(y, 1, getTermDay(y, 2));
  const chineseYear = date < liChun ? y - 1 : y;
  const yOffset = (chineseYear - 4) % 60;
  const yG = (yOffset < 0 ? yOffset + 60 : yOffset) % 10;
  const yZ = (yOffset < 0 ? yOffset + 60 : yOffset) % 12;
  const mZ = (Math.floor(term.idx / 2) + 1) % 12;
  const mG = ([2, 4, 6, 8, 0][yG % 5] + (mZ - 2 + 12) % 12) % 10;
  const utc1 = Date.UTC(1900, 0, 31), utc2 = Date.UTC(y, m, d);
  const dOffset = Math.floor((utc2 - utc1) / 86400000);
  const dG = (dOffset % 10 + 10) % 10, dZ = ((dOffset + 4) % 12 + 12) % 12;
  const hZ = Math.floor((h + 1) / 2) % 12;
  const hG = ([0, 2, 4, 6, 8][dG % 5] + hZ) % 10;
  return {
    y: TIAN_GAN[yG] + DI_ZHI[yZ],
    m: TIAN_GAN[mG] + DI_ZHI[mZ],
    d: TIAN_GAN[dG] + DI_ZHI[dZ],
    h: TIAN_GAN[hG] + DI_ZHI[hZ],
    vals: { yG, yZ, mG, mZ, dG, dZ, hG, hZ },
    term: term.name
  };
}

// 获取状态（刑、墓、迫）
function getStatus(stemIdx, palaceNum, doorIdx) {
  const res = [];
  if (stemIdx === undefined || stemIdx === null) return res;
  const jiXing = { 4: [3], 5: [2], 6: [8], 7: [9], 8: [4], 9: [4] };
  if (jiXing[stemIdx]?.includes(palaceNum)) res.push('刑');
  const ruMu = { 1: [2], 2: [6], 3: [8], 4: [6], 5: [8], 6: [8], 7: [4], 8: [4], 9: [2] };
  if (ruMu[stemIdx]?.includes(palaceNum)) res.push('墓');
  if (doorIdx && PALACE_MAP[palaceNum]) {
    const dE = EIGHT_DOORS[doorIdx].element, pE = PALACE_MAP[palaceNum].element;
    const po = { '金': ['木'], '木': ['土'], '土': ['水'], '水': ['火'], '火': ['金'] };
    if (po[dE]?.includes(pE)) res.push('迫');
  }
  return res;
}

// 获取驿马和空亡
function getExtra(hZ, dG, dZ) {
  const ma = [8, 0, 4].includes(hZ) ? 8 : ([2, 6, 10].includes(hZ) ? 2 : ([11, 3, 7].includes(hZ) ? 4 : 6));
  const kongIdx = (10 - dG + dZ) % 12;
  const kong = [kongIdx, (kongIdx + 1) % 12];
  const kongPalaces = [];
  for (let i = 1; i <= 9; i++) {
    if (PALACE_MAP[i].zhi.some(z => kong.includes(z))) kongPalaces.push(i);
  }
  return { ma, kong: kongPalaces };
}

// 构建盘面
function buildChart(ju, gz) {
  const qiYi = [4, 5, 6, 7, 8, 9, 3, 2, 1];
  let earth = {};
  let cur = ju.num;
  for (let i = 0; i < 9; i++) {
    earth[cur] = qiYi[i];
    cur = ju.type === 'Yang' ? (cur === 9 ? 1 : cur + 1) : (cur === 1 ? 9 : cur - 1);
  }
  let gap = (gz.vals.hG - gz.vals.hZ + 12) % 12;
  const leadStem = { 0: 4, 10: 5, 8: 6, 6: 7, 4: 8, 2: 9 }[gap];
  let leadP = Object.keys(earth).find(k => earth[k] === leadStem);
  const hStemLoc = gz.vals.hG === 0 ? leadP : Object.keys(earth).find(k => earth[k] === gz.vals.hG);
  const rot = [1, 8, 3, 4, 9, 2, 7, 6];
  const shift = (rot.indexOf(Number(hStemLoc == 5 ? 2 : hStemLoc)) - rot.indexOf(Number(leadP == 5 ? 2 : leadP)) + 8) % 8;
  let heaven = {}, heavenStems = {}, doors = {}, gods = {};
  rot.forEach((p, i) => {
    const target = rot[(i + shift) % 8];
    heaven[target] = p;
    heavenStems[target] = { m: earth[p], s: p == 2 ? earth[5] : null };
  });
  const dShift = (gz.vals.hZ - (12 - gap) % 12 + 12) % 12;
  let dP = Number(leadP == 5 ? 2 : leadP);
  for (let i = 0; i < dShift; i++) dP = ju.type === 'Yang' ? (dP === 9 ? 1 : dP + 1) : (dP === 1 ? 9 : dP - 1);
  if (dP === 5) dP = 2;
  const dRotShift = (rot.indexOf(dP) - rot.indexOf(Number(leadP == 5 ? 2 : leadP)) + 8) % 8;
  rot.forEach((p, i) => {
    const target = rot[(i + dRotShift) % 8];
    doors[target] = p === 5 ? null : p;
  });
  const gShift = rot.indexOf(Number(hStemLoc == 5 ? 2 : hStemLoc));
  rot.forEach((p, i) => {
    let idx = ju.type === 'Yang' ? (i - gShift + 8) % 8 : (gShift - i + 8) % 8;
    gods[p] = idx;
  });
  return { earth, heaven, heavenStems, doors, gods, extra: getExtra(gz.vals.hZ, gz.vals.dG, gz.vals.dZ), hStemLoc: Number(hStemLoc) };
}

// 格式化输出
function formatOutput(date) {
  const gz = getGanZhi(date);
  const isYang = ['冬至', '小寒', '大寒', '立春', '雨水', '惊蛰', '春分', '清明', '谷雨', '立夏', '小满', '芒种'].includes(gz.term);
  const ju = { num: SOLAR_TERMS_JU[gz.term]?.[gz.vals.dZ % 3] || 1, type: isYang ? 'Yang' : 'Yin', name: gz.term };
  const chart = buildChart(ju, gz);
  
  // 计算评分
  const hourPalace = chart.hStemLoc;
  const god = EIGHT_GODS[chart.gods[hourPalace]];
  const star = NINE_STARS[chart.heaven[hourPalace]];
  const door = EIGHT_DOORS[chart.doors[hourPalace]];
  const baseScore = (GOD_WEIGHTS[god] + star.weight + door.weight) / 3;
  
  let globalAuspicious = 0;
  Object.values(chart.doors).forEach(d => {
    if (d && [1, 6, 8].includes(d)) globalAuspicious += 5;
  });
  const isKong = chart.extra.kong.includes(hourPalace) ? -20 : 0;
  
  const scores = {
    wealth: Math.min(100, Math.max(0, Math.round(baseScore + (door.name === '生门' ? 20 : -10)))),
    success: Math.min(100, Math.max(0, Math.round(baseScore + (god === '值符' ? 15 : -5)))),
    relation: Math.min(100, Math.max(0, Math.round(baseScore + (god === '六合' ? 25 : -10)))),
    outcome: Math.min(100, Math.max(0, Math.round(baseScore * 0.7 + globalAuspicious + isKong)))
  };
  
  // 吉方吉色
  const zhiFuPalaceIdx = Object.entries(chart.gods).find(([p, g]) => g === 0)?.[0] || 5;
  const pInfo = PALACE_MAP[zhiFuPalaceIdx];
  const colorMap = { '金': '白/金色', '木': '青/绿色', '水': '黑/蓝色', '火': '红/紫色', '土': '黄/棕色' };
  const guidance = { color: colorMap[pInfo.element], dir: pInfo.dir };
  
  // 秘法推语
  const prefixPool = ["天垂象，圣人则之。", "乾坤挪移，气理相随。", "易理深微，存乎一心。", "大衍之数，定于瞬息。", "阴阳顺逆，妙难穷尽。"];
  const horseWords = chart.extra.ma === hourPalace ?
    ["驿马动转，事多变迁，宜速战速决。", "天马行空，贵人指路，远行大吉。"] :
    ["气场内敛，宜守不宜进，深藏若虚。", "根基稳固，潜龙在渊，宜修身养性。", "时机未至，凡事不可强求，待时而发。"];
  const statusWords = chart.extra.kong.includes(hourPalace) ?
    ["落宫空亡，虚火上升，事多阻碍。", "空中楼阁，梦幻泡影，需脚踏实地。"] :
    ["落宫充实，气势如虹，谋事有根。"];
  const successWords = scores.outcome > 75 ?
    ["顺天应人，谋事易成，此乃上吉之兆。", "如鱼得水，事半功倍，贵人暗中相助。"] :
    scores.outcome > 45 ?
    ["中道而行，虽有小阻，坚持可成。", "云遮雾罩，拨云见日，需有耐心。"] :
    ["阴错阳差，此时不宜大举动工。", "路途艰辛，小心驶得万年船。"];
  
  const randomSeed = Math.floor(Math.random() * 100);
  const secretWords = `${prefixPool[randomSeed % prefixPool.length]}${statusWords[randomSeed % statusWords.length]}${horseWords[randomSeed % horseWords.length]}${successWords[randomSeed % successWords.length]}`;
  
  // 构建输出
  let output = '';
  output += '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n';
  output += '          ☯️ 奇门遁甲盘面分析\n';
  output += '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n';
  
  output += `【四柱】${date.getFullYear()}年 ${gz.m}月 ${gz.d}日 ${gz.h}时\n`;
  output += `【节气】${ju.name} · ${['上元', '中元', '下元'][gz.vals.dZ % 3]}\n`;
  output += `【局制】${ju.type === 'Yang' ? '阳' : '阴'}遁 ${ju.num} 局\n`;
  output += '\n';
  
  output += '┌─────────────────────────────────────┐\n';
  output += '│           四大维度评分              │\n';
  output += '├─────────────────────────────────────┤\n';
  output += `│  💰 财运指数        │    ${scores.wealth.toString().padStart(3)}%    │\n`;
  output += `│  📈 问事成功率      │    ${scores.success.toString().padStart(3)}%    │\n`;
  output += `│  💕 人际/感情      │    ${scores.relation.toString().padStart(3)}%    │\n`;
  output += `│  🎯 结果利多/利好    │    ${scores.outcome.toString().padStart(3)}%    │\n`;
  output += '└─────────────────────────────────────┘\n';
  output += '\n';
  
  output += '【开运建议】\n';
  output += `  🧭 吉方：${guidance.dir}\n`;
  output += `  🎨 吉色：${guidance.color}\n`;
  output += '\n';
  
  output += '【秘法推语】\n';
  output += `  "${secretWords}"\n`;
  output += '\n';
  
  output += '【当前时辰宫位】\n';
  output += `  宫位：${PALACE_MAP[hourPalace].name}宫\n`;
  output += `  九星：${star.name}（${star.type}）\n`;
  output += `  八门：${door ? door.name : '无'}${door ? `（${door.type}）` : ''}\n`;
  output += `  八神：${god}\n`;
  if (chart.extra.ma === hourPalace) output += `  驿马：动迁之象\n`;
  if (chart.extra.kong.includes(hourPalace)) output += `  旬空：空亡待用\n`;
  output += '\n';
  
  output += '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n';
  output += '  奇门之妙在于趋吉避凶，望君审时度势\n';
  output += '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n';
  
  return output;
}

// 主入口
const args = process.argv.slice(2);
let date;

if (args.length > 0) {
  // 解析日期参数
  const dateStr = args.join(' ');
  date = new Date(dateStr);
  if (isNaN(date.getTime())) {
    console.log('日期格式错误，请使用: qimen 2026-03-15 14:30');
    process.exit(1);
  }
} else {
  // 默认当前时间
  date = new Date();
}

console.log(formatOutput(date));
