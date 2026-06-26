/**
 * Agent Metacognition Test Suite
 */

const { MetacognitionSystem, SelfMonitor, ReflectionEngine } = require('../src');

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
    console.log('\n🧪 Running Agent Metacognition Tests\n');
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

// Test 1: MetacognitionSystem Creation
runner.test('MetacognitionSystem should be created', () => {
  const meta = new MetacognitionSystem();
  runner.assert(meta, 'System should be created');
});

// Test 2: SelfMonitor Creation
runner.test('SelfMonitor should be created', () => {
  const monitor = new SelfMonitor();
  runner.assert(monitor, 'Monitor should be created');
});

// Test 3: ReflectionEngine Creation
runner.test('ReflectionEngine should be created', () => {
  const reflection = new ReflectionEngine();
  runner.assert(reflection, 'Reflection should be created');
});

// Test 4: Monitor Execution
runner.test('SelfMonitor should monitor execution', async () => {
  const monitor = new SelfMonitor();
  
  const result = await monitor.monitor(async () => {
    return 'success';
  }, { taskId: 'test-1' });
  
  runner.assert(result === 'success', 'Should return result');
});

// Test 5: Reflection Analysis
runner.test('ReflectionEngine should analyze', async () => {
  const reflection = new ReflectionEngine();
  
  const analysis = await reflection.analyze('test-execution');
  runner.assert(typeof analysis === 'object', 'Should return analysis');
});

// Test 6: Metacognitive State
runner.test('MetacognitionSystem should provide state', () => {
  const meta = new MetacognitionSystem();
  
  const state = meta.getMetacognitiveState();
  runner.assert(typeof state === 'object', 'Should return state');
  runner.assert(typeof state.awareness === 'number', 'Should have awareness');
});

// Test 7: System Options
runner.test('MetacognitionSystem should accept options', () => {
  const meta = new MetacognitionSystem({
    monitor: { enabled: true },
    reflection: { depth: 3 }
  });
  
  runner.assert(meta.options, 'Should have options');
});

// Test 8: Monitor Options
runner.test('SelfMonitor should accept options', () => {
  const monitor = new SelfMonitor({ trackDecisions: true });
  runner.assert(monitor.options, 'Should have options');
});

// Test 9: Reflection Options
runner.test('ReflectionEngine should accept options', () => {
  const reflection = new ReflectionEngine({ depth: 5 });
  runner.assert(reflection.options, 'Should have options');
});

// Test 10: Monitor Tracking
runner.test('SelfMonitor should track executions', async () => {
  const monitor = new SelfMonitor();
  
  await monitor.monitor(async () => 'test', { sessionId: 'track-1' });
  
  const report = monitor.getReport('track-1');
  runner.assert(report, 'Should track executions');
});

// Test 11: Reflection Insights
runner.test('ReflectionEngine should provide insights', async () => {
  const reflection = new ReflectionEngine();
  
  const analysis = await reflection.analyze('test');
  runner.assert(analysis, 'Should provide analysis');
});

// Test 12: System Integration
runner.test('MetacognitionSystem components should work together', () => {
  const meta = new MetacognitionSystem();
  
  runner.assert(meta.monitor, 'Should have monitor');
  runner.assert(meta.reflection, 'Should have reflection');
});

// Run tests
runner.run().then(success => {
  process.exit(success ? 0 : 1);
});
