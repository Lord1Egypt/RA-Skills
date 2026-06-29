#!/usr/bin/env node

/**
 * TDX Formula Validator v1.0
 * 通达信公式验证工具 — 语法验证/未来函数检测/自然语言生成
 */

const fs = require('fs');

// === 通达信真实函数大全 ===
const TDX_FUNCTIONS = new Set([
  'OPEN','O','HIGH','H','LOW','L','CLOSE','C','VOL','V','AMOUNT','AMO',
  'ADVANCE','DECLINE','LIMITUP','LIMITDOWN',
  'DYNAINFO','ZTPRICE','WINNER','COST','LWINNER','PWINNER',
  'VOLUNIT','HSL','EXTERN','INNER',
  'DATE','TIME','YEAR','MONTH','WEEK','DAY','HOUR','MINUTE',
  'WEEKDAY','TOTALBARSCOUNT','BARSCOUNT','BARSTATUS',
  'REF','REFV','SUM','COUNT','HHV','LLV','HHVBARS','LLVBARS',
  'MA','EMA','SMA','MEMA','EXPMEMA','WMA','DMA','TMA',
  'CROSS','LONGCROSS','BARSLAST','BARSSINCE',
  'EVERY','EXIST','LAST','FILTER','TFILTER','SUMBARS',
  'CONST','MAX','MIN','ABS',
  'IF','IFC','IFN','VALUEWHEN','RANGE','BETWEEN',
  'POLYLINE','STD','VAR','STDP','VARP',
  'SLOPE','FORCAST','LINEARSLOPE','LINEARREG',
  'DEVSQ','COVAR','CORR','RELATE',
  'TSQRT','TPOWER','LN','LOG','EXP','POW','SQRT',
  'SIN','COS','TAN','ATAN',
  'AVEDEV','MOD','CEILING','FLOOR','INTPART','FRACPART',
  'BACKSET','REFX','XMA','ZIG','PEAK','TROUGH',
  'DRAWLINE','DRAWSL','DRAWKLINE','STICKLINE',
  'DRAWBAND','DRAWICON','DRAWTEXT','DRAWGBK',
  'DRAWNUMBER','FILLRGN','CIRCLEDOT',
  'PEAKBARS','TROUGHBARS','ZIGA','SAR',
  'INBLOCK','DYBLOCK','BLOCKNAME','BLOCKSETNUM',
  'CODELIKE','NAMELIKE','CONCEPTLIKE',
  'FINANCE','FINANCE2','FINVALUE','FINONE',
  'CAPITAL','TOTALCAPITAL',
  'INDEXC','INDEXH','INDEXL','INDEXO','INDEXV','INDEXA',
  'MARKET','TRANSLATE','CALCSTYLE',
  'GP','GPS','BOND','FUTURE','OPTION',
  'CMDX','CMINX','JPOOL','AUTOTYPE','NDAY',
]);

const FUTURE_FUNCTIONS = [
  'BACKSET','REFX','XMA','ZIG','PEAK','TROUGH',
  'DRAWLINE','DRAWSL','STICKLINE','DRAWBAND',
  'DRAWICON','DRAWTEXT','DRAWGBK','DRAWNUMBER',
  'FILLRGN','CIRCLEDOT','PEAKBARS','TROUGHBARS','ZIGA','SAR',
];

// === 自然语言→公式模板库 ===
const TEMPLATES = [
  { keywords: ['金叉','均线金叉','ma金叉'],
    formula: 'MA5:=MA(C,5); MA10:=MA(C,10); CROSS(MA5,MA10) AND VOL>REF(VOL,1);',
    desc: '均线金叉 + 放量' },
  { keywords: ['macd金叉','macd买入'],
    formula: 'DIF:=EMA(C,12)-EMA(C,26); DEA:=EMA(DIF,9); CROSS(DIF,DEA) AND DIF>0 AND DEA>0;',
    desc: 'MACD金叉 + 零轴上方' },
  { keywords: ['涨停','首板','涨停板'],
    formula: 'C>=ZTPRICE(REF(C,1),0.1) AND C=H;',
    desc: '涨停板预警' },
  { keywords: ['连板','2板','二板','连板'],
    formula: 'EVERY(C>=ZTPRICE(REF(C,1),0.1),2) AND C=H;',
    desc: '连板识别（2板起步）' },
  { keywords: ['底背离','macd底背离'],
    formula: 'DIF:=EMA(C,12)-EMA(C,26); LOW_NEW:=LLV(L,60)=L; DIF_LOW:=LLV(DIF,60)=DIF; LOW_NEW AND REF(DIF_LOW,1)=0 AND DIF_LOW=0;',
    desc: 'MACD底背离' },
  { keywords: ['超卖','kdj超卖'],
    formula: 'RSV:=(C-LLV(L,9))/(HHV(H,9)-LLV(L,9))*100; K:=SMA(RSV,3,1); D:=SMA(K,3,1); J:=3*K-2*D; J<20;',
    desc: 'KDJ超卖（买入信号）' },
  { keywords: ['超买','kdj超买'],
    formula: 'RSV:=(C-LLV(L,9))/(HHV(H,9)-LLV(L,9))*100; K:=SMA(RSV,3,1); D:=SMA(K,3,1); J:=3*K-2*D; J>80;',
    desc: 'KDJ超买（卖出信号）' },
  { keywords: ['倍量','放量突破'],
    formula: 'VOL/REF(VOL,1)>2 AND C>REF(HHV(H,10),1);',
    desc: '倍量突破' },
  { keywords: ['多头排列','均线多头'],
    formula: 'MA5:=MA(C,5); MA10:=MA(C,10); MA20:=MA(C,20); MA60:=MA(C,60); MA5>MA10 AND MA10>MA20 AND MA20>MA60;',
    desc: '均线多头排列' },
  { keywords: ['布林','boll','布林带'],
    formula: 'MID:=MA(C,20); STD:=STD(C,20); UPPER:=MID+2*STD; LOWER:=MID-2*STD; C<LOWER AND C>REF(C,1);',
    desc: '布林带下轨反弹' },
  { keywords: ['rsi','rsi超卖'],
    formula: 'RSI1:=SMA(MAX(C-REF(C,1),0),6,1)/SMA(ABS(C-REF(C,1)),6,1)*100; CROSS(RSI1,20);',
    desc: 'RSI超卖买入' },
  { keywords: ['板块龙头','龙头'],
    formula: "INBLOCK('新能源') AND C>(HHV(H,20)*0.95) AND C>=ZTPRICE(REF(C,1),0.1);",
    desc: '板块龙头识别' },
  { keywords: ['放量下跌','主力出货'],
    formula: 'C<REF(C,1) AND V>REF(V,1)*1.5;',
    desc: '放量下跌（主力出货）' },
  { keywords: ['缩量上涨','主力控盘'],
    formula: 'C>REF(C,1) AND V<REF(V,1);',
    desc: '缩量上涨（主力控盘）' },
  { keywords: ['净利润增长','绩优'],
    formula: 'FINANCE(30)>0 AND C/FINANCE(34)<10;',
    desc: '净利润增长 + 低估值' },
  { keywords: ['小市值','小盘'],
    formula: 'CAPITAL*C/100000000<100 AND FINANCE(33)>0.5;',
    desc: '小市值+高增长' },
  { keywords: ['白马股'],
    formula: 'FINANCE(33)>1 AND FINANCE(9)<60 AND FINANCE(18)>2;',
    desc: '绩优白马股' },
];

// === 公式验证 ===
function validateFormula(code) {
  const errors = [];
  const warnings = [];
  const lines = code.split('\n').map(l => l.trim()).filter(l => l && !l.startsWith('//') && !l.startsWith('{'));

  if (lines.length === 0) {
    return { valid: false, errors: ['空公式'], warnings: [] };
  }

  // 提取函数调用
  const allFuncs = new Set();
  const funcPattern = /[A-Z][A-Z0-9_]+(?=\()/g;
  let m;
  while ((m = funcPattern.exec(code)) !== null) allFuncs.add(m[0]);

  const knownVars = new Set(['MA5','MA10','MA20','MA60','MA120','MA250',
    'DIF','DEA','RSV','K','D','J','RSI1','RSI2','RSI3',
    'MID','UPPER','LOWER','HH9','LL9',
    'LOW_NEW','DIF_LOW','DIF_60_LOW']);

  allFuncs.forEach(fn => {
    if (knownVars.has(fn)) return;
    if (!TDX_FUNCTIONS.has(fn)) {
      errors.push('未知函数: ' + fn + '（可能是变量名或AI幻觉）');
    }
  });

  // 检查未来函数
  const codeUpper = code.toUpperCase();
  FUTURE_FUNCTIONS.forEach(ff => {
    if (codeUpper.includes(ff)) {
      errors.push('未来函数 ' + ff + ' — 禁止用于选股公式！');
    }
  });

  // 最后一行不能是赋值
  const lastLine = lines[lines.length - 1];
  if (lastLine && lastLine.includes(':=')) {
    errors.push('最后一行包含赋值(:=)，没有输出条件');
  }

  // 分号检查
  for (let i = 0; i < lines.length - 1; i++) {
    if (lines[i].includes(':=') && !lines[i].endsWith(';')) {
      errors.push('第' + (i+1) + '行: 赋值语句缺分号');
    }
  }

  // 括号匹配
  let parenCount = 0;
  for (const ch of code) {
    if (ch === '(') parenCount++;
    if (ch === ')') parenCount--;
  }
  if (parenCount !== 0) {
    errors.push('括号不匹配（多' + Math.abs(parenCount) + '个' + (parenCount > 0 ? '(' : ')') + '）');
  }

  if (codeUpper.includes('WINNER') || codeUpper.includes('COST')) {
    warnings.push('WINNER/COST 函数结果在不同通达信版本可能有差异');
  }
  if (codeUpper.includes('DYNAINFO')) {
    warnings.push('DYNAINFO 是盘中动态数据，历史回测不生效');
  }

  return { valid: errors.length === 0, errors, warnings };
}

// === 自然语言→公式 ===
function generateFormula(query) {
  const q = query.toLowerCase();
  for (const tpl of TEMPLATES) {
    for (const kw of tpl.keywords) {
      if (q.includes(kw)) {
        return { formula: tpl.formula, desc: tpl.desc, match: '精确匹配' };
      }
    }
  }
  for (const tpl of TEMPLATES) {
    for (const kw of tpl.keywords) {
      const matchCount = [...kw].filter(ch => q.includes(ch)).length;
      if (matchCount / kw.length > 0.6) {
        return { formula: tpl.formula, desc: tpl.desc, match: '模糊匹配(' + kw + ')' };
      }
    }
  }
  return null;
}

// === CLI ===
function main() {
  const args = process.argv.slice(2);
  const cmd = args[0];

  if (!cmd) {
    console.log('');
    console.log('📈 TDX Formula Validator v1.0');
    console.log('');
    console.log('用法:');
    console.log('  check \"<公式>\"    验证公式语法');
    console.log('  check-file <文件>    验证文件中的公式');
    console.log('  gen \"<描述>\"        自然语言生成公式');
    console.log('  list                列出所有模板');
    console.log('');
    console.log('示例:');
    console.log('  check \"CROSS(MA(C,5),MA(C,10)) AND VOL>REF(VOL,1);\"');
    console.log('  gen \"均线金叉放量\"');
    console.log('  gen \"macd底背离\"');
    return;
  }

  switch (cmd) {
    case 'check': {
      const formula = args.slice(1).join(' ');
      if (!formula) { console.log('❌ 请输入公式代码'); return; }
      const result = validateFormula(formula);
      console.log('');
      if (result.valid) {
        console.log('✅ 公式语法正确');
      } else {
        console.log('❌ ' + result.errors.length + ' 个错误:');
        result.errors.forEach(e => console.log('   🔴 ' + e));
      }
      if (result.warnings.length > 0) {
        console.log('⚠️ ' + result.warnings.length + ' 个警告:');
        result.warnings.forEach(w => console.log('   🟡 ' + w));
      }
      break;
    }

    case 'check-file': {
      const filepath = args[1];
      if (!filepath) { console.log('❌ 请输入文件路径'); return; }
      if (!fs.existsSync(filepath)) { console.log('❌ 文件不存在: ' + filepath); return; }
      const content = fs.readFileSync(filepath, 'utf8');
      const result = validateFormula(content);
      console.log('');
      if (result.valid) {
        console.log('✅ 公式语法正确');
      } else {
        console.log('❌ ' + result.errors.length + ' 个错误:');
        result.errors.forEach(e => console.log('   🔴 ' + e));
      }
      if (result.warnings.length > 0) {
        console.log('⚠️ ' + result.warnings.length + ' 个警告:');
        result.warnings.forEach(w => console.log('   🟡 ' + w));
      }
      break;
    }

    case 'gen': {
      const query = args.slice(1).join(' ');
      if (!query) { console.log('❌ 请输入描述'); return; }
      const result = generateFormula(query);
      if (result) {
        console.log('');
        console.log('🎯 ' + result.desc + ' (' + result.match + ')');
        console.log('');
        console.log(result.formula);
        console.log('');
        // 自动验证
        const v = validateFormula(result.formula);
        if (v.valid) {
          console.log('✅ 公式验证通过');
        }
      } else {
        console.log('❌ 未找到匹配公式');
      }
      break;
    }

    case 'list': {
      console.log('');
      console.log('📋 公式模板列表:');
      TEMPLATES.forEach((t, i) => {
        console.log('  ' + (i+1) + '. ' + t.desc + ' [' + t.keywords.join('/') + ']');
      });
      break;
    }

    default:
      console.log('❌ 未知命令: ' + cmd + '（可用: check / check-file / gen / list）');
  }
}

main();