# Podcast Radar CN

中文播客数据工具包——**发现 · 分析 · 追踪 · 报告**

## 简介

Podcast Radar CN 是一个面向中文播客创作者和听众的数据工具包。它整合了 xyzrank 榜单数据、小宇宙详情页、官方趋势 API 等多源数据，提供从播客发现、竞品分析到订阅追踪的完整工作流。

## 核心功能

| 功能 | 说明 | 对应脚本 |
|------|------|---------|
| 🔍 榜单发现 | 获取热门/新锐播客和单集 | `fetch_xyz_rank.py` |
| 📈 趋势分析 | 官方历史订阅增长数据 | `analyze_genre.py`, `generate_report.py` |
| 📝 详情补充 | 小宇宙页面订阅量、播放量 | `enrich_xiaoyuzhou.py` |
| 📊 订阅追踪 | 本地订阅量变化监控 | `batch_track.py` |
| ⚔️ 竞争分析 | 分类竞争格局评估 | `analyze_genre.py` |
| 📋 机会报告 | 完整创作机会分析报告 | `generate_report.py` |
| 🔥 爆款追踪 | 特定话题/嘉宾单集追踪 | `track_episodes.py` |
| 📉 话题趋势 | 话题热度趋势监控 | `topic_trends.py` |

## 快速开始

```bash
# 1. 发现热门播客
python scripts/fetch_xyz_rank.py --list hot-podcasts --limit 20

# 2. 分析某个分类的竞争格局
python scripts/analyze_genre.py --genre 科技

# 3. 生成完整创作机会报告
python scripts/generate_report.py --custom-query "AI"

# 4. 初始化订阅追踪
python scripts/batch_track.py init --max 100

# 5. 追踪特定话题的爆款单集
python scripts/track_episodes.py --topic "职场" --limit 30
```

## 数据来源

- **xyzrank.com API**: 热门/新锐榜单数据
- **api.xyzrank.top**: 官方历史趋势数据（9000+ 播客）
- **小宇宙页面**: 订阅量、播放量、评论数

## 依赖

- Python 3.8+
- 标准库: `urllib`, `json`, `argparse`, `subprocess`
- 无需额外 pip 安装

## 文件结构

```
podcast-radar-cn/
├── SKILL.md                 # 技能主文档
├── README.md               # 本文件
├── scripts/                # 核心脚本
│   ├── fetch_xyz_rank.py   # 榜单获取
│   ├── analyze_genre.py    # 竞争分析
│   ├── generate_report.py  # 报告生成
│   ├── batch_track.py      # 订阅追踪
│   ├── track_episodes.py   # 爆款追踪
│   ├── topic_trends.py     # 话题趋势
│   └── enrich_xiaoyuzhou.py # 详情补充
├── references/             # 参考文档
│   ├── api.md             # API 字段说明
│   ├── title-signals.md   # 标题信号解读
│   └── output-modes.md    # 输出格式指南
└── agents/                # Agent 配置
    └── openai.yaml
```

## 使用场景

### 场景 1: 我想做播客，不知道选什么方向
```bash
python scripts/analyze_genre.py --genre 商业
python scripts/analyze_genre.py --genre 科技
# 对比不同分类的竞争强度，选择机会更大的方向
```

### 场景 2: 我想学习头部播客怎么做
```bash
python scripts/generate_report.py --custom-query "纵横四海"
# 获取对标播客的完整分析报告
```

### 场景 3: 我想追踪自己的播客数据
```bash
python scripts/batch_track.py init --max 50
# 初始化追踪，然后设置 cron 每日自动更新
```

### 场景 4: 我想了解某个话题的热度
```bash
python scripts/topic_trends.py --topics "AI,副业,职场"
# 对比多个话题在榜单中的出现频率
```

## 注意事项

- 数据仅供分析参考，不构成投资建议
- 部分历史数据可能不完整
- 请区分"数据事实"和"分析推断"
- 遵守各平台的数据使用规范

## License

MIT

## 致谢

- 数据来自 [xyzrank.com](https://xyzrank.com) 和 [api.xyzrank.top](https://api.xyzrank.top)
- 小宇宙数据来自 [xiaoyuzhoufm.com](https://www.xiaoyuzhoufm.com)
