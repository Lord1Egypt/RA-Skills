---
name: A股实时热度排名
description_en: "[Go Version] Get real-time A-share market heat ranking TOP50. Aggregates popularity lists from Wencai, Xueqiu, and Eastmoney platforms, calculates composite heat scores. Use this skill when you need to query popular A-shares, real-time popularity rankings, market attention rankings, or limit-up heat analysis. Supports multi-platform heat comparison to discover market hot stocks."
description: "[Go语言版] 获取A股市场实时热度排名TOP50。聚合问财、雪球、东方财富三大平台人气榜单，计算复合热度分数。当用户需要查询A股热门股票、实时人气排名、市场关注度排行、涨停板热度分析时使用此技能。支持多平台热度对比，发现市场热点股票。"
---

# 股票热度排名采集器 (Go版) / A-Share Heat Rank Collector (Go Version)

## 执行流程 / Execution Flow

```
输入/Input: 无/None → 输出/Output: 复合热度TOP50排行榜/Composite Heat TOP50 Ranking
├── 问财人气排名 / Wencai Popularity Rank (50只/stocks)
├── 雪球热榜 / Xueqiu Hot List (50只A股/A-shares)
├── 东方财富人气排名 / Eastmoney Popularity Rank (50只/stocks)
└── 复合热度计算与排名 / Composite Heat Calculation & Ranking
```

---

## 输出格式 / Output Format

```
=== 股票热度排名采集器 / Stock Heat Rank Collector ===
采集时间/Collection Time: 2026-03-21 13:56:22

【问财/Wencai】正在采集.../Collecting...
  成功获取 50 只股票 / Successfully fetched 50 stocks

【雪球/Xueqiu】正在采集.../Collecting...
  成功获取 50 只A股 / Successfully fetched 50 A-shares

【东财/Eastmoney】正在采集.../Collecting...
  成功获取 50 只股票 / Successfully fetched 50 stocks

=== 复合热度排名 / Composite Heat Ranking ===
问财/Wencai: 50 | 雪球/Xueqiu: 50 | 东财/Eastmoney: 50

┌──────┬──────────┬────────────┬──────┬──────┬──────┬──────────┬──────┐
│ 排名 │   代码   │    名称    │ 问财 │ 雪球 │ 东财 │  热度分  │ 出现 │
│ Rank │   Code   │    Name    │ Wencai│Xueqiu│Eastmoney│ HeatScore│Appear│
├──────┼──────────┼────────────┼──────┼──────┼──────┼──────────┼──────┤
│    1 │   601899 │ 紫金矿业   │    3 │    1 │    3 │     98.0 │    3 │
│    2 │   001896 │ 豫能控股   │    6 │   15 │   17 │     89.1 │    3 │
...
│   50 │   600900 │ 长江电力   │    - │   14 │    - │     24.6 │    1 │
└──────┴──────────┴────────────┴──────┴──────┴──────┴──────────┴──────┘
```

---

## 字段说明 / Field Description

| 字段/Field | 说明/Description |
|------|------|
| 排名/Rank | 复合热度排名 (1-50) / Composite heat ranking (1-50) |
| 代码/Code | 6位股票代码 / 6-digit stock code |
| 名称/Name | 股票名称 / Stock name |
| 问财/Wencai | 问财人气排名，`-` 表示未上榜 / Wencai popularity rank, `-` means not listed |
| 雪球/Xueqiu | 雪球热榜排名，`-` 表示未上榜 / Xueqiu hot rank, `-` means not listed |
| 东财/Eastmoney | 东方财富人气排名，`-` 表示未上榜 / Eastmoney popularity rank, `-` means not listed |
| 热度分/HeatScore | 复合热度分数 (越高越热) / Composite heat score (higher is hotter) |
| 出现/Appear | 出现在几个平台 (1-3) / Number of platforms appeared (1-3) |

---

## 复合热度算法 / Composite Heat Algorithm

```
热度分 / Heat Score = (基础分/Base Score + 加成分/Bonus Score) / 3.5

基础分 / Base Score：
- 问财排名得分 = 100 - 排名 / Wencai rank score = 100 - rank
- 雪球排名得分 = 100 - 排名 / Xueqiu rank score = 100 - rank  
- 东财排名得分 = 100 - 排名 / Eastmoney rank score = 100 - rank

加成分 / Bonus Score：
- 出现3个平台 / Appears on 3 platforms: +50分/points
- 出现2个平台 / Appears on 2 platforms: +20分/points
- 出现1个平台 / Appears on 1 platform: +0分/points
```

---

## 执行步骤 / Execution Steps

### Step 1：确保依赖已安装 / Install Dependencies

```bash
cd lib
npm install  # 首次运行需要安装 jsdom 和 canvas / First run requires jsdom and canvas
```

### Step 2：构建或运行 / Build or Run

**方式一 / Method 1：直接运行Go源码（推荐）/ Run Go source directly (Recommended)**
```bash
go run main.go

# 或指定参数 / Or specify parameters
go run main.go --top 20 --format json
```

**方式二 / Method 2：编译后运行 / Run after compilation**
```bash
# 构建可执行文件 / Build executable
./build.sh

# 运行 / Run
./dist/stock-heat-rank

# 或指定参数 / Or specify parameters
./dist/stock-heat-rank --top 20 --format json
```

### Step 3：结果解读 / Result Interpretation

1. **出现=3** 的股票：多平台共振，热度最高 / Stocks with **Appear=3**: Multi-platform resonance, highest heat
2. **热度分>80** 的股票：市场关注度极高 / Stocks with **HeatScore>80**: Extremely high market attention
3. **单平台上榜但热度分高**：可能有预期差 / Single platform but high heat score: May have expectation gap

---

## 平台说明 / Platform Description

| 平台/Platform | 数据来源/Data Source | 特点/Characteristics |
|------|----------|------|
| 问财/Wencai | 同花顺问财人气排名 / THS Wencai Popularity Rank | 散户关注度 / Retail investor attention |
| 雪球/Xueqiu | 雪球热榜 / Xueqiu Hot List | 投资者讨论热度 / Investor discussion heat |
| 东财/Eastmoney | 东方财富人气排名 / Eastmoney Popularity Rank | 股吧活跃度 / Guba activity level |

---

## 注意事项 / Notes

1. **网络依赖 / Network Dependency**：需要能正常访问问财、雪球、东财网站 / Requires access to Wencai, Xueqiu, Eastmoney websites
2. **首次运行 / First Run**：需要在 `lib/` 目录执行 `npm install` 安装依赖 / Run `npm install` in `lib/` directory to install dependencies
3. **Node.js 版本 / Node.js Version**：建议使用 Node.js 18+ / Recommended Node.js 18+
4. **Go环境 / Go Environment**：推荐使用 `go run main.go` 直接运行，无需编译 / Recommend running `go run main.go` directly, no compilation needed

---

## 关于 hexin_v.js / About hexin_v.js

`lib/hexin_v.js` 是问财（同花顺）API的签名生成器，用于生成`Hexin-V`请求头。

`lib/hexin_v.js` is the signature generator for Wencai (THS) API, used to generate the `Hexin-V` request header.

**说明 / Notes:**
- 该文件是问财官方前端代码的提取，用于通过其API的反爬验证 / Extracted from Wencai official frontend code, used to pass anti-scraping verification
- 代码经过压缩（非混淆），是标准的前端打包格式 / Code is minified (not obfuscated), standard frontend bundling format
- 仅用于本地签名计算，不会发起任何网络请求 / Only for local signature calculation, no network requests made
- 不会收集或上传任何用户数据 / Does not collect or upload any user data
- 如有安全顾虑，可使用网络抓包工具验证其行为 / If security concerns, use network packet capture tools to verify behavior

---

## 故障排查 / Troubleshooting

| 问题/Problem | 解决方案/Solution |
|------|------|
| 问财采集失败 / Wencai collection failed | 检查 Node.js 依赖是否安装 / Check if Node.js dependencies are installed |
| 雪球采集失败 / Xueqiu collection failed | 网络问题，稍后重试 / Network issue, retry later |
| 东财采集失败 / Eastmoney collection failed | API 变更，需要更新代码 / API changed, need to update code |
| JSON 输出乱码 / JSON output garbled | 终端编码问题，使用 `--format json > output.json` / Terminal encoding issue, use `--format json > output.json` |

---

## 项目结构 / Project Structure

```
skills/stock-heat-rank/
├── SKILL.md          # 技能文档 / Skill documentation
├── build.sh          # 跨平台构建脚本 / Cross-platform build script
├── dist/             # 预编译可执行文件 / Precompiled executables
│   ├── macos-x64
│   ├── macos-arm64
│   ├── linux-x64
│   ├── linux-arm64
│   └── windows-x64.exe
├── lib/
│   ├── hexin_v.js    # Hexin-V 签名生成器 / Hexin-V signature generator
│   └── package.json  # Node.js 依赖 / Node.js dependencies
├── go.mod
└── main.go           # 主程序 / Main program