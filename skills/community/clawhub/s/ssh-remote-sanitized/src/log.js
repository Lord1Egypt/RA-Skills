/**
 * SSH 日志查看与分析功能
 * 
 * 用法：
 * - 系统日志查看
 * - 应用日志查看
 * - 日志搜索与分析
 * - 日志轮转管理
 */

const { execSSH } = require('./index');

/**
 * 查看系统日志
 * @param {string} serverName - 服务器名称
 * @param {number} lines - 行数
 */
async function viewSystemLog(serverName, lines = 50) {
  const result = await execSSH(serverName, `tail -n ${lines} /var/log/syslog 2>/dev/null || tail -n ${lines} /var/log/messages`);
  
  return {
    success: result.success,
    output: result.stdout
  };
}

/**
 * 查看认证日志
 * @param {string} serverName - 服务器名称
 * @param {number} lines - 行数
 */
async function viewAuthLog(serverName, lines = 50) {
  const result = await execSSH(serverName, `tail -n ${lines} /var/log/auth.log 2>/dev/null || tail -n ${lines} /var/log/secure`);
  
  return {
    success: result.success,
    output: result.stdout
  };
}

/**
 * 查看 Nginx 日志
 * @param {string} serverName - 服务器名称
 * @param {string} type - 日志类型 (access|error)
 * @param {number} lines - 行数
 */
async function viewNginxLog(serverName, type = 'error', lines = 50) {
  const logPath = type === 'access' ? '/var/log/nginx/access.log' : '/var/log/nginx/error.log';
  const result = await execSSH(serverName, `tail -n ${lines} ${logPath}`);
  
  return {
    success: result.success,
    output: result.stdout
  };
}

/**
 * 查看 Apache 日志
 * @param {string} serverName - 服务器名称
 * @param {string} type - 日志类型 (access|error)
 * @param {number} lines - 行数
 */
async function viewApacheLog(serverName, type = 'error', lines = 50) {
  const logPath = type === 'access' ? '/var/log/apache2/access.log' : '/var/log/apache2/error.log';
  const result = await execSSH(serverName, `tail -n ${lines} ${logPath}`);
  
  return {
    success: result.success,
    output: result.stdout
  };
}

/**
 * 查看 MySQL 日志
 * @param {string} serverName - 服务器名称
 * @param {number} lines - 行数
 */
async function viewMySQLLog(serverName, lines = 50) {
  const result = await execSSH(serverName, `tail -n ${lines} /var/log/mysql/error.log 2>/dev/null || tail -n ${lines} /var/log/mysqld.log`);
  
  return {
    success: result.success,
    output: result.stdout
  };
}

/**
 * 查看 Docker 日志
 * @param {string} serverName - 服务器名称
 * @param {string} containerName - 容器名称
 * @param {number} lines - 行数
 */
async function viewDockerLog(serverName, containerName, lines = 50) {
  const result = await execSSH(serverName, `docker logs --tail ${lines} ${containerName}`);
  
  return {
    success: result.success,
    output: result.stdout
  };
}

/**
 * 搜索日志内容
 * @param {string} serverName - 服务器名称
 * @param {string} logFile - 日志文件路径
 * @param {string} pattern - 搜索模式
 * @param {number} lines - 返回行数
 */
async function searchLog(serverName, logFile, pattern, lines = 50) {
  const result = await execSSH(serverName, `grep -i "${pattern}" ${logFile} | tail -n ${lines}`);
  
  return {
    success: result.success,
    output: result.stdout
  };
}

/**
 * 分析日志错误
 * @param {string} serverName - 服务器名称
 * @param {string} logFile - 日志文件路径
 */
async function analyzeLogErrors(serverName, logFile) {
  const result = await execSSH(serverName, `
    echo "=== 错误统计 ===" &&
    grep -ci "error" ${logFile} 2>/dev/null &&
    echo "" &&
    echo "=== 最近错误 ===" &&
    grep -i "error" ${logFile} | tail -20 &&
    echo "" &&
    echo "=== 警告统计 ===" &&
    grep -ci "warning\|warn" ${logFile} 2>/dev/null &&
    echo "" &&
    echo "=== 最近警告 ===" &&
    grep -i "warning\|warn" ${logFile} | tail -10
  `);
  
  return {
    success: result.success,
    output: result.stdout
  };
}

/**
 * 查看 Journal 日志
 * @param {string} serverName - 服务器名称
 * @param {Object} options - 查询选项
 */
async function viewJournalLog(serverName, options = {}) {
  const {
    unit,
    priority,
    since,
    lines = 50
  } = options;
  
  let cmd = `journalctl --no-pager -n ${lines}`;
  
  if (unit) {
    cmd += ` -u ${unit}`;
  }
  
  if (priority) {
    cmd += ` -p ${priority}`;
  }
  
  if (since) {
    cmd += ` --since "${since}"`;
  }
  
  const result = await execSSH(serverName, cmd);
  
  return {
    success: result.success,
    output: result.stdout
  };
}

/**
 * 日志轮转管理
 * @param {string} serverName - 服务器名称
 * @param {string} action - 操作 (list|rotate|status)
 */
async function manageLogrotate(serverName, action = 'list') {
  if (action === 'list') {
    const result = await execSSH(serverName, 'ls -la /etc/logrotate.d/');
    return { success: result.success, output: result.stdout };
  }
  
  if (action === 'rotate') {
    const result = await execSSH(serverName, 'sudo logrotate -f /etc/logrotate.conf');
    return { success: result.success, output: result.stdout };
  }
  
  if (action === 'status') {
    const result = await execSSH(serverName, 'cat /var/lib/logrotate/status');
    return { success: result.success, output: result.stdout };
  }
  
  throw new Error(`未知操作：${action}`);
}

/**
 * 清理旧日志
 * @param {string} serverName - 服务器名称
 * @param {number} days - 保留天数
 */
async function cleanupOldLogs(serverName, days = 7) {
  const result = await execSSH(serverName, `
    echo "=== 清理 ${days} 天前的日志 ===" &&
    sudo find /var/log -type f -name "*.log" -mtime +${days} -delete &&
    echo "清理完成"
  `);
  
  return {
    success: result.success,
    output: result.stdout
  };
}

/**
 * 实时监控日志
 * @param {string} serverName - 服务器名称
 * @param {string} logFile - 日志文件路径
 */
async function followLog(serverName, logFile) {
  const result = await execSSH(serverName, `tail -f ${logFile}`, { pty: true });
  
  return {
    success: result.success,
    output: result.stdout
  };
}

/**
 * 日志分析摘要
 * @param {string} serverName - 服务器名称
 */
async function getLogSummary(serverName) {
  const result = await execSSH(serverName, `
    echo "========== 日志摘要 ==========" &&
    echo "" &&
    echo "=== 系统日志大小 ===" &&
    du -sh /var/log/* 2>/dev/null | sort -hr | head -10 &&
    echo "" &&
    echo "=== 最近系统错误 ===" &&
    grep -i "error" /var/log/syslog 2>/dev/null | tail -5 || echo "无系统日志" &&
    echo "" &&
    echo "=== 最近认证失败 ===" &&
    grep -i "failed" /var/log/auth.log 2>/dev/null | tail -5 || echo "无认证日志"
  `);
  
  return {
    success: result.success,
    output: result.stdout
  };
}

module.exports = {
  viewSystemLog,
  viewAuthLog,
  viewNginxLog,
  viewApacheLog,
  viewMySQLLog,
  viewDockerLog,
  searchLog,
  analyzeLogErrors,
  viewJournalLog,
  manageLogrotate,
  cleanupOldLogs,
  followLog,
  getLogSummary
};
