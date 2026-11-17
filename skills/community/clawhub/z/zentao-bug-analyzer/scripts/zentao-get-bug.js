#!/usr/bin/env node
/**
 * zentao-get-bug.js — 获取禅道 Bug 详情 JSON
 *
 * 用法:
 *   node zentao-get-bug.js --ws=<wsEndpoint> --bug-id=<id> [--zentao-url=http://zentao.gxatek.com:20080]
 *
 * 输出 (stdout):
 *   Bug 详情 JSON 对象 + 操作历史 JSON 数组（分行分隔输出）
 *
 * 需要先启动 zentao-login.js 获取 WS endpoint。
 */

const { parseArgs, connectAndGetPage } = require('./zentao-utils');

/**
 * 从 HTML 中提取 JSON 数组。用于从 zen-tao bug-view 页面提取 historyChanges 数据。
 * 比简单括号匹配更健壮：使用 JSON 感知的解析。
 */
function extractJsonArray(html, keyName) {
  // 尝试找到 keyName 的位置
  let idx = html.indexOf('&quot;' + keyName + '&quot;');
  if (idx < 0) {
    idx = html.indexOf('"' + keyName + '"');
  }
  if (idx < 0) {
    idx = html.indexOf(keyName);
  }
  if (idx < 0) {
    return null; // 未找到，返回 null 让调用方处理
  }

  // 向前找 '['
  let start = idx;
  while (start > 0 && html[start] !== '[') start--;
  if (html[start] !== '[') return null;

  // 括号深度匹配找 ']'
  let depth = 0;
  let end = start;
  let inString = false;
  let escape = false;
  for (let i = start; i < html.length; i++) {
    const ch = html[i];
    if (escape) {
      escape = false;
      continue;
    }
    if (ch === '\\') {
      escape = true;
      continue;
    }
    if (ch === '"') {
      inString = !inString;
      continue;
    }
    if (inString) continue;
    if (ch === '[') depth++;
    else if (ch === ']') { depth--; if (depth === 0) { end = i + 1; break; } }
  }

  const raw = html.substring(start, end);

  // HTML 实体解码（覆盖常见实体）
  const decoded = raw
    .replace(/&quot;/g, '"')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&')
    .replace(/&#39;/g, "'")
    .replace(/&#x27;/g, "'")
    .replace(/&#x2F;/g, '/')
    .replace(/&#(\d+);/g, (_, n) => String.fromCharCode(parseInt(n, 10)))
    .replace(/&#x([0-9a-fA-F]+);/g, (_, n) => String.fromCharCode(parseInt(n, 16)));

  try {
    return JSON.parse(decoded);
  } catch (e) {
    return { _parseError: e.message, _sample: raw.substring(0, 1000) };
  }
}

async function main() {
  const config = parseArgs();

  if (!config.wsEndpoint) {
    console.error('[ERROR] 缺少 --ws 参数（WS endpoint）');
    process.exit(1);
  }
  if (!config.bugId) {
    console.error('[ERROR] 缺少 --bug-id 参数');
    process.exit(1);
  }

  console.error(`[INFO] 连接到浏览器: ${config.wsEndpoint}`);

  const { page } = await connectAndGetPage(config.wsEndpoint);

  console.error(`[INFO] 获取 Bug #${config.bugId} 详情和操作历史...`);

  // 获取 Bug 详情 + 从 bug-view 页面提取操作历史
  // 注意: 必须在两次独立的 page.evaluate 中进行 (同一 evaluate 中串行 fetch 会导致 HTML 缺少 historyChanges)
  const bugResult = await page.evaluate(async ({ bugId, zentaoUrl }) => {
    const resp = await fetch(`${zentaoUrl}/api.php/v1/bugs/${bugId}`, {
      credentials: 'include',
    });
    if (!resp.ok) {
      return { error: true, status: resp.status, statusText: resp.statusText };
    }
    return await resp.json();
  }, { bugId: config.bugId, zentaoUrl: config.zentaoUrl });

  if (bugResult.error) {
    console.error(`[ERROR] API 请求失败 (HTTP ${bugResult.status}): ${bugResult.statusText}`);
    console.log(JSON.stringify(bugResult));
    process.exit(1);
  }

  // 获取 bug-view 页面的 HTML 并提取 history JSON（独立 evaluate，避免与 API fetch 冲突）
  const historyResult = await page.evaluate(async ({ bugId, zentaoUrl }) => {
    const resp = await fetch(`${zentaoUrl}/bug-view-${bugId}.html`, {
      credentials: 'include',
    });
    if (!resp.ok) {
      return { _fetchError: `bug-view 页面请求失败 (HTTP ${resp.status})` };
    }
    const html = await resp.text();
    // 返回原始 HTML，由 Node.js 端做 JSON 提取（更健壮）
    return { _htmlSource: true, html };
  }, { bugId: config.bugId, zentaoUrl: config.zentaoUrl });

  let history;
  if (historyResult._htmlSource) {
    history = extractJsonArray(historyResult.html, 'historyChanges');
    if (history === null) {
      history = []; // historyChanges 未找到，返回空数组
    }
  } else {
    history = historyResult; // 兼容 fetch 错误等返回
  }

  const result = { bug: bugResult, history };

  // 分行输出：先输出 bug，再输出 history（避免单次 JSON.stringify 太大导致进程超时）
  console.log('---BUG_START---');
  console.log(JSON.stringify(result.bug));
  console.log('---BUG_END---');
  console.log('---HISTORY_START---');
  console.log(JSON.stringify(result.history));
  console.log('---HISTORY_END---');
}

main().catch((err) => {
  console.error(`[ERROR] ${err.message}`);
  process.exit(1);
});
