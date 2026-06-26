#!/usr/bin/env node
/**
 * 奇门遁甲排盘核心引擎
 * 支持时家奇门拆补法
 * 天地人神四盘完整排列
 */

// ========== 基础常量 ==========
const TIAN_GAN = ['甲','乙','丙','丁','戊','己','庚','辛','壬','癸'];
const DI_ZHI = ['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥'];

// 三奇六仪顺序（地盘排列用）：戊己庚辛壬癸丁丙乙
const QI_YI_ORDER = ['戊','己','庚','辛','壬','癸','丁','丙','乙'];

// 甲隐遁对应：甲子→戊, 甲戌→己, 甲申→庚, 甲午→辛, 甲辰→壬, 甲寅→癸
const JIA_DUN = { '甲子':'戊', '甲戌':'己', '甲申':'庚', '甲午':'辛', '甲辰':'壬', '甲寅':'癸' };
const YI_TO_JIA = { '戊':'甲子', '己':'甲戌', '庚':'甲申', '辛':'甲午', '壬':'甲辰', '癸':'甲寅' };

// 洛书九宫飞行顺序（跳过5宫）
const FEI_XING = [1,8,3,4,9,2,7,6];

// 九宫信息
const PALACES = {
  1: { name:'坎', gua:'☵', element:'水', dir:'正北', diZhi:['子'] },
  2: { name:'坤', gua:'☷', element:'土', dir:'西南', diZhi:['未','申'] },
  3: { name:'震', gua:'☳', element:'木', dir:'正东', diZhi:['卯'] },
  4: { name:'巽', gua:'☴', element:'木', dir:'东南', diZhi:['辰','巳'] },
  5: { name:'中', gua:'',  element:'土', dir:'中央', diZhi:[] },
  6: { name:'乾', gua:'☰', element:'金', dir:'西北', diZhi:['戌','亥'] },
  7: { name:'兑', gua:'☱', element:'金', dir:'正西', diZhi:['酉'] },
  8: { name:'艮', gua:'☶', element:'土', dir:'东北', diZhi:['丑','寅'] },
  9: { name:'离', gua:'☲', element:'火', dir:'正南', diZhi:['午'] },
};

// 九星（按原始宫位1-9排列）
const NINE_STARS = {
  1: { name:'天蓬', element:'水', type:'凶', weight:30 },
  2: { name:'天芮', element:'土', type:'凶', weight:20 },
  3: { name:'天冲', element:'木', type:'吉', weight:80 },
  4: { name:'天辅', element:'木', type:'吉', weight:90 },
  5: { name:'天禽', element:'土', type:'吉', weight:100 },
  6: { name:'天心', element:'金', type:'吉', weight:90 },
  7: { name:'天柱', element:'金', type:'凶', weight:40 },
  8: { name:'天任', element:'土', type:'吉', weight:85 },
  9: { name:'天英', element:'火', type:'平', weight:60 },
};

// 八门（按原始宫位排列，5宫无门）
const EIGHT_DOORS = {
  1: { name:'休门', element:'水', type:'吉', weight:90 },
  2: { name:'死门', element:'土', type:'凶', weight:10 },
  3: { name:'伤门', element:'木', type:'凶', weight:30 },
  4: { name:'杜门', element:'木', type:'平', weight:50 },
  6: { name:'开门', element:'金', type:'吉', weight:95 },
  7: { name:'惊门', element:'金', type:'凶', weight:40 },
  8: { name:'生门', element:'土', type:'吉', weight:100 },
  9: { name:'景门', element:'火', type:'平', weight:65 },
};

// 八神
const EIGHT_GODS_YANG = ['值符','腾蛇','太阴','六合','白虎','玄武','九地','九天']; // 阳遁顺排
const EIGHT_GODS_YIN  = ['值符','九天','九地','玄武','白虎','六合','太阴','腾蛇']; // 阴遁逆排
const GOD_INFO = {
  '值符': { type:'吉', weight:100 },
  '腾蛇': { type:'凶', weight:20 },
  '太阴': { type:'吉', weight:80 },
  '六合': { type:'吉', weight:85 },
  '白虎': { type:'凶', weight:10 },
  '玄武': { type:'凶', weight:20 },
  '九地': { type:'平', weight:75 },
  '九天': { type:'吉', weight:90 },
};

// 天干五行
const GAN_ELEMENT = { '甲':'木','乙':'木','丙':'火','丁':'火','戊':'土','己':'土','庚':'金','辛':'金','壬':'水','癸':'水' };

// ========== 节气相关 ==========

// 24节气精确系数（寿星天文算法）
const TERM_INFO = [
  // [月, 日近似系数C, 名称, 是否为"节"(true)或"气"(false)]
  // 从小寒开始，与传统排列一致
  { month:1, name:'小寒', C:5.4055 },
  { month:1, name:'大寒', C:20.12 },
  { month:2, name:'立春', C:3.87 },
  { month:2, name:'雨水', C:18.73 },
  { month:3, name:'惊蛰', C:5.63 },
  { month:3, name:'春分', C:20.646 },
  { month:4, name:'清明', C:4.81 },
  { month:4, name:'谷雨', C:20.1 },
  { month:5, name:'立夏', C:5.52 },
  { month:5, name:'小满', C:21.04 },
  { month:6, name:'芒种', C:5.678 },
  { month:6, name:'夏至', C:21.37 },
  { month:7, name:'小暑', C:7.108 },
  { month:7, name:'大暑', C:22.83 },
  { month:8, name:'立秋', C:7.5 },
  { month:8, name:'处暑', C:23.13 },
  { month:9, name:'白露', C:7.646 },
  { month:9, name:'秋分', C:23.042 },
  { month:10, name:'寒露', C:8.318 },
  { month:10, name:'霜降', C:23.438 },
  { month:11, name:'立冬', C:7.438 },
  { month:11, name:'小雪', C:22.36 },
  { month:12, name:'大雪', C:7.18 },
  { month:12, name:'冬至', C:21.94 },
];

// 节气对应局数 [上元, 中元, 下元]
const TERM_JU = {
  '冬至':[1,7,4], '小寒':[2,8,5], '大寒':[3,9,6],
  '立春':[8,5,2], '雨水':[9,6,3], '惊蛰':[1,7,4],
  '春分':[3,9,6], '清明':[4,1,7], '谷雨':[5,2,8],
  '立夏':[4,1,7], '小满':[5,2,8], '芒种':[6,3,9],
  '夏至':[9,3,6], '小暑':[8,2,5], '大暑':[7,1,4],
  '立秋':[2,5,8], '处暑':[1,4,7], '白露':[9,3,6],
  '秋分':[7,1,4], '寒露':[6,9,3], '霜降':[5,8,2],
  '立冬':[6,9,3], '小雪':[5,8,2], '大雪':[4,7,1],
};

// 阳遁节气（冬至到芒种）
const YANG_TERMS = ['冬至','小寒','大寒','立春','雨水','惊蛰','春分','清明','谷雨','立夏','小满','芒种'];

/**
 * 计算某年某个节气的日期
 * 使用寿星天文算法
 */
function getTermDate(year, termIndex) {
  const info = TERM_INFO[termIndex];
  const y = year % 100;
  const d = 0.2422;
  const l = Math.floor((year % 100) / 4);
  let day = Math.floor(y * d + info.C) - l;
  
  // 特殊年份修正
  if (termIndex === 0 && (year === 2019)) day -= 1; // 小寒
  if (termIndex === 2 && (year === 2026)) day += 0; // 立春
  
  return new Date(year, info.month - 1, day);
}

/**
 * 获取所有节气日期（某年）
 */
function getAllTermDates(year) {
  const terms = [];
  // 上一年的冬至开始
  for (let i = 0; i < 24; i++) {
    terms.push({
      name: TERM_INFO[i].name,
      date: getTermDate(year, i),
      index: i,
    });
  }
  // 补上一年冬至
  const prevWinterIdx = 23;
  terms.unshift({
    name: '冬至',
    date: getTermDate(year - 1, prevWinterIdx),
    index: prevWinterIdx,
    prevYear: true,
  });
  return terms;
}

/**
 * 确定日期所在的节气
 */
function getCurrentTerm(date) {
  const year = date.getFullYear();
  const terms = getAllTermDates(year);
  
  let currentTerm = terms[0];
  for (let i = 1; i < terms.length; i++) {
    if (date >= terms[i].date) {
      currentTerm = terms[i];
    } else {
      break;
    }
  }
  return currentTerm;
}

// ========== 干支计算 ==========

/**
 * 计算四柱干支
 */
function getGanZhi(date) {
  const year = date.getFullYear();
  const month = date.getMonth(); // 0-11
  const day = date.getDate();
  const hour = date.getHours();
  
  // 获取当前节气以确定月柱
  const term = getCurrentTerm(date);
  
  // === 年柱 ===
  // 以立春为界
  const lichunDate = getTermDate(year, 2); // 立春index=2
  const chineseYear = date < lichunDate ? year - 1 : year;
  const yOffset = ((chineseYear - 4) % 60 + 60) % 60;
  const yGan = yOffset % 10;
  const yZhi = yOffset % 12;
  
  // === 月柱 ===
  // 月支按"节"定，按日期顺序排列
  const JIE_DEFS = [
    { termIdx:0,  zhi:1  }, // 小寒→丑
    { termIdx:2,  zhi:2  }, // 立春→寅
    { termIdx:4,  zhi:3  }, // 惊蛰→卯
    { termIdx:6,  zhi:4  }, // 清明→辰
    { termIdx:8,  zhi:5  }, // 立夏→巳
    { termIdx:10, zhi:6  }, // 芒种→午
    { termIdx:12, zhi:7  }, // 小暑→未
    { termIdx:14, zhi:8  }, // 立秋→申
    { termIdx:16, zhi:9  }, // 白露→酉
    { termIdx:18, zhi:10 }, // 寒露→戌
    { termIdx:20, zhi:11 }, // 立冬→亥
    { termIdx:22, zhi:0  }, // 大雪→子
  ];
  // 构建带日期的列表（包括去年大雪），按日期排序
  const jieList = [{ date: getTermDate(year - 1, 22), zhi: 0 }]; // 去年大雪→子月
  for (const jie of JIE_DEFS) {
    jieList.push({ date: getTermDate(year, jie.termIdx), zhi: jie.zhi });
  }
  jieList.sort((a, b) => a.date - b.date);
  let mZhi = 1;
  for (const jie of jieList) {
    if (date >= jie.date) {
      mZhi = jie.zhi;
    } else {
      break;
    }
  }
  // 月干根据年干推算（五虎遁月）
  const mGanBase = [2, 4, 6, 8, 0]; // 甲己→丙, 乙庚→戊, 丙辛→庚, 丁壬→壬, 戊癸→甲
  const mGan = (mGanBase[yGan % 5] + ((mZhi - 2 + 12) % 12)) % 10;
  
  // === 日柱 ===
  // 使用已验证的基准日推算（2024-02-10 = 壬辰日, 壬=8, 辰=4）
  const baseDate = Date.UTC(2024, 1, 10); // 2024-02-10 壬辰日
  const targetDate = Date.UTC(year, month, day);
  const dayDiff = Math.floor((targetDate - baseDate) / 86400000);
  const dGan = ((8 + dayDiff) % 10 + 10) % 10;  // 壬=8
  const dZhi = ((4 + dayDiff) % 12 + 12) % 12;  // 辰=4
  
  // === 时柱 ===
  // 子时23-1, 丑时1-3, ..., 亥时21-23
  let hZhi;
  if (hour >= 23 || hour < 1) hZhi = 0; // 子
  else hZhi = Math.floor((hour + 1) / 2);
  
  // 时干根据日干推算（五鼠遁时）
  const hGanBase = [0, 2, 4, 6, 8]; // 甲己→甲, 乙庚→丙, 丙辛→戊, 丁壬→庚, 戊癸→壬
  const hGan = (hGanBase[dGan % 5] + hZhi) % 10;
  
  return {
    year: TIAN_GAN[yGan] + DI_ZHI[yZhi],
    month: TIAN_GAN[mGan] + DI_ZHI[mZhi],
    day: TIAN_GAN[dGan] + DI_ZHI[dZhi],
    hour: TIAN_GAN[hGan] + DI_ZHI[hZhi],
    vals: { yGan, yZhi, mGan, mZhi, dGan, dZhi, hGan, hZhi },
    termName: term.name,
  };
}

// ========== 定局 ==========

/**
 * 拆补法定局
 * 正确方法：
 * 1. 找节气日期
 * 2. 找节气日期当天或之前最近的符头（甲/己日）
 * 3. 从符头开始每5天一元（上中下）
 * 4. 看当前日在第几元
 * 符头：天干为甲或己的日子
 * 甲子/己卯/甲午/己酉 = 上元符头
 * 甲寅/己巳/甲申/己亥 = 中元符头  
 * 甲辰/己未/甲戌/己丑 = 下元符头
 */
function determineJu(date, gz) {
  const termName = gz.termName;
  const isYang = YANG_TERMS.includes(termName);
  const dunType = isYang ? '阳遁' : '阴遁';
  
  const year = date.getFullYear();
  const month = date.getMonth();
  const day = date.getDate();
  
  // 找节气日期
  const term = getCurrentTerm(date);
  const termDate = term.date;
  
  // 从节气日期往前找最近的符头（甲或己日）
  // 符头 = 天干为甲(0)或己(5)的日子
  const baseDate = Date.UTC(1900, 0, 31); // 甲午日
  
  // 节气日的日干
  const termUTC = Date.UTC(termDate.getFullYear(), termDate.getMonth(), termDate.getDate());
  const termDayDiff = Math.floor((termUTC - baseDate) / 86400000);
  const termDayGan = ((termDayDiff % 10) + 10) % 10;
  
  // 往前找甲(0)或己(5)日
  let fuTouOffset = 0;
  for (let i = 0; i <= 9; i++) {
    const gan = ((termDayGan - i) % 10 + 10) % 10;
    if (gan === 0 || gan === 5) { // 甲或己
      fuTouOffset = i;
      break;
    }
  }
  
  // 符头日期
  const fuTouDate = new Date(termDate);
  fuTouDate.setDate(fuTouDate.getDate() - fuTouOffset);
  
  // 当前日距符头的天数
  const currentUTC = Date.UTC(year, month, day);
  const fuTouUTC = Date.UTC(fuTouDate.getFullYear(), fuTouDate.getMonth(), fuTouDate.getDate());
  const daysSinceFuTou = Math.floor((currentUTC - fuTouUTC) / 86400000);
  
  // 每5天一元
  let yuan;
  if (daysSinceFuTou < 5) {
    yuan = 0; // 上元
  } else if (daysSinceFuTou < 10) {
    yuan = 1; // 中元
  } else {
    yuan = 2; // 下元
  }
  
  const yuanNames = ['上元','中元','下元'];
  const juNums = TERM_JU[termName];
  if (!juNums) {
    console.error(`未找到节气 ${termName} 的局数`);
    return { dunType, yuan: yuanNames[0], juNum: 1, termName };
  }
  
  const juNum = juNums[yuan];
  
  return {
    dunType,
    yuan: yuanNames[yuan],
    juNum,
    termName,
    isYang,
  };
}

// ========== 排盘核心 ==========

/**
 * 排地盘
 * 阳遁：从局数对应宫位开始，按洛书顺序顺排 戊己庚辛壬癸丁丙乙
 * 阴遁：从局数对应宫位开始，按洛书逆序排列
 */
function buildEarthPlate(juNum, isYang) {
  const earth = {};
  const startPalace = juNum;
  
  // 含5宫的完整洛书飞行序列
  // 1→8→3→4→5→9→2→7→6（5宫在4和9之间）
  const FULL_SEQ = [1,8,3,4,5,9,2,7,6];
  
  // 找起始位置
  let startIdx = FULL_SEQ.indexOf(startPalace);
  if (startIdx === -1) startIdx = 0;
  
  if (isYang) {
    // 阳遁顺排
    for (let i = 0; i < 9; i++) {
      const palace = FULL_SEQ[(startIdx + i) % 9];
      earth[palace] = QI_YI_ORDER[i];
    }
  } else {
    // 阴遁逆排
    for (let i = 0; i < 9; i++) {
      const palace = FULL_SEQ[((startIdx - i) % 9 + 9) % 9];
      earth[palace] = QI_YI_ORDER[i];
    }
  }
  
  return earth;
}

/**
 * 洛书九宫下一宫
 * 顺序：1→8→3→4→9→2→7→6→1（跳过5由2代替）
 * 包含5宫的完整顺序：1→8→3→4→(5寄2)→9→2→7→6
 */
function nextPalace(current, forward) {
  // 含5宫的完整飞行序列
  const fullSeq = [1,8,3,4,9,2,7,6];
  // 5宫在4和9之间
  
  if (current === 5) current = 2; // 5宫寄2宫
  
  const idx = fullSeq.indexOf(current);
  if (idx === -1) return 1;
  
  if (forward) {
    return fullSeq[(idx + 1) % 8];
  } else {
    return fullSeq[(idx - 1 + 8) % 8];
  }
}

/**
 * 获取洛书飞行序列中从某宫开始的偏移宫
 */
function getPalaceByOffset(start, offset, forward) {
  if (start === 5) start = 2;
  const idx = FEI_XING.indexOf(start);
  if (idx === -1) return 1;
  
  if (forward) {
    return FEI_XING[(idx + offset) % 8];
  } else {
    return FEI_XING[(idx - offset + 80) % 8];
  }
}

/**
 * 排天盘（九星）
 * 正确逻辑：
 * 1. 找时辰所在旬首（六甲之一）对应的六仪
 * 2. 该六仪在地盘的宫位 = 值符原始宫位
 * 3. 找时干在地盘的宫位 = 值符目标宫位
 * 4. 值符星从原始宫位转到目标宫位
 * 5. 其余星按同样偏移量转动
 */
function buildHeavenPlate(earth, gz, isYang) {
  const hourGan = TIAN_GAN[gz.vals.hGan];
  const hGan = gz.vals.hGan;
  const hZhi = gz.vals.hZhi;
  
  // 1. 找旬首：时辰干支所在旬的甲X
  const xunZhi = ((hZhi - hGan) % 12 + 12) % 12;
  // 旬首地支 → 对应的六仪
  const XUN_TO_YI = { 0:'戊', 10:'己', 8:'庚', 6:'辛', 4:'壬', 2:'癸' };
  const xunYi = XUN_TO_YI[xunZhi] || '戊';
  
  // 2. 旬首六仪在地盘的宫位 = 值符原始宫位
  let zhiFuOrigPalace = null;
  for (const [p, stem] of Object.entries(earth)) {
    if (stem === xunYi) {
      zhiFuOrigPalace = parseInt(p);
      break;
    }
  }
  if (!zhiFuOrigPalace) zhiFuOrigPalace = 1;
  if (zhiFuOrigPalace === 5) zhiFuOrigPalace = 2; // 5宫寄2宫
  
  // 3. 时干在地盘的宫位 = 值符目标宫位
  let hourEarthPalace = null;
  for (const [p, stem] of Object.entries(earth)) {
    if (stem === hourGan) {
      hourEarthPalace = parseInt(p);
      break;
    }
  }
  // 如果时干是甲，甲隐于旬首六仪下，宫位同旬首六仪
  if (hourGan === '甲' || !hourEarthPalace) {
    hourEarthPalace = zhiFuOrigPalace;
  }
  if (hourEarthPalace === 5) hourEarthPalace = 2;
  
  const zhiFuTargetPalace = hourEarthPalace;
  const zhiFuStar = NINE_STARS[zhiFuOrigPalace];
  
  // 4. 计算偏移
  const fromIdx = FEI_XING.indexOf(zhiFuOrigPalace);
  const toIdx = FEI_XING.indexOf(zhiFuTargetPalace);
  const shift = ((toIdx - fromIdx) % 8 + 8) % 8;
  
  // 排天盘星
  const heaven = {};
  const heavenStems = {};
  
  for (let i = 0; i < 8; i++) {
    const origPalace = FEI_XING[i];
    const targetPalace = FEI_XING[(i + shift) % 8];
    heaven[targetPalace] = NINE_STARS[origPalace].name;
    // 天盘干 = 原宫地盘干
    heavenStems[targetPalace] = earth[origPalace];
  }
  
  // 5宫天禽星寄2宫
  // 如果2宫还没有天禽，加入标记
  heaven[5] = '天禽(寄' + (heaven[2] ? '2' : '2') + '宫)';
  heavenStems[5] = earth[5] || earth[2];
  
  return {
    stars: heaven,
    stems: heavenStems,
    zhiFu: {
      star: zhiFuStar.name,
      origPalace: zhiFuOrigPalace,
      targetPalace: zhiFuTargetPalace,
    },
    shift,
  };
}

/**
 * 排人盘（八门）
 * 正确逻辑：
 * 1. 值使门 = 旬首六仪在地盘宫位的本宫门
 * 2. 值使门按时辰前进（从值使起始宫按时辰地支-旬首地支步数前进）
 */
function buildHumanPlate(earth, gz, isYang) {
  const hourGan = TIAN_GAN[gz.vals.hGan];
  const hGan = gz.vals.hGan;
  const hZhi = gz.vals.hZhi;
  
  // 找旬首六仪
  const xunZhi = ((hZhi - hGan) % 12 + 12) % 12;
  const XUN_TO_YI = { 0:'戊', 10:'己', 8:'庚', 6:'辛', 4:'壬', 2:'癸' };
  const xunYi = XUN_TO_YI[xunZhi] || '戊';
  
  // 旬首六仪在地盘的宫位
  let xunPalace = null;
  for (const [p, stem] of Object.entries(earth)) {
    if (stem === xunYi) {
      xunPalace = parseInt(p);
      break;
    }
  }
  if (!xunPalace) xunPalace = 1;
  
  // 值使门 = 旬首宫位的本宫门
  const zhiShiOrigPalace = xunPalace === 5 ? 2 : xunPalace;
  const zhiShiDoor = EIGHT_DOORS[zhiShiOrigPalace];
  
  // 时干在地盘的宫位
  let hourEarthPalace = null;
  for (const [p, stem] of Object.entries(earth)) {
    if (stem === hourGan) {
      hourEarthPalace = parseInt(p);
      break;
    }
  }
  if (hourGan === '甲' || !hourEarthPalace) {
    hourEarthPalace = xunPalace;
  }
  if (hourEarthPalace === 5) hourEarthPalace = 2;
  
  // 值使门前进步数
  // 步数 = 从旬首地支到时辰地支的步数（即时干在旬中的序号）
  const steps = hGan; // 时干序号就是在旬中的位置（甲=0, 乙=1, ..., 癸=9）
  
  // 值使门从原始宫位前进steps步
  let zhiShiTargetPalace = zhiShiOrigPalace;
  for (let i = 0; i < steps; i++) {
    zhiShiTargetPalace = nextPalace(zhiShiTargetPalace, isYang);
    // 跳过5宫
    if (zhiShiTargetPalace === 5) {
      zhiShiTargetPalace = nextPalace(zhiShiTargetPalace, isYang);
    }
  }
  
  // 偏移量
  const fromIdx = FEI_XING.indexOf(zhiShiOrigPalace === 5 ? 2 : zhiShiOrigPalace);
  const toIdx = FEI_XING.indexOf(zhiShiTargetPalace === 5 ? 2 : zhiShiTargetPalace);
  const shift = ((toIdx - fromIdx) % 8 + 8) % 8;
  
  // 排八门
  const doors = {};
  for (let i = 0; i < 8; i++) {
    const origPalace = FEI_XING[i];
    if (!EIGHT_DOORS[origPalace]) continue;
    const targetPalace = FEI_XING[(i + shift) % 8];
    doors[targetPalace] = EIGHT_DOORS[origPalace].name;
  }
  
  return {
    doors,
    zhiShi: {
      door: zhiShiDoor ? zhiShiDoor.name : '死门',
      origPalace: zhiShiOrigPalace,
      targetPalace: zhiShiTargetPalace,
    },
    shift,
  };
}

/**
 * 排神盘（八神）
 * 值符神在值符星所在宫
 * 阳遁：从值符宫顺排 值符→腾蛇→太阴→六合→白虎→玄武→九地→九天
 * 阴遁：从值符宫逆排 值符→九天→九地→玄武→白虎→六合→太阴→腾蛇
 */
function buildGodPlate(zhiFuPalace, isYang) {
  const godOrder = isYang ? EIGHT_GODS_YANG : EIGHT_GODS_YIN;
  const gods = {};
  
  let palace = zhiFuPalace === 5 ? 2 : zhiFuPalace;
  
  for (let i = 0; i < 8; i++) {
    gods[palace] = godOrder[i];
    if (isYang) {
      palace = nextPalace(palace, true);
    } else {
      palace = nextPalace(palace, false);
    }
    if (palace === 5) {
      palace = isYang ? nextPalace(palace, true) : nextPalace(palace, false);
    }
  }
  
  return { gods };
}

// ========== 空亡和马星 ==========

/**
 * 计算空亡宫位
 */
function getKongWang(dGan, dZhi) {
  // 日干支所在旬的空亡地支
  const xunZhi = ((dZhi - dGan) % 12 + 12) % 12;
  // 空亡 = 旬中未配到的两个地支
  // 甲子旬(0): 空亡戌(10)亥(11)
  // 甲戌旬(10): 空亡申(8)酉(9)
  // 甲申旬(8): 空亡午(6)未(7)
  // 甲午旬(6): 空亡辰(4)巳(5)
  // 甲辰旬(4): 空亡寅(2)卯(3)
  // 甲寅旬(2): 空亡子(0)丑(1)
  const kongZhi1 = (xunZhi + 10) % 12;
  const kongZhi2 = (xunZhi + 11) % 12;
  
  // 地支对应宫位
  const zhiToPalace = {
    0:1, 1:8, 2:8, 3:3, 4:4, 5:4,
    6:9, 7:2, 8:2, 9:7, 10:6, 11:6
  };
  
  const palaces = new Set();
  palaces.add(zhiToPalace[kongZhi1]);
  palaces.add(zhiToPalace[kongZhi2]);
  
  return {
    diZhi: [DI_ZHI[kongZhi1], DI_ZHI[kongZhi2]],
    palaces: [...palaces],
  };
}

/**
 * 计算马星（驿马）
 */
function getHorse(dZhi) {
  // 申子辰→驿马寅(8宫), 寅午戌→驿马申(2宫)
  // 巳酉丑→驿马亥(6宫), 亥卯未→驿马巳(4宫)
  const groups = {
    '申子辰': { zhi: [8,0,4], horse: 2, horsePalace: 8 },  // 寅在艮8宫
    '寅午戌': { zhi: [2,6,10], horse: 8, horsePalace: 2 }, // 申在坤2宫
    '巳酉丑': { zhi: [5,9,1], horse: 11, horsePalace: 6 }, // 亥在乾6宫
    '亥卯未': { zhi: [11,3,7], horse: 5, horsePalace: 4 }, // 巳在巽4宫
  };
  
  for (const [name, info] of Object.entries(groups)) {
    if (info.zhi.includes(dZhi)) {
      return {
        diZhi: DI_ZHI[info.horse],
        palace: info.horsePalace,
      };
    }
  }
  return { diZhi: '寅', palace: 8 };
}

// ========== 六仪击刑 ==========
/**
 * 判断六仪击刑
 * 戊在震3(卯)受刑(子卯刑), 己在坎1(子)受刑(子卯刑)... 等
 * 具体规则：
 * 戊+震3宫(卯): 子卯之刑
 * 己+坎1宫(子): 子卯之刑  [待验证]
 * 庚+艮8宫(丑寅): 丑戌之刑
 * 辛+离9宫(午): 午午自刑
 * 壬+巽4宫(巳): 寅巳之刑
 * 癸+巽4宫(巳): 寅巳之刑  [待验证]
 */
function checkLiuYiJiXing(earthPlate) {
  const xingRules = [
    { stem:'戊', palace:3, desc:'子卯之刑' },
    { stem:'庚', palace:8, desc:'丑未戌之刑' },
    { stem:'辛', palace:9, desc:'午午自刑' },
    { stem:'壬', palace:4, desc:'寅巳之刑' },
    { stem:'癸', palace:4, desc:'寅巳之刑' },
  ];
  
  const results = [];
  for (const rule of xingRules) {
    if (earthPlate[rule.palace] === rule.stem) {
      results.push(rule);
    }
  }
  return results;
}

// ========== 主排盘函数 ==========

/**
 * 完整排盘
 * @param {string|Date} dateInput - 日期时间
 * @returns {object} 完整盘面数据
 */
function calculate(dateInput) {
  let date;
  if (typeof dateInput === 'string') {
    date = new Date(dateInput);
  } else if (dateInput instanceof Date) {
    date = dateInput;
  } else {
    date = new Date();
  }
  
  if (isNaN(date.getTime())) {
    throw new Error('无效的日期格式');
  }
  
  // 1. 四柱干支
  const gz = getGanZhi(date);
  
  // 2. 定局
  const ju = determineJu(date, gz);
  
  // 3. 排地盘
  const earth = buildEarthPlate(ju.juNum, ju.isYang);
  
  // 4. 排天盘
  const heavenResult = buildHeavenPlate(earth, gz, ju.isYang);
  
  // 5. 排人盘（八门）
  const humanResult = buildHumanPlate(earth, gz, ju.isYang);
  
  // 6. 排神盘
  const godResult = buildGodPlate(heavenResult.zhiFu.targetPalace, ju.isYang);
  
  // 7. 空亡和马星
  const kongWang = getKongWang(gz.vals.dGan, gz.vals.dZhi);
  const horse = getHorse(gz.vals.dZhi);
  
  // 8. 六仪击刑
  const jiXing = checkLiuYiJiXing(earth);
  
  // 9. 组装宫位数据
  const palaces = {};
  for (let i = 1; i <= 9; i++) {
    const flags = [];
    if (kongWang.palaces.includes(i)) flags.push('空');
    if (horse.palace === i) flags.push('马');
    if (jiXing.some(j => j.palace === i)) flags.push('刑');
    
    palaces[i] = {
      position: PALACES[i].name,
      direction: PALACES[i].dir,
      element: PALACES[i].element,
      earthStem: earth[i] || '',
      heavenStem: heavenResult.stems[i] || '',
      star: heavenResult.stars[i] || '',
      door: humanResult.doors[i] || '',
      god: godResult.gods[i] || '',
      flags,
    };
  }
  
  return {
    datetime: {
      year: date.getFullYear(),
      month: date.getMonth() + 1,
      day: date.getDate(),
      hour: date.getHours(),
      minute: date.getMinutes(),
      formatted: `${date.getFullYear()}年${date.getMonth()+1}月${date.getDate()}日 ${date.getHours()}:${String(date.getMinutes()).padStart(2,'0')}`,
    },
    ganZhi: gz,
    solarTerm: gz.termName,
    yuan: ju.yuan,
    dunType: ju.dunType,
    juNum: ju.juNum,
    isYang: ju.isYang,
    method: '拆补法',
    palaces,
    zhiFu: heavenResult.zhiFu,
    zhiShi: humanResult.zhiShi,
    horse,
    kongWang,
    jiXing,
    earth,
    heavenStems: heavenResult.stems,
  };
}

module.exports = { calculate, PALACES, NINE_STARS, EIGHT_DOORS, GOD_INFO, GAN_ELEMENT, TIAN_GAN, DI_ZHI, FEI_XING, QI_YI_ORDER };
