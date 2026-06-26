/**
 * 模块1: 定时触发 (Cron)
 * 
 * 执行时间: 14:06, 18:06, 21:06
 */

const { spawn } = require('child_process');
const path = require('path');

// Cron时间配置
const CRON_TIMES = [
  '0 14 * * *',  // 下午2点
  '0 18 * * *',  // 下午6点
  '0 21 * * *',  // 晚上9点
];

// 运行主程序
const runMonitor = () => {
  console.log('\n========== 定时任务触发 ==========');
  console.log('时间:', new Date().toISOString());
  
  const mainPath = path.join(__dirname, 'main.js');
  
  const child = spawn('node', [mainPath], {
    cwd: path.join(__dirname),
    stdio: 'inherit'
  });
  
  child.on('close', (code) => {
    console.log(`\n========== 任务完成 (code: ${code}) ==========`);
  });
};

// 手动触发
const manualRun = () => {
  runMonitor();
};

// 导出
module.exports = { runMonitor, manualRun, CRON_TIMES };

// 如果直接运行
if (require.main === module) {
  manualRun();
}
