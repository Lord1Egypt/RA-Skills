#!/usr/bin/env node

/**
 * Agent Benchmark - SWE-bench Lite 实现
 * 简化版代码任务评估框架
 */

const fs = require('fs');
const path = require('path');
const { execSync, spawn } = require('child_process');

// 配置
const CONFIG = {
  timeout: 30000, // 30 秒超时
  memoryLimit: 512 * 1024 * 1024, // 512MB
  maxConcurrent: 3,
  languages: {
    python: { command: 'python', ext: '.py' },
    node: { command: 'node', ext: '.js' },
    go: { command: 'go run', ext: '.go' }
  }
};

/**
 * 任务结果类型
 */
class TaskResult {
  constructor(taskId) {
    this.taskId = taskId;
    this.status = 'pending'; // pending, running, passed, failed, error
    this.executionTime = 0;
    this.output = '';
    this.error = '';
    this.exitCode = null;
    this.testsPassed = 0;
    this.testsTotal = 0;
  }

  toJSON() {
    return {
      taskId: this.taskId,
      status: this.status,
      executionTime: this.executionTime,
      output: this.output,
      error: this.error,
      exitCode: this.exitCode,
      testsPassed: this.testsPassed,
      testsTotal: this.testsTotal,
      success: this.status === 'passed'
    };
  }
}

/**
 * 执行单个代码任务
 */
async function executeTask(task) {
  const result = new TaskResult(task.id);
  result.status = 'running';
  
  const startTime = Date.now();
  
  try {
    const language = CONFIG.languages[task.language] || CONFIG.languages.python;
    const tempDir = path.join(__dirname, 'temp', task.id);
    
    // 创建临时目录
    if (!fs.existsSync(tempDir)) {
      fs.mkdirSync(tempDir, { recursive: true });
    }
    
    // 写入代码文件
    const codeFile = path.join(tempDir, `code${language.ext}`);
    const testFile = path.join(tempDir, `test${language.ext}`);
    
    fs.writeFileSync(codeFile, task.input.code);
    fs.writeFileSync(testFile, task.input.test_code || '');
    
    // 构建完整代码 (代码 + 测试)
    const fullCode = task.language === 'python' 
      ? `${task.input.code}\n\n${task.input.test_code || ''}`
      : `${task.input.code}\n${task.input.test_code || ''}`;
    
    const fullFile = path.join(tempDir, `full${language.ext}`);
    fs.writeFileSync(fullFile, fullCode);
    
    // 执行代码
    const execPromise = new Promise((resolve, reject) => {
      const child = spawn(language.command.split(' ')[0], 
        [...language.command.split(' ').slice(1), fullFile],
        {
          timeout: CONFIG.timeout,
          cwd: tempDir,
          env: { ...process.env, NODE_ENV: 'test' }
        }
      );
      
      let stdout = '';
      let stderr = '';
      
      child.stdout.on('data', (data) => {
        stdout += data.toString();
      });
      
      child.stderr.on('data', (data) => {
        stderr += data.toString();
      });
      
      child.on('close', (code) => {
        resolve({ code, stdout, stderr });
      });
      
      child.on('error', (err) => {
        reject(err);
      });
      
      // 超时处理
      setTimeout(() => {
        child.kill('SIGKILL');
        reject(new Error(`Timeout after ${CONFIG.timeout}ms`));
      }, CONFIG.timeout);
    });
    
    const execResult = await execPromise;
    
    result.exitCode = execResult.code;
    result.output = execResult.stdout;
    result.error = execResult.stderr;
    
    // 判断是否通过
    if (execResult.code === 0 && !execResult.stderr.includes('Error')) {
      result.status = 'passed';
      result.testsPassed = task.expected_output?.tests_passed || 1;
      result.testsTotal = task.expected_output?.tests_passed || 1;
    } else {
      result.status = 'failed';
      result.error = execResult.stderr || `Exit code: ${execResult.code}`;
    }
    
  } catch (error) {
    result.status = 'error';
    result.error = error.message;
  }
  
  result.executionTime = Date.now() - startTime;
  
  // 清理临时文件
  const tempDir = path.join(__dirname, 'temp', task.id);
  if (fs.existsSync(tempDir)) {
    fs.rmSync(tempDir, { recursive: true, force: true });
  }
  
  return result;
}

/**
 * 运行批量评估
 */
async function runBenchmark(tasks) {
  console.log(`\n🚀 开始评估，共 ${tasks.length} 个任务\n`);
  
  const results = [];
  let completed = 0;
  
  // 并发执行 (限制并发数)
  for (let i = 0; i < tasks.length; i += CONFIG.maxConcurrent) {
    const batch = tasks.slice(i, i + CONFIG.maxConcurrent);
    const batchResults = await Promise.all(batch.map(task => executeTask(task)));
    results.push(...batchResults);
    
    completed += batch.length;
    console.log(`进度：${completed}/${tasks.length}`);
  }
  
  return results;
}

/**
 * 生成评估报告
 */
function generateReport(results, outputPath) {
  const total = results.length;
  const passed = results.filter(r => r.status === 'passed').length;
  const failed = results.filter(r => r.status === 'failed').length;
  const errors = results.filter(r => r.status === 'error').length;
  const successRate = ((passed / total) * 100).toFixed(1);
  const avgTime = (results.reduce((sum, r) => sum + r.executionTime, 0) / total).toFixed(0);
  
  const report = `# SWE-bench Lite 评估报告

**生成日期**: ${new Date().toISOString().split('T')[0]}  
**总任务数**: ${total}  
**通过**: ${passed} ✅  
**失败**: ${failed} ❌  
**错误**: ${errors} ⚠️  
**成功率**: ${successRate}%  
**平均执行时间**: ${avgTime}ms

---

## 详细结果

| 任务 ID | 状态 | 执行时间 | 测试通过 | 备注 |
|---------|------|----------|----------|------|
${results.map(r => `| ${r.taskId} | ${getStatusIcon(r.status)} | ${r.executionTime}ms | ${r.testsPassed}/${r.testsTotal} | ${r.error ? truncate(r.error, 30) : '-'} |`).join('\n')}

---

## 任务详情

${results.map(r => `### ${r.taskId}

- **状态**: ${r.status}
- **执行时间**: ${r.executionTime}ms
- **退出码**: ${r.exitCode}
- **输出**: \`${truncate(r.output, 100)}\`
- **错误**: \`${truncate(r.error, 100)}\`

---
`).join('\n')}

## 总结

${getSummary(passed, failed, errors, total)}
`;

  fs.writeFileSync(outputPath, report);
  console.log(`\n📊 报告已生成：${outputPath}\n`);
  
  return report;
}

function getStatusIcon(status) {
  switch (status) {
    case 'passed': return '✅ PASS';
    case 'failed': return '❌ FAIL';
    case 'error': return '⚠️ ERROR';
    default: return '⏳ PENDING';
  }
}

function truncate(str, len) {
  if (!str) return '-';
  return str.length > len ? str.substring(0, len) + '...' : str;
}

function getSummary(passed, failed, errors, total) {
  const rate = ((passed / total) * 100).toFixed(1);
  if (rate >= 80) {
    return `🎉 评估表现优秀！成功率 ${rate}%，系统运行稳定。`;
  } else if (rate >= 60) {
    return `👍 评估表现良好。成功率 ${rate}%，建议关注失败任务。`;
  } else {
    return `⚠️ 评估表现需改进。成功率 ${rate}%，请检查失败原因。`;
  }
}

/**
 * CLI 入口
 */
async function main() {
  const args = process.argv.slice(2);
  
  // 解析参数
  const taskFile = args.find((_, i) => args[i - 1] === '--tasks') || 'tasks.json';
  const outputFile = args.find((_, i) => args[i - 1] === '--output') || 'benchmark-report.md';
  
  // 加载任务
  let tasks;
  try {
    const taskPath = path.join(__dirname, taskFile);
    tasks = JSON.parse(fs.readFileSync(taskPath, 'utf-8'));
  } catch (error) {
    console.error('❌ 无法加载任务文件:', error.message);
    process.exit(1);
  }
  
  // 运行评估
  const results = await runBenchmark(tasks);
  
  // 生成报告
  generateReport(results, path.join(__dirname, outputFile));
  
  // 保存到 memory 目录
  const memoryReport = path.join(__dirname, '../../memory/benchmark-results.md');
  generateReport(results, memoryReport);
  
  console.log('✅ 评估完成!\n');
}

// 导出模块
module.exports = {
  executeTask,
  runBenchmark,
  generateReport,
  TaskResult,
  CONFIG
};

// 运行 CLI
if (require.main === module) {
  main().catch(console.error);
}
