/**
 * Multi-Agent 简化测试
 */

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
    console.log('🧪 Multi-Agent Simple Test Suite Starting...\n');
    
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

// 基础测试
runner.test('Multi-Agent - should have src files', async () => {
  const fs = await import('fs');
  const exists = fs.existsSync('./src/agent-team.js');
  if (!exists) throw new Error('agent-team.js should exist');
});

runner.test('Multi-Agent - should have roles', async () => {
  const fs = await import('fs');
  const exists = fs.existsSync('./src/roles.js');
  if (!exists) throw new Error('roles.js should exist');
});

runner.test('Multi-Agent - should have task planner', async () => {
  const fs = await import('fs');
  const exists = fs.existsSync('./src/task-planner.js');
  if (!exists) throw new Error('task-planner.js should exist');
});

runner.test('Multi-Agent - should have orchestrator', async () => {
  const fs = await import('fs');
  const exists = fs.existsSync('./src/orchestrator.js');
  if (!exists) throw new Error('orchestrator.js should exist');
});

runner.test('Multi-Agent - should have SKILL.md', async () => {
  const fs = await import('fs');
  const exists = fs.existsSync('./SKILL.md');
  if (!exists) throw new Error('SKILL.md should exist');
});

// 运行测试
runner.run().then(success => {
  process.exit(success ? 0 : 1);
});
