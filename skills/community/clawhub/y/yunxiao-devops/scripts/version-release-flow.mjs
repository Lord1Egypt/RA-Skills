#!/usr/bin/env node
/**
 * version-release-flow.mjs
 * 版本发布管理：创建版本 + 查看/关联工作项 + 批量更新状态
 *
 * 用法：
 *   node version-release-flow.mjs [projectId]          # 查版本列表
 *   node version-release-flow.mjs create <name> [desc] # 创建版本
 *   node version-release-flow.mjs callback "VER_DETAIL|projectId|versionId"
 *   node version-release-flow.mjs callback "VER_CLOSE|projectId|versionId"
 */

import { readFileSync } from 'fs';
import { TOKEN, ORG_ID, USER_ID, OPEN_ID, requireConfig, YUNXIAO_TOKEN, DEFAULT_PROJECT_ID } from './config.mjs';

requireConfig();

const YUNXIAO_BASE = 'https://openapi-rdc.aliyuncs.com/oapi/v1';
const FEISHU_BASE = 'https://open.feishu.cn/open-apis';

const ALL_TYPE_IDS = [
  '37da3a07df4d08aef2e3b393',
  '9uy29901re573f561d69jn40',
  'bca48ee2a0976d38f4802fae',
  'ba102e46bc6a8483d9b7f25c',
];
const DONE_STATUSES = ['已完成', '已修复', '已关闭', '暂不修复', '测试通过', '已验收', '完成'];

async function getFeishuToken() {
  const cfg = JSON.parse(readFileSync(process.env.HOME + '/.openclaw/openclaw.json', 'utf8'));
  const f = cfg.channels?.feishu ?? cfg.integrations?.feishu ?? {};
  const r = await fetch(`${FEISHU_BASE}/auth/v3/tenant_access_token/internal`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ app_id: f.appId, app_secret: f.appSecret }),
  });
  return (await r.json()).tenant_access_token;
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
  return sendCard({
    config: { wide_screen_mode: true },
    header: { title: { tag: 'plain_text', content: title }, template: color },
    elements: [{ tag: 'div', text: { tag: 'lark_md', content } }],
  });
}

async function yunxiaoGet(path) {
  const r = await fetch(`${YUNXIAO_BASE}${path}`, { headers: { 'x-yunxiao-token': YUNXIAO_TOKEN } });
  const d = await r.json();
  if (d.errorCode) throw new Error(d.errorMessage);
  return d;
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

async function yunxiaoPut(path, body) {
  const r = await fetch(`${YUNXIAO_BASE}${path}`, {
    method: 'PUT',
    headers: { 'x-yunxiao-token': YUNXIAO_TOKEN, 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  const d = await r.json();
  if (d.errorCode) throw new Error(d.errorMessage);
  return d;
}

// 查该版本下的工作项
async function fetchVersionWorkitems(projectId, versionId) {
  const all = [];
  const conditions = JSON.stringify({
    conditionGroups: [[
      { fieldIdentifier: 'versions', operator: 'IN', value: [versionId], className: 'string', format: 'list' },
    ]],
  });
  for (const typeId of ALL_TYPE_IDS) {
    try {
      const res = await yunxiaoPost(`/projex/organizations/${ORG_ID}/workitems:search`, {
        spaceId: projectId, spaceType: 'Project', workitemTypeId: typeId,
        conditions, page: 1, perPage: 50,
      });
      all.push(...(res.workitems || []));
    } catch {}
  }
  return all;
}

// 版本列表
async function showVersionList(projectId) {
  const versions = await yunxiaoGet(`/projex/organizations/${ORG_ID}/projects/${projectId}/versions?page=1&perPage=10`);
  const list = Array.isArray(versions) ? versions : (versions.versions || []);

  if (list.length === 0) {
    await sendNotify('该项目暂无版本，发消息 `创建版本 v1.0.0 描述` 来创建', '📦 版本列表', 'blue');
    return;
  }

  const STATUS_EMOJI = { ACTIVE: '🟢', CLOSED: '🔴', UNRELEASED: '🟡' };
  const versionLines = list.map(v => {
    const emoji = STATUS_EMOJI[v.status] || '⚪';
    const date = v.endDate?.slice(0, 10) || '—';
    return `${emoji} **${v.name}** (截止 ${date})`;
  }).join('\n');

  const card = {
    config: { wide_screen_mode: true },
    header: { title: { tag: 'plain_text', content: `📦 版本列表（${list.length}）` }, template: 'blue' },
    elements: [
      { tag: 'div', text: { tag: 'lark_md', content: versionLines } },
      { tag: 'hr' },
      {
        tag: 'action',
        actions: list.slice(0, 5).map(v => ({
          tag: 'button',
          text: { tag: 'plain_text', content: v.name },
          type: v.status === 'ACTIVE' ? 'primary' : 'default',
          value: { command: `VER_DETAIL|${projectId}|${v.id}` },
        })),
      },
    ],
  };
  const msgId = await sendCard(card);
  console.log(`✅ 版本列表已发送 msgId=${msgId} count=${list.length}`);
}

// 版本详情
async function showVersionDetail(projectId, versionId, updateMsgId = null) {
  const versions = await yunxiaoGet(`/projex/organizations/${ORG_ID}/projects/${projectId}/versions?page=1&perPage=50`);
  const list = Array.isArray(versions) ? versions : (versions.versions || []);
  const version = list.find(v => v.id === versionId) || {};

  const workitems = await fetchVersionWorkitems(projectId, versionId);
  const done = workitems.filter(w => DONE_STATUSES.some(s => (w.status?.displayName || '').includes(s)));
  const total = workitems.length;

  const wiLines = workitems.slice(0, 8).map(w =>
    `${DONE_STATUSES.some(s => (w.status?.displayName || '').includes(s)) ? '✅' : '🔵'} [${w.serialNumber}] ${w.subject?.slice(0, 40)}（${w.status?.displayName}）`
  ).join('\n');

  const pct = total > 0 ? Math.round((done.length / total) * 100) : 0;
  const bar = '█'.repeat(Math.round(pct / 5)) + '░'.repeat(20 - Math.round(pct / 5));

  const card = {
    config: { wide_screen_mode: true },
    header: { title: { tag: 'plain_text', content: `📦 版本 ${version.name || versionId}` }, template: pct === 100 ? 'green' : 'blue' },
    elements: [
      { tag: 'div', fields: [
        { is_short: true, text: { tag: 'lark_md', content: `**状态**\n${version.status || '—'}` } },
        { is_short: true, text: { tag: 'lark_md', content: `**截止日期**\n${version.endDate?.slice(0, 10) || '—'}` } },
      ]},
      { tag: 'div', text: { tag: 'lark_md', content: `**完成进度**\n\`${bar}\` ${pct}%（${done.length}/${total}）` } },
      { tag: 'hr' },
      { tag: 'div', text: { tag: 'lark_md', content: `**工作项：**\n${wiLines || '暂无关联工作项'}` } },
      { tag: 'hr' },
      { tag: 'action', actions: [
        ...(version.status === 'ACTIVE' ? [{
          tag: 'button', text: { tag: 'plain_text', content: '🔴 关闭版本（已发布）' }, type: 'danger',
          value: { command: `VER_CLOSE|${projectId}|${versionId}` },
        }] : []),
        { tag: 'button', text: { tag: 'plain_text', content: '← 版本列表' }, type: 'default',
          value: { command: `VER_LIST|${projectId}` } },
      ]},
    ],
  };

  const msgId = await sendCard(card, updateMsgId);
  if (!updateMsgId) console.log(`✅ 版本详情已发送 msgId=${msgId} progress=${pct}%`);
}

// 创建版本
async function createVersion(projectId, name, description = '') {
  const now = new Date();
  const endDate = new Date(now.getTime() + 14 * 86400000).toISOString().slice(0, 10);

  const result = await yunxiaoPost(`/projex/organizations/${ORG_ID}/projects/${projectId}/versions`, {
    name,
    description,
    startDate: now.toISOString().slice(0, 10),
    endDate,
    owners: [USER_ID],
  });

  // GET 验证
  const versions = await yunxiaoGet(`/projex/organizations/${ORG_ID}/projects/${projectId}/versions?page=1&perPage=10`);
  const list = Array.isArray(versions) ? versions : (versions.versions || []);
  const created = list.find(v => v.name === name);

  if (created) {
    await sendNotify(`✅ 版本 **${name}** 已创建\n截止日期：${endDate}\n\n发送工作项 ID 关联到此版本，或查看版本详情。`, '📦 版本已创建', 'green');
    console.log(`✅ 版本创建成功 id=${created.id} name=${name}`);
  } else {
    await sendNotify(`⚠️ 版本创建请求成功，但列表中未找到，请手动确认。`, '⚠️ 请确认', 'orange');
  }
}

const [,, cmd, ...rest] = process.argv;

if (cmd === 'callback') {
  const parts = (rest[0] || '').split('|');
  const action = parts[0];
  if (action === 'VER_DETAIL') {
    await showVersionDetail(parts[1], parts[2]);
  } else if (action === 'VER_LIST') {
    await showVersionList(parts[1] || DEFAULT_PROJECT_ID);
  } else if (action === 'VER_CLOSE') {
    const [, projectId, versionId] = parts;
    try {
      await yunxiaoPut(`/projex/organizations/${ORG_ID}/projects/${projectId}/versions/${versionId}`, { status: 'CLOSED' });
      await sendNotify(`✅ 版本 \`${versionId}\` 已关闭（状态：已发布）`, '✅ 版本已关闭', 'green');
      console.log(`✅ 版本关闭成功 versionId=${versionId}`);
    } catch (e) {
      await sendNotify(`❌ 关闭失败：${e.message}`, '❌ 失败', 'red');
    }
  }
} else if (cmd === 'create') {
  const [name, ...descParts] = rest;
  await createVersion(DEFAULT_PROJECT_ID, name, descParts.join(' '));
} else {
  await showVersionList(cmd || DEFAULT_PROJECT_ID);
}
