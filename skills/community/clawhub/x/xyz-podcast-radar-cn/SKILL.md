---
name: podcast-radar-cn
description: |
  中文播客数据工具包。用于播客发现、竞品分析、订阅追踪、创作机会评估。
  触发场景：
  · 发现热门/新锐播客或单集
  · 分析某个分类的竞争格局
  · 追踪播客订阅量变化趋势
  · 评估播客创作方向的机会
  · 生成完整的播客创作机会报告
  · 对标学习头部播客案例
  · 话题热度趋势监控
---

# Podcast Radar CN

中文播客数据工具包——**发现 · 分析 · 追踪 · 报告**，覆盖创作者和听众两类核心需求。

## 核心能力矩阵

| 能力 | 数据来源 | 典型场景 |
|------|---------|---------|
| 榜单发现 | xyzrank.com API | 发现热门/新锐播客和单集 |
| 趋势分析 | api.xyzrank.top | 获取播客历史订阅增长曲线 |
| 小宇宙详情 | 小宇宙页面爬取 | 获取订阅量、播放量、评论区 |
| 订阅追踪 | batch_track + 本地 JSON | 监控播客订阅量周变化 |
| 竞争分析 | analyze_genre.py | 评估某分类的竞争强度 |
| 机会报告 | generate_report.py | 生成完整创作机会报告 |
| 爆款追踪 | track_episodes.py | 追踪特定话题/嘉宾的单集表现 |

## 数据来源

### 榜单 API (xyzrank.com)
```
GET https://xyzrank.com/api/episodes      # 热门单集
GET https://xyzrank.com/api/podcasts      # 热门播客
GET https://xyzrank.com/api/new-episodes  # 新锐单集
GET https://xyzrank.com/api/new-podcasts # 新锐播客
```

### 小宇宙详情页
```
# 播客页
https://www.xiaoyuzhoufm.com/podcast/{pid}
  → 订阅量 subscriptionCount

# 单集页
https://www.xiaoyuzhoufm.com/episode/{eid}
  → 播放量、评论数、收藏数、点赞数、节目介绍
```

### 趋势 API (api.xyzrank.top) — 已接入 ✅

官方历史趋势数据，覆盖 9000+ 播客的完整订阅增长曲线。

#### 端点说明

```
GET https://api.xyzrank.top/v1/stats
# 返回所有播客最新订阅统计（含日/月变化）
# 字段: podcast_id, title, latest_count, daily_change, monthly_change

GET https://api.xyzrank.top/v1/metrics/{podcast_id}
# 返回单个播客的完整历史趋势（按日期排列）
# 字段: crawl_date, subscriber_count, status_code
# podcast_id 为小宇宙 24 位字符 ID

GET https://api.xyzrank.top/v1/podcast/{name}
# 按名称搜索播客，返回匹配列表
# 用于获取 podcast_id
```

#### 快速查询示例

```bash
# 查询单个播客历史趋势（以罗永浩为例）
curl -s "https://api.xyzrank.top/v1/metrics/68981df29e7bcd326eb91d88" | python3 -m json.tool

# 查询所有播客最新统计
curl -s "https://api.xyzrank.top/v1/stats" | python3 -c "import json,sys;d=json.load(sys.stdin);[print(f'{p['title']}: {p['latest_count']:,}') for p in d['data'][:10]]"

# 按名称搜索播客获取 ID
curl -s "https://api.xyzrank.top/v1/podcast/纵横四海" | python3 -m json.tool
```

#### 在脚本中使用

**generate_report.py** 和 **analyze_genre.py** 已自动集成趋势 API：

```bash
# 生成报告时自动查询趋势数据
python scripts/generate_report.py --custom-query "纵横四海"
# 输出包含: 当前订阅、总增长、增长率、数据点数量

# 分类分析时自动查询趋势数据
python scripts/analyze_genre.py --genre 科技
# 输出包含: Top 3 增长最快播客的订阅趋势
```

#### 典型响应格式

```json
// /v1/metrics/{podcast_id}
{
  "podcast_id": "68981df29e7bcd326eb91d88",
  "count": 115,
  "data": [
    {"crawl_date": "2026-04-07", "subscriber_count": 317963, "status_code": 200},
    {"crawl_date": "2026-01-24", "subscriber_count": 248242, "status_code": 200}
  ]
}

// /v1/stats
{
  "total": 9464,
  "limit": 50,
  "offset": 0,
  "data": [
    {
      "podcast_id": "625635587bfca4e73e990703",
      "title": "岩中花述",
      "latest_count": 3516964,
      "daily_change": 0,
      "monthly_change": 0
    }
  ]
}
```

## 分析框架

### 增长潜力评估
- 订阅增长率（月度/季度变化，基于 batch_track 历史数据）
- 新入局者数量（新锐榜分析）
- 内容稀缺度（现有数量 vs 需求）
- 趋势方向（热门 vs 新锐交叉）

### 竞争强度评估
- 头部集中度（Top 10 占比 vs 均值）
- 平均播放量差距
- 评论互动率（评论数 / 播放量）
- 更新频率（日更/周更/双周更/月更）

### 内容模式分析
- 时长分布：短（<30min）、中（30-60min）、长（>60min）
- 更新节奏：日更、周更、双周更、月更
- 内容形式：访谈、单口、对话、漫谈
- 标题模式：数字型、话题型、人物型、情绪型

## 场景与工作流

### 场景 1：播客/单集发现（基础）
```bash
# 发现热门单集（默认模式，用户说"热门播客"时触发）
python scripts/fetch_xyz_rank.py --list hot-episodes --limit 20

# 发现热门播客（用户明确要求频道/栏目级时触发）
python scripts/fetch_xyz_rank.py --list hot-podcasts --limit 20

# 新锐播客（发现新入场者）
python scripts/fetch_xyz_rank.py --list new-podcasts --limit 20

# 分类过滤
python scripts/fetch_xyz_rank.py --list hot-podcasts --genre 商业 --limit 20

# 关键词搜索
python scripts/fetch_xyz_rank.py --list hot-episodes --query "AI创业" --limit 20

# 按新鲜度过滤（30天内更新）
python scripts/fetch_xyz_rank.py --list new-episodes --freshness-days-max 30 --limit 20

# 按播放量下限过滤
python scripts/fetch_xyz_rank.py --list hot-episodes --min-play-count 50000 --limit 20
```

### 场景 2：竞品分析
```bash
# 分析某分类的竞争格局
python scripts/analyze_genre.py --genre 商业

# 对比多个分类
python scripts/analyze_genre.py --genre 科技 --compare-genres 商业 个人成长
```

### 场景 3：订阅追踪（需先初始化）
```bash
# 初始化：获取热门播客并抓取订阅量
python scripts/batch_track.py init --max 500

# 更新所有追踪播客的订阅量
python scripts/batch_track.py update

# 查看订阅趋势
python scripts/batch_track.py trends "纵横四海"

# 列出所有追踪的播客
python scripts/batch_track.py list
```

### 场景 4：创作机会报告
```bash
# 分析某分类的完整创作机会
python scripts/generate_report.py --genre 个人成长

# 自定义关键词分析
python scripts/generate_report.py --custom-query "AI创业"

# 完整报告输出包括：
#   · 领域概览（播客数量、新锐数量）
#   · 增长最快的播客（基于订阅追踪数据）
#   · 竞争格局（门槛、中位值、头部集中系数）
#   · 爆款单集模式（内容形式、时长分布）
#   · 推荐对标案例（Top 5 + 是否已追踪标记）
#   · 创作切入点建议
```

### 场景 5：小宇宙详情补充（慎用，最多 20 条）
```bash
# 补充单个播客详情
python scripts/enrich_xiaoyuzhou.py \
  --podcast-url https://www.xiaoyuzhoufm.com/podcast/625635587bfca4e73e990703

# 补充单集详情
python scripts/enrich_xiaoyuzhou.py \
  --episode-url https://www.xiaoyuzhoufm.com/episode/69bf524c2d318777c9169361

# 从榜单 JSON 批量补充（最多 20 条）
python scripts/fetch_xyz_rank.py --list hot-episodes --query "AI" --limit 20 | \
  python scripts/enrich_xiaoyuzhou.py --from-json -
```

### 场景 6：爆款单集追踪
```bash
# 追踪特定话题的爆款单集
python scripts/track_episodes.py --topic "AI" --limit 30

# 追踪特定嘉宾出现过的单集
python scripts/track_episodes.py --guest "张雪峰" --limit 20

# 导出为简报格式
python scripts/track_episodes.py --topic "注意力" --report
```

### 场景 7：话题热度趋势
```bash
# 监控话题在热门/新锐榜的出现频率变化
python scripts/topic_trends.py --topics "AI创业,副业,MBTI,注意力" --weeks 4

# 输出：各话题在热门榜 vs 新锐榜的占比趋势
```

## Query 语义规则

**中文用户的"播客"常指"最近值得点开的内容"**，默认返回单集级结果。

| 用户说 | 默认映射 | 切换条件 |
|--------|---------|---------|
| 热门播客、最近火什么 | hot-episodes | 明确说"频道"/"栏目"时→hot-podcasts |
| 新播客、最近新出的 | new-episodes | 明确要求show-level时→new-podcasts |
| 播客频道/栏目/榜单 | hot-podcasts | — |
| 对标学习/竞品 | hot-podcasts | — |

**标题信号优先**：先从标题、排名、播放量判断，标题信号充足时不 enrich。

## Xiaoyuzhou Enrichment 规则

- ⚠️ 默认 **不 enrich**
- ⚠️ 最多 20 条/次
- ⚠️ 仅在榜单数据无法回答问题时使用

适用场景：
- 短列表需要更好的推荐理由
- 需要从单集页获取真实 PID
- 需要节目介绍/单集简介用于最终推荐

## 数据边界

- 榜单周更，非分钟级实时
- 覆盖主要中文播客平台（小宇宙为主）
- 部分历史数据可能不完整
- 区分"数据事实"和"分析推断"

## 脚本索引

| 脚本 | 功能 | 输入 |
|------|------|------|
| `fetch_xyz_rank.py` | 获取榜单数据 + 过滤 + 标题信号 | list/genre/query |
| `batch_track.py` | 批量订阅追踪（init/update/trends/list） | 播客名 |
| `analyze_genre.py` | 分类竞争格局分析 | --genre |
| `generate_report.py` | 完整创作机会报告 | --genre / --custom-query |
| `track_episodes.py` | 爆款单集追踪 | --topic / --guest |
| `topic_trends.py` | 话题热度趋势监控 | --topics |
| `enrich_xiaoyuzhou.py` | 小宇宙页面详情补充 | URL / JSON |

## API 速查卡

### xyzrank.com 榜单 API
```bash
# 热门单集
https://xyzrank.com/api/episodes?limit=20

# 热门播客
https://xyzrank.com/api/podcasts?limit=20

# 新锐单集
https://xyzrank.com/api/new-episodes?limit=20

# 新锐播客
https://xyzrank.com/api/new-podcasts?limit=20

# 带过滤
https://xyzrank.com/api/episodes?query=AI&genre=科技&limit=20
```

### api.xyzrank.top 趋势 API
```bash
# 所有播客最新统计
https://api.xyzrank.top/v1/stats

# 单个播客历史趋势（pid 为小宇宙 24 位 ID）
https://api.xyzrank.top/v1/metrics/{podcast_id}

# 按名称搜索播客
https://api.xyzrank.top/v1/podcast/{name}
```

### 小宇宙页面
```bash
# 播客页（获取订阅量）
https://www.xiaoyuzhoufm.com/podcast/{pid}

# 单集页（获取播放量、评论数）
https://www.xiaoyuzhoufm.com/episode/{eid}
```

## 参考文档

- [references/title-signals.md](references/title-signals.md) — 标题信号解读
- [references/output-modes.md](references/output-modes.md) — 输出格式指南
- [references/api.md](references/api.md) — API 字段说明
