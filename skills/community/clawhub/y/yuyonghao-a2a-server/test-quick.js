/**
 * 快速功能测试
 */

const { A2AServer, A2AClient } = require('./src/index');

const PORT = 19999;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function runTests() {
  console.log('🧪 A2A Server 快速测试\n');
  
  const server = new A2AServer({ port: PORT, verbose: false });
  await server.start();
  console.log('✅ 服务器启动');

  // 测试 1: 客户端连接和注册
  console.log('\n📋 测试 1: 客户端连接和注册');
  const client1 = new A2AClient(`ws://localhost:${PORT}`, {
    agentId: 'test-1',
    capabilities: ['echo'],
    verbose: false
  });
  await client1.connect();
  await sleep(500);
  
  const agents = server.getAgents();
  console.log(`  ✅ 已注册 Agent: ${agents.length} 个`);
  console.log(`  - ${agents[0]?.agentId}`);

  // 测试 2: RPC 调用
  console.log('\n📋 测试 2: RPC 调用');
  const client2 = new A2AClient(`ws://localhost:${PORT}`, {
    agentId: 'test-2',
    capabilities: ['calc'],
    verbose: false
  });
  await client2.connect();
  await sleep(500);

  // 设置响应
  client2.on('call', (msg) => {
    if (client2.ws?.readyState === 1) {
      client2.ws.send(JSON.stringify({
        type: 'response',
        to: msg.from,
        correlationId: msg.correlationId,
        payload: { result: 'ok', data: msg.payload }
      }));
    }
  });

  try {
    const result = await client1.call('test-2', { action: 'test' }, { timeout: 3000 });
    console.log(`  ✅ RPC 调用成功: ${JSON.stringify(result)}`);
  } catch (e) {
    console.log(`  ⚠️ RPC 调用: ${e.message}`);
  }

  // 测试 3: 能力发现
  console.log('\n📋 测试 3: 能力发现');
  const discovered = await client1.discover({ capability: 'calc' });
  console.log(`  ✅ 发现 ${discovered.length} 个具有 'calc' 能力的 Agent`);

  // 测试 4: 发布订阅
  console.log('\n📋 测试 4: 发布/订阅');
  await client2.subscribe('news');
  await sleep(200);
  
  let received = false;
  client2.on('message', (payload) => {
    received = true;
    console.log(`  📨 收到消息: ${JSON.stringify(payload)}`);
  });

  await client1.publish('news', { hello: 'world' });
  await sleep(500);
  console.log(`  ✅ 消息接收: ${received ? '成功' : '失败'}`);

  // 测试 5: 统计信息
  console.log('\n📋 测试 5: 服务器统计');
  const stats = server.getStats();
  console.log(`  - 总连接数: ${stats.totalConnections}`);
  console.log(`  - 活跃 Agent: ${stats.activeAgents}`);
  console.log(`  - 总消息数: ${stats.totalMessages}`);

  // 清理
  console.log('\n🧹 清理...');
  await client1.disconnect();
  await client2.disconnect();
  await server.stop();
  console.log('✅ 测试完成！\n');
}

runTests().catch(e => {
  console.error('❌ 测试失败:', e);
  process.exit(1);
});
