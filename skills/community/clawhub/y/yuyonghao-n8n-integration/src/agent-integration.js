/**
 * n8n Agent Integration - n8n 与 OpenClaw Agent 集成层
 * 
 * 功能:
 * - 包装 Agent 执行函数
 * - 支持 n8n 数据格式
 * - 错误处理
 * - 超时控制
 * - 可观测性集成
 * 
 * @version 0.1.0
 * @author 小蒲萄 (Clawd)
 */

class N8nAgentIntegration {
  constructor(options = {}) {
    this.options = {
      // 执行器（ReAct/Multi-Agent 等）
      executor: options.executor || null,
      // 可观测性系统
      observability: options.observability || null,
      // 超时配置
      timeout: options.timeout || 30000,
      // 重试配置
      retries: options.retries || 0,
      // 日志
      verbose: options.verbose || false,
    };

    this.log('n8n Agent Integration 初始化完成');
  }

  log(...args) {
    if (this.options.verbose) {
      console.log('[n8n-agent]', ...args);
    }
  }

  /**
   * 执行 Agent（包装版本）
   */
  async execute(workflow, action, params) {
    const startTime = Date.now();
    let trace = null;

    // 开始追踪（如果有可观测性）
    if (this.options.observability) {
      trace = this.options.observability.startTrace('n8n.workflow', {
        workflow,
        action,
        params
      });
    }

    try {
      this.log(`⚙️ 执行工作流：${workflow} (${action})`);

      // 执行 Agent
      let result;
      if (this.options.executor) {
        result = await this._executeWithTimeout(action, params);
      } else {
        throw new Error('Executor not configured');
      }

      // 记录成功
      if (trace) {
        trace.end({ success: true, result });
      }

      this.log(`✅ 执行成功：${workflow} (${action})`);

      return {
        success: true,
        workflow,
        action,
        result,
        duration: Date.now() - startTime,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      this.log(`❌ 执行失败：${error.message}`);

      // 记录错误
      if (trace) {
        trace.end({ success: false, error: error.message });
      }

      if (this.options.observability) {
        this.options.observability.recordError(error, {
          workflow,
          action,
          params
        });
      }

      return {
        success: false,
        workflow,
        action,
        error: error.message,
        duration: Date.now() - startTime,
        timestamp: new Date().toISOString()
      };
    }
  }

  /**
   * 带超时执行
   */
  async _executeWithTimeout(action, params) {
    const timeoutPromise = new Promise((_, reject) => {
      setTimeout(() => {
        reject(new Error(`Execution timeout (${this.options.timeout}ms)`));
      }, this.options.timeout);
    });

    const executionPromise = this._executeWithRetries(action, params);

    return Promise.race([executionPromise, timeoutPromise]);
  }

  /**
   * 带重试执行
   */
  async _executeWithRetries(action, params) {
    let lastError;

    for (let i = 0; i <= this.options.retries; i++) {
      try {
        return await this.options.executor.execute(action, params);
      } catch (error) {
        lastError = error;
        this.log(`⚠️ 执行失败 (尝试 ${i + 1}/${this.options.retries + 1}): ${error.message}`);
        
        if (i < this.options.retries) {
          // 等待后重试（指数退避）
          const delay = Math.pow(2, i) * 1000;
          await new Promise(resolve => setTimeout(resolve, delay));
        }
      }
    }

    throw lastError;
  }

  /**
   * 设置执行器
   */
  setExecutor(executor) {
    this.options.executor = executor;
    this.log('✅ 执行器已设置');
  }

  /**
   * 设置可观测性
   */
  setObservability(observability) {
    this.options.observability = observability;
    this.log('✅ 可观测性已设置');
  }
}

/**
 * 执行器适配器（适配 ReAct/Multi-Agent 等）
 */
class ExecutorAdapter {
  constructor(executor, type = 'react') {
    this.executor = executor;
    this.type = type;
  }

  async execute(action, params) {
    switch (this.type) {
      case 'react':
        return this._executeReAct(action, params);
      case 'multi-agent':
        return this._executeMultiAgent(action, params);
      default:
        throw new Error(`Unknown executor type: ${this.type}`);
    }
  }

  async _executeReAct(action, params) {
    // ReAct Orchestrator 执行
    const result = await this.executor.execute(params.query || action, {
      mode: 'auto',
      ...params
    });

    return {
      answer: result.answer,
      mode: result.mode,
      duration: result.duration,
      iterations: result.iterations
    };
  }

  async _executeMultiAgent(action, params) {
    // Multi-Agent Orchestrator 执行
    const result = await this.executor.executeTask(params.task || action);

    return {
      result: result,
      success: true
    };
  }
}

// 导出
module.exports = { N8nAgentIntegration, ExecutorAdapter };
