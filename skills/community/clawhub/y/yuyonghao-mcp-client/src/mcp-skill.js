#!/usr/bin/env node
// OpenClaw MCP 技能接口
// 将 MCP client 集成到 OpenClaw 技能系统

import { SecureMCPClient } from './secure-client.js';
import { MCPClientConfig, MCPServerConfig } from './client.js';
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

/**
 * OpenClaw MCP 技能主类
 * 提供命令行和 API 两种使用方式
 */
export class OpenClawMCPSkill {
  constructor(options = {}) {
    this.client = new SecureMCPClient(
      new MCPClientConfig({
        name: 'openclaw-mcp-skill',
        version: '0.1.0',
        autoApprove: options.autoApprove ?? false
      }),
      {
        requireApproval: options.requireApproval ?? true,
        autoApprovePatterns: options.autoApprovePatterns || [],
        blockedPatterns: options.blockedPatterns || ['*:delete_*']
      }
    );
    
    this.configFile = join(__dirname, 'mcp-config.json');
    this.loadConfig();
  }

  /**
   * 加载配置
   */
  loadConfig() {
    try {
      if (existsSync(this.configFile)) {
        const config = readFileSync(this.configFile, 'utf-8');
        this.servers = JSON.parse(config);
      } else {
        this.servers = this.getDefaultConfig();
        this.saveConfig();
      }
    } catch (error) {
      console.warn(`[MCP] 加载配置失败，使用默认配置：${error.message}`);
      this.servers = this.getDefaultConfig();
    }
  }

  /**
   * 获取默认配置
   */
  getDefaultConfig() {
    return {
      filesystem: {
        id: 'filesystem',
        name: 'Filesystem Server',
        type: 'stdio',
        command: 'npx',
        args: ['-y', '@modelcontextprotocol/server-filesystem', '.'],
        description: '本地文件系统访问'
      },
      github: {
        id: 'github',
        name: 'GitHub Server',
        type: 'stdio',
        command: 'npx',
        args: ['-y', '@modelcontextprotocol/server-github'],
        env: {
          GITHUB_TOKEN: process.env.GITHUB_TOKEN || ''
        },
        description: 'GitHub API 集成'
      }
    };
  }

  /**
   * 保存配置
   */
  saveConfig() {
    try {
      writeFileSync(this.configFile, JSON.stringify(this.servers, null, 2));
    } catch (error) {
      console.warn(`[MCP] 保存配置失败：${error.message}`);
    }
  }

  /**
   * 添加服务器配置
   */
  addServer(serverConfig) {
    this.servers[serverConfig.id] = serverConfig;
    this.saveConfig();
    console.log(`已添加服务器：${serverConfig.name}`);
  }

  /**
   * 移除服务器配置
   */
  removeServer(serverId) {
    delete this.servers[serverId];
    this.saveConfig();
    console.log(`已移除服务器：${serverId}`);
  }

  /**
   * 列出已配置的服务器
   */
  listServers() {
    console.log('已配置的 MCP 服务器:');
    Object.entries(this.servers).forEach(([id, server]) => {
      console.log(`  - ${id}: ${server.name} (${server.description})`);
    });
    return this.servers;
  }

  /**
   * 连接到服务器
   */
  async connect(serverId) {
    const server = this.servers[serverId];
    if (!server) {
      throw new Error(`未找到服务器配置：${serverId}`);
    }

    console.log(`正在连接到 ${server.name}...`);
    await this.client.connect(server);
    console.log(`已连接到 ${server.name}`);

    return this.getServerInfo(serverId);
  }

  /**
   * 断开服务器连接
   */
  async disconnect(serverId) {
    await this.client.disconnect(serverId);
    console.log(`已断开连接：${serverId}`);
  }

  /**
   * 获取服务器信息
   */
  async getServerInfo(serverId) {
    const capabilities = await this.client.getServerCapabilities(serverId);
    
    return {
      id: serverId,
      name: this.servers[serverId].name,
      tools: capabilities.tools?.length || 0,
      resources: capabilities.resources?.length || 0,
      prompts: capabilities.prompts?.length || 0,
      toolList: capabilities.tools?.map(t => ({
        name: t.name,
        description: t.description
      }))
    };
  }

  /**
   * 列出工具
   */
  async listTools(serverId) {
    return await this.client.listTools(serverId);
  }

  /**
   * 调用工具
   */
  async callTool(serverId, toolName, args, requireApproval = true) {
    console.log(`调用工具：${serverId}:${toolName}`);
    const result = await this.client.callTool(serverId, toolName, args, requireApproval);
    console.log(`工具调用成功`);
    return result;
  }

  /**
   * 读取文件（filesystem server 快捷方法）
   */
  async readFile(filePath) {
    return await this.callTool('filesystem', 'read_file', {
      path: filePath
    });
  }

  /**
   * 列出目录（filesystem server 快捷方法）
   */
  async listDirectory(dirPath) {
    return await this.callTool('filesystem', 'list_directory', {
      path: dirPath
    });
  }

  /**
   * 搜索文件（filesystem server 快捷方法）
   */
  async searchFiles(pattern) {
    return await this.callTool('filesystem', 'search_files', {
      pattern
    });
  }

  /**
   * 创建 Issue（GitHub server 快捷方法）
   */
  async createIssue(owner, repo, title, body = '', labels = []) {
    return await this.callTool('github', 'create_issue', {
      owner,
      repo,
      title,
      body,
      labels
    });
  }

  /**
   * 搜索仓库（GitHub server 快捷方法）
   */
  async searchRepositories(query, limit = 10) {
    return await this.callTool('github', 'search_repositories', {
      query,
      limit
    });
  }

  /**
   * 批准工具
   */
  approveTool(serverId, toolName, permanent = false) {
    this.client.approveTool(serverId, toolName, permanent);
    console.log(`工具已批准：${serverId}:${toolName}`);
  }

  /**
   * 获取审计日志
   */
  getAuditLog(limit = 100) {
    return this.client.getAuditLog(limit);
  }

  /**
   * 获取错误统计
   */
  getErrorStats() {
    return this.client.getErrorStats();
  }

  /**
   * 关闭所有连接
   */
  async closeAll() {
    await this.client.closeAll();
    console.log('所有连接已关闭');
  }
}

/**
 * 命令行接口
 */
async function cli() {
  const args = process.argv.slice(2);
  const skill = new OpenClawMCPSkill({ 
    autoApprove: true,
    requireApproval: false,
    autoApprovePatterns: ['*']
  });

  try {
    const command = args[0];

    switch (command) {
      case 'list':
        skill.listServers();
        break;

      case 'connect':
        if (!args[1]) {
          console.error('用法：mcp connect <server-id>');
          process.exit(1);
        }
        const info = await skill.connect(args[1]);
        console.log('服务器信息:', JSON.stringify(info, null, 2));
        break;

      case 'tools':
        if (!args[1]) {
          console.error('用法：mcp tools <server-id>');
          process.exit(1);
        }
        const tools = await skill.listTools(args[1]);
        console.log('可用工具:');
        tools.forEach(t => {
          console.log(`  - ${t.name}: ${t.description || '无描述'}`);
        });
        break;

      case 'call':
        if (args.length < 4) {
          console.error('用法：mcp call <server-id> <tool-name> [args-json]');
          process.exit(1);
        }
        const toolArgs = args[3] ? JSON.parse(args[3]) : {};
        const result = await skill.callTool(args[1], args[2], toolArgs);
        console.log('执行结果:', JSON.stringify(result, null, 2));
        break;

      case 'read':
        if (!args[1]) {
          console.error('用法：mcp read <file-path>');
          process.exit(1);
        }
        const content = await skill.readFile(args[1]);
        console.log('文件内容:', content.content?.[0]?.text);
        break;

      case 'ls':
        const dir = args[1] || '.';
        const listing = await skill.listDirectory(dir);
        console.log('目录内容:');
        console.log(listing.content?.[0]?.text);
        break;

      case 'search':
        if (!args[1]) {
          console.error('用法：mcp search <pattern>');
          process.exit(1);
        }
        const searchResult = await skill.searchFiles(args[1]);
        console.log('搜索结果:');
        console.log(searchResult.content?.[0]?.text);
        break;

      case 'audit':
        const logs = skill.getAuditLog(20);
        console.log('审计日志:');
        logs.forEach(log => {
          console.log(`  [${log.timestamp.toISOString()}] ${log.action}: ${JSON.stringify(log.details)}`);
        });
        break;

      case 'help':
      default:
        console.log(`
OpenClaw MCP 技能 v0.1.0

用法：
  mcp list                    # 列出已配置的服务器
  mcp connect <server-id>     # 连接到服务器
  mcp tools <server-id>       # 列出可用工具
  mcp call <server> <tool> [args]  # 调用工具
  mcp read <file-path>        # 读取文件
  mcp ls [dir-path]           # 列出目录
  mcp search <pattern>        # 搜索文件
  mcp audit                   # 查看审计日志
  mcp help                    # 显示帮助

示例：
  mcp connect filesystem
  mcp tools filesystem
  mcp read ./package.json
  mcp ls ./src
  mcp search "*.js"
  mcp call github create_issue '{"owner":"user","repo":"repo","title":"Bug"}'
        `);
        break;
    }
  } catch (error) {
    console.error('错误:', error.message);
    if (error.code) {
      console.error('错误码:', error.code);
    }
    process.exit(1);
  } finally {
    await skill.closeAll();
  }
}

// 如果直接运行，执行 CLI
if (process.argv[1]?.endsWith('mcp-skill.js')) {
  cli();
}

// 导出默认实例
export const mcpSkill = new OpenClawMCPSkill();