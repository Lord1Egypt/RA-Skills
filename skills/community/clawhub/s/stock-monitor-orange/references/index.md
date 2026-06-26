# stock-monitor 技能参考文档

## 目录

| 文档 | 说明 |
|------|------|
| [commands.md](./commands.md) | CLI 命令速查，包含所有命令及示例 |
| [config.md](./config.md) | 配置文件结构说明及操作指南 |
| [troubleshooting.md](./troubleshooting.md) | 常见问题排查与解决方案 |

---

## 报告模板

| 文档 | 说明 |
|------|------|
| [reports/templates.md](../reports/templates.md) | 各类报告模板（早报/午报/晚报/盘中） |
| [reports/prompts.md](../reports/prompts.md) | Cron任务标准Prompt模板 |

---

## 快速开始

### 1. 查看帮助
```bash
cd C:\Users\Administrator\.openclaw\skills\stock-monitor\scripts
python stock_monitor.py
```

### 2. 生成综合报告
```bash
python stock_monitor.py report
```

### 3. 管理持仓
```bash
python stock_monitor.py position list              # 查看持仓
python stock_monitor.py position add 600900 6000 28.69  # 添加持仓
```

---

## 核心文件

| 文件 | 位置 |
|------|------|
| 主脚本 | `scripts/stock_monitor.py` |
| 资金流向 | `scripts/stock_capital.py` |
| 配置文件 | `~/.openclaw/stock-*.json` |

---

## 常用命令速查

```bash
# 行情
python stock_monitor.py quote 600900     # 查询行情
python stock_monitor.py index            # 大盘指数

# 分析
python stock_monitor.py analyze 600900   # 技术分析
python stock_monitor.py monitor-a        # A股监控
python stock_monitor.py monitor-hk       # 港股监控
python stock_monitor.py report           # 综合报告

# 持仓
python stock_monitor.py position list    # 查看持仓
python stock_monitor.py position add <code> <qty> <cost>  # 添加持仓
python stock_monitor.py position remove <code>             # 清除持仓

# 交易
python stock_monitor.py trade buy <code> <qty> <price>   # 记录买入
python stock_monitor.py trade sell <code> <qty> <price>  # 记录卖出
python stock_monitor.py trades                              # 交易记录
```

---

## 配置文件位置

| 配置 | 路径 |
|------|------|
| 股票池 | `~/.openclaw/stock-pool.json` |
| 持仓 | `~/.openclaw/stock-positions.json` |
| 交易记录 | `~/.openclaw/stock-trades.json` |
| 预警配置 | `~/.openclaw/stock-alerts.json` |

---

## 定时任务

当前配置的定时任务：

| 任务 | 时间 | 说明 |
|------|------|------|
| 股票早报-A股 | 9:00 (周一至周五) | 生成A股早间报告 |
| 股票早报-港股 | 9:20 (周一至周五) | 生成港股早间报告 |
| 股票午报-A股 | 12:00 (周一至周五) | 生成A股午间报告 |
| 股票午报-港股 | 12:10 (周一至周五) | 生成港股午间报告 |
| A股监控-上午 | 10:05,10:35 (周一至周五) | A股盘中监控 |
| 港股监控-上午 | 10:10,10:35 (周一至周五) | 港股盘中监控 |
| A股监控-下午 | 13:05,13:35 (周一至周五) | A股盘中监控 |
| 港股监控-下午 | 13:10,13:40,14:10,14:40 (周一至周五) | 港股盘中监控 |
| 股票晚报-A股 | 15:20 (周一至周五) | 生成A股晚间报告 |
| 股票晚报-港股 | 16:10 (周一至周五) | 生成港股晚间报告 |

---

## 重要规则

**【强制】数据优先级**

报告中所有"现价/涨跌幅/涨跌额"必须使用脚本返回的数据，禁止使用搜索结果中的价格。

执行顺序：
1. 脚本行情数据（`index`/`monitor-a`/`monitor-hk`）— 权威数据
2. 搜索资讯数据（`web_fetch`）— 仅用于资讯分析
