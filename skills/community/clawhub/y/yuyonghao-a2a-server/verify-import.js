/**
 * 验证导入功能
 */

console.log('验证 A2A Server 导入...\n');

// 1. 验证 index.js 导出
try {
  const { A2AServer, A2AClient } = require('./src/index');
  console.log('✅ 从 src/index.js 导入成功');
  console.log('  - A2AServer:', typeof A2AServer === 'function' ? '函数' : '失败');
  console.log('  - A2AClient:', typeof A2AClient === 'function' ? '函数' : '失败');
} catch (error) {
  console.error('❌ 导入失败:', error.message);
  process.exit(1);
}

// 2. 验证类实例化
try {
  const { A2AServer, A2AClient } = require('./src/index');
  
  const server = new A2AServer({ port: 8888, verbose: false });
  console.log('✅ A2AServer 实例化成功');
  
  const client = new A2AClient('ws://localhost:8888', { verbose: false });
  console.log('✅ A2AClient 实例化成功');
} catch (error) {
  console.error('❌ 实例化失败:', error.message);
  process.exit(1);
}

// 3. 验证服务器启动和停止
try {
  const { A2AServer } = require('./src/index');
  
  const server = new A2AServer({ port: 8889, verbose: false });
  
  server.start().then(() => {
    console.log('✅ 服务器启动成功');
    
    server.stop().then(() => {
      console.log('✅ 服务器停止成功');
      console.log('\n🎉 所有验证通过！');
      process.exit(0);
    });
  });
} catch (error) {
  console.error('❌ 服务器测试失败:', error.message);
  process.exit(1);
}
