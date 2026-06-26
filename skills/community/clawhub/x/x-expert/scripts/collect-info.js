#!/usr/bin/env node

/**
 * X Expert - 信息收集脚本
 * 支持多种搜索服务：Exa, MiniMax, Brave Search
 * Usage: node collect-info.js "搜索主题" [service]
 */

const https = require('https');

// Exa Search
async function searchWithExa(query, numResults = 10) {
  const apiKey = process.env.EXA_API_KEY;
  if (!apiKey) {
    throw new Error('EXA_API_KEY not set');
  }

  const response = await fetch('https://api.exa.ai/search', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': apiKey,
    },
    body: JSON.stringify({
      query,
      numResults,
      type: 'auto',
    }),
  });

  const data = await response.json();
  return data.results || [];
}

// MiniMax Search (使用 MiniMax Web API)
async function searchWithMiniMax(query, numResults = 10) {
  const apiKey = process.env.MINIMAX_API_KEY;
  if (!apiKey) {
    throw new Error('MINIMAX_API_KEY not set');
  }

  const response = await fetch('https://api.minimax.chat/v1/web_search', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      query,
      num_results: numResults,
    }),
  });

  const data = await response.json();
  return data.data?.results || [];
}

// Brave Search
async function searchWithBrave(query, numResults = 10) {
  const apiKey = process.env.BRAVE_API_KEY;
  if (!apiKey) {
    throw new Error('BRAVE_API_KEY not set');
  }

  const url = `https://api.search.brave.com/res/v1/web/search?q=${encodeURIComponent(query)}&count=${numResults}`;

  const response = await fetch(url, {
    headers: {
      'X-Subscription-Token': apiKey,
    },
  });

  const data = await response.json();
  return data.web?.results || [];
}

/**
 * 主搜索函数
 */
async function collectInfo(query, service = 'exa') {
  console.log(`🔍 正在使用 ${service.toUpperCase()} 搜索: "${query}"`);
  console.log('---');

  let results = [];

  try {
    switch (service.toLowerCase()) {
      case 'exa':
        results = await searchWithExa(query);
        break;
      case 'minimax':
        results = await searchWithMiniMax(query);
        break;
      case 'brave':
        results = await searchWithBrave(query);
        break;
      default:
        throw new Error(`Unknown service: ${service}. Use: exa, minimax, or brave`);
    }
  } catch (error) {
    console.error('搜索出错:', error.message);
    console.log('\n请确保已设置相应的 API Key:');
    console.log('- EXA_API_KEY');
    console.log('- MINIMAX_API_KEY');
    console.log('- BRAVE_API_KEY');
    process.exit(1);
  }

  if (results.length === 0) {
    console.log('未找到相关结果');
    return [];
  }

  // 格式化输出
  console.log(`找到 ${results.length} 条结果:\n`);

  const formatted = results.map((item, index) => {
    const title = item.title || item.name || 'Untitled';
    const url = item.url || item.link || '';
    const snippet = item.snippet || item.description || item.content || '';

    return {
      index: index + 1,
      title,
      url,
      snippet: snippet.substring(0, 200) + (snippet.length > 200 ? '...' : ''),
    };
  });

  // 打印结果
  formatted.forEach((item) => {
    console.log(`${item.index}. ${item.title}`);
    console.log(`   ${item.snippet}`);
    console.log(`   🔗 ${item.url}`);
    console.log('');
  });

  return formatted;
}

// CLI 入口
const query = process.argv[2];
const service = process.argv[3] || 'exa';

if (!query) {
  console.error('Usage: node collect-info.js "搜索主题" [service]');
  console.error('Service: exa (default), minimax, brave');
  process.exit(1);
}

collectInfo(query, service);
