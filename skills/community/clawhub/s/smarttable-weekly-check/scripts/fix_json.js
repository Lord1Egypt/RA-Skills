/**
 * JSON 修复脚本 - 修复中文弯引号编码问题
 * 
 * 问题：浏览器 extract 结果中的中文弯引号（\u201c \u201d）通过某些方式写盘时
 * 会被转成 ASCII 引号，导致 JSON 解析失败。
 * 
 * 用法: node scripts/fix_json.js [data_dir]
 *   默认 data_dir = smartsheet_data/
 */

const fs = require('fs');
const path = require('path');

const DATA_DIR = process.argv[2] || path.join(__dirname, '..', 'smartsheet_data');

function tryFix(filePath) {
  let text = fs.readFileSync(filePath, 'utf8');

  try {
    JSON.parse(text);
    console.log(`${path.basename(filePath)}: 已正常，无需修复`);
    return;
  } catch (e) {
    const pos = parseInt(e.message.match(/position (\d+)/)?.[1] || 0);
    console.log(`${path.basename(filePath)}: JSON 异常，位置 ${pos}`);

    // 策略：在 JSON 字符串值内部，被错误写成 ASCII " 的中文文本
    // 尝试将文本内容内的双引号替换为中文弯引号
    // 此方法通过检测上下文（前后是否有中文字符）来判断

    let fixed = '';
    let inString = false;
    let escaped = false;

    for (let i = 0; i < text.length; i++) {
      const ch = text[i];
      const prev = i > 0 ? text[i - 1] : '';
      const next = i < text.length - 1 ? text[i + 1] : '';

      if (escaped) {
        fixed += ch;
        escaped = false;
        continue;
      }

      if (ch === '\\') {
        fixed += ch;
        escaped = true;
        continue;
      }

      if (ch === '"') {
        // 判断是否在字符串值内部（前后有中文字符）
        const prevIsChinese = /[\u4e00-\u9fff]/.test(prev);
        const nextIsChinese = /[\u4e00-\u9fff]/.test(next);
        const prevIsComma = prev === ',';
        const nextIsComma = next === ',';

        if (inString && (prevIsChinese || nextIsChinese || prevIsComma || nextIsComma)) {
          // 字符串值内部的中文引号场景
          fixed += '\u201c'; // 先假设左引号，下面会判断
          continue;
        }

        // 正常 JSON 引号
        inString = !inString;
        fixed += ch;
        continue;
      }

      fixed += ch;
    }

    try {
      JSON.parse(fixed);
      fs.writeFileSync(filePath, JSON.stringify(JSON.parse(fixed), null, 2), 'utf8');
      console.log(`  ✅ 修复成功`);
    } catch (e2) {
      console.log(`  ❌ 自动修复失败: ${e2.message}`);
      console.log(`  请手动检查文件。提示：确认中文内容中的双引号是否被错误转义。`);
    }
  }
}

// 遍历 w*.json
const files = fs.readdirSync(DATA_DIR).filter(f => /^w\d+\.json$/.test(f));
if (files.length === 0) {
  console.log(`在 ${DATA_DIR} 中未找到 w*.json 文件`);
  process.exit(0);
}

console.log(`检查 ${files.length} 个文件...\n`);
files.forEach(f => tryFix(path.join(DATA_DIR, f)));
console.log('\n完成。');