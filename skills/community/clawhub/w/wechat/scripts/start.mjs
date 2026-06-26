#!/usr/bin/env node
/**
 * start.mjs - 微信插件安装 Skill 主入口
 * 
 * 全流程：获取 QR → 启动 HTTP 服务 → 生成引导页 → 轮询状态 → 保存账号
 */

import { spawn, execSync } from 'node:child_process';
import { writeFileSync, readFileSync, existsSync, mkdirSync } from 'node:fs';
import { createRequire } from 'node:module';
import http from 'node:http';
import path from 'node:path';
import os from 'node:os';
import url from 'node:url';

const require = createRequire(import.meta.url);
const QRCode = require('qrcode');

const __dirname = path.dirname(url.fileURLToPath(import.meta.url));
const ROOT = path.dirname(__dirname);

// ─── 配置 ───────────────────────────────────────────────
const SKILL_DIR = path.dirname(__dirname);          // .../wechat-connect

const API_BASE = 'https://ilinkai.weixin.qq.com';
const BOT_TYPE = '3';
const QR_PNG_PATH = '/tmp/weixin-login-qr.png';
const STATUS_FILE = '/tmp/weixin-login-status.json';
const HTML_PATH = '/tmp/weixin-qr-display.html';
const HTTP_PORT = 8765;
const BASE_DIR = '/tmp';



// ─── 工具函数 ───────────────────────────────────────────
function log(msg) { console.log(`[weixin-install] ${msg}`); }
function error(msg) { console.error(`[weixin-install] ❌ ${msg}`); }

async function fetchJSON(url, headers = {}) {
  const resp = await fetch(url, { headers });
  return resp.json();
}

function writeStatus(data) {
  writeFileSync(STATUS_FILE, JSON.stringify(data, null, 2));
}

function readStatus() {
  try {
    return JSON.parse(readFileSync(STATUS_FILE, 'utf-8'));
  } catch {
    return { status: 'wait', message: '等待获取二维码...' };
  }
}

// ─── 1. 检查插件安装状态 ────────────────────────────────
function checkPluginInstalled() {
  try {
    const out = execSync('openclaw config get plugins.installs 2>/dev/null', { encoding: 'utf-8' });
    return out.includes('openclaw-weixin');
  } catch {
    return false;
  }
}

// ─── 2. 获取二维码 ─────────────────────────────────────
async function fetchQRCode() {
  log('正在获取微信登录二维码...');
  
  const data = await fetchJSON(
    `${API_BASE}/ilink/bot/get_bot_qrcode?bot_type=${BOT_TYPE}`,
    { 'iLink-App-ClientVersion': '1' }
  );

  if (data.ret !== 0 || !data.qrcode_img_content) {
    throw new Error(`API 错误: ${JSON.stringify(data)}`);
  }

  // 生成 PNG
  const png = await QRCode.toBuffer(data.qrcode_img_content, {
    type: 'png', width: 400, margin: 2,
    color: { dark: '#000000', light: '#ffffff' }
  });
  writeFileSync(QR_PNG_PATH, png);

  log(`二维码已生成: ${QR_PNG_PATH}`);
  log(`qrcode: ${data.qrcode}`);

  writeStatus({
    qrcode: data.qrcode,
    status: 'wait',
    message: '请使用微信扫描二维码'
  });

  return data.qrcode;
}


// ─── 4. 生成引导页 HTML ────────────────────────────────
function generateHTML() {

  const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>微信插件安装</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: #f5f5f5;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    padding: 40px;
  }
  h2 {
    color: #333;
    margin-bottom: 36px;
    font-size: 24px;
  }
  .steps-row { display: flex; align-items: center; }
  .step {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    width: 200px;
  }
  .step-content {
    background: #fff;
    border-radius: 10px;
    padding: 16px 14px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.10);
    font-size: 14px;
    color: #333;
    line-height: 1.7;
    text-align: left;
    min-height: 100px;
  }
  .step .label {
    font-size: 15px;
    color: #444;
    font-weight: 600;
  }
  .arrow {
    font-size: 22px;
    color: #aaa;
    margin: 0 10px;
    padding-top: 20px;
    vertical-align: top;
  }
  .qr-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    margin-left: 20px;
  }
  .qr-section img {
    height: 160px;
    border-radius: 10px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.12);
  }

  #status-msg {
    margin-top: 24px;
    font-size: 17px;
    color: #555;
    height: 24px;
  }
  #status-msg.wait { color: #888; }
  #status-msg.scaned { color: #e67e22; }
  #status-msg.confirmed { color: #27ae60; }
  #status-msg.error { color: #e74c3c; }

  /* 灯箱 */
  #lightbox {
    display: none;
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.65);
    z-index: 9999;
    align-items: center;
    justify-content: center;
  }
  #lightbox.show { display: flex; }
  .lightbox-content {
    background: #fff;
    border-radius: 16px;
    padding: 40px 50px;
    text-align: center;
    max-width: 480px;
    box-shadow: 0 8px 40px rgba(0,0,0,0.3);
    animation: popIn 0.4s ease;
  }
  @keyframes popIn {
    from { transform: scale(0.7); opacity: 0; }
    to { transform: scale(1); opacity: 1; }
  }
  .lightbox-icon { font-size: 56px; margin-bottom: 16px; }
  .lightbox-title {
    font-size: 22px;
    font-weight: 600;
    color: #27ae60;
    margin-bottom: 10px;
  }
  .lightbox-desc { font-size: 15px; color: #666; line-height: 1.6; }
</style>
</head>
<body>

<h2>微信插件安装指引</h2>

<div class="steps-row">
  <div class="step">
    <div class="step-content">将微信的版本更新到V8.0.70或以上版本，然后重启APP。</div>
    <span class="label">第一步</span>
  </div>
  <span class="arrow">→</span>

  <div class="step">
    <div class="step-content">进入微信的"我 - 设置 - 插件"界面。</div>
    <span class="label">第二步</span>
  </div>
  <span class="arrow">→</span>

  <div class="step">
    <div class="step-content">打开插件界面中的"微信 ClawBot"的详情按钮。</div>
    <span class="label">第三步</span>
  </div>
  <span class="arrow">→</span>

  <div class="step">
    <div class="step-content">在微信ClawBot详情界面中，点击"开始扫一扫"链接，扫描本页面的二维码。</div>
    <span class="label">第四步</span>
  </div>
  <span class="arrow">→</span>

  <div class="step qr-section">
    <img id="qrcode" src="weixin-login-qr.png?${Date.now()}" alt="第五步">
    <span class="label">第五步</span>
  </div>
</div>

<div id="status-msg" class="wait">等待获取二维码...</div>

<!-- 成功灯箱 -->
<div id="lightbox">
  <div class="lightbox-content">
    <div class="lightbox-icon">🎉</div>
    <div class="lightbox-title">恭喜！微信与 OpenClaw 已经配对成功</div>
    <div class="lightbox-desc">你可以开始使用了</div>
  </div>
</div>

<script>
const STATUS_URL = 'http://localhost:${HTTP_PORT}/status';

function showLightbox() {
  document.getElementById('lightbox').classList.add('show');
}

function poll() {
  fetch(STATUS_URL)
    .then(r => r.json())
    .then(data => {
      const msg = document.getElementById('status-msg');
      msg.textContent = data.message || '';
      msg.className = data.status || 'wait';

      if (data.connected || data.status === 'confirmed') {
        showLightbox();
        return;
      }
      if (data.error) {
        msg.textContent = data.message || '二维码已过期，请重新生成';
        return;
      }
      setTimeout(poll, 2000);
    })
    .catch(() => setTimeout(poll, 2000));
}

poll();
</script>

</body>
</html>`;

  writeFileSync(HTML_PATH, html);
  log(`HTML 页面已生成: ${HTML_PATH}`);
}

// ─── 4. 启动 HTTP 服务 ──────────────────────────────
function startHttpServer() {
  const server = http.createServer((req, res) => {
    const parsed = url.parse(req.url, true);
    const pathname = parsed.pathname;

    if (pathname === '/status') {
      // 状态 API（供页面 JS 轮询）
      res.writeHead(200, {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      });
      res.end(JSON.stringify(readStatus()));
    } else if (pathname === '/qrcode') {
      // 动态 QR 图片
      try {
        const png = readFileSync(QR_PNG_PATH);
        res.writeHead(200, { 'Content-Type': 'image/png', 'Cache-Control': 'no-cache' });
        res.end(png);
      } catch {
        res.writeHead(404);
        res.end('not found');
      }
    } else {
      // 静态文件（HTML + PNG + 步骤图）
      let filePath = path.join(BASE_DIR, pathname === '/' ? 'weixin-qr-display.html' : pathname);
      // 安全：禁止访问 /tmp 以外的文件
      if (!filePath.startsWith(BASE_DIR)) {
        res.writeHead(403);
        res.end('forbidden');
        return;
      }
      try {
        const ext = path.extname(filePath);
        const contentTypes = {
          '.html': 'text/html',
          '.png': 'image/png',
          '.jpg': 'image/jpeg',
          '.jpeg': 'image/jpeg',
          '.gif': 'image/gif',
          '.svg': 'image/svg+xml',
        };
        const ct = contentTypes[ext] || 'text/plain';
        const data = readFileSync(filePath);
        res.writeHead(200, { 'Content-Type': ct });
        res.end(data);
      } catch {
        res.writeHead(404);
        res.end('not found');
      }
    }
  });

  return new Promise(resolve => {
    server.listen(HTTP_PORT, () => {
      log(`HTTP 服务已启动: http://localhost:${HTTP_PORT}`);
      resolve(server);
    });
  });
}

// ─── 5. 轮询微信登录状态 ───────────────────────────────
async function pollWeixinStatus(qrcode, server) {
  const checkUrl = `${API_BASE}/ilink/bot/get_qrcode_status?qrcode=${qrcode}`;

  while (true) {
    await new Promise(r => setTimeout(r, 3000));

    const current = readStatus();
    if (current.connected || current.error) break;

    try {
      const data = await fetchJSON(checkUrl, { 'iLink-App-ClientVersion': '1' });

      if (data.status !== current.status) {
        const updated = { ...current, status: data.status };

        switch (data.status) {
          case 'scaned':
            updated.message = '已扫码，请在微信中确认登录';
            log('👀 已扫码，等待确认...');
            break;
          case 'confirmed':
            updated.message = '登录成功！';
            updated.connected = true;
            updated.botToken = data.bot_token;
            updated.ilinkBotId = data.ilink_bot_id;
            updated.ilinkUserId = data.ilink_user_id;
            updated.baseUrl = data.baseurl;
            log('✅ 登录成功！');
            log(`   ilink_bot_id: ${data.ilink_bot_id}`);
            log(`   ilink_user_id: ${data.ilink_user_id}`);
            break;
          case 'expired':
            updated.message = '二维码已过期，请重新生成';
            updated.error = true;
            log('❌ 二维码已过期');
            break;
        }

        writeStatus(updated);
      }
    } catch (err) {
      log(`轮询错误: ${err.message}`);
    }
  }

  // 不关闭 server，灯箱页面保持访问
  return readStatus();
}

// ─── 6. 保存账号 ───────────────────────────────────────
async function saveAccount(data) {
  if (!data.connected || !data.ilinkBotId || !data.botToken) {
    throw new Error('登录未成功，无法保存账号');
  }

  const homeDir = os.homedir();
  const stateDir = path.join(homeDir, '.openclaw', 'openclaw-weixin');
  const accountsDir = path.join(stateDir, 'accounts');

  // 规范化账号 ID
  const botId = data.ilinkBotId; // e.g. "b58206a34d4a@im.bot"
  const accountId = botId.replace('@im.bot', '-im-bot'); // "b58206a34d4a-im-bot"

  mkdirSync(accountsDir, { recursive: true });

  // 保存账号文件
  const accountFile = path.join(accountsDir, `${accountId}.json`);
  const accountData = {
    token: data.botToken,
    savedAt: new Date().toISOString(),
    baseUrl: data.baseUrl || API_BASE,
    userId: data.ilinkUserId
  };
  writeFileSync(accountFile, JSON.stringify(accountData, null, 2));
  log(`账号已保存: ${accountFile}`);

  // 更新索引
  const indexFile = path.join(stateDir, 'accounts.json');
  let accounts = [];
  try {
    accounts = JSON.parse(readFileSync(indexFile, 'utf-8'));
  } catch {}
  if (!accounts.includes(accountId)) {
    accounts.push(accountId);
    writeFileSync(indexFile, JSON.stringify(accounts, null, 2));
  }

  // 更新 OpenClaw 配置
  const userId = data.ilinkUserId;

  const commands = [
    `openclaw config set channels.openclaw-weixin.enabled true`,
    `openclaw config set channels.openclaw-weixin.dmPolicy allowlist`,
    `openclaw config set channels.openclaw-weixin.allowFrom '["${userId}"]'`
  ];
  let successCount = 0;
  for (const cmd of commands) {
    try {
      execSync(cmd, { stdio: 'ignore' });
      successCount++;
    } catch (e) {
      log(`配置更新遇到警告 (执行 ${cmd}): ${e.message}`);
    }
  }
  log(`OpenClaw 配置已更新 (${successCount}/3)`);

  // 后台重启 Gateway（不清除本进程，灯箱页面继续展示）
  log('正在后台重启 Gateway...');
  spawn('openclaw', ['gateway', 'restart'], {
    stdio: 'ignore',
    detached: true,
    shell: true
  }).unref();

  return { accountId, accountFile };
}

// ─── 主流程 ───────────────────────────────────────────
async function main() {
  log('========== 微信插件安装流程开始 ==========');

  // 检查插件
  if (!checkPluginInstalled()) {
    log('⚠️  插件尚未安装，正在自动执行安装命令...');
    log('   $ npx -y @tencent-weixin/openclaw-weixin-cli@latest install');
    try {
      execSync('npx -y @tencent-weixin/openclaw-weixin-cli@latest install', { stdio: 'inherit' });
      log('✅ 插件安装成功！继续配对流程...');
    } catch (e) {
      error('自动安装插件失败，请手动在终端执行: npx -y @tencent-weixin/openclaw-weixin-cli@latest install');
      return;
    }
  }

  // 获取 QR
  const qrcode = await fetchQRCode();

  generateHTML();

  // 启动 HTTP 服务（同时处理静态文件和状态 API）
  const server = await startHttpServer();

  log('请用浏览器打开: http://localhost:8765');
  log('页面将自动更新扫码状态...');
  log('');

  // 轮询状态直到完成
  const result = await pollWeixinStatus(qrcode, server);

  if (result.connected) {
    await saveAccount(result);
    log('');
    log('========== 安装完成！Gateway 正在后台重启 ==========');
  } else {
    log('');
    log('========== 安装未完成，请重新运行本脚本 ==========');
  }
}

main().catch(err => {
  error(`脚本执行失败: ${err.message}`);
  process.exit(1);
});
