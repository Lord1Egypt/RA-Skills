#!/usr/bin/env node

const axios = require('axios');
const { resolveApiKey, emptyResult, successResult, BASE_URL, TIMEOUT_MS } = require('./shared');

// 尝试不同的百科端点
const BAIKE_ENDPOINTS = [
  `${BASE_URL}/baike/baike_summary`,
  `${BASE_URL}/baike/summary`,
  `${BASE_URL}/baike/entry`,
];

async function baike(query) {
  const apiKey = resolveApiKey();
  if (!apiKey) {
    return emptyResult('未配置 BAIDU_API_KEY，请在 OpenClaw Skills 配置页面填入，或本地编辑 config.json。');
  }

  if (!query) {
    return emptyResult('词条名称不能为空。');
  }

  for (const url of BAIKE_ENDPOINTS) {
    try {
      const body = { query };
      const { data } = await axios.post(url, body, {
        timeout: TIMEOUT_MS,
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${apiKey}`,
        },
      });

      if (data && data.code) continue;

      // 解析百科结果
      const result = data?.result || data?.data || {};
      
      return successResult({
        query,
        title: result?.title || query,
        summary: result?.summary || result?.answer || '无摘要',
        image: result?.image || null,
        url: result?.url || null,
        engine: 'baidu-baike'
      });

    } catch (e) {
      continue;
    }
  }

  // 如果所有端点都失败，返回提示
  return emptyResult('百科服务暂时不可用或 API 端点已变更，请联系开发者。');
}

async function main() {
  const args = process.argv.slice(2);
  const query = args.join(' ').trim();

  const result = await baike(query);
  console.log(JSON.stringify(result, null, 2));
}

main();
