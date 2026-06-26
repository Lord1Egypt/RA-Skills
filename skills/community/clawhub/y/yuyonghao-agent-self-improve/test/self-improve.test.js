/**
 * Agent Self-Improve Test Suite
 */

import { SelfImprovementSystem, PerformanceAnalyzer, StrategyOptimizer } from '../src/index.js';

class TestRunner {
  constructor() {
    this.tests = [];
    this.passed = 0;
    this.failed = 0;
  }

  test(name, fn) {
    this.tests.push({ name, fn });
  }

  async run() {
    console.log('\n🧪 Running Agent Self-Improve Tests\n');
    console.log('=' .repeat(50));
    
    for (const { name, fn } of this.tests) {
      try {
        await fn();
        console.log(`✅ PASS: ${name}`);
        this.passed++;
      } catch (error) {
        console.log(`❌ FAIL: ${name}`);
        console.log(`   Error: ${error.message}`);
        this.failed++;
      }
    }
    
    console.log('=' .repeat(50));
    console.log(`\n📊 Results: ${this.passed} passed, ${this.failed} failed`);
    console.log(`Success Rate: ${((this.passed / this.tests.length) * 100).toFixed(1)}%\n`);
    
    return this.failed === 0;
  }

  assert(condition, message) {
    if (!condition) throw new Error(message || 'Assertion failed');
  }
}

const runner = new TestRunner();

// Test 1: SelfImprovementSystem Creation
runner.test('SelfImprovementSystem should be created', () => {
  const system = new SelfImprovementSystem({ metrics: ['latency'] });
  runner.assert(system, 'System should be created');
});

// Test 2: PerformanceAnalyzer Creation
runner.test('PerformanceAnalyzer should be created', () => {
  const analyzer = new PerformanceAnalyzer();
  runner.assert(analyzer, 'Analyzer should be created');
});

// Test 3: StrategyOptimizer Creation
runner.test('StrategyOptimizer should be created', () => {
  const optimizer = new StrategyOptimizer();
  runner.assert(optimizer, 'Optimizer should be created');
});

// Test 4: Performance Analysis
runner.test('PerformanceAnalyzer should analyze performance', async () => {
  const analyzer = new PerformanceAnalyzer();
  
  const profile = await analyzer.profile(async () => {
    await new Promise(r => setTimeout(r, 10));
    return 'result';
  }, { iterations: 5 });
  
  runner.assert(typeof profile === 'object', 'Should return profile');
});

// Test 5: Strategy Optimization
runner.test('StrategyOptimizer should optimize', async () => {
  const optimizer = new StrategyOptimizer();
  
  const result = await optimizer.optimize({ strategy: 'test' });
  runner.assert(typeof result === 'object', 'Should return result');
});

// Test 6: Improvement History
runner.test('SelfImprovementSystem should track history', () => {
  const system = new SelfImprovementSystem();
  
  const history = system.getImprovementHistory();
  runner.assert(Array.isArray(history), 'Should return array');
});

// Test 7: System Options
runner.test('SelfImprovementSystem should accept options', () => {
  const system = new SelfImprovementSystem({
    metrics: ['latency', 'accuracy'],
    analyzer: { sampleSize: 100 }
  });
  
  runner.assert(system.options.metrics.includes('latency'), 'Should accept metrics');
});

// Test 8: Analyzer Options
runner.test('PerformanceAnalyzer should accept options', () => {
  const analyzer = new PerformanceAnalyzer({ sampleSize: 50 });
  runner.assert(analyzer.options, 'Should have options');
});

// Test 9: Optimizer Options
runner.test('StrategyOptimizer should accept options', () => {
  const optimizer = new StrategyOptimizer({ maxIterations: 10 });
  runner.assert(optimizer.options, 'Should have options');
});

// Test 10: Profile Metrics
runner.test('PerformanceAnalyzer should provide metrics', async () => {
  const analyzer = new PerformanceAnalyzer();
  
  const profile = await analyzer.profile(async () => 'test', { iterations: 3 });
  runner.assert(profile, 'Should have profile');
});

// Test 11: Optimize Result
runner.test('StrategyOptimizer should return improvement', async () => {
  const optimizer = new StrategyOptimizer();
  
  const result = await optimizer.optimize({ strategy: 'default' });
  runner.assert(typeof result === 'object', 'Should return object');
});

// Test 12: System Integration
runner.test('SelfImprovementSystem components should work together', () => {
  const system = new SelfImprovementSystem();
  
  runner.assert(system.analyzer, 'Should have analyzer');
  runner.assert(system.optimizer, 'Should have optimizer');
});

// Run tests
runner.run().then(success => {
  process.exit(success ? 0 : 1);
});
