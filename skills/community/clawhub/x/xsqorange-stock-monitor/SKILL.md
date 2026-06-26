---
name: stock-monitor
description: 股票监控分析技能 - 自定义股票池监控、实时行情、技术指标分析、涨跌趋势预测、信号提醒
---

# Stock Monitor - 股票监控分析技能

> 版本：1.2.2 | 更新：优化frontmatter格式，A股/港股监控任务分离

---

## 核心特色

- 多维度技术分析：ADX趋势、BOLL轨道、MACD/KDJ/RSI/OBV/DMI/WR指标
- 资讯情感分析：东方财富+新浪财经+雪球
- 持仓智能管理：自动追踪成本、盈亏、FIFO同步
- 中国股市习惯：🔴红色=上涨/盈利 | 🟢绿色=下跌/亏损

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
