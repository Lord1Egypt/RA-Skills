---
name: A股实时热度排名TOP50
description_en: "[Python Version] Get real-time A-share stock heat ranking TOP50. Aggregates popularity lists from Wencai, Xueqiu, and Eastmoney platforms. Use this skill when: user asks for A-share hot stocks, stock popularity ranking, stock heat ranking, market attention ranking, hot stock list, most followed stocks, trending stocks, real-time stock ranking. Keywords: A股热度, 股票热度排名, 人气排名, 热门股票, 股票人气榜, 关注度排行."
description: "[Python版本] 获取A股股票实时热度排名TOP50。聚合问财、雪球、东方财富三大平台人气榜单。适用场景：用户询问A股热门股票、股票热度排名、股票人气排名、市场关注度排行、热门股票榜单、最受关注股票、实时股票排名、今日热门股。关键词：A股热度、股票热度排名、人气排名、热门股票、股票人气榜、关注度排行、热门股、人气股、热门榜单。"
---

# 股票热度排名采集器 (Python版) / A-Share Heat Rank Collector (Python Version)

## 执行流程 / Execution Flow

```
输入/Input: 无/None → 输出/Output: 复合热度TOP50排行榜/Composite Heat TOP50 Ranking
├── 问财人气排名 / Wencai Popularity Rank (50只/stocks)
├── 雪球热榜 / Xueqiu Hot List (50只A股/A-shares)
├── 东方财富人气排名 / Eastmoney Popularity Rank (50只/stocks)
└── 复合热度计算与排名 / Composite Heat Calculation & Ranking
```

---

## 环境要求 / Requirements

- Python 3.8+
- Node.js (用于生成问财签名 / for Wencai signature generation)

---

## 安装依赖 / Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 执行步骤 / Execution Steps

```bash
# 运行 / Run
python main.py

# 指定参数 / With parameters
python main.py --top 20 --format json
```

---

## 输出格式 / Output Format

```
=== 股票热度排名采集器 ===
采集时间: 2026-03-21 22:49:00

【问财】正在采集...
  成功获取 50 只股票

【雪球】正在采集...
  成功获取 50 只A股

【东财】正在采集...
  成功获取 50 只股票

=== 复合热度排名 ===
问财: 50 | 雪球: 50 | 东财: 50

┌──────┬──────────┬────────────┬──────┬──────┬──────┬──────────┬──────┐
│ 排名 │   代码   │    名称    │ 问财 │ 雪球 │ 东财 │  热度分  │ 出现 │
├──────┼──────────┼────────────┼──────┼──────┼──────┼──────────┼──────┤
│    1 │   601899 │ 紫金矿业   │    3 │    1 │    3 │     98.0 │    3 │
│    2 │   001896 │ 豫能控股   │    6 │   15 │   17 │     89.1 │    3 │
...
└──────┴──────────┴────────────┴──────┴──────┴──────┴──────────┴──────┘
```

---

## 字段说明 / Field Description

| 字段/Field | 说明/Description |
|------|------|
| 排名/Rank | 复合热度排名 (1-50) / Composite heat ranking (1-50) |
| 代码/Code | 6位股票代码 / 6-digit stock code |
| 名称/Name | 股票名称 / Stock name |
| 问财/Wencai | 问财人气排名，`-` 表示未上榜 / Wencai popularity rank |
| 雪球/Xueqiu | 雪球热榜排名，`-` 表示未上榜 / Xueqiu hot rank |
| 东财/Eastmoney | 东方财富人气排名，`-` 表示未上榜 / Eastmoney popularity rank |
| 热度分/HeatScore | 复合热度分数 (越高越热) / Composite heat score |
| 出现/Appear | 出现在几个平台 (1-3) / Number of platforms appeared |

---

## 复合热度算法 / Composite Heat Algorithm

```
热度分 = (基础分 + 加成分) / 3.5

基础分:
- 问财排名得分 = 100 - 排名
- 雪球排名得分 = 100 - 排名
- 东财排名得分 = 100 - 排名

加成分:
- 出现3个平台: +50分
- 出现2个平台: +20分
- 出现1个平台: +0分
```

---

## 项目结构 / Project Structure

```
skills/stock-heat-rank-py/
├── SKILL.md           # 技能文档 / Skill documentation
├── main.py            # 主程序 / Main program
├── requirements.txt   # Python依赖 / Python dependencies
└── lib/
    └── hexin_v.js     # Hexin-V 签名生成器 / Hexin-V signature generator