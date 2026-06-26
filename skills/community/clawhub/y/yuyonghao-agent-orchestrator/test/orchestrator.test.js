/**
 * Agent Orchestrator Test Suite
 */

const { AgentOrchestrator, Scheduler, AgentRegistry, ResourceManager, HealthChecker, LoadBalancer } = require('../src');

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
    console.log('\n🧪 Running Agent Orchestrator Tests\n');
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

// Test 1: AgentOrchestrator Creation
runner.test('AgentOrchestrator should be created', () => {
  const orchestrator = new AgentOrchestrator();
  runner.assert(orchestrator, 'Orchestrator should be created');
  runner.assertEquals(orchestrator.isRunning, false, 'Should not be running initially');
});

// Test 2: AgentRegistry Creation
runner.test('AgentRegistry should be created', () => {
  const registry = new AgentRegistry();
  runner.assert(registry, 'Registry should be created');
});

// Test 3: Scheduler Creation
runner.test('Scheduler should be created', () => {
  const scheduler = new Scheduler();
  runner.assert(scheduler, 'Scheduler should be created');
});

// Test 4: ResourceManager Creation
runner.test('ResourceManager should be created', () => {
  const rm = new ResourceManager();
  runner.assert(rm, 'ResourceManager should be created');
});

// Test 5: HealthChecker Creation
runner.test('HealthChecker should be created', () => {
  const hc = new HealthChecker();
  runner.assert(hc, 'HealthChecker should be created');
});

// Test 6: LoadBalancer Creation
runner.test('LoadBalancer should be created', () => {
  const lb = new LoadBalancer();
  runner.assert(lb, 'LoadBalancer should be created');
});

// Test 7: Agent Registration
runner.test('AgentRegistry should register agents', () => {
  const registry = new AgentRegistry();
  const agent = {
    id: 'agent-1',
    capabilities: ['text-generation'],
    resources: { maxConcurrent: 5 }
  };
  
  registry.register(agent);
  const status = registry.get('agent-1');
  
  runner.assert(status, 'Agent should be registered');
  runner.assertEquals(status.id, 'agent-1', 'Agent ID should match');
});

// Test 8: Agent Unregistration
runner.test('AgentRegistry should unregister agents', () => {
  const registry = new AgentRegistry();
  registry.register({ id: 'agent-2', capabilities: [] });
  registry.unregister('agent-2');
  
  const status = registry.get('agent-2');
  runner.assert(!status, 'Agent should be unregistered');
});

// Test 9: Priority Levels
runner.test('Scheduler should have priority levels', () => {
  const scheduler = new Scheduler();
  
  runner.assert(scheduler.options.defaultPriority, 'Should have default priority');
});

// Test 10: Resource Tracking
runner.test('ResourceManager should track resources', () => {
  const rm = new ResourceManager({ maxAgents: 10 });
  
  const usage = rm.getStats();
  runner.assert(typeof usage === 'object', 'Should return usage object');
});

// Test 11: Load Balancer Strategy
runner.test('LoadBalancer should have strategy', () => {
  const lb = new LoadBalancer('round-robin');
  
  runner.assert(lb.strategy, 'Should have strategy');
  runner.assertEquals(lb.strategy, 'round-robin', 'Strategy should be round-robin');
});

// Test 12: Health Check Config
runner.test('HealthChecker should have config', () => {
  const hc = new HealthChecker({ interval: 5000 });
  
  runner.assertEquals(hc.options.interval, 5000, 'Interval should be 5000');
});

// Test 13: Agent Capabilities
runner.test('AgentRegistry should store capabilities', () => {
  const registry = new AgentRegistry();
  registry.register({
    id: 'agent-cap',
    capabilities: ['text-generation', 'code-execution']
  });
  
  const agent = registry.get('agent-cap');
  runner.assert(agent.capabilities.includes('code-execution'), 'Should store capabilities');
});

// Test 14: Scheduler Queue
runner.test('Scheduler should have task queue', () => {
  const scheduler = new Scheduler();
  
  runner.assert(Array.isArray(scheduler.taskQueue), 'Should have task queue');
});

// Test 15: Orchestrator Config
runner.test('AgentOrchestrator should accept config', () => {
  const orchestrator = new AgentOrchestrator({
    cluster: { enabled: true },
    scheduler: { strategy: 'least-connections' }
  });
  
  runner.assertEquals(orchestrator.options.cluster.enabled, true, 'Should accept cluster config');
  runner.assertEquals(orchestrator.options.scheduler.strategy, 'least-connections', 'Should accept scheduler config');
});

// Run tests
runner.run().then(success => {
  process.exit(success ? 0 : 1);
});
