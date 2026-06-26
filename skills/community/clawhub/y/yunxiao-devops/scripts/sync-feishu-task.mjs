/**
 * sync-feishu-task.mjs
 * 云效工作项创建后，同步在飞书给对应负责人创建关联任务。
 *
 * 用法：
 *   node sync-feishu-task.mjs \
 *     --title "工作项标题" \
 *     --assignee "云效userId" \
 *     --url "https://devops.aliyun.com/projex/..." \
 *     [--due "2026-04-01"] \
 *     [--workitem-id "xxx"]
 *
 * 找不到映射时静默跳过（exit 0），不报错，不影响主流程。
 */

import { readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { homedir } from 'os';

const __dir = dirname(fileURLToPath(import.meta.url));
const MAPPING_FILE = join(__dir, '../references/user-mapping.json');
const API_BASE = 'https://open.feishu.cn/open-apis';

// ── 读配置 ─────────────────────────────────────────────────────────────────────
const config = JSON.parse(readFileSync(join(homedir(), '.openclaw', 'openclaw.json'), 'utf8'));
const APP_ID = config.channels?.feishu?.appId;
const APP_SECRET = config.channels?.feishu?.appSecret;

// ── 读映射表 ───────────────────────────────────────────────────────────────────
function loadMapping() {
  try {
    const raw = JSON.parse(readFileSync(MAPPING_FILE, 'utf8'));
    // 过滤掉以 _ 开头的注释字段
    return Object.fromEntries(Object.entries(raw).filter(([k]) => !k.startsWith('_')));
  } catch {
    return {};
  }
}

// ── 飞书 Token ─────────────────────────────────────────────────────────────────
async function getTenantToken() {
  const res = await fetch(`${API_BASE}/auth/v3/tenant_access_token/internal`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ app_id: APP_ID, app_secret: APP_SECRET }),
  });
  const data = await res.json();
  if (data.code !== 0) throw new Error(`Token error: ${data.msg}`);
  return data.tenant_access_token;
}

// ── 创建飞书任务 ───────────────────────────────────────────────────────────────
async function createFeishuTask({ title, feishuOpenId, yunxiaoUrl, workitemId, due }) {
  const token = await getTenantToken();

  const description = yunxiaoUrl
    ? `云效工作项：${yunxiaoUrl}${workitemId ? `\nID: ${workitemId}` : ''}`
    : (workitemId ? `云效工作项 ID: ${workitemId}` : '');

  const body = {
    summary: `[云效] ${title}`,
    description,
    members: [
      { id: feishuOpenId, role: 'assignee', type: 'user' },
    ],
  };

  if (due) {
    // due 支持 YYYY-MM-DD 格式或时间戳（ms）
    const ts = isNaN(Number(due))
      ? String(new Date(due).getTime())
      : String(due);
    body.due = { timestamp: ts, is_all_day: true };
  }

  const res = await fetch(`${API_BASE}/task/v2/tasks`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  if (data.code !== 0) throw new Error(`Task API error ${data.code}: ${data.msg}`);
  return data.data?.task?.guid ?? data.data?.task?.id ?? '(unknown id)';
}

// ── CLI 入口 ───────────────────────────────────────────────────────────────────
const args = process.argv.slice(2);
function getArg(name) {
  const idx = args.indexOf(`--${name}`);
  return idx !== -1 ? args[idx + 1] : null;
}

const title      = getArg('title');
const assigneeId = getArg('assignee');
const url        = getArg('url');
const due        = getArg('due');
const workitemId = getArg('workitem-id');

if (!title || !assigneeId) {
  console.error('Usage: node sync-feishu-task.mjs --title "..." --assignee "<yunxiao-userId>" [--url "..."] [--due "YYYY-MM-DD"] [--workitem-id "..."]');
  process.exit(1);
}

const mapping = loadMapping();
const feishuOpenId = mapping[assigneeId];

if (!feishuOpenId) {
  console.log(`[skip] 云效用户 ${assigneeId} 没有飞书映射，跳过。`);
  process.exit(0);
}

try {
  const taskId = await createFeishuTask({ title, feishuOpenId, yunxiaoUrl: url, workitemId, due });
  console.log(`✅ 飞书任务已创建 id=${taskId} → 负责人 open_id=${feishuOpenId}`);
} catch (err) {
  // 失败也只是警告，不 exit 1，保证不影响主流程
  console.warn(`⚠️  飞书任务创建失败（不影响主流程）: ${err.message}`);
}
