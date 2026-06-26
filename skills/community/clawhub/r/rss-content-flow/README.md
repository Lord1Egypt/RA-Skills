# RSS 内容流 (rss-content-flow)

将 RSS 订阅转化为多平台发布内容。自动抓取最新资讯，AI 分析核心观点，一键生成适配知乎/小红书/公众号的原创文案。

## 功能

- 📡 **RSS 订阅管理** — 添加/删除/列出订阅源
- 🔍 **智能抓取** — 自动获取最新文章，过滤广告和过期内容
- 🧠 **AI 分析** — 提取核心观点、关键数据、金句标签
- ✍️ **平台改写** — 生成知乎/小红书/公众号风格的原创内容
- 💾 **草稿保存** — 写入飞书文档或直接调用发布工具

## 使用方法

### 触发词
"帮我找今天的选题"、"RSS 订阅"、"监控 XX 更新"、"把 XX 改成小红书"、"我需要内容灵感"

### 快速开始

**1. 初始化订阅源**
```bash
python3 scripts/manage_feeds.py --init
```

**2. 查看今日内容选题**
```bash
python3 scripts/fetch_feed.py --all --limit 5
```

**3. 生成内容**
AI 根据选题列表，为选中的文章生成多平台文案。

### 预置订阅源
| 名称 | URL | 方向 |
|------|-----|------|
| 36氪 | https://36kr.com/feed | 科技/商业 |
| 少数派 | https://sspai.com/feed | 效率/工具 |

### 添加自定义订阅
```bash
python3 scripts/manage_feeds.py --add <名称> <RSS_URL>
python3 scripts/fetch_feed.py --source <名称> --limit 3
```

## 工作流程

```
RSS 订阅源
    ↓
fetch_feed.py 抓取最新文章
    ↓
AI 分析：提取观点+评估平台适配度
    ↓
生成内容草稿（知乎/小红书/公众号）
    ↓
保存到飞书 或 直接发布
```

## 系统要求

- Python 3.8+
- OpenClaw + feishu 工具（用于保存草稿）
- 可访问的 RSS 源（部分源需要代理）

## 文件结构

```
rss-content-flow/
├── SKILL.md              # AI 技能定义
├── scripts/
│   ├── manage_feeds.py   # 订阅管理
│   └── fetch_feed.py     # RSS 抓取
└── references/
    └── platform_style.md # 平台风格指南
```

## 与其他 Skill 配合

- **social-media-poster**：生成内容后直接发布
- **feishu-daily-report**：内容草稿归入日报数据源
- **content-repurposer**：同一篇文章改写到不同平台

## License

MIT
