#!/usr/bin/env node
/**
 * create-workitem-flow.mjs
 * 创建工作项交互式流程（需求/任务/缺陷）
 *
 * 用法：
 *   node create-workitem-flow.mjs [projectId]       # 发类型选择卡片
 *   node create-workitem-flow.mjs callback "<payload>"
 *
 * 回调 payload：
 *   CREATE_TYPE|projectId|typeCategory|typeId|typeName
 *   CREATE_SUBMIT|projectId|typeId|typeName|subject|assignee|priority
 */

import { readFileSync, writeFileSync } from 'fs';
import { join } from 'path';
import { tmpdir } from 'os';
import { execSync } from 'child_process';
import { TOKEN, ORG_ID, USER_ID, OPEN_ID, requireConfig, YUNXIAO_TOKEN, DEFAULT_PROJECT_ID } from './config.mjs';

requireConfig();

// ── 配置 ──────────────────────────────────────────────────────────────────────

const YUNXIAO_BASE = 'https://openapi-rdc.aliyuncs.com/oapi/v1';
const FEISHU_BASE = 'https://open.feishu.cn/open-apis';

// 默认项目

const DEFAULT_PROJECT_NAME = '我的项目';

// 工作项类型 ID（组织级，不同组织可能不同）
// 通过 GET /oapi/v1/projex/organizations/{orgId}/workitemTypes 查询你的实际 ID
const WORKITEM_TYPES = {
  Bug: [
    { id: '37da3a07df4d08aef2e3b393', name: '缺陷', icon: '🐛' },
    { id: 'bba77181ef64f834248a0175', name: '线上故障', icon: '🚨' },
  ],
  Req: [
    { id: '9uy29901re573f561d69jn40', name: '产品类需求', icon: '📋' },
    { id: 'bca48ee2a0976d38f4802fae', name: '技术类需求', icon: '⚙️' },
  ],
  Task: [
    { id: 'ba102e46bc6a8483d9b7f25c', name: '任务', icon: '✅' },
  ],
};

// 优先级选项（从已知工作项中提取）
const PRIORITY_OPTIONS = [
  { id: 'cbe5b0e3b69f73cff27bb697ee', label: '紧急' },
  { id: '20b85abab49c8df20fa9a3e9ea', label: '高' },
  { id: '74d3caa5204b844389ad4a07ef', label: '中' },
  { id: '15fb24a0b94e0f4e7aa6b14aa6', label: '低' },
];

// 严重程度（缺陷专用）
const SERIOUS_LEVEL_OPTIONS = [
  { id: 'ae4f617d2244de3e3a4c5b97c4', label: '1-致命' },
  { id: '56694bfbb20bca16e2697c069f', label: '2-严重' },
  { id: '78ca1fbd11ace718d4d918b473', label: '3-一般' },
  { id: '5c3ce92ff0479b46be0b697a2a', label: '4-轻微' },
];

// ── 飞书 ──────────────────────────────────────────────────────────────────────
async function getFeishuToken() {
  const config = JSON.parse(readFileSync(process.env.HOME + '/.openclaw/openclaw.json', 'utf8'));
  const feishu = config.channels?.feishu ?? config.integrations?.feishu ?? {};
  const res = await fetch(`${FEISHU_BASE}/auth/v3/tenant_access_token/internal`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ app_id: feishu.appId, app_secret: feishu.appSecret }),
  });
  const data = await res.json();
  return data.tenant_access_token;
}

async function sendCard(card, archiveMsgId = null, archiveLabel = '✅ 已完成') {
  const token = await getFeishuToken();
  if (archiveMsgId) {
    const archived = {
      config: { wide_screen_mode: true },
      header: { title: { tag: 'plain_text', content: archiveLabel }, template: 'grey' },
      elements: [{ tag: 'div', text: { tag: 'lark_md', content: '操作已完成，请查看下方卡片。' } }],
    };
    await fetch(`${FEISHU_BASE}/im/v1/messages/${archiveMsgId}`, {
      method: 'PATCH',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ content: JSON.stringify(archived) }),
    }).catch(() => {});
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

async function updateCard(msgId, card) {
  const token = await getFeishuToken();
  await fetch(`${FEISHU_BASE}/im/v1/messages/${msgId}`, {
    method: 'PATCH',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ content: JSON.stringify(card) }),
  });
}

// ── 云效 API ──────────────────────────────────────────────────────────────────
async function yunxiaoGet(path) {
  const res = await fetch(`${YUNXIAO_BASE}${path}`, {
    headers: { 'x-yunxiao-token': YUNXIAO_TOKEN },
  });
  return res.json();
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

// ── 状态文件 ──────────────────────────────────────────────────────────────────
const STATE_FILE = join(tmpdir(), 'create-workitem-state.json');
function loadState() { try { return JSON.parse(readFileSync(STATE_FILE, 'utf8')); } catch { return {}; } }
function saveState(s) { writeFileSync(STATE_FILE, JSON.stringify(s, null, 2)); }

// ── Step 1：发类型选择卡片 ─────────────────────────────────────────────────────
async function stepSelectType(projectId = DEFAULT_PROJECT_ID) {
  const allTypes = [...WORKITEM_TYPES.Bug, ...WORKITEM_TYPES.Req, ...WORKITEM_TYPES.Task];

  const card = {
    config: { wide_screen_mode: true },
    header: { title: { tag: 'plain_text', content: '📝 创建工作项' }, template: 'blue' },
    elements: [
      { tag: 'div', text: { tag: 'lark_md', content: `**项目：** ${DEFAULT_PROJECT_NAME}\n\n请选择要创建的工作项类型：` } },
      { tag: 'hr' },
      {
        tag: 'action',
        actions: allTypes.map(t => ({
          tag: 'button',
          text: { tag: 'plain_text', content: `${t.icon} ${t.name}` },
          type: 'default',
          value: { command: `CREATE_TYPE|${projectId}|${t.id}|${encodeURIComponent(t.name)}` },
        })),
      },
    ],
  };

  const msgId = await sendCard(card);
  saveState({ projectId, step: 'SELECT_TYPE', msgId });
  console.log(`✅ 已发送类型选择卡片 msgId=${msgId}`);
}

// ── Step 2：收到类型 → 发填写表单卡片 ─────────────────────────────────────────
async function stepFillForm(projectId, typeId, typeName, archiveMsgId) {
  const decodedName = decodeURIComponent(typeName);
  const isBug = WORKITEM_TYPES.Bug.some(t => t.id === typeId);

  // 查项目成员（用于负责人选项）
  let members = [];
  try {
    const res = await yunxiaoGet(`/projex/organizations/${ORG_ID}/projects/${projectId}/members`);
    members = Array.isArray(res) ? res.slice(0, 10) : [];
  } catch (e) {
    console.warn('查成员失败:', e.message);
  }

  const memberOptions = members.length > 0
    ? members.map(m => ({
        tag: 'option',
        text: { tag: 'plain_text', content: m.name || m.member?.name || '未知' },
        value: m.id || m.member?.id || '',
      }))
    : [{ tag: 'option', text: { tag: 'plain_text', content: '当前用户' }, value: USER_ID }];

  const priorityButtons = PRIORITY_OPTIONS.map(p => ({
    tag: 'button',
    text: { tag: 'plain_text', content: p.label },
    type: 'default',
    value: {
      command: `CREATE_PRIORITY|${projectId}|${typeId}|${encodeURIComponent(decodedName)}|${p.id}|${encodeURIComponent(p.label)}`,
    },
  }));

  const card = {
    config: { wide_screen_mode: true },
    header: { title: { tag: 'plain_text', content: `📝 创建${decodedName}` }, template: 'blue' },
    elements: [
      { tag: 'div', text: { tag: 'lark_md', content: '请选择优先级，然后告诉我标题和描述（直接回复消息即可）：' } },
      { tag: 'hr' },
      { tag: 'div', text: { tag: 'lark_md', content: '**优先级：**' } },
      { tag: 'action', actions: priorityButtons },
      ...(isBug ? [
        { tag: 'div', text: { tag: 'lark_md', content: '**严重程度（缺陷专用）：**' } },
        {
          tag: 'action',
          actions: SERIOUS_LEVEL_OPTIONS.map(s => ({
            tag: 'button',
            text: { tag: 'plain_text', content: s.label },
            type: 'default',
            value: {
              command: `CREATE_SERIOUS|${projectId}|${typeId}|${encodeURIComponent(decodedName)}|${s.id}|${encodeURIComponent(s.label)}`,
            },
          })),
        },
      ] : []),
      { tag: 'hr' },
      { tag: 'note', elements: [{ tag: 'lark_md', content: '选好优先级后，直接发消息告诉我标题（例如：`标题：登录页样式错误 描述：点击按钮没有反应`）' }] },
    ],
  };

  const msgId = await sendCard(card, archiveMsgId, '✅ 已选择类型');
  saveState({ projectId, typeId, typeName: decodedName, isBug, step: 'FILL_FORM', msgId, priority: PRIORITY_OPTIONS[2].id, priorityLabel: '中', seriousLevel: SERIOUS_LEVEL_OPTIONS[2].id });
  console.log(`✅ 已发送填写表单卡片 msgId=${msgId}`);
}

// ── Step 2b：更新优先级选择 ───────────────────────────────────────────────────
async function stepUpdatePriority(projectId, typeId, typeName, priorityId, priorityLabel) {
  const state = loadState();
  saveState({ ...state, priority: priorityId, priorityLabel: decodeURIComponent(priorityLabel) });

  // 更新卡片显示已选中
  const token = await getFeishuToken();
  const res = await fetch(`${FEISHU_BASE}/im/v1/messages?receive_id_type=open_id`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      receive_id: OPEN_ID, msg_type: 'interactive',
      content: JSON.stringify({
        config: { wide_screen_mode: true },
        header: { title: { tag: 'plain_text', content: `✅ 优先级已选：${decodeURIComponent(priorityLabel)}` }, template: 'green' },
        elements: [{ tag: 'div', text: { tag: 'lark_md', content: `现在告诉我工作项的标题（直接回复）：\n\n格式：\`标题：xxx 描述：xxx\`` } }],
      }),
    }),
  });
  const data = await res.json();
  saveState({ ...loadState(), notifyMsgId: data.data?.message_id });
  console.log(`✅ 优先级已更新为 ${decodeURIComponent(priorityLabel)}`);
}

// ── Step 2c：更新严重程度 ─────────────────────────────────────────────────────
async function stepUpdateSerious(projectId, typeId, typeName, seriousId, seriousLabel) {
  const state = loadState();
  saveState({ ...state, seriousLevel: seriousId, seriousLabel: decodeURIComponent(seriousLabel) });
  console.log(`✅ 严重程度已更新为 ${decodeURIComponent(seriousLabel)}`);
}

// ── Step 3：提交创建（由用户直接发标题触发）──────────────────────────────────
async function stepSubmit(subject, description = '') {
  const state = loadState();
  const { projectId, typeId, typeName, isBug, priority, seriousLevel } = state;

  if (!projectId || !typeId || !subject) {
    throw new Error('状态缺失，请重新开始创建流程');
  }

  const customFieldValues = {};
  if (priority) customFieldValues.priority = [priority];
  if (isBug && seriousLevel) customFieldValues.seriousLevel = [seriousLevel];

  const body = {
    spaceId: projectId,
    spaceType: 'Project',
    subject,
    workitemTypeId: typeId,
    assignedTo: USER_ID, // 默认分配给当前用户
    ...(description ? { description } : {}),
    customFieldValues: Object.keys(customFieldValues).length > 0 ? customFieldValues : undefined,
  };

  const result = await yunxiaoPost(`/projex/organizations/${ORG_ID}/workitems`, body);

  // GET 验证
  const verify = await yunxiaoGet(`/projex/organizations/${ORG_ID}/workitems/${result.id}`);

  const card = {
    config: { wide_screen_mode: true },
    header: { title: { tag: 'plain_text', content: `✅ ${typeName}已创建` }, template: 'green' },
    elements: [
      { tag: 'div', fields: [
        { is_short: true, text: { tag: 'lark_md', content: `**编号**\n${verify.serialNumber}` } },
        { is_short: true, text: { tag: 'lark_md', content: `**类型**\n${typeName}` } },
        { is_short: false, text: { tag: 'lark_md', content: `**标题**\n${subject}` } },
        { is_short: true, text: { tag: 'lark_md', content: `**状态**\n${verify.status?.displayName || '待确认'}` } },
        { is_short: true, text: { tag: 'lark_md', content: `**优先级**\n${state.priorityLabel || '中'}` } },
      ]},
      { tag: 'hr' },
      { tag: 'action', actions: [
        {
          tag: 'button',
          text: { tag: 'plain_text', content: '🔍 查看详情' },
          type: 'primary',
          value: { command: `WI_DETAIL|${result.id}` },
        },
        {
          tag: 'button',
          text: { tag: 'plain_text', content: '🐛 修复这个 Bug' },
          type: 'default',
          value: { command: `BUGFIX_START|${result.id}` },
        },
      ]},
    ],
  };

  const msgId = await sendCard(card, state.notifyMsgId || state.msgId, '✅ 创建完成');
  saveState({});
  console.log(`✅ 工作项已创建 id=${result.id} serial=${verify.serialNumber}`);
}

// ── CLI 入口 ──────────────────────────────────────────────────────────────────
const [,, cmd, ...rest] = process.argv;

if (!cmd || cmd === 'help') {
  console.log('用法: node create-workitem-flow.mjs [projectId]');
  console.log('     node create-workitem-flow.mjs callback "<payload>"');
  console.log('     node create-workitem-flow.mjs submit "标题" ["描述"]');
  process.exit(0);
}

if (cmd === 'callback') {
  const payload = rest[0] || '';
  const parts = payload.split('|');
  const action = parts[0];

  if (action === 'CREATE_TYPE') {
    const [, projectId, typeId, typeName] = parts;
    const state = loadState();
    await stepFillForm(projectId, typeId, typeName, state.msgId);
  } else if (action === 'CREATE_PRIORITY') {
    const [, projectId, typeId, typeName, priorityId, priorityLabel] = parts;
    await stepUpdatePriority(projectId, typeId, typeName, priorityId, priorityLabel);
  } else if (action === 'CREATE_SERIOUS') {
    const [, projectId, typeId, typeName, seriousId, seriousLabel] = parts;
    await stepUpdateSerious(projectId, typeId, typeName, seriousId, seriousLabel);
  } else if (action === 'WI_DETAIL') {
    const [, workitemId] = parts;
    execSync(`node ${import.meta.dirname}/workitem-card.mjs ${workitemId}`, { stdio: 'inherit' });
  } else if (action === 'BUGFIX_START') {
    const [, workitemId] = parts;
    execSync(`node ${import.meta.dirname}/bug-fix-flow.mjs ${workitemId}`, { stdio: 'inherit' });
  } else {
    console.error('未知 payload:', action);
  }
} else if (cmd === 'submit') {
  const subject = rest[0];
  const description = rest[1] || '';
  await stepSubmit(subject, description);
} else {
  // 默认：发类型选择卡片
  const projectId = cmd.length > 10 ? cmd : DEFAULT_PROJECT_ID;
  await stepSelectType(projectId);
}
