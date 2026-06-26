#!/usr/bin/env node
/**
 * release-flow.mjs
 * 发版流程：选仓库 → 选分支 → 输入版本号 → 打 Tag → 触发发版流水线
 *
 * 用法：
 *   node release-flow.mjs [pipelineId]          # 发版本号输入提示
 *   node release-flow.mjs callback "<payload>"
 *
 * 回调 payload：
 *   RELEASE_SELECT_REPO|repoId|repoName|sshUrl
 *   RELEASE_SELECT_BRANCH|repoId|repoName|branch
 *   RELEASE_CONFIRM|repoId|repoName|branch|version|pipelineId
 */

import { readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { tmpdir } from 'os';
import { fileURLToPath } from 'url';
import { TOKEN, ORG_ID, OPEN_ID, requireConfig, YUNXIAO_TOKEN } from './config.mjs';

const __dir = dirname(fileURLToPath(import.meta.url));

requireConfig();

const YUNXIAO_BASE = 'https://openapi-rdc.aliyuncs.com/oapi/v1';
const FEISHU_BASE = 'https://open.feishu.cn/open-apis';

// 常用发版流水线（可扩展）
const RELEASE_PIPELINES = [
  // 在此填入你的流水线 ID，格式：{ id: <number>, name: '<display-name>' }
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

const STATE_FILE = join(tmpdir(), 'release-flow-state.json');
const loadState = () => { try { return JSON.parse(readFileSync(STATE_FILE, 'utf8')); } catch { return {}; } };
const saveState = (s) => writeFileSync(STATE_FILE, JSON.stringify(s, null, 2));

// Step 1：选仓库
async function stepSelectRepo(pipelineId) {
  // 列出最近活跃的仓库
  let repos = [];
  try {
    const r = await yunxiaoGet(`/codeup/organizations/${ORG_ID}/repositories?page=1&perPage=50`);
    repos = (Array.isArray(r) ? r : []).slice(0, 10);
  } catch {}

  const repoButtons = repos.slice(0, 8).map(repo => ({
    tag: 'button',
    text: { tag: 'plain_text', content: repo.name },
    type: 'default',
    value: { command: `RELEASE_SELECT_REPO|${repo.id}|${encodeURIComponent(repo.name)}|${encodeURIComponent(repo.sshUrlToRepo || repo.httpUrlToRepo || '')}|${pipelineId || ''}` },
  }));

  const card = {
    config: { wide_screen_mode: true },
    header: { title: { tag: 'plain_text', content: '🚀 发版流程 - 选择仓库' }, template: 'green' },
    elements: [
      { tag: 'div', text: { tag: 'lark_md', content: '选择要打 Tag 的代码仓库：' } },
      { tag: 'hr' },
      { tag: 'action', actions: repoButtons },
    ],
  };
  const msgId = await sendCard(card);
  saveState({ step: 'SELECT_REPO', msgId, pipelineId: pipelineId || '' });
  console.log(`✅ 已发送仓库选择卡片 msgId=${msgId}`);
}

// Step 2：选分支
async function stepSelectBranch(repoId, repoName, sshUrl, pipelineId, archiveMsgId) {
  let branches = [];
  try {
    const r = await yunxiaoGet(`/codeup/organizations/${ORG_ID}/repositories/${repoId}/branches?page=1&perPage=20`);
    branches = Array.isArray(r) ? r : (r.branches || []);
    // 按最近活跃排序，main/master 置顶
    branches.sort((a, b) => {
      if (a.name === 'main' || a.name === 'master') return -1;
      if (b.name === 'main' || b.name === 'master') return 1;
      return 0;
    });
  } catch {}

  const topBranches = branches.slice(0, 6);
  const card = {
    config: { wide_screen_mode: true },
    header: { title: { tag: 'plain_text', content: `🚀 发版 - 选择分支 [${decodeURIComponent(repoName)}]` }, template: 'green' },
    elements: [
      { tag: 'div', text: { tag: 'lark_md', content: '选择要打 Tag 的分支（通常是 main 或 release 分支）：' } },
      { tag: 'hr' },
      {
        tag: 'action',
        actions: topBranches.map(b => ({
          tag: 'button',
          text: { tag: 'plain_text', content: b.name },
          type: b.name === 'main' || b.name === 'master' ? 'primary' : 'default',
          value: { command: `RELEASE_SELECT_BRANCH|${repoId}|${repoName}|${encodeURIComponent(b.name)}|${encodeURIComponent(sshUrl)}|${pipelineId || ''}` },
        })),
      },
    ],
  };
  const msgId = await sendCard(card, archiveMsgId, '✅ 已选择仓库');
  saveState({ step: 'SELECT_BRANCH', msgId, repoId, repoName: decodeURIComponent(repoName), sshUrl: decodeURIComponent(sshUrl), pipelineId });
  console.log(`✅ 已发送分支选择卡片 msgId=${msgId}`);
}

// Step 3：确认发版信息
async function stepConfirmRelease(repoId, repoName, branch, sshUrl, pipelineId, archiveMsgId) {
  const state = loadState();

  // 查最新 tag 推算下一个版本号
  let nextVersion = 'v1.0.0';
  try {
    const tags = await yunxiaoGet(`/codeup/organizations/${ORG_ID}/repositories/${repoId}/tags?page=1&perPage=5`);
    const tagList = Array.isArray(tags) ? tags : (tags.tags || []);
    if (tagList.length > 0) {
      const lastTag = tagList[0].name;
      const match = lastTag.match(/v?(\d+)\.(\d+)\.(\d+)/);
      if (match) {
        nextVersion = `v${match[1]}.${match[2]}.${parseInt(match[3]) + 1}`;
      }
    }
  } catch {}

  // 选流水线按钮
  const pipelineButtons = RELEASE_PIPELINES.map(p => ({
    tag: 'button',
    text: { tag: 'plain_text', content: p.name },
    type: String(p.id) === String(pipelineId) ? 'primary' : 'default',
    value: { command: `RELEASE_CONFIRM|${repoId}|${repoName}|${encodeURIComponent(branch)}|${encodeURIComponent(nextVersion)}|${p.id}` },
  }));

  const card = {
    config: { wide_screen_mode: true },
    header: { title: { tag: 'plain_text', content: '🚀 确认发版信息' }, template: 'green' },
    elements: [
      { tag: 'div', fields: [
        { is_short: true, text: { tag: 'lark_md', content: `**仓库**\n${decodeURIComponent(repoName)}` } },
        { is_short: true, text: { tag: 'lark_md', content: `**分支**\n\`${decodeURIComponent(branch)}\`` } },
        { is_short: true, text: { tag: 'lark_md', content: `**推荐版本号**\n${nextVersion}` } },
      ]},
      { tag: 'hr' },
      { tag: 'div', text: { tag: 'lark_md', content: '**选择触发的流水线（点击即确认发版）：**' } },
      { tag: 'action', actions: pipelineButtons },
      { tag: 'note', elements: [{ tag: 'lark_md', content: `如需自定义版本号，发消息：\`版本号：v1.2.3\`` }] },
    ],
  };
  const msgId = await sendCard(card, archiveMsgId, '✅ 已选择分支');
  saveState({ ...state, step: 'CONFIRM', msgId, repoId, repoName: decodeURIComponent(repoName), branch: decodeURIComponent(branch), nextVersion });
  console.log(`✅ 已发送发版确认卡片 msgId=${msgId} 推荐版本=${nextVersion}`);
}

// Step 4：打 tag + 触发流水线
async function stepDoRelease(repoId, repoName, branch, version, pipelineId, archiveMsgId) {
  const decodedBranch = decodeURIComponent(branch);
  const decodedVersion = decodeURIComponent(version);

  // 1. 获取分支最新 commit SHA
  let sha = '';
  try {
    const branchInfo = await yunxiaoGet(`/codeup/organizations/${ORG_ID}/repositories/${repoId}/branches/${encodeURIComponent(decodedBranch)}`);
    sha = branchInfo.commit?.id || branchInfo.sha || '';
  } catch (e) {
    console.error('获取 commit SHA 失败:', e.message);
  }

  // 2. 创建 Tag
  let tagCreated = false;
  try {
    await yunxiaoPost(`/codeup/organizations/${ORG_ID}/repositories/${repoId}/tags`, {
      tagName: decodedVersion,
      ref: decodedBranch,
      message: `Release ${decodedVersion}`,
    });
    tagCreated = true;
  } catch (e) {
    console.error('创建 Tag 失败:', e.message);
  }

  // 3. 触发流水线
  let runId = null;
  let runError = null;
  if (pipelineId) {
    try {
      const runRes = await yunxiaoPost(`/flow/organizations/${ORG_ID}/pipelines/${pipelineId}/runs`, {
        branch: decodedBranch,
        params: { version: decodedVersion },
      });
      runId = runRes.pipelineRunId || runRes.runId || runRes.id;
    } catch (e) {
      runError = e.message;
    }
  }

  // 4. GET 验证 Tag
  let tagVerified = false;
  if (tagCreated) {
    try {
      const tags = await yunxiaoGet(`/codeup/organizations/${ORG_ID}/repositories/${repoId}/tags?page=1&perPage=1`);
      const tagList = Array.isArray(tags) ? tags : (tags.tags || []);
      tagVerified = tagList[0]?.name === decodedVersion;
    } catch {}
  }

  const card = {
    config: { wide_screen_mode: true },
    header: {
      title: { tag: 'plain_text', content: tagCreated ? `✅ 发版 ${decodedVersion} 已启动` : '❌ 发版失败' },
      template: tagCreated ? 'green' : 'red',
    },
    elements: [
      { tag: 'div', fields: [
        { is_short: true, text: { tag: 'lark_md', content: `**版本号**\n${decodedVersion}` } },
        { is_short: true, text: { tag: 'lark_md', content: `**Tag 创建**\n${tagVerified ? '✅ 已确认' : tagCreated ? '⚠️ 创建但未验证' : '❌ 失败'}` } },
        { is_short: true, text: { tag: 'lark_md', content: `**流水线**\n${runId ? `✅ runId=${runId}` : (runError || '未触发')}` } },
        { is_short: true, text: { tag: 'lark_md', content: `**分支**\n\`${decodedBranch}\`` } },
      ]},
      ...(runId ? [
        { tag: 'hr' },
        { tag: 'action', actions: [
          { tag: 'button', text: { tag: 'plain_text', content: '📊 查看流水线' }, type: 'primary',
            value: { command: `PIPELINE_STATUS|${pipelineId}|${runId}` } },
        ]},
      ] : []),
    ],
  };

  await updateCard(archiveMsgId, card);
  saveState({});
  console.log(`✅ 发版完成 version=${decodedVersion} tagOK=${tagVerified} runId=${runId}`);

  // 5. 后台轮询（如果流水线触发成功）
  if (runId) {
    const { spawn } = await import('child_process');
    const logPath = `/tmp/poll-pipeline-${runId}.log`;
    const { openSync } = await import('fs');
    const logFd = openSync(logPath, 'a');
    const child = spawn('python3', [
      join(__dir, 'poll-pipeline.py'),
      String(runId), String(pipelineId),
    ], { detached: true, stdio: ['ignore', logFd, logFd] });
    child.unref();  // 与父进程解耦，不阻塞
    console.log(`[info] 轮询进程已后台启动 pid=${child.pid} log=${logPath}`);
  }
}

// CLI
const [,, cmd, ...rest] = process.argv;

if (cmd === 'callback') {
  const payload = rest[0] || '';
  const parts = payload.split('|');
  const action = parts[0];
  const state = loadState();

  if (action === 'RELEASE_SELECT_REPO') {
    const [, repoId, repoName, sshUrl, pipelineId] = parts;
    await stepSelectBranch(repoId, repoName, sshUrl, pipelineId, state.msgId);
  } else if (action === 'RELEASE_SELECT_BRANCH') {
    const [, repoId, repoName, branch, sshUrl, pipelineId] = parts;
    await stepConfirmRelease(repoId, repoName, branch, sshUrl, pipelineId, state.msgId);
  } else if (action === 'RELEASE_CONFIRM') {
    const [, repoId, repoName, branch, version, pipelineId] = parts;
    await stepDoRelease(repoId, repoName, branch, version, pipelineId, state.msgId);
  }
} else if (cmd === 'version') {
  // 用户自定义版本号：node release-flow.mjs version "v1.2.3"
  const state = loadState();
  if (state.step !== 'CONFIRM') {
    console.error('请先启动发版流程');
    process.exit(1);
  }
  const version = rest[0] || state.nextVersion;
  await stepDoRelease(state.repoId, state.repoName, state.branch, version, state.pipelineId, state.msgId);
} else {
  // 默认：发仓库选择卡片
  const pipelineId = cmd || '';
  await stepSelectRepo(pipelineId);
}
