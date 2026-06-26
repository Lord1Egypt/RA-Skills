# zsxq-fetch

知识星球帖子抓取 — [OpenClaw](https://github.com/nicepkg/openclaw) Skill

自动抓取指定知识星球的最新帖子，支持通过帖子链接获取单条帖子详情，支持多星球配置。

## 功能特性

- 抓取指定星球的最新帖子（支持全部 / 仅精华）
- 通过帖子链接或 ID 获取单条帖子完整内容
- 支持多星球配置
- 内置限速与指数退避重试

## 安装

### 手动安装

```bash
# 克隆到 skills 目录
git clone https://github.com/chenmuwen0930-rgb/openclaw-skill-zsxq \
  ~/.openclaw/skills/zsxq-fetch

# 验证 Node.js 环境
bash ~/.openclaw/skills/zsxq-fetch/install.sh
```

## 配置

### 1. 设置 Token

获取方式：浏览器打开 [wx.zsxq.com](https://wx.zsxq.com) → 登录 → F12 → Application → Cookies → 复制 `zsxq_access_token` 的值。

将 Token 添加到 OpenClaw 环境变量（`~/.openclaw/.env`）：

```bash
ZSXQ_TOKEN=你的token值
```

### 2. 配置星球

编辑 `groups.json`：

```json
[
  {
    "group_id": "YOUR_GROUP_ID",
    "name": "你的星球名称",
    "scope": "digests",
    "max_topics": 20
  }
]
```

| 字段 | 说明 |
|------|------|
| `group_id` | 从星球 URL `wx.zsxq.com/group/{group_id}` 获取 |
| `name` | 星球名称（展示用） |
| `scope` | `digests`（仅精华）或 `all`（全部），推荐 `digests` |
| `max_topics` | 每个星球最多抓取帖子数 |

不确定 group_id？运行 `groups` 子命令查看已加入的星球：

```bash
ZSXQ_TOKEN=xxx node fetch_topics.js groups
```

## 使用

在 OpenClaw 中直接对话即可触发：

> 帮我看看知识星球最新有什么内容

## 子命令参考

`fetch_topics.js` 提供以下子命令，可独立使用：

```bash
# 获取帖子（scope: all | digests）
node fetch_topics.js topics <group_id> [count] [scope]

# 获取精华帖（快捷方式）
node fetch_topics.js digests <group_id> [count]

# 获取指定帖子详情（支持 ID 或完整链接）
node fetch_topics.js topic <group_id> <topic_id_or_url>

# 列出已加入的星球
node fetch_topics.js groups
```

## 依赖

- Node.js >= 18（无额外第三方依赖）

## License

[MIT](LICENSE)
