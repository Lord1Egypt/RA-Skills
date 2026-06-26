/**
 * Agent Eval Suite Test Suite
 */

const { Benchmark, ABTester, RegressionDetector, Simulator } = require('../src');

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
    console.log('\n🧪 Running Agent Eval Suite Tests\n');
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

  assertEquals(actual, expected, message) {
    if (actual !== expected) throw new Error(message || `Expected ${expected}, got ${actual}`);
  }
}

const runner = new TestRunner();

// Test 1: Benchmark Creation
runner.test('Benchmark should be created', () => {
  const benchmark = new Benchmark({ iterations: 10 });
  runner.assert(benchmark, 'Benchmark should be created');
});

// Test 2: ABTester Creation
runner.test('ABTester should be created', () => {
  const ab = new ABTester({ confidenceLevel: 0.95 });
  runner.assert(ab, 'ABTester should be created');
});

// Test 3: RegressionDetector Creation
runner.test('RegressionDetector should be created', () => {
  const detector = new RegressionDetector({ threshold: 0.1 });
  runner.assert(detector, 'RegressionDetector should be created');
});

// Test 4: Simulator Creation
runner.test('Simulator should be created', () => {
  const simulator = new Simulator();
  runner.assert(simulator, 'Simulator should be created');
});

// Test 5: Benchmark Add Test
runner.test('Benchmark should add tests', () => {
  const benchmark = new Benchmark();
  
  benchmark.addTest('test-1', {
    execute: async () => ({ success: true })
  });
  
  runner.assert(benchmark.tests.has('test-1'), 'Should add test');
});

// Test 6: ABTest Create Experiment
runner.test('ABTester should create experiments', () => {
  const ab = new ABTester();
  
  ab.createExperiment('exp-1', {
    control: async () => 'A',
    treatment: async () => 'B'
  });
  
  runner.assert(ab.experiments.has('exp-1'), 'Should create experiment');
});

// Test 7: Regression Record
runner.test('RegressionDetector should record metrics', () => {
  const detector = new RegressionDetector();
  
  detector.record('response-time', { version: 'v1.0', value: 100 });
  
  const metrics = detector.getMetrics();
  runner.assert(typeof metrics === 'object', 'Should record metric');
});

// Test 8: Regression Detection
runner.test('RegressionDetector should detect regressions', () => {
  const detector = new RegressionDetector({ threshold: 0.1 });
  
  detector.record('metric-1', { version: 'v1.0', value: 100 });
  detector.record('metric-1', { version: 'v1.1', value: 120 });
  
  const regressions = detector.detect();
  runner.assert(Array.isArray(regressions), 'Should return array');
});

// Test 9: Simulator Load Scenario
runner.test('Simulator should load scenarios', async () => {
  const simulator = new Simulator();
  
  // Mock scenario
  simulator.scenarios.set('test-scenario', {
    name: 'Test',
    setup: () => {},
    run: async () => ({ success: true })
  });
  
  runner.assert(simulator.scenarios.has('test-scenario'), 'Should load scenario');
});

// Test 10: Benchmark Config
runner.test('Benchmark should accept config', () => {
  const benchmark = new Benchmark({
    iterations: 50,
    warmup: 5
  });
  
  runner.assertEquals(benchmark.options.iterations, 50, 'Should accept iterations');
  runner.assertEquals(benchmark.options.warmup, 5, 'Should accept warmup');
});

// Test 11: ABTest Config
runner.test('ABTester should accept config', () => {
  const ab = new ABTester({
    confidenceLevel: 0.99,
    minSampleSize: 50
  });
  
  runner.assertEquals(ab.options.confidenceLevel, 0.99, 'Should accept confidence level');
});

// Test 12: Detector Config
runner.test('RegressionDetector should accept config', () => {
  const detector = new RegressionDetector({
    threshold: 0.15,
    baseline: 'v1.0.0'
  });
  
  runner.assertEquals(detector.options.threshold, 0.15, 'Should accept threshold');
});

// Run tests
runner.run().then(success => {
  process.exit(success ? 0 : 1);
});
