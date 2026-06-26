/**
 * 奇门遁甲 - 精美九宫格格式化输出模块
 * 支持终端文本和飞书消息格式
 */

const { PALACES, NINE_STARS, EIGHT_DOORS, GOD_INFO, GAN_ELEMENT } = require('./engine.js');

// ========== 字符宽度工具 ==========

/** 计算字符串显示宽度（CJK字符宽度2） */
function strWidth(str) {
  let w = 0;
  for (const ch of str) {
    const code = ch.codePointAt(0);
    // CJK范围 + 特殊符号（☵☷☳☴☰☱☶☲ 等）
    if ((code >= 0x2E80 && code <= 0x9FFF) || 
        (code >= 0xF900 && code <= 0xFAFF) ||
        (code >= 0x20000 && code <= 0x2FA1F) ||
        (code >= 0x2600 && code <= 0x27BF) ||  // Misc symbols
        (code >= 0x2190 && code <= 0x21FF)) {   // Arrows
      w += 2;
    } else if (code > 0x7f) {
      w += 2;
    } else {
      w += 1;
    }
  }
  return w;
}

/** 右填充到指定显示宽度 */
function padEnd(str, targetWidth) {
  const cur = strWidth(str);
  const padding = Math.max(0, targetWidth - cur);
  return str + ' '.repeat(padding);
}

/** 居中填充到指定显示宽度 */
function padCenter(str, targetWidth) {
  const cur = strWidth(str);
  const total = Math.max(0, targetWidth - cur);
  const left = Math.floor(total / 2);
  const right = total - left;
  return ' '.repeat(left) + str + ' '.repeat(right);
}

// ========== 九宫格 ==========

// 传统排列：4-9-2 / 3-5-7 / 8-1-6（洛书九宫）
const GRID_ROWS = [[4, 9, 2], [3, 5, 7], [8, 1, 6]];
const COL_WIDTH = 24; // 每列显示宽度

/**
 * 构建单宫格内容（6行）
 */
function buildPalaceLines(palace, palaceNum) {
  const info = PALACES[palaceNum];
  const lines = [];
  
  if (palaceNum === 5) {
    // 中5宫特殊处理
    lines.push(`${info.name}${palaceNum}宫 ${info.dir}`);
    lines.push('天禽(寄2宫)');
    lines.push('');
    lines.push('');
    lines.push(`天:${palace.heavenStem || '乙'} 地:${palace.earthStem || '乙'}`);
    lines.push('');
    return lines;
  }
  
  // 行1: 宫名+方位
  lines.push(`${info.name}${palaceNum}宫 ${info.dir}`);
  
  // 行2: 九星
  lines.push(palace.star || '');
  
  // 行3: 八门
  lines.push(palace.door || '');
  
  // 行4: 八神
  lines.push(palace.god || '');
  
  // 行5: 天地盘干
  lines.push(`天:${palace.heavenStem} 地:${palace.earthStem}`);
  
  // 行6: 标记（空亡、马星、刑等）
  const flags = [];
  if (palace.flags.includes('空')) flags.push('空');
  if (palace.flags.includes('马')) flags.push('马');
  if (palace.flags.includes('刑')) flags.push('刑');
  lines.push(flags.length > 0 ? flags.map(f => `[${f}]`).join('') : '');
  
  return lines;
}

/**
 * 格式化九宫格（纯文本）
 */
function formatGrid(chart) {
  const w = COL_WIDTH;
  let out = '';
  
  const hLine = '─'.repeat(w);
  out += '┌' + hLine + '┬' + hLine + '┬' + hLine + '┐\n';
  
  for (let r = 0; r < 3; r++) {
    const palNums = GRID_ROWS[r];
    const cols = palNums.map(n => buildPalaceLines(chart.palaces[n], n));
    
    // 6行内容
    for (let line = 0; line < 6; line++) {
      out += '│';
      for (let c = 0; c < 3; c++) {
        const text = cols[c][line] || '';
        out += ' ' + padEnd(text, w - 1) + '│';
      }
      out += '\n';
    }
    
    // 分隔线
    if (r < 2) {
      out += '├' + hLine + '┼' + hLine + '┼' + hLine + '┤\n';
    }
  }
  
  out += '└' + hLine + '┴' + hLine + '┴' + hLine + '┘\n';
  return out;
}

/**
 * 格式化头部信息
 */
function formatHeader(chart) {
  let out = '';
  out += '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n';
  out += '          ☯️  奇门遁甲排盘\n';
  out += '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n';
  
  out += `【时间】${chart.datetime.formatted}\n`;
  out += `【四柱】${chart.ganZhi.year}年 ${chart.ganZhi.month}月 ${chart.ganZhi.day}日 ${chart.ganZhi.hour}时\n`;
  out += `【节气】${chart.solarTerm} · ${chart.yuan}\n`;
  out += `【局制】${chart.dunType} ${chart.juNum} 局（${chart.method}）\n`;
  out += `【值符】${chart.zhiFu.star}（${chart.zhiFu.targetPalace}宫）\n`;
  out += `【值使】${chart.zhiShi.door}（${chart.zhiShi.targetPalace}宫）\n`;
  out += `【空亡】${chart.kongWang.diZhi.join('、')}（${chart.kongWang.palaces.join('、')}宫）\n`;
  out += `【马星】${chart.horse.diZhi}（${chart.horse.palace}宫）\n`;
  if (chart.jiXing && chart.jiXing.length > 0) {
    out += `【击刑】${chart.jiXing.map(j => j.stem + '在' + j.palace + '宫(' + j.desc + ')').join('、')}\n`;
  }
  out += '\n';
  return out;
}

/**
 * 格式化格局分析
 */
function formatGejus(gejuResult) {
  if (!gejuResult) return '';
  
  let out = '【格局分析】\n';
  
  if (gejuResult.auspicious.length > 0) {
    out += '🟢 吉格:\n';
    for (const g of gejuResult.auspicious) {
      out += `  ✦ ${g.name}（${g.palace}宫）`;
      if (g.desc) out += `: ${g.desc}`;
      out += '\n';
    }
  } else {
    out += '🟢 吉格: 无\n';
  }
  
  if (gejuResult.inauspicious.length > 0) {
    out += '🔴 凶格:\n';
    for (const g of gejuResult.inauspicious) {
      out += `  ✧ ${g.name}（${g.palace}宫）`;
      if (g.desc) out += `: ${g.desc}`;
      out += '\n';
    }
  } else {
    out += '🔴 凶格: 无\n';
  }
  
  // 天干克应摘要（只列有意义的）
  if (gejuResult.stemCombos) {
    const notable = Object.entries(gejuResult.stemCombos).filter(([p, c]) => c.type !== '平');
    if (notable.length > 0) {
      out += '\n📜 天干克应:\n';
      for (const [palace, combo] of notable) {
        const icon = combo.type === '吉' ? '🟢' : '🔴';
        out += `  ${icon} ${palace}宫 ${combo.heaven}+${combo.earth} = ${combo.name}${combo.desc ? '（' + combo.desc + '）' : ''}\n`;
      }
    }
  }
  
  out += `\n📊 综合评分: ${gejuResult.score}/100\n`;
  return out;
}

/**
 * 格式化解盘结论
 */
function formatInterpretation(interpretResult) {
  if (!interpretResult) return '';
  
  let out = '';
  out += '━'.repeat(40) + '\n';
  out += '【解盘结论】\n\n';
  out += interpretResult.summary + '\n\n';
  out += interpretResult.detail + '\n';
  
  // 方位/颜色/时机
  const meta = [];
  if (interpretResult.direction) meta.push(`🧭 吉方: ${interpretResult.direction}`);
  if (interpretResult.color) meta.push(`🎨 吉色: ${interpretResult.color}`);
  if (interpretResult.timing) meta.push(`⏰ 吉时: ${interpretResult.timing}`);
  if (meta.length > 0) out += '\n' + meta.join('  ') + '\n';
  
  if (interpretResult.advice) {
    out += `\n💡 建议: ${interpretResult.advice}\n`;
  }
  
  return out;
}

/**
 * 完整格式化输出
 */
function formatFull(chart, gejuResult, interpretResult) {
  let out = '';
  out += formatHeader(chart);
  out += formatGrid(chart);
  out += '\n';
  if (gejuResult) out += formatGejus(gejuResult);
  if (interpretResult) out += '\n' + formatInterpretation(interpretResult);
  out += '\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n';
  out += '  奇门之妙在于趋吉避凶，望君审时度势\n';
  out += '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n';
  return out;
}

module.exports = { formatGrid, formatFull, formatHeader, formatGejus, formatInterpretation, strWidth, padEnd };
