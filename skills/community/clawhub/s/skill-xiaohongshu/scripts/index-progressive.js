#!/usr/bin/env node
/**
 * XHS MCP Server - 渐进式测试版
 * 逐步添加工具，找出问题
 */

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js';
import express from 'express';
import { z } from 'zod';

const PORT = 18060;
const server = new McpServer({ name: 'xhs-mcp-test', version: '1.0.0' });

console.error('开始注册工具...');

// 先注册一个简单工具
server.tool('ping', '测试工具', {}, async () => ({
  content: [{ type: 'text', text: JSON.stringify({ status: 'ok', message: 'pong' }) }],
}));

console.error('✅ 简单工具注册完成');

// 再注册一个需要导入的工具
try {
  const { checkLoginStatus } = await import('./xhs-tools.js');
  console.error('✅ xhs-tools.js 导入成功');

  server.tool('check_login_status', '检查登录状态', {}, async () => {
    const result = await checkLoginStatus();
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  });
  console.error('✅ check_login_status 注册成功');
} catch (error) {
  console.error('❌ 导入xhs-tools失败:', error);
}

const app = express();
const transport = new StreamableHTTPServerTransport();

console.error('连接Transport...');
await server.connect(transport);
console.error('✅ Transport连接成功');

app.all('/mcp', async (req, res) => {
  console.error(`\n${req.method} ${req.url}`);
  try {
    await transport.handleRequest(req, res);
  } catch (error) {
    console.error('错误:', error);
    if (!res.headersSent) {
      res.status(500).send(error.message);
    }
  }
});

app.get('/health', (req, res) => res.json({ status: 'ok' }));

app.listen(PORT, () => {
  console.error(`\n✅ 服务启动: http://localhost:${PORT}/mcp`);
});
