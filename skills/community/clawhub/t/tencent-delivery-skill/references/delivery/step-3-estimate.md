# 第三步：询价

> **触发**：`next_state == step3-estimate`

## 命令

```bash
# 首次询价
python3 ./scripts/tms_delivery.py run-estimate

# 询价过期/需重询（以下任一场景必须用它，禁用 run-estimate）
python3 ./scripts/tms_delivery.py re-estimate
```

**`re-estimate` 适用场景**：`select-sku` 返回 `expired` / 下单返 `code == 40205` / 用户主动"刷新报价"。详见 [error-handling §5](../error-handling.md#5-询价过期重试-下单前必须用户二次确认)。

## 分支表：`run-estimate` 返回

| 情况 | 动作 |
|---|---|
| 成功（含 `display_rows`/`skuMap`/`senderAddr`/`receiverAddr`） | → §3.2 展示报价 |
| `stage: assert` | 按 `violations` 回对应步骤；若提示 `estimatePriceRecordId filled` → 改用 `re-estimate` |
| `stage: sanity_check` + `same_location` | 按脚本 `reply_template` 回复寄=收兜底 |
| `stage: sanity_check` + `missing_field` | 回对应步骤补齐 |
| `stage: mcp_call` 失败 | 见 [error-handling](../error-handling.md) |

## 3.2 报价展示规则

**原样贴出脚本返回的 `reply_template`**（markdown 表格已在脚本内拼好，按价格升序、空值以 `-` 显示）。

❌ 禁止：替用户做选择 / 退化成编号嵌套列表 / 拆多张表格 / 自己重排表头

**skuMap 已自动落盘**，LLM 无需再调 `state set skuMap`。

<a id="3-3-个性化筛选"></a>
## 3.3 个性化筛选

### 意图识别速查

| 维度 | 用户表达 | 匹配条件 |
|------|---------|----------|
| 直送 | 直送 / 专送 / 快一点 / 极速 / 赶时间 | `expressTypeName == "极速取送"` |
| 拼送 | 拼送 / 便宜点 / 特惠 / 不急 / 经济 | `expressTypeName == "特惠取送"` |
| 服务商 | "用顺丰" / "京东" / "达达" | `spName contains "..."` |
| 价格 | "20 以内的" / "最便宜的" | `totalFee` 转数值比较/排序 |
| 组合 | "顺丰的直送" | 多条件同时满足 |

### 重筛规则

1. 从 chat history 最近一次 `runerrand_estimate_price` 返回值 `data.spEstimatePrices` 读原数据
2. 按新条件过滤 + `totalFee` 升序
3. 重展示表格 + `state set skuMap` 同步序号映射
4. ❌ **禁止**重调 `runerrand_estimate_price`（会让 `estimatePriceRecordId` 失效）
5. 筛选结果为空 → 兜底展示全量 + 提示"未找到完全匹配"

<a id="-重询价场景必须用-re-estimate-v131"></a>
## 3.4 重询价（与上文 `re-estimate` 同义）

参见本文件顶部 "命令" 章节和 [error-handling §5](../error-handling.md#5-询价过期重试-下单前必须用户二次确认)。
