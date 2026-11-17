/**
 * rl-runtime-guard — Pre-tool-call runtime guardrails
 * ====================================================
 * Adapted from OpenClaw-RL Phase 2.4 (deployed 2026-08-22).
 *
 * Three runtime guards inject soft prompt augmentation:
 *   1. complex_task_guard — catches complex_task_fail (43% of errors)
 *   2. retry_loop_guard — catches retry_loop (27%)
 *   3. tool_guard — catches tool_arg_complex + path_mismatch (11%)
 *
 * Together they cover 82.5% of agent-fault errors.
 *
 * This file is a STANDALONE ESM adaptation of the CommonJS OpenClaw hook
 * handler at ~/.openclaw/hooks/rl-runtime-guard/handler.js.
 *
 * Differences from the production hook:
 *   - ESM (no require/module.exports)
 *   - Configurable thresholds via config object
 *   - Disablable via enabled flag or RL_GUARD_DISABLED env var
 *   - Audit log path configurable
 *   - No "Linux VM" assumptions in prompts (cross-platform)
 */

import { appendFileSync, mkdirSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { homedir } from 'node:os';

// ─── Defaults (override via config object passed to guard()) ───────────

export const DEFAULT_CONFIG = {
  /** Character count above which a user message is treated as "complex". */
  complexTaskThreshold: 400,
  /** Jaccard similarity threshold for retry-loop detection. */
  retryLoopThreshold: 0.4,
  /** Recent messages kept per session for retry-loop detection. */
  recentQueryWindow: 10,
  /** Maximum length of a single exec command (soft advisory). */
  maxExecLength: 2000,
  /** Audit log path; ~ expansion supported. Set to '' or null to disable. */
  auditLogPath: '',
  /** Master switch; can also be overridden by RL_GUARD_DISABLED=1. */
  enabled: true,
};

// ─── Detection helpers ─────────────────────────────────────────────────

/**
 * Heuristic: detect "complex multi-step" user messages.
 * Triggers when:
 *   - Length >= complexTaskThreshold chars
 *   - OR contains explicit multi-step keywords
 */
export function isComplexTask(text, config = DEFAULT_CONFIG) {
  if (!text) return false;
  if (text.length >= config.complexTaskThreshold) return true;
  const multiStepKeywords = [
    /请按以下步骤执行/, /请执行以下/, /执行步骤/, /按照.*步骤/,
    /步骤\s*\d+/, /^\s*\d+[\.、]/m,
    /Task \d+|Goal \d+|Milestone/i,
  ];
  return multiStepKeywords.some(p => p.test(text));
}

/**
 * Character bigram Jaccard similarity — better than word Jaccard for CJK.
 */
export function charBigrams(text) {
  const cleaned = text.toLowerCase().replace(/\s+/g, '');
  const bigrams = new Set();
  for (let i = 0; i < cleaned.length - 1; i++) {
    bigrams.add(cleaned.substring(i, i + 2));
  }
  return bigrams;
}

export function jaccardSimilarity(a, b) {
  const aBigrams = charBigrams(a);
  const bBigrams = charBigrams(b);
  if (aBigrams.size === 0 || bBigrams.size === 0) return 0;
  const intersection = [...aBigrams].filter(g => bBigrams.has(g));
  const union = new Set([...aBigrams, ...bBigrams]);
  return intersection.length / union.size;
}

/**
 * Heuristic: detect "retry loop" by checking similarity to recent queries.
 */
export function isRetryLoop(currentQuery, recentQueries, config = DEFAULT_CONFIG) {
  if (!currentQuery || !recentQueries || recentQueries.length < 2) return false;
  let maxSim = 0;
  for (const prev of recentQueries.slice(-5)) {
    const sim = jaccardSimilarity(currentQuery, prev);
    if (sim > maxSim) maxSim = sim;
  }
  return maxSim >= config.retryLoopThreshold;
}

/**
 * Heuristic: detect Windows-style paths or platform-mismatched hints.
 * Cross-platform: works on Linux, macOS, Windows hosts.
 */
export function hasPlatformPathHint(text) {
  if (!text) return false;
  return /~\/Desktop|~\/Documents|~\/Downloads|\/openclawwin|\\Desktop|\\Documents|Windows 桌面|C:\\|\\\\/i.test(text);
}

// ─── Prompt builders ───────────────────────────────────────────────────

export function buildComplexTaskPrompt(config = DEFAULT_CONFIG) {
  return `## Runtime Guard: 复杂任务先拆解再执行

你收到了一条复杂/多步骤的用户指令（>= ${config.complexTaskThreshold} 字符或含多步骤标记）。
在调用任何工具之前，**必须**遵循以下流程：

1. **明确范围**：用 1-3 句话总结用户的最终目标
2. **列出步骤**：将任务拆解为 3-7 个可验证的子步骤
3. **风险预判**：识别可能的失败点（环境/路径/权限/超时）
4. **分步执行**：每完成一步，立即检查结果再继续，不要一次性写大块代码
5. **失败回退**：如果某步连续失败 ≥2 次，立刻停止并向用户报告当前进展

🚫 **禁止行为**：
- 单次 \`exec\` 命令 > ${config.maxExecLength} 字符（heredoc 大文件应分片或用 write 工具）
- 在未验证路径存在前直接写入（如假设 ~/Desktop 存在）
- 一次调用执行超过 5 个不同工具`;
}

export function buildRetryLoopPrompt(config = DEFAULT_CONFIG) {
  return `## Runtime Guard: 检测到重复查询 — 必须自省

系统检测到你**近 3 次用户消息高度相似**（Jaccard >= ${config.retryLoopThreshold}）。
这通常意味着：
- 用户对之前的回复不满意
- 或者你已经陷入机械重试循环

**强制要求**：在执行任何工具调用之前，先用 3-5 句话回答：

1. **之前做了什么？** 回顾你最近 2-3 轮的回复和工具调用结果
2. **为什么用户还在问？** 推测可能的卡点（信息缺失？理解错误？执行失败？）
3. **这次打算怎么做？** 明确与之前不同的策略
4. **是否需要澄清？** 如果信息不足，先问用户而不是继续尝试`;
}

export function buildToolGuardPrompt(config = DEFAULT_CONFIG) {
  return `## Runtime Guard: 工具调用与环境规范

环境约束：
- 🚫 **禁止**调用其他平台的路径特征：\`~/Desktop\`、\`~/Documents\`、\`C:\\\\\`、\`/openclawwin\` 等
- ✅ 如需桌面文件，改用 \`/tmp/\`、\`~/workspace/\` 或本平台真实存在路径
- 🚫 **禁止**单次 \`exec\` 命令 > ${config.maxExecLength} 字符（heredoc 大块写入应使用 \`write\` 工具分步）
- 🚫 **禁止**不验证路径是否存在就写入（先用 \`read\` 或 \`exec ls\` 确认）

如果违反以上约束，工具调用会以 \`tool_success=0\` 失败并被记为 error。`;
}

// ─── Audit logging ──────────────────────────────────────────────────────

function expandHome(p) {
  return p.startsWith('~') ? join(homedir(), p.slice(1)) : p;
}

function logDecision(entry, config = DEFAULT_CONFIG) {
  if (!config.auditLogPath) return;
  try {
    const logPath = expandHome(config.auditLogPath);
    const logDir = dirname(logPath);
    if (!existsSync(logDir)) mkdirSync(logDir, { recursive: true });
    appendFileSync(logPath, JSON.stringify({
      ...entry,
      timestamp: new Date().toISOString(),
    }) + '\n');
  } catch {
    // Never throw out of audit logging
  }
}

// ─── Main entry point ──────────────────────────────────────────────────

/**
 * Apply runtime guardrails to a request.
 *
 * @param {Object} ctx — hook context
 * @param {Object} ctx.requestData — the request object (mutated in-place)
 * @param {string} ctx.sessionKey — session identifier for state
 * @param {Object} [sessionStore] — external state map (default: in-memory)
 * @param {Object} [config] — override defaults
 * @returns {string[]} — list of decisions made (for testing/debugging)
 */
export function applyGuards(ctx, sessionStore = new Map(), config = { ...DEFAULT_CONFIG }) {
  // Master switches
  if (!config.enabled) return [];
  if (process.env.RL_GUARD_DISABLED === '1') return [];

  const { requestData, sessionKey } = ctx || {};
  if (!requestData || !sessionKey) return [];

  // Extract user content from various request shapes
  let userContent = null;
  if (Array.isArray(requestData.messages)) {
    const lastUserMsg = [...requestData.messages].reverse().find(m => m.role === 'user');
    userContent = typeof lastUserMsg?.content === 'string' ? lastUserMsg.content : null;
  } else if (typeof requestData.context === 'string') {
    userContent = requestData.context;
  } else if (typeof requestData.context?.text === 'string') {
    userContent = requestData.context.text;
  } else if (typeof requestData.prompt === 'string') {
    userContent = requestData.prompt;
  }

  if (!userContent || !userContent.trim()) return [];

  const decisions = [];

  // 1. Complex task detection
  const isComplex = isComplexTask(userContent, config);
  if (isComplex) decisions.push('complex_task');

  // 2. Retry loop detection (uses session-scoped state)
  const state = sessionStore.get(sessionKey) || { recentUserQueries: [] };
  const isLoop = isRetryLoop(userContent, state.recentUserQueries, config);
  if (isLoop) decisions.push('retry_loop');

  // Update state (always — even when no guard fired)
  state.recentUserQueries.push(userContent);
  if (state.recentUserQueries.length > config.recentQueryWindow) {
    state.recentUserQueries = state.recentUserQueries.slice(-config.recentQueryWindow);
  }
  sessionStore.set(sessionKey, state);

  // 3. Platform path hint detection
  const hasBadPath = hasPlatformPathHint(userContent);
  if (hasBadPath) decisions.push('platform_path_hint');

  if (decisions.length === 0) return [];

  // Build combined prompt
  let guardPrompt = '';
  if (decisions.includes('complex_task')) {
    guardPrompt += buildComplexTaskPrompt(config) + '\n\n';
  }
  if (decisions.includes('retry_loop')) {
    guardPrompt += buildRetryLoopPrompt(config) + '\n\n';
  }
  if (decisions.includes('platform_path_hint') || decisions.includes('complex_task')) {
    guardPrompt += buildToolGuardPrompt(config) + '\n\n';
  }
  guardPrompt = guardPrompt.trim();

  // Inject (same pattern as the production hook)
  if (Array.isArray(requestData.messages)) {
    const msgs = requestData.messages;
    const lastSystemIdx = [...msgs].reverse().findIndex(m => m.role === 'system');
    const insertIdx = lastSystemIdx >= 0 ? msgs.length - 1 - lastSystemIdx + 1 : 0;
    msgs.splice(insertIdx, 0, {
      role: 'system',
      content: guardPrompt,
      name: 'rl-runtime-guard',
    });
  } else if (typeof requestData.systemPrompt === 'string') {
    requestData.systemPrompt = guardPrompt + '\n\n' + requestData.systemPrompt;
  } else if (typeof requestData.context === 'object' && requestData.context !== null) {
    if (typeof requestData.context.text === 'string') {
      requestData.context.text = guardPrompt + '\n\n' + requestData.context.text;
    } else if (typeof requestData.context.system === 'string') {
      requestData.context.system = guardPrompt + '\n\n' + requestData.context.system;
    }
  } else if (typeof requestData.context === 'string') {
    requestData.context = guardPrompt + '\n\n' + requestData.context;
  }

  logDecision({
    sessionKey,
    decisions,
    // No userContentPreview — privacy by default. Log only metadata:
    // decisions fired and prompt length. Enable explicit audit via
    // config.auditLogPath only when the operator wants telemetry.
    guardPromptLength: guardPrompt.length,
    userContentLength: userContent.length,
  }, config);

  return decisions;
}

// ─── Convenience wrapper for OpenClaw hook registration ────────────────

/**
 * Default export matching the OpenClaw hook signature.
 * Wraps applyGuards with a session store that lives for the lifetime of
 * the hook process.
 */
const hookSessionStore = new Map();

export default async function requestBeforeHandler(ctx) {
  try {
    return applyGuards(ctx, hookSessionStore);
  } catch (err) {
    // Never break the request pipeline
    try {
      const cfg = DEFAULT_CONFIG;
      logDecision({
        sessionKey: ctx?.sessionKey,
        error: err.message,
      }, cfg);
    } catch {}
    return [];
  }
}