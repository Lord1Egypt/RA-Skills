---
name: xinqing-journal
version: 1.0.0
description: >
  心情日记 — 智能情绪追踪器，通过自然语言记录中文日记、自动识别7种情绪、
  1-10分评分、智能标签提取，生成日/周/月报告和趋势分析。
  数据纯本地JSON存储，零网络请求，保护隐私。
emoji: "\U0001F308"
category: health
tags:
  - health
  - journal
  - mood-tracker
  - chinese
  - mental-health
  - privacy
requires:
  python: ">=3.9"
os:
  - macos
  - linux
  - windows
author: dyby99
license: MIT
---

# Xinqing Journal - 心情日记

用自然语言记录每天的心情，自动分析情绪变化趋势。

## 功能特性

- 📝 **自然语言日记**: "今天工作很顺利，心情不错"
- 🎭 **情绪自动识别**: 开心、平静、兴奋、焦虑、难过、愤怒、疲惫
- ⭐ **情绪评分**: 1-10分自动或手动评分
- 🏷️ **智能标签提取**: 自动提取人、事、物、地点、天气标签
- 📊 **多维度报告**: 日报、周报、月报、趋势分析
- 🔒 **本地数据存储**: JSON文件存储，保护隐私
- 📅 **心情日历**: 可视化月历查看情绪分布
- 💡 **智能建议**: 根据情绪数据给出健康建议

## 快速开始

### 添加日记

```bash
# 简单日记
python scripts/journal.py add "今天工作很顺利，心情不错"

# 指定情绪评分
python scripts/journal.py add "今天下雨了有点郁闷，心情4分"

# 详细日记
python scripts/journal.py add "今天和朋友去了咖啡店，聊得很开心，心情9分"

# 昨天日记
python scripts/journal.py add "昨天加班到很晚很累"
```

### 查看日记

```bash
# 列出最近7天
python scripts/journal.py list

# 列出最近30天
python scripts/journal.py list 30

# 按情绪筛选
python scripts/journal.py list 30 开心
```

### 心情日历

```bash
# 本月日历
python scripts/journal.py calendar

# 指定年月
python scripts/journal.py calendar 2024 1
```

### 生成情绪报告

```bash
# 日报
python scripts/mood-report.py daily
python scripts/mood-report.py daily 2024-01-15

# 周报
python scripts/mood-report.py weekly
python scripts/mood-report.py weekly 1  # 上周

# 月报
python scripts/mood-report.py monthly
python scripts/mood-report.py monthly 1  # 上月

# 趋势分析
python scripts/mood-report.py trend 30
```

### 查看统计

```bash
# 情绪摘要
python scripts/journal.py summary
python scripts/journal.py summary 90

# 情绪类型列表
python scripts/journal.py moods
```

### 编辑和删除

```bash
# 更新日记
python scripts/journal.py update abc123 "修改后的内容"

# 删除日记
python scripts/journal.py delete abc123
```

## 项目结构

```
xinqing-journal/
├── SKILL.md                      # 本文件
├── .clawhubignore               # 发布忽略配置
├── scripts/
│   ├── journal.py               # 核心日记模块
│   └── mood-report.py           # 情绪报告生成器
└── assets/
    └── moods.json               # 情绪配置
```

## 数据存储

- **路径**: `~/.openclaw/workspace/data/journal/entries.json`
- **格式**: JSON
- **隐私**: 纯本地存储，不上传云端
- **原子写入**: 使用临时文件+原子替换，防止数据损坏

数据结构:
```json
{
  "entries": [
    {
      "id": "a1b2c3d4",
      "date": "2024-01-15",
      "content": "今天工作很顺利",
      "mood": "开心",
      "score": 8,
      "tags": ["工作"],
      "raw_text": "今天工作很顺利，心情不错",
      "created_at": "2024-01-15T12:30:00",
      "updated_at": "2024-01-15T12:30:00"
    }
  ],
  "version": "1.0"
}
```

## 自然语言支持

### 时间表达
- "今天..." - 今天
- "昨天..." - 昨天
- "前天..." - 前天
- "2024-01-15..." - 指定日期

### 情绪评分
- "心情8分"
- "评分9"
- "mood 7"
- "8/10"

### 情绪识别关键词

| 情绪 | 触发关键词 |
|------|-----------|
| 开心 | 开心、高兴、快乐、愉快、欢喜、喜悦、美滋滋、哈哈、嘿嘿 |
| 平静 | 平静、平和、安宁、淡定、从容、安稳、宁静、祥和 |
| 兴奋 | 兴奋、激动、亢奋、狂喜、太棒了、绝了、燃、起飞 |
| 焦虑 | 焦虑、担心、紧张、不安、忐忑、发愁、压力大、迷茫 |
| 难过 | 难过、伤心、悲伤、失落、沮丧、郁闷、委屈、想哭、emo |
| 愤怒 | 愤怒、生气、恼火、气愤、不爽、烦躁、火大、爆炸 |
| 疲惫 | 疲惫、累、疲倦、困、乏力、没精神 |

## 标签自动提取

自动识别以下类别标签:

- **人**: 朋友、家人、同事、老板、同学、对象
- **事**: 工作、学习、考试、项目、会议、面试
- **物**: 咖啡、茶、书、电影、音乐、游戏
- **地点**: 公司、家、学校、咖啡店、公园
- **天气**: 晴天、阴天、下雨、下雪、热、冷

## 报告类型

### 日报
- 当日情绪评分
- 情绪类型分布
- 日记内容列表

### 周报
- 本周情绪总览
- 日均情绪评分
- 每日情绪变化
- 主导情绪分析
- 健康建议

### 月报
- 月度情绪总览
- 每周情绪概况
- 情绪分布统计
- 主导情绪变化
- 月度建议

### 趋势分析
- 情绪趋势（上升/下降/稳定）
- 每周情绪评分变化
- 情绪波动异常检测
- 长期健康建议

## 命令行参考

### journal.py 命令

| 命令 | 用法 | 说明 |
|------|------|------|
| add | `add <内容>` | 添加日记 |
| list | `list [天数] [情绪]` | 列出日记 |
| calendar | `calendar [年] [月]` | 心情日历 |
| summary | `summary [天数]` | 情绪摘要 |
| delete | `delete <ID>` | 删除日记 |
| moods | `moods` | 情绪类型列表 |
| update | `update <ID> <内容>` | 更新日记 |

### mood-report.py 命令

| 命令 | 用法 | 说明 |
|------|------|------|
| daily | `daily [日期]` | 日报 |
| weekly | `weekly [偏移]` | 周报 |
| monthly | `monthly [偏移]` | 月报 |
| trend | `trend [天数]` | 趋势分析 |

## 配置文件

情绪配置存储在 `assets/moods.json`:

```json
{
  "moods": {
    "开心": {
      "score_range": [7, 9],
      "keywords": ["开心", "高兴", "快乐"],
      "emoji": "😊",
      "color": "#FFD93D"
    }
  },
  "tag_patterns": {
    "人": ["朋友", "家人", "同事"],
    "事": ["工作", "学习", "考试"]
  }
}
```

可自定义:
- 情绪类型和关键词
- 评分范围
- Emoji和颜色
- 标签提取规则

## 使用建议

1. **每日记录**: 养成每天写日记的习惯，可以在睡前花3-5分钟回顾一天
2. **诚实表达**: 记录真实的情绪，不必掩饰负面情绪
3. **具体描述**: 尝试描述产生情绪的具体原因，而不仅是情绪本身
4. **定期复盘**: 每周查看周报，了解自己的情绪周期
5. **关注趋势**: 注意长期趋势，而非单一天的评分

## 情绪健康提示

- 评分持续低于3分超过一周，建议寻求专业帮助
- 情绪波动过大（忽高忽低）可能提示压力过大
- 长期焦虑或难过情绪需要关注心理健康
- 保持记录本身就是情绪调节的好方法

## 故障排除

### 无法识别情绪
- 在日记中使用更明确的情绪词汇
- 直接指定评分："心情5分"

### 数据文件损坏
- 使用原子写入机制，极少出现损坏
- 如有问题可手动编辑 JSON 文件修复
- 建议定期备份 `entries.json`

### 标签提取不准确
- 在 `moods.json` 中添加自定义标签关键词
- 在日记中使用更具体的词汇

## 扩展开发

### 添加新情绪类型

编辑 `assets/moods.json`:

```json
{
  "moods": {
    "新情绪": {
      "score_range": [4, 6],
      "keywords": ["关键词1", "关键词2"],
      "emoji": "🆕",
      "color": "#FFFFFF"
    }
  }
}
```

### 作为模块使用

```python
from scripts.journal import JournalTracker

tracker = JournalTracker()
entry = tracker.add("今天心情不错")
print(entry)

# 获取统计
summary = tracker.get_summary(days=30)
print(summary)
```

## 技术规格

- **Python版本**: 3.9+
- **依赖**: 无外部依赖，仅使用标准库
- **编码**: UTF-8
- **数据格式**: JSON
- **ID生成**: UUID短ID（8位）
- **文件操作**: 原子写入

## 隐私说明

- 所有数据仅存储在本地
- 无网络传输
- 无云端同步
- 用户完全拥有数据

## 许可证

MIT License
