/**
 * A2A Server - 简单测试
 * 
 * 快速验证服务器和客户端是否能正常工作
 */

const { A2AServer, A2AClient } = require('../src/index');

async function runTest() {
  console.log('🧪 A2A Server 简单测试\n');

  // 1. 启动服务器
  console.log('1. 启动服务器...');
  const server = new A2AServer({
    port: 9999,
    host: 'localhost',
    verbose: false,
  });
  await server.start();
  console.log('   ✅ 服务器启动成功\n');

  // 2. 创建客户端
  console.log('2. 创建客户端...');
  const client1 = new A2AClient('ws://localhost:9999', {
    agentId: 'test-agent-1',
    capabilities: ['test'],
    verbose: false,
  });
  await client1.connect();
  
  // 等待注册完成
  await new Promise(resolve => setTimeout(resolve, 500));
  
  console.log('   ✅ 客户端连接成功\n');

  // 3. 验证注册
  console.log('3. 验证 Agent 注册...');
  const agents = server.getAgents();
  console.log(`   ✅ 已注册 Agent 数量: ${agents.length}`);
  if (agents.length > 0) {
    console.log(`   - ${agents[0].agentId}\n`);
  }

  // 4. 创建第二个客户端测试消息
  console.log('4. 测试消息传递...');
  const client2 = new A2AClient('ws://localhost:9999', {
    agentId: 'test-agent-2',
    capabilities: ['echo'],
    verbose: false,
  });
  await client2.connect();
  await new Promise(resolve => setTimeout(resolve, 500));

  // 设置消息监听 - 处理 call 类型的消息
  client2.on('call', (message) => {
    console.log(`   📨 收到调用: ${JSON.stringify(message.payload)}`);
    
    // 回复
    if (client2.ws && client2.ws.readyState === 1) {
      client2.ws.send(JSON.stringify({
        type: 'response',
        to: message.from,
        correlationId: message.correlationId,
        payload: { echo: message.payload },
      }));
    }
  });

  // 发送调用
  try {
    const result = await client1.call('test-agent-2', { test: 'hello' });
    console.log(`   ✅ 调用成功: ${JSON.stringify(result)}\n`);
  } catch (error) {
    console.log(`   ❌ 调用失败: ${error.message}\n`);
  }

  // 5. 测试发布订阅
  console.log('5. 测试发布/订阅...');
  await client2.subscribe('test-channel');
  await new Promise(resolve => setTimeout(resolve, 200));
  
  let received = false;
  client2.on('message', (payload) => {
    console.log(`   📨 收到频道消息: ${JSON.stringify(payload)}`);
    received = true;
  });

  await client1.publish('test-channel', { msg: 'hello world' });
  
  // 等待消息传递
  await new Promise(resolve => setTimeout(resolve, 500));
  console.log(`   ✅ 消息接收: ${received ? '成功' : '失败'}\n`);

  // 6. 测试能力发现
  console.log('6. 测试能力发现...');
  const discovered = await client1.discover({ capability: 'echo' });
  console.log(`   ✅ 发现 ${discovered.length} 个具有 'echo' 能力的 Agent\n`);

  // 7. 获取统计信息
  console.log('7. 获取服务器统计...');
  const stats = server.getStats();
  console.log(`   - 总连接数: ${stats.totalConnections}`);
  console.log(`   - 活跃 Agent: ${stats.activeAgents}`);
  console.log(`   - 总消息数: ${stats.totalMessages}`);
  console.log(`   - 运行时间: ${Math.floor(stats.uptime)}s\n`);

  // 清理
  console.log('8. 清理...');
  await client1.disconnect();
  await client2.disconnect();
  await server.stop();
  console.log('   ✅ 测试完成！\n');
}

// 运行测试
runTest().catch(error => {
  console.error('❌ 测试失败:', error);
  process.exit(1);
});
