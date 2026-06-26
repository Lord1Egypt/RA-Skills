import axios from 'axios';

// ============================================================
// WorksHub MCP Bridge - CLI 工具调用桥接器
// ============================================================
// 用法: node bridge.js <toolName> <argsJson>
// 示例: node bridge.js get_workers '{"skills":"React","location":"北京"}'
// ============================================================

// 基础域名
const BASE_URL = process.env.WORKSHUB_API_URL || 'https://www.workshub.ai/mcp';
const API_KEY = process.env.WORKSHUB_API_KEY;

// 工具名 + 参数
const toolName = process.argv[2];
const argsJson = process.argv[3] || '{}';

// ============================================================
// 完整工具映射（16个工具，分5个模块）
// ============================================================
const TOOL_MAP = {
  // ==================== 认证工具（2个） ====================
  send_code: {
    method: 'POST',
    path: '/api/v1/auth/send-code',
    description: '发送手机验证码（无需认证）',
  },
  login: {
    method: 'POST',
    path: '/api/v1/auth/login-and-create-key',
    description: '登录并自动创建 API Key（无需认证）',
  },

  // ==================== 技能管理（1个） ====================
  get_skills: {
    method: 'GET',
    path: '/api/v1/skills',
    description: '获取技能列表',
  },

  // ==================== 工作者管理（3个） ====================
  get_workers: {
    method: 'GET',
    path: '/api/v1/workers',
    description: '获取工作者列表（支持技能、地点筛选）',
  },
  get_worker_detail: {
    method: 'GET',
    path: '/api/v1/workers/{workerId}',
    description: '获取工作者详情',
    pathParam: 'workerId',
  },
  get_worker_qrcode: {
    method: 'GET',
    path: '/api/v1/workers/{workerId}',
    description: '获取工作者收款二维码',
    pathParam: 'workerId',
  },

  // ==================== 悬赏任务管理（6个） ====================
  get_bounties: {
    method: 'GET',
    path: '/api/v1/bounties',
    description: '获取悬赏任务列表',
  },
  create_bounty: {
    method: 'POST',
    path: '/api/v1/bounties',
    description: '创建悬赏任务',
  },
  get_bounty_detail: {
    method: 'GET',
    path: '/api/v1/bounties/{bountyId}',
    description: '获取悬赏任务详情',
    pathParam: 'bountyId',
  },
  cancel_bounty: {
    method: 'DELETE',
    path: '/api/v1/bounties/{bountyId}',
    description: '取消悬赏任务',
    pathParam: 'bountyId',
  },
  get_bounty_applications: {
    method: 'GET',
    path: '/api/v1/bounties/{bountyId}/applications',
    description: '获取悬赏任务的申请列表',
    pathParam: 'bountyId',
  },
  accept_bounty_application: {
    method: 'POST',
    path: '/api/v1/bounties/{bountyId}/applications/{applicationId}/accept',
    description: '接受悬赏任务申请',
    pathParams: ['bountyId', 'applicationId'],
  },

  // ==================== 对话管理（4个） ====================
  get_conversations: {
    method: 'GET',
    path: '/api/v1/conversations',
    description: '获取对话列表',
  },
  start_conversation: {
    method: 'POST',
    path: '/api/v1/conversations/start',
    description: '与工作者开始新对话',
  },
  get_conversation_messages: {
    method: 'GET',
    path: '/api/v1/conversations/{conversationId}/messages',
    description: '获取对话消息列表',
    pathParam: 'conversationId',
  },
  send_message: {
    method: 'POST',
    path: '/api/v1/conversations/{conversationId}/messages',
    description: '在对话中发送消息',
    pathParam: 'conversationId',
  },
};

// ============================================================
// 辅助函数
// ============================================================

/**
 * 构建完整 URL（处理路径参数）
 */
function buildUrl(toolConfig, args) {
  let path = toolConfig.path;

  // 处理多个路径参数
  if (toolConfig.pathParams) {
    for (const param of toolConfig.pathParams) {
      if (!args[param]) {
        throw new Error(`缺少路径参数: ${param}`);
      }
      path = path.replace(`{${param}}`, args[param]);
    }
  }
  // 处理单个路径参数
  else if (toolConfig.pathParam) {
    const paramValue = args[toolConfig.pathParam];
    if (!paramValue) {
      throw new Error(`缺少路径参数: ${toolConfig.pathParam}`);
    }
    path = path.replace(`{${toolConfig.pathParam}}`, paramValue);
  }

  return BASE_URL + path;
}

/**
 * 从参数中移除路径参数（避免重复传递）
 */
function removePathParams(toolConfig, args) {
  const result = { ...args };

  if (toolConfig.pathParams) {
    for (const param of toolConfig.pathParams) {
      delete result[param];
    }
  } else if (toolConfig.pathParam) {
    delete result[toolConfig.pathParam];
  }

  return result;
}

// ============================================================
// 主执行函数
// ============================================================
async function run() {
  // 检查工具是否存在
  if (!toolName || !TOOL_MAP[toolName]) {
    console.error('❌ 工具不存在');
    console.error('\n可用工具列表：');
    for (const [name, config] of Object.entries(TOOL_MAP)) {
      console.error(`  - ${name}: ${config.description}`);
    }
    process.exit(1);
  }

  try {
    const toolConfig = TOOL_MAP[toolName];
    const args = JSON.parse(argsJson);

    // 构建请求头
    const headers = {
      'Content-Type': 'application/json',
    };

    // 认证处理
    if (toolConfig.useBearer) {
      // create_api_key 使用 Bearer Token
      if (!args.token) {
        throw new Error('此工具需要 token 参数（Bearer 认证）');
      }
      headers['Authorization'] = `Bearer ${args.token}`;
    } else if (API_KEY) {
      // 其他工具使用 X-API-Key（除了 send_code 和 login 无需认证）
      if (!toolName.startsWith('send_code') && toolName !== 'login') {
        headers['X-API-Key'] = API_KEY;
      }
    }

    // 构建 URL（处理路径参数）
    const url = buildUrl(toolConfig, args);

    // 移除路径参数（避免重复）
    const cleanArgs = removePathParams(toolConfig, args);

    // 执行请求
    const res = await axios({
      method: toolConfig.method,
      url: url,
      headers: headers,
      params: toolConfig.method === 'GET' ? cleanArgs : {},
      data: ['POST', 'PUT', 'PATCH'].includes(toolConfig.method) ? cleanArgs : {},
    });

    console.log('✅ 调用成功：');
    console.log(JSON.stringify(res.data, null, 2));
  } catch (err) {
    console.error('❌ 调用失败：');
    if (err.response) {
      console.error(JSON.stringify(err.response.data, null, 2));
    } else {
      console.error(err.message);
    }
    process.exit(1);
  }
}

// 执行
run();