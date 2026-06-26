/**
 * 一键执行完整流程
 * 顺序执行：话题选择 -> 信息收集 -> 博客生成 -> 反思优化 -> 输出文档
 */

const { spawn } = require('child_process');
const path = require('path');
const { v4: uuidv4 } = require('uuid');

// 解析命令行参数
const args = process.argv.slice(2);
const mode = args.find(a => a.startsWith('--mode='))?.split('=')[1] || 'specific';
const topicArg = args.find(a => a.startsWith('--topic='))?.split('=')[1];

// 生成会话ID
const sessionId = uuidv4().slice(0, 8);

console.log('\n========================================');
console.log('  知乎技术博客生成器 - 完整流程');
console.log('========================================\n');
console.log(`会话ID: ${sessionId}`);
console.log(`模式: ${mode === 'hot' ? '热门话题' : '指定主题'}`);
if (mode === 'specific' && topicArg) {
  console.log(`主题: ${topicArg}`);
}
console.log('\n');

/**
 * 执行脚本
 */
function runScript(scriptName, extraArgs = []) {
  return new Promise((resolve, reject) => {
    const scriptPath = path.join(__dirname, scriptName);
    const allArgs = [scriptPath, `--session=${sessionId}`, ...extraArgs];
    
    console.log(`\n>>> 执行: ${scriptName}`);
    console.log('----------------------------------------\n');
    
    const child = spawn('node', allArgs, {
      stdio: 'inherit',
      shell: true,
    });
    
    child.on('close', (code) => {
      if (code === 0) {
        console.log(`\n<<< ${scriptName} 完成`);
        resolve();
      } else {
        reject(new Error(`${scriptName} 退出码: ${code}`));
      }
    });
    
    child.on('error', (err) => {
      reject(err);
    });
  });
}

/**
 * 主流程
 */
async function main() {
  const startTime = Date.now();
  
  try {
    // Step 1: 话题选择
    if (mode === 'hot') {
      await runScript('01_topic_selector.js', ['--mode=hot']);
      
      // 热门话题模式需要用户选择，暂停等待输入
      console.log('\n========================================');
      console.log('  请选择话题后按回车继续...');
      console.log('========================================\n');
      
      // 等待用户输入（简化处理，实际可能需要更复杂的交互）
      process.stdin.once('data', async () => {
        await continueProcess();
      });
      return;
    } else {
      const topicArgs = topicArg ? [`--topic=${topicArg}`] : [];
      await runScript('01_topic_selector.js', ['--mode=specific', ...topicArgs]);
      await continueProcess();
    }
  } catch (error) {
    console.error('\n❌ 流程中断:', error.message);
    process.exit(1);
  }
}

/**
 * 继续执行后续步骤
 */
async function continueProcess() {
  try {
    // Step 2: 信息收集
    await runScript('02_info_collector.js');
    
    // Step 3: 博客生成
    await runScript('03_blog_generator.js');
    
    // Step 4: 反思优化
    await runScript('04_refine_blog.js');
    
    // Step 5: 输出文档
    await runScript('05_output_md.js');
    
    const endTime = Date.now();
    const duration = ((endTime - startTime) / 1000).toFixed(2);
    
    console.log('\n========================================');
    console.log('  ✅ 全部流程执行完成！');
    console.log('========================================');
    console.log(`总耗时: ${duration} 秒`);
    console.log(`输出目录: D:\\techinsight\\reports\\blog_${sessionId}\\05_output\\`);
    console.log('========================================\n');
    
  } catch (error) {
    console.error('\n❌ 流程中断:', error.message);
    process.exit(1);
  }
}

// 启动流程
main();
