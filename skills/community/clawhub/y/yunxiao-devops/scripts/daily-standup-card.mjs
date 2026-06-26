#!/usr/bin/env node
/**
 * daily-standup-card.mjs
 * 每日站会卡片：我的进行中任务 + 昨日完成 + 流水线最近状态，一张卡片搞定
 *
 * 用法：
 *   node daily-standup-card.mjs [userId] [projectId]
 */

import { readFileSync } from 'fs';
import { TOKEN, ORG_ID, USER_ID, OPEN_ID, requireConfig, YUNXIAO_TOKEN, DEFAULT_PROJECT_ID } from './config.mjs';

const YUNXIAO_BASE = 'https://openapi-rdc.aliyuncs.com/oapi/v1';
const FEISHU_BASE = 'https://open.feishu.cn/open-apis';

// 已知工作项类型
const ALL_TYPE_IDS = [
  '37da3a07df4d08aef2e3b393', // 缺陷
  '9uy29901re573f561d69jn40', // 产品类需求
  'bca48ee2a0976d38f4802fae', // 技术类需求
  'ba102e46bc6a8483d9b7f25c', // 任务
];

const DONE_STATUSES = ['已完成', '已修复', '已关闭', '暂不修复', '测试通过', '已验收', '完成'];
const INPROGRESS_STATUSES = ['处理中', '开发中', '测试中', '待发布', '进行中'];

async function getFeishuToken() {
  const cfg = JSON.parse(readFileSync(process.env.HOME + '/.openclaw/openclaw.json', 'utf8'));
  const f = cfg.channels?.feishu ?? cfg.integrations?.feishu ?? {};
  const r = await fetch(`${FEISHU_BASE}/auth/v3/tenant_access_token/internal`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ app_id: f.appId, app_secret: f.appSecret }),
  });
  return (await r.json()).tenant_access_token;
}

async function sendCard(card) {
  const token = await getFeishuToken();
  const r = await fetch(`${FEISHU_BASE}/im/v1/messages?receive_id_type=open_id`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ receive_id: OPEN_ID, msg_type: 'interactive', content: JSON.stringify(card) }),
  });
  const d = await r.json();
  if (d.code !== 0) throw new Error(d.msg);
  return d.data.message_id;
}

async function yunxiaoPost(path, body) {
  const r = await fetch(`${YUNXIAO_BASE}${path}`, {
    method: 'POST',
    headers: { 'x-yunxiao-token': YUNXIAO_TOKEN, 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  return r.json();
}

async function yunxiaoGet(path) {
  const r = await fetch(`${YUNXIAO_BASE}${path}`, { headers: { 'x-yunxiao-token': YUNXIAO_TOKEN } });
  return r.json();
}

async function fetchMyWorkitems(userId, projectId) {
  const all = [];
  const conditions = JSON.stringify({
    conditionGroups: [[
      { fieldIdentifier: 'assignedTo', operator: 'IN', value: [userId], className: 'string', format: 'member' },
    ]],
  });
  for (const typeId of ALL_TYPE_IDS) {
    try {
      const res = await yunxiaoPost(`/projex/organizations/${ORG_ID}/workitems:search`, {
        spaceId: projectId, spaceType: 'Project', workitemTypeId: typeId,
        conditions, page: 1, perPage: 50,
      });
      const items = res.workitems || [];
      all.push(...items);
    } catch {}
  }
  return all;
}

async function fetchRecentPipelines() {
  const pipelines = [
    // 在此填入你的流水线 ID，或留空（脚本会调 API 动态获取最近流水线）
  ];
  const results = [];
  for (const p of pipelines) {
    try {
      const r = await yunxiaoGet(`/flow/organizations/${ORG_ID}/pipelines/${p.id}/runs?page=1&perPage=1`);
      const run = (r.pipelineRuns || r.runs || r)[0];
      if (run) results.push({ name: p.name, status: run.status, startTime: run.startTime?.slice(5, 16) });
    } catch {}
  }
  return results;
}

const STATUS_EMOJI = { SUCCESS: '✅', FAIL: '❌', RUNNING: '🔄', CANCELED: '⏸️' };

async function main(userId = USER_ID, projectId = DEFAULT_PROJECT_ID) {
  requireConfig();
  const [workitems, pipelines] = await Promise.all([
    fetchMyWorkitems(userId, projectId),
    fetchRecentPipelines(),
  ]);

  const now = new Date();
  const yesterday = new Date(now - 86400000);
  const yStr = yesterday.toISOString().slice(0, 10);

  const inProgress = workitems.filter(w => {
    const s = w.status?.displayName || '';
    return INPROGRESS_STATUSES.some(x => s.includes(x));
  });
  const doneYesterday = workitems.filter(w => {
    const s = w.status?.displayName || '';
    const updated = w.gmtModified ? new Date(w.gmtModified).toISOString().slice(0, 10) : '';
    return DONE_STATUSES.some(x => s.includes(x)) && updated === yStr;
  });
  const pending = workitems.filter(w => {
    const s = w.status?.displayName || '';
    return !INPROGRESS_STATUSES.some(x => s.includes(x)) && !DONE_STATUSES.some(x => s.includes(x));
  });

  const wiLine = (w) => `• [${w.serialNumber}] ${w.subject?.slice(0, 40)}（${w.status?.displayName}）`;

  const elements = [
    { tag: 'div', fields: [
      { is_short: true, text: { tag: 'lark_md', content: `**日期**\n${now.toLocaleDateString('zh-CN')}` } },
      { is_short: true, text: { tag: 'lark_md', content: `**进行中**\n${inProgress.length} 项` } },
    ]},
    { tag: 'hr' },
  ];

  if (inProgress.length > 0) {
    elements.push({ tag: 'div', text: { tag: 'lark_md', content: `**🔵 进行中（${inProgress.length}）**\n${inProgress.slice(0, 5).map(wiLine).join('\n') || '无'}` } });
  }
  if (doneYesterday.length > 0) {
    elements.push({ tag: 'div', text: { tag: 'lark_md', content: `**✅ 昨日完成（${doneYesterday.length}）**\n${doneYesterday.slice(0, 5).map(wiLine).join('\n')}` } });
  }
  if (pending.length > 0) {
    elements.push({ tag: 'div', text: { tag: 'lark_md', content: `**⬜ 待开始（${pending.length}）**\n${pending.slice(0, 3).map(wiLine).join('\n')}` } });
  }
  if (workitems.length === 0) {
    elements.push({ tag: 'div', text: { tag: 'lark_md', content: '暂无工作项分配给你 🎉' } });
  }

  if (pipelines.length > 0) {
    elements.push({ tag: 'hr' });
    const pLines = pipelines.map(p => `${STATUS_EMOJI[p.status] || '❓'} ${p.name}（${p.startTime || '—'}）`).join('\n');
    elements.push({ tag: 'div', text: { tag: 'lark_md', content: `**🚀 流水线最近状态**\n${pLines}` } });
  }

  elements.push({ tag: 'hr' });
  elements.push({ tag: 'action', actions: [
    { tag: 'button', text: { tag: 'plain_text', content: '📋 查看我的工作项' }, type: 'default',
      value: { command: `MY_WORKITEMS|${userId}|${projectId}` } },
    { tag: 'button', text: { tag: 'plain_text', content: '📝 创建工作项' }, type: 'primary',
      value: { command: `CREATE_WORKITEM|${projectId}` } },
  ]});

  const msgId = await sendCard({
    config: { wide_screen_mode: true },
    header: { title: { tag: 'plain_text', content: `☀️ 今日站会 · ${now.toLocaleDateString('zh-CN', { weekday: 'long' })}` }, template: 'blue' },
    elements,
  });
  console.log(`✅ 站会卡片已发送 msgId=${msgId} 进行中=${inProgress.length} 昨完成=${doneYesterday.length}`);
}

const [,, userId, projectId] = process.argv;
await main(userId, projectId);
