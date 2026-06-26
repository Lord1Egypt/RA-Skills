/**
 * Agent Eval Suite - 主入口
 * 提供基准测试、A/B 测试、性能回归检测和模拟环境测试能力
 */

const { Benchmark } = require('./benchmark');
const { ABTester } = require('./ab-tester');
const { RegressionDetector } = require('./regression-detector');
const { Simulator } = require('./simulator');
const { ReportGenerator } = require('./report-generator');

class AgentEvalSuite {
  constructor(options = {}) {
    this.options = {
      dataDir: options.dataDir || './eval-data',
      verbose: options.verbose || false,
      ...options
    };
    
    this.benchmark = new Benchmark(options.benchmark);
    this.abTester = new ABTester(options.abTest);
    this.regressionDetector = new RegressionDetector(options.regression);
    this.simulator = new Simulator(options.simulator);
    this.reportGenerator = new ReportGenerator(options.report);
  }

  /**
   * 获取基准测试实例
   */
  getBenchmark() {
    return this.benchmark;
  }

  /**
   * 获取 A/B 测试实例
   */
  getABTester() {
    return this.abTester;
  }

  /**
   * 获取回归检测实例
   */
  getRegressionDetector() {
    return this.regressionDetector;
  }

  /**
   * 获取模拟器实例
   */
  getSimulator() {
    return this.simulator;
  }

  /**
   * 获取报告生成器实例
   */
  getReportGenerator() {
    return this.reportGenerator;
  }

  /**
   * 运行完整评估套件
   */
  async runFullSuite(tests) {
    const results = {
      timestamp: new Date().toISOString(),
      summary: {},
      details: {}
    };

    if (tests.benchmark) {
      results.details.benchmark = await this.benchmark.run();
    }

    if (tests.abTest) {
      results.details.abTest = await this.abTester.runAll();
    }

    if (tests.regression) {
      results.details.regression = this.regressionDetector.detect();
    }

    if (tests.simulator) {
      results.details.simulator = await this.simulator.run(tests.simulator);
    }

    results.summary = this.generateSummary(results.details);
    return results;
  }

  generateSummary(details) {
    const summary = {
      totalTests: 0,
      passed: 0,
      failed: 0,
      warnings: 0
    };

    for (const [key, value] of Object.entries(details)) {
      if (value && typeof value === 'object') {
        if (value.summary) {
          summary.totalTests += value.summary.total || 0;
          summary.passed += value.summary.passed || 0;
          summary.failed += value.summary.failed || 0;
          summary.warnings += value.summary.warnings || 0;
        }
      }
    }

    return summary;
  }
}

module.exports = {
  AgentEvalSuite,
  Benchmark,
  ABTester,
  RegressionDetector,
  Simulator,
  ReportGenerator
};
