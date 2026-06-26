#!/usr/bin/env node
/**
 * Research Analyzer - 智能研究分析工具
 * 基于 Tavily API 的网络搜索和报告生成
 */

import fs from 'fs';

// 解析参数
const args = process.argv.slice(2);
if (args.length === 0 || args[0] === '-h' || args[0] === '--help') {
  console.log(`Usage: research.mjs "query" [options]

Options:
  --deep              深度搜索模式 (获取更详细内容)
  --output <file>     输出文件路径
  --max-results <n>   最大结果数 (默认: 10, 最大: 20)

Examples:
  research.mjs "AI trends 2025"
  research.mjs "machine learning" --deep
  research.mjs "Rust vs Go" --deep --output report.md
`);
  process.exit(0);
}

const query = args[0];
const options = {
  deep: args.includes('--deep'),
  maxResults: 10
};

// 解析 max-results
const maxResultsIdx = args.indexOf('--max-results');
if (maxResultsIdx !== -1 && args[maxResultsIdx + 1]) {
  options.maxResults = parseInt(args[maxResultsIdx + 1], 10) || 10;
}

// 解析 output
const outputIdx = args.indexOf('--output');
const outputFile = outputIdx !== -1 ? args[outputIdx + 1] : null;

console.log(`🔬 Research Analyzer`);
console.log(`Query: ${query}`);
console.log(`Mode: ${options.deep ? '深度' : '标准'}\n`);

// 检查 API Key - 只从环境变量读取
const apiKey = process.env.TAVILY_API_KEY?.trim();

if (!apiKey) {
  console.error('Error: TAVILY_API_KEY environment variable not set');
  console.error('Please set your Tavily API key:');
  console.error('  export TAVILY_API_KEY="tvly-your-api-key"');
  console.error('Get your API key at https://tavily.com');
  process.exit(1);
}



// 执行搜索
async function performSearch() {
  try {
    const searchDepth = options.deep ? 'advanced' : 'basic';
    
    const body = {
      query: query,
      max_results: Math.min(options.maxResults, 20),
      search_depth: searchDepth,
      topic: 'general',
      include_raw_content: options.deep
    };

    console.log('🔍 Searching...');
    
    const resp = await fetch('https://api.tavily.com/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      },
      body: JSON.stringify(body)
    });

    if (!resp.ok) {
      const text = await resp.text().catch(() => '');
      throw new Error(`Search failed (${resp.status}): ${text}`);
    }

    const data = await resp.json();
    return data;
  } catch (error) {
    console.error('Search error:', error.message);
    process.exit(1);
  }
}

// 生成报告
function generateReport(query, data, options) {
  const results = data.results || [];
  const answer = data.answer || '';
  
  let report = `# 研究报告: ${query}\n\n`;
  
  // 执行摘要
  report += `## 执行摘要\n\n`;
  if (answer) {
    report += `${answer}\n\n`;
  } else {
    report += `本报告基于 ${results.length} 个来源，对「${query}」进行了${options.deep ? '深度' : '标准'}研究分析。\n\n`;
  }
  
  // 关键发现
  report += `## 关键发现\n\n`;
  if (results.length > 0) {
    results.slice(0, 5).forEach((r, i) => {
      const title = r.title || '无标题';
      const content = r.content ? r.content.slice(0, 200) + '...' : '无内容';
      report += `${i + 1}. **${title}**\n   ${content}\n\n`;
    });
  } else {
    report += `未找到相关结果。\n\n`;
  }
  
  // 数据来源
  report += `## 数据来源\n\n`;
  results.forEach((r, i) => {
    report += `${i + 1}. [${r.title || '无标题'}](${r.url || ''})\n`;
  });
  
  // 研究元数据
  report += `\n## 研究元数据\n\n`;
  report += `- 搜索模式: ${options.deep ? '深度' : '标准'}\n`;
  report += `- 结果数量: ${results.length}\n`;
  report += `- 响应时间: ${data.response_time || 'N/A'}s\n`;
  report += `- 生成时间: ${new Date().toLocaleString()}\n`;
  
  return report;
}

// 主函数
async function main() {
  const data = await performSearch();
  const report = generateReport(query, data, options);
  
  if (outputFile) {
    fs.writeFileSync(outputFile, report, 'utf-8');
    console.log(`✅ 报告已保存: ${outputFile}`);
  } else {
    console.log('\n' + '='.repeat(60));
    console.log(report);
  }
}

main();
