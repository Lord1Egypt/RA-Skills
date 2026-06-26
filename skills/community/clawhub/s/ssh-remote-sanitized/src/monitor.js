/**
 * SSH 服务器系统监控功能
 * 
 * 用法：
 * - CPU 监控
 * - 内存监控
 * - 磁盘监控
 * - 网络监控
 * - 进程监控
 */

const { execSSH } = require('./index');

/**
 * 获取 CPU 信息
 * @param {string} serverName - 服务器名称
 */
async function getCPUInfo(serverName) {
  const result = await execSSH(serverName, `
    echo "=== CPU 基本信息 ===" &&
    cat /proc/cpuinfo | grep "model name" | head -1 &&
    echo "核心数：$(nproc)" &&
    echo "=== CPU 使用率 ===" &&
    top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4 "% 已使用"}'
  `);
  
  return {
    success: result.success,
    output: result.stdout
  };
}

/**
 * 获取内存信息
 * @param {string} serverName - 服务器名称
 */
async function getMemoryInfo(serverName) {
  const result = await execSSH(serverName, `
    echo "=== 内存使用概况 ===" &&
    free -h &&
    echo "" &&
    echo "=== 详细内存信息 ===" &&
    cat /proc/meminfo | head -10
  `);
  
  return {
    success: result.success,
    output: result.stdout
  };
}

/**
 * 获取磁盘信息
 * @param {string} serverName - 服务器名称
 */
async function getDiskInfo(serverName) {
  const result = await execSSH(serverName, `
    echo "=== 磁盘空间使用 ===" &&
    df -h &&
    echo "" &&
    echo "=== 磁盘 IO 统计 ===" &&
    iostat -x 1 1 2>/dev/null || echo "iostat 未安装"
  `);
  
  return {
    success: result.success,
    output: result.stdout
  };
}

/**
 * 获取网络信息
 * @param {string} serverName - 服务器名称
 */
async function getNetworkInfo(serverName) {
  const result = await execSSH(serverName, `
    echo "=== 网络接口 ===" &&
    ip addr show | grep -E "^[0-9]+:|inet " &&
    echo "" &&
    echo "=== 网络连接统计 ===" &&
    netstat -s | head -20 &&
    echo "" &&
    echo "=== 监听端口 ===" &&
    netstat -tulpn 2>/dev/null || ss -tulpn
  `);
  
  return {
    success: result.success,
    output: result.stdout
  };
}

/**
 * 获取进程信息
 * @param {string} serverName - 服务器名称
 * @param {string} sortBy - 排序方式 (cpu|memory)
 */
async function getProcessInfo(serverName, sortBy = 'cpu') {
  const sortOpt = sortBy === 'memory' ? '-%mem' : '-%cpu';
  
  const result = await execSSH(serverName, `
    echo "=== TOP 10 进程 (${sortBy === 'memory' ? '内存' : 'CPU'}) ===" &&
    ps aux --sort=${sortOpt} | head -11
  `);
  
  return {
    success: result.success,
    output: result.stdout
  };
}

/**
 * 获取系统负载
 * @param {string} serverName - 服务器名称
 */
async function getLoadAvg(serverName) {
  const result = await execSSH(serverName, `
    echo "=== 系统负载 ===" &&
    uptime &&
    echo "" &&
    echo "=== 负载详情 ===" &&
    cat /proc/loadavg
  `);
  
  return {
    success: result.success,
    output: result.stdout
  };
}

/**
 * 获取完整系统概览
 * @param {string} serverName - 服务器名称
 */
async function getSystemOverview(serverName) {
  const result = await execSSH(serverName, `
    echo "========== 系统信息 ==========" &&
    echo "主机名：$(hostname)" &&
    echo "系统：$(uname -s) $(uname -r)" &&
    echo "运行时间：$(uptime -p 2>/dev/null || uptime)" &&
    echo "" &&
    echo "========== CPU ==========" &&
    echo "核心数：$(nproc)" &&
    echo "负载：$(cat /proc/loadavg | awk '{print $1, $2, $3}')" &&
    echo "" &&
    echo "========== 内存 ==========" &&
    free -h | grep -E "Mem|Swap" &&
    echo "" &&
    echo "========== 磁盘 ==========" &&
    df -h / | tail -1 &&
    echo "" &&
    echo "========== 网络 ==========" &&
    echo "公网 IP: $(curl -s ifconfig.me 2>/dev/null || echo 'N/A')"
  `);
  
  return {
    success: result.success,
    output: result.stdout
  };
}

/**
 * 实时监控（单次快照）
 * @param {string} serverName - 服务器名称
 */
async function getRealtimeMonitor(serverName) {
  const result = await execSSH(serverName, `
    echo "=== 实时系统状态 ===" &&
    top -bn1 | head -20
  `);
  
  return {
    success: result.success,
    output: result.stdout
  };
}

/**
 * 获取 Docker 容器状态（如已安装）
 * @param {string} serverName - 服务器名称
 */
async function getDockerStatus(serverName) {
  const result = await execSSH(serverName, `
    echo "=== Docker 容器状态 ===" &&
    docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || echo "Docker 未安装或未运行"
  `);
  
  return {
    success: result.success,
    output: result.stdout
  };
}

/**
 * 获取系统告警信息
 * @param {string} serverName - 服务器名称
 * @param {Object} thresholds - 告警阈值
 */
async function getSystemAlerts(serverName, thresholds = {}) {
  const {
    cpuThreshold = 80,
    memoryThreshold = 80,
    diskThreshold = 90
  } = thresholds;
  
  const alerts = [];
  
  // 检查 CPU
  const cpuResult = await execSSH(serverName, `top -bn1 | grep "Cpu(s)" | awk '{print int($2 + $4)}'`);
  const cpuUsage = parseInt(cpuResult.stdout.trim()) || 0;
  if (cpuUsage > cpuThreshold) {
    alerts.push({ type: 'CPU', level: 'warning', message: `CPU 使用率 ${cpuUsage}% 超过阈值 ${cpuThreshold}%` });
  }
  
  // 检查内存
  const memResult = await execSSH(serverName, `free | grep Mem | awk '{printf "%.0f", $3/$2 * 100.0}'`);
  const memUsage = parseInt(memResult.stdout.trim()) || 0;
  if (memUsage > memoryThreshold) {
    alerts.push({ type: 'MEMORY', level: 'warning', message: `内存使用率 ${memUsage}% 超过阈值 ${memoryThreshold}%` });
  }
  
  // 检查磁盘
  const diskResult = await execSSH(serverName, `df / | tail -1 | awk '{print int($5)}'`);
  const diskUsage = parseInt(diskResult.stdout.trim()) || 0;
  if (diskUsage > diskThreshold) {
    alerts.push({ type: 'DISK', level: 'critical', message: `磁盘使用率 ${diskUsage}% 超过阈值 ${diskThreshold}%` });
  }
  
  return {
    serverName,
    timestamp: new Date().toISOString(),
    alerts,
    hasAlerts: alerts.length > 0
  };
}

module.exports = {
  getCPUInfo,
  getMemoryInfo,
  getDiskInfo,
  getNetworkInfo,
  getProcessInfo,
  getLoadAvg,
  getSystemOverview,
  getRealtimeMonitor,
  getDockerStatus,
  getSystemAlerts
};
