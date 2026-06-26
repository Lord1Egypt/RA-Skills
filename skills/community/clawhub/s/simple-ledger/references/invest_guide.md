# 投资跟踪指南

## 数据文件

- 交易记录：`~/.openclaw/workspace/data/ledger/investments.csv`
- 价格配置：`~/.openclaw/workspace/data/ledger/prices.json`（需 `--allow-network` 显式允许联网刷新，或手动更新）

> ⚠️ 买入/卖出会持久化写入本地投资账本，必须在交互式终端输入 Y/N 确认；非交互环境不会写入。
> 🌐 行情刷新、代码搜索、按名称查询会联网；命令必须显式添加 `--allow-network`。联网时仅发送证券代码/名称，不发送账本、余额或交易记录。

## 格式说明

投资账本 CSV 格式：
```
# 日期,类型,代码,名称,数量,@单价,金额,账户
买入: 日期,买入,代码,名称,数量,@单价,金额,账户
卖出: 日期,卖出,代码,名称,数量,@单价,金额,账户
```

## 基础操作

### 记录买入

```bash
python scripts/invest.py --buy "沪深300ETF" 510050 1000 3.50 2026-01-15
```

### 记录卖出

```bash
python scripts/invest.py --sell "沪深300ETF" 510050 500 4.00 2026-03-01
```

### 更新当前价格

```bash
python scripts/invest.py --price 510050 3.62
```

### 显式联网刷新行情

```bash
# 联网刷新所有持仓的实时/收盘价（股票/ETF → 新浪，场外基金 → 东方财富）
python scripts/invest.py --refresh --allow-network

# 查询单只证券实时行情。按名称查询会先联网查代码。
python scripts/invest.py --quote 600487 --allow-network
python scripts/invest.py --quote 永赢先锋半导体 --allow-network
```

> ⚠️ 股票/ETF 使用新浪财经接口，场外基金使用东方财富净值接口。联网查询会向第三方发送证券代码/名称；不会发送个人账本数据。未加 `--allow-network` 时命令会拒绝联网。

### 修改成本价

```bash
python scripts/invest.py --cost 600487 75.631
```

> 修改最近一笔买入的单价，系统自动重算总成本。

### 查看持仓

```bash
python scripts/invest.py --portfolio
```

### 单只收益分析

```bash
python scripts/invest.py --return 510050
```

### 汇总收益

```bash
python scripts/invest.py --summary
```

### 查看交易记录

```bash
python scripts/invest.py --list
python scripts/invest.py --list 510050  # 单只历史
```

### 确认机制说明

```bash
python scripts/invest.py --buy "沪深300ETF" 510050 100 3.50 2026-01-15
python scripts/invest.py --sell "沪深300ETF" 510050 500 4.00 2026-03-01
```

> ⚠️ **所有买入/卖出操作必须经过交互式确认（Y/N），不存在跳过确认的快捷参数。**
> 非交互环境会直接取消写入，这是为了防止 Agent 误操作或 prompt 注入导致错误的金融记录。金融操作必须有安全确认环节。

> ⚠️ **数据隔离：** 投资记录仅写入 investments.csv，与日常账本（default.csv）完全独立。

## 收益计算方式

采用**平均成本法**（成本法）：
- 买入时记录成本
- 卖出时按平均成本计算已实现盈亏
- 持仓盈亏 = 当前市值 - 持仓成本
- 总收益 = 持仓盈亏 + 已实现盈亏

## 实用建议

1. **先有应急基金再投资** — 应急金没到位之前不碰高风险投资
2. **用价格配置追踪市价** — 每次 `--buy`/`--sell` 会自动更新价格，也可以手动 `--price` 更新
3. **定期更新价格** — 持仓盈亏需要当前价格；联网更新必须显式添加 `--allow-network`
4. **收益跟踪** — 使用 `--summary` 查看投资总体情况
5. **ETF 适合大多数人** — 沪深 300、中证 500、纳指 ETF 是最简单的选择

## 风险提示

- 投资有风险，入市需谨慎
- 历史收益不代表未来表现
- 本工具仅供记录，不构成投资建议
- 大额投资决策建议咨询专业人士