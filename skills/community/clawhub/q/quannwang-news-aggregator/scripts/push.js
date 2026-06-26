/**
 * push.js — 飞书推送脚本
 * 将生成的每日简报推送到飞书指定会话
 */

const fs = require('fs');
const path = require('path');

// 加载配置
const configPath = path.join(__dirname, '..', 'config.json');
const config = fs.existsSync(configPath) ? JSON.parse(fs.readFileSync(configPath, 'utf-8')) : {};

const feishuConfig = config.feishu || {};
const chatId = feishuConfig.chat_id;
const receiveIdType = feishuConfig.receive_id_type || 'chat_id';

// 历史记录路径
const historyPath = path.join(__dirname, '..', 'data', 'history.json');

/**
 * 加载推送历史
 */
function loadHistory() {
  if (fs.existsSync(historyPath)) {
    return JSON.parse(fs.readFileSync(historyPath, 'utf-8'));
  }
  return { dates: [], titles: [] };
}

/**
 * 保存推送历史
 */
function saveHistory(history) {
  fs.mkdirSync(path.dirname(historyPath), { recursive: true });
  fs.writeFileSync(historyPath, JSON.stringify(history, null, 2));
}

/**
 * 检查是否已推送过相同日期的简报
 */
function isAlreadyPushed(dateStr) {
  const history = loadHistory();
  return history.dates.includes(dateStr);
}

/**
 * 记录推送历史
 */
function recordPush(dateStr, newsCount) {
  const history = loadHistory();
  history.dates.push(dateStr);
  // 保留最近 30 天记录
  if (history.dates.length > 30) {
    history.dates = history.dates.slice(-30);
  }
  saveHistory(history);
}

/**
 * 生成飞书富文本消息
 */
function buildFeishuPost(digestMd) {
  // 简报是 Markdown 格式，飞书 post 消息支持部分 Markdown
  // 这里将 Markdown 转为飞书富文本格式
  const lines = digestMd.split('\n');
  const content = [];
  let inList = false;

  for (const line of lines) {
    if (line.startsWith('# ')) {
      content.push([{ tag: 'h1', text: { content: line.replace('# ', ''), tag: 'text' } }]);
    } else if (line.startsWith('## ')) {
      content.push([{ tag: 'h2', text: { content: line.replace('## ', ''), tag: 'text' } }]);
    } else if (line.startsWith('---')) {
      content.push([{ tag: 'hr' }]);
    } else if (line.match(/^\d+\./)) {
      const match = line.match(/^(\d+)\.\s*\[([^\]]+)\]\(([^)]+)\)/);
      if (match) {
        content.push([{ tag: 'text', text: { content: `${match[1]}. `, tag: 'text' } },
                      { tag: 'a', text: { content: match[2], href: match[3] } }]);
      } else {
        content.push([{ tag: 'text', text: { content: line, tag: 'text' } }]);
      }
    } else if (line.startsWith('> ')) {
      content.push([{ tag: 'quote', text: { content: line.replace(/^>\s?/, ''), tag: 'text' } }]);
    } else if (line.trim() === '') {
      content.push([{ tag: 'text', text: { content: ' ', tag: 'text' } }]);
    } else {
      // 替换 **bold** 为加粗
      let processed = line.replace(/\*\*([^*]+)\*\*/g, (_, t) => t);
      content.push([{ tag: 'text', text: { content: processed, tag: 'text' } }]);
    }
  }

  return {
    msg_type: 'post',
    content: {
      zh_cn: {
        title: '📰 每日新闻简报',
        content: content
      }
    }
  };
}

async function main() {
  const digestPath = path.join(__dirname, '..', 'data', 'daily_digest.md');
  if (!fs.existsSync(digestPath)) {
    console.error('[push] 错误: data/daily_digest.md 不存在，请先运行 digest.js');
    return;
  }

  const digest = fs.readFileSync(digestPath, 'utf-8');
  const today = new Date().toISOString().slice(0, 10);

  if (isAlreadyPushed(today)) {
    console.log(`[push] 今日（${today}）已推送过，跳过`);
    return;
  }

  if (!chatId) {
    console.error('[push] 错误: config.json 中未配置 feishu.chat_id');
    console.error('[push] 请在 config.json 中添加: { "feishu": { "chat_id": "oc_xxx" } }');
    return;
  }

  console.log(`[push] 推送简报到飞书会话 ${chatId}...`);

  const payload = buildFeishuPost(digest);

  try {
    // 通过 OpenClaw 内置的飞书消息接口推送
    const response = await fetch(`https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=${receiveIdType}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.FEISHU_BOT_TOKEN || ''}`
      },
      body: JSON.stringify({
        receive_id: chatId,
        msg_type: 'text',
        content: JSON.stringify({ text: digest.slice(0, 4000) }) // 飞书 text 消息最多 4000 字
      })
    });

    const result = await response.json();
    if (result.code !== 0 && result.msg !== 'success') {
      // 如果没有 bot token，输出为兼容性发送（主 agent 接收）
      console.log('[push] 简报内容（请通过飞书机器人手动发送或配置 FEISHU_BOT_TOKEN）:');
      console.log(digest.slice(0, 500));
    } else {
      console.log(`[push] 推送成功: ${result.code}`);
    }
  } catch (err) {
    console.error('[push] 推送失败:', err.message);
    console.log('[push] 简报已保存到 data/daily_digest.md，可手动发送');
  }

  recordPush(today, 0);
}

module.exports = { main };

if (require.main === module) {
  main().catch(console.error);
}
