/**
 * SSH 系统服务管理功能
 * 
 * 用法：
 * - 系统服务管理 (systemctl)
 * - 服务状态查询
 * - 开机自启管理
 */

const { execSSH } = require('./index');

/**
 * 列出所有服务
 * @param {string} serverName - 服务器名称
 * @param {string} state - 服务状态 (all|active|inactive|failed)
 */
async function listServices(serverName, state = 'all') {
  const result = await execSSH(serverName, `systemctl list-units --type=service --state=${state} --no-pager`);
  
  return {
    success: result.success,
    output: result.stdout
  };
}

/**
 * 获取服务状态
 * @param {string} serverName - 服务器名称
 * @param {string} serviceName - 服务名称
 */
async function getServiceStatus(serverName, serviceName) {
  const result = await execSSH(serverName, `systemctl status ${serviceName} --no-pager`);
  
  return {
    success: result.success,
    output: result.stdout
  };
}

/**
 * 启动服务
 * @param {string} serverName - 服务器名称
 * @param {string} serviceName - 服务名称
 */
async function startService(serverName, serviceName) {
  const result = await execSSH(serverName, `sudo systemctl start ${serviceName}`);
  
  return {
    success: result.success,
    message: result.success ? `服务 ${serviceName} 已启动` : `启动失败：${result.stderr}`
  };
}

/**
 * 停止服务
 * @param {string} serverName - 服务器名称
 * @param {string} serviceName - 服务名称
 */
async function stopService(serverName, serviceName) {
  const result = await execSSH(serverName, `sudo systemctl stop ${serviceName}`);
  
  return {
    success: result.success,
    message: result.success ? `服务 ${serviceName} 已停止` : `停止失败：${result.stderr}`
  };
}

/**
 * 重启服务
 * @param {string} serverName - 服务器名称
 * @param {string} serviceName - 服务名称
 */
async function restartService(serverName, serviceName) {
  const result = await execSSH(serverName, `sudo systemctl restart ${serviceName}`);
  
  return {
    success: result.success,
    message: result.success ? `服务 ${serviceName} 已重启` : `重启失败：${result.stderr}`
  };
}

/**
 * 重载服务配置
 * @param {string} serverName - 服务器名称
 * @param {string} serviceName - 服务名称
 */
async function reloadService(serverName, serviceName) {
  const result = await execSSH(serverName, `sudo systemctl reload ${serviceName}`);
  
  return {
    success: result.success,
    message: result.success ? `服务 ${serviceName} 配置已重载` : `重载失败：${result.stderr}`
  };
}

/**
 * 启用开机自启
 * @param {string} serverName - 服务器名称
 * @param {string} serviceName - 服务名称
 */
async function enableService(serverName, serviceName) {
  const result = await execSSH(serverName, `sudo systemctl enable ${serviceName}`);
  
  return {
    success: result.success,
    message: result.success ? `服务 ${serviceName} 已启用开机自启` : `启用失败：${result.stderr}`
  };
}

/**
 * 禁用开机自启
 * @param {string} serverName - 服务器名称
 * @param {string} serviceName - 服务名称
 */
async function disableService(serverName, serviceName) {
  const result = await execSSH(serverName, `sudo systemctl disable ${serviceName}`);
  
  return {
    success: result.success,
    message: result.success ? `服务 ${serviceName} 已禁用开机自启` : `禁用失败：${result.stderr}`
  };
}

/**
 * 查看服务日志
 * @param {string} serverName - 服务器名称
 * @param {string} serviceName - 服务名称
 * @param {number} lines - 日志行数
 */
async function getServiceLogs(serverName, serviceName, lines = 50) {
  const result = await execSSH(serverName, `journalctl -u ${serviceName} -n ${lines} --no-pager`);
  
  return {
    success: result.success,
    output: result.stdout
  };
}

/**
 * 实时查看服务日志
 * @param {string} serverName - 服务器名称
 * @param {string} serviceName - 服务名称
 */
async function followServiceLogs(serverName, serviceName) {
  const result = await execSSH(serverName, `journalctl -u ${serviceName} -f -n 20`, { pty: true });
  
  return {
    success: result.success,
    output: result.stdout
  };
}

/**
 * 检查服务是否运行
 * @param {string} serverName - 服务器名称
 * @param {string} serviceName - 服务名称
 */
async function isServiceActive(serverName, serviceName) {
  const result = await execSSH(serverName, `systemctl is-active ${serviceName}`);
  
  return {
    active: result.stdout.trim() === 'active',
    status: result.stdout.trim()
  };
}

/**
 * 批量管理服务
 * @param {string} serverName - 服务器名称
 * @param {Array} services - 服务列表
 * @param {string} action - 操作 (start|stop|restart|status)
 */
async function manageServices(serverName, services, action) {
  const results = [];
  
  const actions = {
    start: startService,
    stop: stopService,
    restart: restartService,
    status: getServiceStatus
  };
  
  const actionFn = actions[action];
  
  if (!actionFn) {
    throw new Error(`未知操作：${action}`);
  }
  
  for (const serviceName of services) {
    try {
      const result = await actionFn(serverName, serviceName);
      results.push({ service: serviceName, success: true, ...result });
    } catch (error) {
      results.push({ service: serviceName, success: false, error: error.message });
    }
  }
  
  return results;
}

/**
 * 常用服务列表
 */
const commonServices = [
  'nginx',
  'apache2',
  'httpd',
  'mysql',
  'mysqld',
  'mariadb',
  'postgresql',
  'redis',
  'mongodb',
  'docker',
  'sshd',
  'firewalld',
  'ufw',
  'cron',
  'rsyslog'
];

/**
 * 检查常用服务状态
 * @param {string} serverName - 服务器名称
 */
async function checkCommonServices(serverName) {
  const results = [];
  
  for (const service of commonServices) {
    try {
      const status = await isServiceActive(serverName, service);
      results.push({
        service,
        active: status.active,
        status: status.status
      });
    } catch (error) {
      results.push({
        service,
        active: false,
        status: 'not-found'
      });
    }
  }
  
  return results.filter(r => r.status !== 'not-found');
}

module.exports = {
  listServices,
  getServiceStatus,
  startService,
  stopService,
  restartService,
  reloadService,
  enableService,
  disableService,
  getServiceLogs,
  followServiceLogs,
  isServiceActive,
  manageServices,
  checkCommonServices,
  commonServices
};
