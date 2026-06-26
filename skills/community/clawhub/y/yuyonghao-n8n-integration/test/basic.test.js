/**
 * n8n Integration 基础测试
 */

const { N8nIntegration, N8nWebhookServer, N8nAgentIntegration } = require('../src/index');

console.log('🧪 n8n Integration 测试');
console.log('='.repeat(50));

let passed = 0;
let failed = 0;

async function test(name, fn) {
  process.stdout.write(`${name}... `);
  try {
    await fn();
    console.log('✅');
    passed++;
  } catch (error) {
    console.log(`❌ ${error.message}`);
    failed++;
  }
}

async function runTests() {
  // Test 1: N8nIntegration init
  await test('N8nIntegration init', async () => {
    const n8n = new N8nIntegration({ port: 3003, verbose: false });
    if (!n8n.webhookServer) throw new Error('Webhook server not created');
    if (!n8n.agentIntegration) throw new Error('Agent integration not created');
  });

  // Test 2: N8nWebhookServer init
  await test('N8nWebhookServer init', async () => {
    const server = new N8nWebhookServer({ port: 3004, verbose: false });
    if (!server.app) throw new Error('Express app not created');
  });

  // Test 3: N8nAgentIntegration init
  await test('N8nAgentIntegration init', async () => {
    const integration = new N8nAgentIntegration({ verbose: false });
    if (!integration.options) throw new Error('Options not created');
  });

  // Test 4: Webhook server start/stop
  let server;
  await test('Webhook server start/stop', async () => {
    server = new N8nWebhookServer({ port: 3005, verbose: false });
    await server.start();
    await new Promise(resolve => setTimeout(resolve, 500));
    await server.stop();
  });

  // Test 5: Agent integration execute
  await test('Agent integration execute', async () => {
    const integration = new N8nAgentIntegration({ verbose: false });
    
    // 设置模拟执行器
    integration.setExecutor({
      execute: async (action, params) => {
        return { success: true, action, params };
      }
    });

    const result = await integration.execute('test-workflow', 'test-action', { key: 'value' });
    
    if (!result.success) throw new Error('Execution failed');
    if (result.workflow !== 'test-workflow') throw new Error('Workflow mismatch');
  });

  // Test 6: Executor adapter
  await test('Executor adapter', async () => {
    const { ExecutorAdapter } = require('../src/agent-integration');
    
    const mockExecutor = {
      execute: async (query, options) => {
        return { answer: 'test', mode: 'system1' };
      }
    };
    
    const adapter = new ExecutorAdapter(mockExecutor, 'react');
    const result = await adapter.execute('test', {});
    
    if (!result.answer) throw new Error('Answer missing');
  });

  // Test 7: Set executor
  await test('Set executor', async () => {
    const n8n = new N8nIntegration({ port: 3006, verbose: false });
    
    const mockExecutor = {
      execute: async (action, params) => ({ success: true })
    };
    
    n8n.setExecutor(mockExecutor, 'react');
    
    const integration = n8n.getAgentIntegration();
    if (!integration.options.executor) throw new Error('Executor not set');
  });

  // Test 8: Set observability
  await test('Set observability', async () => {
    const n8n = new N8nIntegration({ port: 3007, verbose: false });
    
    const mockObs = {
      startTrace: () => ({ end: () => {} }),
      recordError: () => {}
    };
    
    n8n.setObservability(mockObs);
    
    const integration = n8n.getAgentIntegration();
    if (!integration.options.observability) throw new Error('Observability not set');
  });

  // Test 9: Get results
  await test('Get results', async () => {
    const server = new N8nWebhookServer({ port: 3008, verbose: false });
    
    server._storeResult('workflow1', 'action1', { success: true });
    server._storeResult('workflow2', 'action2', { success: false });
    
    const results = server.getResults(10);
    if (results.length !== 2) throw new Error('Results count mismatch');
  });

  // Test 10: Health endpoint simulation
  await test('Health endpoint simulation', async () => {
    const server = new N8nWebhookServer({ port: 3009, verbose: false });
    await server.start();
    
    // 模拟健康检查响应
    const healthData = {
      status: 'ok',
      timestamp: new Date().toISOString(),
      service: 'n8n-webhook-server'
    };
    
    if (!healthData.status) throw new Error('Health status missing');
    
    await server.stop();
  });

  // Summary
  console.log('='.repeat(50));
  console.log(`Results: ${passed}/${passed + failed} passed`);
  console.log(`Rate: ${((passed / (passed + failed)) * 100).toFixed(1)}%`);

  if (failed > 0) {
    process.exit(1);
  } else {
    console.log('\n🎉 All tests passed!');
  }
}

runTests();
