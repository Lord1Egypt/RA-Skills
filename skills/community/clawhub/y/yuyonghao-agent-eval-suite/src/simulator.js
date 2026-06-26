/**
 * Simulator - 模拟环境测试
 * 提供沙箱环境、场景模拟、边界条件测试和故障注入
 */

const fs = require('fs');
const path = require('path');

class Simulator {
  constructor(options = {}) {
    this.options = {
      scenarios: options.scenarios || './fixtures/scenarios',
      defaultDuration: options.defaultDuration || 60000,
      maxAgents: options.maxAgents || 100,
      ...options
    };
    this.scenarios = new Map();
    this.activeSimulations = new Map();
    this.currentScenario = null;
  }

  /**
   * 加载场景
   * @param {string} scenarioName - 场景名称或路径
   */
  async loadScenario(scenarioName) {
    const scenarioPath = path.isAbsolute(scenarioName) 
      ? scenarioName 
      : path.join(this.options.scenarios, `${scenarioName}.json`);

    try {
      const content = fs.readFileSync(scenarioPath, 'utf-8');
      const scenario = JSON.parse(content);
      
      this.validateScenario(scenario);
      this.scenarios.set(scenario.name || scenarioName, scenario);
      this.currentScenario = scenario;
      
      return scenario;
    } catch (e) {
      // 如果文件不存在，尝试创建内置场景
      const builtIn = this.getBuiltInScenario(scenarioName);
      if (builtIn) {
        this.scenarios.set(scenarioName, builtIn);
        this.currentScenario = builtIn;
        return builtIn;
      }
      throw new Error(`Failed to load scenario "${scenarioName}": ${e.message}`);
    }
  }

  /**
   * 验证场景配置
   */
  validateScenario(scenario) {
    if (!scenario.name) {
      throw new Error('Scenario must have a name');
    }
    
    if (scenario.agents && (typeof scenario.agents !== 'number' || scenario.agents < 1)) {
      throw new Error('Scenario agents must be a positive number');
    }
    
    if (scenario.duration && (typeof scenario.duration !== 'number' || scenario.duration < 1000)) {
      throw new Error('Scenario duration must be at least 1000ms');
    }
  }

  /**
   * 获取内置场景
   */
  getBuiltInScenario(name) {
    const scenarios = {
      'high-load': {
        name: 'high-load',
        description: 'High concurrent agent load test',
        agents: 50,
        duration: 60000,
        requestRate: 100,  // requests per second
        failureRate: 0.01,
        latencyProfile: { min: 50, max: 500, mean: 150 }
      },
      'low-load': {
        name: 'low-load',
        description: 'Low load baseline test',
        agents: 5,
        duration: 30000,
        requestRate: 10,
        failureRate: 0.001,
        latencyProfile: { min: 20, max: 100, mean: 40 }
      },
      'burst-traffic': {
        name: 'burst-traffic',
        description: 'Sudden traffic spike simulation',
        agents: 10,
        duration: 45000,
        requestRate: 10,
        burstProfile: {
          startTime: 15000,
          duration: 10000,
          multiplier: 10
        },
        failureRate: 0.05,
        latencyProfile: { min: 30, max: 800, mean: 200 }
      },
      'error-storm': {
        name: 'error-storm',
        description: 'High error rate simulation',
        agents: 20,
        duration: 30000,
        requestRate: 50,
        failureRate: 0.3,
        latencyProfile: { min: 100, max: 1000, mean: 400 },
        errorTypes: ['timeout', 'connection_refused', 'internal_error']
      },
      'gradual-increase': {
        name: 'gradual-increase',
        description: 'Gradually increasing load',
        agents: 5,
        duration: 120000,
        requestRate: 10,
        rampUp: {
          enabled: true,
          targetAgents: 50,
          rampDuration: 100000
        },
        failureRate: 0.02,
        latencyProfile: { min: 30, max: 300, mean: 80 }
      },
      'chaos': {
        name: 'chaos',
        description: 'Chaos engineering - random failures',
        agents: 30,
        duration: 60000,
        requestRate: 80,
        failureRate: 0.15,
        latencyProfile: { min: 50, max: 2000, mean: 300 },
        chaos: {
          enabled: true,
          faultInjectionRate: 0.1,
          faultTypes: ['delay', 'error', 'timeout', 'memory_pressure']
        }
      }
    };

    return scenarios[name] || null;
  }

  /**
   * 运行模拟
   * @param {object} options - 运行选项
   */
  async run(options = {}) {
    const scenario = this.currentScenario;
    if (!scenario) {
      throw new Error('No scenario loaded. Call loadScenario() first.');
    }

    const config = {
      duration: options.duration || scenario.duration || this.options.defaultDuration,
      agents: options.agents || scenario.agents || 10,
      ...options
    };

    const simulationId = this.generateId();
    const results = {
      simulationId,
      scenario: scenario.name,
      config,
      startTime: Date.now(),
      events: [],
      metrics: {
        totalRequests: 0,
        successfulRequests: 0,
        failedRequests: 0,
        totalErrors: 0,
        latencies: [],
        agentStats: []
      }
    };

    this.activeSimulations.set(simulationId, results);

    try {
      // 创建 agent 池
      const agents = await this.createAgents(config.agents, scenario);
      
      // 运行模拟
      const endTime = Date.now() + config.duration;
      const agentPromises = agents.map(agent => 
        this.runAgent(agent, endTime, scenario, results)
      );

      await Promise.all(agentPromises);

      // 计算最终指标
      results.endTime = Date.now();
      results.duration = results.endTime - results.startTime;
      results.metrics = this.calculateFinalMetrics(results.metrics);
      results.summary = this.generateSummary(results);

    } catch (e) {
      results.error = e.message;
      throw e;
    } finally {
      this.activeSimulations.delete(simulationId);
    }

    return results;
  }

  /**
   * 创建 Agent 池
   */
  async createAgents(count, scenario) {
    const agents = [];
    for (let i = 0; i < count; i++) {
      agents.push({
        id: `agent-${i}`,
        startTime: Date.now(),
        requestsMade: 0,
        errors: 0,
        latencies: []
      });
    }
    return agents;
  }

  /**
   * 运行单个 Agent
   */
  async runAgent(agent, endTime, scenario, results) {
    while (Date.now() < endTime) {
      const shouldInjectFault = this.shouldInjectFault(scenario);
      
      try {
        const startTime = performance.now();
        
        if (shouldInjectFault) {
          await this.injectFault(scenario);
        } else {
          await this.simulateRequest(scenario);
        }
        
        const latency = performance.now() - startTime;
        
        agent.requestsMade++;
        agent.latencies.push(latency);
        results.metrics.totalRequests++;
        results.metrics.successfulRequests++;
        results.metrics.latencies.push(latency);
        
        this.recordEvent(results, 'request', {
          agentId: agent.id,
          latency,
          success: true
        });
        
      } catch (e) {
        agent.errors++;
        results.metrics.totalRequests++;
        results.metrics.failedRequests++;
        results.metrics.totalErrors++;
        
        this.recordEvent(results, 'error', {
          agentId: agent.id,
          error: e.message,
          errorType: e.type || 'unknown'
        });
      }

      // 根据请求率计算等待时间
      const waitTime = this.calculateWaitTime(scenario);
      await this.sleep(waitTime);
    }

    results.metrics.agentStats.push({
      agentId: agent.id,
      requestsMade: agent.requestsMade,
      errors: agent.errors,
      avgLatency: agent.latencies.length > 0 
        ? agent.latencies.reduce((a, b) => a + b, 0) / agent.latencies.length 
        : 0
    });
  }

  /**
   * 模拟请求
   */
  async simulateRequest(scenario) {
    const latency = this.generateLatency(scenario.latencyProfile);
    await this.sleep(latency);

    // 模拟随机失败
    if (Math.random() < (scenario.failureRate || 0)) {
      const errorTypes = scenario.errorTypes || ['error'];
      const errorType = errorTypes[Math.floor(Math.random() * errorTypes.length)];
      const error = new Error(`Simulated ${errorType}`);
      error.type = errorType;
      throw error;
    }
  }

  /**
   * 是否应该注入故障
   */
  shouldInjectFault(scenario) {
    if (!scenario.chaos || !scenario.chaos.enabled) {
      return false;
    }
    return Math.random() < (scenario.chaos.faultInjectionRate || 0.1);
  }

  /**
   * 注入故障
   */
  async injectFault(scenario) {
    const faultTypes = scenario.chaos?.faultTypes || ['error'];
    const faultType = faultTypes[Math.floor(Math.random() * faultTypes.length)];

    switch (faultType) {
      case 'delay':
        await this.sleep(Math.random() * 5000);
        break;
      case 'timeout':
        await this.sleep(30000);
        throw new Error('Timeout');
      case 'memory_pressure':
        // 模拟内存压力
        const buffer = Buffer.alloc(1024 * 1024 * 10); // 10MB
        await this.sleep(100);
        buffer.fill(0);
        break;
      case 'error':
      default:
        throw new Error(`Injected fault: ${faultType}`);
    }
  }

  /**
   * 生成延迟
   */
  generateLatency(profile) {
    if (!profile) return 100;
    
    // 使用正态分布近似
    const mean = profile.mean || 100;
    const stdDev = (profile.max - profile.min) / 6 || 10;
    
    let latency = mean + (Math.random() * 2 - 1) * stdDev * 3;
    latency = Math.max(profile.min || 0, Math.min(profile.max || 1000, latency));
    
    return Math.round(latency);
  }

  /**
   * 计算等待时间
   */
  calculateWaitTime(scenario) {
    const requestRate = scenario.requestRate || 10;
    const baseWait = 1000 / requestRate;
    
    // 添加一些随机性
    const jitter = baseWait * 0.2;
    return Math.max(10, baseWait + (Math.random() * 2 - 1) * jitter);
  }

  /**
   * 记录事件
   */
  recordEvent(results, type, data) {
    results.events.push({
      timestamp: Date.now(),
      type,
      ...data
    });

    // 限制事件数量
    if (results.events.length > 10000) {
      results.events = results.events.slice(-5000);
    }
  }

  /**
   * 计算最终指标
   */
  calculateFinalMetrics(metrics) {
    const latencies = metrics.latencies;
    
    if (latencies.length === 0) {
      return {
        ...metrics,
        latencyStats: null
      };
    }

    const sorted = [...latencies].sort((a, b) => a - b);
    const mean = latencies.reduce((a, b) => a + b, 0) / latencies.length;
    const p50 = sorted[Math.floor(sorted.length * 0.5)];
    const p95 = sorted[Math.floor(sorted.length * 0.95)];
    const p99 = sorted[Math.floor(sorted.length * 0.99)];
    const min = sorted[0];
    const max = sorted[sorted.length - 1];

    return {
      ...metrics,
      latencyStats: {
        mean: Math.round(mean * 100) / 100,
        p50: Math.round(p50 * 100) / 100,
        p95: Math.round(p95 * 100) / 100,
        p99: Math.round(p99 * 100) / 100,
        min: Math.round(min * 100) / 100,
        max: Math.round(max * 100) / 100,
        count: latencies.length
      },
      throughput: Math.round((metrics.totalRequests / (latencies.length > 0 ? latencies.length : 1)) * 100) / 100,
      errorRate: metrics.totalRequests > 0 
        ? Math.round((metrics.failedRequests / metrics.totalRequests) * 10000) / 10000 
        : 0
    };
  }

  /**
   * 生成摘要
   */
  generateSummary(results) {
    const m = results.metrics;
    
    return {
      status: m.errorRate > 0.1 ? 'failed' : m.errorRate > 0.05 ? 'warning' : 'passed',
      totalRequests: m.totalRequests,
      successRate: m.totalRequests > 0 
        ? Math.round((m.successfulRequests / m.totalRequests) * 10000) / 100 
        : 0,
      errorRate: Math.round(m.errorRate * 10000) / 100,
      avgLatency: m.latencyStats?.mean || 0,
      p95Latency: m.latencyStats?.p95 || 0,
      duration: results.duration,
      agents: results.config.agents
    };
  }

  /**
   * 获取当前场景
   */
  getCurrentScenario() {
    return this.currentScenario;
  }

  /**
   * 获取可用场景列表
   */
  getAvailableScenarios() {
    return ['high-load', 'low-load', 'burst-traffic', 'error-storm', 'gradual-increase', 'chaos'];
  }

  /**
   * 生成 ID
   */
  generateId() {
    return `sim-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * 休眠
   */
  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

module.exports = { Simulator };