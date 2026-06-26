---
name: portfolio-assistant
description: 专门用于查询用户持仓、盈亏情况和历史交易记录的助手。
metadata: {"openclaw": {"requires": {"env": ["STOCK_API_KEY"]}}}
user-invocable: true
---

# 投资组合助手 (Portfolio Assistant)

专门用于查询用户持仓、盈亏情况和历史交易记录的助手。

## 认证与基础配置
- 环境变量: `STOCK_API_KEY`
- Base URL: 从 `config.sh` 中读取 `$STOCK_BASE_URL`（默认 `https://www.mystockearning.cn`，切换域名只需改 `config.sh`）

## API 指令清单

### 获取当前持仓
当用户问 "我现在的苹果股票赚了多少钱？" 或 "查看我的美股持仓" 时：
- 获取特定股票持仓：执行 `./scripts/get_position_by_symbol.sh`（需要设置 `SYMBOL`）
- 获取某市场的所有持仓（按盈亏比例降序）：执行 `./scripts/get_positions_by_market_sorted.sh`（需要设置 `MARKET`）

### 获取交易记录
当用户问 "我最近一个月买过哪些美股？" 时：
- 执行 `./scripts/get_trades.sh`（需要设置 `MARKET`、`TRADE_TYPE`）

### 获取投资表现摘要
当用户问 "我账户总资产多少？" 或 "总盈亏如何？" 时：
- 获取收益摘要：执行 `./scripts/get_summary.sh`

## 执行规则
1. 解析用户指令。
2. **货币显示规则**：在回复任何持仓市值、成本或盈亏金额时，必须根据该股票或账户所在的市场显示正确的货币符号或单位：
   - `cn_a` (A股): `¥` 或 `元` (人民币 CNY)
   - `hk` (港股): `HK$` 或 `港元` (港币 HKD)
   - `us` (美股): `$` 或 `美元` (美元 USD)
3. 执行 `curl` 请求。
4. 从响应中提取关键字段（如 `profit_loss`, `profit_loss_percent`, `market_value`）。
5. 使用带颜色的 Markdown 格式或表格输出结果（如：盈利标红或绿，根据当地市场习惯），金额必须保留两位小数并带上正确的货币单位。
