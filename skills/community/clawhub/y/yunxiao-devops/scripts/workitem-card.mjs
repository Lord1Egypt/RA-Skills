/**
 * workitem-card.mjs
 * 获取云效工作项详情，以飞书交互卡片形式展示，支持点击按钮变更状态。
 *
 * 用法：
 *   node workitem-card.mjs <workitemId>
 *
 * Card payload 回调格式：
 *   WI_STATUS_CHANGE|<workitemId>|<newStatusId>|<newStatusName>
 *
 * agent 收到该 payload 后：
 *   node workitem-card.mjs change-status <workitemId> <newStatusId> <newStatusName>
 */

import { readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { homedir } from 'os';
import { TOKEN, ORG_ID, OPEN_ID, requireConfig } from './config.mjs';

requireConfig();

const __dir = dirname(fileURLToPath(import.meta.url));

function loadWorkflowConfig() {
  try {
    return JSON.parse(readFileSync(join(__dir, '../references/workflow-transitions.json'), 'utf8'));
  } catch { return { projects: {}, workflows: {} }; }
}

const YUNXIAO_BASE = 'https://openapi-rdc.aliyuncs.com/oapi/v1/projex';
const FEISHU_BASE = 'https://open.feishu.cn/open-apis';

// ── 云效 API ───────────────────────────────────────────────────────────────────
async function yunxiaoGet(path) {
  const res = await fetch(`${YUNXIAO_BASE}${path}`, {
    headers: { 'x-yunxiao-token': TOKEN },
  });
  return res.json();
}

async function getWorkitem(workitemId) {
  return yunxiaoGet(`/organizations/${ORG_ID}/workitems/${workitemId}`);
}

async function getWorkflow(projectId, workitemTypeId) {
  return yunxiaoGet(`/organizations/${ORG_ID}/projects/${projectId}/workitemTypes/${workitemTypeId}/workflows`);
}

// 从 workflow-transitions.json 里查当前状态可以流转到哪些状态
// 优先从本地缓存读，没有缓存则降级到全量（排除当前状态）
function getNextStatuses(workflowId, currentStatusId, allStatuses) {
  const cfg = loadWorkflowConfig();
  const wf = cfg.workflows?.[workflowId];
  if (!wf?.transitions) return null; // 无缓存，降级
  const nextIds = wf.transitions[String(currentStatusId)] ?? [];
  // 用缓存里的 displayName，比 API 返回更准确
  return nextIds.map(id => {
    const cached = wf.statuses?.[id];
    // 优先用 API 返回的对象（有完整数据），回退到缓存
    const fromApi = allStatuses.find(s => String(s.id) === String(id));
    return fromApi ?? { id, displayName: cached?.displayName ?? id, name: cached?.displayName ?? id };
  });
}

async function getComments(workitemId) {
  const data = await yunxiaoGet(`/organizations/${ORG_ID}/workitems/${workitemId}/comments`);
  return Array.isArray(data) ? data : [];
}

async function changeStatus(workitemId, statusId) {
  const res = await fetch(`${YUNXIAO_BASE}/organizations/${ORG_ID}/workitems/${workitemId}`, {
    method: 'PUT',
    headers: { 'x-yunxiao-token': TOKEN, 'Content-Type': 'application/json' },
    body: JSON.stringify({ status: statusId }),
  });
  return res.status;
}

// ── 飞书 API ───────────────────────────────────────────────────────────────────
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

async function sendCard(token, card, messageId = null) {
  if (messageId) {
    // PATCH 更新已有卡片
    const res = await fetch(`${FEISHU_BASE}/im/v1/messages/${messageId}`, {
      method: 'PATCH',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ content: JSON.stringify(card) }),
    });
    return res.json();
  }
  const res = await fetch(`${FEISHU_BASE}/im/v1/messages?receive_id_type=open_id`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ receive_id: OPEN_ID, msg_type: 'interactive', content: JSON.stringify(card) }),
  });
  const data = await res.json();
  if (data.code !== 0) throw new Error(`Send error: ${data.msg} (code=${data.code})`);
  return data.data?.message_id;
}

// ── 工具函数 ───────────────────────────────────────────────────────────────────
function formatTime(ms) {
  if (!ms) return '--';
  return new Date(ms).toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai', hour12: false });
}

function getCustomField(item, fieldId) {
  const f = (item.customFieldValues || []).find(f => f.fieldId === fieldId);
  return f?.values?.[0]?.displayValue ?? '--';
}

const STATUS_EMOJI = {
  '待确认': '⏳', '处理中': '🔄', '已修复': '✅',
  '再次打开': '🔁', '暂不修复': '🚫', '已关闭': '🔒',
  '待处理': '📋', '进行中': '🔄', '已完成': '✅', '已取消': '❌',
};

const TYPE_COLOR = { Bug: 'red', Task: 'blue', Req: 'green' };

// ── 卡片构建 ───────────────────────────────────────────────────────────────────
function buildWorkitemCard(item, statuses, comments, workflowId = null) {
  const status = item.status?.displayName ?? '--';
  const statusEmoji = STATUS_EMOJI[status] ?? '•';
  const typeId = item.categoryId ?? item.workitemType?.name ?? 'Task';
  const headerColor = TYPE_COLOR[typeId] ?? 'blue';

  const priority = getCustomField(item, 'priority');
  const seriousLevel = getCustomField(item, 'seriousLevel');

  const priorityEmoji = { '紧急': '🔴', '高': '🟠', '中': '🟡', '低': '🟢' }[priority] ?? '⚪';
  const assignedTo = item.assignedTo?.name ?? '--';

  // 评论文本（最多3条，最新在前）
  const commentLines = comments.length === 0
    ? '暂无评论'
    : comments.slice(-3).reverse().map(c => {
        const t = formatTime(c.gmtCreate);
        const author = c.user?.name ?? c.creator?.name ?? c.operator?.name ?? '未知';
        // 评论内容可能是纯文本、HTML 或 JSON 结构体
        let raw = c.content ?? c.commentContent ?? '';
        let text = raw;
        try {
          const parsed = JSON.parse(raw);
          // 优先取 htmlValue，再取 markdownValue，再取 jsonMLValue 里的文字
          text = parsed.htmlValue ?? parsed.markdownValue ?? raw;
        } catch { /* 不是 JSON，直接用原字符串 */ }
        text = text.replace(/<[^>]+>/g, '').trim().slice(0, 100);
        return `**${author}** (${t})\n${text || '(空)'}`;
      }).join('\n\n');

  // 可用的状态变更按钮：优先用 transitions，没有则降级全量排除当前
  const rawNext = workflowId
    ? getNextStatuses(workflowId, item.status?.id, statuses || [])
    : null;
  const nextStatuses = (rawNext ?? (statuses || []).filter(s => s.id !== String(item.status?.id))).slice(0, 4);

  const statusButtons = nextStatuses.map((s, i) => ({
    tag: 'button',
    text: { tag: 'plain_text', content: `${STATUS_EMOJI[s.displayName] ?? '•'} ${s.displayName}` },
    type: i === 0 ? 'primary' : 'default',
    value: {
      command: `WI_STATUS_CHANGE|${item.id}|${s.id}|${s.displayName}`,
    },
  }));

  const yunxiaoUrl = `https://devops.aliyun.com/projex/project/${item.space?.id}/workitem#openWorkitemIdentifier=${item.id}`;

  return {
    config: { wide_screen_mode: true },
    header: {
      title: {
        tag: 'plain_text',
        content: `${statusEmoji} [${item.serialNumber ?? item.id.slice(0, 8)}] ${item.subject}`,
      },
      template: headerColor,
    },
    elements: [
      // 基本信息字段
      {
        tag: 'div',
        fields: [
          { is_short: true, text: { tag: 'lark_md', content: `**项目**\n${item.space?.name ?? '--'}` } },
          { is_short: true, text: { tag: 'lark_md', content: `**类型**\n${item.workitemType?.name ?? '--'}` } },
          { is_short: true, text: { tag: 'lark_md', content: `**状态**\n${statusEmoji} ${status}` } },
          { is_short: true, text: { tag: 'lark_md', content: `**负责人**\n${assignedTo}` } },
          { is_short: true, text: { tag: 'lark_md', content: `**优先级**\n${priorityEmoji} ${priority}` } },
          ...(typeId === 'Bug'
            ? [{ is_short: true, text: { tag: 'lark_md', content: `**严重程度**\n${seriousLevel}` } }]
            : []),
          { is_short: true, text: { tag: 'lark_md', content: `**创建时间**\n${formatTime(item.gmtCreate)}` } },
          { is_short: true, text: { tag: 'lark_md', content: `**最后更新**\n${formatTime(item.gmtModified)}` } },
        ],
      },
      // 描述
      ...(item.description ? [{
        tag: 'div',
        text: {
          tag: 'lark_md',
          content: `**描述**\n${item.description.replace(/<[^>]+>/g, '').slice(0, 200)}`,
        },
      }] : []),
      { tag: 'hr' },
      // 评论
      {
        tag: 'div',
        text: { tag: 'lark_md', content: `**评论（最新3条）**\n${commentLines}` },
      },
      { tag: 'hr' },
      // 状态变更按钮
      ...(statusButtons.length > 0 ? [{
        tag: 'div',
        text: { tag: 'lark_md', content: '**变更状态**' },
      }, {
        tag: 'action',
        actions: statusButtons,
      }] : []),
      // 云效链接
      {
        tag: 'note',
        elements: [{
          tag: 'lark_md',
          content: `[在云效中查看 ↗](${yunxiaoUrl})`,
        }],
      },
    ],
  };
}

// ── CLI 入口 ───────────────────────────────────────────────────────────────────
const [,, cmd, ...rest] = process.argv;

if (cmd === 'change-status') {
  // node workitem-card.mjs change-status <workitemId> <statusId> <statusName> [messageId]
  const [workitemId, statusId, statusName, messageId] = rest;
  if (!workitemId || !statusId) {
    console.error('Usage: node workitem-card.mjs change-status <workitemId> <statusId> <statusName> [messageId]');
    process.exit(1);
  }
  const httpStatus = await changeStatus(workitemId, statusId);
  console.log(`[status] PUT ${httpStatus}`);

  // 重新拉取工作项并刷新卡片（workflow 依赖 item，需要串行）
  const item = await getWorkitem(workitemId);
  const [wf, comments] = await Promise.all([
    getWorkflow(item.space?.id, item.workitemType?.id).catch(() => ({ statuses: [], id: null })),
    getComments(workitemId),
  ]);
  const cfgWorkflowId2 = loadWorkflowConfig()
    .projects?.[item.space?.id]
    ?.workitemTypes?.[item.workitemType?.id]
    ?.workflowId ?? null;
  const workflowId2 = wf.id ?? cfgWorkflowId2;
  const card = buildWorkitemCard(item, wf.statuses ?? [], comments, workflowId2);
  const token = await getFeishuToken();
  if (messageId) {
    await sendCard(token, card, messageId);
    console.log(`✅ 状态已变更为「${statusName}」，卡片已刷新`);
  } else {
    const newMsgId = await sendCard(token, card);
    console.log(`✅ 状态已变更为「${statusName}」，新卡片 id=${newMsgId}`);
  }

} else {
  // node workitem-card.mjs <workitemId>
  const workitemId = cmd;
  if (!workitemId) {
    console.error('Usage: node workitem-card.mjs <workitemId>');
    process.exit(1);
  }
  const item = await getWorkitem(workitemId);
  const [wf, comments] = await Promise.all([
    getWorkflow(item.space?.id, item.workitemType?.id).catch(() => ({ statuses: [], id: null })),
    getComments(workitemId),
  ]);
  // workflowId 优先用 API 返回，其次从本地配置查
  const cfg = loadWorkflowConfig();
  const cfgWorkflowId = cfg.projects?.[item.space?.id]
    ?.workitemTypes?.[item.workitemType?.id]
    ?.workflowId ?? null;
  const workflowId = wf.id ?? cfgWorkflowId;

  // 如果 workflowId 有了但 transitions 还没缓存，提示用户补录
  if (workflowId && !cfg.workflows?.[workflowId]?.transitions) {
    console.warn(`\n⚠️  工作流 ${workflowId} 的 transitions 尚未缓存。`);
    console.warn(`请在浏览器访问以下链接并将返回 JSON 发给我：`);
    console.warn(`https://devops.aliyun.com/projex/api/workitem/workitem/workflow/getActions/${workflowId}?spaceType=Project&spaceIdentifier=${item.space?.id}&_input_charset=utf-8\n`);
  }

  const card = buildWorkitemCard(item, wf.statuses ?? [], comments, workflowId);
  const token = await getFeishuToken();
  const msgId = await sendCard(token, card);
  console.log(`✅ 工作项卡片已发送 message_id=${msgId}`);
}
