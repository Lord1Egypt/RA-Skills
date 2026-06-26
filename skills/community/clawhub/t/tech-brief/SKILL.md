# 📡 Tech Brief - 科技资讯简报

追踪内存、AI、算力领域的最新资讯、政策、活动和热点话题。

## ⚙️ 前置依赖

首次使用前需安装依赖：

```bash
pip install requests beautifulsoup4 lxml python-dateutil feedparser
```

## 🎯 触发条件

当用户说出以下关键词时激活：

- "科技资讯"
- "每日简报"
- "最新科技"
- "内存新闻"
- "AI新闻"
- "算力动态"

## 📊 覆盖内容

| 类别 | 内容 |
|------|------|
| 行业新闻 | 内存、AI、算力相关新品、技术动态 |
| 政策动态 | 国家/地方AI政策、算力规划 |
| 活动会议 | 发布会、行业峰会、研讨会 |
| 热点话题 | 微博热搜、知乎热榜 |

## 🔄 工作流程

```
Phase 1: 并发采集 → Phase 2: 过滤分类 → Phase 3: 输出简报
```

### Phase 1: 信息采集

| 脚本 | 功能 |
|------|------|
| `fetch_news.py` | 采集科技媒体新闻（RSS + 爬虫） |
| `fetch_policy.py` | 采集AI/算力相关政策（复用 AI Policy Brief） |
| `fetch_trends.py` | 采集热点话题（微博、知乎） |

### Phase 2: 内容过滤

- **时间过滤**：最近7天
- **关键词匹配**：内存、AI、算力、大模型、GPU、DDR5、H100 等
- **去重**：同一内容保留最权威来源

### Phase 3: 输出简报

结构化 Markdown 输出，推送给用户

## 📁 目录结构

```
tech-brief/
├── SKILL.md                    # 本文档
├── scripts/
│   ├── daily_fetch.py          # 每日汇总主脚本
│   ├── fetch_news.py           # 新闻采集
│   ├── fetch_policy.py         # 政策采集
│   └── fetch_trends.py         # 热点采集
├── references/
│   └── sources.md              # 数据源清单
└── output/                     # 生成的简报
```

## 🚀 快速开始

### 方式一：手动触发

```bash
python scripts/daily_fetch.py --days 7
```

### 方式二：定时自动（cron）

```bash
# 每天早上 8:30 自动执行
30 8 * * * python /path/to/scripts/daily_fetch.py
```

## ⚙️ 可选参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--days` | 7 | 时间范围（天） |
| `--output` | output/brief.md | 输出文件 |
| `--topics` | memory,ai,compute | 主题筛选 |
| `--quiet` | False | 静默模式（不打印日志） |

## 📋 输出示例

```markdown
# 📡 科技资讯简报（2026年4月3日）

## 🔥 热点话题
- 微博：#内存价格暴涨# TOP10
- 知乎：英伟达新GPU发布引热议

## 📰 行业新闻
- [三星量产DDR5-9600] 超能网
- [OpenAI发布GPT-5] TechCrunch

## 📜 政策动态
- 国务院：加快推进AI发展意见
- 广东省：算力基础设施专项规划

---
📊 今日共收录 XX 条资讯
```

## 🔧 数据源清单

详见 `references/sources.md`

## ⚠️ 注意事项

- 部分网站有反爬机制，需降低请求频率
- 热点话题获取可能需要登录或 API
- 政策信息以政府官网为准，媒体解读仅作参考