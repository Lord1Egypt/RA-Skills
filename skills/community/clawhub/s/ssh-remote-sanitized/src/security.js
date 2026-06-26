/**
 * SSH 安全检查与加固功能
 * 
 * 用法：
 * - 安全扫描
 * - 漏洞检查
 * - 安全加固建议
 * - 防火墙管理
 */

const { execSSH } = require('./index');

/**
 * 检查系统更新
 * @param {string} serverName - 服务器名称
 */
async function checkSystemUpdates(serverName) {
  const result = await execSSH(serverName, `
    echo "=== 检查系统更新 ===" &&
    if command -v apt &> /dev/null; then
      sudo apt update 2>&1 | tail -5
      sudo apt list --upgradable 2>/dev/null | grep -v "^Listing" | head -20
    elif command -v yum &> /dev/null; then
      sudo yum check-update 2>&1 | head -20
    elif command -v dnf &> /dev/null; then
      sudo dnf check-update 2>&1 | head -20
    else
      echo "未知的包管理器"
    fi
  `);
  
  return {
    success: result.success,
    output: result.stdout
  };
}

/**
 * 检查 SSH 安全配置
 * @param {string} serverName - 服务器名称
 */
async function checkSSHSecurity(serverName) {
  const result = await execSSH(serverName, `
    echo "=== SSH 配置检查 ===" &&
    echo "1. 检查 Root 登录:" &&
    grep -i "PermitRootLogin" /etc/ssh/sshd_config &&
    echo "" &&
    echo "2. 检查密码认证:" &&
    grep -i "PasswordAuthentication" /etc/ssh/sshd_config &&
    echo "" &&
    echo "3. 检查 SSH 端口:" &&
    grep -i "^Port" /etc/ssh/sshd_config &&
    echo "" &&
    echo "4. 检查允许的用户:" &&
    grep -i "AllowUsers" /etc/ssh/sshd_config || echo "未限制用户" &&
    echo "" &&
    echo "5. 检查失败的登录尝试:" &&
    sudo lastb | head -10
  `);
  
  return {
    success: result.success,
    output: result.stdout
  };
}

/**
 * 检查防火墙状态
 * @param {string} serverName - 服务器名称
 */
async function checkFirewall(serverName) {
  const result = await execSSH(serverName, `
    echo "=== 防火墙状态 ===" &&
    if command -v ufw &> /dev/null; then
      echo "--- UFW 状态 ---" &&
      sudo ufw status verbose
    elif command -v firewall-cmd &> /dev/null; then
      echo "--- Firewalld 状态 ---" &&
      sudo firewall-cmd --state &&
      sudo firewall-cmd --list-all
    elif command -v iptables &> /dev/null; then
      echo "--- iptables 规则 ---" &&
      sudo iptables -L -n | head -30
    else
      echo "未检测到防火墙工具"
    fi
  `);
  
  return {
    success: result.success,
    output: result.stdout
  };
}

/**
 * 检查开放端口
 * @param {string} serverName - 服务器名称
 */
async function checkOpenPorts(serverName) {
  const result = await execSSH(serverName, `
    echo "=== 开放端口 ===" &&
    netstat -tulpn 2>/dev/null || ss -tulpn
  `);
  
  return {
    success: result.success,
    output: result.stdout
  };
}

/**
 * 检查用户账户
 * @param {string} serverName - 服务器名称
 */
async function checkUserAccounts(serverName) {
  const result = await execSSH(serverName, `
    echo "=== 系统用户 ===" &&
    cat /etc/passwd | grep -v "nologin\|false" &&
    echo "" &&
    echo "=== 最近登录用户 ===" &&
    last | head -10 &&
    echo "" &&
    echo "=== 当前登录用户 ===" &&
    who
  `);
  
  return {
    success: result.success,
    output: result.stdout
  };
}

/**
 * 检查可疑进程
 * @param {string} serverName - 服务器名称
 */
async function checkSuspiciousProcesses(serverName) {
  const result = await execSSH(serverName, `
    echo "=== CPU 占用 TOP10 ===" &&
    ps aux --sort=-%cpu | head -11 &&
    echo "" &&
    echo "=== 内存占用 TOP10 ===" &&
    ps aux --sort=-%mem | head -11 &&
    echo "" &&
    echo "=== 异常进程检查 ===" &&
    ps aux | grep -v "grep" | grep -E "\[.*\]|/tmp/|/var/tmp/" | head -10 || echo "未发现明显异常进程"
  `);
  
  return {
    success: result.success,
    output: result.stdout
  };
}

/**
 * 检查磁盘使用
 * @param {string} serverName - 服务器名称
 */
async function checkDiskUsage(serverName) {
  const result = await execSSH(serverName, `
    echo "=== 磁盘使用率 ===" &&
    df -h &&
    echo "" &&
    echo "=== 大文件检查 (>/100MB) ===" &&
    sudo find / -type f -size +100M 2>/dev/null | head -20
  `);
  
  return {
    success: result.success,
    output: result.stdout
  };
}

/**
 * 生成安全报告
 * @param {string} serverName - 服务器名称
 */
async function generateSecurityReport(serverName) {
  const result = await execSSH(serverName, `
    echo "========================================" &&
    echo "     服务器安全检查报告" &&
    echo "========================================" &&
    echo "生成时间：$(date)" &&
    echo "主机名：$(hostname)" &&
    echo "系统：$(uname -a)" &&
    echo "" &&
    echo "【1. 系统更新状态】" &&
    if command -v apt &> /dev/null; then
      updates=$(apt list --upgradable 2>/dev/null | grep -v "^Listing" | wc -l)
      echo "可更新包数量：$updates"
    fi &&
    echo "" &&
    echo "【2. SSH 安全】" &&
    grep -i "PermitRootLogin" /etc/ssh/sshd_config &&
    echo "" &&
    echo "【3. 防火墙状态】" &&
    sudo ufw status 2>/dev/null || sudo firewall-cmd --state 2>/dev/null || echo "未知" &&
    echo "" &&
    echo "【4. 开放端口】" &&
    netstat -tulpn 2>/dev/null | grep LISTEN | wc -l &&
    echo "个监听端口" &&
    echo "" &&
    echo "【5. 最近失败登录】" &&
    sudo lastb 2>/dev/null | head -5 || echo "无记录" &&
    echo "" &&
    echo "【6. 磁盘使用】" &&
    df -h / | tail -1 &&
    echo "" &&
    echo "========================================"
  `);
  
  return {
    success: result.success,
    output: result.stdout
  };
}

/**
 * 安全加固建议
 * @param {string} serverName - 服务器名称
 */
async function getSecurityRecommendations(serverName) {
  const recommendations = [];
  
  // 检查 Root 登录
  const sshResult = await execSSH(serverName, 'grep -i "PermitRootLogin" /etc/ssh/sshd_config');
  if (sshResult.stdout.includes('yes')) {
    recommendations.push({
      level: 'high',
      item: 'SSH Root 登录',
      issue: '允许 Root 直接登录',
      suggestion: '设置 PermitRootLogin no'
    });
  }
  
  // 检查密码认证
  if (sshResult.stdout.includes('PasswordAuthentication yes')) {
    recommendations.push({
      level: 'medium',
      item: 'SSH 密码认证',
      issue: '启用密码认证',
      suggestion: '使用密钥认证，设置 PasswordAuthentication no'
    });
  }
  
  // 检查防火墙
  const fwResult = await execSSH(serverName, 'sudo ufw status 2>/dev/null || echo "inactive"');
  if (fwResult.stdout.includes('inactive') || fwResult.stdout.includes('inactive')) {
    recommendations.push({
      level: 'high',
      item: '防火墙',
      issue: '防火墙未启用',
      suggestion: '启用 UFW 或 Firewalld'
    });
  }
  
  // 检查系统更新
  const updateResult = await execSSH(serverName, 'apt list --upgradable 2>/dev/null | grep -v "^Listing" | wc -l');
  const updateCount = parseInt(updateResult.stdout.trim()) || 0;
  if (updateCount > 0) {
    recommendations.push({
      level: 'medium',
      item: '系统更新',
      issue: `有 ${updateCount} 个包可更新`,
      suggestion: '运行 sudo apt update && sudo apt upgrade'
    });
  }
  
  return {
    serverName,
    timestamp: new Date().toISOString(),
    recommendations,
    riskLevel: recommendations.filter(r => r.level === 'high').length > 0 ? 'high' : 'medium'
  };
}

/**
 * 快速安全加固
 * @param {string} serverName - 服务器名称
 * @param {Array} actions - 加固操作列表
 */
async function applySecurityHardening(serverName, actions = []) {
  const results = [];
  
  const hardeningActions = {
    'disable-root-login': async () => {
      return execSSH(serverName, 'sudo sed -i "s/PermitRootLogin yes/PermitRootLogin no/" /etc/ssh/sshd_config && sudo systemctl restart sshd');
    },
    'enable-firewall': async () => {
      return execSSH(serverName, 'sudo ufw --force enable');
    },
    'allow-ssh-only': async () => {
      return execSSH(serverName, 'sudo ufw allow ssh && sudo ufw allow 80/tcp && sudo ufw allow 443/tcp');
    },
    'fail2ban-install': async () => {
      return execSSH(serverName, 'sudo apt install -y fail2ban && sudo systemctl enable fail2ban && sudo systemctl start fail2ban');
    },
    'auto-updates': async () => {
      return execSSH(serverName, 'sudo apt install -y unattended-upgrades && sudo dpkg-reconfigure -plow unattended-upgrades');
    }
  };
  
  for (const action of actions) {
    if (hardeningActions[action]) {
      try {
        const result = await hardeningActions[action]();
        results.push({ action, success: result.success });
      } catch (error) {
        results.push({ action, success: false, error: error.message });
      }
    }
  }
  
  return results;
}

module.exports = {
  checkSystemUpdates,
  checkSSHSecurity,
  checkFirewall,
  checkOpenPorts,
  checkUserAccounts,
  checkSuspiciousProcesses,
  checkDiskUsage,
  generateSecurityReport,
  getSecurityRecommendations,
  applySecurityHardening
};
