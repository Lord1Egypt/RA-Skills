#!/usr/bin/env node

/**
 * 百度热搜 - 使用百度搜索结果
 * 通过搜索"百度热搜"获取当前热门话题
 */

const axios = require('axios');
const { resolveApiKey, emptyResult, successResult, BASE_URL, TIMEOUT_MS } = require('./shared');

const SEARCH_URL = `${BASE_URL}/ai_search/web_search`;

async function hotword() {
  const apiKey = resolveApiKey();
  if (!apiKey) {
    return emptyResult('未配置 BAIDU_API_KEY');
  }

  try {
    const body = {
      messages: [{ role: 'user', content: '百度热搜榜单前20' }],
      search_source: 'baidu_search_v2',
      resource_type_filter: [{ type: 'web', top_k: 10 }],
    };

    const { data } = await axios.post(SEARCH_URL, body, {
      timeout: TIMEOUT_MS,
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
      },
    });

    const refs = data?.references || [];
    const hotwords = refs
      .filter(r => r && r.type === 'web')
      .slice(0, 20)
      .map((r, i) => ({
        rank: i + 1,
        title: r.title || '',
        url: r.url || '',
        snippet: r.snippet || ''
      }));

    return successResult({
      total: hotwords.length,
      hotwords,
      engine: 'baidu-hotword-via-search'
    });

  } catch (e) {
    return emptyResult(`获取热搜失败: ${e.message}`);
  }
}

async function main() {
  const result = await hotword();
  console.log(JSON.stringify(result, null, 2));
}

main();
