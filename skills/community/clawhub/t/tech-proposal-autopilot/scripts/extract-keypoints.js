#!/usr/bin/env node
/**
 * 参考资料关键点提取脚本
 * 
 * 功能：
 * 1. 读取参考资料（PDF/Word/URL/Text）
 * 2. 使用 AI 提取关键点
 * 3. 压缩 80% 后保存
 * 
 * 用法：
 * node extract-keypoints.js <reference-file> [output-file]
 */

const fs = require('fs');
const path = require('path');

async function extractKeyPoints(referencePath, outputPath) {
  console.log(`Extracting keypoints from: ${referencePath}`);
  
  // 检查文件类型
  const ext = path.extname(referencePath).toLowerCase();
  
  let content = '';
  
  if (ext === '.pdf') {
    // PDF 处理需要 pdf-parse 或类似库
    console.log('PDF processing requires pdf-parse library');
    console.log('Please convert PDF to text first or install dependencies');
    process.exit(1);
  } else if (ext === '.docx' || ext === '.doc') {
    // Word 处理需要 mammoth 或类似库
    console.log('Word processing requires mammoth library');
    console.log('Please convert Word to text first or install dependencies');
    process.exit(1);
  } else if (ext === '.md' || ext === '.txt') {
    // 直接读取
    content = fs.readFileSync(referencePath, 'utf8');
  } else {
    console.log(`Unsupported file type: ${ext}`);
    process.exit(1);
  }
  
  // 统计原始字数
  const originalWords = content.length;
  console.log(`Original content: ${originalWords} characters`);
  
  // 提取关键点
  // 这里应该调用 AI 进行提取
  // 但作为模板，我们提供结构
  
  const keypointsTemplate = `# 参考资料关键点提取

## 来源
- 文件：${path.basename(referencePath)}
- 原始字数：${originalWords}

## 提取方法
使用 AI 进行关键点提取，压缩率目标：80%

## 提取流程
1. 分析文档结构
2. 识别核心概念和关键论点
3. 提取重要数据、参数、配置
4. 保留关键图表和表格
5. 生成压缩后的关键点文档

## 关键点

### 核心概念
[待 AI 提取]

### 关键数据
[待 AI 提取]

### 重要参数
[待 AI 提取]

### 核心架构
[待 AI 提取]

### 关键技术
[待 AI 提取]

## 使用说明

此文件为模板。实际使用时，应调用 AI 进行智能提取：

\`\`\`javascript
// 使用 OpenClaw 调用 AI
const result = await openclaw.invoke('ai', {
  prompt: \`请提取以下参考资料的关键点，压缩到原篇幅的20%左右：

${content}

要求：
1. 保留所有核心概念和关键论点
2. 保留重要数据、参数、配置
3. 保留关键图表和表格的结构
4. 删除冗余描述和重复内容
5. 输出为 Markdown 格式
\`
});
\`\`\`

---
生成时间：${new Date().toISOString()}
`;
  
  // 输出
  const finalOutput = outputPath || path.join(path.dirname(referencePath), 'reference-keypoints.md');
  fs.writeFileSync(finalOutput, keypointsTemplate);
  
  console.log(`Key points template saved to: ${finalOutput}`);
  console.log('\n注意：此为模板文件。实际使用时需要调用 AI 进行智能提取。');
}

// 主函数
const args = process.argv.slice(2);
if (args.length < 1) {
  console.log('Usage: node extract-keypoints.js <reference-file> [output-file]');
  console.log('\nSupported formats: .md, .txt');
  console.log('Note: PDF and Word require additional dependencies');
  process.exit(1);
}

extractKeypoints(args[0], args[1]).catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
