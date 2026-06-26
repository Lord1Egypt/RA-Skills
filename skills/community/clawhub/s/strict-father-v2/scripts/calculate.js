#!/usr/bin/env node

/**
 * 紫微斗数排盘脚本 - strict-father skill
 * 基于 iztro 引擎
 * 
 * 用法: node calculate.js <出生日期> <出生时间> <性别>
 * 示例: node calculate.js 1956-09-12 16:00 男
 * 输出: 结构化JSON命盘
 */

const iztro = require('iztro');
const { astro } = iztro;

function calculateChart(solarDate, timeStr, gender) {
  // 解析时辰
  const [h, m] = timeStr.split(':').map(Number);
  const totalMinutes = h * 60 + m;
  
  // 时辰映射:
  // 子时初 23:00-00:59 = 0
  // 丑时 01:00-02:59 = 1
  // 寅时 03:00-04:59 = 2
  // 卯时 05:00-06:59 = 3
  // 辰时 07:00-08:59 = 4
  // 巳时 09:00-10:59 = 5
  // 午时 11:00-12:59 = 6
  // 未时 13:00-14:59 = 7
  // 申时 15:00-16:59 = 8
  // 酉时 17:00-18:59 = 9
  // 戌时 19:00-20:59 = 10
  // 亥时 21:00-22:59 = 11
  // 子时末 23:00-00:00 = 12
  
  let timeIndex;
  if (totalMinutes >= 23 * 60 || totalMinutes < 1 * 60) timeIndex = 0;
  else if (totalMinutes < 3 * 60) timeIndex = 1;
  else if (totalMinutes < 5 * 60) timeIndex = 2;
  else if (totalMinutes < 7 * 60) timeIndex = 3;
  else if (totalMinutes < 9 * 60) timeIndex = 4;
  else if (totalMinutes < 11 * 60) timeIndex = 5;
  else if (totalMinutes < 13 * 60) timeIndex = 6;
  else if (totalMinutes < 15 * 60) timeIndex = 7;
  else if (totalMinutes < 17 * 60) timeIndex = 8;
  else if (totalMinutes < 19 * 60) timeIndex = 9;
  else if (totalMinutes < 21 * 60) timeIndex = 10;
  else timeIndex = 11;
  
  try {
    const r = astro.bySolar(solarDate, timeIndex, gender);
    
    // 结构化输出
    const chart = {
      gender: r.gender,
      solarDate: r.solarDate,
      lunarDate: r.lunarDate,
      chineseDate: r.chineseDate,
      sign: r.sign,
      zodiac: r.zodiac,
      fiveElementsClass: r.fiveElementsClass,
      soul: r.soul,
      body: r.body,
      palaces: r.palaces.map(p => ({
        name: p.name,
        heavenlyStem: p.heavenlyStem,
        earthlyBranch: p.earthlyBranch,
        isBodyPalace: p.isBodyPalace,
        positions: p.positions,
        majorStars: (p.majorStars || []).map(s => ({
          name: s.name,
          type: s.type,
          scope: s.scope || null,
          mutagen: s.mutagen || [],
          isBright: s.isBright
        })),
        minorStars: (p.minorStars || []).map(s => ({
          name: s.name,
          type: s.type,
          scope: s.scope || null,
          mutagen: s.mutagen || [],
          isBright: s.isBright
        }))
      }))
    };
    
    return chart;
  } catch (e) {
    return { error: e.message };
  }
}

// CLI entry point
const args = process.argv.slice(2);
if (args.length < 3) {
  console.log(JSON.stringify({
    usage: "node calculate.js <出生日期> <出生时间> <性别>",
    example: "node calculate.js 1956-09-12 16:00 男",
    note: "时间格式: HH:mm，性别: 男/女",
    error: "缺少参数"
  }));
  process.exit(1);
}

const [solarDate, timeStr, gender] = args;
const result = calculateChart(solarDate, timeStr, gender);
console.log(JSON.stringify(result, null, 2));
