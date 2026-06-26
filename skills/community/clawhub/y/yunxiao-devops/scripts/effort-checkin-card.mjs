#!/usr/bin/env node
/**
 * effort-checkin-card.mjs
 * 工时打卡：查今日已登记工时 + 快捷登记
 *
 * 用法：
 *   node effort-checkin-card.mjs [userId] [projectId]
 *   node effort-checkin-card.mjs callback "EFFORT_LOG|workitemId|hours|desc"
 *   node effort-checkin-card.mjs submit <workitemId> <hours> [desc]
 */

import { readFileSync } from 'fs';
import { TOKEN, ORG_ID, USER_ID, OPEN_ID, requireConfig, YUNXIAO_TOKEN, DEFAULT_PROJECT_ID } from './config.mjs';

const YUNXIAO_BASE = 'https://openapi-rdc.aliyuncs.com/oapi/v1';
const FEISHU_BASE = 'https://open.feishu.cn/open-apis';

const ALL_TYPE_IDS = [
  '37da3a07df4d08aef2e3b393',
  '9uy29901re573f561d69jn40',
  'bca48ee2a0976d38f4802fae',
  'ba102e46bc6a8483d9b7f25c',
];
const INPROGRESS_STATUSES = ['处理中', '开发中', '测试中', '待发布', '进行中', '待确认'];

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

async function sendNotify(content, title, color = 'blue') {
  const token = await getFeishuToken();
  const card = {
    config: { wide_screen_mode: true },
    header: { title: { tag: 'plain_text', content: title }, template: color },
    elements: [{ tag: 'div', text: { tag: 'lark_md', content } }],
  };
  const r = await fetch(`${FEISHU_BASE}/im/v1/messages?receive_id_type=open_id`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ receive_id: OPEN_ID, msg_type: 'interactive', content: JSON.stringify(card) }),
  });
  return (await r.json()).data?.message_id;
}

async function yunxiaoGet(path) {
  const r = await fetch(`${YUNXIAO_BASE}${path}`, { headers: { 'x-yunxiao-token': YUNXIAO_TOKEN } });
  return r.json();
}

async function yunxiaoPost(path, body) {
  const r = await fetch(`${YUNXIAO_BASE}${path}`, {
    method: 'POST',
    headers: { 'x-yunxiao-token': YUNXIAO_TOKEN, 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  const d = await r.json();
  if (d.errorCode) throw new Error(d.errorMessage);
  return d;
}

// 获取今日已登记工时（从进行中工作项）
async function fetchTodayEfforts(workitemIds) {
  const today = new Date().toISOString().slice(0, 10);
  const records = [];
  for (const id of workitemIds.slice(0, 10)) {
    try {
      const r = await yunxiaoGet(`/projex/organizations/${ORG_ID}/workitems/${id}/effortRecords`);
      const list = Array.isArray(r) ? r : (r.records || []);
      const todayRecords = list.filter(e => {
        const d = e.gmtStart ? new Date(e.gmtStart).toISOString().slice(0, 10) : '';
        return d === today;
      });
      records.push(...todayRecords.map(e => ({ ...e, workitemId: id })));
    } catch {}
  }
  return records;
}

// 快捷登记工时
async function logEffort(workitemId, hours, description = '今日工作') {
  const now = new Date();
  const startHour = Math.max(9, now.getHours() - Math.ceil(hours));
  const gmtStart = new Date(now);
  gmtStart.setHours(startHour, 0, 0, 0);
  const gmtEnd = new Date(gmtStart.getTime() + hours * 3600000);

  const result = await yunxiaoPost(`/projex/organizations/${ORG_ID}/workitems/${workitemId}/effortRecords`, {
    actualTime: Math.round(hours * 60),
    gmtStart: gmtStart.toISOString(),
    gmtEnd: gmtEnd.toISOString(),
    description,
  });

  // GET 验证
  const verify = await yunxiaoGet(`/projex/organizations/${ORG_ID}/workitems/${workitemId}/effortRecords`);
  const list = Array.isArray(verify) ? verify : (verify.records || []);
  const today = new Date().toISOString().slice(0, 10);
  const todayTotal = list
    .filter(e => new Date(e.gmtStart || 0).toISOString().slice(0, 10) === today)
    .reduce((sum, e) => sum + (e.actualTime || 0), 0);

  return { recordId: result.id, todayTotalMinutes: todayTotal };
}

async function main(userId = USER_ID, projectId = DEFAULT_PROJECT_ID) {
  requireConfig();
  // 查我的进行中工作项
  const myWorkitems = [];
  for (const typeId of ALL_TYPE_IDS) {
    try {
      const conditions = JSON.stringify({
        conditionGroups: [[
          { fieldIdentifier: 'assignedTo', operator: 'IN', value: [userId], className: 'string', format: 'member' },
        ]],
      });
      const res = await yunxiaoPost(`/projex/organizations/${ORG_ID}/workitems:search`, {
        spaceId: projectId, spaceType: 'Project', workitemTypeId: typeId,
        conditions, page: 1, perPage: 20,
      });
      const items = (res.workitems || []).filter(w => {
        const s = w.status?.displayName || '';
        return INPROGRESS_STATUSES.some(x => s.includes(x));
      });
      myWorkitems.push(...items);
    } catch {}
  }

  // 查今日工时
  const todayEfforts = await fetchTodayEfforts(myWorkitems.map(w => w.id));
  const todayTotalH = (todayEfforts.reduce((sum, e) => sum + (e.actualTime || 0), 0) / 60).toFixed(1);

  // 构建快捷登记按钮（每个工作项 2h/4h 快捷）
  const quickLogButtons = myWorkitems.slice(0, 4).flatMap(w => [
    {
      tag: 'button',
      text: { tag: 'plain_text', content: `${w.serialNumber} +2h` },
      type: 'default',
      value: { command: `EFFORT_LOG|${w.id}|2|${encodeURIComponent(w.subject?.slice(0, 20) || '工作')}` },
    },
    {
      tag: 'button',
      text: { tag: 'plain_text', content: `${w.serialNumber} +4h` },
      type: 'default',
      value: { command: `EFFORT_LOG|${w.id}|4|${encodeURIComponent(w.subject?.slice(0, 20) || '工作')}` },
    },
  ]);

  const wiLines = myWorkitems.slice(0, 6).map(w => `• [${w.serialNumber}] ${w.subject?.slice(0, 40)}（${w.status?.displayName}）`).join('\n');

  const elements = [
    { tag: 'div', fields: [
      { is_short: true, text: { tag: 'lark_md', content: `**今日已登记**\n${todayTotalH}h` } },
      { is_short: true, text: { tag: 'lark_md', content: `**进行中工作项**\n${myWorkitems.length} 项` } },
    ]},
    { tag: 'hr' },
    ...(myWorkitems.length > 0 ? [
      { tag: 'div', text: { tag: 'lark_md', content: `**进行中的工作项：**\n${wiLines}` } },
      { tag: 'hr' },
      { tag: 'div', text: { tag: 'lark_md', content: '**快捷登记工时（点击即登记）：**' } },
      { tag: 'action', actions: quickLogButtons.slice(0, 4) },
      ...(quickLogButtons.length > 4 ? [{ tag: 'action', actions: quickLogButtons.slice(4, 8) }] : []),
    ] : [
      { tag: 'div', text: { tag: 'lark_md', content: '暂无进行中的工作项，无需打卡 🎉' } },
    ]),
    { tag: 'note', elements: [{ tag: 'lark_md', content: '自定义工时：发消息 `打卡 工作项ID 3h 完成功能开发`' }] },
  ];

  const msgId = await sendCard({
    config: { wide_screen_mode: true },
    header: { title: { tag: 'plain_text', content: `⏱️ 工时打卡 · 今日已登记 ${todayTotalH}h` }, template: todayTotalH >= 8 ? 'green' : 'blue' },
    elements,
  });
  console.log(`✅ 工时卡片已发送 msgId=${msgId} 今日=${todayTotalH}h`);
}

const [,, cmd, ...rest] = process.argv;

if (cmd === 'callback') {
  const payload = rest[0] || '';
  const parts = payload.split('|');
  if (parts[0] === 'EFFORT_LOG') {
    const [, workitemId, hours, descEncoded] = parts;
    const desc = decodeURIComponent(descEncoded || '今日工作');
    try {
      const { recordId, todayTotalMinutes } = await logEffort(workitemId, parseFloat(hours), desc);
      const totalH = (todayTotalMinutes / 60).toFixed(1);
      await sendNotify(
        `✅ 已登记 **${hours}h** 工时\n工作项：\`${workitemId}\`\n描述：${desc}\n\n**今日累计：${totalH}h**`,
        '⏱️ 工时已登记', 'green'
      );
      console.log(`✅ 工时登记成功 recordId=${recordId} 今日=${totalH}h`);
    } catch (e) {
      await sendNotify(`❌ 登记失败：${e.message}`, '❌ 登记失败', 'red');
    }
  }
} else if (cmd === 'submit') {
  const [workitemId, hours, ...descParts] = rest;
  const desc = descParts.join(' ') || '今日工作';
  try {
    const { recordId, todayTotalMinutes } = await logEffort(workitemId, parseFloat(hours), desc);
    console.log(`✅ 登记成功 recordId=${recordId} 今日累计=${(todayTotalMinutes / 60).toFixed(1)}h`);
    await sendNotify(
      `✅ 已登记 **${hours}h** 工时\n工作项：\`${workitemId}\`\n描述：${desc}\n\n**今日累计：${(todayTotalMinutes / 60).toFixed(1)}h**`,
      '⏱️ 工时已登记', 'green'
    );
  } catch (e) {
    console.error('登记失败:', e.message);
  }
} else {
  await main(cmd, rest[0]);
}
