#!/usr/bin/env node
/**
 * XHS MCP Server - 修复版
 * 使用标准 SSE 传输代替 Streamable HTTP
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

const PORT = process.env.XHS_PORT || 18060;
const HOST = process.env.XHS_HOST || '0.0.0.0';

const server = new McpServer({
  name: 'xhs-mcp-service',
  version: '1.0.0',
});

// ========== 注册工具（保持不变）==========

server.tool('check_login_status', '检查小红书登录状态', {}, async () => {
  const result = await checkLoginStatus();
  return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
});

server.tool('get_login_qrcode', '获取登录二维码', {}, async () => {
  const result = await getLoginQRCode();
  return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
});

server.tool('delete_cookies', '删除登录状态', {}, async () => {
  const result = await deleteCookies();
  return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
});

server.tool('list_feeds', '获取首页推荐', {}, async () => {
  const result = await listFeeds();
  return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
});

server.tool(
  'search_feeds',
  '搜索笔记',
  {
    keyword: z.string().describe('搜索关键词'),
    filters: z
      .object({
        sort_by: z.enum(['综合', '最新', '最多点赞', '最多评论', '最多收藏']).optional(),
        note_type: z.enum(['不限', '视频', '图文']).optional(),
        publish_time: z.enum(['不限', '一天内', '一周内', '半年内']).optional(),
        search_scope: z.enum(['不限', '已看过', '未看过', '已关注']).optional(),
        location: z.enum(['不限', '同城', '附近']).optional(),
      })
      .optional(),
  },
  async ({ keyword, filters }) => {
    const result = await searchFeeds(keyword, filters || {});
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  }
);

server.tool(
  'get_feed_detail',
  '获取笔记详情',
  {
    feed_id: z.string().describe('笔记ID'),
    xsec_token: z.string().describe('安全令牌'),
    load_all_comments: z.boolean().optional().default(false),
    limit: z.number().optional().default(20),
    click_more_replies: z.boolean().optional().default(false),
  },
  async ({ feed_id, xsec_token, load_all_comments, limit, click_more_replies }) => {
    const result = await getFeedDetail(feed_id, xsec_token, {
      loadAllComments: load_all_comments,
      limit,
      clickMoreReplies: click_more_replies,
    });
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  }
);

server.tool(
  'like_feed',
  '点赞/取消点赞',
  {
    feed_id: z.string().describe('笔记ID'),
    xsec_token: z.string().describe('安全令牌'),
    unlike: z.boolean().optional().default(false),
  },
  async ({ feed_id, xsec_token, unlike }) => {
    const result = await likeFeed(feed_id, xsec_token, unlike);
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  }
);

server.tool(
  'favorite_feed',
  '收藏/取消收藏',
  {
    feed_id: z.string().describe('笔记ID'),
    xsec_token: z.string().describe('安全令牌'),
    unfavorite: z.boolean().optional().default(false),
  },
  async ({ feed_id, xsec_token, unfavorite }) => {
    const result = await favoriteFeed(feed_id, xsec_token, unfavorite);
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  }
);

server.tool(
  'post_comment_to_feed',
  '发表评论',
  {
    feed_id: z.string().describe('笔记ID'),
    xsec_token: z.string().describe('安全令牌'),
    content: z.string().describe('评论内容'),
  },
  async ({ feed_id, xsec_token, content }) => {
    const result = await postComment(feed_id, xsec_token, content);
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  }
);

server.tool(
  'reply_comment_in_feed',
  '回复评论',
  {
    feed_id: z.string().describe('笔记ID'),
    xsec_token: z.string().describe('安全令牌'),
    content: z.string().describe('回复内容'),
    comment_id: z.string().optional(),
    user_id: z.string().optional(),
  },
  async ({ feed_id, xsec_token, content, comment_id, user_id }) => {
    const result = await replyComment(feed_id, xsec_token, content, comment_id, user_id);
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  }
);

server.tool(
  'user_profile',
  '获取用户主页',
  {
    user_id: z.string().describe('用户ID'),
    xsec_token: z.string().describe('安全令牌'),
  },
  async ({ user_id, xsec_token }) => {
    const result = await userProfile(user_id, xsec_token);
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  }
);

server.tool(
  'publish_content',
  '发布图文',
  {
    title: z.string().max(20).describe('标题'),
    content: z.string().max(1000).describe('正文'),
    images: z.array(z.string()).min(1).describe('图片路径'),
    tags: z.array(z.string()).optional(),
    is_original: z.boolean().optional().default(false),
    visibility: z.enum(['公开可见', '仅自己可见', '仅互关好友可见']).optional().default('公开可见'),
    schedule_at: z.string().optional(),
    products: z.array(z.string()).optional(),
  },
  async ({ title, content, images, tags, is_original, visibility, schedule_at, products }) => {
    const result = await publishContent({
      title,
      content,
      images,
      tags,
      isOriginal: is_original,
      visibility,
      scheduleAt: schedule_at,
    });
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  }
);

server.tool(
  'publish_with_video',
  '发布视频',
  {
    title: z.string().max(20).describe('标题'),
    content: z.string().max(1000).describe('正文'),
    video: z.string().describe('视频路径'),
    tags: z.array(z.string()).optional(),
    visibility: z.enum(['公开可见', '仅自己可见', '仅互关好友可见']).optional().default('公开可见'),
    schedule_at: z.string().optional(),
    products: z.array(z.string()).optional(),
  },
  async ({ title, content, video, tags, visibility, schedule_at, products }) => {
    const result = await publishWithVideo({
      title,
      content,
      video,
      tags,
      visibility,
      scheduleAt: schedule_at,
    });
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  }
);

// ========== 启动服务器（使用SSE传输）==========

async function startServer() {
  const app = express();

  // 存储活跃的SSE传输
  const transports = new Map();

  // SSE连接端点
  app.get('/sse', async (req, res) => {
    console.error('New SSE connection');
    const transport = new SSEServerTransport('/message', {});
    transports.set(transport.sessionId, transport);

    res.on('close', () => {
      transports.delete(transport.sessionId);
      console.error('SSE connection closed');
    });

    await server.connect(transport);
    transport.start(res);
  });

  // 消息端点
  app.post('/message', express.json(), async (req, res) => {
    const sessionId = req.query.sessionId;
    const transport = transports.get(sessionId);

    if (!transport) {
      res.status(400).json({ error: 'Invalid session' });
      return;
    }

    await transport.handlePostMessage(req, res, req.body);
  });

  // 健康检查
  app.get('/health', (req, res) => {
    res.json({ status: 'ok', service: 'xhs-mcp-server', version: '1.0.0-sse' });
  });

  app.get('/', (req, res) => {
    res.json({
      name: 'xhs-mcp-service',
      version: '1.0.0-sse',
      description: 'XiaoHongShu MCP Service (SSE Mode)',
      endpoints: { sse: '/sse', message: '/message' },
      tools: 13,
    });
  });

  app.listen(PORT, HOST, () => {
    console.error('='.repeat(60));
    console.error('  XHS MCP Service Started (SSE Mode)');
    console.error('='.repeat(60));
    console.error(`  SSE:     http://localhost:${PORT}/sse`);
    console.error(`  Message: http://localhost:${PORT}/message`);
    console.error(`  Health:  http://localhost:${PORT}/health`);
    console.error('='.repeat(60));
  });

  process.on('SIGINT', async () => {
    console.error('\n正在关闭服务...');
    await closeBrowser();
    process.exit(0);
  });
}

startServer().catch((error) => {
  console.error('启动服务失败:', error);
  process.exit(1);
});
