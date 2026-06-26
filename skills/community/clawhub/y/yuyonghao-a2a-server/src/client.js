/**
 * A2A Client - Agent-to-Agent Communication Client
 * 
 * WebSocket client for connecting to A2A Server
 * Supports:
 * - Agent registration
 * - RPC calls (request/response)
 * - Publish/Subscribe
 * - Capability discovery
 * 
 * @version 0.1.0
 * @author 小蒲萄 (Clawd)
 */

const WebSocket = require('ws');
const { v4: uuidv4 } = require('uuid');

class A2AClient {
  constructor(serverUrl, options = {}) {
    this.options = {
      // Agent 配置
      agentId: options.agentId || `agent-${uuidv4().substr(0, 8)}`,
      capabilities: options.capabilities || [],
      metadata: options.metadata || {},
      // 重连配置
      maxReconnectAttempts: options.maxReconnectAttempts || 10,
      reconnectDelay: options.reconnectDelay || 1000,
      // 超时配置
      callTimeout: options.callTimeout || 30000,
      // 日志
      verbose: options.verbose || false,
    };

    this.serverUrl = serverUrl;
    this.ws = null;
    this.connected = false;
    this.registered = false;
    
    // 响应处理器
    this.responseHandlers = new Map();
    
    // 订阅处理器
    this.messageHandlers = new Map();
    
    // 事件监听器
    this.eventListeners = new Map();
    
    // 重连计数
    this.reconnectAttempts = 0;

    this.log(`🦞 A2A Client 初始化：${this.options.agentId}`);
  }

  log(...args) {
    if (this.options.verbose) {
      console.log(`[A2A:${this.options.agentId}]`, ...args);
    }
  }

  /**
   * 连接到服务器
   */
  connect() {
    return new Promise((resolve, reject) => {
      try {
        this.ws = new WebSocket(this.serverUrl);

        this.ws.on('open', () => {
          this.log('✅ 已连接');
          this.connected = true;
          this.reconnectAttempts = 0;
          
          // 自动注册
          this.register();
          resolve();
        });

        this.ws.on('message', (data) => {
          try {
            const message = JSON.parse(data.toString());
            this.handleMessage(message);
          } catch (error) {
            this.log('❌ 消息解析错误:', error.message);
          }
        });

        this.ws.on('close', () => {
          this.log('🔌 连接关闭');
          this.connected = false;
          this.registered = false;
          
          // 自动重连
          this.reconnect();
        });

        this.ws.on('error', (error) => {
          this.log('❌ 连接错误:', error.message);
          reject(error);
        });
      } catch (error) {
        reject(error);
      }
    });
  }

  /**
   * 断开连接
   */
  disconnect() {
    return new Promise((resolve) => {
      if (this.ws) {
        this.ws.close(1000, 'Client disconnecting');
      }
      
      this.ws = null;
      this.connected = false;
      this.registered = false;
      
      this.log('🛑 已断开');
      resolve();
    });
  }

  /**
   * 重连
   */
  async reconnect() {
    if (this.reconnectAttempts >= this.options.maxReconnectAttempts) {
      this.log(`❌ 重连失败：已达到最大尝试次数 (${this.reconnectAttempts})`);
      this.emit('max-reconnect-reached');
      return;
    }

    this.reconnectAttempts++;
    const delay = this.options.reconnectDelay * this.reconnectAttempts;
    
    this.log(`🔄 重连中... (${this.reconnectAttempts}/${this.options.maxReconnectAttempts}) ${delay}ms 后`);
    this.emit('reconnecting', { attempt: this.reconnectAttempts, delay });

    await new Promise(resolve => setTimeout(resolve, delay));
    
    try {
      await this.connect();
      this.log('✅ 重连成功');
      this.emit('reconnected');
    } catch (error) {
      this.log('❌ 重连失败:', error.message);
    }
  }

  /**
   * 注册 Agent
   */
  register() {
    return new Promise((resolve, reject) => {
      if (!this.connected) {
        reject(new Error('Not connected'));
        return;
      }

      const handler = (message) => {
        if (message.type === 'registered' && message.agentId === this.options.agentId) {
          this.unregisterHandler('register-response', handler);
          this.registered = true;
          this.log(`✅ Agent 注册成功：${this.options.agentId}`);
          this.emit('registered', { agentId: this.options.agentId });
          resolve(message);
        } else if (message.type === 'error') {
          this.unregisterHandler('register-response', handler);
          reject(new Error(message.error));
        }
      };

      this.registerHandler('register-response', handler);

      this.ws.send(JSON.stringify({
        type: 'register',
        agentId: this.options.agentId,
        capabilities: this.options.capabilities,
        metadata: this.options.metadata,
      }));

      this.log(`📝 注册 Agent: ${this.options.agentId}`);
    });
  }

  /**
   * 注销 Agent
   */
  unregister() {
    return new Promise((resolve) => {
      if (!this.registered) {
        resolve();
        return;
      }

      this.ws.send(JSON.stringify({
        type: 'unregister',
        agentId: this.options.agentId,
      }));

      this.registered = false;
      this.log(`🗑️ Agent 注销：${this.options.agentId}`);
      resolve();
    });
  }

  /**
   * 发送原始消息
   */
  send(message) {
    if (!this.ws || !this.connected) {
      throw new Error('Not connected');
    }
    
    this.ws.send(JSON.stringify(message));
    this.log('📤 发送消息:', message.type);
  }

  /**
   * RPC 调用
   */
  call(targetAgentId, payload, options = {}) {
    return new Promise((resolve, reject) => {
      const correlationId = options.correlationId || uuidv4();
      const timeout = options.timeout || this.options.callTimeout;

      const handler = (message) => {
        if (message.type === 'response' && message.correlationId === correlationId) {
          this.unregisterHandler(correlationId, handler);
          
          if (message.error) {
            reject(new Error(message.error));
          } else {
            resolve(message.payload);
          }
        }
      };

      this.registerHandler(correlationId, handler);

      // 设置超时
      const timeoutId = setTimeout(() => {
        this.unregisterHandler(correlationId, handler);
        reject(new Error(`Call timeout (${timeout}ms)`));
      }, timeout);

      // 清理超时时移除 handler
      const originalHandler = handler;
      handler.__timeoutId = timeoutId;
      handler.__originalHandler = originalHandler;

      this.ws.send(JSON.stringify({
        type: 'call',
        from: this.options.agentId,
        to: targetAgentId,
        correlationId,
        payload,
        timestamp: new Date().toISOString()
      }));

      this.log(`📤 调用 ${targetAgentId}: ${correlationId}`);
    });
  }

  /**
   * 发布消息
   */
  publish(channel, payload) {
    return new Promise((resolve, reject) => {
      const handler = (message) => {
        if (message.type === 'published' && message.channel === channel) {
          this.unregisterHandler(`publish-${channel}`, handler);
          resolve(message);
        } else if (message.type === 'error') {
          this.unregisterHandler(`publish-${channel}`, handler);
          reject(new Error(message.error));
        }
      };

      this.registerHandler(`publish-${channel}`, handler);

      this.ws.send(JSON.stringify({
        type: 'publish',
        channel,
        from: this.options.agentId,
        payload,
        timestamp: new Date().toISOString()
      }));

      this.log(`📢 发布到 ${channel}`);
    });
  }

  /**
   * 订阅频道
   */
  subscribe(channel) {
    return new Promise((resolve, reject) => {
      const handler = (message) => {
        if (message.type === 'subscribed' && message.channel === channel) {
          this.unregisterHandler(`subscribe-${channel}`, handler);
          this.log(`📌 已订阅 ${channel}`);
          resolve(message);
        } else if (message.type === 'error') {
          this.unregisterHandler(`subscribe-${channel}`, handler);
          reject(new Error(message.error));
        }
      };

      this.registerHandler(`subscribe-${channel}`, handler);

      this.ws.send(JSON.stringify({
        type: 'subscribe',
        agentId: this.options.agentId,
        channel,
        timestamp: new Date().toISOString()
      }));
    });
  }

  /**
   * 取消订阅
   */
  unsubscribe(channel) {
    this.log(`🔓 取消订阅 ${channel}`);
    // 服务端暂不支持显式取消，客户端移除 handler 即可
    this.messageHandlers.delete(channel);
  }

  /**
   * 能力发现
   */
  discover(options = {}) {
    return new Promise((resolve, reject) => {
      const correlationId = uuidv4();

      const handler = (message) => {
        if (message.type === 'discovery-result' && message.correlationId === correlationId) {
          this.unregisterHandler(correlationId, handler);
          resolve(message.results);
        } else if (message.type === 'error') {
          this.unregisterHandler(correlationId, handler);
          reject(new Error(message.error));
        }
      };

      this.registerHandler(correlationId, handler);

      this.ws.send(JSON.stringify({
        type: 'discover',
        correlationId,
        capability: options.capability,
        filter: options.filter,
        timestamp: new Date().toISOString()
      }));

      this.log(`🔍 能力发现：${options.capability || 'all'}`);
    });
  }

  /**
   * 发送心跳
   */
  heartbeat() {
    if (this.connected && this.registered) {
      this.ws.send(JSON.stringify({
        type: 'heartbeat',
        agentId: this.options.agentId,
        timestamp: new Date().toISOString()
      }));
    }
  }

  /**
   * 注册消息处理器
   */
  registerHandler(key, handler) {
    if (!this.responseHandlers.has(key)) {
      this.responseHandlers.set(key, []);
    }
    this.responseHandlers.get(key).push(handler);
  }

  /**
   * 注销消息处理器
   */
  unregisterHandler(key, handler) {
    const handlers = this.responseHandlers.get(key);
    
    if (!handlers) {
      return;
    }

    if (handler) {
      const index = handlers.indexOf(handler);
      if (index > -1) {
        handlers.splice(index, 1);
        // 清理超时
        if (handler.__timeoutId) {
          clearTimeout(handler.__timeoutId);
        }
      }
    } else {
      // 移除所有 handler
      handlers.forEach(h => {
        if (h.__timeoutId) {
          clearTimeout(h.__timeoutId);
        }
      });
      this.responseHandlers.delete(key);
    }
  }

  /**
   * 处理消息
   */
  handleMessage(message) {
    this.log(`📨 收到消息:`, message.type);

    // 触发事件监听器
    this.emit(message.type, message);

    // 调用响应处理器
    const handlers = this.responseHandlers.get(message.correlationId) ||
                     this.responseHandlers.get(message.type) ||
                     this.responseHandlers.get(message.channel);

    if (handlers) {
      for (const handler of handlers) {
        try {
          handler(message);
        } catch (error) {
          this.log('❌ Handler 错误:', error.message);
        }
      }
    }

    // 特殊处理：频道消息
    if (message.type === 'message' && message.channel) {
      const channelHandlers = this.messageHandlers.get(message.channel);
      if (channelHandlers) {
        for (const handler of channelHandlers) {
          try {
            handler(message.payload, message.from);
          } catch (error) {
            this.log('❌ Channel handler 错误:', error.message);
          }
        }
      }
    }
  }

  /**
   * 事件监听
   */
  on(event, listener) {
    if (!this.eventListeners.has(event)) {
      this.eventListeners.set(event, []);
    }
    this.eventListeners.get(event).push(listener);
  }

  /**
   * 移除事件监听
   */
  off(event, listener) {
    const listeners = this.eventListeners.get(event);
    
    if (!listeners) {
      return;
    }

    if (listener) {
      const index = listeners.indexOf(listener);
      if (index > -1) {
        listeners.splice(index, 1);
      }
    } else {
      this.eventListeners.delete(event);
    }
  }

  /**
   * 一次性事件监听（once）
   */
  once(event, listener) {
    const wrapper = (data) => {
      listener(data);
      this.off(event, wrapper);
    };
    this.on(event, wrapper);
  }

  /**
   * 触发事件
   */
  emit(event, data) {
    const listeners = this.eventListeners.get(event) || [];
    
    for (const listener of listeners) {
      try {
        listener(data);
      } catch (error) {
        this.log('❌ Event listener 错误:', error.message);
      }
    }
  }

  /**
   * 获取状态
   */
  getStatus() {
    return {
      connected: this.connected,
      registered: this.registered,
      serverUrl: this.serverUrl,
      agentId: this.options.agentId,
      reconnectAttempts: this.reconnectAttempts,
    };
  }
}

// 命令行测试
if (require.main === module) {
  const client = new A2AClient('ws://localhost:8080', {
    agentId: 'test-agent',
    capabilities: ['test', 'echo'],
    verbose: true,
  });

  client.connect()
    .then(() => {
      console.log('✅ 连接成功');
      
      // 测试调用
      return client.call('another-agent', { test: 'data' });
    })
    .then(result => {
      console.log('✅ 调用成功:', result);
      return client.disconnect();
    })
    .catch(console.error);
}

// 导出
module.exports = { A2AClient };
