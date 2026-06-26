/**
 * Multi-Agent 测试套件 (ES Module)
 */

import { AgentTeam } from '../src/agent-team.js';
import { TaskPlanner } from '../src/task-planner.js';

// 测试运行器
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
    console.log('🧪 Multi-Agent Test Suite Starting...\n');
    
    for (const { name, fn } of this.tests) {
      try {
        await fn();
        console.log(`✓ ${name}`);
        this.passed++;
      } catch (error) {
        console.log(`✗ ${name}`);
        console.log(`  Error: ${error.message}`);
        this.failed++;
      }
    }
    
    console.log(`\n📊 Results: ${this.passed} passed, ${this.failed} failed`);
    return this.failed === 0;
  }
}

const runner = new TestRunner();

// === AgentTeam Tests ===
runner.test('AgentTeam - should initialize', async () => {
  const team = new AgentTeam({ name: 'Test Team' });
  if (!team) throw new Error('Failed to initialize');
});

runner.test('AgentTeam - should add agent', async () => {
  const team = new AgentTeam({ name: 'Test Team' });
  team.addAgent({
    id: 'agent1',
    name: 'Test Agent',
    role: 'researcher'
  });
  if (team.agents.size !== 1) throw new Error('Should have 1 agent');
});

runner.test('AgentTeam - should get agent by role', async () => {
  const team = new AgentTeam({ name: 'Test Team' });
  team.addAgent({ id: 'agent1', name: 'Researcher', role: 'researcher' });
  const agents = team.getAgentsByRole('researcher');
  if (agents.length !== 1) throw new Error('Should find 1 researcher');
});

// === TaskPlanner Tests ===
runner.test('TaskPlanner - should initialize', async () => {
  const planner = new TaskPlanner({});
  if (!planner) throw new Error('Failed to initialize');
});

runner.test('TaskPlanner - should create task', async () => {
  const planner = new TaskPlanner({});
  const task = planner.createTask({
    id: 'task1',
    description: 'Test task',
    priority: 'high'
  });
  if (!task || task.id !== 'task1') throw new Error('Failed to create task');
});

runner.test('TaskPlanner - should decompose task', async () => {
  const planner = new TaskPlanner({});
  const subtasks = planner.decomposeTask({
    description: 'Build a website',
    complexity: 'high'
  });
  if (!subtasks || subtasks.length === 0) throw new Error('Should decompose task');
});

// 运行测试
runner.run().then(success => {
  process.exit(success ? 0 : 1);
});
