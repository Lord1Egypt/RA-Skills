/**
 * 紫微斗数 Skill - 核心算法
 * 作者：天工长老
 * 版本：v1.1
 * 创建：2026 年 3 月 29 日
 * 更新：2026 年 3 月 30 日 - 添加辅星、流年功能
 */

// 十四主星
const ZHU_XING = [
  '紫微', '天机', '太阳', '武曲', '天同', '廉贞',
  '天府', '太阴', '贪狼', '巨门', '天相', '天梁', '七杀', '破军'
];

// 星曜基本含义（简化版）
const XING_YAO_HAN_YI = {
  '紫微': { 五行：'土', 特性：'帝王之星，尊贵、领导力', 吉凶：'吉' },
  '天机': { 五行：'木', 特性：'智慧之星，聪明、善变', 吉凶：'吉' },
  '太阳': { 五行：'火', 特性：'光明之星，热情、博爱', 吉凶：'吉' },
  '武曲': { 五行：'金', 特性：'财星，刚毅、执行力', 吉凶：'吉' },
  '天同': { 五行：'水', 特性：'福星，温和、享乐', 吉凶：'吉' },
  '廉贞': { 五行：'火', 特性：'囚星，复杂、桃花', 吉凶': '凶' },
  '天府': { 五行：'土', 特性：'库星，稳重、保守', 吉凶：'吉' },
  '太阴': { 五行：'水', 特性：'月星，温柔、内敛', 吉凶：'吉' },
  '贪狼': { 五行：'木', 特性：'桃花星，欲望、交际', 吉凶': '凶' },
  '巨门': { 五行：'土', 特性：'暗星，口舌、是非', 吉凶': '凶' },
  '天相': { 五行：'水', 特性：'印星，辅佐、公正', 吉凶：'吉' },
  '天梁': { 五行：'土', 特性：'荫星，长寿、解厄', 吉凶：'吉' },
  '七杀': { 五行：'金', 特性：'将星，刚烈、变动', 吉凶': '凶' },
  '破军': { 五行：'水', 特性：'耗星，破坏、创新', 吉凶': '凶' }
};

// 十二宫位
const GONG_WEI = [
  '命宫', '兄弟宫', '夫妻宫', '子女宫', '财帛宫', '疾厄宫',
  '迁移宫', '交友宫', '官禄宫', '田宅宫', '福德宫', '父母宫'
];

// 四化
const SI_HUA = ['化禄', '化权', '化科', '化忌'];

// 年干四化表
const NIAN_GAN_SI_HUA = {
  '甲': ['廉贞化禄', '破军化权', '武曲化科', '太阳化忌'],
  '乙': ['天机化禄', '天梁化权', '紫微化科', '太阴化忌'],
  '丙': ['天同化禄', '天机化权', '文昌化科', '廉贞化忌'],
  '丁': ['太阴化禄', '天同化权', '天机化科', '巨门化忌'],
  '戊': ['贪狼化禄', '太阴化权', '右弼化科', '天机化忌'],
  '己': ['武曲化禄', '贪狼化权', '天梁化科', '文曲化忌'],
  '庚': ['太阳化禄', '武曲化权', '太阴化科', '天同化忌'],
  '辛': ['巨门化禄', '太阳化权', '文曲化科', '文昌化忌'],
  '壬': ['天梁化禄', '紫微化权', '左辅化科', '武曲化忌'],
  '癸': ['破军化禄', '巨门化权', '太阴化科', '贪狼化忌']
};

// 天干
const TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];

// 地支
const DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];

// 简化排盘算法（第一版）
function paiPan(year, month, day, hour) {
  // 计算年干
  const ganIndex = (year - 4) % 10;
  const yearGan = TIAN_GAN[ganIndex >= 0 ? ganIndex : ganIndex + 10];
  
  // 简化：以出生年地支为命宫起点
  const zhiIndex = (year - 4) % 12;
  const mingGongIndex = zhiIndex >= 0 ? zhiIndex : zhiIndex + 12;
  
  // 排十四主星（简化：按顺序排布）
  const starStart = (year + month + day) % 14;
  const stars = [];
  for (let i = 0; i < 14; i++) {
    stars.push(ZHU_XING[(starStart + i) % 14]);
  }
  
  // 排十二宫位
  const gongWeiList = [];
  for (let i = 0; i < 12; i++) {
    const gongIndex = (mingGongIndex + i) % 12;
    gongWeiList.push({
      宫位：GONG_WEI[i],
      地支：DI_ZHI[gongIndex],
      主星：stars[i] || '无'
    });
  }
  
  // 四化
  const siHua = NIAN_GAN_SI_HUA[yearGan] || [];
  
  return {
    命宫位置：mingGongIndex,
    年干：yearGan,
    十四主星：stars,
    十二宫位：gongWeiList,
    四化：siHua
  };
}

// 简批断语
function jianPi(gongWeiList, siHua) {
  const piYu = [];
  
  // 找命宫主星
  const mingGong = gongWeiList.find(g => g.宫位 === '命宫');
  if (mingGong) {
    const xingYao = XING_YAO_HAN_YI[mingGong.主星];
    if (xingYao) {
      piYu.push(`命宫${mingGong.主星}：${xingYao.特性}`);
    }
  }
  
  // 找财帛宫
  const caiBoGong = gongWeiList.find(g => g.宫位 === '财帛宫');
  if (caiBoGong) {
    piYu.push(`财帛${caiBoGong.主星}：财运${caiBoGong.主星 === '武曲' ? '旺盛' : '平稳'}`);
  }
  
  // 找夫妻宫
  const fuQiGong = gongWeiList.find(g => g.宫位 === '夫妻宫');
  if (fuQiGong) {
    piYu.push(`夫妻${fuQiGong.主星}：婚姻${fuQiGong.主星 === '天同' ? '和睦' : '需用心经营'}`);
  }
  
  // 四化影响
  if (siHua.length > 0) {
    piYu.push(`四化：${siHua.join('，')}`);
  }
  
  return piYu;
}

// 综合紫微斗数分析
function ziWeiDouShu(year, month, day, hour, gender) {
  const pan = paiPan(year, month, day, hour);
  const piYu = jianPi(pan.十二宫位，pan.四化);
  
  return {
    出生信息：{
      公历：`${year}年${month}月${day}日${hour}时`,
      性别：gender === 'male' ? '男' : '女'
    },
    命盘：pan,
    简批：piYu
  };
}

// ========== v1.1 新增：辅星系统 ==========

// 六吉星
const LIU_JI_XING = ['左辅', '右弼', '文昌', '文曲', '天魁', '天钺'];

// 六煞星
const LIU_SHA_XING = ['擎羊', '陀罗', '火星', '铃星', '地空', '地劫'];

// 四化星（简化版）
const SI_HUA = {
  甲：['廉贞化禄', '破军化权', '武曲化科', '太阳化忌'],
  乙：['天机化禄', '天梁化权', '紫微化科', '太阴化忌'],
  丙：['天同化禄', '天机化权', '文昌化科', '廉贞化忌'],
  丁：['太阴化禄', '天同化权', '天机化科', '巨门化忌'],
  戊：['贪狼化禄', '太阴化权', '右弼化科', '天机化忌'],
  己：['武曲化禄', '贪狼化权', '天梁化科', '文曲化忌'],
  庚：['太阳化禄', '武曲化权', '太阴化科', '天同化忌'],
  辛：['巨门化禄', '太阳化权', '文曲化科', '文昌化忌'],
  壬：['天梁化禄', '紫微化权', '左辅化科', '武曲化忌'],
  癸：['破军化禄', '巨门化权', '太阴化科', '贪狼化忌']
};

// 计算四化
function getSiHua(year) {
  const ganIndex = (year - 4) % 10;
  const gan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'][ganIndex];
  return { 年干：gan, 四化：SI_HUA[gan] };
}

// 流年排盘（简化版）
function getLiuNian(year, basePan) {
  const liuNianGong = (year - 1900) % 12;
  const liuNianGongName = GONG_WEI[liuNianGong];
  
  return {
    流年宫位：liuNianGongName,
    流年天干：getSiHua(year).年干，
    流年四化：getSiHua(year).四化，
    流年运势：'需结合本命盘详细分析'
  };
}

// 导出
module.exports = {
  ziWeiDouShu,
  paiPan,
  jianPi,
  // v1.1 新增
  getSiHua,
  getLiuNian,
  LIU_JI_XING,
  LIU_SHA_XING,
  SI_HUA,
  // 原有
  XING_YAO_HAN_YI,
  GONG_WEI,
  ZHU_XING
};
