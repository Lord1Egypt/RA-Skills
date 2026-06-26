/**
 * Agent Metacognition - Main Entry Point
 * 元认知系统
 */

const { SelfMonitor } = require('./self-monitor');
const { ReflectionEngine } = require('./reflection');

class MetacognitionSystem {
  constructor(options = {}) {
    this.options = options;
    this.monitor = new SelfMonitor(options.monitor);
    this.reflection = new ReflectionEngine(options.reflection);
    this.state = {
      awareness: 0.5,
      strategy: 'default',
      load: 0
    };
  }

  async monitorExecution(fn, context) {
    return await this.monitor.monitor(fn, context);
  }

  async reflect(executionId) {
    return await this.reflection.analyze(executionId);
  }

  getMetacognitiveState() {
    return this.state;
  }
}

module.exports = {
  MetacognitionSystem,
  SelfMonitor,
  ReflectionEngine
};
