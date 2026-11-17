# 库存补货清单

![库存补货清单推广图](assets/promo-1600x900.png)

把一张不超过 100 行的库存表，变成可复核的逐 SKU 补货清单：你会拿到补多少、为什么、以及哪些字段还缺，方便中文小店经营者、小说作者和自媒体创作者做小批量物料准备。

## 输入与结果

为每个 SKU 提供 `sku`、`current_stock`、`recent_sales`、`sales_days`、`lead_time_days`、`target_stock`；可选 `safety_stock` 和包装规格。可用 Markdown 表格、CSV 内容或结构化数据。

结果包含：按建议补货量排序的逐 SKU 表、日均销量与提前期需求的公式依据、提前期缺货风险，以及不完整行的缺失字段。缺少关键字段时会明确指出，不会编造数据。

核心公式：`日均销量 = recent_sales / sales_days`；`提前期需求 = 日均销量 × lead_time_days`；`建议补货 = max(0, target_stock + safety_stock - current_stock)`。有包装规格时，将建议量向上取整到包装倍数。

这不是订单发货工具、实时库存系统或仓储软件部署方案；仅处理有限表格并保留输入事实与建议之间的区别。

## 使用

在支持 Skills 的 Agent 中调用：

```text
使用 $shop-stock-reorder-plan-cn 根据我提供的库存表输出补货建议、公式依据和缺失字段。
```

成功与缺失字段示例见 `fixtures/`。运行独立自测：

```bash
bash scripts/self-test.sh
```

## English

**Stock Reorder Plan** turns a table of up to 100 inventory rows into a reviewable per-SKU reorder list. Provide current stock, recent sales and days covered, lead time, and target stock. The result separates calculated recommendations from supplied facts, shows formulas and lead-time risk, and lists missing required fields instead of inventing values. It is for lightweight table-based planning—not fulfilment, live inventory sync, or warehouse deployment.

## 来源与许可

用途边界参考记录见 [sources/erpnext-reference.md](sources/erpnext-reference.md)。本项目采用 [MIT-0](LICENSE)。
