// notify.mjs — 通知通道：终端/日志、Webhook（通用/Server酱/企业微信/钉钉）、Windows 桌面弹窗
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';

function ts() {
  return new Date().toISOString().replace('T', ' ').slice(0, 19);
}

function ensureDir(file) {
  try {
    if (file) fs.mkdirSync(path.dirname(file), { recursive: true });
  } catch {
    /* 忽略 */
  }
}

export function terminal(message) {
  console.log(`[${ts()}] ${message}`);
}

export function logToFile(message, logFile) {
  try {
    ensureDir(logFile);
    fs.appendFileSync(logFile, `[${ts()}] ${message}\n`, 'utf8');
  } catch {
    /* 日志失败不阻断监控 */
  }
}

// PowerShell 单引号字符串转义：去换行、单引号翻倍
function psEscape(s) {
  return String(s).replace(/\r?\n/g, ' ').replace(/'/g, "''");
}

// Windows 托盘气泡弹窗（依赖系统自带 .NET，无需额外安装）
export function sendToast(title, message) {
  const t = psEscape(title);
  const m = psEscape(message);
  const ps = `
Add-Type -AssemblyName System.Windows.Forms
$n = New-Object System.Windows.Forms.NotifyIcon
$n.Icon = [System.Drawing.SystemIcons]::Information
$n.BalloonTipTitle = '${t}'
$n.BalloonTipText = '${m}'
$n.Visible = $true
$n.ShowBalloonTip(8000)
Start-Sleep -Seconds 9
$n.Dispose()
`;
  try {
    const b64 = Buffer.from(ps, 'utf16le').toString('base64');
    const child = spawn(
      'powershell.exe',
      ['-NoProfile', '-WindowStyle', 'Hidden', '-EncodedCommand', b64],
      { detached: true, stdio: 'ignore' }
    );
    child.unref();
  } catch {
    /* 弹窗失败忽略 */
  }
}

export async function sendWebhooks(title, message, webhooks) {
  if (!Array.isArray(webhooks)) return;
  for (const wh of webhooks) {
    if (!wh) continue;
    try {
      if (wh.type === 'serverchan') {
        await fetch(`https://sctapi.ftqq.com/${wh.key}.send`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: new URLSearchParams({ title, desp: message }).toString(),
        });
      } else if (wh.type === 'wecom') {
        await fetch(`https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=${wh.key}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ msgtype: 'text', text: { content: `${title}\n${message}` } }),
        });
      } else if (wh.type === 'dingtalk') {
        await fetch(`https://oapi.dingtalk.com/robot/send?access_token=${wh.key}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ msgtype: 'text', text: { content: `${title}\n${message}` } }),
        });
      } else if (wh.type === 'generic' && wh.url) {
        await fetch(wh.url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ title, message, text: `${title}\n${message}` }),
        });
      }
    } catch (e) {
      terminal(`[webhook ${wh.type}] 发送失败: ${e.message}`);
    }
  }
}

// 统一分发：终端 + 日志（始终），弹窗/Webhook（按配置）
export async function dispatch(title, message, cfg) {
  const c = cfg || {};
  terminal(`${title} :: ${message}`);
  if (c.log !== false) logToFile(`${title} :: ${message}`, c.logFile);
  if (c.toast) sendToast(title, message);
  if (c.webhooks && c.webhooks.length) await sendWebhooks(title, message, c.webhooks);
}
