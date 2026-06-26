/**
 * n8n Integration Test Suite
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
    console.log('🧪 n8n Integration Test Suite Starting...\n');
    
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
runner.test('n8n-integration - should have package.json', async () => {
  const fs = await import('fs');
  const exists = fs.existsSync('./package.json');
  if (!exists) throw new Error('package.json should exist');
});

runner.test('n8n-integration - should have src files', async () => {
  const fs = await import('fs');
  const exists = fs.existsSync('./src/index.js');
  if (!exists) throw new Error('src/index.js should exist');
});

runner.test('n8n-integration - should have webhook server', async () => {
  const fs = await import('fs');
  const exists = fs.existsSync('./src/webhook-server.js');
  if (!exists) throw new Error('src/webhook-server.js should exist');
});

runner.test('n8n-integration - should have SKILL.md', async () => {
  const fs = await import('fs');
  const exists = fs.existsSync('./SKILL.md');
  if (!exists) throw new Error('SKILL.md should exist');
});

runner.test('n8n-integration - should have examples', async () => {
  const fs = await import('fs');
  const exists = fs.existsSync('./examples/workflow-example.json');
  if (!exists) throw new Error('examples should exist');
});

// 运行测试
runner.run().then(success => {
  process.exit(success ? 0 : 1);
});
