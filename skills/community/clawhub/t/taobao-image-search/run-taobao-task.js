const { runSearchTask, parseCliArgs } = require('./verify-taobao-runner');
const { runAutoLogin } = require('./auto-login-taobao');

async function main() {
  const args = process.argv.slice(2);
  let cli;
  try {
    cli = parseCliArgs(args);
  } catch (err) {
    console.error(`参数解析错误: ${err.message}`);
    process.exit(2);
  }

  process.stdout.write(`\n[系统] 正在启动淘宝搜索任务...\n`);

  try {
    await runSearchTask(cli);
    console.log(`\n[系统] 任务执行完毕。`);
  } catch (err) {
    if (err.message && err.message.includes('未检测到淘宝登录状态')) {
      console.log(`\n[系统] 检测到未登录。正在启动自动登录程序...`);
      console.log(`[系统] 请在弹出的浏览器窗口中完成登录，搜索任务将在登录后自动继续。\n`);
      
      const success = await runAutoLogin();
      if (success) {
        console.log(`\n[系统] 登录成功！正在重新启动搜索任务...\n`);
        try {
          await runSearchTask(cli);
          console.log(`\n[系统] 任务执行完毕。`);
        } catch (retryErr) {
          console.error(`\n[系统] 登录后任务再次失败: ${retryErr.message}`);
          process.exit(1);
        }
      } else {
        console.error(`\n[系统] 登录失败或超时。`);
        process.exit(1);
      }
    } else {
      console.error(`\n[系统] 任务运行失败: ${err.message}`);
      process.exit(1);
    }
  }
}

if (require.main === module) {
  main();
}
