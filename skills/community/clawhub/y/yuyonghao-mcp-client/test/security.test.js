// MCP 安全控制完整测试套件

import { SecureMCPClient, MCPSecurityController, MCPClientError, MCPErrorCode } from '../src/secure-client.js';
import { MCPClientConfig } from '../src/client.js';

// 测试计数器
let testsPassed = 0;
let testsFailed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`  ✅ ${name}`);
    testsPassed++;
  } catch (error) {
    console.log(`  ❌ ${name}: ${error.message}`);
    testsFailed++;
  }
}

function asyncTest(name, fn) {
  return new Promise(async (resolve) => {
    try {
      await fn();
      console.log(`  ✅ ${name}`);
      testsPassed++;
    } catch (error) {
      console.log(`  ❌ ${name}: ${error.message}`);
      testsFailed++;
    }
    resolve();
  });
}

function assertEqual(actual, expected, message) {
  if (actual !== expected) {
    throw new Error(`${message || 'Assertion failed'}: expected ${expected}, got ${actual}`);
  }
}

function assertTrue(value, message) {
  if (!value) {
    throw new Error(message || 'Expected true but got false');
  }
}

function assertFalse(value, message) {
  if (value) {
    throw new Error(message || 'Expected false but got true');
  }
}

console.log('🔒 MCP 安全控制测试开始...\n');

// 测试 1: MCPSecurityController 基础功能
console.log('📦 MCPSecurityController 基础测试');
test('默认配置', () => {
  const security = new MCPSecurityController();
  assertEqual(security.requireApproval, true);
  assertTrue(Array.isArray(security.autoApprovePatterns));
  assertTrue(Array.isArray(security.blockedPatterns));
});

test('自定义配置', () => {
  const security = new MCPSecurityController({
    requireApproval: false,
    autoApprovePatterns: ['read_*'],
    blockedPatterns: ['delete_*']
  });
  assertEqual(security.requireApproval, false);
  assertEqual(security.autoApprovePatterns.length, 1);
  assertEqual(security.blockedPatterns.length, 1);
});

// 测试 2: 工具批准检查
console.log('\n📦 工具批准检查测试');
test('新工具需要批准', () => {
  const security = new MCPSecurityController();
  const needsApproval = security.shouldRequireApproval('server1', 'write_file', {});
  assertTrue(needsApproval);
});

test('已批准工具不需要再次批准', () => {
  const security = new MCPSecurityController();
  security.approveTool('server1', 'read_file');
  const needsApproval = security.shouldRequireApproval('server1', 'read_file', {});
  assertFalse(needsApproval);
});

test('自动批准模式', () => {
  const security = new MCPSecurityController({
    autoApprovePatterns: ['*:read_*']
  });
  const needsApproval = security.shouldRequireApproval('server1', 'read_file', {});
  assertFalse(needsApproval);
});

test('禁止模式', () => {
  const security = new MCPSecurityController({
    blockedPatterns: ['*:delete_*']
  });
  
  try {
    security.shouldRequireApproval('server1', 'delete_file', {});
    throw new Error('应该抛出错误');
  } catch (error) {
    assertTrue(error.message.includes('被禁止'));
  }
});

// 测试 3: 资源访问检查
console.log('\n📦 资源访问检查测试');
test('普通资源访问', () => {
  const security = new MCPSecurityController();
  const needsApproval = security.checkResourceAccess('server1', '/home/user/doc.txt');
  assertTrue(needsApproval);
});

test('已批准资源', () => {
  const security = new MCPSecurityController();
  security.approvedResources.set('server1:/home/user/doc.txt', { approvedAt: new Date() });
  const canAccess = security.checkResourceAccess('server1', '/home/user/doc.txt');
  assertTrue(canAccess);
});

test('敏感路径检测 - .env 文件', () => {
  const security = new MCPSecurityController();
  const isSensitive = security.isSensitivePath('/app/.env');
  assertTrue(isSensitive);
});

test('敏感路径检测 - git 目录', () => {
  const security = new MCPSecurityController();
  const isSensitive = security.isSensitivePath('/project/.git/config');
  assertTrue(isSensitive);
});

test('敏感路径检测 - passwd', () => {
  const security = new MCPSecurityController();
  const isSensitive = security.isSensitivePath('/etc/passwd');
  assertTrue(isSensitive);
});

test('敏感路径访问被拒绝', () => {
  const security = new MCPSecurityController();
  
  try {
    security.checkResourceAccess('server1', '/etc/passwd');
    throw new Error('应该抛出错误');
  } catch (error) {
    assertTrue(error.message.includes('敏感资源'));
  }
});

// 测试 4: 审计日志
console.log('\n📦 审计日志测试');
test('记录日志', () => {
  const security = new MCPSecurityController();
  security.log('test_action', { key: 'value' });
  assertEqual(security.auditLog.length, 1);
  assertEqual(security.auditLog[0].action, 'test_action');
  assertEqual(security.auditLog[0].details.key, 'value');
});

test('获取审计日志', () => {
  const security = new MCPSecurityController();
  security.log('action1', {});
  security.log('action2', {});
  security.log('action3', {});
  
  const logs = security.getAuditLog(2);
  assertEqual(logs.length, 2);
  assertEqual(logs[0].action, 'action2');
  assertEqual(logs[1].action, 'action3');
});

test('日志数量限制', () => {
  const security = new MCPSecurityController();
  
  // 添加超过 1000 条日志
  for (let i = 0; i < 1005; i++) {
    security.log('action', { index: i });
  }
  
  assertTrue(security.auditLog.length <= 1000);
});

// 测试 5: 模式匹配
console.log('\n📦 模式匹配测试');
test('精确匹配', () => {
  const security = new MCPSecurityController();
  const matches = security.matchesPattern('server1:read_file', 'server1:read_file');
  assertTrue(matches);
});

test('通配符匹配', () => {
  const security = new MCPSecurityController();
  const matches = security.matchesPattern('server1:read_file', '*:read_*');
  assertTrue(matches);
});

test('正则表达式匹配', () => {
  const security = new MCPSecurityController();
  const matches = security.matchesPattern('server1:read_file', /read_/);
  assertTrue(matches);
});

test('不匹配', () => {
  const security = new MCPSecurityController();
  const matches = security.matchesPattern('server1:write_file', '*:read_*');
  assertFalse(matches);
});

// 测试 6: SecureMCPClient
console.log('\n📦 SecureMCPClient 测试');
test('安全客户端创建', () => {
  const client = new SecureMCPClient();
  assertTrue(client.security instanceof MCPSecurityController);
  assertEqual(client.retryConfig.maxRetries, 3);
});

test('带安全选项的客户端', () => {
  const client = new SecureMCPClient(
    new MCPClientConfig(),
    {
      requireApproval: false,
      blockedPatterns: ['delete_*']
    }
  );
  assertEqual(client.security.requireApproval, false);
  assertEqual(client.security.blockedPatterns.length, 1);
});

// 测试 7: 错误类
console.log('\n📦 错误类测试');
test('MCPClientError', () => {
  const error = new MCPClientError('TEST_CODE', 'Test message', { detail: 'test' });
  assertEqual(error.code, 'TEST_CODE');
  assertEqual(error.message, 'Test message');
  assertEqual(error.details.detail, 'test');
});

test('错误码常量', () => {
  assertEqual(MCPErrorCode.CONNECTION_FAILED, 'CONNECTION_FAILED');
  assertEqual(MCPErrorCode.PERMISSION_DENIED, 'PERMISSION_DENIED');
  assertEqual(MCPErrorCode.TOOL_EXECUTION_FAILED, 'TOOL_EXECUTION_FAILED');
});

// 测试 8: 重试机制
console.log('\n📦 重试机制测试');
await asyncTest('withRetry 成功', async () => {
  const client = new SecureMCPClient();
  let callCount = 0;
  
  const result = await client.withRetry(async () => {
    callCount++;
    return 'success';
  }, 'ERROR', 'Failed');
  
  assertEqual(result, 'success');
  assertEqual(callCount, 1);
});

await asyncTest('withRetry 失败后成功', async () => {
  const client = new SecureMCPClient();
  let callCount = 0;
  
  const result = await client.withRetry(async () => {
    callCount++;
    if (callCount < 3) {
      throw new Error('Temporary error');
    }
    return 'success';
  }, 'ERROR', 'Failed');
  
  assertEqual(result, 'success');
  assertEqual(callCount, 3);
});

await asyncTest('withRetry 最终失败', async () => {
  const client = new SecureMCPClient();
  
  try {
    await client.withRetry(async () => {
      throw new Error('Persistent error');
    }, 'ERROR', 'Failed');
    throw new Error('应该抛出错误');
  } catch (error) {
    assertEqual(error.code, 'ERROR');
    assertTrue(error.message.includes('Failed'));
  }
});

// 测试 9: 错误统计
console.log('\n📦 错误统计测试');
test('错误统计 - 无错误', () => {
  const client = new SecureMCPClient();
  const stats = client.getErrorStats();
  assertEqual(stats.total, 0);
  assertEqual(stats.errors, 0);
  assertEqual(stats.errorRate, 0);
});

test('错误统计 - 有错误', () => {
  const client = new SecureMCPClient();
  client.security.log('action1', { error: 'error1' });
  client.security.log('action2', {});
  client.security.log('action3', { error: 'error2' });
  
  const stats = client.getErrorStats();
  assertEqual(stats.total, 3);
  assertEqual(stats.errors, 2);
  assertTrue(stats.errorRate > 0);
});

// 测试 10: 批准工具（永久）
console.log('\n📦 永久批准测试');
test('永久批准工具', () => {
  const client = new SecureMCPClient();
  client.approveTool('server1', 'read_file', true);
  
  const approved = client.security.approvedTools.get('server1:read_file');
  assertTrue(approved.permanent);
  assertTrue(approved.approvedAt instanceof Date);
});

// 总结
console.log('\n' + '='.repeat(50));
console.log(`📊 测试结果: ${testsPassed} 通过, ${testsFailed} 失败`);
console.log('='.repeat(50));

if (testsFailed > 0) {
  process.exit(1);
} else {
  console.log('\n🎉 所有安全测试通过！');
}