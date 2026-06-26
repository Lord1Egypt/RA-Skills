/**
 * 主处理器
 * 处理访客消息的核心逻辑
 */

const path = require('path');
const { buildPrompt } = require('./prompt-builder');
const { createSubagent } = require('./subagent-creator');
const { parseResponse } = require('./response-parser');

// 设置数据库路径（从参数或环境变量获取）
let dbPath = null;

function setDbPath(path) {
  dbPath = path;
}

function getDbPath() {
  if (dbPath) return dbPath;
  // 默认路径
  return path.join(process.cwd(), 'data', 'voko.db');
}

/**
 * 处理访客消息
 * @param {Object} args - 参数
 */
async function handleVisitorMessage(args) {
  console.log('[Handler] ========== 处理访客消息 ==========');
  console.log(`[Handler] 访客 UID: ${args.visitorUid}`);
  console.log(`[Handler] 模式: ${args.mode}`);
  
  // 设置数据库路径
  if (args.dbPath) {
    setDbPath(args.dbPath);
  }
  
  // 步骤 1: 组装 Prompt
  console.log('[Handler] [步骤 1/3] 组装 Prompt...');
  let prompt;
  
  if (args.prompt) {
    // 直接传入 Base64 编码的 prompt
    console.log('[Handler] 使用传入的 Prompt');
    prompt = Buffer.from(args.prompt, 'base64').toString('utf8');
  } else if (args.mode === 'build-and-handle') {
    // 从数据库查询并组装
    console.log('[Handler] 从数据库组装 Prompt');
    prompt = await buildPrompt(args.visitorUid, args.messageIds, getDbPath());
  } else {
    throw new Error('缺少 prompt 参数，或 mode 不为 build-and-handle');
  }
  
  console.log(`[Handler] ✅ Prompt 组装完成，长度: ${prompt.length} 字符`);
  
  // 步骤 2: 创建子 Agent
  console.log('[Handler] [步骤 2/3] 创建子 Agent...');
  const subagentResult = await createSubagent({
    visitorUid: args.visitorUid,
    prompt: prompt,
    timeout: args.timeout,
    ownerUid: args.ownerUid
  });
  
  console.log(`[Handler] ✅ 子 Agent 运行完成`);
  console.log(`[Handler]    - runId: ${subagentResult.runId}`);
  console.log(`[Handler]    - status: ${subagentResult.status}`);
  
  // 步骤 3: 解析响应
  console.log('[Handler] [步骤 3/3] 解析响应...');
  const response = parseResponse(subagentResult, args.visitorUid);
  
  console.log('[Handler] ✅ 响应解析完成');
  console.log('[Handler] ========== 处理完成 ==========');
  
  return {
    success: true,
    ...response,
    run_id: subagentResult.runId,
    status: subagentResult.status
  };
}

module.exports = { handleVisitorMessage, setDbPath, getDbPath };
