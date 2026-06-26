---
name: stock-portfolio
description: 股票组合管理与预警技能。支持 A 股/港股/美股行情查询、持仓跟踪、收益计算、价格预警、每日推荐。使用免费 API（腾讯财经），数据本地存储。
---

# 股票组合管理技能

## 核心功能

### 1. 📊 行情查询
- 实时股价、涨跌幅、成交量
- 支持 A 股（600xxx/000xxx/300xxx）、港股（00700）、美股（AAPL）

### 2. 💼 持仓管理
- 记录买入价、持仓数量、加仓/减仓
- 自动计算当前市值、盈亏金额、盈亏比例
- 持仓数据本地存储（JSON 文件）

### 3. 🔔 价格预警
- 设置目标价/涨跌幅阈值
- 主动查询时检查预警状态
- 可选 cron 定时监控

### 4. 💡 每日推荐
- 每日 5 只股票推荐
- 基于技术指标（涨跌幅、振幅、成交量）+ 基本面（行业龙头）
- 多线程获取行情数据，快速响应
- 推荐列表可配置（修改 STOCK_POOL）

## 快速开始

### 查询股价
```bash
# 使用脚本查询
python scripts/stock_fetch.py 600519
python scripts/stock_fetch.py AAPL
```

### 管理持仓
```bash
# 添加持仓
python scripts/portfolio_manager.py add --symbol 600519 --price 1500 --shares 100

# 查看持仓
python scripts/portfolio_manager.py list

# 计算收益
python scripts/portfolio_manager.py summary
```

### 设置预警
```bash
# 设置价格预警
python scripts/portfolio_manager.py alert --symbol 600519 --target 1600

# 查看预警
python scripts/portfolio_manager.py alerts
```

## 数据源

### 腾讯财经 API（免费、无需 key）

**A 股格式：** `sh600519`, `sz000001`, `sz300750`
**港股格式：** `hk00700`
**美股格式：** `usAAPL`, `usTSLA`

**接口：** `http://qt.gtimg.cn/q={symbol}`

**返回示例：**
```
v_sh600519="1~贵州茅台~600519~1408.81~1445.00~1433.33~..."
```

字段说明（~分隔）：
- 字段 0: 未知
- 字段 1: 股票名称
- 字段 2: 股票代码
- 字段 3: 当前价格
- 字段 4: 昨日收盘价
- 字段 5: 今日开盘价
- 字段 6: 成交量（手）
- 字段 31: 涨跌额
- 字段 32: 涨跌幅%
- 字段 33: 今日最高价
- 字段 34: 今日最低价
- 字段 47: 成交额（万）

详细 API 文档见 [references/api_docs.md](references/api_docs.md)

## 数据存储

持仓数据存储在：`~/.openclaw/workspace/skills/stock-portfolio/data/`

- `holdings.json` - 持仓记录
- `alerts.json` - 预警设置
- `history.json` - 查询历史（可选）

## 每日推荐逻辑

推荐策略（见 [references/recommendation_strategy.md](references/recommendation_strategy.md)）：

1. **技术面筛选**（60% 权重）
   - 涨跌幅：温和上涨（0-3%）得分最高
   - 振幅：适度活跃（2-6%）得分高
   - 成交量：大于 500 万股加分

2. **基本面筛选**（40% 权重）
   - 行业龙头优先
   - 业绩稳定增长
   - 市值适中

3. **随机因子**
   - 基于日期种子，确保同一天推荐一致
   - 增加多样性，避免推荐过于集中

推荐结果每日更新，多线程获取行情数据（约 3-5 秒完成）。

## 使用示例

**用户：** "查询茅台今天的股价"
**操作：** 调用 `stock_fetch.py sh600519`，返回实时行情

**用户：** "我买了 100 股茅台，成本 1500"
**操作：** 调用 `portfolio_manager.py add --symbol sh600519 --price 1500 --shares 100`

**用户：** "我的持仓收益怎么样"
**操作：** 调用 `portfolio_manager.py summary`，获取当前股价并计算盈亏

**用户：** "茅台涨到 1600 提醒我"
**操作：** 调用 `portfolio_manager.py alert --symbol sh600519 --target 1600`

**用户：** "今天有什么股票推荐"
**操作：** 调用 `scripts/daily_picks.py`，返回 5 只推荐股票

## 定时任务（可选）

配置 cron 实现：
- 每日 9:00 推送推荐股票
- 每 30 分钟检查预警条件

见 [references/cron_setup.md](references/cron_setup.md)

## 注意事项

1. **数据延迟**：免费 API 有 15 分钟延迟（A 股实时，港股/美股延迟）
2. **交易时间**：非交易时间返回收盘价
3. **复权处理**：当前不支持复权，分红/拆股需手动调整成本
4. **数据备份**：定期备份 `data/` 目录

## 扩展方向

- 接入更多数据源（东方财富、Yahoo Finance）
- 支持基金、债券
- K 线图生成
- 回测功能
