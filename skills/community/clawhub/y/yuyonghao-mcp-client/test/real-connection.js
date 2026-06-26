// MCP Client 真实连接测试
// 测试连接到 filesystem MCP server

import { MCPClient, MCPClientConfig, MCPServerConfig } from '../src/client.js';

async function testRealConnection() {
  console.log('🧪 MCP Client 真实连接测试开始...\n');

  const client = new MCPClient(new MCPClientConfig({
    name: 'openclaw-test',
    version: '0.1.0',
    autoApprove: true // 测试模式：自动批准
  }));

  try {
    // 配置 filesystem MCP server
    const fsServer = new MCPServerConfig({
      id: 'filesystem',
      name: 'Filesystem Server',
      type: 'stdio',
      command: 'npx',
      args: ['-y', '@modelcontextprotocol/server-filesystem', '.'],
      description: '文件系统服务器 - 访问本地文件',
      capabilities: {
        tools: true,
        resources: true
      }
    });

    console.log('📡 正在连接到 filesystem MCP server...');
    await client.connect(fsServer);

    // 获取服务器能力
    console.log('\n🔍 获取服务器能力...');
    const capabilities = await client.getServerCapabilities('filesystem');
    console.log('工具数量:', capabilities.tools?.length || 0);
    console.log('资源数量:', capabilities.resources?.length || 0);
    console.log('提示词数量:', capabilities.prompts?.length || 0);

    // 列出可用工具
    if (capabilities.tools && capabilities.tools.length > 0) {
      console.log('\n🛠️ 可用工具:');
      capabilities.tools.forEach(tool => {
        console.log(`  - ${tool.name}: ${tool.description || '无描述'}`);
      });
    }

    // 测试调用 read_file 工具
    if (capabilities.tools?.some(t => t.name === 'read_file')) {
      console.log('\n📖 测试读取文件 (package.json)...');
      const result = await client.callTool('filesystem', 'read_file', {
        path: './package.json'
      });
      console.log('读取结果:', result.content?.[0]?.text?.substring(0, 200) + '...');
    }

    // 测试调用 list_directory 工具
    if (capabilities.tools?.some(t => t.name === 'list_directory')) {
      console.log('\n📁 测试列出目录...');
      const result = await client.callTool('filesystem', 'list_directory', {
        path: '.'
      });
      console.log('目录内容:', result.content?.[0]?.text?.split('\n').slice(0, 10).join('\n'));
    }

    console.log('\n🎉 真实连接测试成功！');

  } catch (error) {
    console.error('❌ 测试失败:', error.message);
    if (error.message.includes('ENOENT') || error.message.includes('not found')) {
      console.log('\n💡 提示：filesystem server 可能需要先安装：');
      console.log('   npm install -g @modelcontextprotocol/server-filesystem');
    }
    console.error(error.stack);
  } finally {
    // 关闭连接
    await client.closeAll();
    console.log('\n✅ 测试完成，连接已关闭');
  }
}

testRealConnection();
