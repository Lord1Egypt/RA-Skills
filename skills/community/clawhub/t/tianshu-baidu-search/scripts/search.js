#!/usr/bin/env node
/**
 * 百度 AI 搜索 - Node 实现
 * 用法: node search.js '<JSON>'
 * JSON: { "query": "关键词", "count": 10, "freshness": "pd|pw|pm|py|YYYY-MM-DDtoYYYY-MM-DD" }
 */

const apiKey = process.env.BAIDU_API_KEY;
if (!apiKey) {
  console.error('Error: BAIDU_API_KEY must be set in environment.');
  process.exit(1);
}

const input = process.argv[2];
if (!input) {
  console.error('Usage: node search.js \'{"query":"关键词"}\'');
  process.exit(1);
}

let params;
try {
  params = JSON.parse(input);
} catch (e) {
  console.error('JSON parse error:', e.message);
  process.exit(1);
}

if (!params.query) {
  console.error('Error: query must be present in request body.');
  process.exit(1);
}

let count = Math.min(Math.max(parseInt(params.count) || 10, 1), 50);
let searchFilter = {};

if (params.freshness) {
  const now = new Date();
  const endDate = new Date(now);
  endDate.setDate(endDate.getDate() + 1);
  const endStr = endDate.toISOString().slice(0, 10);

  if (['pd', 'pw', 'pm', 'py'].includes(params.freshness)) {
    const startDate = new Date(now);
    if (params.freshness === 'pd') startDate.setDate(startDate.getDate() - 1);
    else if (params.freshness === 'pw') startDate.setDate(startDate.getDate() - 6);
    else if (params.freshness === 'pm') startDate.setDate(startDate.getDate() - 30);
    else if (params.freshness === 'py') startDate.setDate(startDate.getDate() - 364);
    const startStr = startDate.toISOString().slice(0, 10);
    searchFilter = { range: { page_time: { gte: startStr, lt: endStr } } };
  } else if (/^\d{4}-\d{2}-\d{2}to\d{4}-\d{2}-\d{2}$/.test(params.freshness)) {
    const [startStr, endStr2] = params.freshness.split('to');
    searchFilter = { range: { page_time: { gte: startStr, lt: endStr2 } } };
  } else {
    console.error(`Error: freshness (${params.freshness}) must be pd, pw, pm, py, or match YYYY-MM-DDtoYYYY-MM-DD.`);
    process.exit(1);
  }
}

const body = {
  messages: [{ content: params.query, role: 'user' }],
  search_source: 'baidu_search_v2',
  resource_type_filter: [{ type: 'web', top_k: count }],
  search_filter: searchFilter,
};

async function main() {
  const res = await fetch('https://qianfan.baidubce.com/v2/ai_search/web_search', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${apiKey}`,
      'X-Appbuilder-From': 'openclaw',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });

  const data = await res.json();
  if (data.code !== undefined && data.code !== 0) {
    console.error('Error:', data.message || 'Unknown error');
    process.exit(1);
  }

  const refs = data.references || [];
  for (const item of refs) {
    delete item.snippet;
  }
  console.log(JSON.stringify(refs, null, 2));
}

main().catch((e) => {
  console.error('Error:', e.message);
  process.exit(1);
});
