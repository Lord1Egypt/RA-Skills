#!/usr/bin/env node

/**
 * 百度搜索
 * 
 * 用法：node scripts/search.js "关键词"
 * 输出：JSON 格式的搜索结果
 */

const { execSync } = require('child_process');

const query = process.argv[2];
if (!query) {
  console.log('❌ 用法：node search.js "关键词"');
  process.exit(1);
}

const requestBody = {
  query,
  edition: 'standard',
  resource_type_filter: [{ type: 'web', top_k: 10 }],
  search_recency_filter: 'year',
  safe_search: false,
};

try {
  const result = execSync(
    `python3 ~/.openclaw/workspace/skills/baidu-search/scripts/search.py '${JSON.stringify(requestBody)}'`,
    { encoding: 'utf8', env: { ...process.env }, timeout: 30000 }
  );
  
  // 提取 JSON 部分
  const lines = result.toString().split('\n');
  let jsonStart = -1;
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].trim().startsWith('[')) { jsonStart = i; break; }
  }
  
  if (jsonStart === -1) {
    console.log(JSON.stringify([]));
    process.exit(0);
  }
  
  const jsonStr = lines.slice(jsonStart).join('\n');
  const results = JSON.parse(jsonStr);
  
  // 简化输出
  const simplified = results.map(r => ({
    title: r.title || '无标题',
    summary: r.summary || '无摘要',
    url: r.url || '',
  }));
  
  console.log(JSON.stringify(simplified, null, 2));
} catch (error) {
  console.log(JSON.stringify([]));
}
