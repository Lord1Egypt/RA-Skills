/**
 * system_cmd v2 - 系统命令执行脚本（增强版）
 * 支持预定义命令和自定义命令执行
 */

const { exec } = require('child_process');
const { promisify } = require('util');
const execAsync = promisify(exec);

// 预定义命令映射
const PREDEFINED_COMMANDS = {
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

// 危险命令黑名单（禁止执行）
const DANGEROUS_COMMANDS = [
  'del', 'erase', 'rm', 'rmdir', 'rd', 'format', 'chkdsk', 'diskpart',
  'reg', 'regedit', 'shutdown', 'poweroff', 'halt', 'reboot',
  'net user', 'net localgroup', 'wmic', 'bcdedit', 'bootcfg',
  'attrib', 'cacls', 'icacls', 'takeown', 'taskkill', 'tskill',
  'sc', 'schtasks', 'at', 'wusa', 'msiexec', 'dism', 'sfc',
  'vssadmin', 'wbadmin', 'bdehdcfg', 'manage-bde', 'cipher',
  'compact', 'expand', 'makecab', 'extract', 'recover',
  'subst', 'mountvol', 'label', 'vol', 'convert'
];

// 危险命令模式（正则表达式）
const DANGEROUS_PATTERNS = [
  /rm\s+-rf/i,           // rm -rf
  /del\s+\*\.\*/i,       // del *.*
  /format\s+[cdefg]/i,   // format c:
  /shutdown\s+[\/\-]/i,  // shutdown /s
  /reg\s+(add|delete)/i, // reg add/delete
  /net\s+user/i,         // net user
  /wmic\s+/i,            // wmic
  /taskkill\s+/i         // taskkill
];

/**
 * 检查命令是否危险
 * @param {string} command - 要检查的命令
 * @returns {boolean} - 是否危险
 */
function isDangerousCommand(command) {
  const cmdLower = command.toLowerCase().trim();
  
  // 如果是安全只读命令，放宽限制
  if (isSafeReadOnlyCommand(command)) {
    // 安全只读命令只检查最危险的模式
    const criticalPatterns = [
      /\\\.\.\\/i,            // 包含..路径遍历
      /\\\.\.\//i,            // 包含../路径遍历
      /^format\s+[cdefg]:/i,  // format c: 等
      /^del\s+[cdefg]:\\/i,   // del c:\ 等
      />/i,                   // 输出重定向
      />>/i,                  // 追加输出重定向
      /\|/i,                  // 管道
      /&&/i,                  // 逻辑与
      /\|\|/i,                // 逻辑或
      /;/i,                   // 命令分隔符
      /\$/i,                  // 变量引用
      /`/i,                   // 命令替换
      /%/i,                   // 变量
      /&/i                    // 后台执行
    ];
    
    for (const pattern of criticalPatterns) {
      if (pattern.test(cmdLower)) {
        return true;
      }
    }
    
    return false;
  }
  
  // 检查黑名单中的命令
  for (const dangerousCmd of DANGEROUS_COMMANDS) {
    if (cmdLower.startsWith(dangerousCmd.toLowerCase())) {
      return true;
    }
  }
  
  // 检查危险模式
  for (const pattern of DANGEROUS_PATTERNS) {
    if (pattern.test(cmdLower)) {
      return true;
    }
  }
  
  // 检查是否包含危险字符或路径
  const dangerousIndicators = [
    'c:\\windows\\system32', 'c:\\windows\\syswow64',
    '..\\', '../', '>', '>>', '|', '&&', '||', ';',
    '$(', '`', '%', '&'
  ];
  
  // 检查危险路径（必须是完整路径，不是部分匹配）
  for (const indicator of dangerousIndicators) {
    // 对于路径检查，需要确保是完整路径匹配
    if (indicator.includes(':\\')) {
      // 检查是否包含危险系统路径
      if (cmdLower.includes(indicator)) {
        return true;
      }
    } else {
      // 对于其他危险字符，直接检查包含
      if (cmdLower.includes(indicator)) {
        return true;
      }
    }
  }
  
  // 检查危险命令模式（更精确的匹配）
  const dangerousCommandPatterns = [
    /^c:\\windows\\/i,      // 以c:\windows\开头
    /^c:\\program files\\/i, // 以c:\program files\开头
    /\\\.\.\\/i,            // 包含..路径遍历
    /\\\.\.\//i,            // 包含../路径遍历
    /^format\s+[cdefg]:/i,  // format c: 等
    /^del\s+[cdefg]:\\/i,   // del c:\ 等
  ];
  
  for (const pattern of dangerousCommandPatterns) {
    if (pattern.test(cmdLower)) {
      return true;
    }
  }
  
  return false;
}

/**
 * 执行预定义系统命令
 * @param {string} commandName - 命令名称
 * @returns {Promise<string>} - 命令执行结果
 */
async function executePredefinedCommand(commandName) {
  // 检查命令是否支持
  if (!PREDEFINED_COMMANDS[commandName]) {
    const supportedCommands = Object.keys(PREDEFINED_COMMANDS).join(', ');
    throw new Error(`不支持的命令: ${commandName}\n支持的命令: ${supportedCommands}`);
  }

  const commandConfig = PREDEFINED_COMMANDS[commandName];
  
  try {
    console.log(`正在执行预定义命令: ${commandConfig.cmd}`);
    
    // 使用PowerShell执行命令，确保编码正确
    const powershellCommand = `powershell -Command "& {chcp 65001 > $null; ${commandConfig.cmd}}"`;
    
    const options = {
      maxBuffer: 1024 * 1024 * 10, // 10MB buffer
      encoding: 'utf8',
      timeout: 30000 // 30秒超时
    };
    
    const { stdout, stderr } = await execAsync(powershellCommand, options);
    
    if (stderr && stderr.trim() !== '') {
      console.warn(`命令执行警告: ${stderr}`);
    }
    
    // 格式化输出
    return formatOutput(commandName, stdout || '', commandConfig.format, true);
    
  } catch (error) {
    console.error(`预定义命令执行失败: ${error.message}`);
    
    // 提供更友好的错误信息
    if (error.code === 'ENOENT') {
      throw new Error(`找不到命令: ${commandName}。请确保系统路径正确。`);
    } else if (error.code === 1) {
      throw new Error(`命令执行失败: ${commandName}。可能需要管理员权限。`);
    } else if (error.killed) {
      throw new Error(`命令执行超时: ${commandName}。`);
    } else {
      throw new Error(`执行 ${commandName} 时出错: ${error.message}`);
    }
  }
}

/**
 * 检查是否是CMD特有命令
 * @param {string} command - 命令
 * @returns {boolean} - 是否是CMD特有命令
 */
function isCmdSpecificCommand(command) {
  const cmdLower = command.toLowerCase().trim();
  const cmdSpecificCommands = [
    'dir', 'copy', 'xcopy', 'move', 'ren', 'rename',
    'type', 'more', 'find', 'findstr', 'sort',
    'date', 'time', 'ver', 'vol', 'label',
    'tree', 'chcp', 'prompt', 'title', 'cls',
    'color', 'mode', 'echo', 'pause', 'exit'
  ];
  
  // 检查命令是否以CMD特有命令开头
  for (const cmd of cmdSpecificCommands) {
    if (cmdLower.startsWith(cmd + ' ') || cmdLower === cmd) {
      return true;
    }
  }
  
  return false;
}

/**
 * 检查是否是安全的只读命令
 * @param {string} command - 命令
 * @returns {boolean} - 是否是安全的只读命令
 */
function isSafeReadOnlyCommand(command) {
  const cmdLower = command.toLowerCase().trim();
  const safeReadOnlyCommands = [
    'vol', 'ver', 'hostname', 'whoami', 'echo',
    'date', 'time', 'dir', 'tree'
  ];
  
  // 检查命令是否以安全只读命令开头
  for (const cmd of safeReadOnlyCommands) {
    if (cmdLower.startsWith(cmd + ' ') || cmdLower === cmd) {
      return true;
    }
  }
  
  return false;
}

/**
 * 执行自定义命令
 * @param {string} userCommand - 用户输入的命令
 * @returns {Promise<string>} - 命令执行结果
 */
async function executeCustomCommand(userCommand) {
  // 安全检查
  if (isDangerousCommand(userCommand)) {
    throw new Error(`安全限制: 禁止执行危险命令 "${userCommand}"`);
  }
  
  // 命令长度限制
  if (userCommand.length > 1000) {
    throw new Error(`命令过长: 最大允许1000字符，当前${userCommand.length}字符`);
  }
  
  try {
    console.log(`正在执行自定义命令: ${userCommand}`);
    
    let fullCommand;
    
    // 根据命令类型选择执行方式
    if (isCmdSpecificCommand(userCommand)) {
      // CMD特有命令使用CMD执行
      fullCommand = `cmd /c "chcp 65001 >nul && ${userCommand}"`;
    } else {
      // 其他命令使用PowerShell执行
      fullCommand = `powershell -Command "& {chcp 65001 > $null; ${userCommand}}"`;
    }
    
    const options = {
      maxBuffer: 1024 * 1024 * 5, // 5MB buffer（自定义命令限制更严格）
      encoding: 'utf8',
      timeout: 15000 // 15秒超时（自定义命令限制更严格）
    };
    
    const { stdout, stderr } = await execAsync(fullCommand, options);
    
    if (stderr && stderr.trim() !== '') {
      console.warn(`自定义命令执行警告: ${stderr}`);
    }
    
    // 格式化输出
    return formatOutput('自定义命令', stdout || '', 'text', false, userCommand);
    
  } catch (error) {
    console.error(`自定义命令执行失败: ${error.message}`);
    
    // 提供更友好的错误信息
    if (error.code === 'ENOENT') {
      throw new Error(`找不到命令或程序。请检查命令是否正确。`);
    } else if (error.code === 1) {
      throw new Error(`命令执行失败。返回代码: 1`);
    } else if (error.killed) {
      throw new Error(`命令执行超时（15秒限制）。`);
    } else if (error.signal === 'SIGTERM') {
      throw new Error(`命令被终止。`);
    } else {
      throw new Error(`执行自定义命令时出错: ${error.message}`);
    }
  }
}

/**
 * 格式化输出
 * @param {string} commandName - 命令名称
 * @param {string} output - 原始输出
 * @param {string} format - 输出格式
 * @param {boolean} isPredefined - 是否是预定义命令
 * @param {string} originalCommand - 原始命令（仅自定义命令）
 * @returns {string} - 格式化后的输出
 */
function formatOutput(commandName, output, format, isPredefined = true, originalCommand = '') {
  if (!output || output.trim() === '') {
    return `命令执行成功，但未返回任何输出。`;
  }
  
  // 清理输出
  let cleanedOutput = output.trim();
  
  // 添加标题和分隔符
  const title = isPredefined 
    ? `📊 ${commandName.toUpperCase()} 命令执行结果`
    : `🔧 自定义命令执行结果`;
  
  const separator = '='.repeat(50);
  const footer = '✅ 命令执行完成';
  
  let result = `${title}\n${separator}\n`;
  
  // 如果是自定义命令，显示原始命令
  if (!isPredefined && originalCommand) {
    result += `命令: ${originalCommand}\n${separator}\n`;
  }
  
  result += `${cleanedOutput}\n${separator}\n${footer}`;
  
  // 输出长度限制（防止过长）
  const maxLength = 4000;
  if (result.length > maxLength) {
    result = result.substring(0, maxLength) + `\n...（输出已截断，共${output.length}字符）\n${separator}\n${footer}`;
  }
  
  return result;
}

/**
 * 获取命令帮助信息
 * @returns {string} - 帮助信息
 */
function getHelp() {
  let helpText = '📋 **system_cmd 技能帮助 (v2)**\n\n';
  helpText += '**两种使用模式**:\n\n';
  
  helpText += '1. **预定义命令** (原有功能):\n';
  helpText += '   `/system_cmd <命令名>`\n\n';
  
  helpText += '2. **自定义命令** (新增功能):\n';
  helpText += '   `/system_cmd exec <命令>`\n\n';
  
  helpText += '**预定义命令**:\n';
  for (const [cmd, config] of Object.entries(PREDEFINED_COMMANDS)) {
    helpText += `- **${cmd}**: ${config.description}\n`;
  }
  
  helpText += '\n**自定义命令示例**:\n';
  helpText += '- `/system_cmd exec ping 8.8.8.8` - 网络连通性测试\n';
  helpText += '- `/system_cmd exec dir` - 查看当前目录\n';
  helpText += '- `/system_cmd exec echo Hello World` - 输出文本\n';
  helpText += '- `/system_cmd exec whoami` - 查看当前用户\n';
  helpText += '- `/system_cmd exec date /t` - 查看当前日期\n';
  helpText += '- `/system_cmd exec time /t` - 查看当前时间\n';
  helpText += '- `/system_cmd exec hostname` - 查看主机名\n';
  helpText += '- `/system_cmd exec ver` - 查看Windows版本\n';
  
  helpText += '\n**安全限制**:\n';
  helpText += '- 禁止执行危险命令（删除、格式化、系统修改等）\n';
  helpText += '- 命令长度限制：1000字符\n';
  helpText += '- 执行时间限制：15秒\n';
  helpText += '- 输出长度限制：4000字符\n';
  
  helpText += '\n**注意事项**:\n';
  helpText += '- 自定义命令在受限环境中执行\n';
  helpText += '- 复杂命令可能需要管理员权限\n';
  helpText += '- 输出可能被截断以避免过长\n';
  
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
  
  const firstArg = args[0].toLowerCase();
  
  // 特殊处理：显示帮助
  if (firstArg === 'help' || firstArg === '--help' || firstArg === '-h') {
    return getHelp();
  }
  
  // 处理自定义命令模式
  if (firstArg === 'exec') {
    if (args.length < 2) {
      return '❌ 错误: 自定义命令模式需要指定命令\n示例: /system_cmd exec ping 8.8.8.8';
    }
    
    // 提取用户命令（排除"exec"参数）
    const userCommand = args.slice(1).join(' ');
    
    try {
      const result = await executeCustomCommand(userCommand);
      return result;
    } catch (error) {
      return `❌ 自定义命令执行失败: ${error.message}\n\n${getHelp()}`;
    }
  }
  
  // 处理预定义命令模式
  try {
    const result = await executePredefinedCommand(firstArg);
    return result;
  } catch (error) {
    return `❌ 错误: ${error.message}\n\n${getHelp()}`;
  }
}

// 导出模块
module.exports = {
  executePredefinedCommand,
  executeCustomCommand,
  isDangerousCommand,
  getHelp,
  main
};