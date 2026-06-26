#!/usr/bin/env node
/**
 * XHS MCP Server - 使用 SSE 传输
 * 参考: https://github.com/modelcontextprotocol/typescript-sdk
 */

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { SSEServerTransport } from '@modelcontextprotocol/sdk/server/sse.js';
import express from 'express';
import { z } from 'zod';
import {
  checkLoginStatus,
  getLoginQRCode,
  deleteCookies,
  listFeeds,
  searchFeeds,
  getFeedDetail,
  likeFeed,
  favoriteFeed,
  postComment,
  replyComment,
  userProfile,
  publishContent,
  publishWithVideo,
} from './xhs-tools.js';
import { closeBrowser } from './browser.js';

// 配置
const PORT = process.env.XHS_PORT || 18060;
const HOST = process.env.XHS_HOST || '0.0.0.0';

// 创建 MCP Server
const server = new McpServer({
  name: 'xhs-mcp-service',
  version: '1.0.0',
});

// ========== 注册 MCP 工具（与之前相同）==========

// 1. 检查登录状态
server.tool(
  'check_login_status',
  '检查小红书登录状态',
  {},
  async () => {
    const result = await checkLoginStatus();
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(result, null, 2),
        },
      ],
    };
  }
);

// 2. 获取登录二维码
server.tool(
  'get_login_qrcode',
  '获取登录二维码，返回 Base64 图片和超时时间',
  {},
  async () => {
    const result = await getLoginQRCode();
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(result, null, 2),
        },
      ],
    };
  }
);

// 3. 删除登录状态
server.tool(
  'delete_cookies',
  '删除 cookies 文件，重置登录状态，删除后需要重新登录',
  {},
  async () => {
    const result = await deleteCookies();
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(result, null, 2),
        },
      ],
    };
  }
);

// 4. 获取首页推荐
server.tool(
  'list_feeds',
  '获取小红书首页推荐列表',
  {},
  async () => {
    const result = await listFeeds();
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(result, null, 2),
        },
      ],
    };
  }
);

// 5. 搜索笔记
server.tool(
  'search_feeds',
  '搜索小红书内容',
  {
    keyword: z.string().describe('搜索关键词'),
    filters: z.object({
      sort_by: z.enum(['综合', '最新', '最多点赞', '最多评论', '最多收藏']).optional().default('综合'),
      note_type: z.enum(['不限', '视频', '图文']).optional().default('不限'),
      publish_time: z.enum(['不限', '一天内', '一周内', '半年内']).optional().default('不限'),
      search_scope: z.enum(['不限', '已看过', '未看过', '已关注']).optional().default('不限'),
      location: z.enum(['不限', '同城', '附近']).optional().default('不限'),
    }).optional().describe('筛选选项'),
  },
  async ({ keyword, filters }) => {
    const result = await searchFeeds(keyword, filters || {});
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(result, null, 2),
        },
      ],
    };
  }
);

// ========== 启动 HTTP 服务器（使用 SSE）==========

async function startServer() {
  const app = express();

  // 创建 SSE Transport
  const transport = new SSEServerTransport('/message', {});

  // 连接 MCP Server 到 transport
  await server.connect(transport);

  // SSE 端点
  app.get('/sse', async (req, res) => {
    console.error('New SSE connection');
    transport.start(res);
  });

  // 消息端点
  app.post('/message', express.json(), async (req, res) => {
    console.error('Received message:', req.body);
    await transport.handlePostMessage(req, res, req.body);
  });

  // 健康检查端点
  app.get('/health', (req, res) => {
    res.json({
      status: 'ok',
      service: 'xhs-mcp-server',
      version: '1.0.0',
    });
  });

  // 根路径
  app.get('/', (req, res) => {
    res.json({
      name: 'xhs-mcp-service',
      version: '1.0.0',
      description: 'XiaoHongShu MCP Service (SSE)',
      endpoints: {
        sse: '/sse',
        message: '/message',
      },
      tools: 13,
    });
  });

  // 启动服务器
  app.listen(PORT, HOST, () => {
    console.error('='.repeat(60));
    console.error('  XHS MCP Service Started (SSE Mode)');
    console.error('='.repeat(60));
    console.error(`  Address: http://${HOST}:${PORT}`);
    console.error(`  SSE:     http://localhost:${PORT}/sse`);
    console.error(`  Message: http://localhost:${PORT}/message`);
    console.error(`  Health:  http://localhost:${PORT}/health`);
    console.error('='.repeat(60));
  });

  // 优雅关闭
  process.on('SIGINT', async () => {
    console.error('\n正在关闭服务...');
    await closeBrowser();
    process.exit(0);
  });

  process.on('SIGTERM', async () => {
    console.error('\n正在关闭服务...');
    await closeBrowser();
    process.exit(0);
  });
}

// 启动服务
startServer().catch((error) => {
  console.error('启动服务失败:', error);
  process.exit(1);
});
