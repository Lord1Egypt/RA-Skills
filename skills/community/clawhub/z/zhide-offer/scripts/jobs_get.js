#!/usr/bin/env node
/**
 * 获取岗位详情
 * 用法: node jobs_get.js <岗位ID>
 *
 * 示例:
 *   node jobs_get.js 69269dd194a970ef706ba044
 */
const { mcpCall } = require('./mcp_client');

async function main() {
  const id = process.argv[2];
  if (!id) {
    console.error('请提供岗位ID，例如: node jobs_get.js 69269dd194a970ef706ba044');
    process.exit(1);
  }

  const result = await mcpCall('jobs.get', { id });
  const job = result?.data || result;

  console.log('========== 岗位详情 ==========');
  console.log('岗位名称: ' + (job.title || '-'));
  console.log('公司:     ' + (job.company || '-'));
  console.log('城市:     ' + (job.city || '-'));
  console.log('');
  console.log('--- 岗位描述 ---');
  console.log(job.description || job.desc || '（无描述）');
  console.log('');
  console.log('原始数据:');
  console.log(JSON.stringify(job, null, 2));
}

main().catch(e => { console.error('错误:', e.message); process.exit(1); });
