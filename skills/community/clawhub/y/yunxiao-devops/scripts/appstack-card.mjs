#!/usr/bin/env node
/**
 * appstack-card.mjs
 * 应用交付（AppStack）：查看应用列表、环境状态、工作流触发、部署单查看
 *
 * 用法：
 *   node appstack-card.mjs list                                      # 查应用列表
 *   node appstack-card.mjs app <appName>                             # 查应用详情+环境+工作流
 *   node appstack-card.mjs workflows <appName>                       # 查工作流列表
 *   node appstack-card.mjs callback "APP_DETAIL|appName"
 *   node appstack-card.mjs callback "APP_WORKFLOWS|appName"
 *   node appstack-card.mjs callback "APP_RUN_STAGE|appName|wfSn|stageSn|wfName|stageName"
 *   node appstack-card.mjs callback "APP_ORDERS|appName|envName"
 *   node appstack-card.mjs callback "APP_ORDER|appName||orderId"
 *
 * 环境变量覆盖（多组织支持）：
 *   YUNXIAO_ORG_ID=<orgId>   YUNXIAO_TOKEN=<token>
 *
 * ⚠️ API 踩坑（2026-03-18 验证）：
 *   - 应用和环境均用 name 字符串标识，无数字 id
 *   - 应用列表必须传 ?pagination=keyset&orderBy=id，否则 500
 *   - 部署单列表：POST /changeOrders/api，状态字段是 state 不是 status
 *   - 部署单详情：GET /apps/{appName}/changeOrders/{changeOrderSn}（用 changeOrderSn）
 *   - 触发工作流：POST .../releaseWorkflows/{wfSn}/releaseStages/{stageSn}:execute，body={params:{}}
 *   - 云效 URL：https://devops.aliyun.com/appstack/app/{appName}/workflow/{wfSn}/stage/{stageSn}
 */

import { readFileSync, existsSync } from 'fs';
import { spawn } from 'child_process';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { TOKEN, ORG_ID, OPEN_ID, requireConfig, YUNXIAO_TOKEN } from './config.mjs';

const __dir = dirname(fileURLToPath(import.meta.url));

requireConfig();

const YUNXIAO_BASE = 'https://openapi-rdc.aliyuncs.com/oapi/v1';
const FEISHU_BASE = 'https://open.feishu.cn/open-apis';

const POLL_SCRIPT = join(__dir, 'poll-appstack-stage.py');

// ── 飞书 ───────────────────────────────────────────────────────────────────────
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

// ── 云效 REST ──────────────────────────────────────────────────────────────────
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

// ── 常量 ───────────────────────────────────────────────────────────────────────
const ENV_STATUS_EMOJI = { NORMAL: '✅', ABNORMAL: '❌', UNKNOWN: '❓', LOCKED: '🔒', NEW: '🆕' };
const STATE_EMOJI = { SUCCESS: '✅', FAIL: '❌', RUNNING: '🔄', PAUSE: '⏸️', CANCEL: '⛔', WAIT: '⏳' };

// ── 应用列表 ──────────────────────────────────────────────────────────────────
async function showAppList() {
  let apps = [];
  try {
    const r = await yunxiaoGet(`/appstack/organizations/${ORG_ID}/apps:search?pagination=keyset&orderBy=id`);
    apps = r.data || r.apps || (Array.isArray(r) ? r : []);
  } catch (e) { console.error('查应用列表失败:', e.message); }

  if (apps.length === 0) {
    await sendCard({
      config: { wide_screen_mode: true },
      header: { title: { tag: 'plain_text', content: '📦 AppStack 应用列表' }, template: 'orange' },
      elements: [{ tag: 'div', text: { tag: 'lark_md', content: '暂无应用，或账户无访问权限。' } }],
    });
    return;
  }

  const appButtons = apps.slice(0, 8).map(a => ({
    tag: 'button',
    text: { tag: 'plain_text', content: a.name || a.appName || '未命名' },
    type: 'default',
    value: { command: `APP_DETAIL|${a.name || a.appName}` },
  }));

  const card = {
    config: { wide_screen_mode: true },
    header: { title: { tag: 'plain_text', content: `📦 应用列表（${apps.length}）` }, template: 'blue' },
    elements: [
      { tag: 'div', text: { tag: 'lark_md', content: apps.slice(0, 8).map(a => `• **${a.name || a.appName}** ${a.description?.slice(0, 30) || ''}`).join('\n') } },
      { tag: 'hr' },
      { tag: 'action', actions: appButtons },
    ],
  };
  const msgId = await sendCard(card);
  console.log(`✅ 应用列表已发送 msgId=${msgId} count=${apps.length}`);
}

// ── 应用详情 + 环境 + 工作流入口 ──────────────────────────────────────────────
async function showAppDetail(appId, updateMsgId = null) {
  let app = {}, envs = [];

  try { app = await yunxiaoGet(`/appstack/organizations/${ORG_ID}/apps/${appId}`); } catch (e) { console.error('查应用详情失败:', e.message); }
  try {
    const r = await yunxiaoGet(`/appstack/organizations/${ORG_ID}/apps/${appId}/envs?pagination=keyset&orderBy=id`);
    envs = r.data || r.envs || (Array.isArray(r) ? r : []);
  } catch (e) { console.error('查环境列表失败:', e.message); }

  const envFields = envs.slice(0, 6).map(env => ({
    is_short: true,
    text: { tag: 'lark_md', content: `**${env.name}**\n${ENV_STATUS_EMOJI[env.state || env.status] || '❓'} ${env.descriptiveName || env.name}` },
  }));

  const orderButtons = envs.slice(0, 5).map(env => ({
    tag: 'button',
    text: { tag: 'plain_text', content: `📋 ${env.name}` },
    type: 'default',
    value: { command: `APP_ORDERS|${appId}|${encodeURIComponent(env.name)}` },
  }));

  const card = {
    config: { wide_screen_mode: true },
    header: { title: { tag: 'plain_text', content: `📦 ${app.name || appId}` }, template: 'blue' },
    elements: [
      { tag: 'div', text: { tag: 'lark_md', content: app.description || '无描述' } },
      { tag: 'hr' },
      ...(envFields.length > 0 ? [
        { tag: 'div', text: { tag: 'lark_md', content: `**环境（${envs.length}）**` } },
        { tag: 'div', fields: envFields },
        { tag: 'hr' },
        { tag: 'div', text: { tag: 'lark_md', content: '**查看部署单：**' } },
        { tag: 'action', actions: orderButtons },
      ] : [
        { tag: 'div', text: { tag: 'lark_md', content: '暂无环境配置。' } },
      ]),
      { tag: 'hr' },
      { tag: 'action', actions: [
        { tag: 'button', text: { tag: 'plain_text', content: '▶ 运行工作流' }, type: 'primary',
          value: { command: `APP_WORKFLOWS|${appId}` } },
        { tag: 'button', text: { tag: 'plain_text', content: '← 应用列表' }, type: 'default',
          value: { command: 'APP_LIST|' } },
      ]},
    ],
  };

  const msgId = await sendCard(card, updateMsgId);
  if (!updateMsgId) console.log(`✅ 应用详情已发送 msgId=${msgId} envs=${envs.length}`);
}

// ── 工作流列表 ────────────────────────────────────────────────────────────────
async function showAppWorkflows(appName, updateMsgId = null) {
  let workflows = [];
  try {
    const r = await yunxiaoGet(`/appstack/organizations/${ORG_ID}/apps/${appName}/releaseWorkflows`);
    workflows = Array.isArray(r) ? r : (r.data || r.releaseWorkflows || []);
  } catch (e) { console.error('查工作流失败:', e.message); }

  if (workflows.length === 0) {
    await sendCard({
      config: { wide_screen_mode: true },
      header: { title: { tag: 'plain_text', content: `📦 ${appName} · 工作流` }, template: 'orange' },
      elements: [
        { tag: 'div', text: { tag: 'lark_md', content: '暂无工作流配置。' } },
        { tag: 'hr' },
        { tag: 'action', actions: [
          { tag: 'button', text: { tag: 'plain_text', content: `← ${appName}` }, type: 'default',
            value: { command: `APP_DETAIL|${appName}` } },
        ]},
      ],
    });
    return;
  }

  // 展开每个工作流的每个阶段为独立按钮
  const stageButtons = [];
  const lines = [];
  for (const wf of workflows) {
    lines.push(`**${wf.name}**`);
    for (const stage of (wf.releaseStages || [])) {
      lines.push(`　• ${stage.name}`);
      stageButtons.push({
        tag: 'button',
        text: { tag: 'plain_text', content: `▶ ${wf.name} · ${stage.name}` },
        type: stage.name?.includes('prod') || stage.name?.includes('生产') ? 'danger' : 'primary',
        value: {
          command: `APP_RUN_STAGE|${appName}|${wf.sn}|${stage.sn}|${encodeURIComponent(wf.name)}|${encodeURIComponent(stage.name)}`,
        },
      });
    }
  }

  const card = {
    config: { wide_screen_mode: true },
    header: { title: { tag: 'plain_text', content: `▶ ${appName} · 选择要运行的阶段` }, template: 'blue' },
    elements: [
      { tag: 'div', text: { tag: 'lark_md', content: lines.join('\n') } },
      { tag: 'hr' },
      // 每行最多 3 个按钮
      ...chunkArray(stageButtons, 3).map(group => ({ tag: 'action', actions: group })),
      { tag: 'hr' },
      { tag: 'action', actions: [
        { tag: 'button', text: { tag: 'plain_text', content: `← ${appName}` }, type: 'default',
          value: { command: `APP_DETAIL|${appName}` } },
      ]},
    ],
  };

  const msgId = await sendCard(card, updateMsgId);
  console.log(`✅ 工作流列表已发送 msgId=${msgId} workflows=${workflows.length}`);
}

function chunkArray(arr, size) {
  const result = [];
  for (let i = 0; i < arr.length; i += size) result.push(arr.slice(i, i + size));
  return result;
}

// ── 触发阶段 + 后台轮询 ───────────────────────────────────────────────────────
async function runStage(appName, wfSn, stageSn, wfName, stageName) {
  const stageUrl = `https://devops.aliyun.com/appstack/app/${appName}/workflow/${wfSn}/stage/${stageSn}`;
  let result;
  try {
    result = await yunxiaoPost(
      `/appstack/organizations/${ORG_ID}/apps/${appName}/releaseWorkflows/${wfSn}/releaseStages/${stageSn}:execute`,
      { params: {} }
    );
  } catch (e) {
    const errCard = {
      config: { wide_screen_mode: true },
      header: { title: { tag: 'plain_text', content: `❌ ${appName} · ${stageName} 触发失败` }, template: 'red' },
      elements: [
        { tag: 'div', text: { tag: 'lark_md', content: `**错误：** ${e.message}` } },
        { tag: 'hr' },
        { tag: 'action', actions: [
          { tag: 'button', text: { tag: 'plain_text', content: '↩ 重试', }, type: 'danger',
            value: { command: `APP_RUN_STAGE|${appName}|${wfSn}|${stageSn}|${encodeURIComponent(wfName)}|${encodeURIComponent(stageName)}` } },
        ]},
      ],
    };
    await sendCard(errCard);
    console.error('触发失败:', e.message);
    return;
  }

  const { object: execNum, pipelineId, pipelineRunId } = result;
  console.log(`触发成功 execNum=${execNum} pipelineId=${pipelineId} pipelineRunId=${pipelineRunId}`);

  // 发"已触发"卡片
  const triggerCard = {
    config: { wide_screen_mode: true },
    header: { title: { tag: 'plain_text', content: `🚀 ${appName} · ${wfName} · ${stageName} 已触发` }, template: 'green' },
    elements: [
      { tag: 'div', fields: [
        { is_short: true, text: { tag: 'lark_md', content: `**应用**\n${appName}` } },
        { is_short: true, text: { tag: 'lark_md', content: `**工作流**\n${wfName}` } },
        { is_short: true, text: { tag: 'lark_md', content: `**阶段**\n${stageName}` } },
        { is_short: true, text: { tag: 'lark_md', content: `**状态**\n🔄 运行中` } },
        { is_short: true, text: { tag: 'lark_md', content: `**流水线**\n#${pipelineId} Run #${pipelineRunId}` } },
        { is_short: true, text: { tag: 'lark_md', content: `**执行编号**\n#${execNum}` } },
      ]},
      { tag: 'hr' },
      { tag: 'action', actions: [
        { tag: 'button', text: { tag: 'plain_text', content: '🔗 查看云效' }, type: 'primary', url: stageUrl },
      ]},
    ],
  };
  await sendCard(triggerCard);

  // 后台启动轮询
  if (pipelineId && pipelineRunId && existsSync(POLL_SCRIPT)) {
    const pollEnv = { ...process.env, APPSTACK_PIPELINE_ID: String(pipelineId), APPSTACK_PIPELINE_RUN_ID: String(pipelineRunId) };
    const pollProc = spawn('python3', [POLL_SCRIPT, appName, wfSn, stageSn, String(execNum), stageName], {
      env: pollEnv,
      detached: true,
      stdio: 'ignore',
    });
    pollProc.unref();
    console.log(`✅ 轮询已后台启动 pid=${pollProc.pid}`);
  } else {
    console.warn('⚠️ 未能启动轮询（缺少 pipelineId/pipelineRunId 或 poll 脚本不存在）');
  }
}

// ── 部署单列表 ────────────────────────────────────────────────────────────────
async function showEnvOrders(appId, envName, updateMsgId = null) {
  let records = [], total = 0;
  try {
    const r = await yunxiaoPost(`/appstack/organizations/${ORG_ID}/apps/${appId}/changeOrders/api`, {
      pagination: 'keyset', orderBy: 'id', perPage: 8, envName: decodeURIComponent(envName),
    });
    records = r.records || [];
    total = r.total || 0;
  } catch (e) { console.error('查部署单失败:', e.message); }

  const elements = records.length > 0
    ? records.map(o => {
        const state = o.state || 'UNKNOWN';
        const ts = o.gmtCreate ? new Date(o.gmtCreate).toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' }).slice(0, 16) : '—';
        const source = o.source?.workflowName ? `${o.source.workflowName} · ${o.source.stageName}` : '';
        return { tag: 'div', text: { tag: 'lark_md', content: `${STATE_EMOJI[state] || '❓'} **${o.changeOrderName || o.name}**\n${ts}${source ? ' · ' + source : ''} · ${state}` } };
      })
    : [{ tag: 'div', text: { tag: 'lark_md', content: '该环境暂无部署记录。' } }];

  const card = {
    config: { wide_screen_mode: true },
    header: { title: { tag: 'plain_text', content: `📋 ${decodeURIComponent(envName)} 部署记录（共 ${total}）` }, template: 'blue' },
    elements: [
      ...elements,
      { tag: 'hr' },
      { tag: 'action', actions: [
        { tag: 'button', text: { tag: 'plain_text', content: `← ${appId}` }, type: 'default',
          value: { command: `APP_DETAIL|${appId}` } },
      ]},
    ],
  };

  const msgId = await sendCard(card, updateMsgId);
  console.log(`✅ 部署单列表发送 msgId=${msgId} count=${records.length}`);
}

// ── 部署单详情 ────────────────────────────────────────────────────────────────
async function showOrderStatus(appId, orderId) {
  let order = {};
  try {
    order = await yunxiaoGet(`/appstack/organizations/${ORG_ID}/apps/${appId}/changeOrders/${orderId}`);
  } catch (e) { console.error('查部署单失败:', e.message); }

  const state = order.state || order.status || 'UNKNOWN';
  await sendCard({
    config: { wide_screen_mode: true },
    header: {
      title: { tag: 'plain_text', content: `${STATE_EMOJI[state] || '❓'} 部署单 ${orderId}` },
      template: state === 'SUCCESS' ? 'green' : state === 'FAIL' ? 'red' : 'blue',
    },
    elements: [
      { tag: 'div', fields: [
        { is_short: true, text: { tag: 'lark_md', content: `**状态**\n${state}` } },
        { is_short: true, text: { tag: 'lark_md', content: `**环境**\n${order.envName || '—'}` } },
        { is_short: true, text: { tag: 'lark_md', content: `**修改时间**\n${order.gmtModified ? new Date(order.gmtModified).toLocaleString('zh-CN', {timeZone:'Asia/Shanghai'}).slice(0,16) : '—'}` } },
      ]},
    ],
  });
  console.log(`✅ 部署单状态 orderId=${orderId} state=${state}`);
}

// ── 路由 ──────────────────────────────────────────────────────────────────────
const [,, cmd, ...rest] = process.argv;

if (cmd === 'list' || !cmd) {
  await showAppList();
} else if (cmd === 'app') {
  await showAppDetail(rest[0]);
} else if (cmd === 'workflows') {
  await showAppWorkflows(rest[0]);
} else if (cmd === 'callback') {
  const parts = (rest[0] || '').split('|');
  const action = parts[0];
  if (action === 'APP_DETAIL') {
    await showAppDetail(parts[1]);
  } else if (action === 'APP_LIST') {
    await showAppList();
  } else if (action === 'APP_WORKFLOWS') {
    await showAppWorkflows(parts[1]);
  } else if (action === 'APP_RUN_STAGE') {
    const [, appName, wfSn, stageSn, wfNameEnc, stageNameEnc] = parts;
    await runStage(appName, wfSn, stageSn, decodeURIComponent(wfNameEnc || ''), decodeURIComponent(stageNameEnc || ''));
  } else if (action === 'APP_ORDERS') {
    await showEnvOrders(parts[1], parts[2]);
  } else if (action === 'APP_ORDER') {
    await showOrderStatus(parts[1], parts[3]);  // parts[2] 是废弃的 envId
  } else {
    console.log('未知 callback action:', action);
  }
}
