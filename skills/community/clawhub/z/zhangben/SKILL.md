---
name: zhangben
description: 个人记账与资产管理。通过陶朱账本 MCP 接口管理收入、支出、资产买入/卖出、负债、交易记录、财富看板等。触发场景：用户提到记账、记收入、记支出、买资产、卖资产、查资产、查负债、查交易、查收支、财富看板、账本等个人财务操作。
version: 1.0.2
---

# 陶朱账本 (zhangben) MCP 技能

通过 `https://moneydata.cn/mcp` 的 MCP 接口管理个人财务。

## §1 连接与认证

⚠️ **首次使用必须先完成认证。** 详细流程见 `references/auth.md`。

**认证流程概述**：
1. 检查是否有已保存的有效 Token
   - ✅ 有且有效 → 跳过本节，直接使用
   - ❌ 无或失效 → 进入认证流程
2. **向用户展示两个选项，等待用户选择后再执行**（不可自行决定）：
   - **选项一（推荐）**：用户提供陶朱账本微信小程序的 Token，账户与微信打通
   - **选项二**：自动生成身份标识ID 并通过 API 获取 Token（不支持微信查看）
3. 获取凭证后保存到 memory：身份标识ID（如生成）和 Token

> 关键提醒：
> - **选项一（微信Token）**：不需要保存身份标识ID，Token 本身已包含用户信息
> - **选项二（API获取）**：必须保存身份标识ID（32位，MAC 地址 MD5），Token 过期后用同一身份标识ID + 新时间戳即可换新 token；**更换身份标识ID 会导致历史数据丢失！**

## §2 参数陷阱（必读！）

| 工具 | ❌ 易错写法 | ✅ 正确写法 |
|------|------------|------------|
| `buy_asset` | `code: "600519"` | `price_code: "600519"` |
| `buy_asset` | `price: 1268` | `cost_unit_price: 1268` |
| `buy_asset` | 不传币种 | `pay_currency: "CNY"` (**必填!**) |
| `sell_asset` | 不传币种 | `deposit_currency: "CNY"` (**必填!**) |
| `income`/`expense` | 不传币种 | `currency: "CNY"` (**必填!**) |
| `borrow`/`repay` | 不传币种 | `from_currency`/`to_currency: "CNY"` (**必填!**) |
| `get_category_list` | `direction: "income"` | `direction: 1` (int) |
| 各工具数字参数 | `"101"` (string) | `101` (number) |


## §3 操作速查

> 完整参数 schema 见 `references/mcp-api.md`，平台ID见 `references/platform-ids.md`，分类代码见 `references/category-codes.md`，认证流程见 `references/auth.md`

### 记录收入
```
income(sub_category=10002, amount=1000, platform_id=101, currency="CNY", remark="比赛奖金")
```
- 工具名是 `income`，不是 `record_income`
- `record_date`: 可选 YYYY-MM-DD

### 记录支出
```
expense(sub_category=20044, platform_id=101, amount=2000, currency="CNY", pay_mode="balance", remark="买手机")
```
- `pay_mode` 枚举: `balance`(余额) | `credit`(信用卡)，其他值报 [30018]
- 信用消费不扣活期余额，记为信用卡欠款，通过 `repay` 还款

### 使用AI专属账户支出
```
ai_expense(sub_category=20044, platform_id=101, amount=2000, currency="CNY", remark="AI AGENT买手机")
```
- AI AGENT 使用AI账户支付后，可以通过 ai_expense 接口记录这笔支出。

### 买入资产
```
buy_asset(sub_category=1, price_code="600519", quantity=2, cost_unit_price=1268,
          platform_id=1, from_platform_id=101, pay_currency="CNY")
```
- `platform_id`: 存放平台(券商)，`from_platform_id`: 扣款平台(银行)，不传则同 platform_id
- price_code: A股 `600519`/`SH600519` 均可，基金 `F000051`，黄金 `UDFGOLD001`

### 卖出资产
```
sell_asset(sub_category=1, price_code="SH600519", platform_id=1, quantity=1,
           sell_unit_price=1300, deposit_currency="CNY", to_platform_id=101)
```
- price_code **最佳实践**: 用 `get_asset_list` 返回的格式(A股 `SH600519`，港股 `HK00700`)
- 返回: `remaining_quantity`(剩余持有)、`realized_profit`(盈亏)、`deposit_asset_id`

### 借款/还款
```
borrow(from_sub_category=46, from_platform_id=101, from_currency="CNY",
       to_sub_category=21, to_platform_id=105, to_currency="CNY", quantity=100000)
repay(from_sub_category=21, from_platform_id=101, from_currency="CNY",
      to_sub_category=49, to_platform_id=101, to_currency="CNY", quantity=100)
```
- borrow: from_sub_category=46(房贷)/47(车贷)/48(消费贷)/49(信用贷)，to_sub_category=**仅21(活期)**
- repay: from_sub_category=**仅21(活期)**，to_sub_category=46/47/48/49

### 查询工具
| 工具 | 用途 | 关键提醒 |
|------|------|----------|
| `get_asset_list` | 资产列表 | 证券 category=0(非10)；看 `base`(CNY) 非 `original`；`include_cleared`(bool)含已清仓 |
| `get_liability_list` | 负债列表 | 看 `remaining_amount`，⚠️ `base.total_value` 可能=0 |
| `get_transaction_list` | 交易记录 | biz_type: buy_asset/sell_asset/income/expense/repay/borrow/transfer |
| `get_dashboard_summary` | 财富看板 | 总资产/总负债/净资产/月年变化 |
| `get_income_summary` | 收入汇总 | 传 category 按二级汇总，不传按一级 |
| `get_expense_summary` | 支出汇总 | 同上 |
| `get_category_list` | 分类列表 | 可按 direction 过滤；每天刷新引用 |
| `get_platform_list` | 平台列表 | 可按 sub_category 过滤；每天刷新引用 |

## §4 重要提醒

- **分类列表每日刷新**: 每天第一次使用，调用 `get_category_list()` 获取最新分类数据，当天后续使用直接引用，不要硬编码分类代码
- **平台列表每日刷新**: 每天第一次使用，调用 `get_platform_list()` 获取最新平台数据，当天后续使用直接引用，不要硬编码平台ID
- **跨币种买入**: 买港股必须传 `pay_currency="CNY"`，系统自动按汇率折算扣款
- **负债查询**: 看 `remaining_amount`(待还金额)
- **数量单位**: 股票=股，基金=份，黄金=克
- **错误码速查**: 30014(余额不足) 31002(必填缺失) — 完整列表见 `references/errorcode.md`

