---
slug: rss-content-flow
name: RSS内容流
version: "1.0.0"
author: 千策
---


# RSS 内容抓取

将 RSS 订阅转化为结构化内容素材。

## 核心能力

1. **RSS 订阅管理** — 添加/删除/列出订阅源
2. **内容抓取** — 自动获取最新 N 篇文章（支持 RSS 2.0 和 Atom）
3. **智能过滤** — 去除广告/软文，过滤7天前的旧文章

## 快速开始

用户说"帮我找今天的选题"时：

```
1. 读取 ~/.qclaw/skills/rss-content-flow/scripts/config.json（订阅列表）
2. 用 fetch_feed.py 获取各源最新条目
3. 呈现可用选题供用户选择
4. 用户确认后 → 用 AI 改写内容
```

## 订阅管理

### 添加订阅源
```bash
python3 scripts/manage_feeds.py --add <名称> <URL>
# 示例：python3 scripts/manage_feeds.py --add 36氪 https://36kr.com/feed
```

### 列出订阅
```bash
python3 scripts/manage_feeds.py --list
```

### 删除订阅
```bash
python3 scripts/manage_feeds.py --remove <名称>
```

### 初始化默认订阅
```bash
python3 scripts/manage_feeds.py --init
```

### 默认订阅源（预配置）
| 名称 | URL | 内容方向 |
|------|-----|---------|
| 36氪 | https://36kr.com/feed | 科技/商业 |
| 虎嗅 | https://www.huxiu.com/rss/0.xml | 商业/创业 |
| 少数派 | https://sspai.com/feed | 效率/工具 |
| AI研习社 | https://ai.googleblog.com/feed/ | AI/技术 |

## 内容抓取

### 单源抓取
```bash
python3 scripts/fetch_feed.py --source 36氪 --limit 5
```

### 全源抓取
```bash
python3 scripts/fetch_feed.py --all --limit 3
```

输出示例：
```
📰 36氪 | 4篇新文章
  ① [AI创业] 标题：xxx
  ② [商业] 标题：xxx
  ...

📰 虎嗅 | 2篇新文章
  ① [汽车] 标题：xxx
  ...
```

### 抓取逻辑
1. 解析 RSS XML，获取 title/link/description/pubDate
2. 过滤：去除广告/软文/太旧的文章（>7天）
3. 按时间倒序排列
4. 返回结构化 JSON

### JSON 输出（供程序处理）
```bash
python3 scripts/fetch_feed.py --all --json
```

## 后续处理

获取文章列表后，用户可将标题和摘要复制给 AI 进行分析和改写。Skill本身只负责数据抓取，不包含自动内容生成功能。

## 配置项

| 配置 | 说明 | 默认值 |
|------|------|--------|
| 订阅源 | 监控哪些 RSS | 36氪+虎嗅+少数派 |
| 抓取数量 | 每次取几条 | 每源3条 |
| 文章有效期 | 过滤几天前的文章 | 7天 |

## 文件结构

```
rss-content-flow/
├── SKILL.md              # 本文件
├── scripts/
│   ├── manage_feeds.py   # 订阅管理（增删查）
│   ├── fetch_feed.py     # RSS 抓取脚本
│   └── config.json       # 订阅配置（运行时生成）
└── assets/               # 封面图模板等（可选）
```

## 与其他 Skill 的配合

- **cn-auto-publisher**：获取文章后，生成内容可交给 cn-auto-publisher 发布到知乎/小红书
- **cn-trends-ai**：热点 + RSS 结合，获得更完整的内容来源

## 注意事项

- RSS 源需确保可访问，过期/失效的源自动跳过
- 抓取间隔建议不低于 30 分钟，避免对源站造成压力
- 本 Skill 只负责 RSS 数据抓取，不包含内容分析和改写功能

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
