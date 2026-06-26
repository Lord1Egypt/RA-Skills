# 小红书 MCP 服务 - 完整使用说明

## 📋 目录

1. [服务概述](#服务概述)
2. [快速开始](#快速开始)
3. [功能列表](#功能列表)
4. [使用方式](#使用方式)
5. [API文档](#api文档)
6. [常见问题](#常见问题)
7. [最佳实践](#最佳实践)

---

## 🎯 服务概述

小红书MCP服务是一个基于Model Context Protocol (MCP) 的自动化工具，提供完整的小红书操作能力。

### 技术架构

- **协议**: MCP v2024-11-05
- **传输**: Streamable HTTP + SSE
- **自动化**: Puppeteer v24.39.1
- **框架**: Express.js v4.18.2

### 核心特性

✅ 13个完整功能工具
✅ 支持图文/视频发布
✅ 完整的互动操作（点赞、收藏、评论）
✅ 登录状态管理
✅ Cookies持久化
✅ 错误处理和重试机制

---

## 🚀 快速开始

### 1. 安装和启动

```bash
# 进入项目目录
cd D:\work\xiaohongshu\xhs-mcp-service

# 安装依赖（首次使用）
npm install

# 首次登录（扫码登录）
npm run login

# 启动MCP服务
npm start
```

### 2. 验证服务

```bash
# 健康检查
curl http://localhost:18060/health
# 返回: {"status":"ok","service":"xhs-mcp-server","version":"1.0.0"}

# 检查登录状态
node -e "import('./src/xhs-tools.js').then(m => m.checkLoginStatus()).then(console.log)"
```

### 3. 基础使用

```javascript
// 方式1: 直接调用工具函数
import { listFeeds, searchFeeds } from './src/xhs-tools.js';

// 获取首页推荐
const feeds = await listFeeds();
console.log(feeds);

// 搜索笔记
const results = await searchFeeds('美食');
console.log(results);
```

---

## 🛠️ 功能列表

### 13个完整工具

| # | 工具名称 | 功能说明 | 参数 |
|---|---------|---------|------|
| 1 | `check_login_status` | 检查登录状态 | 无 |
| 2 | `get_login_qrcode` | 获取登录二维码 | 无 |
| 3 | `delete_cookies` | 删除登录状态 | 无 |
| 4 | `list_feeds` | 获取首页推荐 | 无 |
| 5 | `search_feeds` | 搜索笔记 | `keyword`, `filters?` |
| 6 | `get_feed_detail` | 获取笔记详情 | `feed_id`, `xsec_token` |
| 7 | `like_feed` | 点赞/取消点赞 | `feed_id`, `xsec_token`, `unlike?` |
| 8 | `favorite_feed` | 收藏/取消收藏 | `feed_id`, `xsec_token`, `unfavorite?` |
| 9 | `post_comment_to_feed` | 发表评论 | `feed_id`, `xsec_token`, `content` |
| 10 | `reply_comment_in_feed` | 回复评论 | `feed_id`, `xsec_token`, `content`, `comment_id?` |
| 11 | `user_profile` | 获取用户主页 | `user_id`, `xsec_token` |
| 12 | `publish_content` | 发布图文 | `title`, `content`, `images`, `tags?` |
| 13 | `publish_with_video` | 发布视频 | `title`, `content`, `video`, `tags?` |

---

## 💻 使用方式

### 方式1: Node.js 直接调用（推荐）

**最稳定、最直接的方式**

```javascript
// 创建脚本 test-xhs.js
import {
  checkLoginStatus,
  listFeeds,
  searchFeeds,
  likeFeed,
  publishContent
} from './src/xhs-tools.js';

// 1. 检查登录
const loginStatus = await checkLoginStatus();
console.log('登录状态:', loginStatus);

// 2. 获取首页推荐
const feeds = await listFeeds();
console.log(`获取到 ${feeds.feeds.length} 条推荐`);

// 3. 搜索笔记
const results = await searchFeeds('咖啡', {
  sort_by: '最新',
  note_type: '图文'
});
console.log(`搜索到 ${results.feeds.length} 条结果`);

// 4. 点赞笔记
if (results.feeds[0]) {
  const feed = results.feeds[0];
  await likeFeed(feed.id, feed.xsec_token);
  console.log('点赞成功');
}

// 5. 发布图文
await publishContent({
  title: '我的第一篇笔记',
  content: '这是正文内容，最多1000字',
  images: ['./photo1.jpg', './photo2.jpg'],
  tags: ['美食', '探店'],
  visibility: '公开可见'
});
```

运行：
```bash
node test-xhs.js
```

### 方式2: 通过 MCP Inspector 测试

**适合调试和探索**

```bash
# 安装并启动MCP Inspector
npx @modelcontextprotocol/inspector

# 在浏览器中打开显示的地址
# 连接到: http://localhost:18060/mcp

# 在Inspector中可以：
# - 查看所有工具
# - 测试工具调用
# - 查看请求/响应
```

### 方式3: 集成到 Claude Desktop/Code

**AI助手直接操作小红书**

```bash
# 添加MCP服务到Claude
claude mcp add --transport http xhs-mcp http://localhost:18060/mcp

# 在Claude中使用
# "帮我搜索小红书上关于咖啡的笔记"
# "帮我点赞搜索结果的前3条"
# "帮我发布一篇图文笔记"
```

### 方式4: 通过命令行快速操作

**单次操作**

```bash
# 检查登录状态
node -e "import('./src/xhs-tools.js').then(m => m.checkLoginStatus()).then(console.log)"

# 搜索笔记
node -e "import('./src/xhs-tools.js').then(m => m.searchFeeds('美食')).then(r => console.log(r.feeds.length))"

# 获取首页推荐
node -e "import('./src/xhs-tools.js').then(m => m.listFeeds()).then(r => console.log(r.feeds.slice(0, 3)))"
```

---

## 📖 API文档

### 1. 登录管理

#### check_login_status()
检查当前登录状态

```javascript
const result = await checkLoginStatus();
// 返回: { success: true, logged_in: true, message: "已登录" }
```

#### get_login_qrcode()
获取登录二维码

```javascript
const result = await getLoginQRCode();
// 返回: { success: true, qrCode: "base64图片数据", expiresIn: 300 }
```

#### delete_cookies()
删除登录状态

```javascript
const result = await deleteCookies();
// 返回: { success: true, message: "Cookies已删除" }
```

### 2. 内容获取

#### list_feeds()
获取首页推荐

```javascript
const result = await listFeeds();
// 返回: {
//   success: true,
//   feeds: [
//     {
//       id: "笔记ID",
//       xsec_token: "安全令牌",
//       title: "标题",
//       author: "作者",
//       like_count: "点赞数",
//       cover: "封面图URL"
//     },
//     ...
//   ]
// }
```

#### search_feeds(keyword, filters?)
搜索笔记

```javascript
const result = await searchFeeds('咖啡', {
  sort_by: '最新',          // 综合 | 最新 | 最多点赞 | 最多评论 | 最多收藏
  note_type: '图文',        // 不限 | 视频 | 图文
  publish_time: '一周内',   // 不限 | 一天内 | 一周内 | 半年内
  search_scope: '不限',     // 不限 | 已看过 | 未看过 | 已关注
  location: '不限'          // 不限 | 同城 | 附近
});
// 返回格式同 list_feeds
```

#### get_feed_detail(feed_id, xsec_token, options?)
获取笔记详情

```javascript
const result = await getFeedDetail('笔记ID', 'xsec_token', {
  loadAllComments: false,      // 是否加载全部评论
  limit: 20,                    // 限制评论数量
  clickMoreReplies: false       // 是否展开二级回复
});
// 返回: {
//   success: true,
//   title: "标题",
//   content: "正文",
//   images: ["图片URL"],
//   author: { name: "作者名", id: "作者ID" },
//   comments: [...]
// }
```

### 3. 互动操作

#### like_feed(feed_id, xsec_token, unlike?)
点赞/取消点赞

```javascript
// 点赞
await likeFeed('笔记ID', 'xsec_token', false);

// 取消点赞
await likeFeed('笔记ID', 'xsec_token', true);
```

#### favorite_feed(feed_id, xsec_token, unfavorite?)
收藏/取消收藏

```javascript
// 收藏
await favoriteFeed('笔记ID', 'xsec_token', false);

// 取消收藏
await favoriteFeed('笔记ID', 'xsec_token', true);
```

#### post_comment_to_feed(feed_id, xsec_token, content)
发表评论

```javascript
await postComment('笔记ID', 'xsec_token', '评论内容');
```

#### reply_comment_in_feed(feed_id, xsec_token, content, comment_id?, user_id?)
回复评论

```javascript
await replyComment('笔记ID', 'xsec_token', '回复内容', '评论ID', '用户ID');
```

### 4. 用户信息

#### user_profile(user_id, xsec_token)
获取用户主页信息

```javascript
const result = await userProfile('用户ID', 'xsec_token');
// 返回: {
//   success: true,
//   user: {
//     nickname: "昵称",
//     desc: "简介",
//     fansCount: "粉丝数",
//     followsCount: "关注数"
//   },
//   notes: [...]  // 用户发布的笔记
// }
```

### 5. 内容发布

#### publish_content(options)
发布图文

```javascript
const result = await publishContent({
  title: '标题（最多20字）',
  content: '正文内容（最多1000字）',
  images: [
    './photo1.jpg',           // 本地路径
    'https://example.com/img.jpg'  // 或URL
  ],
  tags: ['标签1', '标签2'],
  isOriginal: false,          // 是否声明原创
  visibility: '公开可见',     // 公开可见 | 仅自己可见 | 仅互关好友可见
  scheduleAt: '2026-03-16T10:00:00Z'  // 定时发布（可选）
});
```

#### publish_with_video(options)
发布视频

```javascript
const result = await publishWithVideo({
  title: '标题（最多20字）',
  content: '正文内容（最多1000字）',
  video: './video.mp4',       // 本地视频路径
  tags: ['标签1', '标签2'],
  visibility: '公开可见'
});
```

---

## ❓ 常见问题

### Q1: 服务启动后无法访问？

**A**: 检查以下几点：
1. 确认端口18060未被占用
2. 检查防火墙设置
3. 查看控制台是否有错误信息

```bash
# 检查端口占用
netstat -ano | findstr :18060

# 如果被占用，修改端口
set XHS_PORT=18061
npm start
```

### Q2: 提示未登录？

**A**: 重新登录：
```bash
npm run login
# 扫描二维码登录
```

### Q3: 操作很慢（4-14秒）？

**A**: 这是正常现象，因为：
- Puppeteer需要启动浏览器
- 页面加载和渲染需要时间
- 网络请求延迟

优化建议：
- 复用浏览器实例（服务已实现）
- 批量操作时增加延迟
- 使用代理加速（如需要）

### Q4: Cookies过期怎么办？

**A**: 定期重新登录：
```bash
# 删除旧cookies
npm run login
```

建议：每周重新登录一次

### Q5: 如何避免被风控？

**A**: 遵循最佳实践：
- 操作间隔 > 2秒
- 每天发布 < 50篇
- 避免频繁点赞/收藏
- 使用正常的浏览行为

### Q6: MCPorter调用失败？

**A**: MCPorter在Windows下有SSE连接问题，建议：
- 使用Node.js直接调用
- 使用MCP Inspector
- 集成到Claude Desktop

### Q7: 发布笔记失败？

**A**: 检查：
1. 图片/视频是否存在
2. 标题是否超过20字
3. 正文是否超过1000字
4. 是否已登录
5. 是否达到发布限制（50篇/天）

---

## 🎯 最佳实践

### 1. 性能优化

```javascript
// ❌ 不好的做法 - 每次都新建实例
for (const keyword of keywords) {
  await searchFeeds(keyword);
}

// ✅ 好的做法 - 批量操作，增加延迟
for (const keyword of keywords) {
  await searchFeeds(keyword);
  await new Promise(r => setTimeout(r, 3000)); // 3秒延迟
}
```

### 2. 错误处理

```javascript
// ✅ 完善的错误处理
try {
  const result = await searchFeeds('美食');

  if (!result.success) {
    console.error('搜索失败:', result.message);
    return;
  }

  if (result.feeds.length === 0) {
    console.log('无搜索结果');
    return;
  }

  // 处理结果
  console.log(`找到 ${result.feeds.length} 条结果`);

} catch (error) {
  console.error('操作出错:', error.message);
  console.error('堆栈:', error.stack);
}
```

### 3. 登录状态管理

```javascript
// ✅ 定期检查登录状态
async function ensureLoggedIn() {
  const status = await checkLoginStatus();

  if (!status.logged_in) {
    console.log('未登录，请先登录');
    process.exit(1);
  }

  return true;
}

// 在每次操作前检查
await ensureLoggedIn();
await searchFeeds('美食');
```

### 4. 批量操作示例

```javascript
// ✅ 批量搜索和互动
const keywords = ['咖啡', '美食', '旅行'];

for (const keyword of keywords) {
  console.log(`\n搜索: ${keyword}`);

  const results = await searchFeeds(keyword, {
    sort_by: '最新',
    note_type: '图文'
  });

  if (results.success && results.feeds.length > 0) {
    // 点赞前3条
    for (let i = 0; i < Math.min(3, results.feeds.length); i++) {
      const feed = results.feeds[i];
      console.log(`  点赞: ${feed.title}`);

      await likeFeed(feed.id, feed.xsec_token);
      await new Promise(r => setTimeout(r, 2000));
    }
  }

  // 关键词间隔
  await new Promise(r => setTimeout(r, 5000));
}
```

### 5. 定时任务

```bash
# 使用cron定时发布
# 每天上午10点发布
0 10 * * * cd /path/to/xhs-mcp-service && node publish-daily.js
```

```javascript
// publish-daily.js
import { publishContent } from './src/xhs-tools.js';

await publishContent({
  title: '早安打卡',
  content: '今天的早安打卡...',
  images: ['./daily-photo.jpg'],
  tags: ['早安', '打卡'],
  visibility: '公开可见'
});
```

### 6. 数据分析

```javascript
// ✅ 分析搜索结果
const results = await searchFeeds('咖啡');

const analysis = {
  total: results.feeds.length,
  avgLikes: 0,
  avgCollects: 0,
  topAuthors: {}
};

results.feeds.forEach(feed => {
  analysis.avgLikes += parseInt(feed.like_count) || 0;
  analysis.avgCollects += parseInt(feed.collect_count) || 0;

  const author = feed.author;
  analysis.topAuthors[author] = (analysis.topAuthors[author] || 0) + 1;
});

analysis.avgLikes /= results.feeds.length;
analysis.avgCollects /= results.feeds.length;

console.log('数据分析:', analysis);
```

---

## 📊 性能指标

基于实际测试：

| 操作 | 平均耗时 | 备注 |
|------|---------|------|
| 检查登录状态 | 14秒 | 首次加载浏览器 |
| 获取首页推荐 | 10.5秒 | 35条数据 |
| 搜索笔记 | 5.6秒 | 22条结果 |
| 获取笔记详情 | 5.7秒 | 包含评论 |
| 点赞/取消点赞 | 4.5-6秒 | - |
| 收藏/取消收藏 | 4.2-4.8秒 | - |

---

## 🔧 配置选项

### 环境变量

```bash
# 服务端口（默认18060）
export XHS_PORT=18060

# 绑定地址（默认0.0.0.0）
export XHS_HOST=0.0.0.0

# 代理设置（可选）
export XHS_PROXY=http://proxy:port
```

### 文件结构

```
xhs-mcp-service/
├── src/
│   ├── index.js          # MCP服务入口
│   ├── xhs-tools.js      # 工具实现
│   ├── browser.js        # 浏览器管理
│   └── login.js          # 登录工具
├── data/
│   └── cookies.json      # Cookies存储
├── package.json
└── README.md
```

---

## 📞 支持

- **GitHub**: https://github.com/xpzouying/xiaohongshu-mcp
- **MCP协议**: https://modelcontextprotocol.io/
- **问题反馈**: 提交GitHub Issue

---

## 📄 许可证

MIT License

---

## 🎉 总结

小红书MCP服务提供：

✅ **13个完整功能** - 覆盖所有常用操作
✅ **多种使用方式** - Node.js、MCP Inspector、Claude集成
✅ **稳定可靠** - 完善的错误处理和重试机制
✅ **易于使用** - 简单的API设计
✅ **生产就绪** - 经过全面测试

开始使用吧！🚀
