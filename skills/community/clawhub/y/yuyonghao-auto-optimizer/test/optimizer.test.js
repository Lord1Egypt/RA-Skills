/**
 * Auto Optimizer 测试套件
 */

const { PerformanceMonitor } = require('../src/monitor');
const { BottleneckAnalyzer } = require('../src/analyzer');
const { OptimizationEngine } = require('../src/optimizer');
const { OptimizationApplier } = require('../src/applier');
const { AutoOptimizer } = require('../src/index');

// 简单的测试框架
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
    console.log('\n🧪 Running Auto Optimizer Tests\n');
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
    if (!condition) {
      throw new Error(message || 'Assertion failed');
    }
  }

  assertEqual(actual, expected, message) {
    if (actual !== expected) {
      throw new Error(message || `Expected ${expected}, got ${actual}`);
    }
  }

  assertTrue(value, message) {
    this.assert(value === true, message || `Expected true, got ${value}`);
  }

  assertFalse(value, message) {
    this.assert(value === false, message || `Expected false, got ${value}`);
  }

  assertThrows(fn, message) {
    let threw = false;
    try {
      fn();
    } catch (e) {
      threw = true;
    }
    this.assert(threw, message || 'Expected function to throw');
  }
}

const runner = new TestRunner();

// ==================== PerformanceMonitor Tests ====================

runner.test('PerformanceMonitor: should start and end operation', () => {
  const monitor = new PerformanceMonitor();
  
  monitor.startOperation('test-op-1', 'test-skill');
  const result = monitor.endOperation('test-op-1', { data: 'test' });
  
  runner.assert(result.metrics !== undefined, 'Should return metrics');
  runner.assert(result.metrics.skillName === 'test-skill', 'Should have correct skill name');
  runner.assert(result.metrics.status === 'success', 'Should have success status');
});

runner.test('PerformanceMonitor: should track operation duration', async () => {
  const monitor = new PerformanceMonitor();
  
  monitor.startOperation('test-op-2', 'test-skill');
  await new Promise(resolve => setTimeout(resolve, 50));
  const result = monitor.endOperation('test-op-2', null);
  
  runner.assert(result.metrics.duration >= 50, 'Duration should be at least 50ms');
});

runner.test('PerformanceMonitor: should handle errors', () => {
  const monitor = new PerformanceMonitor();
  
  monitor.startOperation('test-op-3', 'test-skill');
  const result = monitor.endOperation('test-op-3', null, new Error('Test error'));
  
  runner.assert(result.metrics.status === 'error', 'Should have error status');
  runner.assert(result.metrics.error === 'Test error', 'Should have error message');
});

runner.test('PerformanceMonitor: should throw on invalid operationId', () => {
  const monitor = new PerformanceMonitor();
  
  runner.assertThrows(() => {
    monitor.startOperation('', 'test-skill');
  }, 'Should throw on empty operationId');
  
  runner.assertThrows(() => {
    monitor.startOperation('test', '');
  }, 'Should throw on empty skillName');
});

runner.test('PerformanceMonitor: should calculate skill stats', () => {
  const monitor = new PerformanceMonitor();
  
  // Simulate multiple operations
  for (let i = 0; i < 5; i++) {
    monitor.startOperation(`op-${i}`, 'test-skill');
    monitor.endOperation(`op-${i}`, null);
  }
  
  const stats = monitor.getSkillStats('test-skill');
  
  runner.assert(stats !== null, 'Should return stats');
  runner.assertEqual(stats.totalExecutions, 5, 'Should have 5 executions');
  runner.assertEqual(stats.successCount, 5, 'Should have 5 successes');
});

// ==================== BottleneckAnalyzer Tests ====================

runner.test('BottleneckAnalyzer: should detect high execution time', () => {
  const analyzer = new BottleneckAnalyzer();
  
  const metrics = [];
  for (let i = 0; i < 10; i++) {
    metrics.push({
      duration: 6000, // 6 seconds, above threshold
      memoryDelta: { rss: 1000000 },
      status: 'success',
      timestamp: new Date().toISOString()
    });
  }
  
  const analysis = analyzer.analyzeSkill('test-skill', metrics);
  
  runner.assert(analysis.status === 'bottlenecks_detected', 'Should detect bottlenecks');
  runner.assert(analysis.bottlenecks.length > 0, 'Should have bottlenecks');
  
  const highTimeBottleneck = analysis.bottlenecks.find(b => b.ruleId === 'high_execution_time');
  runner.assert(highTimeBottleneck !== undefined, 'Should detect high execution time');
});

runner.test('BottleneckAnalyzer: should detect high error rate', () => {
  const analyzer = new BottleneckAnalyzer();
  
  const metrics = [];
  for (let i = 0; i < 10; i++) {
    metrics.push({
      duration: 100,
      memoryDelta: { rss: 1000000 },
      status: i < 5 ? 'success' : 'error', // 50% error rate
      timestamp: new Date().toISOString()
    });
  }
  
  const analysis = analyzer.analyzeSkill('test-skill', metrics);
  
  const errorBottleneck = analysis.bottlenecks.find(b => b.ruleId === 'high_error_rate');
  runner.assert(errorBottleneck !== undefined, 'Should detect high error rate');
});

runner.test('BottleneckAnalyzer: should return insufficient_data for small samples', () => {
  const analyzer = new BottleneckAnalyzer({ minSampleSize: 10 });
  
  const metrics = [{ duration: 100, memoryDelta: { rss: 1000 }, status: 'success', timestamp: new Date().toISOString() }];
  
  const analysis = analyzer.analyzeSkill('test-skill', metrics);
  
  runner.assert(analysis.status === 'insufficient_data', 'Should return insufficient_data');
});

runner.test('BottleneckAnalyzer: should return healthy when no issues', () => {
  const analyzer = new BottleneckAnalyzer();
  
  const metrics = [];
  for (let i = 0; i < 10; i++) {
    metrics.push({
      duration: 100, // Fast execution
      memoryDelta: { rss: 1000000 },
      status: 'success',
      timestamp: new Date().toISOString()
    });
  }
  
  const analysis = analyzer.analyzeSkill('test-skill', metrics);
  
  runner.assert(analysis.status === 'healthy', 'Should return healthy');
  runner.assertEqual(analysis.bottlenecks.length, 0, 'Should have no bottlenecks');
});

runner.test('BottleneckAnalyzer: should analyze multiple skills', () => {
  const analyzer = new BottleneckAnalyzer();
  
  const metrics = [];
  for (let i = 0; i < 10; i++) {
    metrics.push({
      duration: 100,
      memoryDelta: { rss: 1000000 },
      status: 'success',
      timestamp: new Date().toISOString()
    });
  }
  
  const result = analyzer.analyzeMultipleSkills({
    'skill-1': metrics,
    'skill-2': metrics
  });
  
  runner.assertEqual(result.skillsAnalyzed, 2, 'Should analyze 2 skills');
  runner.assert(result.results['skill-1'] !== undefined, 'Should have skill-1 results');
  runner.assert(result.results['skill-2'] !== undefined, 'Should have skill-2 results');
});

// ==================== OptimizationEngine Tests ====================

runner.test('OptimizationEngine: should generate recommendations', () => {
  const engine = new OptimizationEngine();
  
  const bottleneck = {
    ruleId: 'high_execution_time',
    name: 'High Execution Time',
    type: 'performance',
    severity: 'high',
    confidence: 0.9
  };
  
  const recommendations = engine.generateRecommendations(bottleneck, { skillName: 'test-skill' });
  
  runner.assert(recommendations.length > 0, 'Should generate recommendations');
  runner.assert(recommendations[0].title !== undefined, 'Should have title');
  runner.assert(recommendations[0].actions !== undefined, 'Should have actions');
});

runner.test('OptimizationEngine: should generate optimization plan', () => {
  const engine = new OptimizationEngine();
  
  const analysis = {
    skillName: 'test-skill',
    status: 'bottlenecks_detected',
    bottlenecks: [{
      ruleId: 'high_execution_time',
      name: 'High Execution Time',
      type: 'performance',
      severity: 'high',
      confidence: 0.9
    }]
  };
  
  const plan = engine.generateOptimizationPlan(analysis);
  
  runner.assert(plan.skillName === 'test-skill', 'Should have skill name');
  runner.assert(plan.recommendations.length > 0, 'Should have recommendations');
  runner.assert(plan.estimatedImpact !== undefined, 'Should have impact estimate');
  runner.assert(plan.implementationOrder.length > 0, 'Should have implementation order');
});

runner.test('OptimizationEngine: should estimate impact correctly', () => {
  const engine = new OptimizationEngine();
  
  const recommendations = [
    { impact: 'critical', priority: 'critical' },
    { impact: 'high', priority: 'high' },
    { impact: 'medium', priority: 'medium' }
  ];
  
  const impact = engine.estimateImpact(recommendations);
  
  runner.assert(impact.score > 0, 'Should have positive score');
  runner.assert(impact.percentage !== undefined, 'Should have percentage');
  runner.assert(['high', 'medium', 'low'].includes(impact.level), 'Should have valid level');
});

runner.test('OptimizationEngine: should find common strategies', () => {
  const engine = new OptimizationEngine();
  
  const recommendations = [
    { strategyId: 'cache', skillName: 'skill-1' },
    { strategyId: 'cache', skillName: 'skill-2' },
    { strategyId: 'cache', skillName: 'skill-3' },
    { strategyId: 'async', skillName: 'skill-1' }
  ];
  
  const common = engine.findCommonStrategies(recommendations);
  
  runner.assert(common.length > 0, 'Should find common strategies');
  const cacheStrategy = common.find(s => s.strategyId === 'cache');
  runner.assert(cacheStrategy !== undefined, 'Should find cache strategy');
  runner.assertEqual(cacheStrategy.affectedSkills, 3, 'Should affect 3 skills');
});

// ==================== OptimizationApplier Tests ====================

runner.test('OptimizationApplier: should apply recommendations in dry-run mode', async () => {
  const applier = new OptimizationApplier({ dryRun: true });
  
  const recommendation = {
    strategyId: 'cache_frequently_used_data',
    title: 'Test Recommendation'
  };
  
  const result = await applier.applyRecommendation(recommendation, {});
  
  runner.assert(result.status === 'success' || result.status === 'partial', 'Should complete');
  runner.assert(result.changes !== undefined, 'Should have changes');
});

runner.test('OptimizationApplier: should track applied optimizations', async () => {
  const applier = new OptimizationApplier({ dryRun: true });
  
  const recommendation = {
    strategyId: 'performance_monitoring',
    title: 'Test'
  };
  
  await applier.applyRecommendation(recommendation, {});
  const applied = applier.getAppliedOptimizations();
  
  runner.assert(applied.length > 0, 'Should track optimizations');
});

runner.test('OptimizationApplier: should handle unknown strategies', async () => {
  const applier = new OptimizationApplier({ dryRun: true });
  
  const recommendation = {
    strategyId: 'unknown_strategy',
    title: 'Unknown'
  };
  
  const result = await applier.applyRecommendation(recommendation, {});
  
  runner.assert(result.status === 'skipped', 'Should skip unknown strategy');
});

runner.test('OptimizationApplier: should set dry run mode', () => {
  const applier = new OptimizationApplier({ dryRun: false });
  
  applier.setDryRun(true);
  runner.assertTrue(applier.dryRun, 'Should set dry run to true');
  
  applier.setDryRun(false);
  runner.assertFalse(applier.dryRun, 'Should set dry run to false');
});

// ==================== AutoOptimizer Integration Tests ====================

runner.test('AutoOptimizer: should monitor operation', async () => {
  const optimizer = new AutoOptimizer();
  
  const { result, metrics } = await optimizer.monitorOperation(
    'test-op',
    'test-skill',
    async () => 'test-result'
  );
  
  runner.assertEqual(result, 'test-result', 'Should return correct result');
  runner.assert(metrics.metrics !== undefined, 'Should return metrics');
});

runner.test('AutoOptimizer: should handle operation errors', async () => {
  const optimizer = new AutoOptimizer();
  
  try {
    await optimizer.monitorOperation(
      'test-op-error',
      'test-skill',
      async () => { throw new Error('Test error'); }
    );
    runner.assert(false, 'Should have thrown');
  } catch (error) {
    runner.assert(error.error !== undefined, 'Should have error');
    runner.assert(error.metrics !== undefined, 'Should have metrics');
  }
});

runner.test('AutoOptimizer: should analyze skill', async () => {
  const optimizer = new AutoOptimizer();
  
  // Add some metrics
  for (let i = 0; i < 5; i++) {
    await optimizer.monitorOperation(`op-${i}`, 'test-skill', async () => 'result');
  }
  
  const analysis = optimizer.analyzeSkill('test-skill');
  
  runner.assert(analysis.skillName === 'test-skill', 'Should have skill name');
  runner.assert(analysis.status !== undefined, 'Should have status');
});

runner.test('AutoOptimizer: should get stats', async () => {
  const optimizer = new AutoOptimizer();
  
  await optimizer.monitorOperation('op-stats', 'test-skill', async () => 'result');
  
  const stats = optimizer.getStats();
  
  runner.assert(stats['test-skill'] !== undefined, 'Should have skill stats');
});

// ==================== Error Handling Tests ====================

runner.test('Error Handling: should validate inputs', () => {
  const monitor = new PerformanceMonitor();
  
  runner.assertThrows(() => {
    monitor.startOperation(null, 'skill');
  }, 'Should throw on null operationId');
  
  runner.assertThrows(() => {
    monitor.startOperation('op', null);
  }, 'Should throw on null skillName');
});

runner.test('Error Handling: should handle analyzer invalid inputs', () => {
  const analyzer = new BottleneckAnalyzer();
  
  runner.assertThrows(() => {
    analyzer.analyzeSkill('', []);
  }, 'Should throw on empty skill name');
  
  runner.assertThrows(() => {
    analyzer.analyzeSkill('skill', 'not-an-array');
  }, 'Should throw on non-array metrics');
});

runner.test('Error Handling: should handle optimizer invalid inputs', () => {
  const engine = new OptimizationEngine();
  
  runner.assertThrows(() => {
    engine.generateOptimizationPlan(null);
  }, 'Should throw on null analysis');
  
  runner.assertThrows(() => {
    engine.generateRecommendations(null);
  }, 'Should throw on null bottleneck');
});

// ==================== Run Tests ====================

(async () => {
  const success = await runner.run();
  process.exit(success ? 0 : 1);
})();
