/**
 * scheduler.js — Cron 定时调度器
 * 按配置的时间间隔自动运行新闻聚合任务
 */

const cron = require('node-cron');
const path = require('path');

// 加载配置
const configPath = path.join(__dirname, '..', 'config.json');
const fs = require('fs');

let config = { schedule: '0 8 * * *' };
if (fs.existsSync(configPath)) {
  config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
}

const schedule = config.schedule || '0 8 * * *';
const runScript = path.join(__dirname, 'run.js');

console.log(`[scheduler] 定时任务已启动`);
console.log(`[scheduler] Cron 表达式: ${schedule}`);
console.log(`[scheduler] 下次运行: ${getNextRun(schedule)}`);

if (!cron.validate(schedule)) {
  console.error(`[scheduler] 无效的 Cron 表达式: ${schedule}`);
  console.error('[scheduler] 默认使用: 0 8 * * * (每天 08:00 UTC)');
}

// 调度任务
const job = cron.schedule(schedule, async () => {
  console.log(`[scheduler] ⏰ 触发定时任务: ${new Date().toISOString()}`);
  try {
    const { main } = require(runScript);
    await main();
    console.log(`[scheduler] ✅ 任务完成，下次运行: ${getNextRun(schedule)}`);
  } catch (err) {
    console.error('[scheduler] ❌ 任务失败:', err.message);
  }
}, {
  scheduled: true,
  timezone: 'UTC'
});

/**
 * 计算下次运行时间
 */
function getNextRun(cronExpr) {
  try {
    // 简单估算：解析 cron 并计算
    const parts = cronExpr.split(' ');
    if (parts.length < 5) return '未知';
    
    // 对于日 cron (0 8 * * *)，计算明天 8:00 UTC
    const now = new Date();
    const next = new Date(now);
    next.setUTCHours(parseInt(parts[0]) || 8, parseInt(parts[1]) || 0, 0, 0);
    if (next <= now) {
      next.setUTCDate(next.getUTCDate() + 1);
    }
    return next.toISOString().replace('T', ' ').slice(0, 16) + ' UTC';
  } catch {
    return '未知';
  }
}

console.log('[scheduler] 按 Ctrl+C 停止');

// 优雅退出
process.on('SIGINT', () => {
  console.log('\n[scheduler] 停止定时任务...');
  job.stop();
  process.exit(0);
});
