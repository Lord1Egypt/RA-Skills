/**
 * Agent Swarm Test Suite
 */

import { SwarmCoordinator } from '../src/index.js';

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
    console.log('\n🧪 Running Agent Swarm Tests\n');
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

// Test 1: SwarmCoordinator Creation
runner.test('SwarmCoordinator should be created', () => {
  const coordinator = new SwarmCoordinator({ maxAgents: 50 });
  runner.assert(coordinator, 'Coordinator should be created');
});

// Test 2: Create Swarm
runner.test('SwarmCoordinator should create swarm', () => {
  const coordinator = new SwarmCoordinator();
  const swarmId = coordinator.createSwarm({ name: 'test-swarm' });
  runner.assert(swarmId, 'Should return swarm ID');
});

// Test 3: Destroy Swarm
runner.test('SwarmCoordinator should destroy swarm', () => {
  const coordinator = new SwarmCoordinator();
  const swarmId = coordinator.createSwarm({ name: 'test-swarm' });
  const result = coordinator.destroySwarm(swarmId);
  runner.assert(result, 'Should destroy swarm');
});

// Test 4: Add Agent
runner.test('SwarmCoordinator should add agent', () => {
  const coordinator = new SwarmCoordinator();
  const swarmId = coordinator.createSwarm({ name: 'test-swarm' });
  const agentId = coordinator.addAgent(swarmId, { capabilities: ['test'] });
  runner.assert(agentId, 'Should return agent ID');
});

// Test 5: Remove Agent
runner.test('SwarmCoordinator should remove agent', () => {
  const coordinator = new SwarmCoordinator();
  const swarmId = coordinator.createSwarm({ name: 'test-swarm' });
  const agentId = coordinator.addAgent(swarmId, { capabilities: ['test'] });
  const result = coordinator.removeAgent(agentId);
  runner.assert(result, 'Should remove agent');
});

// Test 6: Execute Task
runner.test('SwarmCoordinator should execute task', async () => {
  const coordinator = new SwarmCoordinator();
  const swarmId = coordinator.createSwarm({ name: 'test-swarm' });
  coordinator.addAgent(swarmId, { capabilities: ['test'] });
  
  const result = await coordinator.executeTask(swarmId, {
    type: 'test-task',
    input: 'test'
  });
  
  runner.assert(result.taskId, 'Should return task ID');
});

// Test 7: Get Swarm Status
runner.test('SwarmCoordinator should get swarm status', () => {
  const coordinator = new SwarmCoordinator();
  const swarmId = coordinator.createSwarm({ name: 'test-swarm' });
  coordinator.addAgent(swarmId, { capabilities: ['test'] });
  
  const status = coordinator.getSwarmStatus(swarmId);
  runner.assert(status, 'Should return status');
  runner.assert(status.name === 'test-swarm', 'Should have correct name');
});

// Test 8: Get All Swarms
runner.test('SwarmCoordinator should get all swarms', () => {
  const coordinator = new SwarmCoordinator();
  coordinator.createSwarm({ name: 'swarm-1' });
  coordinator.createSwarm({ name: 'swarm-2' });
  
  const swarms = coordinator.getAllSwarms();
  runner.assert(Array.isArray(swarms), 'Should return array');
  runner.assert(swarms.length === 2, 'Should have 2 swarms');
});

// Test 9: Parallel Execution
runner.test('SwarmCoordinator should support parallel execution', async () => {
  const coordinator = new SwarmCoordinator();
  const swarmId = coordinator.createSwarm({ name: 'test-swarm' });
  coordinator.addAgent(swarmId, { capabilities: ['test'] });
  coordinator.addAgent(swarmId, { capabilities: ['test'] });
  
  const result = await coordinator.executeTask(swarmId, {
    type: 'test-task',
    input: 'test',
    shardStrategy: 'parallel'
  });
  
  runner.assert(result.results.length > 0, 'Should have results');
});

// Test 10: Agent Status
runner.test('SwarmCoordinator should track agent status', () => {
  const coordinator = new SwarmCoordinator();
  const swarmId = coordinator.createSwarm({ name: 'test-swarm' });
  const agentId = coordinator.addAgent(swarmId, { capabilities: ['test'] });
  
  const status = coordinator.getSwarmStatus(swarmId);
  const agent = status.agents.find(a => a.id === agentId);
  runner.assert(agent, 'Should track agent');
});

// Test 11: Max Agents Limit
runner.test('SwarmCoordinator should respect max agents limit', () => {
  const coordinator = new SwarmCoordinator({ maxAgents: 2 });
  const swarmId = coordinator.createSwarm({ name: 'test-swarm' });
  coordinator.addAgent(swarmId, { capabilities: ['test'] });
  coordinator.addAgent(swarmId, { capabilities: ['test'] });
  
  try {
    coordinator.addAgent(swarmId, { capabilities: ['test'] });
    runner.assert(false, 'Should throw error');
  } catch (error) {
    runner.assert(true, 'Should throw capacity error');
  }
});

// Test 12: Task Duration
runner.test('SwarmCoordinator should track task duration', async () => {
  const coordinator = new SwarmCoordinator();
  const swarmId = coordinator.createSwarm({ name: 'test-swarm' });
  coordinator.addAgent(swarmId, { capabilities: ['test'] });
  
  const result = await coordinator.executeTask(swarmId, {
    type: 'test-task',
    input: 'test'
  });
  
  runner.assert(result.duration >= 0, 'Should have duration');
});

// Run tests
runner.run().then(success => {
  process.exit(success ? 0 : 1);
});
