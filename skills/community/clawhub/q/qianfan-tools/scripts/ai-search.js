#!/usr/bin/env node

const axios = require('axios');
const { resolveApiKey, emptyResult, successResult, BASE_URL, TIMEOUT_MS } = require('./shared');

const SEARCH_URL = `${BASE_URL}/ai_search/web_search`;
const DEFAULT_NUM = 10;
const MAX_NUM = 50;

async function aiSearch(query, numResults = DEFAULT_NUM) {
  const apiKey = resolveApiKey();
  if (!apiKey) {
    return emptyResult('未配置 BAIDU_API_KEY，请在 OpenClaw Skills 配置页面填入，或本地编辑 config.json。');
  }

  try {
    const body = {
      messages: [{ role: 'user', content: query }],
      search_source: 'baidu_search_v2',
      resource_type_filter: [{ type: 'web', top_k: Math.min(numResults, MAX_NUM) }],
    };

    const { data } = await axios.post(SEARCH_URL, body, {
      timeout: TIMEOUT_MS,
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
      },
    });

    if (data && data.code) {
      return emptyResult(`搜索服务错误: ${data.message || '未知错误'}`);
    }

    const refs = data?.references || [];
    const results = refs
      .filter(r => r && r.type === 'web')
      .map(r => ({
        title: r.title || '',
        url: r.url || '',
        snippet: r.snippet ?? r.content ?? '',
        date: r.date || null
      }));

    return successResult({
      query,
      total: results.length,
      results,
      engine: 'baidu-ai-search'
    });

  } catch (e) {
    return emptyResult(`搜索失败: ${e.message}`);
  }
}

async function main() {
  const args = process.argv.slice(2);
  const query = (args[0] || '').trim();
  const numResults = Math.min(Math.max(Number(args[1]) || DEFAULT_NUM, 1), MAX_NUM);

  if (!query) {
    console.log(JSON.stringify(emptyResult('搜索查询不能为空。')));
    process.exit(1);
  }

  const result = await aiSearch(query, numResults);
  console.log(JSON.stringify(result, null, 2));
}

main();
