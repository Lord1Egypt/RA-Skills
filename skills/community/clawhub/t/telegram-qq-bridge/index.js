/**
 * Telegram → QQ 自动转发插件
 * 
 * 监听 Telegram 消息，自动转发到 QQ
 * 作为 OpenClaw 插件运行，随 OpenClaw 自动启动
 * 
 * @author OpenClaw Community
 * @license MIT
 * @version 1.0.0
 */

const fs = require('fs');
const path = require('path');

// 配置（从环境变量或配置文件中读取）
const CONFIG = {
  sessionFile: process.env.TELEGRAM_QQ_SESSION_FILE || 
    path.join(
      process.env.HOME || process.env.USERPROFILE || '/home/raolin',
      '.openclaw/agents/stockworker/sessions/bb586ba3-6b35-4def-87e9-94c0dbf6d216.jsonl'
    ),
  qqTarget: process.env.QQ_TARGET || 'qqbot:c2c:YOUR_OPENID_HERE',
  qqAccount: process.env.QQ_ACCOUNT || 'youyanli',
  pollInterval: parseInt(process.env.POLL_INTERVAL) || 2000,
};

// 状态
let lastSize = 0;
const processedMessages = new Set();

/**
 * 获取最新的 Telegram 消息
 */
function getTelegramMessages() {
  try {
    if (!fs.existsSync(CONFIG.sessionFile)) {
      return [];
    }

    const content = fs.readFileSync(CONFIG.sessionFile, 'utf-8');
    const lines = content.split('\n').slice(-10); // 只读最后 10 行
    const messages = [];

    for (const line of lines) {
      if (!line.trim()) continue;

      try {
        const obj = JSON.parse(line);
        const msg = obj.message || {};
        const role = msg.role || '';

        // 只处理用户消息
        if (role === 'user') {
          let content = msg.content || '';
          
          // 处理列表格式
          if (Array.isArray(content)) {
            for (const item of content) {
              if (item.type === 'text' && item.text) {
                if (item.text.includes('@ollama_openclaw_at_dzt_bot')) {
                  messages.push(item.text);
                }
              }
            }
          } else if (typeof content === 'string' && content.includes('@ollama_openclaw_at_dzt_bot')) {
            messages.push(content);
          }
        }
      } catch (e) {
        // 跳过无效行
      }
    }

    return messages;
  } catch (error) {
    console.error('[telegram-qq-bridge] 读取失败:', error.message);
    return [];
  }
}

/**
 * 转发消息到 QQ
 */
function forwardToQQ(text) {
  // 清理消息
  const cleanText = text.replace('@ollama_openclaw_at_dzt_bot', '').trim();
  if (!cleanText) return;

  // 检查是否已处理
  if (processedMessages.has(cleanText)) {
    return;
  }

  processedMessages.add(cleanText);
  // 限制历史记录大小
  if (processedMessages.size > 100) {
    processedMessages.clear();
  }

  console.log(`[telegram-qq-bridge] 转发到 QQ: ${cleanText.substring(0, 100)}`);

  // 调用 openclaw message send
  const cmd = `openclaw message send --channel qqbot --account ${CONFIG.qqAccount} --target "${CONFIG.qqTarget}" --message "[Telegram] ${cleanText}"`;
  
  try {
    const result = require('child_process').execSync(cmd, { encoding: 'utf-8', timeout: 30000 });
    if (result.includes('Sent via QQ Bot')) {
      console.log('[telegram-qq-bridge] ✅ 转发成功');
    } else {
      console.error('[telegram-qq-bridge] ❌ 转发失败:', result);
    }
  } catch (error) {
    console.error('[telegram-qq-bridge] ❌ 转发异常:', error.message);
  }
}

/**
 * 主循环
 */
function main() {
  console.log('[telegram-qq-bridge] 🚀 启动 Telegram → QQ 自动转发');
  console.log('[telegram-qq-bridge] 监听文件:', CONFIG.sessionFile);
  console.log('[telegram-qq-bridge] 转发目标:', CONFIG.qqTarget);
  console.log('[telegram-qq-bridge] 转发账号:', CONFIG.qqAccount);
  console.log('[telegram-qq-bridge] 轮询间隔:', CONFIG.pollInterval, 'ms');

  setInterval(() => {
    try {
      const messages = getTelegramMessages();
      if (messages.length > 0) {
        for (const msg of messages) {
          forwardToQQ(msg);
        }
      }
    } catch (error) {
      console.error('[telegram-qq-bridge] 处理失败:', error.message);
    }
  }, CONFIG.pollInterval);
}

// 启动
main();

// 导出插件信息
module.exports = {
  id: 'telegram-qq-bridge',
  name: 'Telegram → QQ 自动转发',
  version: '1.0.0',
  description: '监听 Telegram 消息并自动转发到 QQ',
  config: {
    qqTarget: 'QQ 目标地址 (qqbot:c2c:OPENID)',
    qqAccount: 'QQ 账号名',
    pollInterval: '轮询间隔 (毫秒)',
  }
};
