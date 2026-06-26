/**
 * n8n Integration - n8n 工作流集成主入口
 * 
 * 功能:
 * - Webhook 服务器
 * - Agent 集成
 * - 工作流示例
 * 
 * @version 0.1.0
 * @author 小蒲萄 (Clawd)
 */

const { N8nWebhookServer } = require('./webhook-server');
const { N8nAgentIntegration, ExecutorAdapter } = require('./agent-integration');

class N8nIntegration {
  constructor(options = {}) {
    this.options = {
      port: options.port || 3002,
      verbose: options.verbose || false,
    };

    // 创建 Webhook 服务器
    this.webhookServer = new N8nWebhookServer({
      port: this.options.port,
      verbose: this.options.verbose,
    });

    // 创建 Agent 集成
    this.agentIntegration = new N8nAgentIntegration({
      verbose: this.options.verbose,
    });

    // 设置执行器
    this.webhookServer.setExecutor({
      execute: (workflow, action, params) => 
        this.agentIntegration.execute(workflow, action, params)
    });

    this.log('n8n Integration 初始化完成');
  }

  log(...args) {
    if (this.options.verbose) {
      console.log('[n8n]', ...args);
    }
  }

  /**
   * 启动服务
   */
  async start() {
    await this.webhookServer.start();
    this.log('✅ n8n Integration 已启动');
  }

  /**
   * 停止服务
   */
  async stop() {
    await this.webhookServer.stop();
    this.log('🛑 n8n Integration 已停止');
  }

  /**
   * 设置 Agent 执行器
   */
  setExecutor(executor, type = 'react') {
    const adapter = new ExecutorAdapter(executor, type);
    this.agentIntegration.setExecutor(adapter);
    this.log(`✅ Agent 执行器已设置 (${type})`);
  }

  /**
   * 设置可观测性
   */
  setObservability(observability) {
    this.agentIntegration.setObservability(observability);
    this.log('✅ 可观测性已设置');
  }

  /**
   * 获取 Webhook 服务器
   */
  getWebhookServer() {
    return this.webhookServer;
  }

  /**
   * 获取 Agent 集成
   */
  getAgentIntegration() {
    return this.agentIntegration;
  }
}

// 导出
module.exports = { N8nIntegration, N8nWebhookServer, N8nAgentIntegration, ExecutorAdapter };
