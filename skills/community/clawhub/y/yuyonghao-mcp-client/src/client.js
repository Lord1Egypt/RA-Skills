// MCP Client for OpenClaw
// 基于官方 MCP TypeScript SDK 实现 - 完整版

import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import { SSEClientTransport } from '@modelcontextprotocol/sdk/client/sse.js';

// MCP 客户端配置
export class MCPClientConfig {
  constructor(options = {}) {
    this.name = options.name || 'openclaw-mcp-client';
    this.version = options.version || '0.1.0';
    this.timeout = options.timeout || 30000;
    this.autoApprove = options.autoApprove || false;
    this.retryAttempts = options.retryAttempts || 3;
    this.retryDelay = options.retryDelay || 1000;
  }
}

// MCP 服务器连接配置
export class MCPServerConfig {
  constructor(options) {
    this.id = options.id;
    this.name = options.name;
    this.type = options.type;
    this.command = options.command;
    this.args = options.args || [];
    this.url = options.url;
    this.env = options.env || {};
    this.description = options.description || '';
    this.capabilities = options.capabilities || {};
    this.headers = options.headers || {};
  }
}

// MCP 连接状态
export const ConnectionState = {
  DISCONNECTED: 'disconnected',
  CONNECTING: 'connecting',
  CONNECTED: 'connected',
  ERROR: 'error'
};

// MCP 错误类
export class MCPError extends Error {
  constructor(message, code, details = {}) {
    super(message);
    this.name = 'MCPError';
    this.code = code;
    this.details = details;
    this.timestamp = new Date();
  }
}

// MCP 连接错误类
export class MCPConnectionError extends MCPError {
  constructor(message, serverId, originalError = null) {
    super(message, 'CONNECTION_FAILED', { serverId, originalError });
    this.serverId = serverId;
  }
}

// MCP 客户端主类
export class MCPClient {
  constructor(config = new MCPClientConfig()) {
    this.config = config;
    this.connections = new Map();
    this.approvedTools = new Set();
    this.approvedResources = new Set();
    this.eventHandlers = new Map();
  }

  // 创建传输层
  createTransport(serverConfig) {
    switch (serverConfig.type) {
      case 'stdio':
        return new StdioClientTransport({
          command: serverConfig.command,
          args: serverConfig.args,
          env: { ...process.env, ...serverConfig.env }
        });
      
      case 'sse':
        const url = new URL(serverConfig.url);
        return new SSEClientTransport(url, { headers: serverConfig.headers });
      
      default:
        throw new MCPError(`不支持的传输类型：${serverConfig.type}`, 'UNSUPPORTED_TRANSPORT');
    }
  }

  // 连接到 MCP 服务器
  async connect(serverConfig) {
    console.log(`[MCP] 正在连接到服务器：${serverConfig.name} (${serverConfig.id})`);
    
    if (this.connections.has(serverConfig.id)) {
      console.log(`[MCP] 服务器 ${serverConfig.id} 已连接，复用现有连接`);
      return this.connections.get(serverConfig.id).client;
    }

    try {
      const transport = this.createTransport(serverConfig);
      const client = new Client(
        { name: this.config.name, version: this.config.version },
        { capabilities: { tools: {}, resources: {}, prompts: {} } }
      );

      await client.connect(transport);
      
      this.connections.set(serverConfig.id, {
        client,
        config: serverConfig,
        connectedAt: new Date()
      });

      console.log(`[MCP] 已连接到服务器：${serverConfig.name}`);
      this.emit('connected', { serverId: serverConfig.id, config: serverConfig });

      return client;
    } catch (error) {
      throw new MCPConnectionError(`连接失败：${error.message}`, serverConfig.id, error);
    }
  }

  // 断开与服务器的连接
  async disconnect(serverId) {
    const connection = this.connections.get(serverId);
    if (connection) {
      try {
        await connection.client.close();
        console.log(`[MCP] 已断开连接：${serverId}`);
      } catch (error) {
        console.warn(`[MCP] 断开连接时出错：${error.message}`);
      }
      this.connections.delete(serverId);
      this.emit('disconnected', { serverId });
    }
  }

  // 获取服务器能力
  async getServerCapabilities(serverId) {
    const connection = this.connections.get(serverId);
    if (!connection) {
      throw new MCPError(`未找到连接：${serverId}`, 'CONNECTION_NOT_FOUND');
    }

    const capabilities = { tools: [], resources: [], prompts: [], resourceTemplates: [] };
    
    try {
      const tools = await connection.client.listTools();
      capabilities.tools = tools.tools || [];
    } catch (e) {}

    try {
      const resources = await connection.client.listResources();
      capabilities.resources = resources.resources || [];
      capabilities.resourceTemplates = resources.resourceTemplates || [];
    } catch (e) {}

    try {
      const prompts = await connection.client.listPrompts();
      capabilities.prompts = prompts.prompts || [];
    } catch (e) {}

    return capabilities;
  }

  // 列出可用工具
  async listTools(serverId) {
    const connection = this.connections.get(serverId);
    if (!connection) {
      throw new MCPError(`未找到连接：${serverId}`, 'CONNECTION_NOT_FOUND');
    }
    const result = await connection.client.listTools();
    return result.tools || [];
  }

  // 调用工具
  async callTool(serverId, toolName, args, requireApproval = true) {
    const connection = this.connections.get(serverId);
    if (!connection) {
      throw new MCPError(`未找到连接：${serverId}`, 'CONNECTION_NOT_FOUND');
    }

    const toolKey = `${serverId}:${toolName}`;
    if (requireApproval && !this.approvedTools.has(toolKey) && !this.config.autoApprove) {
      console.warn(`[MCP] 工具调用需要批准：${toolName}`);
    }

    console.log(`[MCP] 调用工具：${toolName}`, args);
    
    try {
      const result = await connection.client.callTool({
        name: toolName,
        arguments: args
      });
      this.emit('toolCalled', { serverId, toolName, args, result });
      return result;
    } catch (error) {
      throw new MCPError(
        `工具执行失败：${error.message}`,
        'TOOL_EXECUTION_FAILED',
        { serverId, toolName, originalError: error }
      );
    }
  }

  // 列出可用资源
  async listResources(serverId) {
    const connection = this.connections.get(serverId);
    if (!connection) {
      throw new MCPError(`未找到连接：${serverId}`, 'CONNECTION_NOT_FOUND');
    }
    const result = await connection.client.listResources();
    return result.resources || [];
  }

  // 读取资源
  async readResource(serverId, resourceUri, requireApproval = true) {
    const connection = this.connections.get(serverId);
    if (!connection) {
      throw new MCPError(`未找到连接：${serverId}`, 'CONNECTION_NOT_FOUND');
    }

    if (requireApproval && !this.approvedResources.has(resourceUri) && !this.config.autoApprove) {
      console.warn(`[MCP] 资源访问需要批准：${resourceUri}`);
    }

    console.log(`[MCP] 读取资源：${resourceUri}`);
    
    try {
      const result = await connection.client.readResource({ uri: resourceUri });
      this.emit('resourceRead', { serverId, resourceUri, result });
      return result;
    } catch (error) {
      throw new MCPError(
        `资源读取失败：${error.message}`,
        'RESOURCE_READ_FAILED',
        { serverId, resourceUri, originalError: error }
      );
    }
  }

  // 列出可用提示词
  async listPrompts(serverId) {
    const connection = this.connections.get(serverId);
    if (!connection) {
      throw new MCPError(`未找到连接：${serverId}`, 'CONNECTION_NOT_FOUND');
    }
    const result = await connection.client.listPrompts();
    return result.prompts || [];
  }

  // 获取提示词
  async getPrompt(serverId, promptName, args = {}) {
    const connection = this.connections.get(serverId);
    if (!connection) {
      throw new MCPError(`未找到连接：${serverId}`, 'CONNECTION_NOT_FOUND');
    }

    try {
      const result = await connection.client.getPrompt({
        name: promptName,
        arguments: args
      });
      this.emit('promptRetrieved', { serverId, promptName, args, result });
      return result;
    } catch (error) {
      throw new MCPError(
        `获取提示词失败：${error.message}`,
        'PROMPT_RETRIEVAL_FAILED',
        { serverId, promptName, originalError: error }
      );
    }
  }

  // 批准工具
  approveTool(serverId, toolName) {
    const toolKey = `${serverId}:${toolName}`;
    this.approvedTools.add(toolKey);
    console.log(`[MCP] 工具已批准：${toolName}`);
  }

  // 批准资源
  approveResource(resourceUri) {
    this.approvedResources.add(resourceUri);
    console.log(`[MCP] 资源已批准：${resourceUri}`);
  }

  // 获取所有连接状态
  getConnectionStatus() {
    const status = [];
    for (const [id, connection] of this.connections.entries()) {
      status.push({
        id,
        name: connection.config.name,
        connectedAt: connection.connectedAt,
        duration: Date.now() - connection.connectedAt.getTime()
      });
    }
    return status;
  }

  // 关闭所有连接
  async closeAll() {
    console.log(`[MCP] 正在关闭所有连接...`);
    const closePromises = [];
    for (const [id, connection] of this.connections.entries()) {
      closePromises.push(connection.client.close());
    }
    await Promise.all(closePromises);
    this.connections.clear();
    console.log(`[MCP] 所有连接已关闭`);
  }

  // 事件监听
  on(event, handler) {
    if (!this.eventHandlers.has(event)) {
      this.eventHandlers.set(event, []);
    }
    this.eventHandlers.get(event).push(handler);
  }

  // 触发事件
  emit(event, data) {
    const handlers = this.eventHandlers.get(event);
    if (handlers) {
      handlers.forEach(handler => {
        try {
          handler(data);
        } catch (error) {
          console.error(`[MCP] 事件处理器错误：${error.message}`);
        }
      });
    }
  }

  // 带重试的执行
  async withRetry(fn, errorCode, errorMessage) {
    let lastError;
    
    for (let attempt = 0; attempt < this.config.retryAttempts; attempt++) {
      try {
        return await fn();
      } catch (error) {
        lastError = error;
        
        if (error instanceof MCPError) {
          throw error;
        }
        
        if (attempt < this.config.retryAttempts - 1) {
          const delay = Math.min(
            this.config.retryDelay * Math.pow(2, attempt),
            10000
          );
          console.warn(`[MCP] 尝试 ${attempt + 1}/${this.config.retryAttempts} 失败，${delay}ms 后重试...`);
          await this.sleep(delay);
        }
      }
    }
    
    throw new MCPError(
      errorMessage,
      errorCode,
      { originalError: lastError?.message, attempts: this.config.retryAttempts }
    );
  }

  // 睡眠工具
  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// 导出默认实例
export const mcpClient = new MCPClient();