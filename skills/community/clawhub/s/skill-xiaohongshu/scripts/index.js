#!/usr/bin/env node
/**
 * XHS MCP Server - 小红书 MCP 服务
 * 使用 @modelcontextprotocol/sdk 实现标准 MCP 协议
 * 支持 Streamable HTTP 模式
 */

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js';
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

// ========== 注册 MCP 工具 ==========

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

// 6. 获取笔记详情
server.tool(
  'get_feed_detail',
  '获取帖子详情，包括互动数据和评论',
  {
    feed_id: z.string().describe('笔记 ID'),
    xsec_token: z.string().describe('安全令牌'),
    load_all_comments: z.boolean().optional().default(false).describe('是否加载全部评论'),
    limit: z.number().optional().default(20).describe('限制加载的一级评论数量'),
    click_more_replies: z.boolean().optional().default(false).describe('是否展开二级回复'),
  },
  async ({ feed_id, xsec_token, load_all_comments, limit, click_more_replies }) => {
    const result = await getFeedDetail(feed_id, xsec_token, {
      loadAllComments: load_all_comments,
      limit,
      clickMoreReplies: click_more_replies,
    });
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

// 7. 发表评论
server.tool(
  'post_comment_to_feed',
  '发表评论到小红书帖子',
  {
    feed_id: z.string().describe('笔记 ID'),
    xsec_token: z.string().describe('安全令牌'),
    content: z.string().describe('评论内容'),
  },
  async ({ feed_id, xsec_token, content }) => {
    const result = await postComment(feed_id, xsec_token, content);
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

// 8. 回复评论
server.tool(
  'reply_comment_in_feed',
  '回复笔记下的指定评论',
  {
    feed_id: z.string().describe('笔记 ID'),
    xsec_token: z.string().describe('安全令牌'),
    content: z.string().describe('回复内容'),
    comment_id: z.string().optional().describe('评论 ID'),
    user_id: z.string().optional().describe('用户 ID'),
  },
  async ({ feed_id, xsec_token, content, comment_id, user_id }) => {
    const result = await replyComment(feed_id, xsec_token, content, comment_id, user_id);
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

// 9. 点赞/取消点赞
server.tool(
  'like_feed',
  '为笔记点赞或取消点赞',
  {
    feed_id: z.string().describe('笔记 ID'),
    xsec_token: z.string().describe('安全令牌'),
    unlike: z.boolean().optional().default(false).describe('是否取消点赞'),
  },
  async ({ feed_id, xsec_token, unlike }) => {
    const result = await likeFeed(feed_id, xsec_token, unlike);
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

// 10. 收藏/取消收藏
server.tool(
  'favorite_feed',
  '收藏笔记或取消收藏',
  {
    feed_id: z.string().describe('笔记 ID'),
    xsec_token: z.string().describe('安全令牌'),
    unfavorite: z.boolean().optional().default(false).describe('是否取消收藏'),
  },
  async ({ feed_id, xsec_token, unfavorite }) => {
    const result = await favoriteFeed(feed_id, xsec_token, unfavorite);
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

// 11. 获取用户主页
server.tool(
  'user_profile',
  '获取用户个人主页信息',
  {
    user_id: z.string().describe('用户 ID'),
    xsec_token: z.string().describe('安全令牌'),
  },
  async ({ user_id, xsec_token }) => {
    const result = await userProfile(user_id, xsec_token);
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

// 12. 发布图文
server.tool(
  'publish_content',
  '发布图文内容到小红书',
  {
    title: z.string().max(20).describe('标题（最多20字）'),
    content: z.string().max(1000).describe('正文内容（最多1000字）'),
    images: z.array(z.string()).min(1).describe('图片路径列表（HTTP链接或本地绝对路径）'),
    tags: z.array(z.string()).optional().describe('话题标签列表'),
    is_original: z.boolean().optional().default(false).describe('是否声明原创'),
    visibility: z.enum(['公开可见', '仅自己可见', '仅互关好友可见']).optional().default('公开可见').describe('可见范围'),
    schedule_at: z.string().optional().describe('定时发布时间（ISO8601格式，1小时至14天内）'),
    products: z.array(z.string()).optional().describe('商品关键词列表'),
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

// 13. 发布视频
server.tool(
  'publish_with_video',
  '发布视频内容到小红书',
  {
    title: z.string().max(20).describe('标题（最多20字）'),
    content: z.string().max(1000).describe('正文内容（最多1000字）'),
    video: z.string().describe('本地视频文件绝对路径'),
    tags: z.array(z.string()).optional().describe('话题标签列表'),
    visibility: z.enum(['公开可见', '仅自己可见', '仅互关好友可见']).optional().default('公开可见').describe('可见范围'),
    schedule_at: z.string().optional().describe('定时发布时间（ISO8601格式）'),
    products: z.array(z.string()).optional().describe('商品关键词列表'),
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

// ========== 启动 HTTP 服务器 ==========

async function startServer() {
  const app = express();

  // 创建 Streamable HTTP Transport
  const transport = new StreamableHTTPServerTransport();

  // 连接 MCP Server 到 transport
  await server.connect(transport);

  // 处理所有 /mcp 路由的请求
  app.all('/mcp', async (req, res) => {
    console.error(`\n收到请求: ${req.method} ${req.url}`);
    console.error('Content-Type:', req.headers['content-type']);
    console.error('Accept:', req.headers.accept);

    try {
      await transport.handleRequest(req, res);
      console.error('✅ 请求处理成功');
    } catch (error) {
      console.error('❌ 处理 MCP 请求失败:', error);
      console.error('错误类型:', error.constructor.name);
      console.error('错误消息:', error.message);
      console.error('错误堆栈:', error.stack);

      if (!res.headersSent) {
        res.status(500).json({
          jsonrpc: '2.0',
          error: {
            code: -32603,
            message: error.message,
            data: error.stack,
          },
          id: null,
        });
      }
    }
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
      description: 'XiaoHongShu MCP Service',
      endpoint: '/mcp',
      tools: 13,
    });
  });

  // 启动服务器
  app.listen(PORT, HOST, () => {
    console.error('='.repeat(60));
    console.error('  XHS MCP Service Started');
    console.error('='.repeat(60));
    console.error(`  Address: http://${HOST}:${PORT}`);
    console.error(`  MCP:     http://localhost:${PORT}/mcp`);
    console.error(`  Health:  http://localhost:${PORT}/health`);
    console.error('='.repeat(60));
    console.error('');
    console.error('Usage:');
    console.error('  1. Test with MCP Inspector:');
    console.error(`     npx @modelcontextprotocol/inspector`);
    console.error(`     Connect to: http://localhost:${PORT}/mcp`);
    console.error('');
    console.error('  2. Add to Claude Code:');
    console.error(`     claude mcp add --transport http xhs-mcp http://localhost:${PORT}/mcp`);
    console.error('');
    console.error('Available Tools (13):');
    console.error('  - check_login_status');
    console.error('  - get_login_qrcode');
    console.error('  - delete_cookies');
    console.error('  - list_feeds');
    console.error('  - search_feeds');
    console.error('  - get_feed_detail');
    console.error('  - like_feed');
    console.error('  - favorite_feed');
    console.error('  - post_comment_to_feed');
    console.error('  - reply_comment_in_feed');
    console.error('  - user_profile');
    console.error('  - publish_content');
    console.error('  - publish_with_video');
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
