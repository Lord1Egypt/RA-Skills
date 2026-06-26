#!/usr/bin/env node
/**
 * 搜索面经列表
 * 用法: node interviews_search.js <关键词> [--company 公司] [--city 城市] [--tag 校招|实习|社招] [--limit 数量]
 *
 * 示例:
 *   node interviews_search.js 数据产品经理
 *   node interviews_search.js 产品经理 --company 字节跳动 --tag 校招 --limit 5
 *
 * ⚠️ 建议使用单一精准关键词，多词组合可能返回空结果
 */
const { mcpCall } = require('./mcp_client');

async function main() {
  const args = process.argv.slice(2);
  const params = {};

  let i = 0;
  while (i < args.length) {
    if (args[i] === '--company' && args[i+1]) { params.company = args[++i]; }
    else if (args[i] === '--city' && args[i+1]) { params.city = args[++i]; }
    else if (args[i] === '--tag' && args[i+1]) { params.recruitment_tag = args[++i]; }
    else if (args[i] === '--limit' && args[i+1]) { params.limit = parseInt(args[++i]); }
    else if (!args[i].startsWith('--')) { params.position_query = args[i]; }
    i++;
  }

  if (!params.position_query) {
    console.error('请提供搜索关键词，例如: node interviews_search.js 数据产品经理');
    process.exit(1);
  }

  console.log('搜索参数:', params);
  console.log('（面经搜索约需8秒，请稍候...）');
  const result = await mcpCall('interviews.search', params);
  const items = result?.data?.items || [];

  if (items.length === 0) {
    console.log('\n未找到相关面经。建议尝试更精准的单词组（如"产品经理"而不是"产品经理 互联网"）');
    return;
  }

  console.log('\n找到 ' + items.length + ' 条面经:\n');
  items.forEach((it, idx) => {
    console.log((idx + 1) + '. ' + it.title);
    console.log('   公司: ' + (it.company || '-') + '  |  岗位: ' + (it.position || '-'));
    console.log('   城市: ' + (it.city || '-') + '  |  类型: ' + (it.difficulty || '-'));
    console.log('   标签: ' + (it.tags || []).join(', '));
    console.log('   摘要: ' + (it.summary || '').substring(0, 80) + '...');
    console.log('   ID: ' + it.id);
    console.log('');
  });

  console.log('提示: 使用 node interviews_get.js <ID> 查看完整面经');
}

main().catch(e => { console.error('错误:', e.message); process.exit(1); });
