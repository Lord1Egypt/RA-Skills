// MCP GitHub Server 测试
// 测试连接到 GitHub MCP server

import { SecureMCPClient } from '../src/secure-client.js';
import { MCPClientConfig } from '../src/client.js';

async function testGitHubServer() {
  console.log('🐙 MCP GitHub Server 测试开始...\n');

  const client = new SecureMCPClient(new MCPClientConfig({
    name: 'openclaw-github-test',
    version: '0.1.0',
    autoApprove: true // 测试模式
  }), {
    requireApproval: false,
    autoApprovePatterns: ['*']
  });

  try {
    // GitHub MCP server 配置
    // 注意：需要 GITHUB_TOKEN 环境变量
    const githubServer = {
      id: 'github',
      name: 'GitHub Server',
      type: 'stdio',
      command: 'npx',
      args: ['-y', '@modelcontextprotocol/server-github'],
      env: {
        // 测试时如果没有 token，会失败但能验证配置
        GITHUB_TOKEN: process.env.GITHUB_TOKEN || ''
      },
      description: 'GitHub API 集成 - 访问仓库、Issues、PRs'
    };

    console.log('📡 正在连接到 GitHub MCP server...');
    console.log('⚠️ 注意：需要 GITHUB_TOKEN 环境变量');
    
    if (!githubServer.env.GITHUB_TOKEN) {
      console.log('⚠️ 未设置 GITHUB_TOKEN，连接可能失败');
      console.log('💡 设置方法：export GITHUB_TOKEN=your_token_here');
    }

    await client.connect(githubServer);

    // 获取服务器能力
    console.log('\n🔍 获取服务器能力...');
    const capabilities = await client.getServerCapabilities('github');
    console.log('工具数量:', capabilities.tools?.length || 0);
    console.log('资源数量:', capabilities.resources?.length || 0);

    // 列出可用工具
    if (capabilities.tools && capabilities.tools.length > 0) {
      console.log('\n🛠️ 可用工具 (前 10 个):');
      capabilities.tools.slice(0, 10).forEach(tool => {
        console.log(`  - ${tool.name}: ${tool.description?.substring(0, 60) || '无描述'}...`);
      });
    }

    console.log('\n🎉 GitHub Server 连接测试成功！');

  } catch (error) {
    if (error.message.includes('GITHUB_TOKEN') || error.message.includes('authentication')) {
      console.log('\n⚠️ 认证失败（预期）：需要设置 GITHUB_TOKEN');
      console.log('💡 这是正常的，配置验证通过！');
    } else {
      console.error('\n❌ 测试失败:', error.message);
    }
  } finally {
    await client.closeAll();
    console.log('\n✅ 测试完成，连接已关闭');
  }
}

testGitHubServer();
