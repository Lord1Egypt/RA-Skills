---
name: social-intel
description: 社媒情报中心 - 多平台爬虫 + 数据分析 + AI洞察 + 词云 + 趋势追踪
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires":
          {
            "bins": ["mcporter", "python3"],
            "dirs": ["/Users/kk/openclaw-media", "/Users/kk/openclaw-crawl4ai"],
            "python_pkgs": ["wordcloud", "matplotlib", "openpyxl"],
          },
        "install":
          [
            {
              "id": "deps",
              "kind": "manual",
              "label": "pip3 install wordcloud matplotlib openpyxl",
            },
          ],
      },
  }
---

# Social Intel Hub v2 — 社媒情报中心

一句话需求，结构化数据 + 可视化 + AI洞察，全套出来。

## 触发方式

> "爬小红书服装数据并分析"
> "分析微博AI相关内容"
> "生成奶茶的词云图"
> "对比咖啡和茶饮的差异"

## 核心脚本

```
/Users/kk/.openclaw/workspace/skills/social-intel/social_intel.py
```

## 支持平台

| 平台 | 参数 | 主要数据 |
|------|------|---------|
| 小红书 | `xhs` | 笔记/点赞/收藏/评论数 |
| 微博 | `weibo` / `wb` | 帖子/转发/评论数 |
| B站 | `bilibili` / `bili` | 视频/点赞/浏览/弹幕 |
| 抖音 | `douyin` / `dy` | 视频/点赞/浏览/评论 |
| 快手 | `kuaishou` / `ks` | 短视频/点赞/浏览 |
| TikTok | `tiktok` | 视频 |
| YouTube | `youtube` / `yt` | 视频/字幕 |

## 意图索引

| 用户意图 | 触发条件 | 功能 |
|---------|---------|------|
| 搜索 + 分析 | "爬/分析/查看+平台+关键词" | 默认模式 |
| 多平台并行 | "所有平台+关键词" | `--all-platforms` |
| 竞品对比 | "对比/比较+关键词1+关键词2" | `--compare` |
| 趋势追踪 | "趋势/近期+关键词" | `--trend` |
| 词云图 | "词云/可视化+关键词" | `--wordcloud` |
| 评论采集 | "评论+关键词" | `--comments` |
| 数据导出 | "导出/csv/excel+关键词" | `--export` |

## 使用示例

### 基础搜索 + 分析报告
```bash
python3 social_intel.py -k "咖啡" -p xhs -m 30 --analyze
```
输出：高频标签 TOP15 + 高赞内容 + 日期趋势 + AI洞察prompt

### 多平台并行搜索
```bash
python3 social_intel.py -k "AI" --all-platforms -m 20
```
同时爬取微博/B站/小红书/抖音/快手，一次看全网反应

### 竞品对比
```bash
python3 social_intel.py -k "对比" -p xhs --compare "咖啡" "奶茶" "气泡水"
```
输出对比表：哪个话题更热、标签差异、用户偏好

### 趋势追踪（近7天）
```bash
python3 social_intel.py -k "新品" -p xhs --trend
```
每天一条快照，自动判断上升/下降/平稳趋势

### 生成词云图
```bash
python3 social_intel.py -k "穿搭" -p xhs -m 30 --wordcloud -o /tmp/chuanda.png
```

### 采集指定笔记评论
```bash
python3 social_intel.py -k "咖啡" -p xhs --comments 69aae46f000000001a0298f1
```

### 导出数据
```bash
# CSV
python3 social_intel.py -k "运动鞋" -p xhs -m 50 --export csv -o /tmp/shoes.csv

# Excel（多平台对比）
python3 social_intel.py -k "咖啡" --all-platforms -m 30 --export excel -o /tmp/coffee_multi.xlsx
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `-k / --keyword` | 搜索关键词（必填） |
| `-p / --platform` | 平台，默认 xhs；`all` 表示全部平台 |
| `-m / --max` | 最大笔记数，默认 20 |
| `--pages` | 搜索页数，默认 1（每页约 20 条） |
| `--analyze` | 输出完整分析报告（默认开启） |
| `--all-platforms` | 并行搜索所有平台 |
| `--compare KW1 KW2...` | 竞品对比模式 |
| `--trend` | 近7天趋势分析 |
| `--wordcloud` | 生成词云图 PNG |
| `--comments NOTE_ID` | 采集指定笔记评论 |
| `--export csv\|excel\|both` | 导出格式 |
| `-o / --output` | 输出文件路径 |
| `--no-cache` | 禁用缓存，强制重新请求 |

## 分析报告内容

- 📈 **总体指标**：总点赞/收藏/浏览/评论 + 均值
- 🏷️ **高频话题**：TOP20 标签 + 可视化条形图
- 🔥 **TOP3**：点赞最高 + 评论最多 + 浏览最多
- 📅 **趋势**：按日期聚合 + 热度条形图
- 💡 **AI洞察**：自动生成可复制的 LLM 分析 prompt

## 缓存机制

- 自动缓存：每个搜索请求缓存 24 小时
- 缓存路径：`/tmp/social_intel_cache/`
- 重复查询走缓存，不消耗 TikHub 余额
- 用 `--no-cache` 强制刷新

## 依赖

| 包 | 用途 | 安装 |
|----|------|------|
| wordcloud | 词云生成 | `pip3 install wordcloud` |
| matplotlib | 词云可视化 | `pip3 install matplotlib` |
| openpyxl | Excel 导出 | `pip3 install openpyxl` |

## 底层架构

```
用户需求 → social_intel.py（统一入口）
    ├── TikHub MCP（主力，零登录，7平台并行）
    ├── 24h 缓存（节省余额）
    ├── 数据分析（词频/趋势/竞品对比）
    ├── 词云生成（wordcloud）
    ├── 导出（CSV/Excel）
    └── AI洞察 prompt（喂给 MiniMax LLM）
```

## 后续可扩展方向

- [ ] MediaCrawler 评论情感分析（需登录）
- [ ] MiniMax LLM 直接生成洞察文字
- [ ] Cron 定时趋势监控 + 飞书推送
- [ ] 热度预测模型
