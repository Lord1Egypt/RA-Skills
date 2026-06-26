#!/usr/bin/env node
/**
 * mr-review-card.mjs
 * 待 Code Review 的 MR 列表卡片
 *
 * 用法：
 *   node mr-review-card.mjs [repoId]     # 查指定仓库 MR，不传则查所有
 *   node mr-review-card.mjs callback "MR_MERGE|repoId|mrId"
 *   node mr-review-card.mjs callback "MR_CLOSE|repoId|mrId"
 */

import { readFileSync } from 'fs';
import { execSync } from 'child_process';
import { TOKEN, ORG_ID, OPEN_ID, requireConfig, YUNXIAO_TOKEN } from './config.mjs';

requireConfig();

// ── 配置 ──────────────────────────────────────────────────────────────────────

const YUNXIAO_BASE = 'https://openapi-rdc.aliyuncs.com/oapi/v1';
const FEISHU_BASE = 'https://open.feishu.cn/open-apis';

// 需要监控的重要仓库（填入你的仓库 ID，通过 GET /oapi/v1/codeup/organizations/{orgId}/repositories 查询）
const WATCHED_REPOS = [
  // { id: 123456, name: 'my-repo' },
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
  const d = await res.json();
  return d.tenant_access_token;
}

async function sendCard(card) {
  const token = await getFeishuToken();
  const res = await fetch(`${FEISHU_BASE}/im/v1/messages?receive_id_type=open_id`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ receive_id: OPEN_ID, msg_type: 'interactive', content: JSON.stringify(card) }),
  });
  const data = await res.json();
  if (data.code !== 0) throw new Error(`Feishu error: ${data.msg}`);
  return data.data.message_id;
}

async function sendNotify(content, title, color = 'blue') {
  const token = await getFeishuToken();
  const card = {
    config: { wide_screen_mode: true },
    header: { title: { tag: 'plain_text', content: title }, template: color },
    elements: [{ tag: 'div', text: { tag: 'lark_md', content } }],
  };
  const res = await fetch(`${FEISHU_BASE}/im/v1/messages?receive_id_type=open_id`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ receive_id: OPEN_ID, msg_type: 'interactive', content: JSON.stringify(card) }),
  });
  return (await res.json()).data?.message_id;
}

// ── 云效 API ──────────────────────────────────────────────────────────────────
async function yunxiaoGet(path) {
  const res = await fetch(`${YUNXIAO_BASE}${path}`, {
    headers: { 'x-yunxiao-token': YUNXIAO_TOKEN },
  });
  const data = await res.json();
  if (data.errorCode) throw new Error(data.errorMessage);
  return data;
}

async function yunxiaoPost(path, body) {
  const res = await fetch(`${YUNXIAO_BASE}${path}`, {
    method: 'POST',
    headers: { 'x-yunxiao-token': YUNXIAO_TOKEN, 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  if (data.errorCode) throw new Error(data.errorMessage);
  return data;
}

// ── 查单仓库 MR ───────────────────────────────────────────────────────────────
async function fetchRepoMRs(repoId, repoName) {
  const mrs = [];
  // 查待 review 和待合并
  for (const state of ['UNDER_REVIEW', 'TO_BE_MERGED']) {
    try {
      const res = await yunxiaoGet(
        `/codeup/organizations/${ORG_ID}/repositories/${repoId}/changeRequests?state=${state}&page=1&perPage=20`
      );
      const list = Array.isArray(res) ? res : (res.changeRequests || res.list || []);
      list.forEach(mr => mrs.push({ ...mr, repoId, repoName }));
    } catch (e) {
      // 仓库无权限或无 MR，跳过
    }
  }
  return mrs;
}

// ── 构建 MR 卡片 ──────────────────────────────────────────────────────────────
function buildMRCard(mrs) {
  const total = mrs.length;
  if (total === 0) {
    return {
      config: { wide_screen_mode: true },
      header: { title: { tag: 'plain_text', content: '✅ 暂无待处理 MR' }, template: 'green' },
      elements: [{ tag: 'div', text: { tag: 'lark_md', content: '所有 MR 已处理，代码仓库干净整洁 👍' } }],
    };
  }

  const underReview = mrs.filter(m => m.status === 'UNDER_REVIEW');
  const toBeMerged = mrs.filter(m => m.status === 'TO_BE_MERGED');

  const elements = [];

  // 待合并（优先展示）
  if (toBeMerged.length > 0) {
    elements.push({ tag: 'div', text: { tag: 'lark_md', content: `**🟢 待合并（${toBeMerged.length}）**` } });
    for (const mr of toBeMerged) {
      elements.push({
        tag: 'div',
        fields: [
          { is_short: false, text: { tag: 'lark_md', content: `**[${mr.repoName}] ${mr.title}**` } },
          { is_short: true, text: { tag: 'lark_md', content: `作者：${mr.author?.name || '—'}` } },
          { is_short: true, text: { tag: 'lark_md', content: `\`${mr.sourceBranch}\` → \`${mr.targetBranch}\`` } },
        ],
      });
      elements.push({
        tag: 'action',
        actions: [
          {
            tag: 'button',
            text: { tag: 'plain_text', content: '✅ 合并' },
            type: 'primary',
            value: { command: `MR_MERGE|${mr.repoId}|${mr.localId}` },
          },
          {
            tag: 'button',
            text: { tag: 'plain_text', content: '🔗 在 Codeup 查看' },
            type: 'default',
            value: { command: `MR_OPEN|${mr.detailUrl || mr.webUrl}` },
          },
        ],
      });
      elements.push({ tag: 'hr' });
    }
  }

  // 待 Review
  if (underReview.length > 0) {
    elements.push({ tag: 'div', text: { tag: 'lark_md', content: `**🔵 待 Review（${underReview.length}）**` } });
    for (const mr of underReview.slice(0, 5)) {
      elements.push({
        tag: 'div',
        fields: [
          { is_short: false, text: { tag: 'lark_md', content: `**[${mr.repoName}] ${mr.title}**` } },
          { is_short: true, text: { tag: 'lark_md', content: `作者：${mr.author?.name || '—'}` } },
          { is_short: true, text: { tag: 'lark_md', content: `变更：${mr.changeSizeBucket || '—'}` } },
        ],
      });
    }
    if (underReview.length > 5) {
      elements.push({ tag: 'note', elements: [{ tag: 'lark_md', content: `还有 ${underReview.length - 5} 个待 Review...` }] });
    }
  }

  return {
    config: { wide_screen_mode: true },
    header: {
      title: { tag: 'plain_text', content: `🔀 待处理 MR（${total}）` },
      template: toBeMerged.length > 0 ? 'green' : 'blue',
    },
    elements,
  };
}

// ── 合并 MR ───────────────────────────────────────────────────────────────────
async function mergeMR(repoId, mrId) {
  // 先 squash，失败再 fast_forward
  try {
    return await yunxiaoPost(
      `/codeup/organizations/${ORG_ID}/repositories/${repoId}/changeRequests/${mrId}/merge`,
      { mergeType: 'squash' }
    );
  } catch (e) {
    if (e.message?.includes('不支持')) {
      return await yunxiaoPost(
        `/codeup/organizations/${ORG_ID}/repositories/${repoId}/changeRequests/${mrId}/merge`,
        { mergeType: 'fast_forward' }
      );
    }
    throw e;
  }
}

// ── 主逻辑 ───────────────────────────────────────────────────────────────────
async function showMRList(specificRepoId = null) {
  const repos = specificRepoId
    ? [{ id: specificRepoId, name: `仓库 ${specificRepoId}` }]
    : WATCHED_REPOS;

  let allMRs = [];
  for (const repo of repos) {
    const mrs = await fetchRepoMRs(repo.id, repo.name);
    allMRs = allMRs.concat(mrs);
  }

  const card = buildMRCard(allMRs);
  const msgId = await sendCard(card);
  console.log(`✅ MR 看板已发送 msgId=${msgId} 总计=${allMRs.length}`);
}

// ── CLI 入口 ──────────────────────────────────────────────────────────────────
const [,, cmd, ...rest] = process.argv;

if (cmd === 'callback') {
  const payload = rest[0] || '';
  const parts = payload.split('|');
  const action = parts[0];

  if (action === 'MR_MERGE') {
    const [, repoId, mrId] = parts;
    try {
      const result = await mergeMR(repoId, mrId);
      // GET 验证
      const verify = await yunxiaoGet(`/codeup/organizations/${ORG_ID}/repositories/${repoId}/changeRequests/${mrId}`);
      if (verify.status === 'MERGED') {
        await sendNotify(`✅ MR #${mrId} 已成功合并（squash）\n\n仓库 ID：${repoId}`, '✅ MR 已合并', 'green');
        console.log(`✅ MR #${mrId} 合并成功 status=${verify.status}`);
      } else {
        await sendNotify(`⚠️ MR #${mrId} 合并请求已发送，但状态为 ${verify.status}，请手动确认。`, '⚠️ 请确认', 'orange');
        console.warn(`MR 状态异常: ${verify.status}`);
      }
    } catch (e) {
      await sendNotify(`❌ 合并失败：${e.message}`, '❌ 合并失败', 'red');
    }
  } else if (action === 'MR_OPEN') {
    const url = parts[1];
    await sendNotify(`[在 Codeup 查看 MR ↗](${url})`, '🔗 MR 链接', 'blue');
  } else {
    console.error('未知 callback:', action);
  }
} else {
  const repoId = cmd && /^\d+$/.test(cmd) ? parseInt(cmd) : null;
  await showMRList(repoId);
}
