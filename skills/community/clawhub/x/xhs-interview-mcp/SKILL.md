---
name: xiaohongshu-mcp-skill
description: 操作小红书（搜索笔记、获取面经、查看热门内容）。当用户想搜索小红书面经、查找面试经验、了解某公司/岗位的面试情况时使用。基于本地 MCP 服务（localhost:18060）。
---

# 小红书 MCP 服务

通过本地 MCP 服务操作小红书，搜索真实面经和面试经验。

## 前置要求

- MCP 服务已启动：`~/xiaohongshu-mcp/bin/`
- 服务地址：`http://localhost:18060/mcp`

## 工具列表

| 工具 | 说明 |
|------|------|
| `check_login_status` | 检查登录状态 |
| `search_feeds` | 搜索内容（搜索面经用 keyword="产品经理面试"） |
| `get_feed_detail` | 获取笔记详情 |
| `list_feeds` | 首页推荐 |

## 搜索面经

当用户需要搜索面试经验时：

```bash
mcporter call xiaohongshu search_feeds keyword="产品经理面试"
```

结合目标公司/岗位搜索：
- `字节跳动 产品经理 面试`
- `腾讯 产品 实习 面经`
- `阿里 产品经理 实习 面经`

## 获取笔记详情

拿到笔记 ID 后获取完整内容：

```bash
mcporter call xiaohongshu get_feed_detail note_id="笔记ID" xsecToken="token"
```

## 面经提取

搜索结果返回字段：
- `displayTitle` — 标题
- `nickname` — 作者
- `likedCount` — 点赞数（越多越真实）
- `commentCount` — 评论数
- `collectedCount` — 收藏数

**筛选高质量面经：** 点赞>500 或 评论>20 的笔记更可能有真实细节。
