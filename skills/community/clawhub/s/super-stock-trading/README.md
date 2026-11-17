# 超级股票操盘 Skill（super-stock-trading）

> 遵循 [agentskills.io](https://agentskills.io) 规范的 A 股全流程操盘智能体 Skill 包。整合 **137 个细粒度 Skills** 与 **31 位数字人专家**，内置《短线金手》七册实战战法体系（私募盈利系统/经典形态/涨停狙击/急速拉升/分时图/T+0/K线精通），覆盖盘前分析、盘中决策、盘后复盘、选股、持仓体检、月度组合管理等完整投资闭环。

---

## 一、功能介绍

本 Skill 包面向 A 股（沪深京）个人投资者，将「投研—交易—风控—复盘」四大环节抽象为可被智能体调用的能力组合，核心特性：

- **全流程覆盖**：从盘前 07:00 隔夜复盘，到盘后 22:00 次日计划，再到周末选股、月末组合再平衡，形成闭环。
- **137 个细粒度 Skill**：按 16 大类组织（GitHub 开源、Serenity 产业链、市场分析、资金面、题材产业链、选股、个股研究、估值财务、财报、公告事件、交易执行、日常盘面、周期风控、社区、辅助、短线战法），每个均声明 `tier`（T1–T4）、`data_source`、`trigger`。其中「短线战法」类（20 个）沉淀自《短线金手》七册，主攻 1~20 日及日内/T+1 短线决策。
- **31 位数字人专家**：涵盖价值投资（巴菲特、芒格）、技术操盘（王开、赵哲）、产业链（Serenity白毛股神）、宏观策略（陶川、刘高畅）、量化风控（塔勒布、聂方义）、配置理财（纳瓦尔、望京博格）、短线战术派（吴国平、陈旭、王炳洁、曹芝烨、杨涛）等流派，编排层按任务类型召集「圆桌讨论」。
- **四层架构**：数据层 → Skill 层 → 专家层 → 编排层，职责清晰、可独立替换。
- **风控前置**：内置 7 条风控规则（个股止损 5%、组合止损 8%、单只仓位上限 30%、行业集中度 50%、黑天鹅熔断、事件前置审查、流动性约束），任何交易动作执行前必须通过闸门校验。
- **多数据源**：默认使用开源 `akshare`，可叠加 `wind_aifin_market`、`tushare` 提升数据质量，支持主备降级。
- **3 份全球财富报告**：内置莱坊 2026 财富报告、瑞银 2026 全球财富报告、BCG 2026 全球财富报告（大重构），为宏观资产配置提供顶层视野。

> 触发关键词：股票操盘、盘前分析、盘后复盘、选股、持仓体检、月度组合管理、仓位管理、止损止盈、板块轮动、题材挖掘、龙头战法、财报季、公告解读、资金面、北向资金、龙虎榜、风险体检、组合再平衡、定投、指数基金、期权对冲、产业链、护城河、估值、异动、全球财富、资产配置、短线、打板、涨停、集合竞价、分时图、T+0、主力吸筹、仙人指路、黄金十字、梅开二度、大长腿、黄金分割、急速拉升。

---

## 二、安装方法

### 前置依赖
- Python 3.9+
- Node.js 18+（如需运行 Skill 包内脚本）
- 可选数据源账号：Wind 终端 / Tushare Pro Token

### 步骤
1. **克隆仓库**
   ```bash
   git clone https://github.com/<owner>/super-stock-trading-skill.git
   cd super-stock-trading-skill
   ```

2. **安装 Python 依赖**
   ```bash
   python -m venv ~/.claude/stock-skills-venv
   source ~/.claude/stock-skills-venv/bin/activate
   pip install akshare tushare pywind pandas numpy
   ```

3. **注册 Skill 到 Agent 平台**
   将本目录作为 Skill 包路径注册到支持 agentskills.io 规范的智能体平台（如 Claude / ClawHub）。平台会读取根目录 `SKILL.md` 作为入口。

4. **配置 `config.json`**
   填入 API Key、自选股、风控参数与财富报告配置（详见第五节）。

5. **（可选）一键安装脚本**
   ```bash
   bash scripts/install.sh   # 交互式生成 config.json 并安装依赖
   ```

---

## 三、目录结构

```
super-stock-trading-skill/
├── SKILL.md                          # Skill 入口（frontmatter + 架构 + 时间表 + 风控）
├── README.md                         # 本说明文档
├── config.json                       # 数据源 / API Key / 自选股 / 风控 / 财富报告配置
├── references/                       # 参考注册表与详细文档
│   ├── skills_registry.json          # 137 个 Skill 注册表（name/category/tier/data_source/trigger）
│   ├── experts_registry.json         # 31 位数字人专家注册表（role/research_area/priority）
│   ├── short_line_mastery.md         # 《短线金手》七册实战战法知识库（v1.1.0 新增）
│   ├── daily_workflow.md             # 盘前/盘中/盘后/周末/月度/事件驱动六阶段工作流
│   ├── risk_rules.md                 # 7 条风控规则详表（触发条件/执行动作/关联 Skill）
│   └── wealth_reports/               # 3 份 2026 全球财富报告（莱坊/瑞银/BCG）
│       ├── 莱坊2026财富报告_中文版.html
│       ├── 瑞银2026全球财富报告_中文版.html
│       ├── BCG_2026全球财富报告_中文版.html
│       └── README.md                 # 财富报告索引与使用指南
├── scripts/                          # 运维脚本
│   ├── install.sh                    # 一键安装
│   ├── daily_pipeline.py             # 日常 Pipeline 运行器
│   ├── data_fetcher.py               # 数据获取层（三源降级 + 缓存）
│   └── risk_manager.py               # 风险管理引擎（7 条规则）
├── templates/                        # 报告模板（盘前/盘后/周报/月报/交易日志/日报）
├── reports/                          # 运行时输出的复盘与计划报告
└── assets/                           # 配置模板与素材
```

---

## 四、使用示例

### 示例 1：盘前分析（07:00–09:15）
```text
用户：今天盘前帮我分析一下，重点看看我的持仓有没有风险。
Agent：
  1. market-overview-skill —— 拉取隔夜外盘与要闻
  2. announcement-monitor-skill —— 扫描持仓相关公告
  3. portfolio-risk-monitor —— 持仓体检，输出风险评分
  4. 调度「沃伦·巴菲特 + 塔勒布」圆桌，给出当日操作建议
  5. 7 条风控闸门校验后输出「盘前策略卡」
```

### 示例 2：选股（周末）
```text
用户：周末帮我更新一下选股池，要价值+成长兼顾。
Agent：
  1. multi-factor-stock-screening —— 多因子初筛
  2. valuation-multi-model-skill —— 估值校验
  3. 调度「查理·芒格 + 望京博格」圆桌
  4. watchlist-monitoring —— 写入选股池并设置监控
```

### 示例 3：持仓体检 + 月度组合管理
```text
用户：月底了，做一次持仓体检和组合再平衡。
Agent：
  1. portfolio-risk-monitor + cycle-position-assessment —— 风险与周期定位
  2. portfolio-rebalance-skill —— 生成再平衡方案
  3. position-sizing-calculator —— 重算仓位
  4. 调度「策略分析师 + 纳瓦尔」圆桌
  5. 风控闸门校验后输出「月度组合报告」
```

---

## 五、配置说明

所有配置集中在根目录 `config.json`，关键字段：

| 配置块 | 字段 | 说明 |
|-------|------|------|
| `data_sources` | `akshare` / `wind_aifin_market` / `tushare` | 三大数据源开关、优先级与限频 |
| `api_keys` | `wind_api_key` / `tushare_token` / `alphavantage_api_key` | API Key 占位符，首次使用须填入真实值 |
| `watchlist` | `stocks` / `indices` / `themes` | 自选股、关注指数、关注题材占位 |
| `risk_control` | `stop_loss` / `portfolio_stop_loss` / `single_position_limit` 等 | 风控参数（止损 5%、组合止损 8%、单只仓位上限 30% 等） |
| `wealth_reports` | `directory` / `reports` / `auto_reference` | 3 份全球财富报告路径与自动引用开关 |

> 安全提示：`config.json` 中的 API Key 为占位符，请勿提交真实密钥到公开仓库；建议使用环境变量或 `.env` 覆盖。

---

## 六、风控提示

- 本 Skill 默认开启 7 条风控规则，可在 `config.json` → `risk_control` 调整阈值或临时关闭（不建议）。
- **个股止损 5%**、**组合止损 8%** 为默认值，激进型投资者可适当放宽，但不应突破单只仓位 30% 与行业集中度 50% 的硬性上限。
- **黑天鹅熔断**触发后会暂停新开仓并启动对冲评估，需人工确认后方可解除。
- **事件前置审查**：重大公告/异动后 30 分钟内禁止对相关标的新增仓位，须先完成事件评估。
- 所有交易建议均需用户人工二次确认，本 Skill 不提供直接下单通道。

---

## 免责声明

本 Skill 仅供学习与研究使用，**不构成任何投资建议**。A 股市场有风险，投资需谨慎。所有交易决策与盈亏由用户自行承担。请在合法合规的前提下使用，并遵守所在地区的证券法律法规。

---

## 许可证

MIT License © super-stock-trading-team
