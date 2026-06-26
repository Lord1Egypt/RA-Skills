#!/usr/bin/env node
/**
 * testcase-card.mjs
 * 测试用例管理：查看/创建/更新测试用例，查看测试计划结果
 *
 * 用法：
 *   node testcase-card.mjs list [projectId]             # 查测试用例列表
 *   node testcase-card.mjs plan [projectId]             # 查测试计划列表
 *   node testcase-card.mjs create <title> [projectId]  # 创建测试用例
 *   node testcase-card.mjs callback "TC_DETAIL|caseId|projectId"
 *   node testcase-card.mjs callback "TC_PLAN|planId|projectId"
 */

import { readFileSync } from 'fs';
import { TOKEN, ORG_ID, OPEN_ID, requireConfig, YUNXIAO_TOKEN, DEFAULT_PROJECT_ID } from './config.mjs';

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

const RESULT_EMOJI = {
  PASS: '✅', FAIL: '❌', BLOCKED: '🚫', SKIP: '⏭️', UNEXECUTED: '⬜',
};

// 查测试用例列表
async function showTestcaseList(projectId) {
  let cases = [];
  try {
    const r = await yunxiaoPost(`/testhub/organizations/${ORG_ID}/projects/${projectId}/testcases:search`, {
      page: 1, perPage: 20,
    });
    cases = r.testcases || r.data || [];
  } catch (e) {
    console.error('查测试用例失败:', e.message);
  }

  const caseLines = cases.slice(0, 10).map(c =>
    `• [${c.identifier || c.id?.slice(0, 8)}] ${c.subject || c.title || '未命名'} (${c.status || '—'})`
  ).join('\n');

  const card = {
    config: { wide_screen_mode: true },
    header: { title: { tag: 'plain_text', content: `🧪 测试用例（${cases.length}）` }, template: 'blue' },
    elements: [
      { tag: 'div', text: { tag: 'lark_md', content: caseLines || '暂无测试用例' } },
      { tag: 'hr' },
      { tag: 'action', actions: [
        { tag: 'button', text: { tag: 'plain_text', content: '📋 查看测试计划' }, type: 'default',
          value: { command: `TC_PLANS|${projectId}` } },
        { tag: 'button', text: { tag: 'plain_text', content: '➕ 创建用例' }, type: 'primary',
          value: { command: `TC_CREATE_START|${projectId}` } },
      ]},
    ],
  };
  const msgId = await sendCard(card);
  console.log(`✅ 测试用例列表已发送 msgId=${msgId} count=${cases.length}`);
}

// 查测试计划列表
async function showTestPlanList(projectId) {
  let plans = [];
  try {
    const r = await yunxiaoGet(`/testhub/organizations/${ORG_ID}/projects/${projectId}/testplans?page=1&perPage=10`);
    plans = Array.isArray(r) ? r : (r.testPlans || r.data || []);
  } catch (e) {
    console.error('查测试计划失败:', e.message);
  }

  const planLines = plans.map(p =>
    `• **${p.name || p.planName || '未命名'}** (${p.status || '—'})`
  ).join('\n');

  const card = {
    config: { wide_screen_mode: true },
    header: { title: { tag: 'plain_text', content: `📋 测试计划（${plans.length}）` }, template: 'blue' },
    elements: [
      { tag: 'div', text: { tag: 'lark_md', content: planLines || '暂无测试计划' } },
      ...(plans.length > 0 ? [
        { tag: 'hr' },
        { tag: 'action', actions: plans.slice(0, 5).map(p => ({
          tag: 'button',
          text: { tag: 'plain_text', content: p.name || p.planName || '计划' },
          type: 'default',
          value: { command: `TC_PLAN|${p.planId || p.id}|${projectId}` },
        }))},
      ] : []),
    ],
  };
  const msgId = await sendCard(card);
  console.log(`✅ 测试计划列表已发送 msgId=${msgId} count=${plans.length}`);
}

// 查测试计划执行结果
async function showTestPlanResult(planId, projectId) {
  let results = [];
  let passCount = 0, failCount = 0, totalCount = 0;
  try {
    const r = await yunxiaoGet(`/testhub/organizations/${ORG_ID}/projects/${projectId}/testplans/${planId}/testcases?page=1&perPage=50`);
    results = Array.isArray(r) ? r : (r.testcases || r.testResults || []);
    passCount = results.filter(t => t.result === 'PASS' || t.status === 'PASS').length;
    failCount = results.filter(t => t.result === 'FAIL' || t.status === 'FAIL').length;
    totalCount = results.length;
  } catch (e) {
    console.error('查测试结果失败:', e.message);
  }

  const pct = totalCount > 0 ? Math.round((passCount / totalCount) * 100) : 0;
  const resultLines = results.slice(0, 10).map(t => {
    const status = t.result || t.status || 'UNEXECUTED';
    const emoji = RESULT_EMOJI[status] || '❓';
    const name = t.subject || t.title || t.caseName || '未命名';
    return `${emoji} ${name.slice(0, 50)}`;
  }).join('\n');

  const card = {
    config: { wide_screen_mode: true },
    header: {
      title: { tag: 'plain_text', content: `🧪 测试计划结果` },
      template: pct === 100 ? 'green' : failCount > 0 ? 'red' : 'blue',
    },
    elements: [
      { tag: 'div', fields: [
        { is_short: true, text: { tag: 'lark_md', content: `**通过**\n✅ ${passCount}` } },
        { is_short: true, text: { tag: 'lark_md', content: `**失败**\n❌ ${failCount}` } },
        { is_short: true, text: { tag: 'lark_md', content: `**合计**\n${totalCount}` } },
        { is_short: true, text: { tag: 'lark_md', content: `**通过率**\n${pct}%` } },
      ]},
      { tag: 'hr' },
      { tag: 'div', text: { tag: 'lark_md', content: `**用例执行详情：**\n${resultLines || '暂无执行记录'}` } },
    ],
  };
  const msgId = await sendCard(card);
  console.log(`✅ 测试结果已发送 msgId=${msgId} pass=${passCount}/${totalCount}`);
}

// 创建测试用例
async function createTestcase(title, projectId) {
  try {
    const result = await yunxiaoPost(`/testhub/organizations/${ORG_ID}/projects/${projectId}/testcases`, {
      subject: title,
      priority: 2, // 中等优先级
    });

    // GET 验证
    let verified = false;
    try {
      const verify = await yunxiaoGet(`/testhub/organizations/${ORG_ID}/projects/${projectId}/testcases/${result.id}`);
      verified = verify.id === result.id;
    } catch {}

    await sendCard({
      config: { wide_screen_mode: true },
      header: { title: { tag: 'plain_text', content: verified ? '✅ 测试用例已创建' : '⚠️ 请确认创建结果' }, template: verified ? 'green' : 'orange' },
      elements: [
        { tag: 'div', text: { tag: 'lark_md', content: `**${title}**\n\nID：\`${result.id}\`` } },
      ],
    });
    console.log(`✅ 测试用例创建成功 id=${result.id} verified=${verified}`);
  } catch (e) {
    await sendCard({
      config: { wide_screen_mode: true },
      header: { title: { tag: 'plain_text', content: '❌ 创建失败' }, template: 'red' },
      elements: [{ tag: 'div', text: { tag: 'lark_md', content: e.message } }],
    });
  }
}

const [,, cmd, ...rest] = process.argv;

if (cmd === 'list') {
  await showTestcaseList(rest[0] || DEFAULT_PROJECT_ID);
} else if (cmd === 'plan') {
  await showTestPlanList(rest[0] || DEFAULT_PROJECT_ID);
} else if (cmd === 'create') {
  await createTestcase(rest[0], rest[1] || DEFAULT_PROJECT_ID);
} else if (cmd === 'callback') {
  const parts = (rest[0] || '').split('|');
  const action = parts[0];
  if (action === 'TC_PLAN') {
    await showTestPlanResult(parts[1], parts[2] || DEFAULT_PROJECT_ID);
  } else if (action === 'TC_PLANS') {
    await showTestPlanList(parts[1] || DEFAULT_PROJECT_ID);
  } else if (action === 'TC_DETAIL') {
    // 查单个用例详情（简化处理，直接跳到列表）
    await showTestcaseList(parts[2] || DEFAULT_PROJECT_ID);
  } else if (action === 'TC_CREATE_START') {
    const projectId = parts[1] || DEFAULT_PROJECT_ID;
    await sendCard({
      config: { wide_screen_mode: true },
      header: { title: { tag: 'plain_text', content: '🧪 创建测试用例' }, template: 'blue' },
      elements: [{ tag: 'div', text: { tag: 'lark_md', content: '请发消息告诉我用例标题：\n\n`创建测试用例 用户登录-正常密码登录成功`' } }],
    });
  }
} else {
  // 默认显示用例列表
  await showTestcaseList(rest[0] || DEFAULT_PROJECT_ID);
}
