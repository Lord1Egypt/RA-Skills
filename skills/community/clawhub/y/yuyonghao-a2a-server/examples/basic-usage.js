/**
 * A2A Server - 基础使用示例
 * 
 * 演示如何启动服务器、连接客户端、进行 RPC 调用和发布订阅
 */

const { A2AServer, A2AClient } = require('../src/index');

// 示例 1: 启动服务器
async function startServer() {
  const server = new A2AServer({
    port: 8080,
    host: 'localhost',
    verbose: true,
  });

  await server.start();
  console.log('✅ 服务器已启动');

  return server;
}

// 示例 2: 创建客户端并连接
async function createClient(agentId, capabilities = []) {
  const client = new A2AClient('ws://localhost:8080', {
    agentId,
    capabilities,
    metadata: { version: '1.0.0' },
    verbose: true,
  });

  await client.connect();
  console.log(`✅ 客户端 ${agentId} 已连接`);

  return client;
}

// 示例 3: RPC 调用
async function rpcExample() {
  console.log('\n=== RPC 调用示例 ===');

  // 创建两个客户端
  const caller = await createClient('caller-agent', ['planning']);
  const receiver = await createClient('receiver-agent', ['execution']);

  // 接收者监听调用
  receiver.on('call', (message) => {
    console.log(`📨 Receiver 收到调用:`, message.payload);
    
    // 发送响应
    receiver.ws.send(JSON.stringify({
      type: 'response',
      to: message.from,
      correlationId: message.correlationId,
      payload: { result: 'Task completed!', data: message.payload },
    }));
  });

  // 调用者发起调用
  try {
    const result = await caller.call('receiver-agent', {
      action: 'execute',
      task: 'analyze data',
    });
    console.log('✅ 调用成功:', result);
  } catch (error) {
    console.log('❌ 调用失败:', error.message);
  }

  // 断开连接
  await caller.disconnect();
  await receiver.disconnect();
}

// 示例 4: 发布/订阅
async function pubSubExample() {
  console.log('\n=== 发布/订阅示例 ===');

  // 创建发布者和订阅者
  const publisher = await createClient('publisher', ['publishing']);
  const subscriber1 = await createClient('subscriber-1', ['listening']);
  const subscriber2 = await createClient('subscriber-2', ['listening']);

  // 订阅者订阅频道
  await subscriber1.subscribe('news');
  await subscriber2.subscribe('news');

  // 监听消息
  subscriber1.on('message', (payload, from) => {
    console.log(`📨 Subscriber-1 收到消息 from ${from}:`, payload);
  });

  subscriber2.on('message', (payload, from) => {
    console.log(`📨 Subscriber-2 收到消息 from ${from}:`, payload);
  });

  // 发布消息
  await publisher.publish('news', {
    type: 'announcement',
    content: 'Hello from A2A!',
  });

  // 等待消息传递
  await new Promise(resolve => setTimeout(resolve, 1000));

  // 断开连接
  await publisher.disconnect();
  await subscriber1.disconnect();
  await subscriber2.disconnect();
}

// 示例 5: 能力发现
async function discoveryExample() {
  console.log('\n=== 能力发现示例 ===');

  // 创建多个具有不同能力的 Agent
  const searchAgent = await createClient('search-agent', ['web-search', 'tavily']);
  const analyzeAgent = await createClient('analyze-agent', ['analysis', 'summarize']);
  const multiAgent = await createClient('multi-agent', ['search', 'analysis', 'planning']);

  // 创建发现客户端
  const discoverer = await createClient('discoverer', ['discovery']);

  // 发现所有 Agent
  const allAgents = await discoverer.discover();
  console.log(`🔍 发现 ${allAgents.length} 个 Agent`);
  allAgents.forEach(agent => {
    console.log(`  - ${agent.agentId}: ${agent.capabilities.join(', ')}`);
  });

  // 按能力发现
  const searchAgents = await discoverer.discover({ capability: 'search' });
  console.log(`\n🔍 具有 'search' 能力的 Agent: ${searchAgents.length} 个`);
  searchAgents.forEach(agent => {
    console.log(`  - ${agent.agentId}`);
  });

  // 断开连接
  await searchAgent.disconnect();
  await analyzeAgent.disconnect();
  await multiAgent.disconnect();
  await discoverer.disconnect();
}

// 主函数
async function main() {
  console.log('🦞 A2A Server 基础使用示例\n');

  // 启动服务器
  const server = await startServer();

  try {
    // 运行示例
    await rpcExample();
    await pubSubExample();
    await discoveryExample();

    console.log('\n✅ 所有示例运行完成！');
  } catch (error) {
    console.error('❌ 示例运行失败:', error);
  } finally {
    // 停止服务器
    await server.stop();
    console.log('🛑 服务器已停止');
  }
}

// 如果直接运行此文件
if (require.main === module) {
  main().catch(console.error);
}

module.exports = {
  startServer,
  createClient,
  rpcExample,
  pubSubExample,
  discoveryExample,
};
