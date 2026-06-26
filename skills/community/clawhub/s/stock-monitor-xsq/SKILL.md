---
name: stock-monitor
description: 股票监控分析技能 - 自定义股票池监控、实时行情、技术指标分析、涨跌趋势预测、信号提醒
version: 1.2.1
---

# Metadata
```yaml
openclaw:
  requires:
    files:
      - ~/.openclaw/stock-pool.json        # 股票监控池配置（公开数据）
      - ~/.openclaw/stock-positions.json   # 持仓记录（个人数据，仅本地使用）
      - ~/.openclaw/stock-trades.json      # 交易记录（个人数据，仅本地使用）
      - ~/.openclaw/stock-alerts.json      # 预警配置
      - ~/.openclaw/cron/jobs.json         # 定时任务配置
    apis:
      - 腾讯行情API (qt.gtimg.cn)         # 实时行情（主要数据源）
      - 新浪财经API (sina.com.cn)          # 实时行情（备用数据源）
      - 东方财富API (eastmoney.com)        # K线数据、资讯（主备双通道）
      - Agent Reach (Jina/Exa)            # 资讯获取备选（当Tavily额度满时）
    credentials:
      - Tavily API Key (可选，额度满时使用Agent-Reach替代)
    network: true
    python: true
```

# Stock Monitor - 股票监控分析技能


---

## 核心特色

- 多维度技术分析：ADX趋势、BOLL轨道、MACD/KDJ/RSI/OBV/DMI/WR指标
- 资讯情感分析：东方财富+新浪财经+雪球
- 持仓智能管理：自动追踪成本、盈亏、FIFO同步
- **买卖点位建议**：基于支撑/阻力位+BOLL+均线的精确入场/出场/止损/目标价位
- 中国股市习惯：🔴红色=上涨/盈利 | 🟢绿色=下跌/亏损
- **数据源自动降级**：行情/K线失败自动切换备用源，告别数据中断

---

## 目录结构

```
stock-monitor/
├── SKILL.md                    本文件
├── references/
│   ├── commands.md             CLI命令速查
│   ├── config.md               配置文件说明
│   ├── index.md                指标说明
│   ├── scheduled-tasks.md      定时任务配置
│   └── troubleshooting.md      故障排查
├── reports/
│   ├── prompts.md              Cron任务Prompt模板
│   └── templates.md            报告模板（完整模板）
└── scripts/
    ├── stock_monitor.py        主监控脚本
    └── stock_capital.py        资金流向脚本
```

---

## 数据源降级机制（v1.1+）

为应对数据源不稳定，脚本内置多级自动降级：

| 数据类型 | 主数据源 | 备用① | 备用② | 最终保底 |
|---------|---------|-------|-------|---------|
| A股实时行情 | 腾讯 qt.gtimg.cn | 新浪 hq.sinajs.cn | — | 返回空 |
| 港股实时行情 | 腾讯 qt.gtimg.cn | 新浪 hq.sinajs.cn | — | 返回空 |
| A股K线 | 东方财富 push2his | 新浪财经 | — | 返回空 |
| 港股K线 | 腾讯 web.ifzq.gtimg.cn | 东方财富 push2his | 实时行情构造单日K线 | 返回空 |
| 大盘指数 | 腾讯 qt.gtimg.cn | 新浪 hq.sinajs.cn | — | 返回空 |

**降级标识**：当触发备用源时，脚本会打印 `[降级]` 或 `[保底]` 日志，便于排查。

---

## CLI 命令

> 工作目录：`scripts` | 格式：`python stock_monitor.py <command> [args]`

### 行情与指数
| 命令 | 说明 |
|------|------|
| `quote <code>` | 查询单只股票行情 |
| `index` | 查询大盘指数 |

### 技术分析
| 命令 | 说明 |
|------|------|
| `analyze <code>` | 分析股票技术指标 |
| `monitor-a` | 监控所有A股 |
| `monitor-hk` | 监控所有港股 |

### 综合报告
| 命令 | 说明 |
|------|------|
| `report` | 生成完整综合报告 |
| `report-a` | 生成A股综合报告 |
| `report-hk` | 生成港股综合报告 |

### 持仓管理
| 命令 | 说明 |
|------|------|
| `position add <code> <qty> <cost>` | 添加/更新持仓 |
| `position remove <code>` | 清除持仓 |
| `position list` | 查看持仓 |

### 交易记录
| 命令 | 说明 |
|------|------|
| `trade buy <code> <qty> <price>` | 记录买入 |
| `trade sell <code> <qty> <price>` | 记录卖出 |
| `trades [code]` | 查看交易记录 |

---

## 重要规则

### 数据优先级（强制）
1. 脚本行情数据（`index`/`monitor-a`/`monitor-hk`）— 权威数据
2. 搜索资讯数据（`web_fetch`）— 仅用于资讯分析

**【强制】报告中所有"现价/涨跌幅/涨跌额"必须使用脚本返回的数据，禁止使用搜索结果中的价格。**

### 技术指标（必须包含）
每只股票：现价、涨跌幅、MA均线多空、MACD状态、KDJ状态、RSI数值、BOLL位置、OBV背离、DMI趋势、WR威廉、综合信号

### 综合信号评级
| 评分差 | 信号 |
|--------|------|
| buy > sell + 3 | ⭐⭐⭐ 强烈买入 |
| buy > sell | ⭐⭐ 建议买入 |
| abs差 ≤ 3 | ⚪ 观望 |
| sell > buy | ⭐ 建议卖出 |
| sell > buy + 3 | ⭐⭐ 强烈卖出 |

### 买卖点位计算规则
| 场景 | 买入点位 | 买入区间 | 卖出点位 | 卖出区间 | 止损位 | 目标位 |
|------|---------|---------|---------|---------|--------|--------|
| 回踩支撑 | 支撑位 | 支撑×0.98~1.02 | - | - | 支撑下方3% | 阻力位/BOLL上轨 |
| 突破阻力 | 突破后确认 | 阻力~阻力×1.02 | - | - | 阻力下方3% | 上一阻力位 |
| RSI超卖 | BOLL下轨/支撑 | 下轨×0.98~1.02 | - | - | 前低下方3% | BOLL上轨/阻力位 |
| RSI超买 | - | - | BOLL上轨/阻力位 | 上轨×0.97~1.01 | - | - |
| MACD死叉 | - | - | 短线阻力位 | 阻力×0.97~1.01 | - | - |

**计算依据**：
- 支撑位：近30日低点、BOLL下轨、60日均线
- 阻力位：近30日高点、BOLL上轨、近期反弹高点
- 止损：支撑/均线下方3%（保守可设2%）
- 目标位：阻力位、BOLL上轨、量度涨幅（前一高低点差）
- **买入区间**：在点位附近±2%范围分批建仓
- **卖出区间**：在点位附近±3%范围分批止盈

---

## 报告模板

详见 `reports/templates.md`

### 报告生成流程
1. `python stock_monitor.py index` 获取大盘指数
2. 读取 `~/.openclaw/stock-pool.json` 获取股票列表
3. `python stock_monitor.py monitor-a/hk` 获取技术面数据
4. `web_fetch` 获取资讯（优先东方财富/新浪/雪球）
5. 生成报告（价格数据必须用步骤3返回的数据）
6. 推送至飞书群聊

---

## 配置文件

| 文件 | 路径 |
|------|------|
| 股票池 | `~/.openclaw/stock-pool.json` |
| 持仓记录 | `~/.openclaw/stock-positions.json` |
| 交易记录 | `~/.openclaw/stock-trades.json` |
| 预警配置 | `~/.openclaw/stock-alerts.json` |
| Cron任务 | `~/.openclaw/cron/jobs.json` |

---

## 使用提示

- 技术指标有滞后性，用于确认趋势而非预测
- 多条件共振更可靠，单一指标容易假信号
- 动态止盈：回撤5%减仓、10%清仓（建议，根据市场灵活调整）
- **核心原则**：预警系统目标是"不错过大机会，不犯大错误"
