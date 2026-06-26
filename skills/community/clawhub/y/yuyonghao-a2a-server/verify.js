/**
 * A2A Server 手动验证脚本
 * 
 * 使用方法:
 * 1. 终端 1: node verify.js server
 * 2. 终端 2: node verify.js client1
 * 3. 终端 3: node verify.js client2
 */

const { A2AServer } = require('./src/server');
const { A2AClient } = require('./src/client');

const PORT = 8080;

async function runServer() {
  console.log('🚀 Starting A2A Server...');
  const server = new A2AServer({ port: PORT, verbose: true });
  await server.start();
  console.log(`✅ Server running on ws://localhost:${PORT}`);
  
  // 每 10 秒打印统计
  setInterval(() => {
    const stats = server.getStats();
    console.log(`📊 Stats: ${stats.activeAgents} agents, ${stats.totalMessages} messages`);
  }, 10000);

  process.on('SIGINT', async () => {
    await server.stop();
    process.exit(0);
  });
}

async function runClient1() {
  console.log('🤖 Starting Client 1 (Service Provider)...');
  const client = new A2AClient(`ws://localhost:${PORT}`, {
    agentId: 'service-provider',
    capabilities: ['search', 'analyze'],
    verbose: true
  });

  client.on('registered', () => {
    console.log('✅ Registered as service-provider');
    console.log('   Capabilities: search, analyze');
  });

  client.on('call', async (message) => {
    console.log(`📨 Received call from ${message.from}:`, message.payload);
    
    // Echo response
    client.ws.send(JSON.stringify({
      type: 'response',
      to: message.from,
      correlationId: message.correlationId,
      payload: { 
        result: `Echo: ${JSON.stringify(message.payload)}`,
        timestamp: new Date().toISOString()
      }
    }));
  });

  await client.connect();
  
  console.log('\n💡 Client 1 ready. Waiting for calls...');
  console.log('   Press Ctrl+C to exit');

  process.on('SIGINT', async () => {
    await client.disconnect();
    process.exit(0);
  });
}

async function runClient2() {
  console.log('🤖 Starting Client 2 (Service Consumer)...');
  const client = new A2AClient(`ws://localhost:${PORT}`, {
    agentId: 'service-consumer',
    verbose: true
  });

  client.on('registered', async () => {
    console.log('✅ Registered as service-consumer');
    
    // Discover agents
    console.log('\n🔍 Discovering agents...');
    const agents = await client.discover();
    console.log(`   Found ${agents.length} agent(s):`);
    agents.forEach(a => {
      console.log(`   - ${a.agentId}: ${a.capabilities.join(', ')}`);
    });

    // Call service provider
    if (agents.some(a => a.agentId === 'service-provider')) {
      console.log('\n📞 Calling service-provider...');
      const result = await client.call('service-provider', {
        action: 'search',
        query: 'AI trends 2026'
      }, { timeout: 10000 });
      
      console.log('✅ Response:', result);
    }

    // Test pub/sub
    console.log('\n📢 Testing publish/subscribe...');
    await client.subscribe('test-channel');
    
    client.messageHandlers.set('test-channel', [(payload) => {
      console.log('📨 Received message:', payload);
    }]);

    await client.publish('test-channel', { 
      message: 'Hello from client 2',
      timestamp: new Date().toISOString()
    });
    console.log('✅ Message published');

    console.log('\n✅ All tests completed!');
    console.log('   Press Ctrl+C to exit');
  });

  await client.connect();

  process.on('SIGINT', async () => {
    await client.disconnect();
    process.exit(0);
  });
}

// Main
const command = process.argv[2];

switch (command) {
  case 'server':
    runServer();
    break;
  case 'client1':
    runClient1();
    break;
  case 'client2':
    runClient2();
    break;
  default:
    console.log('Usage: node verify.js [server|client1|client2]');
    console.log('');
    console.log('Terminal 1: node verify.js server   # Start server');
    console.log('Terminal 2: node verify.js client1  # Start service provider');
    console.log('Terminal 3: node verify.js client2  # Start service consumer (runs tests)');
    process.exit(1);
}
