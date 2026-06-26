#!/usr/bin/env node
/**
 * Yunxiao MCP CLI
 * 
 * Command-line interface for Yunxiao (阿里云云效) integration.
 * Uses the alibabacloud-devops-mcp-server under the hood.
 * 
 * Usage: node yunxiao-mcp.cjs <command> [args...]
 * 
 * Commands:
 *   get_organizations              Get organization list
 *   get_current_user               Get current user info
 *   search_projects [keyword]      Search projects
 *   get_work_item <id>             Get work item details
 *   search_workitems <spaceId> [options]  Search work items
 *   get_comments <id> [page] [perPage]  Get work item comments
 *   create_comment <id> <content>  Create a comment
 *   search_members <keyword>       Search organization members
 */

const { spawn } = require('child_process');

const { resolveOrgId } = require('./org-id.cjs');

// Environment configuration
const ACCESS_TOKEN = process.env.YUNXIAO_ACCESS_TOKEN;
const ORG_ID = process.env.YUNXIAO_ORG_ID;
const ORG_ID_ERROR = 'Cannot determine organization ID. Set YUNXIAO_ORG_ID, pass [orgId], or run get_organizations first.';

// 状态ID映射（常用状态）
const STATUS_MAP = {
  'pending_confirmation': '28',
  'pending_processing': '100005',
  'reopened': '30',
  'deferred_fix': '34',
  'confirmed': '32',
  'selected': '625489',
  'in_analysis': '154395',
  'analysis_complete': '165115',
  'in_progress': '100010',
  'in_design': '156603',
  'design_complete': '307012',
  'in_development': '142838',
  'development_complete': '100011',
  'in_testing': '100012'
};

// 工作项类型映射
const CATEGORY_MAP = {
  'req': 'Req',      // 需求
  'task': 'Task',    // 任务
  'bug': 'Bug',      // 缺陷
  'risk': 'Risk',    // 风险
  'epic': 'Epic'     // 史诗
};

/**
 * Call Yunxiao MCP server
 */
function callMCP(requests) {
  return new Promise((resolve, reject) => {
    const server = spawn('npx', ['-y', 'alibabacloud-devops-mcp-server'], {
      env: { ...process.env, YUNXIAO_ACCESS_TOKEN: ACCESS_TOKEN },
      stdio: ['pipe', 'pipe', 'inherit']
    });

    let buffer = '';
    const responses = [];

    server.stdout.on('data', (data) => {
      buffer += data.toString();
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';
      
      for (const line of lines) {
        if (line.trim()) {
          try {
            responses.push(JSON.parse(line));
          } catch (e) {
            // Ignore invalid JSON lines
          }
        }
      }
    });

    server.on('close', () => resolve(responses));
    server.on('error', reject);

    // Initialize MCP connection
    server.stdin.write(JSON.stringify({
      jsonrpc: '2.0',
      id: 0,
      method: 'initialize',
      params: {
        protocolVersion: '2024-11-05',
        capabilities: {},
        clientInfo: { name: 'yunxiao-cli', version: '1.0.0' }
      }
    }) + '\n');

    // Send tool calls
    for (let i = 0; i < requests.length; i++) {
      server.stdin.write(JSON.stringify({ jsonrpc: '2.0', id: i + 1, ...requests[i] }) + '\n');
    }
    
    server.stdin.end();
    
    // Timeout after 30 seconds
    setTimeout(() => {
      server.kill();
      resolve(responses);
    }, 30000);
  });
}

/**
 * Extract content from MCP response
 */
function extractContent(response) {
  if (response.result?.content?.[0]?.text) {
    try {
      return JSON.parse(response.result.content[0].text);
    } catch {
      return response.result.content[0].text;
    }
  }
  if (response.error) {
    return { error: response.error };
  }
  return response;
}

/**
 * Get organization ID (from env or auto-detect)
 */
async function getOrgId(explicitOrgId) {
  const orgs = await getOrganizations();
  return resolveOrgId({
    explicitOrgId,
    envOrgId: ORG_ID,
    organizations: Array.isArray(orgs) ? orgs : []
  });
}

/**
 * Call a Yunxiao tool and return the result
 */
async function callTool(toolName, args) {
  const responses = await callMCP([
    { method: 'tools/call', params: { name: toolName, arguments: args } }
  ]);
  
  for (const resp of responses) {
    if (resp.id === 1) {
      return extractContent(resp);
    }
  }
  return { error: 'No response from MCP server' };
}

// ==================== API Functions ====================

async function getOrganizations() {
  return callTool('get_user_organizations', {});
}

async function getCurrentUser(orgId) {
  const finalOrgId = await getOrgId(orgId);
  if (!finalOrgId) {
    return { error: ORG_ID_ERROR };
  }
  return callTool('get_current_user', { organizationId: finalOrgId });
}

async function searchProjects(keyword, orgId) {
  const finalOrgId = await getOrgId(orgId);
  if (!finalOrgId) {
    return { error: ORG_ID_ERROR };
  }
  const args = { organizationId: finalOrgId };
  if (keyword) args.keyword = keyword;
  return callTool('search_projects', args);
}

async function getWorkItem(workItemId, orgId) {
  const finalOrgId = await getOrgId(orgId);
  if (!finalOrgId) {
    return { error: ORG_ID_ERROR };
  }
  return callTool('get_work_item', { organizationId: finalOrgId, workItemId });
}

/**
 * 搜索工作项
 * 
 * @param {string} spaceId - 项目ID（必填）
 * @param {object} options - 搜索选项
 * @param {string} options.category - 工作项类型: req, task, bug, risk, epic
 * @param {string} options.status - 状态ID或状态名
 * @param {string} options.assignedTo - 指派人ID，'self' 表示当前用户
 * @param {string} options.creator - 创建人ID，'self' 表示当前用户
 * @param {string} options.subject - 标题关键词
 * @param {string} options.sprint - 迭代ID
 * @param {number} options.page - 页码
 * @param {number} options.perPage - 每页条数
 * @param {boolean} options.includeDetails - 是否包含详情
 */
async function searchWorkitems(spaceId, options = {}, orgId) {
  const finalOrgId = await getOrgId(orgId);
  if (!finalOrgId) {
    return { error: ORG_ID_ERROR };
  }
  
  // 解析 category
  let category = options.category || 'Req';
  if (CATEGORY_MAP[category.toLowerCase()]) {
    category = CATEGORY_MAP[category.toLowerCase()];
  }
  
  // 构建参数
  const args = {
    organizationId: finalOrgId,
    spaceId,
    spaceType: 'Project',
    category
  };
  
  // 添加可选参数
  if (options.status) {
    // 支持状态名或状态ID
    args.status = STATUS_MAP[options.status.toLowerCase()] || options.status;
  }
  if (options.assignedTo) args.assignedTo = options.assignedTo;
  if (options.creator) args.creator = options.creator;
  if (options.subject) args.subject = options.subject;
  if (options.sprint) args.sprint = options.sprint;
  if (options.page) args.page = parseInt(options.page);
  if (options.perPage) args.perPage = parseInt(options.perPage);
  if (options.includeDetails) args.includeDetails = true;
  if (options.orderBy) args.orderBy = options.orderBy;
  if (options.sort) args.sort = options.sort;
  
  return callTool('search_workitems', args);
}

async function getComments(workItemId, orgId, page = 1, perPage = 20) {
  const finalOrgId = await getOrgId(orgId);
  if (!finalOrgId) {
    return { error: ORG_ID_ERROR };
  }
  return callTool('list_work_item_comments', {
    organizationId: finalOrgId,
    workItemId,
    page: parseInt(page) || 1,
    perPage: parseInt(perPage) || 20
  });
}

async function createComment(workItemId, content, orgId) {
  const finalOrgId = await getOrgId(orgId);
  if (!finalOrgId) {
    return { error: ORG_ID_ERROR };
  }
  return callTool('create_work_item_comment', {
    organizationId: finalOrgId,
    workItemId,
    content
  });
}

async function searchMembers(keyword, orgId) {
  const finalOrgId = await getOrgId(orgId);
  if (!finalOrgId) {
    return { error: ORG_ID_ERROR };
  }
  return callTool('search_organization_members', {
    organizationId: finalOrgId,
    keyword
  });
}

// ==================== CLI ====================

function printError(message) {
  console.error(JSON.stringify({ error: message }, null, 2));
}

function printHelp() {
  console.error(`
Yunxiao CLI - Yunxiao (阿里云云效) integration

Usage: node yunxiao-mcp.cjs <command> [args...]

Commands:
  get_organizations                    Get organization list
  get_current_user                     Get current user info
  search_projects [keyword]            Search projects
  get_work_item <workItemId>           Get work item details
  search_workitems <spaceId> [options] Search work items
  get_comments <workItemId> [page] [perPage]  Get work item comments
  create_comment <workItemId> <content>       Create a comment
  search_members <keyword>             Search organization members

Search Work Items Options (JSON format):
  category     Work item type: req, task, bug, risk, epic (default: req)
  status       Status ID or name (e.g., "pending_processing", "in_progress")
  assignedTo   Assignee user ID, use "self" for current user
  creator      Creator user ID, use "self" for current user
  subject      Title keyword
  sprint       Sprint ID
  page         Page number (default: 1)
  perPage      Items per page (default: 20, max: 200)
  includeDetails  Include full details (default: false)

Environment Variables:
  YUNXIAO_ACCESS_TOKEN  (required) Your Yunxiao access token
  YUNXIAO_ORG_ID        (optional) Default organization ID

Organization Resolution Order:
  1. Explicit [orgId] argument
  2. YUNXIAO_ORG_ID environment variable
  3. First organization returned by get_organizations

Examples:
  # Get organizations
  YUNXIAO_ACCESS_TOKEN=xxx node yunxiao-mcp.cjs get_organizations

  # Get current user
  YUNXIAO_ACCESS_TOKEN=xxx node yunxiao-mcp.cjs get_current_user

  # Search projects
  YUNXIAO_ACCESS_TOKEN=xxx node yunxiao-mcp.cjs search_projects "keyword"
  
  # Get work item
  YUNXIAO_ACCESS_TOKEN=xxx node yunxiao-mcp.cjs get_work_item PROJ-12345

  # Search work items assigned to me
  YUNXIAO_ACCESS_TOKEN=xxx node yunxiao-mcp.cjs search_workitems <projectId> '{"assignedTo":"self"}'

  # Search pending requirements
  YUNXIAO_ACCESS_TOKEN=xxx node yunxiao-mcp.cjs search_workitems <projectId> '{"category":"req","status":"pending_processing"}'

  # Search with pagination
  YUNXIAO_ACCESS_TOKEN=xxx node yunxiao-mcp.cjs search_workitems <projectId> '{"perPage":50,"page":1}'
`);
}

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  // Check for help flag
  if (!command || command === '-h' || command === '--help') {
    printHelp();
    process.exit(0);
  }

  // Check for access token
  if (!ACCESS_TOKEN) {
    printError('YUNXIAO_ACCESS_TOKEN environment variable is required');
    process.exit(1);
  }

  let result;

  switch (command) {
    case 'get_organizations':
      result = await getOrganizations();
      break;

    case 'get_current_user':
      result = await getCurrentUser(args[1]);
      break;

    case 'search_projects':
      result = await searchProjects(args[1], args[2]);
      break;

    case 'get_work_item':
      if (!args[1]) {
        printError('Usage: get_work_item <workItemId> [orgId]');
        process.exit(1);
      }
      result = await getWorkItem(args[1], args[2]);
      break;

    case 'search_workitems':
      if (!args[1]) {
        printError('Usage: search_workitems <spaceId> [optionsJson] [orgId]');
        process.exit(1);
      }
      const options = args[2] ? JSON.parse(args[2]) : {};
      result = await searchWorkitems(args[1], options, args[3]);
      break;

    case 'get_comments':
      if (!args[1]) {
        printError('Usage: get_comments <workItemId> [orgId] [page] [perPage]');
        process.exit(1);
      }
      result = await getComments(args[1], args[2], args[3], args[4]);
      break;

    case 'create_comment':
      if (!args[1] || !args[2]) {
        printError('Usage: create_comment <workItemId> <content> [orgId]');
        process.exit(1);
      }
      result = await createComment(args[1], args[2], args[3]);
      break;

    case 'search_members':
      if (!args[1]) {
        printError('Usage: search_members <keyword> [orgId]');
        process.exit(1);
      }
      result = await searchMembers(args[1], args[2]);
      break;

    default:
      printError(`Unknown command: ${command}`);
      console.error('Run with --help for usage information');
      process.exit(1);
  }

  console.log(JSON.stringify(result, null, 2));
}

main().catch(err => {
  printError(err.message);
  process.exit(1);
});