#!/usr/bin/env node

/**
 * 云效 MCP 操作示例脚本
 *
 * 演示如何使用 YunxiaoMCPClient API：
 * - 连接 MCP Server
 * - 查看工具列表
 * - 调用工具
 *
 * 用法: node examples/demo.mjs
 */

import { createClient } from '../src/index.mjs';

async function main() {
  // 1. 连接 MCP Server
  console.error('[demo] connecting to MCP Server...');
  const client = await createClient('http://localhost:3000');

  if (!client.tools.length) {
    console.error('[demo] no tools available');
    await client.close();
    process.exit(1);
  }

  // 2. 列出工具
  console.error(`[demo] found ${client.tools.length} tools`);
  const tools = client.listTools();
  console.log(JSON.stringify(tools.slice(0, 5), null, 2)); // 只显示前 5 个

  // 3. 查找流水线相关工具
  const pipelineTools = tools.filter((t) => t.name.toLowerCase().includes('pipeline'));
  console.error(`[demo] pipeline tools: ${pipelineTools.map((t) => t.name).join(', ')}`);

  // 4. 查找项目相关工具
  const projectTools = tools.filter((t) => t.name.toLowerCase().includes('project'));
  console.error(`[demo] project tools: ${projectTools.map((t) => t.name).join(', ')}`);

  // 5. 示例：获取当前用户信息
  console.error('[demo] calling get_current_user...');
  const user = await client.callTool('get_current_user', {});
  if (user) {
    console.log(JSON.stringify(user, null, 2));
  } else {
    console.error('[demo] get_current_user returned null');
  }

  await client.close();
}

main().catch((e) => {
  console.error(`[demo] error: ${e.message}`);
  process.exit(1);
});
