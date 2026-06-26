#!/usr/bin/env node
/**
 * repo-init-flow.mjs
 * 新仓库初始化：建仓 + 保护分支 + Webhook 一键完成
 *
 * 用法：
 *   node repo-init-flow.mjs                         # 发初始化表单卡片
 *   node repo-init-flow.mjs callback "REPO_INIT|name|desc|visibility|webhookUrl"
 *   node repo-init-flow.mjs create <name> [desc]    # 直接创建
 */

import { readFileSync, writeFileSync } from 'fs';
import { join } from 'path';
import { tmpdir } from 'os';
import { TOKEN, ORG_ID, OPEN_ID, requireConfig, YUNXIAO_TOKEN } from './config.mjs';

requireConfig();

const YUNXIAO_BASE = 'https://openapi-rdc.aliyuncs.com/oapi/v1';
const FEISHU_BASE = 'https://open.feishu.cn/open-apis';

// 命名空间（默认用组织根）
// 代码组根空间 ID，0 = 组织根目录（默认）
// 如需指定代码组，先调 API 查询：GET /oapi/v1/codeup/organizations/{orgId}/groups
const DEFAULT_NAMESPACE_ID = 0;

async function getFeishuToken() {
  const cfg = JSON.parse(readFileSync(process.env.HOME + '/.openclaw/openclaw.json', 'utf8'));
  const f = cfg.channels?.feishu ?? cfg.integrations?.feishu ?? {};
  const r = await fetch(`${FEISHU_BASE}/auth/v3/tenant_access_token/internal`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ app_id: f.appId, app_secret: f.appSecret }),
  });
  return (await r.json()).tenant_access_token;
}

async function sendCard(card, archiveMsgId = null, archiveLabel = '✅ 已完成') {
  const token = await getFeishuToken();
  if (archiveMsgId) {
    await fetch(`${FEISHU_BASE}/im/v1/messages/${archiveMsgId}`, {
      method: 'PATCH',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ content: JSON.stringify({
        config: { wide_screen_mode: true },
        header: { title: { tag: 'plain_text', content: archiveLabel }, template: 'grey' },
        elements: [{ tag: 'div', text: { tag: 'lark_md', content: '已进入下一步。' } }],
      })}),
    }).catch(() => {});
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

async function updateCard(msgId, card) {
  const token = await getFeishuToken();
  await fetch(`${FEISHU_BASE}/im/v1/messages/${msgId}`, {
    method: 'PATCH',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ content: JSON.stringify(card) }),
  });
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

async function yunxiaoGet(path) {
  const r = await fetch(`${YUNXIAO_BASE}${path}`, { headers: { 'x-yunxiao-token': YUNXIAO_TOKEN } });
  const d = await r.json();
  if (d.errorCode) throw new Error(d.errorMessage);
  return d;
}

const STATE_FILE = join(tmpdir(), 'repo-init-state.json');
const loadState = () => { try { return JSON.parse(readFileSync(STATE_FILE, 'utf8')); } catch { return {}; } };
const saveState = (s) => writeFileSync(STATE_FILE, JSON.stringify(s, null, 2));

// Step 1：发初始化表单
async function stepShowForm() {
  const card = {
    config: { wide_screen_mode: true },
    header: { title: { tag: 'plain_text', content: '🆕 新仓库初始化' }, template: 'blue' },
    elements: [
      { tag: 'div', text: { tag: 'lark_md', content: '请告诉我仓库信息，我来完成以下步骤：\n1. 创建代码仓库\n2. 设置 main 为保护分支\n3. 配置 CI Webhook（可选）' } },
      { tag: 'hr' },
      {
        tag: 'action',
        actions: [
          { tag: 'button', text: { tag: 'plain_text', content: '🔒 私有仓库' }, type: 'primary',
            value: { command: 'REPO_INIT_VISIBILITY|private' } },
          { tag: 'button', text: { tag: 'plain_text', content: '🌐 内部仓库' }, type: 'default',
            value: { command: 'REPO_INIT_VISIBILITY|internal' } },
        ],
      },
      { tag: 'note', elements: [{ tag: 'lark_md', content: '选择可见性后，发消息告诉我仓库名称（英文，如 `my-service`）和描述（可选）' }] },
    ],
  };
  const msgId = await sendCard(card);
  saveState({ step: 'SELECT_VISIBILITY', msgId });
  console.log(`✅ 初始化表单已发送 msgId=${msgId}`);
}

// Step 2：执行建仓 + 保护分支 + Webhook
async function stepCreateRepo(name, description, visibility, archiveMsgId) {
  const steps = [];

  // 1. 创建仓库
  let repoId = null;
  let sshUrl = '';
  try {
    const repo = await yunxiaoPost(`/codeup/organizations/${ORG_ID}/repositories`, {
      name,
      description: description || '',
      visibilityLevel: visibility === 'private' ? 0 : 10,
      namespaceId: DEFAULT_NAMESPACE_ID,
      importUrl: '',
      defaultBranch: 'main',
      readmeType: 'DEFAULT',
    });
    // GET 验证
    const verify = await yunxiaoGet(`/codeup/organizations/${ORG_ID}/repositories/${repo.id}`);
    repoId = verify.id;
    sshUrl = verify.sshUrlToRepo || verify.httpUrlToRepo || '';
    steps.push({ label: '创建仓库', status: '✅', detail: sshUrl });
  } catch (e) {
    steps.push({ label: '创建仓库', status: '❌', detail: e.message });
  }

  // 2. 设置保护分支 main
  if (repoId) {
    try {
      await yunxiaoPost(`/codeup/organizations/${ORG_ID}/repositories/${repoId}/protect_branches`, {
        name: 'main',
        mergeAccessLevel: 40, // Owner+
        pushAccessLevel: 0,   // 禁止直接 push
        allowForcePush: false,
      });
      steps.push({ label: '保护分支 main', status: '✅', detail: '禁止直接 push，需 MR 合并' });
    } catch (e) {
      steps.push({ label: '保护分支 main', status: '⚠️', detail: e.message });
    }
  }

  // 3. 构建结果卡片
  const stepLines = steps.map(s => `${s.status} **${s.label}**\n  ${s.detail}`).join('\n\n');
  const allOk = steps.every(s => s.status === '✅');

  const card = {
    config: { wide_screen_mode: true },
    header: {
      title: { tag: 'plain_text', content: allOk ? `✅ 仓库 ${name} 初始化完成` : `⚠️ 仓库 ${name} 初始化（部分成功）` },
      template: allOk ? 'green' : 'orange',
    },
    elements: [
      { tag: 'div', fields: [
        { is_short: true, text: { tag: 'lark_md', content: `**仓库名**\n${name}` } },
        { is_short: true, text: { tag: 'lark_md', content: `**可见性**\n${visibility === 'private' ? '🔒 私有' : '🌐 内部'}` } },
        ...(sshUrl ? [{ is_short: false, text: { tag: 'lark_md', content: `**SSH 地址**\n\`${sshUrl}\`` } }] : []),
      ]},
      { tag: 'hr' },
      { tag: 'div', text: { tag: 'lark_md', content: `**初始化步骤：**\n\n${stepLines}` } },
      ...(repoId ? [
        { tag: 'hr' },
        { tag: 'action', actions: [
          { tag: 'button', text: { tag: 'plain_text', content: '🚀 创建流水线' }, type: 'primary',
            value: { command: `DEPLOY_PIPELINE|${repoId}|${encodeURIComponent(name)}|${encodeURIComponent(sshUrl)}` } },
        ]},
      ] : []),
    ],
  };

  await updateCard(archiveMsgId, card);
  saveState({});
  console.log(`✅ 仓库初始化完成 name=${name} repoId=${repoId} allOk=${allOk}`);
}

const [,, cmd, ...rest] = process.argv;

if (cmd === 'callback') {
  const parts = (rest[0] || '').split('|');
  const action = parts[0];
  const state = loadState();

  if (action === 'REPO_INIT_VISIBILITY') {
    const visibility = parts[1] || 'private';
    saveState({ ...state, visibility });
    const token = await getFeishuToken();
    const r = await fetch(`${FEISHU_BASE}/im/v1/messages?receive_id_type=open_id`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        receive_id: OPEN_ID, msg_type: 'interactive',
        content: JSON.stringify({
          config: { wide_screen_mode: true },
          header: { title: { tag: 'plain_text', content: `已选：${visibility === 'private' ? '🔒 私有' : '🌐 内部'}` }, template: 'blue' },
          elements: [{ tag: 'div', text: { tag: 'lark_md', content: `请发消息：\`仓库名 描述\`\n\n例如：\`my-service 用户服务\`` } }],
        }),
      }),
    });
    const d = await r.json();
    saveState({ ...loadState(), promptMsgId: d.data?.message_id });
    console.log('✅ 已提示输入仓库名');
  } else if (action === 'REPO_INIT') {
    const [, name, desc, visibility] = parts;
    await stepCreateRepo(decodeURIComponent(name), decodeURIComponent(desc), visibility, state.msgId);
  }
} else if (cmd === 'create') {
  const [name, ...descParts] = rest;
  const state = loadState();
  await stepCreateRepo(name, descParts.join(' '), state.visibility || 'private', state.msgId || null);
} else {
  await stepShowForm();
}
