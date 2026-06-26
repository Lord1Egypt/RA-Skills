#!/usr/bin/env node
/**
 * commit-activity-card.mjs
 * Commit 活动查看：最近 N 次提交记录，支持按仓库/分支筛选
 *
 * 用法：
 *   node commit-activity-card.mjs [repoId] [branch] [limit]
 *   node commit-activity-card.mjs callback "COMMIT_REPO|repoId|repoName"
 */

import { readFileSync } from 'fs';
import { TOKEN, ORG_ID, OPEN_ID, requireConfig, YUNXIAO_TOKEN } from './config.mjs';

requireConfig();

const YUNXIAO_BASE = 'https://openapi-rdc.aliyuncs.com/oapi/v1';
const FEISHU_BASE = 'https://open.feishu.cn/open-apis';

// 重点监控仓库（填入你的仓库 ID，通过 GET /oapi/v1/codeup/organizations/{orgId}/repositories 查询）
const WATCHED_REPOS = [
  // { id: 123456, name: 'my-repo' },
];

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

function timeAgo(dateStr) {
  const diff = Date.now() - new Date(dateStr).getTime();
  const h = Math.floor(diff / 3600000);
  const d = Math.floor(diff / 86400000);
  if (h < 1) return '刚刚';
  if (h < 24) return `${h}h 前`;
  return `${d}d 前`;
}

async function showCommits(repoId, repoName, branch = 'main', limit = 10) {
  let commits = [];
  try {
    const r = await yunxiaoGet(
      `/codeup/organizations/${ORG_ID}/repositories/${repoId}/commits?refName=${encodeURIComponent(branch)}&page=1&perPage=${limit}`
    );
    commits = Array.isArray(r) ? r : (r.commits || []);
  } catch (e) {
    console.error('查询 commit 失败:', e.message);
  }

  const commitLines = commits.slice(0, 10).map(c => {
    const sha = (c.id || c.sha || '').slice(0, 7);
    const msg = (c.title || c.message || '').split('\n')[0].slice(0, 50);
    const author = c.authorName || c.author?.name || '—';
    const time = timeAgo(c.authoredDate || c.createdAt || '');
    return `• \`${sha}\` **${msg}**\n  ${author} · ${time}`;
  }).join('\n\n');

  // 仓库切换按钮
  const repoButtons = WATCHED_REPOS.map(r => ({
    tag: 'button',
    text: { tag: 'plain_text', content: r.name },
    type: String(r.id) === String(repoId) ? 'primary' : 'default',
    value: { command: `COMMIT_REPO|${r.id}|${encodeURIComponent(r.name)}` },
  }));

  const card = {
    config: { wide_screen_mode: true },
    header: { title: { tag: 'plain_text', content: `📝 最近提交 · ${repoName} · \`${branch}\`` }, template: 'blue' },
    elements: [
      { tag: 'div', text: { tag: 'lark_md', content: commitLines || '暂无提交记录' } },
      { tag: 'hr' },
      { tag: 'div', text: { tag: 'lark_md', content: '**切换仓库：**' } },
      { tag: 'action', actions: repoButtons },
    ],
  };

  const msgId = await sendCard(card);
  console.log(`✅ Commit 卡片已发送 msgId=${msgId} repo=${repoName} commits=${commits.length}`);
}

// 查所有监控仓库的汇总提交
async function showAllReposCommits() {
  const allCommits = [];
  for (const repo of WATCHED_REPOS) {
    try {
      const r = await yunxiaoGet(
        `/codeup/organizations/${ORG_ID}/repositories/${repo.id}/commits?refName=main&page=1&perPage=5`
      );
      const commits = Array.isArray(r) ? r : (r.commits || []);
      commits.forEach(c => allCommits.push({ ...c, repoName: repo.name, repoId: repo.id }));
    } catch {}
  }

  allCommits.sort((a, b) => new Date(b.authoredDate || 0) - new Date(a.authoredDate || 0));

  const lines = allCommits.slice(0, 12).map(c => {
    const sha = (c.id || c.sha || '').slice(0, 7);
    const msg = (c.title || c.message || '').split('\n')[0].slice(0, 45);
    const author = c.authorName || '—';
    const time = timeAgo(c.authoredDate || '');
    return `• \`${sha}\` **[${c.repoName}]** ${msg}\n  ${author} · ${time}`;
  }).join('\n\n');

  const repoButtons = WATCHED_REPOS.map(r => ({
    tag: 'button',
    text: { tag: 'plain_text', content: r.name },
    type: 'default',
    value: { command: `COMMIT_REPO|${r.id}|${encodeURIComponent(r.name)}` },
  }));

  const card = {
    config: { wide_screen_mode: true },
    header: { title: { tag: 'plain_text', content: '📝 最近提交汇总（全仓库）' }, template: 'blue' },
    elements: [
      { tag: 'div', text: { tag: 'lark_md', content: lines || '暂无提交记录' } },
      { tag: 'hr' },
      { tag: 'div', text: { tag: 'lark_md', content: '**查看单仓库：**' } },
      { tag: 'action', actions: repoButtons },
    ],
  };

  const msgId = await sendCard(card);
  console.log(`✅ 全仓库 commit 汇总已发送 msgId=${msgId}`);
}

const [,, cmd, ...rest] = process.argv;

if (cmd === 'callback') {
  const parts = (rest[0] || '').split('|');
  if (parts[0] === 'COMMIT_REPO') {
    const [, repoId, repoName] = parts;
    await showCommits(repoId, decodeURIComponent(repoName));
  }
} else if (cmd && /^\d+$/.test(cmd)) {
  // node commit-activity-card.mjs <repoId> [branch] [limit]
  const [branch, limit] = rest;
  const repo = WATCHED_REPOS.find(r => String(r.id) === cmd) || { id: cmd, name: `仓库${cmd}` };
  await showCommits(cmd, repo.name, branch || 'main', parseInt(limit) || 10);
} else {
  await showAllReposCommits();
}
