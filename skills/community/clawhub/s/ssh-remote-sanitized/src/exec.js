/**
 * SSH 远程命令执行功能
 * 
 * 用法：
 * - 执行单个命令
 * - 执行多个命令
 * - 后台执行
 */

const { execSSH, getSSHConnection } = require('./index');

/**
 * 执行单个命令
 * @param {string} serverName - 服务器名称
 * @param {string} command - 命令
 */
async function execCommand(serverName, command) {
  const result = await execSSH(serverName, command);
  
  return {
    serverName,
    command,
    exitCode: result.code,
    output: result.stdout,
    error: result.stderr,
    success: result.success
  };
}

/**
 * 执行多个命令
 * @param {string} serverName - 服务器名称
 * @param {Array} commands - 命令列表
 */
async function execCommands(serverName, commands) {
  const results = [];
  
  for (const command of commands) {
    try {
      const result = await execSSH(serverName, command);
      results.push({
        command,
        exitCode: result.code,
        output: result.stdout,
        error: result.stderr,
        success: result.success
      });
    } catch (error) {
      results.push({
        command,
        success: false,
        error: error.message
      });
    }
  }
  
  return results;
}

/**
 * 执行命令并解析 JSON 输出
 * @param {string} serverName - 服务器名称
 * @param {string} command - 命令
 */
async function execJSON(serverName, command) {
  const result = await execSSH(serverName, command);
  
  if (!result.success) {
    throw new Error(result.stderr || '命令执行失败');
  }
  
  try {
    return JSON.parse(result.stdout);
  } catch (e) {
    throw new Error('输出不是有效的 JSON 格式');
  }
}

/**
 * 交互式执行（支持多行命令）
 * @param {string} serverName - 服务器名称
 * @param {string} script - 脚本内容
 */
async function execScript(serverName, script) {
  // 将脚本写入临时文件并执行
  const tempFile = `/tmp/ssh_remote_${Date.now()}.sh`;
  
  await execSSH(serverName, `cat > ${tempFile} << 'EOF'\n${script}\nEOF`);
  await execSSH(serverName, `chmod +x ${tempFile}`);
  const result = await execSSH(serverName, `bash ${tempFile}`);
  await execSSH(serverName, `rm -f ${tempFile}`);
  
  return {
    serverName,
    exitCode: result.code,
    output: result.stdout,
    error: result.stderr,
    success: result.success
  };
}

/**
 * 常用系统命令
 */
const systemCommands = {
  // 系统信息
  systemInfo: 'uname -a',
  hostname: 'hostname',
  uptime: 'uptime',
  
  // CPU
  cpuInfo: 'cat /proc/cpuinfo | grep "model name" | head -1',
  cpuCount: 'nproc',
  loadAvg: 'cat /proc/loadavg',
  
  // 内存
  memoryInfo: 'free -h',
  memoryDetail: 'cat /proc/meminfo | head -10',
  
  // 磁盘
  diskUsage: 'df -h',
  diskIO: 'iostat -x 1 1',
  
  // 网络
  networkInfo: 'ip addr show',
  networkStat: 'netstat -tulpn',
  publicIP: 'curl -s ifconfig.me',
  
  // 进程
  topProcess: 'ps aux --sort=-%cpu | head -10',
  topMemory: 'ps aux --sort=-%mem | head -10',
  
  // 用户
  whoami: 'whoami',
  users: 'who',
  lastLogin: 'last -n 5'
};

/**
 * 执行预定义系统命令
 * @param {string} serverName - 服务器名称
 * @param {string} commandKey - 命令键
 */
async function execSystemCommand(serverName, commandKey) {
  const command = systemCommands[commandKey];
  
  if (!command) {
    throw new Error(`未知命令：${commandKey}`);
  }
  
  return execCommand(serverName, command);
}

/**
 * 获取系统概览
 * @param {string} serverName - 服务器名称
 */
async function getSystemOverview(serverName) {
  const commands = [
    'hostname',
    'uname -r',
    'uptime -p',
    'free -h',
    'df -h /',
    'cat /proc/loadavg'
  ];
  
  const results = await execCommands(serverName, commands);
  
  return {
    hostname: results[0].output.trim(),
    kernel: results[1].output.trim(),
    uptime: results[2].output.trim(),
    memory: results[3].output.trim(),
    disk: results[4].output.trim(),
    load: results[5].output.trim()
  };
}

/**
 * 批量执行命令（多台服务器）
 * @param {Array} serverNames - 服务器名称列表
 * @param {string} command - 命令
 */
async function execOnMultiple(serverNames, command) {
  const results = [];
  
  for (const serverName of serverNames) {
    try {
      const result = await execCommand(serverName, command);
      results.push({
        server: serverName,
        success: true,
        ...result
      });
    } catch (error) {
      results.push({
        server: serverName,
        success: false,
        error: error.message
      });
    }
  }
  
  return results;
}

module.exports = {
  execCommand,
  execCommands,
  execJSON,
  execScript,
  execSystemCommand,
  getSystemOverview,
  execOnMultiple,
  systemCommands
};
