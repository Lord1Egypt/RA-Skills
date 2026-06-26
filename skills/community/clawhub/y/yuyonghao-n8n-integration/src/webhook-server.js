/**
 * n8n Webhook Server - n8n 工作流触发服务器
 * 
 * 功能:
 * - 接收 n8n Webhook 请求
 * - 验证请求签名/Token
 * - 触发 Agent 执行
 * - 回调 n8n 结果
 * 
 * @version 0.1.0
 * @author 小蒲萄 (Clawd)
 */

const express = require('express');
const crypto = require('crypto');
const path = require('path');

class N8nWebhookServer {
  constructor(options = {}) {
    this.options = {
      // 服务器配置
      port: options.port || 3002,
      host: options.host || 'localhost',
      // 认证配置
      authToken: options.authToken || process.env.N8N_AUTH_TOKEN || 'n8n-webhook-token',
      // 回调配置
      callbackTimeout: options.callbackTimeout || 30000,
      // 日志
      verbose: options.verbose || false,
      // Agent 执行器（外部注入）
      executor: options.executor || null,
    };

    this.app = express();
    this.app.use(express.json());

    // 请求日志
    if (this.options.verbose) {
      this.app.use((req, res, next) => {
        console.log(`[n8n] ${req.method} ${req.path}`);
        next();
      });
    }

    // 注册路由
    this._registerRoutes();

    this.log('n8n Webhook Server 初始化完成');
  }

  log(...args) {
    if (this.options.verbose) {
      console.log('[n8n]', ...args);
    }
  }

  /**
   * 注册路由
   */
  _registerRoutes() {
    // 健康检查
    this.app.get('/health', (req, res) => {
      res.json({
        status: 'ok',
        timestamp: new Date().toISOString(),
        service: 'n8n-webhook-server'
      });
    });

    // n8n Webhook 触发端点
    this.app.post('/webhook/trigger', async (req, res) => {
      try {
        await this._handleTrigger(req, res);
      } catch (error) {
        this.log('❌ Webhook 触发失败:', error.message);
        res.status(500).json({
          success: false,
          error: error.message
        });
      }
    });

    // n8n 回调端点（接收 Agent 执行结果）
    this.app.post('/webhook/callback', async (req, res) => {
      try {
        await this._handleCallback(req, res);
      } catch (error) {
        this.log('❌ 回调处理失败:', error.message);
        res.status(500).json({
          success: false,
          error: error.message
        });
      }
    });

    // 状态端点
    this.app.get('/status', (req, res) => {
      res.json({
        status: 'running',
        port: this.options.port,
        authToken: this.options.authToken ? '***' : 'none',
        executor: this.options.executor ? 'configured' : 'none'
      });
    });
  }

  /**
   * 验证请求
   */
  _verifyRequest(req) {
    const token = req.headers['x-n8n-token'] || req.query.token;
    
    if (!token) {
      throw new Error('Missing authentication token');
    }

    if (token !== this.options.authToken) {
      throw new Error('Invalid authentication token');
    }

    return true;
  }

  /**
   * 处理 Webhook 触发
   */
  async _handleTrigger(req, res) {
    // 验证请求
    this._verifyRequest(req);

    const { workflow, action, params, callbackUrl } = req.body;

    if (!workflow || !action) {
      throw new Error('Missing required fields: workflow, action');
    }

    this.log(`📨 收到工作流触发：${workflow} (${action})`);

    // 执行 Agent
    let result;
    try {
      if (this.options.executor) {
        result = await this.options.executor.execute(workflow, action, params);
      } else {
        // 默认执行器（模拟）
        result = await this._defaultExecutor(action, params);
      }
    } catch (error) {
      this.log('❌ Agent 执行失败:', error.message);
      result = {
        success: false,
        error: error.message
      };
    }

    // 回调 n8n
    if (callbackUrl) {
      await this._callbackToN8n(callbackUrl, { workflow, action, result });
    }

    // 返回结果
    res.json({
      success: true,
      workflow,
      action,
      result,
      timestamp: new Date().toISOString()
    });
  }

  /**
   * 处理回调
   */
  async _handleCallback(req, res) {
    this._verifyRequest(req);

    const { workflow, action, result } = req.body;

    this.log(`📥 收到回调：${workflow} (${action})`);

    // 存储结果（用于监控/日志）
    this._storeResult(workflow, action, result);

    res.json({
      success: true,
      received: true
    });
  }

  /**
   * 默认执行器（模拟）
   */
  async _defaultExecutor(action, params) {
    this.log(`⚙️ 执行默认操作：${action}`);
    
    // 模拟执行延迟
    await new Promise(resolve => setTimeout(resolve, 100));

    return {
      success: true,
      message: `Executed ${action}`,
      data: params,
      timestamp: new Date().toISOString()
    };
  }

  /**
   * 回调 n8n
   */
  async _callbackToN8n(callbackUrl, data) {
    this.log(`📤 回调 n8n: ${callbackUrl}`);

    try {
      const response = await fetch(callbackUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-N8N-Token': this.options.authToken
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error(`Callback failed: ${response.status}`);
      }

      const result = await response.json();
      this.log('✅ 回调成功');
      return result;
    } catch (error) {
      this.log('❌ 回调失败:', error.message);
      throw error;
    }
  }

  /**
   * 存储结果（简化版，内存存储）
   */
  _storeResult(workflow, action, result) {
    if (!this.results) {
      this.results = new Map();
    }

    const key = `${workflow}-${action}-${Date.now()}`;
    this.results.set(key, {
      workflow,
      action,
      result,
      timestamp: new Date().toISOString()
    });

    // 限制存储数量
    if (this.results.size > 100) {
      const firstKey = this.results.keys().next().value;
      this.results.delete(firstKey);
    }
  }

  /**
   * 获取结果历史
   */
  getResults(limit = 10) {
    if (!this.results) {
      return [];
    }

    return Array.from(this.results.values())
      .slice(-limit)
      .reverse();
  }

  /**
   * 启动服务器
   */
  start() {
    return new Promise((resolve, reject) => {
      this.server = this.app.listen(this.options.port, this.options.host, () => {
        this.log(`✅ n8n Webhook Server 启动在 http://${this.options.host}:${this.options.port}`);
        this.log(`   Endpoints:`);
        this.log(`   - POST /webhook/trigger  - n8n 触发端点`);
        this.log(`   - POST /webhook/callback - 回调端点`);
        this.log(`   - GET  /health          - 健康检查`);
        this.log(`   - GET  /status          - 状态信息`);
        resolve();
      });

      this.server.on('error', (error) => {
        this.log('❌ 服务器错误:', error.message);
        reject(error);
      });
    });
  }

  /**
   * 停止服务器
   */
  stop() {
    return new Promise((resolve) => {
      if (this.server) {
        this.server.close(() => {
          this.log('🛑 n8n Webhook Server 已停止');
          resolve();
        });
      } else {
        resolve();
      }
    });
  }

  /**
   * 设置执行器
   */
  setExecutor(executor) {
    this.options.executor = executor;
    this.log('✅ 执行器已设置');
  }
}

// 命令行启动
if (require.main === module) {
  const server = new N8nWebhookServer({
    port: process.env.N8N_PORT || 3002,
    verbose: process.env.N8N_VERBOSE === 'true',
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
module.exports = { N8nWebhookServer };
