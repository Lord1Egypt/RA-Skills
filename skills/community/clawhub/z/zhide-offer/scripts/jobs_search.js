#!/usr/bin/env node
/**
 * 搜索岗位列表
 * 用法: node jobs_search.js [keyword] [--company 公司] [--city 城市] [--size 数量]
 *
 * 示例:
 *   node jobs_search.js 数据产品经理
 *   node jobs_search.js 产品经理 --company 字节跳动 --city 北京 --size 5
 */
const { mcpCall } = require('./mcp_client');

async function main() {
  const args = process.argv.slice(2);
  const params = {};

  // 解析参数
  let i = 0;
  while (i < args.length) {
    if (args[i] === '--company' && args[i+1]) { params.company = args[++i]; }
    else if (args[i] === '--city' && args[i+1]) { params.city = args[++i]; }
    else if (args[i] === '--size' && args[i+1]) { params.pageSize = parseInt(args[++i]); }
    else if (!args[i].startsWith('--')) { params.keyword = args[i]; }
    i++;
  }

  if (!params.keyword && !params.company) {
    console.error('请提供搜索关键词，例如: node jobs_search.js 数据产品经理');
    process.exit(1);
  }

  console.log('搜索参数:', params);
  const result = await mcpCall('jobs.search', params);
  const items = result?.data?.items || [];

  if (items.length === 0) {
    console.log('未找到相关岗位');
    return;
  }

  console.log('\n找到 ' + items.length + ' 个岗位:\n');
  items.forEach((job, idx) => {
    console.log((idx + 1) + '. ' + (job.title || '(岗位名见详情)'));
    console.log('   公司: ' + (job.company || '-'));
    console.log('   城市: ' + (job.city || '-'));
    console.log('   ID: ' + job.id);
    console.log('');
  });

  console.log('提示: 使用 node jobs_get.js <ID> 查看岗位详情');
}

main().catch(e => { console.error('错误:', e.message); process.exit(1); });
