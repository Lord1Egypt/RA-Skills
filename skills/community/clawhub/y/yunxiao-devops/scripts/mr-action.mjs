#!/usr/bin/env node
/**
 * mr-action.mjs
 * Codeup MR 操作工具：审批（投票）、合并、关闭、查状态
 *
 * 用法：
 *   node mr-action.mjs approve  <repoId> <mrId>           # 当前 token 账号投票审批
 *   node mr-action.mjs merge    <repoId> <mrId> [squash]  # 合并（默认 squash）
 *   node mr-action.mjs close    <repoId> <mrId>           # 关闭 MR
 *   node mr-action.mjs status   <repoId> <mrId>           # 查状态 + 审批情况
 *   node mr-action.mjs approve-merge <repoId> <mrId>      # 先投票再合并
 */

import { readFileSync } from 'fs';
import { homedir } from 'os';

const TOKEN = 'pt-2cOur1wYEV34hBAfOapVwfCA_fc929387-46c5-4f53-9cea-e824134bbcb9';
const ORG = '614a9324e43534781c03c140';
const FEISHU_BASE = 'https://open.feishu.cn/open-apis';
const OPEN_ID = 'ou_3310bb816dfd43532448087823b8aa90';
const BASE = `https://openapi-rdc.aliyuncs.com/oapi/v1/codeup/organizations/${ORG}/repositories`;

const [,, action, repoId, mrId, mergeType = 'squash'] = process.argv;

if (!action || !repoId || !mrId) {
  console.error('Usage: node mr-action.mjs <approve|merge|close|status|approve-merge> <repoId> <mrId>');
  process.exit(1);
}

const headers = { 'x-yunxiao-token': TOKEN, 'Content-Type': 'application/json' };

async function api(method, path, body) {
  const res = await fetch(`${BASE}/${repoId}/${path}`, {
    method, headers, body: body ? JSON.stringify(body) : undefined
  });
  const text = await res.text();
  try { return { status: res.status, data: JSON.parse(text) }; }
  catch { return { status: res.status, data: text }; }
}

async function getMR() {
  const { data } = await api('GET', `changeRequests/${mrId}`);
  return data;
}

async function approveMR(comment = 'LGTM') {
  // 官方接口：reviewOpinion=PASS 触发正式 reviewer 审批
  const { status, data } = await api('POST', `changeRequests/${mrId}/review`, {
    reviewOpinion: 'PASS',
    reviewComment: comment,
  });
  return { success: status === 200 && data?.result === true, data };
}

async function mergeMR(type = 'squash') {
  const { status, data } = await api('POST', `changeRequests/${mrId}/merge`, { mergeType: type });
  if (status === 200 && data?.status === 'MERGED') {
    return { success: true, commit: data.mergedRevision?.slice(0, 12), data };
  }
  return { success: false, error: data?.errorDescription || data?.errorMessage || JSON.stringify(data), data };
}

async function closeMR() {
  const { status, data } = await api('POST', `changeRequests/${mrId}/close`, {});
  return { success: status === 200, data };
}

// ─── 飞书通知 ────────────────────────────────────────────────────────────────
async function getFeishuToken() {
  const config = JSON.parse(readFileSync(`${homedir()}/.openclaw/openclaw.json`, 'utf8'));
  const res = await fetch(`${FEISHU_BASE}/auth/v3/tenant_access_token/internal`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ app_id: config.channels.feishu.appId, app_secret: config.channels.feishu.appSecret }),
  });
  return (await res.json()).tenant_access_token;
}

async function sendCard(card) {
  const token = await getFeishuToken();
  const res = await fetch(`${FEISHU_BASE}/im/v1/messages?receive_id_type=open_id`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ receive_id: OPEN_ID, msg_type: 'interactive', content: JSON.stringify(card) })
  });
  return (await res.json());
}

function makeResultCard(title, color, mr, fields, actions = []) {
  return {
    config: { wide_screen_mode: true },
    header: { title: { tag: 'plain_text', content: title }, template: color },
    elements: [
      {
        tag: 'div',
        fields: [
          { is_short: true, text: { tag: 'lark_md', content: `**仓库 ID**\n${repoId}` } },
          { is_short: true, text: { tag: 'lark_md', content: `**MR #${mrId}**\n${mr?.title || '-'}` } },
          { is_short: true, text: { tag: 'lark_md', content: `**源分支**\n\`${mr?.sourceBranch || '-'}\`` } },
          { is_short: true, text: { tag: 'lark_md', content: `**目标分支**\n\`${mr?.targetBranch || '-'}\`` } },
        ]
      },
      ...fields.map(f => ({ tag: 'div', text: { tag: 'lark_md', content: f } })),
      ...(actions.length ? [{ tag: 'hr' }, { tag: 'action', actions }] : []),
    ]
  };
}

// ─── 执行动作 ────────────────────────────────────────────────────────────────
const mr = await getMR();
const mrUrl = mr?.detailUrl || mr?.webUrl || `https://codeup.aliyun.com/${ORG.slice(0,8)}`;

if (action === 'status') {
  const checks = mr?.checkList?.requirementRuleItems || [];
  const reviewers = mr?.reviewers || [];
  const checkLines = checks.map(c => `${c.pass ? '✅' : '❌'} ${c.itemType}`).join('\n');
  const reviewerLines = reviewers.map(r => `${r.hasReviewed ? '✅' : '⏳'} ${r.name}`).join('\n');

  const card = makeResultCard(
    `MR #${mrId} 状态`,
    mr?.allRequirementsPass ? 'green' : 'yellow',
    mr,
    [
      `**检查项**\n${checkLines || '无'}`,
      `**Reviewers**\n${reviewerLines || '无'}`,
      `**可合并：** ${mr?.allRequirementsPass ? '✅ 是' : '❌ 否'}`,
    ],
    [
      { tag: 'button', text: { tag: 'plain_text', content: '👀 查看 MR' }, type: 'default', url: mrUrl },
      ...(mr?.allRequirementsPass ? [
        { tag: 'button', text: { tag: 'plain_text', content: '✅ 合并' }, type: 'primary', value: `MR_MERGE|${repoId}|${mrId}` }
      ] : [
        { tag: 'button', text: { tag: 'plain_text', content: '👍 审批通过' }, type: 'primary', value: `MR_APPROVE_MERGE|${repoId}|${mrId}` }
      ])
    ]
  );
  const r = await sendCard(card);
  console.log(r.code === 0 ? `✅ 状态卡片已发送` : `❌ ${JSON.stringify(r)}`);

} else if (action === 'approve') {
  const result = await approveMR();
  console.log(result.success ? '✅ 投票审批成功' : `❌ 投票失败: ${JSON.stringify(result.data)}`);

} else if (action === 'merge') {
  const result = await mergeMR(mergeType);
  if (result.success) {
    const card = makeResultCard('✅ MR 已合并', 'green', mr, [
      `**Commit:** \`${result.commit}\``,
      `**合并方式:** ${mergeType}`,
    ], [
      { tag: 'button', text: { tag: 'plain_text', content: '🔍 查看记录' }, type: 'default', url: mrUrl }
    ]);
    const r = await sendCard(card);
    console.log(r.code === 0 ? `✅ 合并成功，卡片已发送` : `❌ 卡片发送失败`);
  } else {
    console.error(`❌ 合并失败: ${result.error}`);
    process.exit(1);
  }

} else if (action === 'approve-merge') {
  // 先投票，再检查是否满足合并条件，再合并
  console.log('Step 1: 投票审批...');
  const approveResult = await approveMR();
  console.log(approveResult.success ? '  ✅ 投票成功' : `  ⚠️ 投票响应: ${JSON.stringify(approveResult.data)}`);

  // 重新查状态
  const updatedMR = await getMR();
  console.log(`Step 2: 检查合并条件... allRequirementsPass=${updatedMR?.allRequirementsPass}`);

  if (updatedMR?.allRequirementsPass) {
    console.log('Step 3: 执行合并...');
    const mergeResult = await mergeMR(mergeType);
    if (mergeResult.success) {
      const card = makeResultCard('✅ MR 已审批并合并', 'green', updatedMR, [
        `**Commit:** \`${mergeResult.commit}\``,
        `**合并方式:** ${mergeType}`,
      ], [
        { tag: 'button', text: { tag: 'plain_text', content: '🔍 查看记录' }, type: 'default', url: mrUrl }
      ]);
      const r = await sendCard(card);
      console.log(r.code === 0 ? `✅ 审批+合并成功，卡片已发送` : `❌ 卡片发送失败`);
    } else {
      console.error(`❌ 合并失败: ${mergeResult.error}`);
      process.exit(1);
    }
  } else {
    // 仍有检查未过，发状态卡片告知
    const checks = updatedMR?.checkList?.requirementRuleItems || [];
    const reviewers = updatedMR?.reviewers || [];
    const failedChecks = checks.filter(c => !c.pass).map(c => `❌ ${c.itemType}`).join('\n');
    const reviewerLines = reviewers.map(r => `${r.hasReviewed ? '✅' : '⏳'} ${r.name}`).join('\n');

    const card = makeResultCard('⚠️ MR 仍无法合并', 'yellow', updatedMR, [
      `**未通过的检查**\n${failedChecks}`,
      `**Reviewers 状态**\n${reviewerLines}`,
      `投票已提交，但 reviewer 审批需在 Codeup 页面操作。`,
    ], [
      { tag: 'button', text: { tag: 'plain_text', content: '🔗 去审批' }, type: 'primary', url: mrUrl },
    ]);
    const r = await sendCard(card);
    console.log(r.code === 0 ? `⚠️ 状态卡片已发送` : `❌ ${JSON.stringify(r)}`);
    process.exit(1);
  }

} else if (action === 'close') {
  const result = await closeMR();
  console.log(result.success ? '✅ MR 已关闭' : `❌ 关闭失败: ${JSON.stringify(result.data)}`);

} else {
  console.error(`未知 action: ${action}`);
  process.exit(1);
}
