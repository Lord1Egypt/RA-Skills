/**
 * Qwen Portal Auth Helper
 * 
 * 自动化解决 qwen-portal OAuth 认证问题
 * 基于 2026-03-09 实战经验
 * 
 * 核心功能:
 * 1. 自动化获取 OAuth 链接 (解决 interactive TTY 问题)
 * 2. 监控 qwen-portal 任务健康状态
 * 3. 提供任务状态重置工具
 * 4. 生成维护报告和建议
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class QwenPortalAuthHelper {
  constructor() {
    this.skillPath = __dirname;
    this.scriptsPath = path.join(this.skillPath, 'scripts');
    this.examplesPath = path.join(this.skillPath, 'examples');
  }

  /**
   * 获取技能信息
   */
  getInfo() {
    return {
      name: 'qwen-portal-auth-helper',
      version: '1.0.0',
      description: 'Automate qwen-portal OAuth authentication',
      author: 'Bessent (based on 2026-03-09 practical experience)',
      commands: {
        'get-link': '获取 qwen-portal OAuth 链接',
        'check-health': '检查 qwen-portal 任务健康状态',
        'reset-task': '重置任务状态 (认证成功后使用)',
        'setup-monitoring': '设置每周自动监控'
      }
    };
  }

  /**
   * 检查环境依赖
   */
  checkDependencies() {
    const dependencies = {
      tmux: { command: 'tmux --version', required: true },
      openclaw: { command: 'openclaw --version', required: true },
      python3: { command: 'python3 --version', required: false }
    };

    const results = {};
    let allOk = true;

    for (const [name, dep] of Object.entries(dependencies)) {
      try {
        execSync(dep.command, { stdio: 'pipe' });
        results[name] = { ok: true, message: '已安装' };
      } catch (error) {
        results[name] = { 
          ok: !dep.required, 
          message: dep.required ? '未安装 (必需)' : '未安装 (可选)'
        };
        if (dep.required) allOk = false;
      }
    }

    return { allOk, results };
  }

  /**
   * 运行获取 OAuth 链接脚本
   */
  getOAuthLink(options = {}) {
    const scriptPath = path.join(this.scriptsPath, 'get-qwen-oauth-link.sh');
    
    if (!fs.existsSync(scriptPath)) {
      throw new Error(`脚本不存在: ${scriptPath}`);
    }

    let command = scriptPath;
    if (options.testOnly) command += ' --test-only';
    if (options.verbose) command += ' --verbose';

    try {
      const output = execSync(command, { encoding: 'utf-8' });
      return {
        success: true,
        output: output,
        command: command
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
        stderr: error.stderr?.toString(),
        stdout: error.stdout?.toString()
      };
    }
  }

  /**
   * 检查 qwen-portal 任务健康状态
   */
  checkHealth(options = {}) {
    const scriptPath = path.join(this.scriptsPath, 'check-qwen-auth.sh');
    
    if (!fs.existsSync(scriptPath)) {
      throw new Error(`脚本不存在: ${scriptPath}`);
    }

    let command = scriptPath;
    if (options.quick) command += ' --quick';
    if (options.full) command += ' --full';

    try {
      const output = execSync(command, { encoding: 'utf-8' });
      
      // 尝试查找报告文件
      const reportFiles = fs.readdirSync('/tmp')
        .filter(file => file.startsWith('qwen-auth-report-'))
        .sort()
        .reverse();
      
      let latestReport = null;
      if (reportFiles.length > 0) {
        latestReport = `/tmp/${reportFiles[0]}`;
      }

      return {
        success: true,
        output: output,
        report: latestReport,
        command: command
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
        stderr: error.stderr?.toString(),
        stdout: error.stdout?.toString()
      };
    }
  }

  /**
   * 重置任务状态
   */
  resetTaskState(taskId) {
    const scriptPath = path.join(this.scriptsPath, 'reset-task-state.py');
    
    if (!fs.existsSync(scriptPath)) {
      throw new Error(`脚本不存在: ${scriptPath}`);
    }

    try {
      const output = execSync(`python3 "${scriptPath}" "${taskId}"`, { 
        encoding: 'utf-8' 
      });
      
      return {
        success: true,
        output: output,
        taskId: taskId
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
        stderr: error.stderr?.toString(),
        stdout: error.stdout?.toString(),
        taskId: taskId
      };
    }
  }

  /**
   * 设置每周自动监控
   */
  setupMonitoring() {
    const cronJob = '0 9 * * 1 ~/.openclaw/skills/qwen-portal-auth-helper/scripts/check-qwen-auth.sh >> ~/.openclaw/logs/qwen-check.log 2>&1';
    
    try {
      // 检查是否已存在
      const existingCron = execSync('crontab -l 2>/dev/null || echo ""', { 
        encoding: 'utf-8' 
      });
      
      if (existingCron.includes('check-qwen-auth')) {
        return {
          success: true,
          alreadyExists: true,
          message: '监控任务已存在'
        };
      }
      
      // 添加新任务
      const newCron = existingCron.trim() + '\n' + cronJob + '\n';
      execSync(`echo '${newCron}' | crontab -`, { encoding: 'utf-8' });
      
      return {
        success: true,
        alreadyExists: false,
        message: '监控任务已添加',
        cronJob: cronJob
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * 获取使用示例
   */
  getExamples() {
    const examples = [];
    
    try {
      const exampleFiles = fs.readdirSync(this.examplesPath);
      
      for (const file of exampleFiles) {
        if (file.endsWith('.md')) {
          const content = fs.readFileSync(
            path.join(this.examplesPath, file), 
            'utf-8'
          );
          
          // 提取标题
          const titleMatch = content.match(/^# (.+)$/m);
          const title = titleMatch ? titleMatch[1] : file;
          
          // 提取前几行作为描述
          const description = content.split('\n')
            .slice(1, 4)
            .filter(line => line.trim() && !line.startsWith('>'))
            .join(' ')
            .substring(0, 150) + '...';
          
          examples.push({
            file: file,
            title: title,
            description: description,
            path: path.join(this.examplesPath, file)
          });
        }
      }
    } catch (error) {
      // 如果 examples 目录不存在，返回默认示例
      examples.push({
        file: 'quick-recovery.md',
        title: '快速恢复指南',
        description: '当 qwen-portal 新闻任务失败时的5分钟修复流程',
        path: path.join(this.examplesPath, 'quick-recovery.md')
      });
    }
    
    return examples;
  }

  /**
   * CLI 接口
   */
  async runCommand(command, args = {}) {
    switch (command) {
      case 'info':
        return this.getInfo();
        
      case 'check-deps':
        return this.checkDependencies();
        
      case 'get-link':
        return this.getOAuthLink(args);
        
      case 'check-health':
        return this.checkHealth(args);
        
      case 'reset-task':
        if (!args.taskId) {
          throw new Error('需要提供 taskId 参数');
        }
        return this.resetTaskState(args.taskId);
        
      case 'setup-monitoring':
        return this.setupMonitoring();
        
      case 'examples':
        return this.getExamples();
        
      default:
        throw new Error(`未知命令: ${command}`);
    }
  }
}

// 导出模块
module.exports = QwenPortalAuthHelper;

// 如果直接运行此文件
if (require.main === module) {
  const helper = new QwenPortalAuthHelper();
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log(helper.getInfo());
    console.log('\n可用命令:');
    console.log('  node index.js info             显示技能信息');
    console.log('  node index.js check-deps       检查环境依赖');
    console.log('  node index.js get-link         获取 OAuth 链接');
    console.log('  node index.js check-health     检查健康状态');
    console.log('  node index.js reset-task <id>  重置任务状态');
    console.log('  node index.js setup-monitoring 设置自动监控');
    console.log('  node index.js examples         查看使用示例');
    process.exit(0);
  }
  
  const command = args[0];
  const commandArgs = {};
  
  // 解析参数
  for (let i = 1; i < args.length; i++) {
    if (args[i] === '--test-only') commandArgs.testOnly = true;
    if (args[i] === '--verbose') commandArgs.verbose = true;
    if (args[i] === '--quick') commandArgs.quick = true;
    if (args[i] === '--full') commandArgs.full = true;
    if (args[i] === '--task-id' && args[i + 1]) {
      commandArgs.taskId = args[i + 1];
      i++;
    }
    if (command === 'reset-task' && i === 1) {
      // reset-task 命令的第一个参数是 taskId
      commandArgs.taskId = args[i];
    }
  }
  
  helper.runCommand(command, commandArgs)
    .then(result => {
      console.log(JSON.stringify(result, null, 2));
    })
    .catch(error => {
      console.error('错误:', error.message);
      process.exit(1);
    });
}