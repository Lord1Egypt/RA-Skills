#!/usr/bin/env node
/**
 * pipeline-log-card.mjs
 * 流水线失败日志快查：不登录网页，飞书直接看最后 N 行日志
 *
 * 用法：
 *   node pipeline-log-card.mjs [pipelineId] [runId]   # 查最近一次 run 的失败 job 日志
 *   node pipeline-log-card.mjs callback "PIPE_LOG|pipelineId|runId|jobId"
 */

import { readFileSync } from 'fs';
import { TOKEN, ORG_ID, OPEN_ID, requireConfig, YUNXIAO_TOKEN } from './config.mjs';

requireConfig();

const YUNXIAO_BASE = 'https://openapi-rdc.aliyuncs.com/oapi/v1';
const FEISHU_BASE = 'https://open.feishu.cn/open-apis';

// 在此填入你的流水线 ID，或留空由脚本动态从 API 查询
// 格式：{ id: <number>, name: '<display-name>' }
const KNOWN_PIPELINES = [];

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

async function yunxiaoGet(path) {
  const r = await fetch(`${YUNXIAO_BASE}${path}`, { headers: { 'x-yunxiao-token': YUNXIAO_TOKEN } });
  const d = await r.json();
  if (d.errorCode) throw new Error(d.errorMessage);
  return d;
}

const STATUS_EMOJI = {
  SUCCESS: '✅', FAIL: '❌', RUNNING: '🔄', CANCELED: '⏸️', WAITING: '⏳',
};

async function showPipelineLog(pipelineId, runId) {
  // 如果没有 runId，查最近一次
  if (!runId) {
    try {
      const latest = await yunxiaoGet(`/flow/organizations/${ORG_ID}/pipelines/${pipelineId}/runs?page=1&perPage=1`);
      const runs = latest.pipelineRuns || latest.runs || (Array.isArray(latest) ? latest : []);
      runId = runs[0]?.pipelineRunId || runs[0]?.id;
    } catch (e) {
      console.error('获取最近 run 失败:', e.message);
    }
  }

  if (!runId) {
    await sendCard({
      config: { wide_screen_mode: true },
      header: { title: { tag: 'plain_text', content: '❓ 找不到流水线运行记录' }, template: 'orange' },
      elements: [{ tag: 'div', text: { tag: 'lark_md', content: '该流水线暂无运行记录。' } }],
    });
    return;
  }

  // 查 run 详情
  let run = {};
  try {
    run = await yunxiaoGet(`/flow/organizations/${ORG_ID}/pipelines/${pipelineId}/runs/${runId}`);
  } catch {}

  // 查 job 列表
  let jobs = [];
  try {
    const r = await yunxiaoGet(`/flow/organizations/${ORG_ID}/pipelines/${pipelineId}/runs/${runId}/jobs`);
    jobs = Array.isArray(r) ? r : (r.pipelineJobs || r.jobs || []);
  } catch {}

  const failedJobs = jobs.filter(j => j.status === 'FAIL' || j.result === 'FAIL');
  const runStatus = run.status || 'UNKNOWN';

  // 查失败 job 的日志
  let logContent = '';
  let logJobName = '';
  if (failedJobs.length > 0) {
    const job = failedJobs[0];
    logJobName = job.name || job.jobName || `Job ${job.id}`;
    try {
      const logRes = await yunxiaoGet(
        `/flow/organizations/${ORG_ID}/pipelines/${pipelineId}/runs/${runId}/jobs/${job.id || job.pipelineRunJobId}/log`
      );
      const rawLog = logRes.content || logRes.log || logRes.data || '';
      const lines = rawLog.split('\n').filter(Boolean);
      logContent = lines.slice(-30).join('\n');
    } catch {}
  }

  const jobLines = jobs.slice(0, 8).map(j => {
    const emoji = STATUS_EMOJI[j.status || j.result] || '❓';
    return `${emoji} ${j.name || j.jobName || 'Job'} (${j.status || '—'})`;
  }).join('\n');

  const pipelineName = KNOWN_PIPELINES.find(p => String(p.id) === String(pipelineId))?.name || `Pipeline ${pipelineId}`;

  const elements = [
    { tag: 'div', fields: [
      { is_short: true, text: { tag: 'lark_md', content: `**流水线**\n${pipelineName}` } },
      { is_short: true, text: { tag: 'lark_md', content: `**状态**\n${STATUS_EMOJI[runStatus] || '—'} ${runStatus}` } },
      { is_short: true, text: { tag: 'lark_md', content: `**Run ID**\n${runId}` } },
      { is_short: true, text: { tag: 'lark_md', content: `**触发时间**\n${run.startTime?.slice(5, 16) || '—'}` } },
    ]},
    { tag: 'hr' },
    { tag: 'div', text: { tag: 'lark_md', content: `**各阶段状态**\n${jobLines || '—'}` } },
  ];

  if (logContent && failedJobs.length > 0) {
    elements.push({ tag: 'hr' });
    elements.push({ tag: 'div', text: { tag: 'lark_md', content: `**❌ 失败 Job 最后 30 行日志：** \`${logJobName}\`\n\`\`\`\n${logContent.slice(-2000)}\n\`\`\`` } });
  } else if (runStatus === 'SUCCESS') {
    elements.push({ tag: 'div', text: { tag: 'lark_md', content: '✅ 所有 Job 执行成功，无失败日志。' } });
  }

  // 其他流水线切换按钮
  const switchButtons = KNOWN_PIPELINES.map(p => ({
    tag: 'button',
    text: { tag: 'plain_text', content: p.name },
    type: String(p.id) === String(pipelineId) ? 'primary' : 'default',
    value: { command: `PIPE_LOG|${p.id}|` },
  }));
  elements.push({ tag: 'hr' });
  elements.push({ tag: 'div', text: { tag: 'lark_md', content: '**切换流水线：**' } });
  elements.push({ tag: 'action', actions: switchButtons });

  const msgId = await sendCard({
    config: { wide_screen_mode: true },
    header: {
      title: { tag: 'plain_text', content: `🔍 流水线日志 · ${pipelineName}` },
      template: runStatus === 'SUCCESS' ? 'green' : runStatus === 'FAIL' ? 'red' : 'blue',
    },
    elements,
  });
  console.log(`✅ 日志卡片已发送 msgId=${msgId} status=${runStatus} failedJobs=${failedJobs.length}`);
}

const [,, cmd, ...rest] = process.argv;

if (cmd === 'callback') {
  const parts = (rest[0] || '').split('|');
  if (parts[0] === 'PIPE_LOG') {
    const [, pipelineId, runId] = parts;
    await showPipelineLog(pipelineId, runId || null);
  }
} else {
  const pipelineId = cmd || KNOWN_PIPELINES[0].id;
  const runId = rest[0] || null;
  await showPipelineLog(pipelineId, runId);
}
