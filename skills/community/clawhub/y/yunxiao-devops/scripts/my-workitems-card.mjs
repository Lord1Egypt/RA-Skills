/**
 * my-workitems-card.mjs
 * 列出指定用户（默认当前用户 YUNXIAO_USER_ID）需要处理的所有工作项，以飞书卡片分页展示。
 *
 * 用法：
 *   node my-workitems-card.mjs [--user <yunxiaoUserId>] [--project <projectId>] [--page <n>]
 *
 * 分页翻页 payload 格式：
 *   WI_LIST_PAGE|<userId>|<projectId>|<page>
 *
 * agent 收到后：
 *   node my-workitems-card.mjs --page <n> [--user <id>] [--project <id>] --update-msg <messageId>
 */

import { readFileSync } from 'fs';
import { homedir } from 'os';
import { TOKEN, ORG_ID, USER_ID, OPEN_ID, requireConfig, DEFAULT_PROJECT_ID } from './config.mjs';

requireConfig();

const FEISHU_BASE = 'https://open.feishu.cn/open-apis';
const YUNXIAO_BASE = 'https://openapi-rdc.aliyuncs.com/oapi/v1/projex';
const PLATFORM_BASE = 'https://openapi-rdc.aliyuncs.com/oapi/v1/platform';

const PAGE_SIZE = 8;  // 每页展示条数

// ── 自动获取当前用户 ID ────────────────────────────────────────────────────────
async function getCurrentUserId() {
  const res = await fetch(`${PLATFORM_BASE}/user`, {
    headers: { 'x-yunxiao-token': TOKEN },
  });
  const data = await res.json();
  if (!data.id) throw new Error(`无法获取当前用户 ID：${JSON.stringify(data)}`);
  return data.id;
}

// ── 获取所有项目 ID 列表 ───────────────────────────────────────────────────────
async function getAllProjects() {
  const res = await fetch(`${YUNXIAO_BASE}/organizations/${ORG_ID}/projects:search`, {
    method: 'POST',
    headers: { 'x-yunxiao-token': TOKEN, 'Content-Type': 'application/json' },
    body: JSON.stringify({ logicalStatus: 'NORMAL', page: 1, perPage: 100 }),
  });
  const data = await res.json();
  return (Array.isArray(data) ? data : []).map(p => ({ id: p.id, name: p.name }));
}

// ── 并发控制：最多同时 N 个请求 ───────────────────────────────────────────────
async function pLimit(tasks, concurrency = 5) {
  const results = [];
  let i = 0;
  async function worker() {
    while (i < tasks.length) {
      const idx = i++;
      results[idx] = await tasks[idx]();
    }
  }
  await Promise.all(Array.from({ length: Math.min(concurrency, tasks.length) }, worker));
  return results;
}

// ── 飞书 Token ─────────────────────────────────────────────────────────────────
async function getFeishuToken() {
  const config = JSON.parse(readFileSync(`${homedir()}/.openclaw/openclaw.json`, 'utf8'));
  const res = await fetch(`${FEISHU_BASE}/auth/v3/tenant_access_token/internal`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      app_id: config.channels?.feishu?.appId,
      app_secret: config.channels?.feishu?.appSecret,
    }),
  });
  const data = await res.json();
  if (data.code !== 0) throw new Error(`Token error: ${data.msg}`);
  return data.tenant_access_token;
}

// ── 查询某类别工作项（单项目）────────────────────────────────────────────────
async function searchByCategory(category, projectId, userId, openOnly = true) {
  if (!projectId || !userId) return [];
  const condList = [
    { fieldIdentifier: 'assignedTo', operator: 'CONTAINS', value: [userId], toValue: null, className: 'user', format: 'list' },
  ];
  if (openOnly) {
    condList.push({ fieldIdentifier: 'logicalStatus', operator: 'NOT_IN', value: ['CLOSED'], className: 'string', format: 'list' });
  }
  const conditions = JSON.stringify({ conditionGroups: [condList] });

  const res = await fetch(`${YUNXIAO_BASE}/organizations/${ORG_ID}/workitems:search`, {
    method: 'POST',
    headers: {
      'x-yunxiao-token': TOKEN,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      category,
      spaceId: projectId,
      spaceType: 'Project',
      conditions,
      orderBy: 'gmtCreate',
      sort: 'desc',
      page: 1,
      perPage: 200,
    }),
  });
  const data = await res.json();
  return Array.isArray(data) ? data : [];
}

// "需要处理"的状态 nameEn 白名单（服务端过滤不到 Done/Fixed 等，客户端补刀）
// 只有 nameEn 在此集合内的工作项才会展示
const ACTIONABLE_EN = new Set([
  'New',          // 待确认
  'To Do',        // 待处理
  'Open',         // 打开
  'In Progress',  // 处理中 / 进行中
  'Reopen',       // 再次打开
  'Reopened',
  'In Development',
  'In Testing',
  'Pending',
  'Processing',
  'Review',
  'To Be Merged',
  'Blocked',
]);

// ── 跨所有项目查询当前用户工作项 ──────────────────────────────────────────────
// 返回 { items, projectSummary }
async function searchAllProjects(userId) {
  const projects = await getAllProjects();
  const categories = ['Task', 'Bug', 'Req'];

  const tasks = [];
  for (const p of projects) {
    for (const cat of categories) {
      tasks.push(() => searchByCategory(cat, p.id, userId, true).then(items =>
        items.map(i => ({ ...i, _projectId: p.id, _projectName: p.name }))
      ).catch(() => []));
    }
  }

  const results = await pLimit(tasks, 5);
  const allItems = results.flat();

  // 客户端过滤：只保留"需要处理"状态
  const actionable = allItems.filter(item => ACTIONABLE_EN.has(item.status?.nameEn));

  // 按 gmtModified 倒序
  actionable.sort((a, b) => (b.gmtModified ?? b.gmtCreate ?? 0) - (a.gmtModified ?? a.gmtCreate ?? 0));

  // 项目摘要
  const projectSummary = {};
  for (const item of actionable) {
    const name = item._projectName ?? '--';
    projectSummary[name] = (projectSummary[name] ?? 0) + 1;
  }

  return { items: actionable, projectSummary };
}

// ── 查询项目信息 ──────────────────────────────────────────────────────────────
async function getProject(projectId) {
  const res = await fetch(`${YUNXIAO_BASE}/organizations/${ORG_ID}/projects/${projectId}`, {
    headers: { 'x-yunxiao-token': TOKEN },
  });
  return res.json();
}

// ── 发飞书卡片 ────────────────────────────────────────────────────────────────
async function sendCard(token, card, updateMsgId = null) {
  if (updateMsgId) {
    await fetch(`${FEISHU_BASE}/im/v1/messages/${updateMsgId}`, {
      method: 'PATCH',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ content: JSON.stringify(card) }),
    });
    return updateMsgId;
  }
  const res = await fetch(`${FEISHU_BASE}/im/v1/messages?receive_id_type=open_id`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ receive_id: OPEN_ID, msg_type: 'interactive', content: JSON.stringify(card) }),
  });
  const data = await res.json();
  if (data.code !== 0) throw new Error(`Send error: ${data.msg}`);
  return data.data?.message_id;
}

// ── 工具函数 ──────────────────────────────────────────────────────────────────
const TYPE_EMOJI = { Task: '📋', Bug: '🐛', Req: '💡', Topic: '📌', Request: '📣', Risk: '⚠️' };
const STATUS_EMOJI = {
  '待处理': '⏳', '处理中': '🔄', '已完成': '✅', '已取消': '❌',
  '待确认': '⏳', '已修复': '✅', '暂不修复': '🚫', '再次打开': '🔁', '已关闭': '🔒',
};

function fmtItem(item) {
  const typeEmoji = TYPE_EMOJI[item.categoryId] ?? '•';
  const statusEmoji = STATUS_EMOJI[item.status?.displayName] ?? '•';
  const serial = item.serialNumber ?? item.id?.slice(0, 8) ?? '?';
  const subject = item.subject?.slice(0, 30) ?? '(无标题)';
  const status = item.status?.displayName ?? '--';
  const proj = item._projectName ? ` · ${item._projectName.slice(0, 10)}` : '';
  return `${typeEmoji} **${serial}** ${subject}\n　${statusEmoji} ${status}${proj}`;
}

// ── 构建卡片 ──────────────────────────────────────────────────────────────────
function buildListCard({ items, page, totalPages, projectName, userName, userId, projectId, projectSummary }) {
  const start = (page - 1) * PAGE_SIZE;
  const pageItems = items.slice(start, start + PAGE_SIZE);
  const total = items.length;

  // 按状态分类统计
  const statusCount = {};
  for (const item of items) {
    const s = item.status?.displayName ?? '--';
    statusCount[s] = (statusCount[s] ?? 0) + 1;
  }
  const statsText = Object.entries(statusCount)
    .map(([s, n]) => `${STATUS_EMOJI[s] ?? '•'} ${s} ×${n}`)
    .join('　');

  const elements = [
    {
      tag: 'div',
      fields: [
        { is_short: true, text: { tag: 'lark_md', content: `**项目**\n${projectName}` } },
        { is_short: true, text: { tag: 'lark_md', content: `**负责人**\n${userName}` } },
        { is_short: true, text: { tag: 'lark_md', content: `**合计**\n${total} 项` } },
        { is_short: true, text: { tag: 'lark_md', content: `**页数**\n${page} / ${totalPages}` } },
      ],
    },
    { tag: 'div', text: { tag: 'lark_md', content: statsText || '暂无工作项' } },
  ];

  // 跨项目模式：展示项目摘要
  if (projectSummary && Object.keys(projectSummary).length > 0) {
    const summaryText = Object.entries(projectSummary)
      .sort(([, a], [, b]) => b - a)
      .slice(0, 6)
      .map(([name, cnt]) => `**${name.slice(0, 8)}** ×${cnt}`)
      .join('　');
    elements.push({ tag: 'div', text: { tag: 'lark_md', content: `📂 ${summaryText}` } });
  }

  elements.push({ tag: 'hr' });

  // 工作项列表
  for (const item of pageItems) {
    elements.push({
      tag: 'div',
      text: { tag: 'lark_md', content: fmtItem(item) },
    });
  }

  if (pageItems.length === 0) {
    elements.push({ tag: 'div', text: { tag: 'lark_md', content: '本页暂无数据' } });
  }

  elements.push({ tag: 'hr' });

  // 分页按钮
  const pageActions = [];
  if (page > 1) {
    pageActions.push({
      tag: 'button',
      text: { tag: 'plain_text', content: '◀ 上一页' },
      type: 'default',
      value: { command: `WI_LIST_PAGE|${userId}|${projectId}|${page - 1}` },
    });
  }
  if (page < totalPages) {
    pageActions.push({
      tag: 'button',
      text: { tag: 'plain_text', content: '下一页 ▶' },
      type: 'primary',
      value: { command: `WI_LIST_PAGE|${userId}|${projectId}|${page + 1}` },
    });
  }
  if (pageActions.length > 0) {
    elements.push({ tag: 'action', actions: pageActions });
  }

  elements.push({
    tag: 'note',
    elements: [{ tag: 'lark_md', content: `第 ${start + 1}–${Math.min(start + PAGE_SIZE, total)} 项，共 ${total} 项` }],
  });

  return {
    config: { wide_screen_mode: true },
    header: {
      title: { tag: 'plain_text', content: `📋 我的工作项（第 ${page} 页）` },
      template: 'blue',
    },
    elements,
  };
}

// ── CLI 入口 ──────────────────────────────────────────────────────────────────
const args = process.argv.slice(2);
function getArg(name) {
  const idx = args.indexOf(`--${name}`);
  return idx !== -1 ? args[idx + 1] : null;
}

const argUserId = getArg('user');
const argProjectId = getArg('project');
const page = parseInt(getArg('page') ?? '1', 10);
const updateMsgId = getArg('update-msg');

// 1. 解析 userId（优先命令行参数 → 环境变量 → 自动从 token 查）
const userId = argUserId || USER_ID || await getCurrentUserId();
if (!userId) throw new Error('无法确定用户 ID，请配置 YUNXIAO_USER_ID');

// 2. 查工作项：有 projectId 则单项目查，否则遍历所有项目
const projectId = argProjectId || DEFAULT_PROJECT_ID;
let allItems, projectName;

if (projectId) {
  // 单项目模式（原有逻辑）
  const [taskItems, bugItems, reqItems, project] = await Promise.all([
    searchByCategory('Task', projectId, userId),
    searchByCategory('Bug', projectId, userId),
    searchByCategory('Req', projectId, userId),
    getProject(projectId),
  ]);
  allItems = [...reqItems, ...taskItems, ...bugItems];
  projectName = project.name ?? projectId;
} else {
  // 跨所有项目模式
  const { items: crossItems, projectSummary } = await searchAllProjects(userId);
  allItems = crossItems;
  projectName = `全部项目（进行中，最近活跃）`;
  // 把项目摘要注入到 buildListCard 里展示
  allItems._projectSummary = projectSummary;
}

// 从组织成员缓存里找用户名（简化：直接从第一条工作项的 assignedTo 取）
const userName = allItems[0]?.assignedTo?.name ?? userId;

const totalPages = Math.max(1, Math.ceil(allItems.length / PAGE_SIZE));
const safePage = Math.min(Math.max(1, page), totalPages);

const card = buildListCard({ items: allItems, page: safePage, totalPages, projectName, userName, userId, projectId, projectSummary: allItems._projectSummary });
const token = await getFeishuToken();
const msgId = await sendCard(token, card, updateMsgId);
console.log(`✅ 工作项列表卡片已发送 message_id=${msgId}，共 ${allItems.length} 条，第 ${safePage}/${totalPages} 页`);
