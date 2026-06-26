# 小红书 MCP Skill

通过本地 MCP 服务操作小红书，搜索面经、获取笔记详情、查看热门内容。

---

## 功能

- 🔍 **搜索内容**：搜索笔记、热门话题、面经
- 📋 **获取详情**：获取笔记正文、图片、评论
- 👍 **互动操作**：点赞、收藏、评论
- 👤 **用户信息**：查看用户主页和笔记列表
- 📊 **登录状态**：检查当前账号登录状态

---

## 前置要求

### 1. 下载 MCP 服务

从 GitHub 下载对应平台的可执行文件：
- macOS ARM64: `xiaohongshu-mcp-darwin-arm64.tar.gz`
- macOS x64: `xiaohongshu-mcp-darwin-x64.tar.gz`
- Linux: `xiaohongshu-mcp-linux-amd64.tar.gz`

下载地址：https://github.com/example/xiaohongshu-mcp（项目地址）

### 2. 启动服务

```bash
cd ~/xiaohongshu-mcp/bin
# 首次登录
./xiaohongshu-login-darwin-arm64
# 启动 MCP 服务
nohup ./xiaohongshu-mcp-darwin-arm64 > ../mcp.log 2>&1 &
```

### 3. 配置 mcporter

```bash
mcporter config add xiaohongshu --type http --url http://localhost:18060/mcp
```

### 4. 检查登录状态

```bash
mcporter call xiaohongshu check_login_status
```

---

## 常用命令

### 搜索面经

```bash
# PM 相关面经
mcporter call xiaohongshu search_feeds keyword="产品经理面试"

# 指定公司+岗位
mcporter call xiaohongshu search_feeds keyword="腾讯广告 产品策划 面试"

# 带筛选条件
mcporter call xiaohongshu search_feeds keyword="字节跳动 商业化产品 实习" filters='{"sort":"by_time"}'
```

### 获取笔记详情（含图片）

```bash
mcporter call xiaohongshu get_feed_detail \
  feed_id="68bc3f17000000001d035c33" \
  xsec_token="AB_wL6p9ZA0PmODiLLL97TQ7vx9xvg6rVG655oG2Za6XA="
```

### 首页推荐

```bash
mcporter call xiaohongshu list_feeds
```

---

## 工具列表

| 工具 | 说明 |
|------|------|
| `check_login_status` | 检查小红书登录状态 |
| `search_feeds` | 搜索笔记内容 |
| `get_feed_detail` | 获取笔记详情（正文+图片+评论） |
| `list_feeds` | 首页推荐列表 |
| `user_profile` | 获取用户主页信息 |
| `like_feed` | 点赞笔记 |
| `favorite_feed` | 收藏笔记 |
| `post_comment_to_feed` | 评论笔记 |

---

## 图片内容读取

笔记中的面试题截图需要用 vision 模型识别：

```python
image(
  tool,
  prompt="请识别并提取这张图片中的所有文字内容，特别是面试题目和答案要点",
  model="minimax/MiniMax-VL-01"
)
```

---

## 注意事项

- MCP 服务必须从 `~/xiaohongshu-mcp/bin/` 目录启动，才能找到 cookies
- cookies 文件位置：`~/xiaohongshu-mcp/bin/cookies.json`
- 服务端口：`18060`

---

## 链接

- ClawHub: https://clawhub.ai/skills/xiaohongshu-mcp-skill
