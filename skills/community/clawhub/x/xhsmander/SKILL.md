---
name: xhsmander
description: |
  小红书自动化发布技能。通过 Docker 容器中的 xiaohongshu-mcp 服务，实现登录、发布图文、搜索、互动等操作。
  当用户提到发小红书、发笔记、发布内容、扫码登录小红书、小红书自动化、小红书发布时使用此技能。
---

# xhsmander - 小红书定制化发布技能（完整工作流）

通过 `xiaohongshu-mcp` (Docker) 提供完整的小红书自动化能力。

## 文件结构

```
xhsmander/
├── SKILL.md              # 本技能说明
├── docker-compose.yml    # Docker 启动配置
├── _meta.json            # 元数据
├── scripts/
│   ├── mcp_dispatcher.py  # MCP 调度器（核心）
│   ├── check_login.py    # 检查登录状态
│   ├── get_qrcode.py     # 获取登录二维码
│   ├── publish.py         # 发布图文（原始）
│   ├── search.py         # 搜索内容
│   ├── cli.py            # CLI 工具
│   ├── __init__.py
│   ├── check_status.py   # 检查登录状态（简化版）
│   ├── get_qr.py         # 获取二维码并保存（简化版）
│   └── publish_post.py    # 发布图文（直接运行版）
└── references/
    └── mcp_api.md        # MCP API 参考
```

## 快速部署

### 1. 启动 Docker 容器

```bash
cd skills/xhsmander
docker compose up -d
```

### 2. 检查服务状态

```bash
python scripts/check_status.py
```

输出 `Done` 即表示服务正常运行。

### 3. 首次登录（获取二维码）

```bash
python scripts/get_qr.py
```

二维码保存在 `scripts/qrcode.png`，发送给用户扫码登录。

### 4. 发布图文笔记

编辑 `scripts/publish_post.py` 中的 title、content、images 路径，然后运行：

```bash
python scripts/publish_post.py
```

## 核心脚本

### mcp_dispatcher.py
`MCP HTTP+JSON-RPC` 调度器，每次调用自动处理 initialize + session 管理。

### publish_post.py（直接运行版）
封装好的发布脚本，直接修改顶部变量即可发布：

```python
title = "笔记标题（≤20字）"
content = "笔记正文（≤1000字）"
images = ['/app/images/your_image.png']  # 容器内路径
tags = ["标签1", "标签2"]
```

**图片路径规则：**
- 图片必须放在 `scripts/images/` 目录
- 容器内路径为 `/app/images/xxx.png`
- 本机路径需映射到容器内路径

### check_status.py
简化版登录状态检查，运行后结果保存在 `scripts/login_status.json`。

### get_qr.py
简化版二维码获取，运行后：
- 二维码图片：`scripts/qrcode.png`
- 完整响应：`scripts/qrcode_result.json`

## 架构说明

```
本机(OpenClaw)  --HTTP+JSON-RPC-->  Docker容器(xiaohongshu-mcp)  --Chrome/ROD--> 小红书网页
```

**关键路径规则：**
- 本机路径（如图片）→ 容器无法直接访问
- 容器内路径 `/app/images/` → 本机 `scripts/images/` 目录（docker-compose 挂载）
- 发布图片时，images 参数传容器内路径 `/app/images/xxx.png`

## MCP API 工具列表

| 工具名 | 用途 | 关键参数 |
|---|---|---|
| `check_login_status` | 检查登录状态 | 无 |
| `get_login_qrcode` | 获取登录二维码 | 无 |
| `publish_content` | 发布图文 | title, content, images, tags |
| `search_feeds` | 搜索笔记 | keyword |
| `list_feeds` | 首页推荐 | 无 |
| `like_feed` | 点赞 | feed_id, xsec_token |
| `favorite_feed` | 收藏 | feed_id, xsec_token |
| `get_feed_detail` | 笔记详情 | feed_id, xsec_token |
| `user_profile` | 用户主页 | user_id, xsec_token |
| `post_comment_to_feed` | 评论 | feed_id, xsec_token, content |

## 限制与注意事项

1. **Session 不可复用**：每次 MCP 请求前必须先发 initialize 获取新 session ID
2. **图片路径**：必须是 `/app/images/xxx.png`（容器内路径），不是本机路径
3. **Cookie 有效期**：Cookie 存储在 Docker volume 中，重启容器需重新登录
4. **二维码时效**：有效期约5分钟，超时需重新获取
5. **发布限制**：每天发帖量建议≤50篇
6. **标题限制**：≤20字
7. **正文限制**：≤1000字

## Docker 环境信息

- 容器名：`xiaohongshu-mcp`
- 端口：18060
- 镜像：`xpzouying/xiaohongshu-mcp`
- 数据卷：`./data`（cookies）、`./images`（发布图片）
- 挂载配置：见 `docker-compose.yml`
