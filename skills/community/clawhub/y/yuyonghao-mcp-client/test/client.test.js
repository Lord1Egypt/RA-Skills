// MCP Client 完整测试套件
// 测试基础连接和功能

import { MCPClient, MCPClientConfig, MCPServerConfig, MCPError, MCPConnectionError } from '../src/client.js';

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

function assertInstanceOf(obj, constructor, message) {
  if (!(obj instanceof constructor)) {
    throw new Error(message || `Expected instance of ${constructor.name}`);
  }
}

console.log('🧪 MCP Client 测试开始...\n');

// 测试 1: MCPClientConfig
console.log('📦 MCPClientConfig 测试');
test('默认配置', () => {
  const config = new MCPClientConfig();
  assertEqual(config.name, 'openclaw-mcp-client');
  assertEqual(config.version, '0.1.0');
  assertEqual(config.timeout, 30000);
  assertEqual(config.autoApprove, false);
});

test('自定义配置', () => {
  const config = new MCPClientConfig({
    name: 'custom-client',
    version: '1.0.0',
    timeout: 60000,
    autoApprove: true
  });
  assertEqual(config.name, 'custom-client');
  assertEqual(config.version, '1.0.0');
  assertEqual(config.timeout, 60000);
  assertEqual(config.autoApprove, true);
});

// 测试 2: MCPServerConfig
console.log('\n📦 MCPServerConfig 测试');
test('stdio 服务器配置', () => {
  const config = new MCPServerConfig({
    id: 'test-fs',
    name: 'Test Filesystem',
    type: 'stdio',
    command: 'npx',
    args: ['-y', '@modelcontextprotocol/server-filesystem', '.']
  });
  assertEqual(config.id, 'test-fs');
  assertEqual(config.name, 'Test Filesystem');
  assertEqual(config.type, 'stdio');
  assertEqual(config.command, 'npx');
  assertEqual(config.args.length, 3);
});

test('sse 服务器配置', () => {
  const config = new MCPServerConfig({
    id: 'test-sse',
    name: 'Test SSE Server',
    type: 'sse',
    url: 'http://localhost:3000/sse'
  });
  assertEqual(config.id, 'test-sse');
  assertEqual(config.type, 'sse');
  assertEqual(config.url, 'http://localhost:3000/sse');
});

// 测试 3: MCPClient 基础功能
console.log('\n📦 MCPClient 基础功能测试');
test('客户端实例创建', () => {
  const client = new MCPClient();
  assertTrue(client instanceof MCPClient);
  assertTrue(client.connections instanceof Map);
  assertTrue(client.approvedTools instanceof Set);
});

test('带配置的客户端实例', () => {
  const config = new MCPClientConfig({ name: 'test-client', autoApprove: true });
  const client = new MCPClient(config);
  assertEqual(client.config.name, 'test-client');
  assertEqual(client.config.autoApprove, true);
});

// 测试 4: 错误类
console.log('\n📦 MCPError 测试');
test('MCPError 基础功能', () => {
  const error = new MCPError('Test error', 'TEST_CODE', { detail: 'test' });
  assertEqual(error.message, 'Test error');
  assertEqual(error.code, 'TEST_CODE');
  assertEqual(error.details.detail, 'test');
  assertInstanceOf(error, Error);
});

test('MCPConnectionError', () => {
  const error = new MCPConnectionError('Connection failed', 'server-1', new Error('timeout'));
  assertEqual(error.message, 'Connection failed');
  assertEqual(error.code, 'CONNECTION_FAILED');
  assertEqual(error.serverId, 'server-1');
  assertInstanceOf(error, MCPError);
});

// 测试 5: 事件系统
console.log('\n📦 事件系统测试');
test('事件监听和触发', () => {
  const client = new MCPClient();
  let eventFired = false;
  let eventData = null;
  
  client.on('test', (data) => {
    eventFired = true;
    eventData = data;
  });
  
  client.emit('test', { foo: 'bar' });
  
  assertTrue(eventFired, '事件应该被触发');
  assertEqual(eventData.foo, 'bar');
});

test('多个事件处理器', () => {
  const client = new MCPClient();
  let count = 0;
  
  client.on('multi', () => count++);
  client.on('multi', () => count++);
  
  client.emit('multi', {});
  
  assertEqual(count, 2, '两个处理器都应该被调用');
});

// 测试 6: 工具和资源批准
console.log('\n📦 批准系统测试');
test('批准工具', () => {
  const client = new MCPClient();
  client.approveTool('server1', 'tool1');
  assertTrue(client.approvedTools.has('server1:tool1'));
});

test('批准资源', () => {
  const client = new MCPClient();
  client.approveResource('file:///test.txt');
  assertTrue(client.approvedResources.has('file:///test.txt'));
});

// 测试 7: 连接状态
console.log('\n📦 连接状态测试');
test('初始连接状态为空', () => {
  const client = new MCPClient();
  const status = client.getConnectionStatus();
  assertEqual(status.length, 0);
});

// 测试 8: 重试机制
console.log('\n📦 重试机制测试');
await asyncTest('withRetry 成功', async () => {
  const client = new MCPClient();
  let callCount = 0;
  
  const result = await client.withRetry(async () => {
    callCount++;
    return 'success';
  }, 'ERROR', 'Failed');
  
  assertEqual(result, 'success');
  assertEqual(callCount, 1);
});

await asyncTest('withRetry 失败后成功', async () => {
  const client = new MCPClient();
  let callCount = 0;
  
  const result = await client.withRetry(async () => {
    callCount++;
    if (callCount < 2) {
      throw new Error('Temporary error');
    }
    return 'success';
  }, 'ERROR', 'Failed');
  
  assertEqual(result, 'success');
  assertEqual(callCount, 2);
});

// 测试 9: 传输层创建
console.log('\n📦 传输层创建测试');
test('创建 stdio 传输层配置', () => {
  const client = new MCPClient();
  const config = new MCPServerConfig({
    id: 'test',
    name: 'Test',
    type: 'stdio',
    command: 'node',
    args: ['script.js']
  });
  
  // 验证配置正确性，实际创建需要 SDK
  assertEqual(config.type, 'stdio');
  assertEqual(config.command, 'node');
});

test('创建 sse 传输层配置', () => {
  const client = new MCPClient();
  const config = new MCPServerConfig({
    id: 'test',
    name: 'Test',
    type: 'sse',
    url: 'http://localhost:3000/sse'
  });
  
  assertEqual(config.type, 'sse');
  assertEqual(config.url, 'http://localhost:3000/sse');
});

test('不支持的传输类型', () => {
  const client = new MCPClient();
  const config = new MCPServerConfig({
    id: 'test',
    name: 'Test',
    type: 'unsupported'
  });
  
  try {
    client.createTransport(config);
    throw new Error('应该抛出错误');
  } catch (error) {
    assertEqual(error.code, 'UNSUPPORTED_TRANSPORT');
  }
});

// 测试 10: 睡眠工具
console.log('\n📦 工具函数测试');
await asyncTest('sleep 函数', async () => {
  const client = new MCPClient();
  const start = Date.now();
  await client.sleep(50);
  const elapsed = Date.now() - start;
  assertTrue(elapsed >= 45, '应该等待至少 50ms');
});

// 总结
console.log('\n' + '='.repeat(50));
console.log(`📊 测试结果: ${testsPassed} 通过, ${testsFailed} 失败`);
console.log('='.repeat(50));

if (testsFailed > 0) {
  process.exit(1);
} else {
  console.log('\n🎉 所有测试通过！');
}
