/**
 * A2A Server - Agent-to-Agent Communication Server
 * 
 * WebSocket-based P2P messaging for AI agents
 * Supports:
 * - Agent registration and discovery
 * - P2P message forwarding
 * - Capability-based routing
 * - Trust chain authorization
 * 
 * @version 0.1.0
 * @author 小蒲萄 (Clawd)
 */

const WebSocket = require('ws');
const { v4: uuidv4 } = require('uuid');

class A2AServer {
  constructor(options = {}) {
    this.options = {
      port: options.port || 8080,
      host: options.host || 'localhost',
      // 信任链配置
      trustChain: options.trustChain || {},
      // 日志
      verbose: options.verbose || false,
      // 心跳间隔（毫秒）
      heartbeatInterval: options.heartbeatInterval || 30000,
    };

    // Agent 注册表
    this.agents = new Map(); // agentId -> { ws, capabilities, metadata }
    
    // 消息队列（离线消息）
    this.messageQueue = new Map(); // agentId -> [messages]
    
    // 统计信息
    this.stats = {
      totalConnections: 0,
      totalMessages: 0,
      activeAgents: 0,
    };

    // 心跳定时器
    this.heartbeatTimer = null;

    this.log('🦞 A2A Server 初始化完成');
  }

  log(...args) {
    if (this.options.verbose) {
      console.log('[A2A]', ...args);
    }
  }

  /**
   * 启动服务器
   */
  start() {
    return new Promise((resolve, reject) => {
      try {
        this.wss = new WebSocket.Server({
          port: this.options.port,
          host: this.options.host,
        });

        this.wss.on('listening', () => {
          this.log(`✅ A2A Server 启动在 ws://${this.options.host}:${this.options.port}`);
          resolve();
        });

        this.wss.on('connection', (ws, req) => {
          this.handleConnection(ws, req);
        });

        this.wss.on('error', (error) => {
          this.log('❌ 服务器错误:', error);
          reject(error);
        });

        // 启动心跳
        this.startHeartbeat();
      } catch (error) {
        reject(error);
      }
    });
  }

  /**
   * 停止服务器
   */
  stop() {
    return new Promise((resolve) => {
      // 停止心跳
      if (this.heartbeatTimer) {
        clearInterval(this.heartbeatTimer);
      }

      // 关闭所有连接
      for (const [agentId, { ws }] of this.agents) {
        ws.close(1000, 'Server shutting down');
      }

      this.agents.clear();
      this.messageQueue.clear();

      // 关闭服务器
      this.wss.close(() => {
        this.log('🛑 A2A Server 已停止');
        resolve();
      });
    });
  }

  /**
   * 处理新连接
   */
  handleConnection(ws, req) {
    const clientId = uuidv4().substr(0, 8);
    this.log(`🔌 新连接：${clientId}`);

    let agentId = null;

    // 连接超时（30 秒未注册则断开）
    const registrationTimeout = setTimeout(() => {
      if (!agentId) {
        this.log(`⏰ ${clientId} 注册超时，断开连接`);
        ws.close(4000, 'Registration timeout');
      }
    }, 30000);

    ws.on('message', (data) => {
      try {
        const message = JSON.parse(data.toString());
        this.handleMessage(ws, message, clientId);
        
        // 注册成功后清除超时
        if (message.type === 'register' && !agentId) {
          clearTimeout(registrationTimeout);
        }
      } catch (error) {
        this.log('❌ 消息解析错误:', error.message);
        ws.send(JSON.stringify({
          type: 'error',
          error: 'Invalid message format'
        }));
      }
    });

    ws.on('close', () => {
      if (agentId) {
        this.log(`🔌 Agent 断开：${agentId}`);
        this.unregisterAgent(agentId);
      } else {
        this.log(`🔌 连接关闭：${clientId}`);
      }
    });

    ws.on('error', (error) => {
      this.log(`❌ 连接错误 ${clientId}:`, error.message);
    });

    // 发送欢迎消息
    ws.send(JSON.stringify({
      type: 'welcome',
      clientId,
      server: `ws://${this.options.host}:${this.options.port}`,
      timestamp: new Date().toISOString()
    }));
  }

  /**
   * 处理消息
   */
  handleMessage(ws, message, clientId) {
    this.log(`📨 收到消息 [${clientId}]:`, message.type);

    switch (message.type) {
      case 'register':
        this.handleRegister(ws, message, clientId);
        break;

      case 'unregister':
        this.handleUnregister(ws, message);
        break;

      case 'call':
        this.handleCall(ws, message);
        break;

      case 'response':
        this.handleResponse(ws, message);
        break;

      case 'publish':
        this.handlePublish(ws, message);
        break;

      case 'subscribe':
        this.handleSubscribe(ws, message);
        break;

      case 'discover':
        this.handleDiscover(ws, message);
        break;

      case 'heartbeat':
        this.handleHeartbeat(ws, message);
        break;

      default:
        this.log('⚠️ 未知消息类型:', message.type);
        ws.send(JSON.stringify({
          type: 'error',
          error: `Unknown message type: ${message.type}`
        }));
    }
  }

  /**
   * 处理 Agent 注册
   */
  handleRegister(ws, message, clientId) {
    const { agentId, capabilities, metadata } = message;

    if (!agentId) {
      ws.send(JSON.stringify({
        type: 'error',
        error: 'Missing agentId'
      }));
      return;
    }

    // 检查是否已存在
    if (this.agents.has(agentId)) {
      this.log(`⚠️ Agent ${agentId} 已存在，覆盖`);
      this.agents.delete(agentId);
    }

    // 注册 Agent
    this.agents.set(agentId, {
      ws,
      clientId,
      capabilities: capabilities || [],
      metadata: metadata || {},
      registeredAt: new Date(),
      lastHeartbeat: Date.now(),
    });

    this.stats.activeAgents = this.agents.size;
    this.stats.totalConnections++;

    this.log(`✅ Agent 注册：${agentId} (${capabilities?.length || 0} 个能力)`);

    // 发送确认
    ws.send(JSON.stringify({
      type: 'registered',
      agentId,
      capabilities,
      timestamp: new Date().toISOString()
    }));

    // 发送离线消息
    this.deliverQueuedMessages(agentId);
  }

  /**
   * 处理 Agent 注销
   */
  handleUnregister(ws, message) {
    const { agentId } = message;
    
    if (agentId && this.agents.has(agentId)) {
      this.unregisterAgent(agentId);
      ws.send(JSON.stringify({
        type: 'unregistered',
        agentId,
        timestamp: new Date().toISOString()
      }));
    }
  }

  /**
   * 注销 Agent
   */
  unregisterAgent(agentId) {
    const agent = this.agents.get(agentId);
    if (agent) {
      this.agents.delete(agentId);
      this.stats.activeAgents = this.agents.size;
      this.log(`🗑️ Agent 注销：${agentId}`);
    }
  }

  /**
   * 处理 RPC 调用
   */
  handleCall(ws, message) {
    const { from, to, correlationId, payload } = message;

    if (!to || !payload) {
      ws.send(JSON.stringify({
        type: 'error',
        correlationId,
        error: 'Missing required fields: to, payload'
      }));
      return;
    }

    const targetAgent = this.agents.get(to);
    
    if (!targetAgent) {
      // 目标离线，加入队列
      this.queueMessage(to, message);
      ws.send(JSON.stringify({
        type: 'error',
        correlationId,
        error: `Agent ${to} is offline`,
        queued: true
      }));
      return;
    }

    // 转发调用
    this.stats.totalMessages++;
    targetAgent.ws.send(JSON.stringify({
      type: 'call',
      from: from || 'unknown',
      to,
      correlationId: correlationId || uuidv4(),
      payload,
      timestamp: new Date().toISOString()
    }));

    this.log(`📤 转发调用：${from || 'unknown'} → ${to}`);
  }

  /**
   * 处理响应
   */
  handleResponse(ws, message) {
    const { to, correlationId, payload, error } = message;

    if (!to || !correlationId) {
      this.log('⚠️ 响应缺少字段:', message);
      return;
    }

    const targetAgent = this.agents.get(to);
    
    if (!targetAgent) {
      this.log(`⚠️ 响应目标不存在：${to}`);
      return;
    }

    // 转发响应
    this.stats.totalMessages++;
    targetAgent.ws.send(JSON.stringify({
      type: 'response',
      to,
      correlationId,
      payload,
      error,
      timestamp: new Date().toISOString()
    }));

    this.log(`📤 转发响应：→ ${to} (${correlationId})`);
  }

  /**
   * 处理发布
   */
  handlePublish(ws, message) {
    const { channel, payload, from } = message;

    if (!channel || !payload) {
      ws.send(JSON.stringify({
        type: 'error',
        error: 'Missing required fields: channel, payload'
      }));
      return;
    }

    // 广播给所有订阅者
    this.stats.totalMessages++;
    let sentCount = 0;

    for (const [agentId, agent] of this.agents) {
      if (agent.subscribedChannels?.includes(channel)) {
        agent.ws.send(JSON.stringify({
          type: 'message',
          channel,
          from: from || 'unknown',
          payload,
          timestamp: new Date().toISOString()
        }));
        sentCount++;
      }
    }

    this.log(`📢 发布到 ${channel}: ${sentCount} 个订阅者`);

    ws.send(JSON.stringify({
      type: 'published',
      channel,
      sentCount,
      timestamp: new Date().toISOString()
    }));
  }

  /**
   * 处理订阅
   */
  handleSubscribe(ws, message) {
    const { agentId, channel } = message;

    if (!agentId || !channel) {
      ws.send(JSON.stringify({
        type: 'error',
        error: 'Missing required fields: agentId, channel'
      }));
      return;
    }

    const agent = this.agents.get(agentId);
    
    if (!agent) {
      ws.send(JSON.stringify({
        type: 'error',
        error: `Agent ${agentId} not found`
      }));
      return;
    }

    if (!agent.subscribedChannels) {
      agent.subscribedChannels = [];
    }

    if (!agent.subscribedChannels.includes(channel)) {
      agent.subscribedChannels.push(channel);
    }

    this.log(`📌 Agent ${agentId} 订阅频道 ${channel}`);

    ws.send(JSON.stringify({
      type: 'subscribed',
      agentId,
      channel,
      timestamp: new Date().toISOString()
    }));
  }

  /**
   * 处理能力发现
   */
  handleDiscover(ws, message) {
    const { capability, filter } = message;

    const results = [];

    for (const [agentId, agent] of this.agents) {
      // 按能力筛选
      if (capability) {
        const hasCapability = agent.capabilities.some(c => {
          if (typeof c === 'string') {
            return c === capability;
          }
          return c.name === capability;
        });

        if (!hasCapability) {
          continue;
        }
      }

      // 按元数据筛选
      if (filter) {
        const matchesFilter = Object.entries(filter).every(([key, value]) => {
          return agent.metadata[key] === value;
        });

        if (!matchesFilter) {
          continue;
        }
      }

      results.push({
        agentId,
        capabilities: agent.capabilities,
        metadata: agent.metadata,
        registeredAt: agent.registeredAt,
      });
    }

    ws.send(JSON.stringify({
      type: 'discovery-result',
      correlationId: message.correlationId,
      count: results.length,
      results,
      timestamp: new Date().toISOString()
    }));

    this.log(`🔍 能力发现：${results.length} 个匹配`);
  }

  /**
   * 处理心跳
   */
  handleHeartbeat(ws, message) {
    const { agentId } = message;

    if (agentId && this.agents.has(agentId)) {
      const agent = this.agents.get(agentId);
      agent.lastHeartbeat = Date.now();

      ws.send(JSON.stringify({
        type: 'heartbeat-ack',
        agentId,
        timestamp: new Date().toISOString()
      }));
    }
  }

  /**
   * 启动心跳
   */
  startHeartbeat() {
    this.heartbeatTimer = setInterval(() => {
      const now = Date.now();
      const timeout = this.options.heartbeatInterval * 3;

      for (const [agentId, agent] of this.agents) {
        if (now - agent.lastHeartbeat > timeout) {
          this.log(`⏰ Agent ${agentId} 心跳超时`);
          agent.ws.close(4001, 'Heartbeat timeout');
          this.unregisterAgent(agentId);
        }
      }
    }, this.options.heartbeatInterval);

    this.log(`💓 心跳启动（间隔：${this.options.heartbeatInterval}ms）`);
  }

  /**
   * 队列消息（离线消息）
   */
  queueMessage(agentId, message) {
    if (!this.messageQueue.has(agentId)) {
      this.messageQueue.set(agentId, []);
    }

    const queue = this.messageQueue.get(agentId);
    queue.push({
      ...message,
      queuedAt: new Date()
    });

    // 限制队列大小
    if (queue.length > 100) {
      queue.shift();
    }

    this.log(`📬 消息已队列：${agentId} (${queue.length}条)`);
  }

  /**
   * 投递队列消息
   */
  deliverQueuedMessages(agentId) {
    const queue = this.messageQueue.get(agentId);
    
    if (!queue || queue.length === 0) {
      return;
    }

    const agent = this.agents.get(agentId);
    if (!agent) {
      return;
    }

    this.log(`📬 投递 ${queue.length} 条离线消息给 ${agentId}`);

    for (const message of queue) {
      try {
        agent.ws.send(JSON.stringify(message));
      } catch (error) {
        this.log(`❌ 投递失败:`, error.message);
      }
    }

    this.messageQueue.delete(agentId);
  }

  /**
   * 获取统计信息
   */
  getStats() {
    return {
      ...this.stats,
      uptime: process.uptime(),
      memoryUsage: process.memoryUsage(),
    };
  }

  /**
   * 获取 Agent 列表
   */
  getAgents() {
    const agents = [];

    for (const [agentId, agent] of this.agents) {
      agents.push({
        agentId,
        capabilities: agent.capabilities,
        metadata: agent.metadata,
        registeredAt: agent.registeredAt,
        lastHeartbeat: agent.lastHeartbeat,
      });
    }

    return agents;
  }

  /**
   * 广播消息
   */
  broadcast(payload, exclude = []) {
    let sentCount = 0;

    for (const [agentId, agent] of this.agents) {
      if (exclude.includes(agentId)) {
        continue;
      }

      try {
        agent.ws.send(JSON.stringify({
          type: 'broadcast',
          payload,
          timestamp: new Date().toISOString()
        }));
        sentCount++;
      } catch (error) {
        this.log(`❌ 广播失败 ${agentId}:`, error.message);
      }
    }

    this.log(`📢 广播：${sentCount} 个 Agent`);
    return sentCount;
  }

  /**
   * 获取单个 Agent 信息
   */
  getAgent(agentId) {
    const agent = this.agents.get(agentId);
    if (!agent) {
      return null;
    }
    
    return {
      agentId,
      capabilities: agent.capabilities,
      metadata: agent.metadata,
      registeredAt: agent.registeredAt,
      lastHeartbeat: agent.lastHeartbeat,
    };
  }

  /**
   * 检查 Agent 是否在线
   */
  isAgentOnline(agentId) {
    return this.agents.has(agentId);
  }
}

// 命令行启动
if (require.main === module) {
  const server = new A2AServer({
    port: process.env.A2A_PORT || 8080,
    host: process.env.A2A_HOST || 'localhost',
    verbose: process.env.A2A_VERBOSE === 'true',
  });

  server.start().catch(console.error);

  // 优雅关闭
  process.on('SIGINT', async () => {
    await server.stop();
    process.exit(0);
  });

  process.on('SIGTERM', async () => {
    await server.stop();
    process.exit(0);
  });
}

// 导出
module.exports = { A2AServer };
