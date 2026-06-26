// MCP Servers 集成测试
// 测试 filesystem 和 github 服务器连接

import { MCPClient, MCPServerConfig, MCPClientConfig } from '../src/client.js';
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// 加载配置
const configPath = join(__dirname, '../src/mcp-config.json');
const serverConfigs = JSON.parse(readFileSync(configPath, 'utf-8'));

async function testFilesystemServer() {
  console.log('\n=== 测试 Filesystem MCP Server ===\n');
  
  const client = new MCPClient(new MCPClientConfig({
    name: 'mcp-test-client',
    version: '0.1.0'
  }));

  try {
    // 连接到 filesystem server
    const fsConfig = serverConfigs.filesystem;
    fsConfig.args = [
      '-y',
      '@modelcontextprotocol/server-filesystem',
      'C:\\Users\\99236\\.openclaw\\workspace'
    ];

    console.log('正在连接 filesystem server...');
    await client.connect(fsConfig);

    // 获取服务器能力
    console.log('\n获取服务器能力...');
    const capabilities = await client.getServerCapabilities('filesystem');
    console.log('可用工具:', capabilities.tools.map(t => t.name).join(', '));
    console.log('可用资源:', capabilities.resources.length, '个');
    console.log('可用提示词:', capabilities.prompts.length, '个');

    // 列出工具详情
    console.log('\n工具列表:');
    capabilities.tools.forEach(tool => {
      console.log(`  - ${tool.name}: ${tool.description || '无描述'}`);
    });

    // 测试读取文件
    console.log('\n测试读取文件 (mcp-config.json)...');
    const readResult = await client.callTool('filesystem', 'read_file', {
      path: 'C:\\Users\\99236\\.openclaw\\workspace\\skills\\mcp-client\\src\\mcp-config.json'
    });
    console.log('读取结果:', readResult.content?.[0]?.text?.slice(0, 200) + '...');

    // 测试列出目录
    console.log('\n测试列出目录 (skills/)...');
    const listResult = await client.callTool('filesystem', 'list_directory', {
      path: 'C:\\Users\\99236\\.openclaw\\workspace\\skills'
    });
    console.log('目录内容:', listResult.content?.[0]?.text?.slice(0, 300) + '...');

    console.log('\n✅ Filesystem Server 测试通过！');
    
  } catch (error) {
    console.error('❌ Filesystem Server 测试失败:', error.message);
    throw error;
  } finally {
    await client.closeAll();
  }
}

async function testGitHubServer() {
  console.log('\n=== 测试 GitHub MCP Server ===\n');
  
  const client = new MCPClient(new MCPClientConfig({
    name: 'mcp-test-client',
    version: '0.1.0'
  }));

  try {
    // 检查 GITHUB_TOKEN
    const githubConfig = serverConfigs.github;
    const token = process.env.GITHUB_TOKEN || githubConfig.env.GITHUB_TOKEN;
    
    if (!token) {
      console.log('⚠️  未设置 GITHUB_TOKEN，跳过 GitHub server 测试');
      console.log('设置方法：在 mcp-config.json 中配置 env.GITHUB_TOKEN');
      return;
    }

    githubConfig.env.GITHUB_TOKEN = token;

    console.log('正在连接 GitHub server...');
    await client.connect(githubConfig);

    // 获取服务器能力
    console.log('\n获取服务器能力...');
    const capabilities = await client.getServerCapabilities('github');
    console.log('可用工具:', capabilities.tools.map(t => t.name).join(', '));

    // 列出工具详情
    console.log('\n工具列表:');
    capabilities.tools.forEach(tool => {
      console.log(`  - ${tool.name}: ${tool.description || '无描述'}`);
    });

    console.log('\n✅ GitHub Server 测试通过！');
    
  } catch (error) {
    console.error('❌ GitHub Server 测试失败:', error.message);
    throw error;
  } finally {
    await client.closeAll();
  }
}

async function runTests() {
  console.log('🚀 MCP Servers 集成测试开始\n');
  console.log('工作目录:', 'C:\\Users\\99236\\.openclaw\\workspace');
  
  try {
    // 测试 filesystem server
    await testFilesystemServer();
    
    // 测试 github server
    await testGitHubServer();
    
    console.log('\n🎉 所有测试完成！');
  } catch (error) {
    console.error('\n💥 测试失败:', error.message);
    process.exit(1);
  }
}

// 运行测试
runTests();
