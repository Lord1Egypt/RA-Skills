# 小红书 MCP 客户端
[English](./README.md) | 简体中文

一个用于小红书 MCP (Model Context Protocol) REST API 的 Python 客户端，提供全面的命令行界面，用于管理小红书账号和与平台交互。

## 功能特性

- **账号管理**
  - 添加、删除、列出和切换多个账号
  - 导入和导出 cookies
  - 跟踪最后使用时间和账号备注
  - **自动用户名检测** - 当未提供用户名时，自动检测当前登录的昵称
  - **当前账号管理** - 轻松检查和切换账号

- **登录管理**
  - 检查登录状态
  - 获取登录二维码
  - 登出（清除 cookies）

- **内容发布**
  - 发布带图片和标签的图文内容
  - 发布视频内容
  - 支持可见性设置

- **Feed 管理**
  - 列出推荐的 feeds
  - 按关键词搜索 feeds
  - 获取 feed 详细信息

- **互动功能**
  - 发表评论
  - 回复评论

- **用户信息**
  - 获取当前用户资料
  - 获取其他用户资料

## 安装

### 前置条件
- Python 3.12+
- 运行中的小红书 MCP 服务器（默认：`http://localhost:18060`）

### 从源码安装
```bash
cd xiaohongshu-aio
uv sync
uv run xhs --help
```

### 从 PyPI 安装（推荐）
```bash
uv tool install xiaohongshu-aio
```

### 安装并启动 MCP 服务器
1. 下载 MCP 服务器：`xhs mcp download`
2. 启动 MCP 服务器：`xhs mcp start`
3. 检查状态：`xhs mcp status`

## 使用方法

### 命令结构
```bash
xhs <命令> [选项]
```

### 账号管理
```bash
# 列出所有账号
xhs account list

# 添加新账号（自动从当前登录检测用户名）
xhs account add

# 添加带自定义用户名和备注的新账号
xhs account add --username 我的账号 --notes "我的个人账号"

# 删除账号
xhs account remove --username 我的账号

# 切换到另一个账号
xhs account switch --username 我的账号

# 导入账号的 cookies（自动检测用户名）
xhs account import

# 导入带自定义用户名的 cookies
xhs account import --username 我的账号

# 获取当前账号
xhs account current
```

### 登录管理
```bash
# 检查登录状态
xhs login status

# 使用自定义服务器 URL 检查登录状态
xhs login status --base-url http://localhost:18060

# 获取登录二维码
xhs login qrcode

# 登出
xhs login logout
```

### 发布内容
```bash
# 发布图文内容
xhs publish "标题" "内容" "https://example.com/image1.jpg" "https://example.com/image2.jpg" --tags 美食,旅行

# 发布视频内容
xhs publish "视频标题" "视频内容" "C:\path\to\video.mp4" --is-video

# 使用自定义服务器 URL 发布
xhs publish "标题" "内容" "https://example.com/image.jpg" --base-url http://localhost:18060
```

### Feed 管理
```bash
# 列出 feeds
xhs feed list

# 搜索 feeds
xhs feed search --keyword "咖啡"

# 获取 feed 详情
xhs feed detail --feed-id "feed123" --xsec-token "token123"

# 使用自定义服务器 URL
xhs feed list --base-url http://localhost:18060
```

### 互动操作
```bash
# 发表评论
xhs interact comment "feed123" "token123" --content "很棒的帖子！"

# 回复评论
xhs interact reply "feed123" "token123" --comment-id "comment_id" --content "回复内容"

# 使用自定义服务器 URL
xhs interact comment "feed123" "token123" --content "很棒的帖子！" --base-url http://localhost:18060
```

### 用户信息
```bash
# 获取当前用户资料
xhs user me

# 获取其他用户资料
xhs user profile --user-id "user123" --xsec-token "token123"

# 使用自定义服务器 URL
xhs user me --base-url http://localhost:18060
```

### MCP 服务器管理
```bash
# 下载 MCP 服务器
xhs mcp download

# 测试 MCP 连接
xhs mcp test

# 启动 MCP 服务器
xhs mcp start

# 停止 MCP 服务器
xhs mcp stop

# 重启 MCP 服务器
xhs mcp restart

# 检查 MCP 服务器状态
xhs mcp status
```

## 配置

你可以使用环境变量配置客户端：

| 环境变量 | 默认值 | 描述 |
|---------|--------|------|
| `XHS_MCP_BASE_URL` | `http://localhost:18060` | MCP 服务器基础 URL（优先） |
| `XHS_BASE_URL` | `http://localhost:18060` | MCP 服务器基础 URL（备用） |
| `XHS_TIMEOUT` | `60` | HTTP 请求超时时间（秒） |
| `XHS_VERIFY_SSL` | `true` | 是否验证 SSL 证书 |

## 项目结构

```
xiaohongshu-aio/
├── src/
│   └── xiaohongshu_aio/
│       ├── __init__.py          # 包初始化
│       ├── client.py            # REST API 客户端
│       ├── account.py           # 账号管理
│       ├── cli.py               # 命令行界面
│       └── mcp_service.py       # MCP 服务器管理
├── pyproject.toml               # 项目配置
├── README.md                    # 本文档
└── user_cookies.json            # 账号 cookies 存储
```

## 依赖

- `httpx` - 现代 HTTP 客户端
- `typer` - 命令行界面
- `pydantic` - 数据验证
- `pydantic-settings` - 设置管理
- `rich` - 富文本控制台输出

## 感谢

本项目基于 [xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) 项目开发，感谢原项目作者的贡献。

## 许可证

MIT
