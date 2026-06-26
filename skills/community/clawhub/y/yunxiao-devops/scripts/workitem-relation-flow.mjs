#!/usr/bin/env node
/**
 * workitem-relation-flow.mjs
 * 工作项关联：查看/创建 ASSOCIATED 关联关系
 *
 * 用法：
 *   node workitem-relation-flow.mjs <workitemId>          # 查看工作项及其关联
 *   node workitem-relation-flow.mjs link <fromId> <toId>  # 创建关联
 *   node workitem-relation-flow.mjs callback "WI_RELATE|fromId|toId"
 *
 * 环境变量覆盖（多组织支持）：
 *   YUNXIAO_ORG_ID=<orgId>   YUNXIAO_TOKEN=<token>
 *
 * ⚠️ API 踩坑（2026-03-18 验证）：
 *   - 创建关联：POST /workitems/{id}/relationRecords?relationType=ASSOCIATED&workitemId={targetId}
 *     参数走 query string，body 传 {}，不是 /relations 路径也不是 body 传参
 *   - 查关联：GET /workitems/{id}/relationRecords?relationType=ASSOCIATED
 *   - OpenAPI 只支持 ASSOCIATED 类型
 */

import { readFileSync } from 'fs';
import { TOKEN, ORG_ID, OPEN_ID, requireConfig, YUNXIAO_TOKEN } from './config.mjs';

requireConfig();

const YUNXIAO_BASE = 'https://openapi-rdc.aliyuncs.com/oapi/v1';
const FEISHU_BASE = 'https://open.feishu.cn/open-apis';

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

async function yunxiaoPost(path, body = {}) {
  const r = await fetch(`${YUNXIAO_BASE}${path}`, {
    method: 'POST',
    headers: { 'x-yunxiao-token': YUNXIAO_TOKEN, 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  const d = await r.json();
  if (d.errorCode) throw new Error(d.errorMessage);
  return d;
}

async function showWorkitemWithRelations(workitemId) {
  const wi = await yunxiaoGet(`/projex/organizations/${ORG_ID}/workitems/${workitemId}`);

  // 查关联项（正确路径）
  let relations = [];
  try {
    const r = await yunxiaoGet(`/projex/organizations/${ORG_ID}/workitems/${workitemId}/relationRecords?relationType=ASSOCIATED`);
    relations = Array.isArray(r) ? r : [];
  } catch (e) {
    console.warn('查关联项失败:', e.message);
  }

  // 关联项展示：拿到 workitemId 后查详情
  const relLines = [];
  for (const rel of relations.slice(0, 8)) {
    const targetId = rel.workitemId || rel.relatedWorkitemId;
    if (!targetId) continue;
    try {
      const target = await yunxiaoGet(`/projex/organizations/${ORG_ID}/workitems/${targetId}`);
      relLines.push(`• [${target.serialNumber || targetId}] ${target.subject?.slice(0, 40) || '—'} (${target.status?.displayName || '—'})`);
    } catch {
      relLines.push(`• ${targetId}`);
    }
  }

  const card = {
    config: { wide_screen_mode: true },
    header: { title: { tag: 'plain_text', content: `🔗 ${wi.serialNumber} 工作项关联` }, template: 'blue' },
    elements: [
      { tag: 'div', fields: [
        { is_short: false, text: { tag: 'lark_md', content: `**${wi.subject}**` } },
        { is_short: true, text: { tag: 'lark_md', content: `**状态**\n${wi.status?.displayName || '—'}` } },
        { is_short: true, text: { tag: 'lark_md', content: `**类型**\n${wi.workitemType?.name || '—'}` } },
      ]},
      { tag: 'hr' },
      { tag: 'div', text: { tag: 'lark_md', content: `**关联项（${relations.length}）**\n${relLines.join('\n') || '暂无关联工作项'}` } },
      { tag: 'hr' },
      { tag: 'div', text: { tag: 'lark_md', content: '**新建关联：**\n发消息 `关联 <目标工作项ID>` 将当前工作项与目标关联（ASSOCIATED 类型）' } },
      { tag: 'action', actions: [
        { tag: 'button', text: { tag: 'plain_text', content: '+ 关联工作项' }, type: 'primary',
          value: { command: `WI_RELATE_START|${workitemId}` } },
      ]},
    ],
  };

  const msgId = await sendCard(card);
  console.log(`✅ 关联卡片已发送 msgId=${msgId} relations=${relations.length}`);
}

async function createRelation(fromId, toId) {
  // ✅ 正确方式：query string 传参，body 传 {}
  const result = await yunxiaoPost(
    `/projex/organizations/${ORG_ID}/workitems/${fromId}/relationRecords?relationType=ASSOCIATED&workitemId=${toId}`,
    {}
  );

  // GET 验证
  const verify = await yunxiaoGet(
    `/projex/organizations/${ORG_ID}/workitems/${fromId}/relationRecords?relationType=ASSOCIATED`
  );
  const records = Array.isArray(verify) ? verify : [];
  const created = records.find(r => r.id === result?.id);

  if (result?.id) {
    await sendNotify(
      `✅ 关联已创建\n\n**${fromId}** ↔ **ASSOCIATED** ↔ **${toId}**\n\n关联记录 ID：\`${result.id}\``,
      '🔗 关联创建成功', 'green'
    );
    console.log(`✅ 关联创建成功 from=${fromId} to=${toId} id=${result.id}`);
  } else {
    await sendNotify(`⚠️ 关联请求已发送，但未收到 ID，请到云效页面手动确认。`, '⚠️ 请确认', 'orange');
    console.warn('关联创建未返回 id');
  }
}

const [,, cmd, ...rest] = process.argv;

if (cmd === 'callback') {
  const parts = (rest[0] || '').split('|');
  const action = parts[0];
  if (action === 'WI_RELATE') {
    const [, fromId, toId] = parts;
    await createRelation(fromId, toId);
  } else if (action === 'WI_RELATE_START') {
    const [, fromId] = parts;
    await sendNotify(
      `请发消息告诉我要关联的目标工作项 ID。\n\n格式：\`关联 <工作项ID>\`\n\n当前工作项：\`${fromId}\``,
      '🔗 输入目标工作项', 'blue'
    );
  }
} else if (cmd === 'link') {
  const [fromId, toId] = rest;
  if (!fromId || !toId) {
    console.error('用法: node workitem-relation-flow.mjs link <fromId> <toId>');
    process.exit(1);
  }
  await createRelation(fromId, toId);
} else if (cmd) {
  await showWorkitemWithRelations(cmd);
} else {
  console.log('用法: node workitem-relation-flow.mjs <workitemId>');
  console.log('     node workitem-relation-flow.mjs link <fromId> <toId>');
}
