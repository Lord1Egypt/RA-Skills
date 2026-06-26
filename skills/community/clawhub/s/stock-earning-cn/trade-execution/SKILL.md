---
name: trade-execution
description: 专门用于代表用户向系统中记录买入或卖出交易的助手。
user-invocable: true
---

# 交易执行助手 (Trade Execution)

专门用于代表用户向系统中记录买入或卖出交易的助手。

## 认证与基础配置
- 环境变量: `STOCK_API_KEY`
- Base URL: 从 `config.sh` 中读取 `$STOCK_BASE_URL`（默认 `https://www.mystockearning.cn`，切换域名只需改 `config.sh`）

## API 指令清单

### 记录新交易与券商配置
当用户说 "我今天以 150 美元买入了 100 股苹果" 时：
- 1) 检查市场券商：执行 `./scripts/get_brokers.sh`（需要设置 `MARKET`）
- 2) 如需导入默认券商：执行 `./scripts/seed_defaults.sh`（需要设置 `MARKET`）
- 3) 计算手续费：执行 `./scripts/calculate_commission.sh`（需要设置 `BROKER_ID`、`TRADE_TYPE`、`QUANTITY`、`PRICE`）
- 4) 记录交易：执行 `./scripts/create_trade.sh`（需要设置 `SYMBOL`、`NAME`、`MARKET`、`TRADE_TYPE`、`QUANTITY`、`PRICE`、`TRADE_DATE`；可选 `COMMISSION`、`CURRENCY`、`NOTES`）

## 严格执行规则
1. 分析用户指令。
2. **货币显示规则**：在回复任何金额（如价格、手续费、总额等）时，必须根据该股票所在的市场显示正确的货币符号或单位：
   - `cn_a` (A股): `¥` 或 `元` (人民币 CNY)
   - `hk` (港股): `HK$` 或 `港元` (港币 HKD)
   - `us` (美股): `$` 或 `美元` (美元 USD)
3. **智能补全与确认机制**：当用户想要记录交易时，你必须按照以下逻辑处理：
   - **(代码补全)**：如果没有提供完整的股票代码和市场，先调 `GET /api/positions/` 查持仓；没找到则调用搜索 API (`/api/markets/search/stocks`) 遍历 cn_a, hk, us。
   - **(清仓智能识别)**：如果用户说“清仓”、“全卖了”，且未提供数量，必须先调用 `GET /api/positions/` 获取该股票的当前持仓数量，并自动填入。
   - **(防爆仓拦截)**：如果是卖出操作且提供了数量，必须先调用 `GET /api/positions/` 检查余额。如果余额不足，直接拒绝并提示用户当前实际持有量。
   - **(市价智能获取)**：如果用户未提供**买入价格**，静默调用 `/api/markets/stocks/{symbol}/price` 获取当前市价，并作为默认建议价询问用户。
   - **(按金额反推数量)**：如果用户提供了总金额和单价但未提供数量，自动计算 `数量 = 向下取整(总金额 / 单价)` 并向用户确认。
3. **券商前置拦截与算费机制**：在确认了股票代码、数量和价格后，在发起最终交易前，必须执行以下步骤：
   - 调用 `GET /api/brokers/?market={对应的市场}`。
   - 如果返回空列表 `[]`，说明该市场无券商。你必须**拦截交易并暂停**，询问用户：“您在这个市场尚未配置券商，无法计算印花税和交易佣金。是否需要为您一键导入该市场的默认券商配置？或者您想自定义配置？”
   - **等待用户回答**。如果用户回答“一键导入”或“同意导入”，你才调用 `POST /api/brokers/seed-defaults` 传入该市场代码，然后再调用 `GET /api/brokers/` 获取刚创建的 `broker_id`。如果用户要求“自定义”，请引导用户提供券商名称和佣金费率。
   - 拿到 `broker_id` 后，调用 `POST /api/brokers/calculate-commission` 计算精确的手续费（commission、stamp_duty 等）。
4. **最终确认**：在发起最终的 `POST /api/trades/` 之前，**必须**向用户输出一段确认信息（包含代码、名称、市场、数量、价格、以及**预估的手续费/印花税总计**）。只有在用户回复确认后，才能执行。
5. **确认后执行**：执行 `curl -X POST /api/trades/` 记录交易（带上获取到的 broker_id 和费用数据）。
6. **输出结果**：根据 API 响应，向用户确认交易已成功记录，并展示总金额。
