# 第四步：用户选择服务商

> **触发**：用户回复报价表格的序号

## 命令

```bash
# 用户回数字序号
python3 ./scripts/tms_delivery.py select-sku <序号>

# 用户回"确认/好的/确定" → 兜底选价格最低的极速取送后再走 select-sku
```

`select-sku` 内部自动：从 skuMap 取 skuId → 落盘 `selectedSkuId` → TTL 预检（3 分钟新鲜窗口）。

## 分支表：`select-sku` 返回

| status | 含义 | 动作 |
|---|---|---|
| `ok` + `fresh: true` | 新鲜有效 | → [第五步](./step-5-book.md) |
| `expired`（`reason ∈ {stale, no_estimate_at}`） | 询价过期 | 调 `re-estimate` → 展示新报价 → 等用户按新序号重选 |
| `error` + `index_not_in_sku_map` | 序号无效 | 提示用户回复 1-N 之间的序号 |

## 选择规则

| 用户回复 | 动作 |
|---|---|
| 单个数字（"1"） | `select-sku 1` |
| 多个数字（"1,3"） | 提示"每次只能选一个，请回复一个序号" |
| "确认/确定/好的" | 选**价格最低的极速取送**；二次确认后走 `select-sku <对应序号>` |
| 新筛选条件 | 回 [第三步 §3.3](./step-3-estimate.md#3-3-个性化筛选) |

## 硬约束

- ✅ 本步**纯 session 操作**，禁止调任何 MCP（尤其禁止重询价）
- ❌ `expired` 时用 `re-estimate`，**禁止**用 `run-estimate`（会被 `step3-entry` 断言挡下）
- ❌ `expired` 时**禁止**用新 recordId + 旧 skuId 静默下单（会返 510008/40205）
- 防泄露规则见 [SKILL.md §4](../../SKILL.md#output-leak-firewall)
