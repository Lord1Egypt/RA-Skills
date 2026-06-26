// Gateway 重启确认钩子（JavaScript 版本）
const fs = require('fs');
const path = require('path');

const BACKUP_DIR = path.join(__dirname, '..', '..', 'backups');

const gatewayRestartConfirmed = async (event) => {
  // 只处理 Gateway 重启命令
  if (event.type !== 'command' || event.command !== 'gateway:restart') {
    return;
  }

  console.log('[gateway-restart-confirmed] Gateway restart command detected');

  // 检查是否有 --confirmed 参数
  const hasConfirmed = event.args?.includes('--confirmed') || 
                       event.args?.includes('-c') ||
                       process.argv?.includes('--confirmed') ||
                       process.argv?.includes('-c');

  if (!hasConfirmed) {
    // 没有确认参数，提示用户
    const message = `
⚠️ **Gateway 重启保护机制已激活**

检测到 Gateway 重启请求，但未提供确认参数。

## 📋 请先检查保护报告

保护钩子已自动保存配置并生成报告，请查看：
1. 飞书消息中的保护报告
2. 或查看备份目录：\`${BACKUP_DIR}\`

## ✅ 确认安全后重启

确认配置已备份且可以安全重启后，执行：
\`\`\`bash
openclaw gateway restart --confirmed
\`\`\`

## 🚫 禁止擅自重启

**请勿直接重启 Gateway**，这可能导致配置丢失！
`.trim();

    if (event.messages) {
      event.messages.push(message);
    }

    // 阻止重启
    event.preventDefault?.();
    event.blocked = true;

    console.log('[gateway-restart-confirmed] Restart blocked, waiting for --confirmed flag');
    return;
  }

  // 有确认参数，允许重启
  console.log('[gateway-restart-confirmed] --confirmed flag detected, allowing restart');

  // 检查最近的备份报告
  const latestReport = getLatestBackupReport();
  
  if (latestReport) {
    const successMessage = `
✅ **Gateway 重启确认**

检测到 --confirmed 参数，允许执行重启。

## 📋 最近的备份报告

**时间：** ${latestReport.timestamp}
**文件：** ${latestReport.path}

## 🔄 正在重启 Gateway...

请稍候，Gateway 正在重启中...
`.trim();

    if (event.messages) {
      event.messages.push(successMessage);
    }

    console.log('[gateway-restart-confirmed] Allowing restart to proceed');
  } else {
    const warningMessage = `
⚠️ **未找到备份报告**

虽然有 --confirmed 参数，但未找到最近的备份报告。

## 建议

建议先执行一次正常重启（不带 --confirmed），让保护钩子生成备份报告，
确认安全后再使用 --confirmed 参数重启。

## 继续重启？

如果确认不需要备份，可以直接继续重启。
`.trim();

    if (event.messages) {
      event.messages.push(warningMessage);
    }

    console.log('[gateway-restart-confirmed] No backup report found, but allowing restart due to --confirmed flag');
  }

  // 不阻止重启，允许继续
  // event.preventDefault() 不被调用
};

// 获取最新的备份报告
function getLatestBackupReport() {
  if (!fs.existsSync(BACKUP_DIR)) {
    return null;
  }

  const files = fs.readdirSync(BACKUP_DIR)
    .filter(f => f.startsWith('restart-report-') && f.endsWith('.md'))
    .map(f => ({
      name: f,
      path: path.join(BACKUP_DIR, f),
      time: fs.statSync(path.join(BACKUP_DIR, f)).mtimeMs
    }))
    .sort((a, b) => b.time - a.time);

  if (files.length === 0) {
    return null;
  }

  const latest = files[0];
  const timestamp = latest.name
    .replace('restart-report-', '')
    .replace('.md', '')
    .replace(/-/g, ':')
    .replace(/(\d{4}:\d{2}:\d{2}):(\d{2}):(\d{2}):(\d{2})/, '$1 $2:$3:$4');

  return {
    timestamp,
    path: latest.path
  };
}

module.exports = gatewayRestartConfirmed;
