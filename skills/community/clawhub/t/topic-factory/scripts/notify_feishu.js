#!/usr/bin/env node
/**
 * notify_feishu.js - 选题飞书推送脚本（每天 09:00 跑）
 *
 * 功能：
 *   1. 读取 ${TOPICS_DIR}/claude-hub/topics/YYYYMMDD_topics.md（当天选题文件）
 *   2. 提取标记为 ⭐推送 的前 10 个选题
 *   3. 解析每个选题的：钩子文案 + 3个数据点 + 关键词命中
 *   4. 通过飞书 webhook 发送飞书消息（text 格式）
 *   5. 失败只 console.error，不阻塞、不抛异常
 *
 * 飞书 webhook：https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK_TOKEN
 *
 * 依赖：Node.js >= 18（原生 fetch）
 *
 * 作者：Claude
 * 日期：2026-08-14
 */

'use strict';

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

// ============================================================
// 1. 路径和配置（写死在代码里）
// ============================================================

// 飞书 webhook 地址（飞书官方机器人 webhook）
const FEISHU_WEBHOOK = 'https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK_TOKEN';

// topics/ 目录
const TOPICS_DIR = path.join(
  process.env.HOME || require('os').homedir(),
  '.openclaw/workspace/claude-hub/topics'
);

// ============================================================
// 2. 辅助函数
// ============================================================

/**
 * 获取今天日期字符串（YYYYMMDD），北京时间
 */
function getTodayStr() {
  const now = new Date();
  // 使用 Asia/Shanghai 时区获取 YYYYMMDD
  const shanghaiTime = now.toLocaleString('en-CA', {
    timeZone: 'Asia/Shanghai',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  });
  // shanghaiTime 格式: YYYY-MM-DD
  return shanghaiTime.replace(/-/g, '');
}

/**
 * 解析选题块，提取关键字段
 *
 * 字段提取顺序（按在块内出现的先后）：
 *   1. 原始命中（从 "**原始命中**：" 行）
 *   2. 钩子文案（从 "**钩子文案" 行开始，到下一个 ** 开头段落）
 *   3. 3个数据点（从 "**3 个数据点" 开始，到 "**来源链接" 之前）
 *
 * @param {string} body - 选题块 body 部分（不含 "## 选题 N · ⭐推送" 标题行）
 * @returns {{rawHit: string, hooks: string[], dataPoints: string[]}}
 */
function extractFields(body) {
  // 跳过可能存在的开头的空行（如标题行后紧跟的空行）
  const allLines = body.split('\n');
  const lines = allLines; // 保留所有行，包括空行
  const result = {
    rawHit: '',
    hooks: [],
    dataPoints: []
  };

  let currentSection = null; // 'hooks' | 'datapoints'
  const hookLines = [];
  const dataPointLines = [];
  let dataPointCount = 0;

  for (const rawLine of lines) {
    // 去掉首尾空白（保留内部缩进）
    const trimmed = rawLine.trim();
    if (!trimmed) continue; // 跳过空行

    // 原始命中：`- **原始命中**：D AI科技(命中词：人工智能)`
    if (trimmed.startsWith('**原始命中**') || trimmed.startsWith('- **原始命中**')) {
      // 从冒号后面提取，兼容 `- ` 前缀或直接在 ** 内
      const colonIdx = trimmed.lastIndexOf('：');
      result.rawHit = colonIdx !== -1 ? trimmed.slice(colonIdx + 1).trim() : '';
      continue;
    }

    // 钩子文案 section
    if (trimmed.startsWith('**钩子文案') || trimmed.startsWith('- **钩子文案')) {
      currentSection = 'hooks';
      continue;
    }

    // 3个数据点 section
    if (trimmed.startsWith('**3 个数据点') || trimmed.startsWith('**3个数据点') ||
        trimmed.startsWith('- **3 个数据点') || trimmed.startsWith('- **3个数据点')) {
      currentSection = 'datapoints';
      continue;
    }

    // 来源链接 section 结束
    if (trimmed.startsWith('**来源链接**') || trimmed.startsWith('- **来源链接**') ||
        trimmed.startsWith('**来源**')) {
      currentSection = null;
      continue;
    }

    // 用户操作 section 结束
    if (trimmed.startsWith('**用户操作**') || trimmed.startsWith('- **用户操作**')) {
      currentSection = null;
      continue;
    }

    // 收集钩子文案（无序列表 - 开头为 "- " 或 "  - "）
    // 钩子可能含数字序号（如 "公众号候选1"），不过滤内容，只过滤空行
    if (currentSection === 'hooks' && (trimmed.startsWith('- ') || trimmed.startsWith('  - '))) {
      const hookText = trimmed.replace(/^-\s*/, '').replace(/^-\s*/, '').trim();
      if (hookText && hookText.length > 5) {
        hookLines.push(hookText);
      }
    }

    // 收集数据点（数字序号开头的行，如 "1. xxx"）
    if (currentSection === 'datapoints' && /^\d+\.\s/.test(trimmed)) {
      const dp = trimmed.replace(/^\d+\.\s*/, '').trim();
      if (dp) {
        dataPointCount++;
        dataPointLines.push(`${dataPointCount}. ${dp}`);
      }
    }
  }

  result.hooks = hookLines.slice(0, 3); // 最多3个钩子
  result.dataPoints = dataPointLines.slice(0, 3); // 正好3个

  return result;
}

/**
 * 解析今天的选题文件，提取所有 ⭐推送 选题
 *
 * 用 "\n---\n" 分割内容为各个 section，取第一个 section 的第一行
 * 作为选题标题，剩余内容作为 body 供 extractFields 解析。
 *
 * @param {string} content
 * @returns {Array<{num: number, title: string, fields: ReturnType<extractFields>}>}
 */
function parseStarredTopics(content) {
  const sections = content.split(/\n---\n/);
  const topics = [];

  for (const section of sections) {
    const trimmed = section.trim();
    if (!trimmed) continue;

    // 解析 "## 选题 N · ⭐推送" 标题行
    const titleMatch = trimmed.match(/^\s*## 选题 (\d+) · ⭐推送/);
    if (!titleMatch) continue;
    const num = parseInt(titleMatch[1], 10);

    // 去掉第一行（标题行），保留后续所有内容作为 body
    const bodyLines = trimmed.split('\n');
    const body = bodyLines.slice(1).join('\n');

    // 提取热榜标题（body 第一行粗体 **...**）
    const hotTitleMatch = body.match(/^\*\*(.+?)\*\*/);
    const title = hotTitleMatch ? hotTitleMatch[1] : `选题 ${num}`;

    const fields = extractFields(body);
    topics.push({ num, title, fields });
  }

  return topics;
}

/**
 * 发送文本消息到飞书 webhook
 *
 * 使用原生 https 模块，不依赖任何外部库
 * 与 send_report.py 保持一致：用 JSON.stringify + Content-Type: application/json
 *
 * @param {string} text - 纯文本内容
 * @returns {Promise<{code: number, msg: string}>}
 */
function sendFeishuText(text) {
  return new Promise((resolve) => {
    const payload = JSON.stringify({
      msg_type: 'text',
      content: { text }
    });

    const url = new URL(FEISHU_WEBHOOK);
    const options = {
      hostname: url.hostname,
      path: url.pathname,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload)
      },
      timeout: 30000 // 30秒超时
    };

    const transport = FEISHU_WEBHOOK.startsWith('https') ? https : http;
    const req = transport.request(options, (res) => {
      let data = '';
      res.on('data', chunk => { data += chunk; });
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data.toString());
          resolve(parsed);
        } catch {
          resolve({ code: -1, msg: `响应解析失败: ${data.toString().slice(0, 100)}` });
        }
      });
    });

    req.on('error', (e) => {
      resolve({ code: -1, msg: `请求失败: ${e.message}` });
    });

    req.on('timeout', () => {
      req.destroy();
      resolve({ code: -1, msg: '请求超时' });
    });

    req.write(payload);
    req.end();
  });
}

/**
 * 格式化单个选题为飞书消息段落
 *
 * @param {object} topic - parseStarredTopics 返回的单个选题
 * @returns {string}
 */
function formatTopicMessage(topic) {
  const { num, title, fields } = topic;
  const { rawHit, hooks, dataPoints } = fields;

  // 构建消息
  const parts = [];

  // 标题行
  parts.push(`【选题 ${num}】${title}`);

  // 关键词命中
  if (rawHit) {
    parts.push(`【命中】${rawHit}`);
  }

  // 钩子文案（选第一个）
  if (hooks.length > 0) {
    parts.push(`\n【钩子】${hooks[0]}`);
  }

  // 3个数据点
  if (dataPoints.length > 0) {
    parts.push(`\n【数据点】`);
    for (const dp of dataPoints) {
      parts.push(`   ${dp}`);
    }
  }

  return parts.join('\n');
}

// ============================================================
// 3. 主逻辑
// ============================================================

async function run() {
  const today = getTodayStr();
  const topicFile = path.join(TOPICS_DIR, `${today}_topics.md`);

  // 检查今天的选题文件是否存在
  if (!fs.existsSync(topicFile)) {
    console.error(`notify_feishu: 今天的选题文件不存在: ${topicFile}`);
    return { success: false, reason: '选题文件不存在' };
  }

  // 读取文件内容
  let content;
  try {
    content = fs.readFileSync(topicFile, 'utf-8');
  } catch (e) {
    console.error(`notify_feishu: 读取选题文件失败: ${e.message}`);
    return { success: false, reason: `读取失败: ${e.message}` };
  }

  // 解析 ⭐推送选题
  const starredTopics = parseStarredTopics(content);

  if (starredTopics.length === 0) {
    console.log('notify_feishu: 今天无 ⭐推送选题，跳过发送');
    return { success: true, sent: 0 };
  }

  // 最多取前3个
  const topicsToSend = starredTopics.slice(0, 10);
  console.log(`notify_feishu: 准备发送 ${topicsToSend.length} 个 ⭐推送选题`);

  // 构建飞书消息
  const tz = new Date();
  const nowStr = `${tz.getFullYear()}-${String(tz.getMonth() + 1).padStart(2, '0')}-${String(tz.getDate()).padStart(2, '0')} ${String(tz.getHours()).padStart(2, '0')}:${String(tz.getMinutes()).padStart(2, '0')}`;

  const header = [
    `📋 自媒体选题日报`,
    `日期：${today}`,
    `发送时间：${nowStr}`,
    `⭐推送选题：${topicsToSend.length} 个`,
    ``,
    `━━━━━━ 选题详情 ━━━━━━`,
    ``
  ].join('\n');

  const topicMessages = topicsToSend.map(t => formatTopicMessage(t));
  const footer = [
    ``,
    `━━━━━━`,
    `⚠️ 仅供参考，内容请自行核实`,
    `🤖 由 notify_feishu.js 自动推送 · ${today}`
  ].join('\n');

  const fullText = [header, ...topicMessages, footer].join('\n\n');

  // 发送飞书消息（使用 fetch Node 18+ 原生支持）
  let webhookSuccess = false;
  let webhookError = null;

  try {
    const response = await fetch(FEISHU_WEBHOOK, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        msg_type: 'text',
        content: { text: fullText }
      })
    });

    const data = await response.json();

    if (data.code === 0) {
      console.log(`notify_feishu: ✓ 成功发送 ${topicsToSend.length} 个选题到飞书`);
      webhookSuccess = true;
    } else if (data.code !== undefined) {
      console.error(`notify_feishu: 飞书返回错误 - code=${data.code}, msg=${data.msg}`);
      webhookError = `飞书错误 code=${data.code}: ${data.msg}`;
    } else {
      console.error(`notify_feishu: 飞书响应格式异常 - ${JSON.stringify(data).slice(0, 200)}`);
      webhookError = '响应格式异常';
    }
  } catch (e) {
    // fetch 失败（网络问题等）
    console.error(`notify_feishu: 发送失败 - ${e.message}`);
    webhookError = `网络错误: ${e.message}`;
  }

  // Webhook 推送失败 → 输出 fallback 内容（供 cron agent 推用户私聊）
  if (!webhookSuccess) {
    console.log('');
    console.log('=== FALLBACK_MESSAGE_START ===');
    console.log(fullText);
    console.log('=== FALLBACK_MESSAGE_END ===');
    console.log('');
    console.error(`[notify_feishu] ⚠️ Webhook 推送失败 (${webhookError})，已输出 fallback 消息供 agent 推用户私聊`);
    return { success: false, reason: webhookError, fallbackProvided: true };
  }

  return { success: true, sent: topicsToSend.length };
}

// ============================================================
// 4. 入口
// ============================================================

(async () => {
  console.log(`=== notify_feishu.js 启动 (${new Date().toISOString()}) ===`);

  try {
    const res = await run();

    if (!res.success) {
      console.error(`notify_feishu: 推送失败 - ${res.reason}`);
      // 失败不阻塞，不抛异常，只记录
    }

    console.log(`=== notify_feishu.js 结束 ===`);
    process.exit(0);
  } catch (err) {
    // 全局兜底：捕获所有未处理异常
    console.error(`notify_feishu: 未捕获异常 - ${err.message}`);
    process.exit(0); // 不阻塞 cron
  }
})();
