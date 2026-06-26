/**
 * 子 Agent 创建器
 * 使用 OpenClaw API 创建真正的子 Agent
 */

// OpenClaw API - 在 Gateway 内部运行时可用
let sessionsSpawn = null;

try {
  const openclaw = require('openclaw');
  sessionsSpawn = openclaw.sessions_spawn;
  console.log('[SubagentCreator] ✅ OpenClaw API 已加载');
} catch (err) {
  console.error('[SubagentCreator] ❌ OpenClaw API 不可用:', err.message);
  console.error('[SubagentCreator] 此 Skill 必须在 OpenClaw Gateway 内部运行');
}

/**
 * 创建子 Agent
 * @param {Object} params - 参数
 * @param {string} params.visitorUid - 访客 UID
 * @param {string} params.prompt - Prompt
 * @param {number} params.timeout - 超时时间（秒）
 * @param {string} params.ownerUid - 主人 UID
 */
async function createSubagent(params) {
  console.log('[SubagentCreator] ========== 创建子 Agent ==========');
  console.log(`[SubagentCreator] 访客: ${params.visitorUid}`);
  console.log(`[SubagentCreator] 超时: ${params.timeout}秒`);
  
  if (!sessionsSpawn) {
    throw new Error('OpenClaw API 不可用，无法创建子 Agent');
  }
  
  // 构建子 Agent 的 task
  const task = buildSubagentTask(params);
  
  console.log('[SubagentCreator] 调用 sessions_spawn...');
  
  // 调用 OpenClaw 创建子 Agent
  const result = await sessionsSpawn({
    runtime: 'subagent',
    sandbox: 'require',
    task: task,
    cleanup: 'keep',
    label: `VOKO回复-${params.visitorUid.slice(-8)}`,
    timeoutSeconds: params.timeout || 120
  });
  
  console.log('[SubagentCreator] ✅ 子 Agent 创建完成');
  console.log(`[SubagentCreator]    - runId: ${result.runId}`);
  console.log(`[SubagentCreator]    - status: ${result.status}`);
  
  return {
    runId: result.runId,
    status: result.status,
    output: result.output,
    error: result.error
  };
}

/**
 * 构建子 Agent 的 Task
 */
function buildSubagentTask(params) {
  return `你是 VOKO 智能客服助手。

【任务】
根据提供的访客信息和对话历史，回复访客消息。

${params.prompt}

【重要】
1. 仔细分析访客的需求和情绪
2. 回复要简洁、友好、专业
3. 不确定的内容标记 need_owner_attention=true
4. 必须返回合法的 JSON 格式`;
}

module.exports = { createSubagent };
