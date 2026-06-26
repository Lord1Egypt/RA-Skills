#!/usr/bin/env node
/**
 * 智能文档处理助手 - 核心处理脚本
 * 支持 PDF 提取、摘要生成、翻译等功能
 */

import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';

// 解析参数
const args = process.argv.slice(2);
const options = {
  input: null,
  output: null,
  action: 'extract', // extract, summarize, translate
  from: 'auto',
  to: 'zh',
  length: 'medium', // short, medium, long
  type: 'text' // text, entities, tables
};

for (let i = 0; i < args.length; i++) {
  switch (args[i]) {
    case '--input':
    case '-i':
      options.input = args[++i];
      break;
    case '--output':
    case '-o':
      options.output = args[++i];
      break;
    case '--action':
    case '-a':
      options.action = args[++i];
      break;
    case '--from':
    case '-f':
      options.from = args[++i];
      break;
    case '--to':
    case '-t':
      options.to = args[++i];
      break;
    case '--length':
    case '-l':
      options.length = args[++i];
      break;
    case '--type':
      options.type = args[++i];
      break;
    case '--help':
    case '-h':
      showHelp();
      process.exit(0);
      break;
  }
}

function showHelp() {
  console.log(`
📄 智能文档处理助手

用法:
  node process.mjs [选项]

选项:
  -i, --input <file>     输入文件路径 (必填)
  -o, --output <file>    输出文件路径
  -a, --action <action>  操作: extract|summarize|translate (默认: extract)
  -f, --from <lang>      源语言 (默认: auto)
  -t, --to <lang>        目标语言 (默认: zh)
  -l, --length <length>  摘要长度: short|medium|long (默认: medium)
  --type <type>          提取类型: text|entities|tables (默认: text)
  -h, --help             显示帮助

示例:
  node process.mjs -i ./doc.pdf -o ./output.md
  node process.mjs -i ./report.pdf -a summarize -l medium
  node process.mjs -i ./paper.pdf -a translate -f en -t zh
`);
}

// 主函数
async function main() {
  if (!options.input) {
    console.error('❌ 错误: 请提供输入文件 (--input)');
    process.exit(1);
  }

  if (!fs.existsSync(options.input)) {
    console.error(`❌ 错误: 文件不存在: ${options.input}`);
    process.exit(1);
  }

  console.log(`📄 正在处理文档...`);
  console.log(`   文件: ${options.input}`);
  console.log(`   操作: ${options.action}\n`);

  let result = '';

  switch (options.action) {
    case 'extract':
      result = await extractText(options.input, options.type);
      break;
    case 'summarize':
      result = await summarizeDocument(options.input, options.length);
      break;
    case 'translate':
      result = await translateDocument(options.input, options.from, options.to);
      break;
    default:
      console.error(`❌ 未知操作: ${options.action}`);
      process.exit(1);
  }

  // 输出结果
  if (options.output) {
    fs.writeFileSync(options.output, result, 'utf-8');
    console.log(`\n✅ 处理完成，已保存至: ${options.output}`);
  } else {
    console.log('\n' + '='.repeat(60));
    console.log(result);
    console.log('='.repeat(60));
  }
}

// 提取文本
async function extractText(inputFile, type) {
  const ext = path.extname(inputFile).toLowerCase();
  let text = '';

  console.log('🔍 正在提取文本...');

  if (ext === '.pdf') {
    try {
      // 尝试使用 pdftotext
      text = execSync(`pdftotext "${inputFile}" -`, { encoding: 'utf-8' });
    } catch (e) {
      // 回退到简单提取
      text = `[PDF 文件: ${path.basename(inputFile)}]\n\n`;
      text += `文件大小: ${(fs.statSync(inputFile).size / 1024).toFixed(2)} KB\n`;
      text += `注意: 需要安装 pdftotext 工具以提取完整文本\n`;
      text += `安装命令: brew install poppler (macOS) 或 apt-get install poppler-utils (Linux)`;
    }
  } else if (ext === '.md') {
    text = fs.readFileSync(inputFile, 'utf-8');
  } else if (ext === '.txt') {
    text = fs.readFileSync(inputFile, 'utf-8');
  } else {
    text = `[文件: ${path.basename(inputFile)}]\n`;
    text += `类型: ${ext || '未知'}\n`;
    text += `大小: ${(fs.statSync(inputFile).size / 1024).toFixed(2)} KB\n`;
    text += `\n该文件类型暂不支持直接提取文本。`;
  }

  // 根据类型处理
  if (type === 'entities') {
    return extractEntities(text);
  }

  return formatOutput(text, inputFile);
}

// 提取实体
function extractEntities(text) {
  console.log('🔍 正在提取关键信息...');

  const entities = {
    dates: [],
    amounts: [],
    emails: [],
    phones: [],
    names: []
  };

  // 日期匹配
  const datePatterns = [
    /\d{4}[年/-]\d{1,2}[月/-]\d{1,2}[日]?/g,
    /\d{1,2}[月/-]\d{1,2}[日]?/g
  ];
  datePatterns.forEach(pattern => {
    const matches = text.match(pattern);
    if (matches) entities.dates.push(...matches);
  });

  // 金额匹配
  const amountPattern = /[¥$€]?\d+[,.]?\d*\s*(万元?|亿元?|元?|USD?|CNY?)/g;
  const amounts = text.match(amountPattern);
  if (amounts) entities.amounts.push(...amounts);

  // 邮箱匹配
  const emailPattern = /[\w.-]+@[\w.-]+\.\w+/g;
  const emails = text.match(emailPattern);
  if (emails) entities.emails.push(...emails);

  // 电话匹配
  const phonePattern = /1[3-9]\d{9}|\d{3,4}-\d{7,8}/g;
  const phones = text.match(phonePattern);
  if (phones) entities.phones.push(...phones);

  // 生成报告
  let output = `# 📊 关键信息提取报告\n\n`;
  output += `**文档**: ${path.basename(options.input)}\n`;
  output += `**提取时间**: ${new Date().toLocaleString('zh-CN')}\n\n`;

  output += `## 📅 日期\n\n`;
  output += entities.dates.length > 0 
    ? entities.dates.slice(0, 20).map(d => `- ${d}`).join('\n')
    : '未检测到日期';
  output += '\n\n';

  output += `## 💰 金额\n\n`;
  output += entities.amounts.length > 0
    ? entities.amounts.slice(0, 20).map(a => `- ${a}`).join('\n')
    : '未检测到金额';
  output += '\n\n';

  output += `## 📧 邮箱\n\n`;
  output += entities.emails.length > 0
    ? entities.emails.map(e => `- ${e}`).join('\n')
    : '未检测到邮箱';
  output += '\n\n';

  output += `## 📞 电话\n\n`;
  output += entities.phones.length > 0
    ? entities.phones.map(p => `- ${p}`).join('\n')
    : '未检测到电话';
  output += '\n\n';

  output += `---\n\n*由 智能文档处理助手 生成*`;

  return output;
}

// 生成摘要
async function summarizeDocument(inputFile, length) {
  console.log('📝 正在生成摘要...');

  const text = await extractText(inputFile, 'text');
  const maxLength = { short: 500, medium: 1000, long: 2000 }[length] || 1000;

  // 简单的摘要生成（实际应用中可以使用 AI API）
  const lines = text.split('\n').filter(line => line.trim());
  const summary = lines.slice(0, Math.min(lines.length, 20)).join('\n\n');

  let output = `# 📝 文档摘要\n\n`;
  output += `**原文**: ${path.basename(inputFile)}\n`;
  output += `**摘要长度**: ${length}\n`;
  output += `**生成时间**: ${new Date().toLocaleString('zh-CN')}\n\n`;

  output += `## 📋 内容摘要\n\n`;
  output += summary.substring(0, maxLength);
  if (text.length > maxLength) {
    output += '\n\n... (内容已截断)';
  }

  output += '\n\n';
  output += `## 📊 文档统计\n\n`;
  output += `- 总字符数: ${text.length}\n`;
  output += `- 总行数: ${lines.length}\n`;
  output += `- 摘要长度: ${maxLength} 字符\n`;

  output += '\n\n---\n\n*由 智能文档处理助手 生成*';

  return output;
}

// 翻译文档
async function translateDocument(inputFile, from, to) {
  console.log(`🌐 正在翻译 (${from} → ${to})...`);

  const text = await extractText(inputFile, 'text');

  // 这里应该调用翻译 API，现在使用占位符
  let output = `# 🌐 文档翻译\n\n`;
  output += `**原文**: ${path.basename(inputFile)}\n`;
  output += `**翻译方向**: ${from} → ${to}\n`;
  output += `**生成时间**: ${new Date().toLocaleString('zh-CN')}\n\n`;

  output += `## ⚠️ 说明\n\n`;
  output += `当前版本使用基础文本提取功能。\n`;
  output += `完整翻译功能需要集成翻译 API（如 Google Translate、DeepL 等）。\n\n`;

  output += `## 📄 原文内容\n\n`;
  output += text.substring(0, 2000);
  if (text.length > 2000) {
    output += '\n\n... (内容已截断)';
  }

  output += '\n\n---\n\n*由 智能文档处理助手 生成*';

  return output;
}

// 格式化输出
function formatOutput(text, inputFile) {
  let output = `# 📄 文档提取结果\n\n`;
  output += `**文件**: ${path.basename(inputFile)}\n`;
  output += `**路径**: ${inputFile}\n`;
  output += `**时间**: ${new Date().toLocaleString('zh-CN')}\n\n`;
  output += `---\n\n`;
  output += text;
  output += '\n\n---\n\n*由 智能文档处理助手 生成*';
  return output;
}

// 运行
main().catch(console.error);
