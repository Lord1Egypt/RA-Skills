#!/usr/bin/env node

/**
 * Second Brain Triage CLI
 * 信息分诊命令行工具
 */

const fs = require('fs');
const path = require('path');
const { SecondBrainTriage } = require('../src');

function printHelp() {
  console.log(`
Usage: triage.js [options] <content>

Options:
  -f, --file <path>      从文件读取内容
  -b, --batch <path>     批量处理JSON文件
  -o, --output <path>    输出文件路径
  -F, --format <format>  输出格式: json|markdown|csv (默认: json)
  -h, --help             显示帮助

Examples:
  triage.js "TODO: 完成项目报告"
  triage.js --file ./note.txt --format markdown
  triage.js --batch ./items.json --output report.md --format markdown
`);
}

function parseArgs(args) {
  const options = {
    content: null,
    file: null,
    batch: null,
    output: null,
    format: 'json',
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    
    switch (arg) {
      case '-f':
      case '--file':
        options.file = args[++i];
        break;
      case '-b':
      case '--batch':
        options.batch = args[++i];
        break;
      case '-o':
      case '--output':
        options.output = args[++i];
        break;
      case '-F':
      case '--format':
        options.format = args[++i];
        break;
      case '-h':
      case '--help':
        printHelp();
        process.exit(0);
        break;
      default:
        if (!arg.startsWith('-') && !options.content) {
          options.content = arg;
        }
    }
  }

  return options;
}

function formatResult(result, format) {
  switch (format) {
    case 'json':
      return JSON.stringify(result, null, 2);
    case 'markdown':
      return formatAsMarkdown(result);
    case 'csv':
      return formatAsCsv(result);
    default:
      throw new Error(`Unknown format: ${format}`);
  }
}

function formatAsMarkdown(result) {
  const lines = [];
  
  if (Array.isArray(result)) {
    // 批量结果
    lines.push('# 信息分诊报告\n');
    
    // 统计
    const triage = new SecondBrainTriage();
    const stats = triage.getCategoryStats(result);
    lines.push('## 统计概览\n');
    lines.push(`总计: ${stats.total} 项`);
    lines.push(`- 项目: ${stats.byCategory.projects}`);
    lines.push(`- 领域: ${stats.byCategory.areas}`);
    lines.push(`- 资源: ${stats.byCategory.resources}`);
    lines.push(`- 归档: ${stats.byCategory.archive}`);
    lines.push(`- 收件箱: ${stats.byCategory.inbox}\n`);
    
    // 高紧急度
    const highUrgency = result.filter(r => r.urgency.score >= 7);
    if (highUrgency.length > 0) {
      lines.push('## 高紧急度项目\n');
      for (const item of highUrgency) {
        lines.push(`- [${item.urgency.score}] ${item.summary.title}`);
      }
      lines.push('');
    }
    
    // 详细列表
    lines.push('## 详细结果\n');
    for (const item of result) {
      lines.push(...formatSingleResult(item));
      lines.push('---\n');
    }
  } else {
    // 单个结果
    lines.push(...formatSingleResult(result));
  }
  
  return lines.join('\n');
}

function formatSingleResult(result) {
  const lines = [];
  const { summary, classification, urgency, analysis } = result;
  
  lines.push(`# ${summary.title}\n`);
  lines.push(`**分类**: ${summary.category} (置信度: ${(classification.confidence * 100).toFixed(1)}%)`);
  lines.push(`**紧急度**: ${summary.urgency} (${summary.urgencyScore}/10)`);
  lines.push(`**类型**: ${summary.type}`);
  lines.push(`**字数**: ${summary.wordCount} (阅读时间: ${summary.readingTime}分钟)\n`);
  
  if (summary.keyTags.length > 0) {
    lines.push(`**标签**: ${summary.keyTags.join(', ')}\n`);
  }
  
  lines.push(`## 建议行动`);
  lines.push(`${summary.action}\n`);
  
  if (classification.suggestions.length > 0) {
    lines.push(`## 分类建议`);
    for (const suggestion of classification.suggestions) {
      lines.push(`- ${suggestion}`);
    }
    lines.push('');
  }
  
  if (classification.reasons.length > 0) {
    lines.push(`## 分类理由`);
    for (const reason of classification.reasons) {
      lines.push(`- ${reason}`);
    }
    lines.push('');
  }
  
  if (result.relatedness && result.relatedness.hasRelated) {
    lines.push(`## 关联内容`);
    const { strong, medium } = result.relatedness.relatedItems;
    if (strong.length > 0) {
      lines.push(`强关联 (${strong.length}):`);
      for (const item of strong.slice(0, 3)) {
        lines.push(`- ${item.metadata.title} (${(item.similarity * 100).toFixed(0)}%)`);
      }
    }
    if (medium.length > 0) {
      lines.push(`中等关联 (${medium.length}):`);
      for (const item of medium.slice(0, 3)) {
        lines.push(`- ${item.metadata.title} (${(item.similarity * 100).toFixed(0)}%)`);
      }
    }
    lines.push('');
  }
  
  return lines;
}

function formatAsCsv(result) {
  const headers = ['标题', '类型', '分类', '紧急度', '置信度', '标签', '建议'];
  const lines = [headers.join(',')];
  
  const items = Array.isArray(result) ? result : [result];
  
  for (const item of items) {
    const s = item.summary;
    const row = [
      `"${s.title}"`,
      s.type,
      s.category,
      s.urgencyScore,
      item.classification.confidence.toFixed(2),
      `"${s.keyTags.join(';')}"`,
      `"${s.action}"`,
    ];
    lines.push(row.join(','));
  }
  
  return lines.join('\n');
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  
  const triage = new SecondBrainTriage();
  let result;
  
  try {
    if (options.batch) {
      // 批量处理
      const data = JSON.parse(fs.readFileSync(options.batch, 'utf8'));
      if (!Array.isArray(data)) {
        throw new Error('Batch file must contain an array');
      }
      result = triage.triageBatch(data);
    } else if (options.file) {
      // 从文件读取
      const content = fs.readFileSync(options.file, 'utf8');
      result = triage.triage(content);
    } else if (options.content) {
      // 直接处理
      result = triage.triage(options.content);
    } else {
      printHelp();
      process.exit(1);
    }
    
    // 格式化输出
    const output = formatResult(result, options.format);
    
    // 输出到文件或控制台
    if (options.output) {
      fs.writeFileSync(options.output, output);
      console.log(`Output written to: ${options.output}`);
    } else {
      console.log(output);
    }
    
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

main();