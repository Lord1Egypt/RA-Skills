/**
 * Benchmark - 基准测试框架
 * 提供标准化测试用例、多维度评估指标和基准对比
 */

class Benchmark {
  constructor(options = {}) {
    this.options = {
      iterations: options.iterations || 100,
      warmup: options.warmup || 10,
      timeout: options.timeout || 30000,
      ...options
    };
    this.tests = new Map();
    this.results = new Map();
  }

  /**
   * 添加测试用例
   * @param {string} name - 测试名称
   * @param {object} config - 测试配置
   * @param {function} config.setup - 初始化函数
   * @param {function} config.execute - 执行函数
   * @param {function} config.teardown - 清理函数
   */
  addTest(name, config) {
    if (!config.execute || typeof config.execute !== 'function') {
      throw new Error(`Test "${name}" must have an execute function`);
    }

    this.tests.set(name, {
      name,
      setup: config.setup || (() => {}),
      execute: config.execute,
      teardown: config.teardown || (() => {}),
      iterations: config.iterations || this.options.iterations,
      warmup: config.warmup || this.options.warmup
    });
  }

  /**
   * 移除测试用例
   */
  removeTest(name) {
    this.tests.delete(name);
    this.results.delete(name);
  }

  /**
   * 运行所有测试
   */
  async run(testNames) {
    const namesToRun = testNames || Array.from(this.tests.keys());
    const results = {};

    for (const name of namesToRun) {
      if (this.tests.has(name)) {
        results[name] = await this.runSingleTest(name);
      }
    }

    return results;
  }

  /**
   * 运行单个测试
   */
  async runSingleTest(name) {
    const test = this.tests.get(name);
    if (!test) {
      throw new Error(`Test "${name}" not found`);
    }

    const measurements = [];
    const errors = [];
    let agent;

    try {
      // Warmup phase
      agent = await test.setup();
      for (let i = 0; i < test.warmup; i++) {
        try {
          await this.runWithTimeout(test.execute(agent), this.options.timeout);
        } catch (e) {
          // Ignore warmup errors
        }
      }
      await test.teardown(agent);

      // Actual test phase
      for (let i = 0; i < test.iterations; i++) {
        agent = await test.setup();
        const startTime = performance.now();
        let success = false;

        try {
          await this.runWithTimeout(test.execute(agent), this.options.timeout);
          success = true;
        } catch (e) {
          errors.push({ iteration: i, error: e.message });
        }

        const endTime = performance.now();
        measurements.push({
          duration: endTime - startTime,
          success,
          iteration: i
        });

        await test.teardown(agent);
      }

      const result = this.calculateMetrics(measurements, errors);
      this.results.set(name, result);
      return result;

    } catch (e) {
      throw new Error(`Test "${name}" failed: ${e.message}`);
    }
  }

  /**
   * 带超时的运行
   */
  async runWithTimeout(promise, timeout) {
    return Promise.race([
      promise,
      new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Timeout')), timeout)
      )
    ]);
  }

  /**
   * 计算性能指标
   */
  calculateMetrics(measurements, errors) {
    const successfulMeasurements = measurements.filter(m => m.success);
    const durations = successfulMeasurements.map(m => m.duration);
    
    if (durations.length === 0) {
      return {
        mean: 0,
        median: 0,
        p95: 0,
        p99: 0,
        min: 0,
        max: 0,
        stdDev: 0,
        successRate: 0,
        totalIterations: measurements.length,
        successfulIterations: 0,
        failedIterations: measurements.length,
        errors: errors.map(e => e.error)
      };
    }

    const sorted = [...durations].sort((a, b) => a - b);
    const mean = durations.reduce((a, b) => a + b, 0) / durations.length;
    const median = this.calculatePercentile(sorted, 50);
    const p95 = this.calculatePercentile(sorted, 95);
    const p99 = this.calculatePercentile(sorted, 99);
    const min = sorted[0];
    const max = sorted[sorted.length - 1];
    const variance = durations.reduce((acc, val) => acc + Math.pow(val - mean, 2), 0) / durations.length;
    const stdDev = Math.sqrt(variance);

    return {
      mean: Math.round(mean * 100) / 100,
      median: Math.round(median * 100) / 100,
      p95: Math.round(p95 * 100) / 100,
      p99: Math.round(p99 * 100) / 100,
      min: Math.round(min * 100) / 100,
      max: Math.round(max * 100) / 100,
      stdDev: Math.round(stdDev * 100) / 100,
      successRate: Math.round((successfulMeasurements.length / measurements.length) * 100) / 100,
      totalIterations: measurements.length,
      successfulIterations: successfulMeasurements.length,
      failedIterations: measurements.length - successfulMeasurements.length,
      errors: errors.map(e => e.error).slice(0, 10) // Keep first 10 errors
    };
  }

  /**
   * 计算百分位数
   */
  calculatePercentile(sorted, percentile) {
    const index = Math.ceil((percentile / 100) * sorted.length) - 1;
    return sorted[Math.max(0, index)];
  }

  /**
   * 与基准对比
   */
  compareToBaseline(testName, baseline) {
    const current = this.results.get(testName);
    if (!current) {
      throw new Error(`No results found for test "${testName}"`);
    }

    const comparison = {
      testName,
      metrics: {}
    };

    for (const [metric, baselineValue] of Object.entries(baseline)) {
      if (current[metric] !== undefined) {
        const currentValue = current[metric];
        const change = baselineValue !== 0 
          ? ((currentValue - baselineValue) / baselineValue) 
          : 0;
        
        comparison.metrics[metric] = {
          baseline: baselineValue,
          current: currentValue,
          change: Math.round(change * 100) / 100,
          changePercent: Math.round(change * 10000) / 100
        };
      }
    }

    return comparison;
  }

  /**
   * 获取所有测试结果
   */
  getResults() {
    return Object.fromEntries(this.results);
  }

  /**
   * 清空测试结果
   */
  clearResults() {
    this.results.clear();
  }

  /**
   * 获取测试列表
   */
  getTestList() {
    return Array.from(this.tests.keys());
  }
}

module.exports = { Benchmark };
