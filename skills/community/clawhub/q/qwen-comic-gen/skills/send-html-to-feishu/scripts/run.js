#!/usr/bin/env node

// 发送 HTML 到飞书 - 主脚本
// 整合 HTML 转 PDF + 发送飞书

const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

// 获取技能目录
const skillDir = __dirname;
const scriptsDir = path.join(skillDir, 'scripts');

// 命令行参数
const args = process.argv.slice(2);
const inputHtml = args[0];
const customMessage = args.slice(1).join(' ');

if (!inputHtml) {
  console.error('用法：npx skills run send-html-to-feishu <input.html> [message]');
  console.error('示例：npx skills run send-html-to-feishu expert-review.html "HTML 转 PDF 报告"');
  process.exit(1);
}

// 验证 HTML 文件
if (!fs.existsSync(inputHtml)) {
  console.error(`❌ 文件不存在：${inputHtml}`);
  process.exit(1);
}

// 生成输出 PDF 路径
const outputPdf = inputHtml.replace('.html', '.pdf');

console.log('📄 发送 HTML 到飞书');
console.log('=' .repeat(50));

// 步骤 1：HTML 转 PDF
console.log('\n步骤 1/2: HTML 转 PDF');
console.log('-'.repeat(50));
try {
  execSync(`node "${path.join(scriptsDir, 'html-to-pdf.js')}" "${inputHtml}" "${outputPdf}"`, {
    stdio: 'inherit'
  });
} catch (error) {
  console.error('❌ HTML 转 PDF 失败');
  process.exit(1);
}

// 步骤 2：发送飞书
console.log('\n步骤 2/2: 发送飞书');
console.log('-'.repeat(50));
const message = customMessage || `HTML 报告已转换：${path.basename(inputHtml)}`;
try {
  execSync(`node "${path.join(scriptsDir, 'send-to-feishu.js')}" "${outputPdf}" "${message}"`, {
    stdio: 'inherit'
  });
} catch (error) {
  console.error('❌ 发送飞书失败');
  process.exit(1);
}

console.log('\n' + '='.repeat(50));
console.log('✅ 完成！PDF 已发送到飞书');
