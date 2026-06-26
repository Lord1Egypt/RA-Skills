# 分类代码

## 分类结构

收支分类分两级：**大类 (category)** → **子分类 (sub_category)**。

- 收入: `direction=1`，大类: 工作收入 / 经营收入 / 财产收入 / 其他收入
- 支出: `direction=2`，大类: 餐饮 / 交通 / 购物 / 居住 / 娱乐 / 其他支出
- 资产: `direction=3`，大类: 证券 / 房产 / 现金类 / 保险 / 贵金属 / 其他资产
- 负债: `direction=4`，大类: 贷款

## 资产子分类(sub_category)

| sub_category | 名称 | price_code 格式 |
|----------|------|----------------|
| 1 | 股票 | 股票代码，如 `600519` |
| 2 | 基金 | `F` + 基金代码，如 `F000051` |
| 3 | 债券 | — |
| 11 | 住宅 | — |
| 21 | 活期 | — |
| 22 | 定期 | — |
| 37 | 黄金 | `UDFGOLD001` |

> 具体分类代码和 ID 是动态数据，**不要硬编码**。

## 每日刷新

每天**第一次**使用陶朱账本时，调用 `get_category_list()` 获取最新分类列表并记住结果：

- `get_category_list(direction=1)` — 收入分类
- `get_category_list(direction=2)` — 支出分类
- `get_category_list(direction=3)` — 资产分类
- `get_category_list(direction=4)` — 负债分类

当天后续使用直接引用缓存结果。
