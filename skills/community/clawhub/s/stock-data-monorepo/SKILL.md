---
name: stock-data-monorepo
description: |
  A 股数据查询技能集合，包含 4 个子技能：cn-stock-volume（成交量）、stock-top-gainers（涨幅排名）、ths-stock-themes（题材概念）、stock-theme-events（题材事件）。
  
  **触发场景**:
  - 作为 stock-daily-report 的数据源依赖
  - 单独查询股票数据时

metadata:
  {
    "emoji": "📈",
    "requires": { "bins": ["python3"], "tools": ["browser"] },
    "install": [
      { "id": "akshare", "kind": "pip", "package": "akshare" },
      { "id": "sentence-transformers", "kind": "pip", "package": "sentence-transformers" },
      { "id": "scikit-learn", "kind": "pip", "package": "scikit-learn" }
    ],
    "sub_skills": ["cn-stock-volume", "stock-top-gainers", "ths-stock-themes", "stock-theme-events"]
  }
---

# Stock Data Monorepo - A 股数据查询技能集合

统一的 A 股数据查询技能集合，包含 4 个相关技能。

## 📦 包含的技能

| 技能名称 | 功能 | 版本 |
|----------|------|------|
| **cn-stock-volume** | 获取四市（沪市/深市/创业板/北交所）成交金额、放缩量、涨跌家数 | v1.2.2 |
| **stock-top-gainers** | 获取近 10 日个股涨幅排名（前 20 只，排除 ST） | v1.0.0 |
| **ths-stock-themes** | 获取同花顺个股题材/概念板块和人气排名数据 | v1.0.0 |
| **stock-theme-events** | 获取 A 股市场炒作题材对应的真实新闻事件 | v1.0.3 |

## 🚀 使用方式

本 Monorepo 是一个技能集合，建议在 `stock-daily-report` 等上层技能中通过调用各子技能的脚本使用：

```bash
# 设置路径变量（推荐）
STOCK_DATA_PATH=~/.hermes/skills/stock-data-monorepo

# 查询四市成交量
python3 $STOCK_DATA_PATH/cn-stock-volume/scripts/fetch_data.py

# 获取近 10 日涨幅排名
python3 $STOCK_DATA_PATH/stock-top-gainers/scripts/fetch_gainers.py

# 查询股票题材
python3 $STOCK_DATA_PATH/ths-stock-themes/scripts/fetch_themes.py [股票代码]

# 生成题材事件报告
python3 $STOCK_DATA_PATH/stock-theme-events/scripts/generate_report.py
```

## 📊 技能依赖关系

```
stock-daily-report (上层应用)
    ├── cn-stock-volume ⭐ (必需 - 指数数据)
    ├── stock-top-gainers ⭐ (必需 - 涨幅排名)
    ├── ths-stock-themes ⭐ (必需 - 题材数据)
    └── stock-theme-events (可选 - 深度分析)
```

## 目录结构

```
stock-data-monorepo/
├── SKILL.md                    # 本文件
├── cn-stock-volume/           # 成交量数据
│   ├── SKILL.md
│   └── scripts/
│       └── fetch_data.py
├── stock-top-gainers/         # 涨幅排名
│   ├── SKILL.md
│   └── scripts/
├── ths-stock-themes/          # 题材概念
│   ├── SKILL.md
│   └── scripts/
└── stock-theme-events/        # 题材事件
    ├── SKILL.md
    └── scripts/
```

## ⚠️ 注意事项

1. **数据时效性**：所有数据均为实时或 T+1 数据，建议在报告中注明数据获取时间
2. **ST 股票**：涨幅排名自动排除 ST 股票，其他技能需手动过滤
3. **依赖安装**：
   ```bash
   pip install akshare sentence-transformers scikit-learn
   ```
4. **browser 工具**：部分技能需要 browser 工具访问网页获取数据

## 📝 更新日志

### v1.2.3 (2026-04-16)
- 添加 YAML frontmatter 元数据
- 修正硬编码路径为可配置路径

### v1.2.2 (2026-03-21)
- **cn-stock-volume**: 修复非交易日数据处理逻辑，自动使用最近交易日数据
- **stock-top-gainers**: 新增完整脚本（browser_fetch.py, fetch_gainers.py, parse_snapshot.py）
- **stock-theme-events**: 新增 run_full_analysis.py 完整分析脚本

### v1.2.1 (2026-03-21)
- Monorepo 合并，统一目录结构