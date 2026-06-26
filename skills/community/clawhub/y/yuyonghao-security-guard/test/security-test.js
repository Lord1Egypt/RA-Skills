/**
 * Security Guard 测试套件
 */

import { SecurityGuard } from '../src/security-guard.js';
import { PermissionManager } from '../src/permission-manager.js';
import { ContentSafety } from '../src/content-safety.js';
import { AuditLogger } from '../src/audit-logger.js';

// 测试配置
const testConfig = {
  enabled: true,
  strictMode: false,
  permissions: {
    defaultRole: 'user',
    roles: {
      admin: { permissions: ['*'] },
      user: { permissions: ['file:read', 'file:write:home'] },
      guest: { permissions: ['file:read:home'] }
    }
  },
  contentSafety: {
    enabled: true,
    maxInputLength: 10000,
    blockedPatterns: ['password', 'secret', 'token']
  },
  audit: {
    logDir: './test-logs',
    bufferSize: 10
  }
};

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
    console.log('🧪 Security Guard Test Suite Starting...\n');
    
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

// === PermissionManager Tests ===
runner.test('PermissionManager - should initialize', async () => {
  const pm = new PermissionManager(testConfig.permissions);
  if (!pm) throw new Error('Failed to initialize');
});

runner.test('PermissionManager - admin should have all permissions', async () => {
  const pm = new PermissionManager(testConfig.permissions);
  pm.assignRole('admin', 'admin');
  const result = pm.checkPermission('admin', 'file', 'delete');
  if (!result.allowed) throw new Error('Admin should have all permissions');
});

runner.test('PermissionManager - user should have read/write', async () => {
  const pm = new PermissionManager(testConfig.permissions);
  pm.assignRole('user', 'user');
  const readResult = pm.checkPermission('user', 'file', 'read');
  const writeResult = pm.checkPermission('user', 'file', 'write:home');
  if (!readResult.allowed || !writeResult.allowed) {
    throw new Error('User should have read/write permissions');
  }
});

runner.test('PermissionManager - user should not have delete', async () => {
  const pm = new PermissionManager(testConfig.permissions);
  pm.assignRole('user', 'user');
  const result = pm.checkPermission('user', 'file', 'delete');
  if (result.allowed) throw new Error('User should not have delete permission');
});

runner.test('PermissionManager - guest should only have read', async () => {
  const pm = new PermissionManager(testConfig.permissions);
  pm.defineRole('guest', { permissions: ['file:read:home'] });
  pm.assignRole('guest', 'guest');
  const readResult = pm.checkPermission('guest', 'file', 'read:home');
  const writeResult = pm.checkPermission('guest', 'file', 'write:home');
  if (!readResult.allowed || writeResult.allowed) {
    throw new Error('Guest should only have read permission');
  }
});

// === ContentSafety Tests ===
runner.test('ContentSafety - should initialize', async () => {
  const cs = new ContentSafety(testConfig.contentSafety);
  if (!cs) throw new Error('Failed to initialize');
});

runner.test('ContentSafety - should allow safe content', async () => {
  const cs = new ContentSafety(testConfig.contentSafety);
  const result = cs.checkInput('Hello world');
  if (!result.safe) throw new Error('Safe content should pass');
});

runner.test('ContentSafety - should detect blocked patterns', async () => {
  const cs = new ContentSafety(testConfig.contentSafety);
  const result = cs.checkInput('My password is 123456');
  const hasPasswordWarning = result.warnings.some(w => 
    w.type === 'sensitive_word' && w.word === 'password'
  );
  if (!hasPasswordWarning) throw new Error('Should detect password in content');
});

runner.test('ContentSafety - should check input length', async () => {
  const cs = new ContentSafety(testConfig.contentSafety);
  const longContent = 'a'.repeat(10001);
  const result = cs.checkInput(longContent);
  if (result.safe) throw new Error('Should block content exceeding max length');
});

// === AuditLogger Tests ===
runner.test('AuditLogger - should initialize', async () => {
  const al = new AuditLogger(testConfig.audit);
  if (!al) throw new Error('Failed to initialize');
  await al.close();
});

runner.test('AuditLogger - should log operation', async () => {
  const al = new AuditLogger(testConfig.audit);
  await al.log({
    userId: 'user123',
    action: 'read',
    resource: 'file.txt',
    status: 'success'
  });
  await al.close();
});

// === SecurityGuard Integration Tests ===
runner.test('SecurityGuard - should initialize', async () => {
  const guard = new SecurityGuard(testConfig);
  if (!guard) throw new Error('Failed to initialize');
});

runner.test('SecurityGuard - should allow permitted action', async () => {
  const guard = new SecurityGuard(testConfig);
  guard.permissionManager.assignRole('user', 'user');
  const result = await guard.check('user', 'file', 'read', 'Hello');
  if (!result.allowed) throw new Error('Should allow permitted action');
});

runner.test('SecurityGuard - should deny forbidden action', async () => {
  const guard = new SecurityGuard(testConfig);
  guard.permissionManager.assignRole('user', 'user');
  const result = await guard.check('user', 'file', 'delete', 'Hello');
  if (result.allowed) throw new Error('Should deny forbidden action');
});

runner.test('SecurityGuard - should block unsafe content', async () => {
  const guard = new SecurityGuard(testConfig);
  guard.permissionManager.assignRole('user', 'user');
  const result = await guard.check('user', 'file', 'write', 'My password is secret');
  if (result.allowed) throw new Error('Should block unsafe content');
});

runner.test('SecurityGuard - disabled mode should allow all', async () => {
  const guard = new SecurityGuard({ ...testConfig, enabled: false });
  const result = await guard.check('user', 'delete', 'file.txt', 'My password');
  if (!result.allowed) throw new Error('Disabled mode should allow all');
});

// 运行测试
runner.run().then(success => {
  process.exit(success ? 0 : 1);
});
