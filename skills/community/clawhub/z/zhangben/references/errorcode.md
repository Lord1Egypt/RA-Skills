# 常见错误码

| code | message | 原因 | 解决 |
|------|---------|------|------|
| 30008 | 卖出数量不能超过当前持有数量 | sell_asset 数量超持仓 | 检查 get_asset_list 持有量 |
| 30009 | 卖出数量必须大于0 | sell_asset quantity≤0 | 传入正整数 |
| 30014 | XX 余额不足 | buy_asset 扣款余额不够 | 检查 from_platform_id 余额；跨币种传 pay_currency |
| 30016 | 子分类 sub_category 不存在 | income/expense 的 sub_category 无效 | 用 get_income_expense_category 获取有效值 |
| 30018 | 支付方式无效，可选: balance, credit | expense pay_mode 不合法 | 传 balance 或 credit |
| 30021 | 不支持的转出/转入账户类型 | borrow/repay 的 sub_category 不合法 | from: 仅21(活期)用于repay，46/47/48/49用于borrow; to: 仅21(活期)用于borrow，46/47/48/49用于repay |
| 31001 | 转出数量与转入数量都为0 | borrow/repay quantity 缺失或为0 | 传入正数 |
| 31002 | 各种必填参数缺失 | 缺少 required 字段 | 检查 schema required 列表 |

