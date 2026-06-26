# Stock Data Monorepo - A 股数据查询技能集合

统一的 A 股数据查询技能集合，包含 4 个相关技能。

## 📦 包含的技能

| 技能名称 | 功能 | 版本 |
|----------|------|------|
| **cn-stock-volume** | 获取四市（沪市/深市/创业板/北交所）成交金额、放缩量、涨跌家数 | v1.2.0 |
| **stock-top-gainers** | 获取近 10 日个股涨幅排名（前 20 只，排除 ST） | v1.0.0 |
| **ths-stock-themes** | 获取同花顺个股题材/概念板块和人气排名数据 | v1.0.0 |
| **stock-theme-events** | 获取 A 股市场炒作题材对应的真实新闻事件 | v1.0.3 |

## 📁 目录结构

```
stock-data-monorepo/
├── README.md                    # 本文件
├── cn-stock-volume/             # 成交量查询技能
│   ├── SKILL.md
│   ├── package.json
│   ├── _meta.json
│   ├── scripts/
│   │   └── fetch_volume.py
│   └── ...
├── stock-top-gainers/           # 涨幅排名技能
│   ├── SKILL.md
│   └── ...
├── ths-stock-themes/            # 同花顺题材技能
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── fetch_themes.py
│   │   └── fetch_popularity.py
│   └── ...
└── stock-theme-events/          # 题材事件分析技能
    ├── SKILL.md
    ├── package.json
    ├── _meta.json
    ├── config/
    │   └── theme_synonyms.json
    ├── scripts/
    │   ├── cluster_themes.py
    │   ├── search_news.py
    │   └── generate_report.py
    └── ...
```

## 🚀 安装方式

### 方式 1：整体安装（推荐）

```bash
# 克隆整个 Monorepo
cd ~/.jvs/.openclaw/workspace/skills/
# stock-data-monorepo 已存在
```

### 方式 2：单独使用某个技能

每个技能都是独立的，可以单独调用：

```bash
# cn-stock-volume
python3 ~/.jvs/.openclaw/workspace/skills/stock-data-monorepo/cn-stock-volume/scripts/fetch_volume.py

# stock-top-gainers
# 使用 browser 工具访问同花顺问财

# ths-stock-themes
python3 ~/.jvs/.openclaw/workspace/skills/stock-data-monorepo/ths-stock-themes/scripts/fetch_themes.py [股票代码]

# stock-theme-events
python3 ~/.jvs/.openclaw/workspace/skills/stock-data-monorepo/stock-theme-events/scripts/generate_report.py
```

## 📊 技能依赖关系

```
stock-daily-report (上层应用)
    ├── cn-stock-volume ⭐
    ├── stock-top-gainers ⭐
    ├── ths-stock-themes ⭐
    └── stock-theme-events (可选，深度分析时使用)
```

## 🔄 版本历史

### 2026-03-21 - v1.2.2

- **cn-stock-volume**: 修复非交易日数据处理逻辑，自动使用最近交易日数据
- **stock-top-gainers**: 新增完整脚本（browser_fetch.py, fetch_gainers.py, parse_snapshot.py）
- **stock-theme-events**: 新增 run_full_analysis.py 完整分析脚本

### 2026-03-21 - Monorepo 合并

- 合并原有多个重复的 Monorepo（cn-stock-volume、stock-theme-events）
- 统一目录结构，消除重复文件
- 保留所有技能的最新版本

### 各技能独立版本

- **cn-stock-volume**: v1.2.2 (修复非交易日处理 + 四市成交 + 涨跌家数)
- **stock-top-gainers**: v1.0.0 (近 10 日涨幅前 20)
- **ths-stock-themes**: v1.0.0 (同花顺题材 + 人气排名)
- **stock-theme-events**: v1.0.3 (题材 - 事件关联分析，已发布 ClawHub)

## 📝 使用示例

### 示例 1：查询今日四市成交

```bash
python3 ~/.jvs/.openclaw/workspace/skills/stock-data-monorepo/cn-stock-volume/scripts/fetch_volume.py
```

### 示例 2：获取近 10 日涨幅前 20

使用 browser 工具访问：
```
https://www.iwencai.com/unifiedwap/result?w=近 10 日涨幅排名
```

### 示例 3：查询股票题材

```bash
python3 ~/.jvs/.openclaw/workspace/skills/stock-data-monorepo/ths-stock-themes/scripts/fetch_themes.py 600519
```

### 示例 4：生成题材事件报告

```bash
# 在 stock-daily-report skill 中调用
python3 ~/.jvs/.openclaw/workspace/skills/stock-data-monorepo/stock-theme-events/scripts/generate_report.py \
  --themes clustered_themes.json \
  --news theme_news.json \
  --output ~/Desktop/A 股每日复盘/theme-events-2026-03-21.md
```

## ⚠️ 注意事项

1. **数据时效性**：所有数据均为实时或 T+1 数据，建议在报告中注明数据获取时间
2. **ST 股票**：涨幅排名自动排除 ST 股票，其他技能需手动过滤
3. **依赖安装**：
   ```bash
   pip install akshare sentence-transformers scikit-learn
   ```
4. **browser 工具**：部分技能需要 browser 工具访问网页获取数据

## 📞 问题反馈

- GitHub: https://github.com/shinelp100/stock-data-monorepo/issues
- ClawHub: https://clawhub.ai/shinelp100/stock-data-monorepo

---

**最后更新**：2026-03-21

## 更新日志

### v1.2.3 (2026-03-21)
- v1.2.2: 修复非交易日数据处理，新增 stock-top-gainers 完整脚本，完善 stock-theme-events 分析功能

### v0.1.0 (2026-03-21)
- v1.2.2: 修复非交易日数据处理，新增 stock-top-gainers 完整脚本，完善 stock-theme-events 分析功能
