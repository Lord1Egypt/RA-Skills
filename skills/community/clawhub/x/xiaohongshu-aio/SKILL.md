---
name: xiaohongshu-aio
description: |
  小红书MCP服务下载、启动、重启、检测，小红书多账号管理、登录、状态检查、内容发布、小红书笔记和视频发布、点赞评论操作和用户信息查询等需要调用本技能。当用户需要从小红书获取笔记和视频数据、用户数据、发布笔记或视频时需要调用本技能。
metadata:
  {
    "openclaw": {
      "requires": { "bins": ["python","uv"], "env": ["XHS_MCP_BASE_URL"], "config": [] },
      "primaryEnv": "XHS_MCP_BASE_URL",
      "emoji": "📱"
    }
  }
---

# 小红书All in One技能

## 功能概述

本技能提供完整的小红书账号管理和内容操作功能，基于小红书 MCP 服务器 API。

### 主要功能
- **账号管理**：添加、删除、列出、切换账号
- **登录管理**：检查登录状态、获取登录二维码、登出
- **内容发布**：发布图文和视频内容
- **Feed 管理**：列出推荐内容、搜索、获取详情
- **互动操作**：点赞、收藏、发表评论
- **用户信息**：获取当前用户和其他用户资料

## 安装

### 安装技能
#### 方案1：从源代码安装
1. 克隆本仓库到本地
2. 进入项目目录
3. 安装依赖

```bash
cd xiaohongshu-aio
uv sync
uv run xhs --help
```

#### 方案2：从 PyPI 安装(推荐)

1. 执行：`uv tool install xiaohongshu-aio`

### 安装启动 MCP 服务器
1. 执行：`xhs mcp download` 下载 MCP 服务器
2. 执行：`xhs mcp start` 启动 MCP 服务器
3. 执行：`xhs mcp status` 检查 MCP 服务器状态

## 执行流程

**执行任何操作前，都需要先检查 MCP 服务器是否运行**：
```bash
xhs mcp status
```

### 1. 账号管理流程

#### 添加账号
1. 执行：`xhs login status`确保 MCP 服务器已登录
2. 执行：`xhs account add`（自动检测用户名）
3. 或执行：`xhs account add --username 账号名称 --notes "备注"`
4. 系统会自动将当前 cookies 保存为指定账号

#### 切换账号
1. 执行：`xhs account switch --username 账号名称`
2. 系统会将指定账号的 cookies 写入 MCP 服务器的 cookies.json
3. 执行：`xhs login status` 确认切换成功

#### 查看账号
- 查看所有账号：`xhs account list`
- 查看当前账号：`xhs account current`

### 2. 登录管理流程

#### 检查登录状态
1. 执行：`xhs login status`
2. 系统返回当前登录状态和用户名

#### 扫码登录
1. 执行：`xhs login qrcode`
2. 系统返回登录二维码（Base64 格式）
3. 用户使用小红书 App 扫描二维码
4. 扫描后执行：`xhs login status` 确认登录成功

#### 登出
1. 执行：`xhs login logout`
2. 系统会清除当前登录状态

### 3. 内容发布流程

#### 发布图文内容
1. 执行：
   ```bash
   xhs publish "标题" "内容" "图片URL1" "图片URL2" --tags 标签1 标签2
   ```

#### 发布视频内容
1. 执行：
   ```bash
   xhs publish "视频标题" "视频内容" "视频文件路径" --is-video
   ```

### 4. 笔记管理流程

#### 搜索笔记
1. 执行：`xhs feed search --keyword "关键词"`
2. 系统返回相关内容列表

#### 获取笔记详情
1. 从搜索结果中获取 feed_id 和 xsec_token
2. 执行：
   ```bash
   xhs feed detail --feed-id "feed_id" --xsec-token "token"
   ```

### 5. 互动操作流程

#### 点赞笔记
1. 执行：`xhs interact like "feed_id" "token"`

#### 发表笔记评论
1. 执行：
   ```bash
   xhs interact comment "feed_id" "token" --content "评论内容"
   ```

## 命令参考

### 账号管理
- `xhs account list` - 列出所有账号
- `xhs account add [--username 用户名] [--notes 备注]` - 添加账号
- `xhs account remove --username 用户名` - 删除账号
- `xhs account switch --username 用户名` - 切换账号
- `xhs account import [--username 用户名]` - 导入 cookies
- `xhs account current` - 获取当前账号

### 登录管理
- `xhs login status [--base-url URL]` - 检查登录状态
- `xhs login qrcode [--base-url URL]` - 获取登录二维码
- `xhs login logout [--base-url URL]` - 登出

### 内容发布
- `xhs publish 标题 内容 媒体文件... [--tags 标签...] [--is-video] [--base-url URL]` - 发布笔记或视频内容

### 笔记管理
- `xhs feed list [--base-url URL]` - 列出推荐笔记
- `xhs feed search --keyword 关键词 [--base-url URL]` - 搜索笔记
- `xhs feed detail --feed-id ID --xsec-token 令牌 [--base-url URL]` - 获取笔记详情

### 互动操作
- `xhs interact like  feed_id 令牌 [--unlike] [--base-url URL]` - 点赞/取消点赞
- `xhs interact favorite feed_id 令牌 [--unfavorite] [--base-url URL]` - 收藏/取消收藏
- `xhs interact comment feed_id 令牌 --content 内容 [--base-url URL]` - 发表评论

### 用户信息
- `xhs user me [--base-url URL]` - 获取当前用户资料
- `xhs user profile --user-id ID --xsec-token 令牌 [--base-url URL]` - 获取其他用户资料

### MCP 服务器管理
- `xhs mcp download` - 下载 MCP 服务器
- `xhs mcp test` - 检查 MCP 服务器是否运行
- `xhs mcp start` - 启动 MCP 服务器
- `xhs mcp stop` - 停止 MCP 服务器
- `xhs mcp status` - 检查 MCP 服务器状态
- `xhs mcp restart` - 重启 MCP 服务器

### 其他命令
- `xhs --help` - 显示帮助信息
- 具体的命令参考可以使用 `xhs 命令名['user', 'feed', 'interact', 'mcp'] --help` 查看详细帮助



## 配置

### 环境变量
- `XHS_MCP_BASE_URL` - MCP 服务器地址（优先）
- `XHS_BASE_URL` - MCP 服务器地址（备用）
- `XHS_TIMEOUT` - HTTP 请求超时时间
- `XHS_VERIFY_SSL` - 是否验证 SSL 证书

### 配置文件
- 账号信息存储在 `user_cookies.json`
- cookies 存储在 MCP 服务器目录的 `cookies.json`

## 注意事项

1. **账号安全**：请妥善保管 `user_cookies.json` 文件
2. **频率限制**：避免过于频繁的操作，遵守平台规则
3. **服务器依赖**：本技能依赖运行中的小红书 MCP 服务器
4. **网络连接**：发布视频时需要稳定的网络连接
5. **错误处理**：遇到错误时检查 MCP 服务器状态

## 故障排除

### 常见问题

| 问题 | 解决方案 |
|------|----------|
| 无法连接服务器 | 检查 MCP 服务器是否运行，地址是否正确、重启 MCP 服务器 |
| 登录失败 | 确保二维码扫描及时，检查账号状态 |
| 发布失败 | 检查内容是否符合平台规范，文件是否可访问 |
| 账号切换失败 | 检查账号是否存在，重启 MCP 服务器 |

**失败时重启 MCP 服务器**：
```bash
xhs mcp restart
```

## 依赖

- Python 3.12+
- 运行中的小红书 MCP 服务器
- 依赖包：httpx, typer, pydantic, rich


## 完整发布流程

1. **检查登录状态**
   ```bash
   xhs login status
   ```

2. **如未登录，获取二维码**
   ```bash
   xhs login qrcode
   ```

3. **扫码登录后确认**
   ```bash
   xhs login status
   ```

4. **添加账号**
   ```bash
   xhs account add
   ```

5. **发布内容**
   ```bash
   xhs publish "我的第一篇笔记" "这是内容" "https://example.com/image.jpg" --tags 测试 小红书
   ```

6. **搜索相关内容**
   ```bash
   xhs feed search --keyword "咖啡"
   ```