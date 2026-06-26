#!/usr/bin/env node
/**
 * 六星占術 v2.0 — 多语言版本
 * 细木数子 1980年创立
 * 用法: node rokusei.js <year> <month> <day> [--lang zh|en|ja] [--json]
 */

const { Lunar } = require('lunar-typescript');
const i18n = require('./i18n');

const TIAN_GAN = ['甲','乙','丙','丁','戊','己','庚','辛','壬','癸'];
const DI_ZHI = ['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥'];

function getStarNumber(year, month, day) {
  const lunar = Lunar.fromYmdHms(year, month, day, 12, 0, 0);
  const dayGanZhi = lunar.getDayInGanZhi();
  let idx = 0;
  for (let i = 0; i < 60; i++) {
    if (TIAN_GAN[i % 10] === dayGanZhi[0] && DI_ZHI[i % 12] === dayGanZhi[1]) { idx = i + 1; break; }
  }
  return { ganZhi: dayGanZhi, starNumber: idx };
}

function getStarType(starNumber) {
  if (starNumber >= 1 && starNumber <= 10) return '土星';
  if (starNumber >= 11 && starNumber <= 20) return '金星';
  if (starNumber >= 21 && starNumber <= 30) return '火星';
  if (starNumber >= 31 && starNumber <= 40) return '天王星';
  if (starNumber >= 41 && starNumber <= 50) return '木星';
  if (starNumber >= 51 && starNumber <= 60) return '水星';
  return '未知';
}

function getPolarity(year) {
  const lunar = Lunar.fromYmd(year, 1, 1);
  const yearBranch = lunar.getYearInGanZhi()[1];
  return DI_ZHI.indexOf(yearBranch) % 2 === 0 ? '+' : '-';
}

function isReigoSeijin(starType, year) {
  const lunar = Lunar.fromYmd(year, 1, 1);
  const yearBranch = lunar.getYearInGanZhi()[1];
  const kongWangMap = { 土星:['戌','亥'], 金星:['申','酉'], 火星:['午','未'], 天王星:['辰','巳'], 木星:['寅','卯'], 水星:['子','丑'] };
  return (kongWangMap[starType] || []).includes(yearBranch);
}

function getCyclePhase(year, currentYear) {
  const age = currentYear - year;
  return { ...i18n.cyclePhases[age % 12], position: age % 12, age };
}

function getShukumei(year, currentYear) {
  const age = currentYear - year;
  return i18n.shukumei[Math.floor(age / 10) % 10];
}

function generateChart(year, month, day, lang = 'zh') {
  const currentYear = new Date().getFullYear();
  const { ganZhi, starNumber } = getStarNumber(year, month, day);
  const starType = getStarType(starNumber);
  const polarity = getPolarity(year);
  const isReigo = isReigoSeijin(starType, year);
  const starData = i18n.starTypes[starType]?.[lang] || i18n.starTypes[starType]?.zh;
  const labels = i18n.labels[lang] || i18n.labels.zh;
  const oppositeStarKey = i18n.oppositeStar[starType];
  const oppositeData = i18n.starTypes[oppositeStarKey]?.[lang] || i18n.starTypes[oppositeStarKey]?.zh;
  const cyclePhase = getCyclePhase(year, currentYear);
  const shukumei = getShukumei(year, currentYear);
  const warnings = i18n.warnings[lang] || i18n.warnings.zh;
  const compat = i18n.compatibility[lang] || i18n.compatibility.zh;

  const cycleLocalized = {
    name: cyclePhase.name[lang] || cyclePhase.name.zh,
    roman: cyclePhase.roman,
    desc: cyclePhase.desc[lang] || cyclePhase.desc.zh,
    advice: cyclePhase.advice[lang] || cyclePhase.advice.zh,
    fortune: cyclePhase.fortune?.[lang] || cyclePhase.fortune?.zh || '★★★',
    position: cyclePhase.position,
    age: cyclePhase.age,
  };

  const warningKey = i18n.cyclePhases[cyclePhase.position]?.name?.zh;

  // Get compatibility for this star type with all others
  const compatKey = `${starType}-${oppositeStarKey}`;
  const compatResult = compat[compatKey] || '';

  return {
    input: { year, month, day }, lang, ganZhi, starNumber, starType, starData, polarity,
    polarityLabel: polarity === '+' ? labels.polarityPos : labels.polarityNeg,
    fullStarName: polarity === '+' ? starData.polarity_pos : starData.polarity_neg,
    isReigo, oppositeStar: oppositeStarKey, oppositeData,
    personality: starData.personality, career: starData.career, love: starData.love, advice: starData.advice,
    lucky: starData.lucky, weakness: starData.weakness, strength: starData.strength,
    cyclePhase: cycleLocalized,
    shukumei: { name: shukumei.name, en: shukumei.en, desc: shukumei.desc[lang] || shukumei.desc.zh },
    currentAge: currentYear - year,
    warning: warnings[warningKey] || null,
    labels, compatibility: compatResult,
    oppositeInfo: { starType: oppositeStarKey, polarity: polarity === '+' ? '-' : '+', description: oppositeData?.description || '' },
    getPhaseForYear(y) {
      const p = getCyclePhase(year, y);
      const w = i18n.warnings[lang] || i18n.warnings.zh;
      const pKey = i18n.cyclePhases[p.position]?.name?.zh;
      return { ...p, name: p.name[lang] || p.name.zh, desc: p.desc[lang] || p.desc.zh, advice: p.advice[lang] || p.advice.zh, fortune: p.fortune?.[lang] || p.fortune?.zh || '★★★', warning: w[pKey] || null };
    },
  };
}

if (require.main === module) {
  const args = process.argv.slice(2);
  let lang = 'zh', json = false, positional = [];
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--lang' && args[i+1]) { lang = args[++i]; }
    else if (args[i] === '--json') { json = true; }
    else if (args[i] === '--help' || args[i] === '-h') { console.log('Usage: node rokusei.js <year> <month> <day> [--lang zh|en|ja] [--json]'); process.exit(0); }
    else { positional.push(args[i]); }
  }
  if (positional.length < 3) { console.log('Usage: node rokusei.js <year> <month> <day> [--lang zh|en|ja] [--json]'); process.exit(1); }
  const [year, month, day] = positional.map(Number);
  const chart = generateChart(year, month, day, lang);
  if (json) {
    const out = { ...chart, starData: undefined, getPhaseForYear: undefined };
    console.log(JSON.stringify(out, null, 2));
  } else {
    const L = chart.labels;
    console.log(`\n═══ ${L.title} ═══`);
    console.log(`${L.date}: ${chart.input.year}/${chart.input.month}/${chart.input.day}`);
    console.log(`${L.dayPillar}: ${chart.ganZhi} | ${L.starNumber}: ${chart.starNumber}/60`);
    console.log(`${L.starType}: ${chart.fullStarName}`);
    if (chart.isReigo) console.log(`🌟 ${L.reigo}`);
    console.log(`\n── ${chart.starData.icon} ${chart.starData.summary} ──`);
    console.log(`${L.personality}: ${chart.personality}`);
    console.log(`${L.strength}: ${chart.strength}`);
    console.log(`${L.weakness}: ${chart.weakness}`);
    console.log(`${L.career}: ${chart.career}`);
    console.log(`${L.love}: ${chart.love}`);
    console.log(`${L.advice}: ${chart.advice}`);
    if (chart.lucky) {
      console.log(`\n🍀 ${L.lucky}:`);
      console.log(`  ${lang==='ja'?'色':lang==='en'?'Color':'颜色'}: ${chart.lucky.color.join(', ')} | ${lang==='ja'?'方向':lang==='en'?'Direction':'方向'}: ${chart.lucky.direction} | ${lang==='ja'?'数字':lang==='en'?'Numbers':'数字'}: ${chart.lucky.number.join(', ')} | ${lang==='ja'?'季節':lang==='en'?'Season':'季节'}: ${chart.lucky.season}`);
    }
    if (chart.compatibility) console.log(`\n💕 ${L.compatibility}: ${chart.compatibility}`);
    console.log(`\n🔄 ${L.cycle}: ${chart.cyclePhase.name}（${chart.cyclePhase.roman}）${chart.cyclePhase.fortune}`);
    console.log(`  ${chart.cyclePhase.desc}`);
    console.log(`  💡 ${chart.cyclePhase.advice}`);
    console.log(`\n🌟 ${L.shukumei}: ${chart.shukumei.name} (${chart.shukumei.en})`);
    console.log(`  ${chart.shukumei.desc}`);
    console.log(`\n↔️ ${L.opposite}: ${chart.oppositeStar}`);
    if (chart.warning) console.log(`\n${chart.warning}`);
    console.log('');
  }
}

module.exports = { generateChart, getStarNumber, getStarType, getPolarity, i18n };
