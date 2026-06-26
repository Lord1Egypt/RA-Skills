/**
 * run.js — 一键运行脚本
 * 串联：抓取 → 过滤 → 生成 → 推送
 */

const fetch = require('./fetch');
const filter = require('./filter');
const digest = require('./digest');
const push = require('./push');

async function main() {
  console.log('========== 新闻聚合任务开始 ==========');
  console.log(`[run] 开始时间: ${new Date().toISOString()}`);

  try {
    // Step 1: 抓取
    console.log('\n[run] Step 1/4: 抓取新闻...');
    await fetch.main();

    // Step 2: 过滤
    console.log('\n[run] Step 2/4: 过滤与分类...');
    await filter.main();

    // Step 3: 生成简报
    console.log('\n[run] Step 3/4: 生成简报...');
    await digest.main();

    // Step 4: 推送
    console.log('\n[run] Step 4/4: 推送飞书...');
    await push.main();

    console.log('\n========== 任务完成 ==========');
  } catch (err) {
    console.error('[run] 任务失败:', err);
    process.exit(1);
  }
}

if (require.main === module) {
  main().catch(console.error);
}
