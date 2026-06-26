#!/usr/bin/env node
/**
 * sprint-dashboard-card.mjs
 * 迭代进展看板：展示当前/指定迭代的工作项完成率、各状态分布
 *
 * 用法：
 *   node sprint-dashboard-card.mjs [projectId] [sprintId]
 *   node sprint-dashboard-card.mjs callback "SPRINT_SWITCH|projectId|sprintId"
 */

import { readFileSync } from 'fs';
import { TOKEN, ORG_ID, OPEN_ID, requireConfig, YUNXIAO_TOKEN, DEFAULT_PROJECT_ID } from './config.mjs';

requireConfig();

// ── 配置 ──────────────────────────────────────────────────────────────────────

const YUNXIAO_BASE = 'https://openapi-rdc.aliyuncs.com/oapi/v1';
const FEISHU_BASE = 'https://open.feishu.cn/open-apis';

const DEFAULT_PROJECT_NAME = '我的项目';

// 逻辑状态分类（云效三大 logicalStatus）
const DONE_STATUSES = ['已完成', '已修复', '已关闭', '暂不修复', '测试通过', '已验收', '完成'];
const IN_PROGRESS_STATUSES = ['处理中', '开发中', '测试中', '待发布', '进行中'];

// ── 飞书 ──────────────────────────────────────────────────────────────────────
async function getFeishuToken() {
  const config = JSON.parse(readFileSync(process.env.HOME + '/.openclaw/openclaw.json', 'utf8'));
  const feishu = config.channels?.feishu ?? config.integrations?.feishu ?? {};
  const res = await fetch(`${FEISHU_BASE}/auth/v3/tenant_access_token/internal`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ app_id: feishu.appId, app_secret: feishu.appSecret }),
  });
  const d = await res.json();
  return d.tenant_access_token;
}

async function sendCard(card, updateMsgId = null) {
  const token = await getFeishuToken();
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
  if (data.code !== 0) throw new Error(`Feishu error: ${data.msg}`);
  return data.data.message_id;
}

// ── 云效 API ──────────────────────────────────────────────────────────────────
async function yunxiaoGet(path) {
  const res = await fetch(`${YUNXIAO_BASE}${path}`, {
    headers: { 'x-yunxiao-token': YUNXIAO_TOKEN },
  });
  const data = await res.json();
  if (data.errorCode) throw new Error(data.errorMessage || JSON.stringify(data));
  return data;
}

async function yunxiaoPost(path, body) {
  const res = await fetch(`${YUNXIAO_BASE}${path}`, {
    method: 'POST',
    headers: { 'x-yunxiao-token': YUNXIAO_TOKEN, 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  if (data.errorCode) throw new Error(data.errorMessage || JSON.stringify(data));
  return data;
}

// ── 进度条（飞书 lark_md 模拟）────────────────────────────────────────────────
function progressBar(done, total, width = 20) {
  if (total === 0) return '无工作项';
  const pct = Math.round((done / total) * 100);
  const filled = Math.round((done / total) * width);
  const bar = '█'.repeat(filled) + '░'.repeat(width - filled);
  return `\`${bar}\` ${pct}%（${done}/${total}）`;
}

// ── 主逻辑 ───────────────────────────────────────────────────────────────────
async function showDashboard(projectId, sprintId, updateMsgId = null) {
  // 1. 获取迭代列表
  let sprints = [];
  try {
    const res = await yunxiaoGet(`/projex/organizations/${ORG_ID}/projects/${projectId}/sprints?page=1&perPage=10`);
    sprints = Array.isArray(res) ? res : (res.sprints || []);
  } catch (e) {
    console.error('查询迭代失败:', e.message);
  }

  if (sprints.length === 0) {
    await sendCard({
      config: { wide_screen_mode: true },
      header: { title: { tag: 'plain_text', content: '📊 迭代看板' }, template: 'orange' },
      elements: [{ tag: 'div', text: { tag: 'lark_md', content: '当前项目暂无迭代，请先创建迭代。' } }],
    }, updateMsgId);
    return;
  }

  // 2. 选目标迭代（默认最新活跃迭代，或指定）
  let targetSprint = sprintId
    ? sprints.find(s => s.id === sprintId) || sprints[0]
    : sprints.find(s => s.status === 'ACTIVE') || sprints[0];

  // 3. 查该迭代下所有工作项（遍历各类型）
  const typeIds = [
    '37da3a07df4d08aef2e3b393', // 缺陷
    '9uy29901re573f561d69jn40', // 产品类需求
    'bca48ee2a0976d38f4802fae', // 技术类需求
    'ba102e46bc6a8483d9b7f25c', // 任务
  ];

  let allWorkitems = [];
  for (const typeId of typeIds) {
    try {
      const conditions = JSON.stringify({
        conditionGroups: [[
          { fieldIdentifier: 'sprint', operator: 'IN', value: [targetSprint.id], className: 'string', format: 'list' },
        ]],
      });
      const res = await yunxiaoPost(`/projex/organizations/${ORG_ID}/workitems:search`, {
        spaceId: projectId,
        spaceType: 'Project',
        workitemTypeId: typeId,
        conditions,
        page: 1,
        perPage: 100,
      });
      const items = res.workitems || [];
      allWorkitems = allWorkitems.concat(items);
    } catch (e) {
      // 某个类型查不到，跳过
    }
  }

  // 4. 统计
  const total = allWorkitems.length;
  const done = allWorkitems.filter(w => {
    const name = w.status?.displayName || w.status?.name || '';
    return DONE_STATUSES.some(s => name.includes(s));
  }).length;
  const inProgress = allWorkitems.filter(w => {
    const name = w.status?.displayName || w.status?.name || '';
    return IN_PROGRESS_STATUSES.some(s => name.includes(s));
  }).length;
  const pending = total - done - inProgress;

  // 按负责人统计
  const byAssignee = {};
  for (const w of allWorkitems) {
    const name = w.assignedTo?.name || '未分配';
    if (!byAssignee[name]) byAssignee[name] = { total: 0, done: 0 };
    byAssignee[name].total++;
    const statusName = w.status?.displayName || w.status?.name || '';
    if (DONE_STATUSES.some(s => statusName.includes(s))) byAssignee[name].done++;
  }

  // 5. 构建卡片
  const sprintName = targetSprint.name || '未命名迭代';
  const startDate = targetSprint.startDate ? targetSprint.startDate.slice(0, 10) : '—';
  const endDate = targetSprint.endDate ? targetSprint.endDate.slice(0, 10) : '—';

  // 成员进展
  const memberLines = Object.entries(byAssignee)
    .sort((a, b) => b[1].total - a[1].total)
    .slice(0, 8)
    .map(([name, stat]) => `• **${name}**：${stat.done}/${stat.total} 已完成`)
    .join('\n');

  // 迭代切换按钮（最近 5 个）
  const switchButtons = sprints.slice(0, 5).map(s => ({
    tag: 'button',
    text: { tag: 'plain_text', content: s.id === targetSprint.id ? `▶ ${s.name}` : s.name },
    type: s.id === targetSprint.id ? 'primary' : 'default',
    value: { command: `SPRINT_SWITCH|${projectId}|${s.id}` },
  }));

  const card = {
    config: { wide_screen_mode: true },
    header: {
      title: { tag: 'plain_text', content: `📊 迭代进展：${sprintName}` },
      template: done === total && total > 0 ? 'green' : 'blue',
    },
    elements: [
      {
        tag: 'div', fields: [
          { is_short: true, text: { tag: 'lark_md', content: `**开始**\n${startDate}` } },
          { is_short: true, text: { tag: 'lark_md', content: `**结束**\n${endDate}` } },
        ],
      },
      { tag: 'hr' },
      { tag: 'div', text: { tag: 'lark_md', content: `**完成进度**\n${progressBar(done, total)}` } },
      {
        tag: 'div', fields: [
          { is_short: true, text: { tag: 'lark_md', content: `**待处理** ⬜\n${pending}` } },
          { is_short: true, text: { tag: 'lark_md', content: `**进行中** 🔵\n${inProgress}` } },
          { is_short: true, text: { tag: 'lark_md', content: `**已完成** ✅\n${done}` } },
          { is_short: true, text: { tag: 'lark_md', content: `**合计**\n${total}` } },
        ],
      },
      ...(memberLines ? [
        { tag: 'hr' },
        { tag: 'div', text: { tag: 'lark_md', content: `**成员进展**\n${memberLines}` } },
      ] : []),
      ...(sprints.length > 1 ? [
        { tag: 'hr' },
        { tag: 'div', text: { tag: 'lark_md', content: '**切换迭代：**' } },
        { tag: 'action', actions: switchButtons },
      ] : []),
    ],
  };

  const msgId = await sendCard(card, updateMsgId);
  if (!updateMsgId) console.log(`✅ 迭代看板已发送 msgId=${msgId} sprint=${sprintName} 完成率=${done}/${total}`);
}

// ── CLI 入口 ──────────────────────────────────────────────────────────────────
const [,, cmd, ...rest] = process.argv;

if (cmd === 'callback') {
  const payload = rest[0] || '';
  const parts = payload.split('|');
  if (parts[0] === 'SPRINT_SWITCH') {
    const [, projectId, sprintId] = parts;
    // 找发送过的卡片 msgId（从 pending-cards.json）
    let updateMsgId = null;
    try {
      const cards = JSON.parse(readFileSync(
        `${process.env.HOME}/.openclaw/pending-cards.json`, 'utf8'
      ));
      updateMsgId = cards[cards.length - 1]?.messageId || null;
    } catch {}
    await showDashboard(projectId, sprintId, updateMsgId);
  }
} else {
  // 默认：发看板
  const projectId = cmd && cmd.length > 10 ? cmd : DEFAULT_PROJECT_ID;
  const sprintId = rest[0] || null;
  await showDashboard(projectId, sprintId);
}
