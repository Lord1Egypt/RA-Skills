/**
 * Deployment Kit 测试套件
 */

import { DeployManager } from '../src/deploy-manager.js';

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
    console.log('🧪 Deployment Kit Test Suite Starting...\n');
    
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

// === DeployManager Tests ===
runner.test('DeployManager - should initialize', async () => {
  const manager = new DeployManager({
    imageName: 'test-image',
    containerName: 'test-container'
  });
  if (!manager) throw new Error('Failed to initialize');
  if (manager.config.imageName !== 'test-image') throw new Error('Config not set');
});

runner.test('DeployManager - should have default config', async () => {
  const manager = new DeployManager({});
  if (manager.config.imageName !== 'openclaw') throw new Error('Default image name not set');
  if (manager.config.port !== 18789) throw new Error('Default port not set');
});

runner.test('DeployManager - should check Docker availability', async () => {
  const manager = new DeployManager({});
  const result = await manager.checkDocker();
  // 在 Windows 上可能没有 Docker，所以不强制要求返回 true
  console.log(`  Docker available: ${result}`);
});

runner.test('DeployManager - should emit events', async () => {
  const manager = new DeployManager({});
  let eventFired = false;
  
  manager.on('test-event', () => {
    eventFired = true;
  });
  
  manager.emit('test-event');
  if (!eventFired) throw new Error('Event should be fired');
});

runner.test('DeployManager - should track status', async () => {
  const manager = new DeployManager({});
  if (manager.status !== 'idle') throw new Error('Initial status should be idle');
});

// 运行测试
runner.run().then(success => {
  process.exit(success ? 0 : 1);
});
