/**
 * system_cmd - 系统命令执行脚本（简化版）
 * 执行常见的 Windows 系统命令并返回格式化的结果
 */

const { exec } = require('child_process');
const { promisify } = require('util');
const execAsync = promisify(exec);

// 支持的命令映射
const COMMANDS = {
  'ipconfig': {
    cmd: 'ipconfig /all',
    description: '查看网络接口配置和IP地址',
    format: 'text'
  },
  'tasklist': {
    cmd: 'tasklist',
    description: '查看当前运行的进程列表',
    format: 'table'
  },
  'netstat': {
    cmd: 'netstat -an',
    description: '查看所有网络连接和监听端口',
    format: 'table'
  },
  'systeminfo': {
    cmd: 'systeminfo',
    description: '查看详细的系统信息',
    format: 'text'
  }
};

/**
 * 执行系统命令
 * @param {string} commandName - 命令名称
 * @returns {Promise<string>} - 命令执行结果
 */
async function executeSystemCommand(commandName) {
  // 检查命令是否支持
  if (!COMMANDS[commandName]) {
    const supportedCommands = Object.keys(COMMANDS).join(', ');
    throw new Error(`不支持的命令: ${commandName}\n支持的命令: ${supportedCommands}`);
  }

  const commandConfig = COMMANDS[commandName];
  
  try {
    console.log(`正在执行命令: ${commandConfig.cmd}`);
    
    // 使用PowerShell执行命令，确保编码正确
    const powershellCommand = `powershell -Command "& {chcp 65001 > $null; ${commandConfig.cmd}}"`;
    
    const options = {
      maxBuffer: 1024 * 1024 * 10, // 10MB buffer
      encoding: 'utf8'
    };
    
    const { stdout, stderr } = await execAsync(powershellCommand, options);
    
    if (stderr && stderr.trim() !== '') {
      console.warn(`命令执行警告: ${stderr}`);
    }
    
    // 格式化输出
    return formatOutput(commandName, stdout || '', commandConfig.format);
    
  } catch (error) {
    console.error(`命令执行失败: ${error.message}`);
    
    // 提供更友好的错误信息
    if (error.code === 'ENOENT') {
      throw new Error(`找不到命令: ${commandName}。请确保系统路径正确。`);
    } else if (error.code === 1) {
      throw new Error(`命令执行失败: ${commandName}。可能需要管理员权限。`);
    } else {
      throw new Error(`执行 ${commandName} 时出错: ${error.message}`);
    }
  }
}

/**
 * 格式化输出
 * @param {string} commandName - 命令名称
 * @param {string} output - 原始输出
 * @param {string} format - 输出格式
 * @returns {string} - 格式化后的输出
 */
function formatOutput(commandName, output, format) {
  if (!output || output.trim() === '') {
    return `命令 ${commandName} 执行成功，但未返回任何输出。`;
  }
  
  // 清理输出
  let cleanedOutput = output.trim();
  
  // 添加标题和分隔符
  const title = `📊 ${commandName.toUpperCase()} 命令执行结果`;
  const separator = '='.repeat(50);
  const footer = '✅ 命令执行完成';
  
  return `${title}\n${separator}\n${cleanedOutput}\n${separator}\n${footer}`;
}

/**
 * 获取命令帮助信息
 * @returns {string} - 帮助信息
 */
function getHelp() {
  let helpText = '📋 **system_cmd 技能帮助**\n\n';
  helpText += '**用法**: /system_cmd <命令名>\n\n';
  helpText += '**支持的命令**:\n';
  
  for (const [cmd, config] of Object.entries(COMMANDS)) {
    helpText += `- **${cmd}**: ${config.description}\n`;
  }
  
  helpText += '\n**示例**:\n';
  helpText += '- `/system_cmd ipconfig` - 查看IP配置\n';
  helpText += '- `/system_cmd tasklist` - 查看进程列表\n';
  helpText += '- `/system_cmd netstat` - 查看网络连接\n';
  helpText += '- `/system_cmd systeminfo` - 查看系统信息\n';
  
  return helpText;
}

/**
 * 主处理函数
 * @param {Object} context - 执行上下文
 * @param {Array} args - 命令参数
 * @returns {Promise<string>} - 处理结果
 */
async function main(context, args) {
  // 如果没有参数，显示帮助
  if (!args || args.length === 0) {
    return getHelp();
  }
  
  const commandName = args[0].toLowerCase();
  
  // 特殊处理：显示帮助
  if (commandName === 'help' || commandName === '--help' || commandName === '-h') {
    return getHelp();
  }
  
  try {
    const result = await executeSystemCommand(commandName);
    return result;
  } catch (error) {
    return `❌ 错误: ${error.message}\n\n${getHelp()}`;
  }
}

// 导出模块
module.exports = {
  executeSystemCommand,
  getHelp,
  main
};