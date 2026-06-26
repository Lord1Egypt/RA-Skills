#!/usr/bin/env node

/**
 * 百度千帆 - 百度学术搜索
 */

const axios = require('axios');
const { resolveApiKey, emptyResult, successResult, BASE_URL, TIMEOUT_MS } = require('./shared');

const ACADEMIC_URL = `${BASE_URL}/search/academic`;

async function academic(query, numResults = 10) {
  const apiKey = resolveApiKey();
  if (!apiKey) {
    return emptyResult('未配置 BAIDU_API_KEY');
  }

  if (!query) {
    return emptyResult('搜索关键词不能为空。');
  }

  try {
    const body = {
      query,
      num: Math.min(numResults, 20)
    };

    const { data } = await axios.post(ACADEMIC_URL, body, {
      timeout: TIMEOUT_MS,
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
      },
    });

    if (data && data.code) {
      return emptyResult(`学术搜索服务错误: ${data.message || '需开通百度学术 API'}`);
    }

    const items = data?.result?.items || data?.result?.data || [];
    
    const papers = items.map(item => ({
      title: item?.title || '',
      authors: item?.authors || item?.author || [],
      abstract: item?.abstract || item?.summary || '',
      venue: item?.venue || item?.journal || '',
      year: item?.year || null,
      citations: item?.citations || 0,
      url: item?.url || ''
    }));

    return successResult({
      query,
      total: papers.length,
      papers,
      engine: 'qianfan-academic'
    });

  } catch (e) {
    return emptyResult(`学术搜索失败: ${e.message} (需开通百度学术 API)`);
  }
}

async function main() {
  const args = process.argv.slice(2);
  const query = args[0];
  const numResults = Number(args[1]) || 10;

  if (!query) {
    console.log(JSON.stringify(emptyResult('用法: node academic.js <关键词> [返回数量]')));
    process.exit(1);
  }

  const result = await academic(query, numResults);
  console.log(JSON.stringify(result, null, 2));
}

main();
