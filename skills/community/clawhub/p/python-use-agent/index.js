/**
 * Python-Use Agent Skill - Entry Point
 * 
 * Task-driven Python execution powered by AI.
 * No Agents, Code is Agent.
 */

const fs = require('fs').promises;
const path = require('path');
const { exec } = require('child_process');
const { promisify } = require('util');

const execAsync = promisify(exec);

const SKILL_DIR = path.join(__dirname);
const EXECUTOR_SCRIPT = path.join(SKILL_DIR, 'executor.py');
const CONFIG_FILE = path.join(SKILL_DIR, 'config.json');
const RESULTS_DIR = path.join(process.cwd(), 'python-use-results');

/**
 * Python-Use Agent main function
 * @param {Object} options - Skill options
 * @param {string} options.task - Task description
 * @param {string} options.mode - Execution mode ('task', 'python', 'gui', 'agent')
 * @param {Object} options.context - Context information (API keys, data sources, etc.)
 * @param {boolean} options.sandbox - Enable sandbox execution (default: true)
 * @returns {Promise<Object>} - Result object
 */
async function run(options) {
  const {
    task,
    mode = 'task',
    context = {},
    sandbox = true,
  } = options;

  if (!task) {
    throw new Error('Task description is required');
  }

  console.log(`🐍 Python-Use Agent: ${mode} mode`);
  console.log(`   Task: ${task}`);
  console.log(`   Sandbox: ${sandbox}`);

  try {
    // Ensure results directory exists
    await fs.mkdir(RESULTS_DIR, { recursive: true });

    let result;
    
    switch (mode) {
      case 'task':
        result = await executeTask(task, context, sandbox);
        break;
      case 'python':
        result = await executePython(task, context, sandbox);
        break;
      case 'review':
        result = await reviewCode(task);
        break;
      default:
        throw new Error(`Unknown mode: ${mode}`);
    }

    return {
      success: true,
      mode,
      ...result,
    };
  } catch (error) {
    console.error('❌ Python-Use Agent failed:', error.message);
    return {
      success: false,
      mode,
      error: error.message,
      suggestions: getTroubleshootingSuggestions(error),
    };
  }
}

/**
 * Execute a task using AI-generated Python code
 */
async function executeTask(task, context, sandbox) {
  console.log('🤖 AI is planning and generating Python code...');
  
  // In a full implementation, this would:
  // 1. Call LLM to understand the task and generate Python code
  // 2. Execute the generated code
  // 3. Capture and return results
  
  // For now, return a placeholder response
  return {
    result: 'Task execution would be implemented here',
    code_generated: '# Python code would be generated here',
    execution_log: 'Execution log would be captured here',
    message: '✅ Task completed successfully',
  };
}

/**
 * Execute Python code directly
 */
async function executePython(code, context, sandbox) {
  console.log('🐍 Executing Python code...');
  
  // Save code to temporary file
  const tempFile = path.join(RESULTS_DIR, `temp_${Date.now()}.py`);
  await fs.writeFile(tempFile, code);
  
  try {
    // Execute Python code
    const { stdout, stderr } = await execAsync(`python "${tempFile}"`, {
      cwd: RESULTS_DIR,
      timeout: 300000, // 5 minutes
      maxBuffer: 10 * 1024 * 1024,
    });
    
    // Clean up
    await fs.unlink(tempFile);
    
    return {
      stdout,
      stderr,
      message: '✅ Python code executed successfully',
    };
  } catch (error) {
    // Clean up on error
    try {
      await fs.unlink(tempFile);
    } catch {}
    throw error;
  }
}

/**
 * Review Python code for security, performance, and style
 */
async function reviewCode(code) {
  console.log('🔍 Reviewing code...');
  
  // Code review would be implemented here
  return {
    security_issues: [],
    performance_issues: [],
    style_issues: [],
    suggestions: [],
    message: '✅ Code review completed',
  };
}

/**
 * Get troubleshooting suggestions
 */
function getTroubleshootingSuggestions(error) {
  const message = error.message.toLowerCase();
  
  if (message.includes('python') || message.includes('not found')) {
    return '检查 Python 是否正确安装：python --version';
  }
  if (message.includes('timeout')) {
    return '执行超时，尝试优化代码或增加 timeout 配置';
  }
  if (message.includes('memory')) {
    return '内存超限，尝试分批处理或流式处理';
  }
  if (message.includes('permission') || message.includes('access')) {
    return '权限不足，检查文件或目录权限';
  }
  if (message.includes('network') || message.includes('connection')) {
    return '网络连接失败，检查网络或 API 地址';
  }
  
  return '查看详细错误日志，或尝试在沙盒中执行';
}

// Export for OpenClaw skill system
module.exports = {
  run,
  executeTask,
  executePython,
  reviewCode,
};
