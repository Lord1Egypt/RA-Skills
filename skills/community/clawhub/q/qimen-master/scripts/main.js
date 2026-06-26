#!/usr/bin/env node
/**
 * 奇门遁甲排盘系统 - CLI入口
 * 
 * 用法:
 *   node main.js                              # 当前时间排盘（综合）
 *   node main.js --time "2026-03-25 14:30"    # 指定时间
 *   node main.js --question wealth            # 指定问题类型
 *   node main.js --json                       # JSON输出
 *   node main.js --grid                       # 只输出九宫格
 */

const path = require('path');
const { calculate } = require('./engine.js');

// 动态加载可选模块（可能还在开发中）
let formatModule, gejusModule, interpretModule;
try { formatModule = require('./format.js'); } catch(e) { formatModule = null; }
try { gejusModule = require('./gejus.js'); } catch(e) { gejusModule = null; }
try { interpretModule = require('./interpret.js'); } catch(e) { interpretModule = null; }

// ========== 参数解析 ==========
function parseArgs(argv) {
  const args = {
    time: null,
    question: 'general',
    json: false,
    grid: false,
    help: false,
  };
  
  for (let i = 0; i < argv.length; i++) {
    switch(argv[i]) {
      case '--time': case '-t':
        args.time = argv[++i];
        break;
      case '--question': case '-q':
        args.question = argv[++i];
        break;
      case '--json': case '-j':
        args.json = true;
        break;
      case '--grid': case '-g':
        args.grid = true;
        break;
      case '--help': case '-h':
        args.help = true;
        break;
    }
  }
  return args;
}

// ========== 简易格式化（当format.js不可用时）==========
function simpleFormat(chart) {
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
  
  out += '\n';
  
  // 简易九宫格
  // 传统排列：4-9-2 / 3-5-7 / 8-1-6
  const rows = [[4,9,2],[3,5,7],[8,1,6]];
  const width = 22;
  
  out += '┌' + '─'.repeat(width) + '┬' + '─'.repeat(width) + '┬' + '─'.repeat(width) + '┐\n';
  
  for (let r = 0; r < 3; r++) {
    const ps = rows[r].map(n => chart.palaces[n]);
    
    // 行1: 宫名
    out += '│';
    for (const p of ps) {
      const label = `${p.position}${rows[r][ps.indexOf(p)]}宫 ${p.direction}`;
      out += ` ${label}${' '.repeat(Math.max(0, width - label.length - strWidth(label) + label.length - 1))}│`;
    }
    out += '\n';
    
    // 行2: 九星
    out += '│';
    for (const p of ps) {
      const label = p.star || '(天禽寄2宫)';
      out += ` ${label}${' '.repeat(Math.max(0, width - strWidth(label) - 1))}│`;
    }
    out += '\n';
    
    // 行3: 八门
    out += '│';
    for (const p of ps) {
      const label = p.door || '';
      out += ` ${label}${' '.repeat(Math.max(0, width - strWidth(label) - 1))}│`;
    }
    out += '\n';
    
    // 行4: 八神
    out += '│';
    for (const p of ps) {
      const label = p.god || '';
      out += ` ${label}${' '.repeat(Math.max(0, width - strWidth(label) - 1))}│`;
    }
    out += '\n';
    
    // 行5: 天地盘干
    out += '│';
    for (const p of ps) {
      const label = `天:${p.heavenStem || '-'} 地:${p.earthStem || '-'}`;
      out += ` ${label}${' '.repeat(Math.max(0, width - strWidth(label) - 1))}│`;
    }
    out += '\n';
    
    // 行6: 标记
    out += '│';
    for (const p of ps) {
      const label = p.flags.length > 0 ? `[${p.flags.join('][')}]` : '';
      out += ` ${label}${' '.repeat(Math.max(0, width - strWidth(label) - 1))}│`;
    }
    out += '\n';
    
    if (r < 2) {
      out += '├' + '─'.repeat(width) + '┼' + '─'.repeat(width) + '┼' + '─'.repeat(width) + '┤\n';
    }
  }
  
  out += '└' + '─'.repeat(width) + '┴' + '─'.repeat(width) + '┴' + '─'.repeat(width) + '┘\n';
  
  return out;
}

// 计算字符串显示宽度（中文字符宽度2）
function strWidth(str) {
  let w = 0;
  for (const ch of str) {
    w += ch.charCodeAt(0) > 0x7f ? 2 : 1;
  }
  return w;
}

// 右填充到指定显示宽度
function padEnd(str, targetWidth) {
  const currentWidth = strWidth(str);
  const padding = Math.max(0, targetWidth - currentWidth);
  return str + ' '.repeat(padding);
}

// ========== 帮助信息 ==========
function showHelp() {
  console.log(`
☯️  奇门遁甲排盘系统

用法:
  node main.js [选项]

选项:
  --time, -t <时间>      指定排盘时间（默认当前时间）
                         格式: "2026-03-25 14:30"
  --question, -q <类型>  指定问题类型（默认 general）
  --json, -j             JSON格式输出
  --grid, -g             只输出九宫格
  --help, -h             显示帮助

问题类型:
  general   综合运势      wealth    求财
  career    事业官运      marriage  婚姻感情
  health    疾病健康      travel    出行
  lawsuit   官司诉讼      exam      考试学业
  lost      失物寻找      missing   走失寻人
  weather   天气预测      fengshui  住宅风水
  invest    投资理财

示例:
  node main.js
  node main.js --time "2026-03-25 14:30"
  node main.js --time "2026-03-25 14:30" --question wealth
  node main.js --json
`);
}

// ========== 主入口 ==========
function main() {
  const args = parseArgs(process.argv.slice(2));
  
  if (args.help) {
    showHelp();
    return;
  }
  
  // 排盘
  const dateInput = args.time || new Date();
  let chart;
  try {
    chart = calculate(dateInput);
  } catch(e) {
    console.error('❌ 排盘失败:', e.message);
    process.exit(1);
  }
  
  // 格局识别
  let gejuResult = null;
  if (gejusModule) {
    try {
      gejuResult = gejusModule.identifyGejus(chart);
    } catch(e) {
      // 格局模块出错不影响基本排盘
    }
  }
  
  // 解盘
  let interpretResult = null;
  if (interpretModule) {
    try {
      interpretResult = interpretModule.interpret(chart, gejuResult, args.question);
    } catch(e) {
      // 解盘模块出错不影响基本排盘
    }
  }
  
  // JSON输出
  if (args.json) {
    const output = {
      chart,
      gejus: gejuResult,
      interpretation: interpretResult,
    };
    console.log(JSON.stringify(output, null, 2));
    return;
  }
  
  // 文本输出
  let output = '';
  
  // 使用format模块（包含格局+解盘）或简易格式化
  if (formatModule && !args.grid) {
    output = formatModule.formatFull(chart, gejuResult, interpretResult);
  } else if (formatModule && args.grid) {
    output = formatModule.formatGrid(chart);
  } else {
    // 无format模块时用简易格式化 + 手动拼接格局和解盘
    output = simpleFormat(chart);
    
    if (gejuResult && !args.grid) {
      output += '\n【格局分析】\n';
      if (gejuResult.auspicious.length > 0) {
        output += '🟢 吉格:\n';
        for (const g of gejuResult.auspicious) {
          output += `  ✦ ${g.name}（${g.palace}宫）${g.desc ? ': ' + g.desc : ''}\n`;
        }
      }
      if (gejuResult.inauspicious.length > 0) {
        output += '🔴 凶格:\n';
        for (const g of gejuResult.inauspicious) {
          output += `  ✧ ${g.name}（${g.palace}宫）${g.desc ? ': ' + g.desc : ''}\n`;
        }
      }
      output += `\n📊 综合评分: ${gejuResult.score}/100\n`;
    }
    
    if (interpretResult && !args.grid) {
      output += '\n' + '━'.repeat(40) + '\n';
      output += '【解盘结论】\n\n';
      output += interpretResult.summary + '\n\n';
      output += interpretResult.detail + '\n';
      if (interpretResult.direction) output += `\n🧭 吉方: ${interpretResult.direction}`;
      if (interpretResult.color) output += `  🎨 吉色: ${interpretResult.color}`;
      if (interpretResult.timing) output += `  ⏰ 吉时: ${interpretResult.timing}`;
      output += '\n';
      if (interpretResult.advice) output += `\n💡 建议: ${interpretResult.advice}\n`;
    }
    
    output += '\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n';
    output += '  奇门之妙在于趋吉避凶，望君审时度势\n';
    output += '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n';
  }
  
  console.log(output);
}

main();
