/**
 * Self-Improvement Hook for OpenClaw
 *
 * Handles four OpenClaw event types:
 * 1. agent:bootstrap      → inject reminder file (session start) + reset session state
 * 2. command:new          → reset session state (new task)
 * 3. command:reset       → reset session state (explicit reset)
 * 4. message:preprocessed → keyword detection + push reminders + Hermes-style self-review
 *
 * v4.7.0: Hermes-style task review — message counting + self-review prompt injection
 */

// ── Imports + Config ──────────────────────────────────────────
const { execSync } = require('child_process');
const { existsSync, readFileSync } = require('fs');

const WORKSPACE = process.env.HOME + '/.openclaw/workspace';
const SELF_IMPROVEMENT_DIR = WORKSPACE + '/skills/self-improvement-loop/scripts';
const MAX_MESSAGES = 10;

// ── Per-agent workspace routing ──────────────────────────────
const OPENCLAW_JSON = process.env.HOME + '/.openclaw/openclaw.json';

/**
 * Extract agent ID from sessionKey.
 * Format: "agent:<id>:..." e.g., "agent:main:telegram:direct:7754385134"
 */
function extractAgentId(sessionKey) {
  if (!sessionKey || typeof sessionKey !== 'string') return 'main';
  const match = sessionKey.match(/^agent:([^:]+)/);
  return match ? match[1] : 'main';
}

/**
 * Load agent workspace from openclaw.json.
 * Falls back to global workspace if agent not found.
 */
function getAgentWorkspace(agentId) {
  const globalWorkspace = process.env.HOME + '/.openclaw/workspace';
  try {
    const config = require(OPENCLAW_JSON);
    const agents = config.agents?.list || [];
    const agent = agents.find(a => a.id === agentId);
    if (agent?.workspace) {
      return agent.workspace;
    }
  } catch (e) {
    // openclaw.json not found or parse error — use global
  }
  return globalWorkspace;
}

/**
 * Get the .learnings directory for the current agent.
 */
function getLearningsDir(sessionKey) {
  const agentId = extractAgentId(sessionKey);
  const workspace = getAgentWorkspace(agentId);
  return workspace + '/.learnings';
}

// ── Script runner helper ─────────────────────────────────────
function runScript(scriptName, agentId, ...args) {
  const scriptPath = SELF_IMPROVEMENT_DIR + '/' + scriptName;
  const env = { ...process.env, LEARNINGS_DIR: learningsDir };
  try {
    return execSync(`bash "${scriptPath}" "${agentId}" ${args.join(' ')}`, {
      encoding: 'utf8',
      timeout: 5000,
      cwd: process.env.HOME,
      env,
    }).trim();
  } catch (e) {
    return '';
  }
}

// Placeholder for runtime replacement
const WORKSPACE_PLACEHOLDER = '{{WORKSPACE_LEARNINGS}}';
const BOOTSTRAP_REMINDER = `
## Self-Improvement Reminder

**主动回顾 · 主动记录 · 不要等用户纠正**

### 记录条件
- 用户纠正你（"不对"、"错了"、"actually"）→ \`${WORKSPACE_PLACEHOLDER}/LEARNINGS.md\`
- 命令/操作失败 → \`${WORKSPACE_PLACEHOLDER}/ERRORS.md\`
- 发现知识过时/错误 → \`${WORKSPACE_PLACEHOLDER}/LEARNINGS.md\`
- 找到更好的方法 → \`${WORKSPACE_PLACEHOLDER}/LEARNINGS.md\`
- 用户要求不存在的功能 → \`${WORKSPACE_PLACEHOLDER}/FEATURE_REQUESTS.md\`

### 主动记录（不等纠正）
- 每个任务完成后问自己：这次学到了什么？下次要注意什么？
- 有价值的新发现 → 立即写入 \`${WORKSPACE_PLACEHOLDER}/LEARNINGS.md\`
- 遇到重复 pattern → 更新 Recurrence-Count

### 格式
写入前先参考模板的10~25行(包含所有有效 category 值和完整格式)：
- 纠正/洞察/最佳实践 → \`${WORKSPACE_PLACEHOLDER}/LEARNINGS.md\`
- 命令/操作失败 → \`${WORKSPACE_PLACEHOLDER}/ERRORS.md\`
- 功能缺失请求 → \`${WORKSPACE_PLACEHOLDER}/FEATURE_REQUESTS.md\`

按模板格式填写即可。

### 关键规则
- **Pattern-Key**：\`<source>.<type>.<identifier>\`（如：\`hook.correction.forgot-to-verify\`）
- **Recurrence-Count**：首次记录写 \`1\`，下次遇到相同 pattern 累加
- **ID 格式**：\`YYYYMMDD-NNN\`（如：\`20260421-001\`）

Keep entries simple. Patterns compound — the more you log, the smarter the distill loop becomes.
`.trim();

function generateSelfReviewPrompt(learningsDir) {
  return runScript('inject_review.sh', '', learningsDir);
}

// ── Keywords ────────────────────────────────────────────────
const CORRECTION_KEYWORDS = [
  // English
  "no, that's wrong", "actually,", "that's not right", "you're wrong", "wrong.",
  "no wait", "actually i meant", "I said", "not quite", "almost but", "close, but",
  "that's not what I meant", "I meant to say", "that's wrong","you should learn","you should notice",
  // Chinese
  "不对", "不是", "错了", "等等", "等等不对", "其实", "应该",
  "我想说的是", "不是这样的", "不是这个", "等等重新来", "不是我想的",
  "等等再想想", "好像不对", "好像不是","你应该学习","你应该注意"
];

const ERROR_KEYWORDS = [
  // English
  "error", "failed", "doesn't work", "crashed", "broke", "not working", "stuck",
  "cannot", "can't", "unable to", "invalid", "timeout", "exception",
  // Chinese
  "不能", "不行", "用不了", "坏了", "崩了", "出错了", "报错",
  "失败了", "坏掉了", "打不开", "没反应", "没用了",
  "无法", "不行了", "有问题",
];

const FEATURE_KEYWORDS = [
  // English
  "can you add", "is there a way to", "feature request", "I wish it could",
  "could you make it", "can it do", "I'd like it to", "it would be nice if",
  "would be great if", "can we have", "want to add", "need a way to",
  // Chinese
  "能不能加", "可不可以加", "能不能帮我加", "加个功能", "加一个",
  "能做一个吗", "能做一个", "我想要", "要是能", "要是可以",
  "我想让它能", "能不能让它", "能加个吗", "加一下", "做个功能",
  "做个", "帮我做个", "帮我加", "能不能帮我做", "我希望它能",
];

function containsKeyword(text, keywords) {
  const lower = text.toLowerCase();
  return keywords.some(kw => lower.includes(kw));
}

// ── Handler ────────────────────────────────────────────────
const handler = async (event) => {
  if (!event || typeof event !== 'object') return;

  const sessionKey = event.sessionKey || '';
  const agentId = extractAgentId(sessionKey);
  const learningsDir = getLearningsDir(sessionKey);
  const workspace = learningsDir.replace('/.learnings', '');

  // ── agent:bootstrap ──────────────────────────────────────
  if (event.type === 'agent' && event.action === 'bootstrap') {
    if (Array.isArray(event.context?.bootstrapFiles)) {
      const reminder = BOOTSTRAP_REMINDER.replace(/\{\{WORKSPACE_LEARNINGS\}\}/g, learningsDir);
      event.context.bootstrapFiles.push({
        path: 'SELF_IMPROVEMENT_REMINDER.md',
        content: reminder,
        virtual: true,
      });
    }
    return;
  }

  // ── command:new / command:reset ───────────────────────────
  if ((event.type === 'command:new' || event.type === 'command:reset')) {
    return;
  }

  // ── session_end ─────────────────────────────────────────────
  // Self-review 由 agent 通过 prompt 自触发，hook 不注入，
  // session_end 不需要完成标记

  // ── message:preprocessed ─────────────────────────────────
  if (event.type === 'message' && event.action === 'preprocessed') {
    const body = event.context?.bodyForAgent || '';
    if (!body || typeof body !== 'string') return;

    const isCorrection = containsKeyword(body, CORRECTION_KEYWORDS);
    const isErrorFeedback = containsKeyword(body, ERROR_KEYWORDS);
    const isFeatureRequest = containsKeyword(body, FEATURE_KEYWORDS);

    if (isCorrection) {
      event.context.messages?.push(
        `[Self-Improvement] 🪝 检测到校正信号 — 考虑将这次纠正记入 \`${learningsDir}/LEARNINGS.md\``
      );
    } else if (isErrorFeedback) {
      event.context.messages?.push(
        `[Self-Improvement] 🪝 检测到错误反馈 — 考虑将问题记入 \`${learningsDir}/ERRORS.md\``
      );
    } else if (isFeatureRequest) {
      event.context.messages?.push(
        `[Self-Improvement] 🪝 检测到功能请求信号 — 考虑将需求记入 \`${learningsDir}/FEATURE_REQUESTS.md\``
      );
    }
    // Self-review 触发由 prompt 引导（工具调用≥5 / 发现绕弯 / 预判重复）
    // 不再由 hook 计数注入
    return;
  }
};

module.exports = handler;
module.exports.default = handler;