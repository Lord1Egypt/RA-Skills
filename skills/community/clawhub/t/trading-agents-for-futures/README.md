# Trading_Agents_for_Futures

> 期货六维分析数据引擎 — 纯规则引擎，零 API Key 依赖。通过 AkShare 从公开数据源获取行情，覆盖 48 个期货品种。

## 两种使用模式

| 模式 | 命令 | 适合谁 | 输出 |
|------|------|--------|------|
| **数据模式**（默认） | `python main.py -s RB` | AI Agent / 量化程序 | 纯指标 JSON + 数据缺口报告，不做方向判断 |
| **决策模式** | `python main.py -s RB --decision` | 人类交易者 | 指标 + 数据来源追溯 + 口语化多空辩论 + 风控 + CIO 仓位建议 |

## 快速开始

```bash
python main.py -s RB              # 数据模式：纯指标 JSON
python main.py -s RB --decision   # 决策模式：辩论 + 风控 + CIO 建议
python main.py -s RB,CU,M         # 批量分析
python main.py -s ALL             # 全市场扫描 48 个品种
python main.py -s RB -o out.json  # 额外输出到文件
```

首次运行自动下载约 1 年历史数据（基差模块约 5~10 分钟），后续运行秒级。

## 六维分析能力

| 分析模块 | 计算指标 | 数据来源 |
|---------|---------|---------|
| 技术面分析 | MA5/20/60, EMA20, MACD+Signal+Hist, RSI14, BB, ATR14, 量仓 | 新浪财经 |
| 基差分析 | 现货-期货基差, 基差率, 季节性Z-score, 斜率, Contango/Backwardation | 100ppi.com |
| 期限结构 | 合约价差, 展期结构, spread%, contango/backwardation | AkShare 多策略 |
| 库存仓单 | 库存量, 周/月变化率, 季节性Z-score, 仓单量 | 东方财富 |
| 持仓席位 | 净持仓, 净持仓变化, 加权HHI集中度, 前20多空比, 关键席位追踪 | 三大交易所 |
| 新闻情绪 | 48 词关键词匹配, 利多/利空/中性计数, 情绪比率 | 上海金属网 |

## API 失效时的处理

当数据接口（AkShare）在周末/节假日/不可用时，系统**不会**静默失败：

| 策略 | 说明 |
|------|------|
| **30 天回退** | 逐日回溯找最近的交易日数据，跳过周末 |
| **过期缓存兜底** | 在线 API 全部失败后自动使用本地历史缓存 |
| **Zip 损坏精准清除** | 遇到 AkShare 缓存损坏时按需清理，不滥杀合法缓存 |
| **数据缺口报告** | `coverage` 如实统计可用维度，`data_gap_report` 列出每个缺失维度的 `search_actions`（AI 搜索指令） |
| **AI Fill 槽位** | 每个维度预留 `ai_fill` 字段，AI Agent 搜索后可按 `fillability` 分级回填（`fillable` 正常参与评分，`direction_only` 降权参与） |

## 核心特色

- **零 API Key：** 不调 LLM，纯规则引擎。装完即用，只需要网络（AkShare 下载行情）。
- **四维动态权重：** 品种品类 × 置信度 Sigmoid × 市场状态自适应 × 数据质量折损
- **数据诚实：** `coverage` 从不虚报，缺失维度追加 `warning_flags` + `data_gap_report`
- **信号校正：** 持仓口径矛盾交叉验证、基差斜率×结构矛盾检测、回退数据自动降权
- **永不 null：** 止损止盈始终有值（ATR 动态计算 → 固定值兜底）
- **48 品种覆盖：** Sina 映射 + 品类分类完整，JD/EG/LC/SI 等小品种无遗漏

## 输出结构

数据模式输出的 JSON 包含：

```
{
  "symbol": "JD",
  "coverage": {"total": 6, "available": 4, "missing": ["positioning_analysis", "term_structure_analysis"]},
  "analysis_details": { ... 各维度指标 ... },
  "warning_flags": [{ "skill": "term_structure_analysis", "search_actions": [...] }],
  "data_gap_report": {
    "total_gaps": 2,
    "summary": {"fillable": 1, "direction_only": 1, "not_fillable": 0},
    "gaps": [
      { "skill": "term_structure_analysis", "fillability": "direction_only",
        "search_actions": [{"query": "JD 期货 期限结构 contango", "source": "web"}],
        "ai_fill_schema": { "fields": ["structure"], "cannot_fill": ["prices", "spread_pct"] }
      }
    ]
  }
}
```

## 项目结构

```
Trading_Agents_for_Futures/
├── main.py            # 命令行入口
├── manifest.yaml      # Skill 元数据
├── requirements.txt   # 7 个核心依赖
├── README.md          # 本文件（人类阅读）
├── SKILL.md           # 分析框架知识库 + AI Fill 模板（AI Agent 阅读）
├── setup.py           # 自动安装依赖
├── config/
│   ├── core.yaml      # 默认配置（数据源、风控、日志）
│   └── user.yaml      # 用户覆盖
├── core/
│   ├── core_engine.py # 核心引擎 + 共享工具函数
│   └── data_utils.py  # AkShare 数据获取（6 种数据类型 + 缓存管理）
└── skills/
    ├── technical_analysis.py     # 技术面
    ├── basis_analysis.py         # 基差
    ├── term_structure_analysis.py # 期限结构
    ├── inventory_analysis.py     # 库存仓单
    ├── positioning_analysis.py   # 持仓席位
    ├── news_analysis.py          # 新闻情绪
    └── debate_risk_decision.py   # 辩论风控决策
```

## 配置文件

```yaml
# config/user.yaml
data:
  default_lookback_days: 180
  use_cache: true

risk:
  max_position_per_symbol: 0.20
  atr_stop_multiplier: 2.5
```

## License

MIT
