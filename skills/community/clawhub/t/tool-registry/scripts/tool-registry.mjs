#!/usr/bin/env node
/**
 * Tool Registry - 工具注册与发现系统
 * 基于Token匹配的工具路由，支持权限控制和子代理工具白名单
 */

import { fileURLToPath, pathToFileURL } from 'url';
import path from 'path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// ============ 常量 ============

const PERMISSION_LEVELS = {
  read: 1,
  write: 2,
  danger: 3,
  admin: 4
};

const DEFAULT_AGENT_TYPES = ['general'];

// ============ 工具注册项 ============

class ToolSpec {
  constructor(config) {
    this.name = config.name;
    this.aliases = config.aliases || [];
    this.description = config.description || '';
    this.permission = config.permission || 'read';
    this.agentTypes = config.agentTypes || DEFAULT_AGENT_TYPES;
    this.keywords = config.keywords || [];
    this.execute = config.execute;
    this.inputSchema = config.inputSchema || null;
    this.outputSchema = config.outputSchema || null;
  }

  /**
   * 检查是否匹配给定权限
   */
  meetsPermission(userLevel) {
    const required = PERMISSION_LEVELS[this.permission] || 1;
    const user = PERMISSION_LEVELS[userLevel] || 1;
    return user >= required;
  }

  /**
   * 检查是否允许指定代理类型使用
   */
  allowsAgentType(agentType) {
    return this.agentTypes.includes(agentType) || this.agentTypes.includes('general');
  }
}

// ============ 匹配结果 ============

class MatchResult {
  constructor(tool, score, matchType) {
    this.tool = tool;
    this.score = score;
    this.matchType = matchType; // 'alias' | 'keyword' | 'description' | 'name'
  }
}

// ============ 工具注册表 ============

class ToolRegistry {
  constructor() {
    this.tools = new Map();
    this.nameIndex = new Map(); // name -> ToolSpec
  }

  /**
   * 注册工具
   */
  register(config) {
    const tool = new ToolSpec(config);
    this.tools.set(tool.name, tool);
    this.nameIndex.set(tool.name.toLowerCase(), tool);

    // 注册别名
    for (const alias of tool.aliases) {
      this.nameIndex.set(alias.toLowerCase(), tool);
    }

    return this;
  }

  /**
   * 批量注册工具
   */
  registerMany(tools) {
    for (const tool of tools) {
      this.register(tool);
    }
    return this;
  }

  /**
   * 获取工具
   */
  get(name) {
    return this.nameIndex.get(name.toLowerCase());
  }

  /**
   * 工具是否存在
   */
  has(name) {
    return this.nameIndex.has(name.toLowerCase());
  }

  /**
   * 提取输入的Token
   * 注意：中文字符不做lowercase处理
   */
  _tokenize(input) {
    if (!input || typeof input !== 'string') {
      return [];
    }
    return input
      .replace(/[/\-]/g, ' ')
      .split(/\s+/)
      .filter(t => t.length > 0);
  }

  /**
   * 计算单个工具的匹配得分
   */
  _scoreTool(tool, tokens) {
    if (tokens.length === 0) {
      return new MatchResult(tool, 0, null);
    }

    let score = 0;
    let matchType = null;

    const nameLower = tool.name.toLowerCase();
    const descLower = tool.description.toLowerCase();
    const aliasLower = tool.aliases.map(a => a.toLowerCase());

    for (const token of tokens) {
      const tokenLower = token.toLowerCase();

      // 别名匹配 (最高权重)
      if (aliasLower.some(a => a === tokenLower || a.includes(tokenLower) || tokenLower.includes(a))) {
        score += 2;
        matchType = 'alias';
      }
      // 关键词匹配
      else if (tool.keywords.some(k => {
        const kLower = k.toLowerCase();
        return kLower === tokenLower || kLower.includes(tokenLower) || tokenLower.includes(kLower);
      })) {
        score += 1;
        matchType = matchType || 'keyword';
      }
      // 名称匹配
      else if (nameLower === tokenLower || nameLower.includes(tokenLower) || tokenLower.includes(nameLower)) {
        score += 1.5;
        matchType = matchType || 'name';
      }
      // 描述匹配 (最低权重)
      else if (descLower.includes(tokenLower)) {
        score += 0.5;
        matchType = matchType || 'description';
      }
    }

    return score > 0 ? new MatchResult(tool, score, matchType) : null;
  }

  /**
   * 搜索工具（Token匹配）
   */
  search(input, options = {}) {
    const tokens = this._tokenize(input);
    const limit = options.limit || 10;
    const agentType = options.agentType;
    const maxPermission = options.permission;

    // 收集所有匹配
    const matches = [];
    const seen = new Set();

    for (const token of tokens) {
      for (const [key, tool] of this.nameIndex) {
        if (seen.has(tool.name)) continue;

        // 权限过滤
        if (maxPermission && !tool.meetsPermission(maxPermission)) {
          continue;
        }

        // 代理类型过滤
        if (agentType && !tool.allowsAgentType(agentType)) {
          continue;
        }

        const score = this._scoreTool(tool, [token]);
        if (score) {
          matches.push(score);
          seen.add(tool.name);
        }
      }
    }

    // 对所有工具进行全Token匹配（如果输入有多个Token）
    if (tokens.length > 1) {
      for (const [name, tool] of this.tools) {
        if (seen.has(tool.name)) continue;

        if (maxPermission && !tool.meetsPermission(maxPermission)) continue;
        if (agentType && !tool.allowsAgentType(agentType)) continue;

        const score = this._scoreTool(tool, tokens);
        if (score) {
          matches.push(score);
          seen.add(tool.name);
        }
      }
    }

    // 如果上面没找到，对每个token尝试关键词匹配（包括中文）
    if (matches.length === 0) {
      for (const token of tokens) {
        for (const [name, tool] of this.tools) {
          if (seen.has(tool.name)) continue;

          if (maxPermission && !tool.meetsPermission(maxPermission)) continue;
          if (agentType && !tool.allowsAgentType(agentType)) continue;

          // 直接检查中文关键词是否在工具描述或关键词中
          const tokenMatchesKeyword = tool.keywords.some(k => 
            k.includes(token) || token.includes(k) ||
            k.toLowerCase().includes(token.toLowerCase()) ||
            token.toLowerCase().includes(k.toLowerCase())
          );
          
          const tokenMatchesDesc = tool.description.includes(token) ||
            tool.description.toLowerCase().includes(token.toLowerCase());

          if (tokenMatchesKeyword || tokenMatchesDesc) {
            const score = this._scoreTool(tool, [token]);
            if (score) {
              matches.push(score);
              seen.add(tool.name);
            }
          }
        }
      }
    }

    // 排序
    matches.sort((a, b) => {
      if (b.score !== a.score) return b.score - a.score;
      return a.tool.name.localeCompare(b.tool.name);
    });

    return matches.slice(0, limit);
  }

  /**
   * 获取所有工具
   */
  list(options = {}) {
    const agentType = options.agentType;
    const maxPermission = options.permission;

    let tools = Array.from(this.tools.values());

    if (agentType) {
      tools = tools.filter(t => t.allowsAgentType(agentType));
    }

    if (maxPermission) {
      tools = tools.filter(t => t.meetsPermission(maxPermission));
    }

    return tools;
  }

  /**
   * 执行工具
   */
  async execute(name, input, context = {}) {
    const tool = this.get(name);
    if (!tool) {
      return {
        success: false,
        error: `Unknown tool: ${name}`,
        availableTools: Array.from(this.tools.keys())
      };
    }

    try {
      const result = await tool.execute(context, input);
      return {
        success: true,
        tool: name,
        result
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
        tool: name
      };
    }
  }

  /**
   * 按权限级别获取工具
   */
  filterByPermission(maxPermission) {
    return this.list({ permission: maxPermission });
  }

  /**
   * 按代理类型获取工具
   */
  filterByAgentType(agentType) {
    return this.list({ agentType });
  }

  /**
   * 获取工具统计
   */
  stats() {
    const permissions = {};
    const agentTypes = {};

    for (const tool of this.tools.values()) {
      permissions[tool.permission] = (permissions[tool.permission] || 0) + 1;

      for (const at of tool.agentTypes) {
        agentTypes[at] = (agentTypes[at] || 0) + 1;
      }
    }

    return {
      totalTools: this.tools.size,
      byPermission: permissions,
      byAgentType: agentTypes
    };
  }
}

// ============ 预定义工具注册表 ============

function createBasicRegistry() {
  const registry = new ToolRegistry();

  registry.registerMany([
    {
      name: 'read_file',
      aliases: ['read', 'cat', 'type'],
      description: '读取文件内容',
      permission: 'read',
      agentTypes: ['explore', 'plan', 'verification', 'general'],
      keywords: ['file', 'read', '文本', '内容', '查看', '读', '文件', '读取'],
      execute: async (ctx, input) => {
        const fs = await import('fs');
        const path = await import('path');
        const filePath = typeof input === 'string' ? input : input.path;
        if (!filePath) throw new Error('path required');
        const content = fs.readFileSync(filePath, 'utf-8');
        return { path: filePath, content, size: content.length };
      }
    },
    {
      name: 'write_file',
      aliases: ['write', 'create', 'save'],
      description: '写入文件内容',
      permission: 'write',
      agentTypes: ['plan', 'general'],
      keywords: ['file', 'write', '创建', '保存', '编辑'],
      execute: async (ctx, input) => {
        const fs = await import('fs');
        const path = await import('path');
        const { file: filePath, content } = typeof input === 'string' ? JSON.parse(input) : input;
        if (!filePath || content === undefined) throw new Error('file and content required');
        fs.writeFileSync(filePath, content, 'utf-8');
        return { path: filePath, bytes: content.length };
      }
    },
    {
      name: 'bash',
      aliases: ['shell', 'exec', 'run'],
      description: '执行Shell命令',
      permission: 'danger',
      agentTypes: ['verification', 'general'],
      keywords: ['shell', 'bash', 'cmd', '命令', '终端', '执行'],
      execute: async (ctx, input) => {
        const { spawn } = await import('child_process');
        const command = typeof input === 'string' ? input : input.command;
        if (!command) throw new Error('command required');

        return new Promise((resolve) => {
          const isWindows = process.platform === 'win32';
          const shell = isWindows ? 'cmd' : '/bin/sh';
          const args = isWindows ? ['/C', command] : ['-c', command];

          const child = spawn(shell, args, { shell: true });
          let stdout = '';
          let stderr = '';

          child.stdout.on('data', (data) => { stdout += data; });
          child.stderr.on('data', (data) => { stderr += data; });

          child.on('close', (code) => {
            resolve({
              command,
              exitCode: code,
              stdout,
              stderr,
              success: code === 0
            });
          });
        });
      }
    },
    {
      name: 'glob',
      aliases: ['find', 'search'],
      description: '搜索文件',
      permission: 'read',
      agentTypes: ['explore', 'plan', 'general'],
      keywords: ['file', 'find', 'glob', '搜索', '查找', '匹配'],
      execute: async (ctx, input) => {
        const { glob } = await import('glob');
        const pattern = typeof input === 'string' ? input : input.pattern;
        if (!pattern) throw new Error('pattern required');
        const files = await glob(pattern);
        return { pattern, files, count: files.length };
      }
    },
    {
      name: 'web_search',
      aliases: ['search', 'google'],
      description: '网络搜索',
      permission: 'read',
      agentTypes: ['plan', 'general'],
      keywords: ['search', 'web', 'google', '搜索', '网络', '查询'],
      execute: async (ctx, input) => {
        // 实际实现需要调用搜索API
        return { query: input.query || input, message: 'Web search not implemented in basic registry' };
      }
    },
    {
      name: 'todo',
      aliases: ['task', 'checklist'],
      description: '待办事项管理',
      permission: 'write',
      agentTypes: ['plan', 'general'],
      keywords: ['todo', 'task', '待办', '任务', '清单'],
      execute: async (ctx, input) => {
        // 简化实现
        return { action: 'todo', input, message: 'Todo management not fully implemented' };
      }
    }
  ]);

  return registry;
}

// ============ 导出 ============

export { ToolRegistry, ToolSpec, MatchResult, PERMISSION_LEVELS, createBasicRegistry };

// ============ CLI 入口 ============

function printHelp() {
  console.log(`
Tool Registry - 工具注册与发现系统
====================================

用法:
  node tool-registry.mjs <command> [options]

命令:
  list [options]       列出所有工具
  search <query>       搜索工具
  get <name>           获取工具详情
  stats                显示统计信息
  exec <name> <input> 执行工具（测试用）

示例:
  node tool-registry.mjs list
  node tool-registry.mjs search "读文件"
  node tool-registry.mjs get read_file
  node tool-registry.mjs stats
`);
}

async function main(args) {
  const registry = createBasicRegistry();

  const cmd = args[0];

  if (cmd === 'list') {
    const tools = registry.list();
    console.log(`\n工具列表 (${tools.length}):\n`);
    for (const tool of tools) {
      console.log(`  ${tool.name}`);
      console.log(`    别名: ${tool.aliases.join(', ') || '-'}`);
      console.log(`    权限: ${tool.permission}`);
      console.log(`    代理: ${tool.agentTypes.join(', ')}`);
      console.log(`    描述: ${tool.description}`);
      console.log();
    }
    return 0;
  }

  if (cmd === 'search') {
    const query = args.slice(1).join(' ');
    if (!query) {
      console.log('请提供搜索关键词');
      return 1;
    }

    const matches = registry.search(query);
    console.log(`\n搜索 "${query}" 的结果:\n`);
    if (matches.length === 0) {
      console.log('  无匹配结果');
    }
    for (const match of matches) {
      console.log(`  ${match.tool.name} (得分: ${match.score}, 类型: ${match.matchType})`);
      console.log(`    ${match.tool.description}`);
      console.log();
    }
    return 0;
  }

  if (cmd === 'get') {
    const name = args[1];
    const tool = registry.get(name);
    if (!tool) {
      console.log(`工具不存在: ${name}`);
      return 1;
    }
    console.log(`\n工具详情: ${tool.name}\n`);
    console.log(`  别名: ${tool.aliases.join(', ') || '-'}`);
    console.log(`  描述: ${tool.description}`);
    console.log(`  权限: ${tool.permission}`);
    console.log(`  代理: ${tool.agentTypes.join(', ')}`);
    console.log(`  关键词: ${tool.keywords.join(', ') || '-'}`);
    return 0;
  }

  if (cmd === 'stats') {
    const stats = registry.stats();
    console.log('\n工具统计:\n');
    console.log(`  总工具数: ${stats.totalTools}`);
    console.log('\n  按权限:');
    for (const [perm, count] of Object.entries(stats.byPermission)) {
      console.log(`    ${perm}: ${count}`);
    }
    console.log('\n  按代理类型:');
    for (const [type, count] of Object.entries(stats.byAgentType)) {
      console.log(`    ${type}: ${count}`);
    }
    return 0;
  }

  printHelp();
  return 0;
}

// CLI 入口（仅在直接运行时执行）
const isMain = import.meta.url === pathToFileURL(process.argv[1]).href;
if (isMain) {
  const args = process.argv.slice(2);
  if (args[0] === '--help' || args[0] === '-h') {
    printHelp();
  } else {
    main(args).then(code => process.exit(code));
  }
}
