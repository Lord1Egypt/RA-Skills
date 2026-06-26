/**
 * bug-fix-flow.mjs
 * 从缺陷工作项到代码修复的完整自动化流程。
 *
 * 流程：
 *   1. 获取工作项详情
 *   2. 选择关联代码库
 *   3. 克隆/拉取代码，创建 fix 分支
 *   4. 调 Claude Code 自动修复（AI 生成 diff）
 *   5. 飞书展示 diff，等待人工确认
 *   6. 确认后推送分支，创建 Codeup MR
 *   7. 飞书卡片展示 MR，等待确认合并
 *   8. 合并 MR，更新工作项状态为「已修复」
 *
 * 用法：
 *   node bug-fix-flow.mjs <workitemId>
 *
 * 回调处理：
 *   BUGFIX_SELECT_REPO|<workitemId>|<repoId>|<repoName>|<sshUrl>
 *   BUGFIX_CONFIRM_DIFF|<workitemId>|<repoId>|<branch>|<workDir>
 *   BUGFIX_REJECT_DIFF|<workitemId>
 *   BUGFIX_CONFIRM_MERGE|<workitemId>|<repoId>|<mrId>
 *   BUGFIX_REJECT_MERGE|<workitemId>|<mrId>
 */

import { readFileSync, existsSync, writeFileSync } from 'fs';
import { execSync, spawnSync } from 'child_process';
import { homedir, tmpdir } from 'os';
import { join } from 'path';
import { TOKEN, ORG_ID, OPEN_ID, requireConfig, YUNXIAO_TOKEN } from './config.mjs';

requireConfig();

const YUNXIAO_BASE = 'https://openapi-rdc.aliyuncs.com/oapi/v1';
const FEISHU_BASE = 'https://open.feishu.cn/open-apis';

// ── 飞书 Token ─────────────────────────────────────────────────────────────────
let _feishuToken = null;
async function getFeishuToken() {
  if (_feishuToken) return _feishuToken;
  const config = JSON.parse(readFileSync(`${homedir()}/.openclaw/openclaw.json`, 'utf8'));
  const res = await fetch(`${FEISHU_BASE}/auth/v3/tenant_access_token/internal`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ app_id: config.channels?.feishu?.appId, app_secret: config.channels?.feishu?.appSecret }),
  });
  const data = await res.json();
  _feishuToken = data.tenant_access_token;
  return _feishuToken;
}

// 将旧卡片归档为静态"已完成"样式（去掉 actions，灰色）
async function archiveCard(token, msgId, label = '✅ 已完成') {
  if (!msgId) return;
  const archived = {
    config: { wide_screen_mode: true },
    header: { title: { tag: 'plain_text', content: label }, template: 'grey' },
    elements: [{ tag: 'div', text: { tag: 'lark_md', content: '操作已完成，请查看下方新卡片。' } }],
  };
  await fetch(`${FEISHU_BASE}/im/v1/messages/${msgId}`, {
    method: 'PATCH',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ content: JSON.stringify(archived) }),
  }).catch(() => {}); // 归档失败不阻断主流程
}

// 发新卡片（始终 POST）；如果传了 archiveMsgId，先把旧卡片归档
async function sendCard(card, archiveMsgId = null, archiveLabel = '✅ 已完成') {
  const token = await getFeishuToken();
  if (archiveMsgId) await archiveCard(token, archiveMsgId, archiveLabel);
  const res = await fetch(`${FEISHU_BASE}/im/v1/messages?receive_id_type=open_id`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ receive_id: OPEN_ID, msg_type: 'interactive', content: JSON.stringify(card) }),
  });
  const data = await res.json();
  if (data.code !== 0) throw new Error(`Feishu send error: ${data.msg}`);
  return data.data.message_id;
}

// 原地更新卡片（仅用于合并完成后刷新当前卡片）
async function updateCard(msgId, card) {
  const token = await getFeishuToken();
  await fetch(`${FEISHU_BASE}/im/v1/messages/${msgId}`, {
    method: 'PATCH',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ content: JSON.stringify(card) }),
  });
  return msgId;
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
  const data = await res.json();
  return data.data?.message_id;
}

// ── 云效 API ───────────────────────────────────────────────────────────────────
async function yunxiaoGet(path) {
  const res = await fetch(`${YUNXIAO_BASE}${path}`, { headers: { 'x-yunxiao-token': YUNXIAO_TOKEN } });
  return res.json();
}

async function yunxiaoPost(path, body) {
  const res = await fetch(`${YUNXIAO_BASE}${path}`, {
    method: 'POST', headers: { 'x-yunxiao-token': YUNXIAO_TOKEN, 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  return res.json();
}

async function yunxiaoPut(path, body) {
  const res = await fetch(`${YUNXIAO_BASE}${path}`, {
    method: 'PUT', headers: { 'x-yunxiao-token': YUNXIAO_TOKEN, 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  return res.text();
}

async function getWorkitem(workitemId) {
  return yunxiaoGet(`/projex/organizations/${ORG_ID}/workitems/${workitemId}`);
}

async function listRepos() {
  const data = await yunxiaoGet(`/codeup/organizations/${ORG_ID}/repositories?page=1&perPage=50`);
  return Array.isArray(data) ? data : (data.result ?? data.data ?? []);
}

async function getRepoBranches(repoId) {
  const data = await yunxiaoGet(`/codeup/organizations/${ORG_ID}/repositories/${repoId}/branches?page=1&perPage=50`);
  return Array.isArray(data) ? data : (data.result ?? []);
}

async function createMR(repoId, { sourceBranch, targetBranch, title, description, workItemIds }) {
  return yunxiaoPost(`/codeup/organizations/${ORG_ID}/repositories/${repoId}/changeRequests`, {
    sourceBranch,
    targetBranch,
    sourceProjectId: Number(repoId),
    targetProjectId: Number(repoId),
    title,
    description,
    workItemIds,
    createFrom: 'WEB',
  });
}

async function mergeMR(repoId, mrId) {
  // 先尝试 squash，不行再试 fast_forward
  try {
    return await yunxiaoPost(`/codeup/organizations/${ORG_ID}/repositories/${repoId}/changeRequests/${mrId}/merge`, {
      mergeType: 'squash',
    });
  } catch (e) {
    if (e.message?.includes('不支持')) {
      return await yunxiaoPost(`/codeup/organizations/${ORG_ID}/repositories/${repoId}/changeRequests/${mrId}/merge`, {
        mergeType: 'fast_forward',
      });
    }
    throw e;
  }
}

// ── 状态文件（保存流程中间状态）────────────────────────────────────────────────
const STATE_FILE = join(tmpdir(), 'bug-fix-state.json');

function loadState() {
  try { return JSON.parse(readFileSync(STATE_FILE, 'utf8')); } catch { return {}; }
}

function saveState(state) {
  writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

// ── SSH Key 自动注册 ───────────────────────────────────────────────────────────
async function ensureSSHKey() {
  let pubkey;
  try {
    pubkey = readFileSync(`${homedir()}/.ssh/id_rsa.pub`, 'utf8').trim();
  } catch {
    // 没有公钥，生成一个
    spawnSync('ssh-keygen', ['-t', 'rsa', '-b', '4096', '-f', `${homedir()}/.ssh/id_rsa`, '-N', ''], { stdio: 'pipe' });
    pubkey = readFileSync(`${homedir()}/.ssh/id_rsa.pub`, 'utf8').trim();
  }

  const pubkeyBody = pubkey.split(' ')[1];

  // 查已注册的 SSH Key 列表
  const listData = await yunxiaoGet(`/codeup/organizations/${ORG_ID}/keys?perPage=100`);
  const keys = Array.isArray(listData) ? listData : (listData.result ?? []);
  const exists = keys.find(k => (k.key ?? '').trim().split(' ')[1] === pubkeyBody);

  if (exists) {
    console.log(`[ssh] 公钥已注册: ${exists.title}`);
    return;
  }

  // 未注册，自动注册
  console.log('[ssh] 公钥未注册，正在通过 API 注册...');
  const result = await yunxiaoPost(`/codeup/organizations/${ORG_ID}/keys`, {
    key: pubkey,
    title: '@openclaw-server',
    keyScope: 'ALL',
  });
  console.log(`[ssh] 注册成功 id=${result.id}, title=${result.title}`);
}

// ── Step 1：展示工作项 + 选择仓库 ─────────────────────────────────────────────
async function stepSelectRepo(workitemId) {
  // 前置检查：确保 SSH Key 已注册
  await ensureSSHKey();

  const [item, repos] = await Promise.all([getWorkitem(workitemId), listRepos()]);

  if (item.categoryId !== 'Bug') {
    await sendNotify(`⚠️ 工作项 ${item.serialNumber} 类型为「${item.workitemType?.name}」，不是缺陷，无法走 Bug 修复流程。`, '⚠️ 类型不匹配', 'orange');
    return;
  }

  const bugTitle = item.subject;
  const bugDesc = (item.description ?? '').replace(/<[^>]+>/g, '').trim().slice(0, 300);

  // 只列出名字比较接近或常见的仓库，最多 4 个按钮
  const topRepos = repos.slice(0, 4);

  const actions = topRepos.map((r, i) => ({
    tag: 'button',
    text: { tag: 'plain_text', content: r.name ?? `仓库 ${r.id}` },
    type: i === 0 ? 'primary' : 'default',
    value: { command: `BUGFIX_SELECT_REPO|${workitemId}|${r.id}|${encodeURIComponent(r.name ?? '')}|${encodeURIComponent(r.sshUrl ?? r.httpsUrl ?? '')}` },
  }));

  const card = {
    config: { wide_screen_mode: true },
    header: { title: { tag: 'plain_text', content: `🐛 Bug 修复流程启动` }, template: 'red' },
    elements: [
      { tag: 'div', text: { tag: 'lark_md', content: `**${item.serialNumber}** ${bugTitle}` } },
      { tag: 'div', text: { tag: 'lark_md', content: `**描述**\n${bugDesc || '（无描述）'}` } },
      { tag: 'hr' },
      { tag: 'div', text: { tag: 'lark_md', content: `**选择关联代码库**（点击按钮）` } },
      { tag: 'action', actions },
      { tag: 'note', elements: [{ tag: 'lark_md', content: `如果目标仓库不在列表中，请直接告诉我仓库名称` }] },
    ],
  };

  const msgId = await sendCard(card);
  saveState({ workitemId, step: 'SELECT_REPO', msgId });
  console.log(`✅ 已发送仓库选择卡片 msgId=${msgId}`);
}

// ── Step 1.5：选好仓库后，先让用户选开发分支 ──────────────────────────────────
async function stepSelectBranch(workitemId, repoId, repoName, sshUrl) {
  const state = loadState();
  const item = await getWorkitem(workitemId);

  // 拉取分支列表，按最近更新排序，取前6个热门分支
  const branches = await getRepoBranches(repoId);
  // 过滤掉 fix/ 开头的，排列常见主干在前
  const priorityOrder = ['main', 'master', 'develop', 'release', 'dev'];
  const sorted = [...branches].sort((a, b) => {
    const ai = priorityOrder.indexOf(a.name);
    const bi = priorityOrder.indexOf(b.name);
    if (ai !== -1 && bi !== -1) return ai - bi;
    if (ai !== -1) return -1;
    if (bi !== -1) return 1;
    return 0;
  });
  const topBranches = sorted
    .filter(b => !b.name.startsWith('fix/') && !b.name.startsWith('hotfix/'))
    .slice(0, 4);

  const actions = topBranches.map((b, i) => ({
    tag: 'button',
    text: { tag: 'plain_text', content: b.name },
    type: i === 0 ? 'primary' : 'default',
    value: { command: `BUGFIX_SELECT_BRANCH|${workitemId}|${repoId}|${encodeURIComponent(repoName)}|${encodeURIComponent(sshUrl)}|${encodeURIComponent(b.name)}` },
  }));

  const card = {
    config: { wide_screen_mode: true },
    header: { title: { tag: 'plain_text', content: `🌿 选择开发分支` }, template: 'blue' },
    elements: [
      { tag: 'div', text: { tag: 'lark_md', content: `**仓库：** ${repoName}\n**Bug：** ${item.subject}\n\n请选择该 Bug 所在的开发分支（修复分支将基于此创建）：` } },
      { tag: 'action', actions },
      { tag: 'note', elements: [{ tag: 'lark_md', content: `显示最近活跃的 ${topBranches.length} 个分支，如果目标分支不在此处请告诉我` }] },
    ],
  };

  const msgId = await sendCard(card, state.msgId, '✅ 已选择仓库');
  saveState({ ...state, workitemId, repoId, repoName, sshUrl, step: 'SELECT_BRANCH', msgId });
  console.log(`✅ 已发送分支选择卡片 msgId=${msgId}`);
}

// ── Step 2：选好分支后，克隆 + AI 修复 ───────────────────────────────────────
async function stepStartFix(workitemId, repoId, repoName, sshUrl, baseBranch) {
  const state = loadState();
  const item = await getWorkitem(workitemId);
  const bugTitle = item.subject;
  const bugDesc = (item.description ?? '').replace(/<[^>]+>/g, '').trim().slice(0, 500);

  // 使用用户选择的分支，而不是自动猜
  const mainBranch = baseBranch ?? 'main';
  const fixBranch = `fix/bug-${item.serialNumber?.toLowerCase() ?? workitemId.slice(0, 8)}-${Date.now()}`;

  // 克隆或更新本地仓库
  const workDir = join(tmpdir(), `bugfix-${repoId}`);
  const decodedSsh = decodeURIComponent(sshUrl);

  await sendNotify(`🔄 正在克隆仓库 **${repoName}**，创建分支 \`${fixBranch}\`...`, '⚙️ 准备中', 'blue');

  try {
    if (!existsSync(workDir)) {
      console.log(`[git] 克隆仓库 (depth=1)...`);
      execSync(`git clone --depth 1 -b ${mainBranch} ${decodedSsh} ${workDir}`, { stdio: 'pipe', timeout: 120000 });
    } else {
      console.log(`[git] 更新已有仓库...`);
      execSync(`git -C ${workDir} fetch origin ${mainBranch} --depth=1`, { stdio: 'pipe', timeout: 60000 });
      execSync(`git -C ${workDir} checkout ${mainBranch}`, { stdio: 'pipe' });
      execSync(`git -C ${workDir} reset --hard origin/${mainBranch}`, { stdio: 'pipe' });
    }
    console.log(`[git] 创建分支 ${fixBranch}...`);
    execSync(`git -C ${workDir} checkout -b ${fixBranch}`, { stdio: 'pipe' });
  } catch (e) {
    await sendNotify(`❌ Git 操作失败：\n\`\`\`\n${e.message.slice(0, 500)}\n\`\`\``, '❌ 克隆失败', 'red');
    return;
  }

  // AI 代码修复 via Claude Code（以 ccuser 执行，规避 root 限制）
  await sendNotify(`🤖 正在调用 Claude Code 分析并修复 Bug...\n\n**Bug：** ${bugTitle}\n\n这可能需要 2-3 分钟，请稍候。`, '🤖 Claude Code 修复中', 'blue');

  const ccPrompt = `你是一名资深工程师。请修复以下 Bug：

标题：${bugTitle}
描述：${bugDesc || '（无详细描述）'}

要求：
1. 分析代码库，找到导致 bug 的根本原因
2. 修复代码，保持最小改动原则
3. 不要修改测试文件或文档，专注于修复
4. 修复完成后简要说明改了什么文件以及为什么`;

  // 以 ccuser 身份运行 Claude Code（规避 root 限制）
  const isRoot = process.getuid?.() === 0;
  let aiOutput = '';
  let ccSuccess = false;

  if (isRoot) {
    console.log('[cc] 检测到 root 环境，切换到 ccuser 执行 Claude Code...');
    try { execSync(`chmod -R o+rw ${workDir}`, { stdio: 'pipe' }); } catch {}

    // 把 prompt 和启动脚本都写成临时文件，完全避免 shell 转义问题
    const ts = Date.now();
    const promptFile = `/tmp/cc-prompt-${ts}.txt`;
    const scriptFile = `/tmp/cc-run-${ts}.sh`;
    writeFileSync(promptFile, ccPrompt, 'utf8');
    writeFileSync(scriptFile,
      `#!/bin/bash
export PATH=/home/ccuser/.local/bin:$PATH
export ANTHROPIC_API_KEY=\${ANTHROPIC_API_KEY:-your-anthropic-api-key}
export ANTHROPIC_BASE_URL=\${ANTHROPIC_BASE_URL:-https://api.anthropic.com}
cd ${workDir}
cat ${promptFile} | claude --model claude-sonnet-4-6 --permission-mode bypassPermissions --print
`, 'utf8');
    try { execSync(`chown ccuser:ccuser ${promptFile} ${scriptFile} && chmod +x ${scriptFile}`); } catch {}

    const result = spawnSync('su', ['-s', '/bin/bash', 'ccuser', scriptFile],
      { encoding: 'utf8', timeout: 180000, maxBuffer: 10 * 1024 * 1024 }
    );
    try { execSync(`rm -f ${promptFile} ${scriptFile}`); } catch {}
    aiOutput = result.stdout ?? '';
    if (result.status === 0 && aiOutput) {
      ccSuccess = true;
      console.log('[cc] Claude Code 执行成功');
    } else {
      console.warn('[cc] Claude Code 执行失败:', result.stderr?.slice(0, 200));
    }
  } else {
    // 非 root 直接执行
    const result = spawnSync(
      'claude', ['--model', 'claude-sonnet-4-6', '--permission-mode', 'bypassPermissions', '--print', ccPrompt],
      { cwd: workDir, encoding: 'utf8', timeout: 180000, maxBuffer: 10 * 1024 * 1024,
        env: { ...process.env, ANTHROPIC_AUTH_TOKEN: process.env.ANTHROPIC_API_KEY, ANTHROPIC_BASE_URL: process.env.ANTHROPIC_BASE_URL || 'https://api.anthropic.com' } }
    );
    aiOutput = result.stdout ?? '';
    if (result.status === 0 && aiOutput) ccSuccess = true;
  }

  if (!aiOutput) aiOutput = '（Claude Code 未返回输出，请手动修复）';

  // 检查是否有代码改动
  let diff = '';
  try { diff = execSync(`git -C ${workDir} diff HEAD`, { encoding: 'utf8' }); } catch {}
  const hasChanges = diff.trim().length > 0;

  const analysisPreview = aiOutput.slice(0, 1000) + (aiOutput.length > 1000 ? '\n\n...(内容已截断)' : '');

  const diffPreview = hasChanges
    ? diff.slice(0, 800) + (diff.length > 800 ? '\n...(截断)' : '')
    : null;

  const card = {
    config: { wide_screen_mode: true },
    header: {
      title: { tag: 'plain_text', content: hasChanges ? `✏️ Claude Code 已修复，请 Review` : `🔍 AI 分析完成，请手动修复后确认` },
      template: hasChanges ? 'green' : 'orange',
    },
    elements: [
      { tag: 'div', text: { tag: 'lark_md', content: `**Bug：** ${bugTitle}` } },
      { tag: 'hr' },
      { tag: 'div', text: { tag: 'lark_md', content: `**Claude Code 说明：**\n${analysisPreview}` } },
      ...(diffPreview ? [
        { tag: 'hr' },
        { tag: 'div', text: { tag: 'lark_md', content: `**Code Diff：**\n\`\`\`diff\n${diffPreview}\n\`\`\`` } },
      ] : []),
      { tag: 'hr' },
      { tag: 'div', text: { tag: 'lark_md', content: `**代码目录：** \`${workDir}\`\n**分支：** \`${fixBranch}\`${!hasChanges ? '\n\n⚠️ Claude Code 未检测到代码改动，请手动修复后点确认' : ''}` } },
      {
        tag: 'action',
        actions: [
          {
            tag: 'button', text: { tag: 'plain_text', content: '✅ 已修复，推送并创建 MR' },
            type: 'primary',
            value: { command: `BUGFIX_CONFIRM_DIFF|${workitemId}|${repoId}|${fixBranch}|${encodeURIComponent(workDir)}` },
          },
          {
            tag: 'button', text: { tag: 'plain_text', content: '❌ 放弃本次修复' },
            type: 'danger',
            value: { command: `BUGFIX_REJECT_DIFF|${workitemId}` },
          },
        ],
      },
    ],
  };

  const msgId = await sendCard(card, state.msgId, '✅ 已选择分支');
  saveState({ workitemId, repoId, repoName, mainBranch, fixBranch, workDir, step: 'REVIEW_DIFF', msgId });
  console.log(`✅ Diff 展示卡片已发送 msgId=${msgId}`);
}

// ── Step 3：确认 diff → 推送分支 + 创建 MR ────────────────────────────────────
async function stepCreateMR(workitemId, repoId, fixBranch, workDir) {
  const state = loadState();
  const item = await getWorkitem(workitemId);
  const decodedDir = decodeURIComponent(workDir);

  await sendNotify(`🚀 正在推送分支 \`${fixBranch}\` 并创建 MR...`, '⚙️ 创建 MR 中', 'blue');

  // git add + commit + push
  try {
    execSync(`git -C ${decodedDir} add -A`, { stdio: 'pipe' });
    execSync(`git -C ${decodedDir} commit -m "fix: ${item.subject} [${item.serialNumber}]"`, { stdio: 'pipe' });
    execSync(`git -C ${decodedDir} push origin ${fixBranch}`, { stdio: 'pipe', timeout: 30000 });
  } catch (e) {
    await sendNotify(`❌ 推送失败：\n\`\`\`\n${e.message.slice(0, 400)}\n\`\`\``, '❌ 推送失败', 'red');
    return;
  }

  // 创建 MR
  const mainBranch = state.mainBranch ?? 'main';
  let mrData;
  try {
    mrData = await createMR(repoId, {
      sourceBranch: fixBranch,
      targetBranch: mainBranch,
      title: `fix: ${item.subject} [${item.serialNumber}]`,
      description: `关联云效工作项：${item.serialNumber}\n\n${(item.description ?? '').replace(/<[^>]+>/g, '').trim().slice(0, 300)}`,
      workItemIds: workitemId,
    });
  } catch (e) {
    await sendNotify(`❌ 创建 MR 失败：${e.message.slice(0, 300)}`, '❌ MR 创建失败', 'red');
    return;
  }

  const mrId = mrData?.id ?? mrData?.localId ?? mrData?.result?.id;
  const mrUrl = mrData?.webUrl ?? mrData?.result?.webUrl ?? '';

  const card = {
    config: { wide_screen_mode: true },
    header: { title: { tag: 'plain_text', content: `🔀 MR 已创建，确认合并？` }, template: 'green' },
    elements: [
      { tag: 'div', fields: [
        { is_short: true, text: { tag: 'lark_md', content: `**工作项**\n${item.serialNumber} ${item.subject.slice(0, 30)}` } },
        { is_short: true, text: { tag: 'lark_md', content: `**分支**\n\`${fixBranch}\` → \`${mainBranch}\`` } },
      ]},
      ...(mrUrl ? [{ tag: 'div', text: { tag: 'lark_md', content: `[在 Codeup 查看 MR ↗](${mrUrl})` } }] : []),
      { tag: 'hr' },
      {
        tag: 'action',
        actions: [
          {
            tag: 'button', text: { tag: 'plain_text', content: '✅ 确认合并' },
            type: 'primary',
            value: { command: `BUGFIX_CONFIRM_MERGE|${workitemId}|${repoId}|${mrId}` },
          },
          {
            tag: 'button', text: { tag: 'plain_text', content: '⏸️ 暂不合并' },
            type: 'default',
            value: { command: `BUGFIX_REJECT_MERGE|${workitemId}|${mrId}` },
          },
        ],
      },
    ],
  };

  const msgId = await sendCard(card, state.msgId, '✅ 已确认代码改动');
  saveState({ ...state, mrId, mrUrl, step: 'REVIEW_MR', msgId });
  console.log(`✅ MR 创建成功，等待确认合并 mrId=${mrId}`);
}

// ── Step 4：确认合并 ──────────────────────────────────────────────────────────
async function stepMerge(workitemId, repoId, mrId) {
  const state = loadState();

  await sendNotify(`🔀 正在合并 MR...`, '⚙️ 合并中', 'blue');

  try {
    await mergeMR(repoId, mrId);
  } catch (e) {
    await sendNotify(`❌ 合并失败：${e.message.slice(0, 300)}`, '❌ 合并失败', 'red');
    return;
  }

  // 更新工作项状态为「已修复」(id=29)
  await yunxiaoPut(`/projex/organizations/${ORG_ID}/workitems/${workitemId}`, { status: '29' });

  const item = await getWorkitem(workitemId);

  const card = {
    config: { wide_screen_mode: true },
    header: { title: { tag: 'plain_text', content: `✅ Bug 已修复完成` }, template: 'green' },
    elements: [
      { tag: 'div', fields: [
        { is_short: true, text: { tag: 'lark_md', content: `**工作项**\n${item.serialNumber} ${item.subject.slice(0, 30)}` } },
        { is_short: true, text: { tag: 'lark_md', content: `**状态**\n✅ ${item.status?.displayName}` } },
        { is_short: true, text: { tag: 'lark_md', content: `**MR**\n#${mrId} 已合并` } },
        { is_short: true, text: { tag: 'lark_md', content: `**分支**\n\`${state.fixBranch}\`` } },
      ]},
    ],
  };

  await updateCard(state.msgId, card);
  console.log(`✅ MR 已合并，工作项状态更新为「已修复」`);
}

// ── CLI 入口 ──────────────────────────────────────────────────────────────────
const [,, cmd, ...rest] = process.argv;

if (cmd === 'callback') {
  // bug-fix-flow.mjs callback "BUGFIX_SELECT_REPO|...|...|..."
  const payload = rest[0] ?? '';
  const parts = payload.split('|');
  const action = parts[0];
  console.log('[callback] action:', action, 'parts:', parts.length);

  try {
  if (action === 'BUGFIX_SELECT_REPO') {
    const [, workitemId, repoId, repoName, sshUrl] = parts;
    await stepSelectBranch(workitemId, repoId, repoName, sshUrl);
  } else if (action === 'BUGFIX_SELECT_BRANCH') {
    const [, workitemId, repoId, repoName, sshUrl, baseBranch] = parts;
    await stepStartFix(workitemId, repoId, repoName, sshUrl, decodeURIComponent(baseBranch));
  } else if (action === 'BUGFIX_CONFIRM_DIFF') {
    const [, workitemId, repoId, fixBranch, workDir] = parts;
    await stepCreateMR(workitemId, repoId, fixBranch, workDir);
  } else if (action === 'BUGFIX_REJECT_DIFF') {
    const [, workitemId] = parts;
    const state = loadState();
    await sendNotify(
      `好的，请在以下目录手动修改代码，改完告诉我，我来帮你推送和创建 MR：\n\n\`${state.workDir}\`\n\n完成后发：\`手动修复完毕\``,
      '✏️ 等待手动修复', 'orange'
    );
  } else if (action === 'BUGFIX_CONFIRM_MERGE') {
    const [, workitemId, repoId, mrId] = parts;
    await stepMerge(workitemId, repoId, mrId);
  } else if (action === 'BUGFIX_REJECT_MERGE') {
    const [, workitemId, mrId] = parts;
    await sendNotify(`好的，MR #${mrId} 暂不合并，你可以在 Codeup 上继续 review 后再手动合并。`, '⏸️ 暂不合并', 'orange');
  } else {
    console.error('Unknown callback payload:', payload);
  }
  } catch (err) {
    console.error('[callback] Error:', err.message);
    console.error(err.stack);
  }

} else {
  // 默认：node bug-fix-flow.mjs <workitemId>
  const workitemId = cmd;
  if (!workitemId) {
    console.error('Usage: node bug-fix-flow.mjs <workitemId>');
    process.exit(1);
  }
  await stepSelectRepo(workitemId);
}
