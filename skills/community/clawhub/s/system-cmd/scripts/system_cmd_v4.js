/**
 * system_cmd v4 - 系统命令执行脚本（带别名功能版）
 * 支持命令别名、预定义命令、自定义命令执行，高危命令需要确认
 */

const { exec } = require('child_process');
const { promisify } = require('util');
const execAsync = promisify(exec);
const fs = require('fs');
const path = require('path');

// 配置文件路径
const CONFIG_FILE = path.join(__dirname, '..', 'config.json');

// 默认配置
const DEFAULT_CONFIG = {
  pingDefaultTarget: '8.8.8.8',
  aliases: {
    'ip': 'ipconfig',
    '进程': 'tasklist',
    '网络': 'netstat',
    '系统': 'systeminfo',
    'ping': 'ping ${pingDefaultTarget}'
  }
};

// 加载配置
let config = { ...DEFAULT_CONFIG };
try {
  if (fs.existsSync(CONFIG_FILE)) {
    const configData = fs.readFileSync(CONFIG_FILE, 'utf8');
    const userConfig = JSON.parse(configData);
    config = { ...DEFAULT_CONFIG, ...userConfig };
    
    // 确保aliases合并正确
    if (userConfig.aliases) {
      config.aliases = { ...DEFAULT_CONFIG.aliases, ...userConfig.aliases };
    }
  }
} catch (error) {
  console.warn(`无法加载配置文件 ${CONFIG_FILE}:`, error.message);
}

// 预定义命令映射
const PREDEFINED_COMMANDS = {
  'ipconfig': {
    cmd: 'ipconfig /all',
    description: '查看网络接口配置和IP地址',
    format: 'text',
    aliases: ['ip', '网络配置', 'ip地址']
  },
  'tasklist': {
    cmd: 'tasklist',
    description: '查看当前运行的进程列表',
    format: 'table',
    aliases: ['进程', '进程列表', '任务列表']
  },
  'netstat': {
    cmd: 'netstat -an',
    description: '查看所有网络连接和监听端口',
    format: 'table',
    aliases: ['网络', '网络连接', '端口']
  },
  'systeminfo': {
    cmd: 'systeminfo',
    description: '查看详细的系统信息',
    format: 'text',
    aliases: ['系统', '系统信息', '系统状态']
  },
  'ping': {
    cmd: `ping ${config.pingDefaultTarget}`,
    description: `Ping测试（默认目标: ${config.pingDefaultTarget}）`,
    format: 'text',
    aliases: ['ping测试', '网络测试'],
    isAliasCommand: true // 标记为别名命令，不直接执行
  }
};

// 高危命令列表（需要用户确认）
const HIGH_RISK_COMMANDS = [
  'del', 'erase', 'rm', 'rmdir', 'rd',
  'format', 'chkdsk', 'diskpart',
  'taskkill /f', 'taskkill /im',
  'net stop', 'net start',
  'sc delete', 'sc stop', 'sc start',
  'reg delete', 'reg add',
  'shutdown', 'poweroff', 'halt', 'reboot'
];

// 危险命令黑名单（完全禁止执行）
const FORBIDDEN_COMMANDS = [
  'rm -rf', 'del *.*', 'format c:', 'format d:', 'format e:', 'format f:',
  'reg delete HKLM', 'reg delete HKCU',
  'net user administrator', 'net localgroup administrators'
];

// 高危命令模式（正则表达式）
const HIGH_RISK_PATTERNS = [
  /^del\s+[cdefg]:\\/i,          // del c:\
  /^format\s+[cdefg]:/i,         // format c:
  /^taskkill\s+\/f/i,            // taskkill /f
  /^net\s+stop/i,                // net stop
  /^sc\s+delete/i,               // sc delete
  /^reg\s+delete/i,              // reg delete
  /^shutdown\s+[\/\-]/i,         // shutdown /s
  /rm\s+-rf/i                    // rm -rf
];

// 完全禁止的命令模式
const FORBIDDEN_PATTERNS = [
  /rm\s+-rf\s+[\/\\]/i,          // rm -rf /
  /del\s+\*\.\*\s+[\/\\]/i,      // del *.* /
  /format\s+[cdefg]:\s+\/y/i,    // format c: /y
  /reg\s+delete\s+HKLM/i,        // reg delete HKLM
  /net\s+user\s+administrator/i  // net user administrator
];

/**
 * 解析命令别名
 * @param {string} command - 用户输入的命令
 * @returns {Object} - 解析结果 {command: 实际命令, isAlias: 是否是别名, original: 原始输入}
 */
function resolveCommandAlias(userCommand) {
  const trimmedCmd = userCommand.trim();
  
  // 1. 首先检查是否是预定义命令
  if (PREDEFINED_COMMANDS[trimmedCmd]) {
    return {
      command: trimmedCmd,
      isAlias: false,
      original: trimmedCmd,
      resolved: trimmedCmd
    };
  }
  
  // 2. 检查配置中的别名
  if (config.aliases && config.aliases[trimmedCmd]) {
    const aliasValue = config.aliases[trimmedCmd];
    
    // 处理变量替换
    let resolvedCmd = aliasValue;
    if (aliasValue.includes('${pingDefaultTarget}')) {
      resolvedCmd = aliasValue.replace('${pingDefaultTarget}', config.pingDefaultTarget);
    }
    
    return {
      command: resolvedCmd,
      isAlias: true,
      original: trimmedCmd,
      resolved: resolvedCmd,
      aliasFrom: trimmedCmd,
      aliasTo: aliasValue
    };
  }
  
  // 3. 检查预定义命令的aliases数组
  for (const [cmdName, cmdConfig] of Object.entries(PREDEFINED_COMMANDS)) {
    if (cmdConfig.aliases && cmdConfig.aliases.includes(trimmedCmd)) {
      return {
        command: cmdName,
        isAlias: true,
        original: trimmedCmd,
        resolved: cmdName,
        aliasFrom: trimmedCmd,
        aliasTo: cmdName
      };
    }
  }
  
  // 4. 不是别名，返回原始命令
  return {
    command: trimmedCmd,
    isAlias: false,
    original: trimmedCmd,
    resolved: trimmedCmd
  };
}

/**
 * 检查命令是否完全禁止
 * @param {string} command - 要检查的命令
 * @returns {boolean} - 是否完全禁止
 */
function isForbiddenCommand(command) {
  const cmdLower = command.toLowerCase().trim();
  
  // 检查完全禁止的命令
  for (const forbiddenCmd of FORBIDDEN_COMMANDS) {
    if (cmdLower.includes(forbiddenCmd.toLowerCase())) {
      return true;
    }
  }
  
  // 检查完全禁止的模式
  for (const pattern of FORBIDDEN_PATTERNS) {
    if (pattern.test(cmdLower)) {
      return true;
    }
  }
  
  return false;
}

/**
 * 检查命令是否是高危命令（需要确认）
 * @param {string} command - 要检查的命令
 * @returns {boolean} - 是否是高危命令
 */
function isHighRiskCommand(command) {
  const cmdLower = command.toLowerCase().trim();
  
  // 如果是完全禁止的命令，直接返回true（会被完全阻止）
  if (isForbiddenCommand(command)) {
    return true;
  }
  
  // 检查高危命令列表
  for (const highRiskCmd of HIGH_RISK_COMMANDS) {
    if (cmdLower.startsWith(highRiskCmd.toLowerCase())) {
      return true;
    }
  }
  
  // 检查高危命令模式
  for (const pattern of HIGH_RISK_PATTERNS) {
    if (pattern.test(cmdLower)) {
      return true;
    }
  }
  
  return false;
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
    'date', 'time', 'dir', 'tree', 'ping',
    'ipconfig', 'netstat', 'tasklist', 'systeminfo'
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
 * 获取高危命令的风险描述
 * @param {string} command - 高危命令
 * @returns {string} - 风险描述
 */
function getHighRiskDescription(command) {
  const cmdLower = command.toLowerCase().trim();
  
  if (cmdLower.startsWith('del') || cmdLower.startsWith('erase') || cmdLower.startsWith('rm')) {
    return '⚠️ 删除文件/目录操作 - 可能导致数据丢失';
  } else if (cmdLower.startsWith('format')) {
    return '💥 磁盘格式化操作 - 将清除整个磁盘数据';
  } else if (cmdLower.startsWith('taskkill')) {
    return '🔴 强制终止进程 - 可能导致程序异常或数据丢失';
  } else if (cmdLower.startsWith('net stop') || cmdLower.startsWith('sc stop')) {
    return '🛑 停止系统服务 - 可能影响系统功能';
  } else if (cmdLower.startsWith('sc delete')) {
    return '🗑️ 删除系统服务 - 永久移除服务配置';
  } else if (cmdLower.startsWith('reg delete')) {
    return '🔧 删除注册表项 - 可能影响系统或程序运行';
  } else if (cmdLower.startsWith('shutdown')) {
    return '⏰ 系统关机/重启 - 将中断当前工作';
  } else {
    return '⚠️ 高危系统操作';
  }
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
  
  // 如果是别名命令（如ping），需要特殊处理
  if (commandConfig.isAliasCommand) {
    return executeCustomCommand(commandConfig.cmd, false, true);
  }
  
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
    return formatOutput(commandName, stdout || '', commandConfig.format, true, '', false, false);
    
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
 * 执行自定义命令（带权限控制）
 * @param {string} userCommand - 用户输入的命令
 * @param {boolean} confirmed - 用户是否已确认高危命令
 * @param {boolean} isFromAlias - 是否来自别名解析
 * @returns {Promise<string>} - 命令执行结果
 */
async function executeCustomCommand(userCommand, confirmed = false, isFromAlias = false) {
  // 检查命令是否完全禁止
  if (isForbiddenCommand(userCommand)) {
    throw new Error(`🚫 安全限制: 禁止执行危险命令 "${userCommand}"\n该命令可能对系统造成严重破坏。`);
  }
  
  // 检查是否是高危命令
  const isHighRisk = isHighRiskCommand(userCommand);
  
  // 如果是高危命令且用户未确认，返回确认提示
  if (isHighRisk && !confirmed) {
    const riskDesc = getHighRiskDescription(userCommand);
    return `⚠️ **高危命令需要确认**\n\n` +
           `命令: \`${userCommand}\`\n` +
           `风险: ${riskDesc}\n\n` +
           `如果你确定要执行此命令，请回复:\n` +
           `\`/system_cmd exec ${userCommand} --yes\`\n\n` +
           `**警告**: 高危命令可能导致数据丢失或系统异常！`;
  }
  
  // 命令长度限制
  if (userCommand.length > 1000) {
    throw new Error(`命令过长: 最大允许1000字符，当前${userCommand.length}字符`);
  }
  
  try {
    console.log(`正在执行自定义命令: ${userCommand} ${isHighRisk ? '(高危命令，已确认)' : ''} ${isFromAlias ? '(来自别名)' : ''}`);
    
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
      timeout: isHighRisk ? 30000 : 15000 // 高危命令30秒，普通命令15秒
    };
    
    const { stdout, stderr } = await execAsync(fullCommand, options);
    
    if (stderr && stderr.trim() !== '') {
      console.warn(`自定义命令执行警告: ${stderr}`);
    }
    
    // 格式化输出
    const isHighRiskExecuted = isHighRisk;
    return formatOutput('自定义命令', stdout || '', 'text', false, userCommand, isHighRiskExecuted, isFromAlias);
    
  } catch (error) {
    console.error(`自定义命令执行失败: ${error.message}`);
    
    // 提供更友好的错误信息
    if (error.code === 'ENOENT') {
      throw new Error(`找不到命令或程序。请检查命令是否正确。`);
    } else if (error.code === 1) {
      throw new Error(`命令执行失败。返回代码: 1`);
    } else if (error.killed) {
      throw new Error(`命令执行超时（${isHighRisk ? '30' : '15'}秒限制）。`);
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
 * @param {boolean} isHighRisk - 是否是高危命令
 * @param {boolean} isFromAlias - 是否来自别名
 * @returns {string} - 格式化后的输出
 */
function formatOutput(commandName, output, format, isPredefined = true, originalCommand = '', isHighRisk = false, isFromAlias = false) {
  if (!output || output.trim() === '') {
    return `命令执行成功，但未返回任何输出。`;
  }
  
  // 清理输出
  let cleanedOutput = output.trim();
  
  // 添加标题和分隔符
  let title;
  if (isPredefined) {
    title = `📊 ${commandName.toUpperCase()} 命令执行结果`;
  } else if (isHighRisk) {
    title = `⚠️ 高危命令执行结果`;
  } else {
    title = `🔧 自定义命令执行结果`;
  }
  
  const separator = '='.repeat(50);
  const footer = isHighRisk ? '⚠️ 高危命令执行完成（请谨慎操作）' : '✅ 命令执行完成';
  
  let result = `${title}\n${separator}\n`;
  
  // 如果是自定义命令，显示原始命令
  if (!isPredefined && originalCommand) {
    result += `命令: ${originalCommand}\n`;
    if (isHighRisk) {
      result += `类型: ⚠️ 高危命令\n`;
    }
    if (isFromAlias) {
      result += `来源: 🔄 命令别名\n`;
    }
    result += `${separator}\n`;
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
  let helpText = '📋 **system_cmd 技能帮助 (v4 - 带别名功能)**\n\n';
  helpText += '**四种使用模式**:\n\n';
  
  helpText += '1. **预定义命令** (安全命令):\n';
  helpText += '   `/system_cmd <命令名>`\n\n';
  
  helpText += '2. **命令别名** (快捷方式):\n';
  helpText += '   `/system_cmd <别名>`\n\n';
  
  helpText += '3. **自定义命令** (普通命令):\n';
  helpText += '   `/system_cmd exec <命令>`\n\n';
  
  helpText += '4. **高危命令** (需要确认):\n';
  helpText += '   `/system_cmd exec <高危命令> --yes`\n\n';
  
  helpText += '**预定义命令及别名**:\n';
  for (const [cmd, config] of Object.entries(PREDEFINED_COMMANDS)) {
    helpText += `- **${cmd}**: ${config.description}\n`;
    if (config.aliases && config.aliases.length > 0) {
      helpText += `  别名: ${config.aliases.join(', ')}\n`;
    }
  }
  
  helpText += '\n**配置别名** (config.json):\n';
  if (config.aliases) {
    for (const [alias, target] of Object.entries(config.aliases)) {
      helpText += `- **${alias}** → ${target}\n`;
    }
  }
  
  helpText += '\n**常用别名示例**:\n';
  helpText += '- `/system_cmd ip` → 查看IP配置\n';
  helpText += '- `/system_cmd 进程` → 查看进程列表\n';
  helpText += '- `/system_cmd 网络` → 查看网络连接\n';
  helpText += '- `/system_cmd 系统` → 查看系统信息\n';
  helpText += '- `/system_cmd ping` → Ping测试 (默认: ' + config.pingDefaultTarget + ')\n';
  
  helpText += '\n**自定义命令示例**:\n';
  helpText += '- `/system_cmd exec ping google.com` - 自定义Ping目标\n';
  helpText += '- `/system_cmd exec dir` - 查看当前目录\n';
  helpText += '- `/system_cmd exec echo Hello World` - 输出文本\n';
  helpText += '- `/system_cmd exec whoami` - 查看当前用户\n';
  
  helpText += '\n**高危命令示例** (需要 `--yes` 确认):\n';
  helpText += '- `/system_cmd exec del temp.txt --yes` - 删除文件\n';
  helpText += '- `/system_cmd exec taskkill /f notepad.exe --yes` - 强制结束进程\n';
  helpText += '- `/system_cmd exec net stop wuauserv --yes` - 停止Windows更新服务\n';
  
  helpText += '\n**安全等级**:\n';
  helpText += '🟢 **安全命令**: 预定义命令和别名，直接执行\n';
  helpText += '🟡 **普通命令**: 自定义命令，安全检查后执行\n';
  helpText += '🔴 **高危命令**: 需要用户确认 (`--yes`) 后执行\n';
  helpText += '🚫 **禁止命令**: 完全禁止，无法执行\n';
  
  helpText += '\n**配置说明**:\n';
  helpText += '- 配置文件: `config.json`\n';
  helpText += '- 默认Ping目标: ' + config.pingDefaultTarget + '\n';
  helpText += '- 可自定义别名和配置\n';
  
  helpText += '\n**安全限制**:\n';
  helpText += '- 命令长度限制：1000字符\n';
  helpText += '- 执行时间限制：普通15秒，高危30秒\n';
  helpText += '- 输出长度限制：4000字符\n';
  
  helpText += '\n**注意事项**:\n';
  helpText += '- 高危命令需要明确确认 (`--yes`)\n';
  helpText += '- 完全禁止的命令无法执行\n';
  helpText += '- 输出可能被截断以避免过长\n';
  helpText += '- 别名功能提供更便捷的操作方式\n';
  
  return helpText;
}

/**
 * 解析命令参数
 * @param {Array} args - 命令参数数组
 * @returns {Object} - 解析后的参数
 */
function parseCommandArgs(args) {
  const result = {
    command: '',
    confirmed: false,
    isHelp: false,
    isAlias: false,
    aliasInfo: null
  };
  
  if (!args || args.length === 0) {
    result.isHelp = true;
    return result;
  }
  
  const firstArg = args[0].toLowerCase();
  
  // 检查是否是帮助请求
  if (firstArg === 'help' || firstArg === '--help' || firstArg === '-h') {
    result.isHelp = true;
    return result;
  }
  
  // 检查是否是exec模式
  if (firstArg === 'exec') {
    if (args.length < 2) {
      result.isHelp = true;
      return result;
    }
    
    // 提取命令和确认标志
    const commandParts = [];
    let confirmed = false;
    
    for (let i = 1; i < args.length; i++) {
      if (args[i] === '--yes' || args[i] === '-y' || args[i] === '--confirm') {
        confirmed = true;
      } else {
        commandParts.push(args[i]);
      }
    }
    
    const userCommand = commandParts.join(' ');
    const aliasResult = resolveCommandAlias(userCommand);
    
    result.command = aliasResult.resolved;
    result.confirmed = confirmed;
    result.isAlias = aliasResult.isAlias;
    result.aliasInfo = aliasResult;
  } else {
    // 预定义命令或别名模式
    const aliasResult = resolveCommandAlias(args.join(' '));
    
    result.command = aliasResult.command;
    result.isAlias = aliasResult.isAlias;
    result.aliasInfo = aliasResult;
  }
  
  return result;
}

/**
 * 主处理函数
 * @param {Object} context - 执行上下文
 * @param {Array} args - 命令参数
 * @returns {Promise<string>} - 处理结果
 */
async function main(context, args) {
  // 解析参数
  const parsed = parseCommandArgs(args);
  
  // 如果是帮助请求，显示帮助
  if (parsed.isHelp) {
    return getHelp();
  }
  
  // 处理预定义命令或别名模式
  if (args[0] !== 'exec') {
    try {
      // 检查是否是预定义命令
      if (PREDEFINED_COMMANDS[parsed.command]) {
        const result = await executePredefinedCommand(parsed.command);
        
        // 如果是别名，添加别名信息
        if (parsed.isAlias && parsed.aliasInfo) {
          const aliasMsg = `\n\n🔄 别名映射: ${parsed.aliasInfo.aliasFrom} → ${parsed.aliasInfo.aliasTo}`;
          return result + aliasMsg;
        }
        
        return result;
      } else {
        // 不是预定义命令，尝试作为自定义命令执行
        const result = await executeCustomCommand(parsed.command, false, parsed.isAlias);
        
        // 如果是别名，添加别名信息
        if (parsed.isAlias && parsed.aliasInfo) {
          const aliasMsg = `\n\n🔄 别名映射: ${parsed.aliasInfo.aliasFrom} → ${parsed.aliasInfo.aliasTo}`;
          return result + aliasMsg;
        }
        
        return result;
      }
    } catch (error) {
      return `❌ 错误: ${error.message}\n\n${getHelp()}`;
    }
  }
  
  // 处理自定义命令模式
  try {
    const result = await executeCustomCommand(parsed.command, parsed.confirmed, parsed.isAlias);
    
    // 如果是别名，添加别名信息
    if (parsed.isAlias && parsed.aliasInfo) {
      const aliasMsg = `\n\n🔄 别名映射: ${parsed.aliasInfo.aliasFrom} → ${parsed.aliasInfo.aliasTo}`;
      return result + aliasMsg;
    }
    
    return result;
  } catch (error) {
    return `❌ 错误: ${error.message}\n\n${getHelp()}`;
  }
}

// 导出模块
module.exports = {
  executePredefinedCommand,
  executeCustomCommand,
  resolveCommandAlias,
  isHighRiskCommand,
  isForbiddenCommand,
  getHighRiskDescription,
  getHelp,
  main,
  parseCommandArgs,
  config
};