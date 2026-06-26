# MCP 调用参考

## JSON-RPC 2.0 调用格式

```python
import json, urllib.request, re

# 读取 token
token = ""

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

# 调用工具
def call_zhangben(tool_name, arguments):
    data = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }).encode()
    req = urllib.request.Request(
        "https://moneydata.cn/mcp",
        data=data, headers=headers, method='POST'
    )
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read().decode())
    return result['result']['content'][0]['text']
```

## 6个写操作工具参数 Schema


### income（记录收入）
**Required**: `sub_category`(number), `platform_id`(number), `amount`(number), `currency`(string)

| 参数 | 类型 | 说明 |
|------|------|------|
| sub_category | number | 收入子分类 |
| platform_id | number | 入账平台ID |
| amount | number | 收入金额（CNY=元, HKD=港元） |
| currency | string | 币种: CNY 或 HKD |
| remark | string | 选填，备注 |
| record_date | string | 选填，YYYY-MM-DD，默认当天 |

### expense（记录支出）
**Required**: `sub_category`(number), `platform_id`(number), `amount`(number), `currency`(string), `pay_mode`(string)

| 参数 | 类型 | 说明 |
|------|------|------|
| sub_category | number | 支出子分类 |
| platform_id | number | 支付平台ID |
| amount | number | 支出金额 |
| currency | string | 币种: CNY 或 HKD |
| pay_mode | string | **枚举**: `balance`（余额支付）| `credit`（信用支付） |
| remark | string | 选填，备注 |
| record_date | string | 选填，YYYY-MM-DD，默认当天 |

### ai_expense（记录一笔AI账户的支出）
**Required**: `sub_category`(number), `platform_id`(number), `amount`(number), `currency`(string)

| 参数 | 类型 | 说明 |
|------|------|------|
| sub_category | number | 支出子分类 |
| platform_id | number | 支付平台ID |
| amount | number | 支出金额 |
| currency | string | 币种: CNY 或 HKD |
| remark | string | 选填，备注 |
| record_date | string | 选填，YYYY-MM-DD，默认当天 |

### buy_asset（买入资产）
**Required**: `sub_category`(number), `price_code`(string), `platform_id`(number), `quantity`(number), `pay_currency`(string)

| 参数 | 类型 | 说明 |
|------|------|------|
| sub_category | number | 资产子类型: 1=股票,2=基金,3=债券,11=住宅,21=活期,22=定期,37=黄金 |
| price_code | string | 资产代码: A股纯数字如600519，基金F+代码如F000051，黄金UDFGOLD001 |
| platform_id | number | 资产存放平台ID（券商等） |
| quantity | number | 数量（股票=股, 基金=份, 黄金=克） |
| pay_currency | string | 支付币种: CNY 或 HKD |
| cost_unit_price | number | 选填，买入单价，默认收盘价 |
| from_platform_id | number | 选填，扣款账户平台ID，未传=platform_id |
| purchase_date | string | 选填，YYYY-MM-DD，默认当天 |
| remark | string | 选填，备注 |

### sell_asset（卖出资产）
**Required**: `sub_category`(number), `price_code`(string), `platform_id`(number), `quantity`(number), `deposit_currency`(string)

| 参数 | 类型 | 说明 |
|------|------|------|
| sub_category | number | 资产子类型 |
| price_code | string | 资产代码 |
| platform_id | number | 资产存放平台ID |
| quantity | number | 卖出数量 |
| deposit_currency | string | 到账币种: CNY 或 HKD |
| sell_unit_price | number | 选填，卖出单价，默认收盘价 |
| to_platform_id | number | 选填，资金到账平台ID，未传=platform_id |
| sell_date | string | 选填，YYYY-MM-DD，默认当天 |
| remark | string | 选填，备注 |

**返回值**: `{remaining_quantity, realized_profit, deposit_asset_id}`

### borrow（借款）
**Required**: `from_sub_category`(number), `from_platform_id`(number), `from_currency`(string), `to_sub_category`(number), `to_platform_id`(number), `to_currency`(string), `quantity`(number)

| 参数 | 类型 | 说明 |
|------|------|------|
| from_sub_category | number | 负债子类型: 46=房贷,47=车贷,48=消费贷,49=信用贷 |
| from_platform_id | number | 负债所在平台ID |
| from_currency | string | 负债币种: CNY 或 HKD |
| to_sub_category | number | 存入子类型: **仅支持21=活期** |
| to_platform_id | number | 存入平台ID |
| to_currency | string | 到账币种: CNY 或 HKD |
| quantity | number | 贷款数量 |
| channel_id | number | 选填，交易渠道 |
| remark | string | 选填，备注 |

### repay（还款）
**Required**: `from_sub_category`(number), `from_platform_id`(number), `from_currency`(string), `to_sub_category`(number), `to_platform_id`(number), `to_currency`(string), `quantity`(number)

| 参数 | 类型 | 说明 |
|------|------|------|
| from_sub_category | number | 支付子类型: **仅支持21=活期** |
| from_platform_id | number | 支付平台ID |
| from_currency | string | 支付币种: CNY 或 HKD |
| to_sub_category | number | 欠款子类型: 46=房贷,47=车贷,48=消费贷,49=信用贷 |
| to_platform_id | number | 欠款平台ID |
| to_currency | string | 欠款币种: CNY 或 HKD |
| quantity | number | 还款数量 |
| channel_id | number | 选填，交易渠道，默认=to_platform_id |
| remark | string | 选填，备注 |


## ⚠️ schema required

**建议**: 始终按 schema required 传参，避免意外情况。

## 只读工具返回结构要点

### get_asset_list
- 证券类资产 `category` 返回 **0**（非 schema 中的 10=证券）
- 每项资产有两套金额：`base`（主币种 CNY）和 `original`（原始币种，港股=HKD）
- `exchange_rate` 字段提供汇率，同币种=1
- 顶层有 `total_current_value`/`total_cost_value`/`total_profit` 汇总
- `sub_categorys` 数组列出当前持有的资产子类型

### get_transaction_list
- `biz_type` 枚举：buy_asset, sell_asset, income, expense, repay, borrow, transfer
- `from_*/to_*` 双向结构，每侧含 id/name/price_code/category/sub_category/platform_id/platform_name/quantity/amount/currency
- 信用卡 price_code = `UDFCR00001`

### get_dashboard_summary
- `breakdown` 数组：每项含 category/name/current_value/percentage
- 顶层：total_assets, total_liabilities, net_worth, month_change, year_change, currency

## 15 个工具一览

1. `get_asset_list` — 查询资产列表（+include_cleared参数）
2. `sell_asset` — 卖出资产
3. `repay` — 还款
4. `get_platform_list` — 获取平台列表
5. `borrow` — 借款
6. `get_dashboard_summary` — 财富看板汇总
7. `get_income_summary` — 收入汇总
8. `get_liability_list` — 负债列表
9. `expense` — 记录支出
10. `get_category_list` — 获取分类列表
11. `income` — 记录收入
12. `get_transaction_list` — 交易记录
13. `buy_asset` — 买入资产
14. `get_expense_summary` — 支出汇总
15. `ai_expense` — 记录AI账户支出