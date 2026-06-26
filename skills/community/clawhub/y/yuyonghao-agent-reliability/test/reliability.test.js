/**
 * Agent Reliability Test Suite
 */

const { ReliabilityMonitor, FallbackManager, ConfidenceCalculator, VotingConsensus } = require('../src');

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
    console.log('\n🧪 Running Agent Reliability Tests\n');
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

// Test 1: ReliabilityMonitor Creation
runner.test('ReliabilityMonitor should be created', () => {
  const monitor = new ReliabilityMonitor({
    errorThreshold: 0.15,
    confidenceThreshold: 0.85
  });
  
  runner.assert(monitor, 'Monitor should be created');
});

// Test 2: Record Execution
runner.test('ReliabilityMonitor should record executions', () => {
  const monitor = new ReliabilityMonitor();
  
  monitor.record({ stepId: 'step-1', success: true, confidence: 0.9 });
  monitor.record({ stepId: 'step-1', success: false, confidence: 0.5 });
  
  const history = monitor.getHistory();
  runner.assert(history.length >= 2, 'Should record executions');
});

// Test 3: FallbackManager Creation
runner.test('FallbackManager should be created', () => {
  const fallback = new FallbackManager({ maxRetries: 3 });
  runner.assert(fallback, 'FallbackManager should be created');
});

// Test 4: ConfidenceCalculator Creation
runner.test('ConfidenceCalculator should be created', () => {
  const calc = new ConfidenceCalculator();
  runner.assert(calc, 'ConfidenceCalculator should be created');
});

// Test 5: VotingConsensus Creation
runner.test('VotingConsensus should be created', () => {
  const consensus = new VotingConsensus({ strategy: 'simple-majority' });
  runner.assert(consensus, 'VotingConsensus should be created');
});

// Test 6: Voting Session Creation
runner.test('VotingConsensus should create sessions', () => {
  const consensus = new VotingConsensus();
  
  const sessionId = consensus.createSession();
  runner.assert(sessionId, 'Should create session');
  
  const session = consensus.getSession(sessionId);
  runner.assert(session, 'Should get session');
});

// Test 7: Simple Voting
runner.test('VotingConsensus should accept votes', () => {
  const consensus = new VotingConsensus();
  
  const sessionId = consensus.createSession();
  const result = consensus.vote('agent-1', { decision: 'approve', confidence: 0.9 }, sessionId);
  
  runner.assert(result, 'Should accept votes');
});

// Test 8: Reliability Score
runner.test('ReliabilityMonitor should calculate reliability score', () => {
  const monitor = new ReliabilityMonitor();
  
  monitor.record({ stepId: 'step-1', success: true, confidence: 0.9, duration: 1000 });
  monitor.record({ stepId: 'step-1', success: true, confidence: 0.8, duration: 1000 });
  
  const score = monitor.getReliabilityScore();
  runner.assert(typeof score === 'object', 'Should return score');
  runner.assert(typeof score.overall === 'object', 'Should have overall');
});

// Test 9: Step Stats
runner.test('ReliabilityMonitor should track step stats', () => {
  const monitor = new ReliabilityMonitor();
  
  monitor.record({ stepId: 'step-1', success: true, confidence: 0.9 });
  
  const stats = monitor.getStepStats('step-1');
  runner.assert(stats, 'Should have step stats');
});

// Test 10: Error Categories
runner.test('ReliabilityMonitor should track error categories', () => {
  const monitor = new ReliabilityMonitor();
  
  const categories = monitor.getErrorCategories();
  runner.assert(typeof categories === 'object', 'Should return categories');
});

// Test 11: Voting Stats
runner.test('VotingConsensus should provide stats', () => {
  const consensus = new VotingConsensus();
  
  const stats = consensus.getStats();
  runner.assert(typeof stats === 'object', 'Should return stats');
});

// Test 12: Monitor Reset
runner.test('ReliabilityMonitor should support reset', () => {
  const monitor = new ReliabilityMonitor();
  
  monitor.record({ stepId: 'step-1', success: true, confidence: 0.9 });
  monitor.reset();
  
  const history = monitor.getHistory();
  runner.assert(history.length === 0, 'Should reset history');
});

// Run tests
runner.run().then(success => {
  process.exit(success ? 0 : 1);
});
