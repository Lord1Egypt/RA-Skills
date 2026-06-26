# 跑腿 MCP 接口契约

LLM 通过 `python3 ./scripts/tms_delivery.py mcp-call <tool_name> '<json>'` 调用 MCP Server（脚本自动注入 Token）。

## 工具清单

| 工具名（大小写敏感） | LLM 直调？ | 说明 |
|----------------------|:---------:|------|
| `runerrand_estimate_price` | ❌ | 由 `run-estimate` / `re-estimate` 封装 |
| `runerrand_book_order` | ✅ | 下单（第五步） |
| `runerrand_precancel_order` | ✅ | 预取消（查取消费） |
| `runerrand_cancel_order` | ✅ | 确认取消 |
| `runerrand_query_going_order` | ❌ | 由 `bootstrap` 封装，全局只调一次 |
| `runerrand_query_order_detail` | ✅ | 查单 / 骑手追踪 |
| `get_place_suggestion` | ❌ | 由 `resolve-address` 封装 |

> 传错工具名 → `tool not found`；参数名错了 → 见各工具下"参数名红线"。

## 公共响应码

| code | 说明 |
|------|------|
| 0 | 成功 |
| 10000 | 服务器异常 |
| 10001 | 参数校验错误（对照本文修正入参） |
| 40000 | 业务失败（通用，展示 message） |
| 40001 | 无数据 |

---

<a id="mcp_estimate_price"></a>
## 1. runerrand_estimate_price（询价）

> 🛑 **LLM 不直调**。仅通过 `run-estimate` / `re-estimate` 命令触发，入参由脚本从 session 拼装。

**LLM 需理解的响应字段**（chat history 里回溯原始数据时使用）：

```
data.estimatePriceRecordId  // 下单必传（脚本已自动写 session）
data.spEstimatePrices[i]:
  skuId              String  // 如 "60797_2"，下单原样传递
  spName             String  // "顺丰同城"
  expressTypeName    String  // "极速取送" / "特惠取送"
  defaultChecked     0/1     // 1=默勾
  totalFee           String  // 元字符串，直接展示
  couponFee          String  // 元字符串
  deliveryTime       String  // "2026-04-28 15:00:53"
```

> 🛑 **skuId 硬约束**：必须从 `spEstimatePrices[i].skuId` 原样复制——是 `"{productId}_{serviceLevel}"` 格式的字符串，**禁止**用展示序号（1/2/3）或猜测数字代替。

> ⚠️ 询价过期时后端返回 40205，改调 `re-estimate` 重新走一遍。

---

<a id="mcp_book_order"></a>
## 2. runerrand_book_order（下单，LLM 直调）

**请求**：

| 字段 | 类型 | 说明 |
|------|------|------|
| estimatePriceRecordId | String | 取自 session（`state get estimatePriceRecordId`） |
| expressSkuInfos | Array\<String\> | **仅单选**，长度 1，元素为 skuId 字符串 |

```json
{"estimatePriceRecordId":"1497190455679606785","expressSkuInfos":["600018_1"]}
```

**skill 需读的响应字段**：

| 字段 | 说明 |
|------|------|
| orderCode | 订单编码（立即 `state set orderCode`） |
| payInfo.codeUrl | 微信支付 URL，**优先** |
| payInfo.scanUrl | 扫码支付页，**兜底** |

> 其他字段（tradeType/paySign/prepayId/nonceStr/signType/timeStamp）一律忽略。

**业务错误码**：

| code | 说明 | 处理 |
|------|------|------|
| 40200 | 下单失败 | 展示 message |
| 40201 | 需先完成支付分授权 | 引导去小程序 |
| 40202 | 存在未完成订单 | 提示先处理现有订单 |
| 40205 | 询价已过期 | **静默 `re-estimate` 让用户按新报价重选**，❌ 禁止代下单（详见 [error-handling.md §5](./error-handling.md)） |
| 40206 | 重复下单 | 提示已有订单 |
| 40207-40211 | 风控拦截 | 展示 message |

---

<a id="mcp_pre_cancel_order"></a>
## 3. runerrand_precancel_order（预取消，LLM 直调）

**请求**：`{"orderCode": "<orderCode>"}`

**响应**：

- `couldCancel` (Boolean)
- `cancelFee` (String，元，无取消费 "0.00")

**处理**：
- `couldCancel == true` → 展示取消费，等用户确认后调 `runerrand_cancel_order`
- `couldCancel == false` → 提示"该订单当前不可取消，请前往小程序操作"

---

<a id="mcp_cancel_order"></a>
## 4. runerrand_cancel_order（确认取消，LLM 直调）

**请求**：`{"orderCode": "<orderCode>", "preCancel": true}`（`preCancel` 固定 `true`）

**响应**：`code == 0` 成功；其他展示 `msg`。

> ⚠️ **必须两步走**：先 `precancel` → 用户确认 → `cancel`。❌ 禁止跳过 precancel。

**业务错误码**：40400（取消失败）/ 40401（获取规则失败）/ 40402（确认失败）。

---

<a id="mcp_query_ongoing_order"></a>
## 5. runerrand_query_going_order（查进行中订单）

> 🛑 **LLM 不直调**。由 `bootstrap` 命令内部调用，全局唯一调用时机。其他场景一律从 session 读取，详见 [order-workflow.md](./order-workflow.md)。

---

<a id="mcp_query_order_info"></a>
## 6. runerrand_query_order_detail（查单详情，LLM 直调）

**请求**：`{"orderCode": "<orderCode>"}`

> 🛑 **核心约束：skill 只读 `orderSuggestion` 一个字段**
> - ✅ `orderSuggestion` 是后端大模型生成的完整订单状态描述（含骑手位置、预计送达、联系方式等），**直接原样展示**
> - ❌ 禁止读取 / 解析 / 展示任何其他字段（spName / riderName / riderPhone / expressTypeName / deliveryTime / totalFee / payFee / paidFee / couponFee / cancelFee / refundFee / customerInfo ...）
> - ❌ 禁止"精选字段自己拼表格"——`orderSuggestion` 已完整呈现
> - ⚠️ **唯一例外**：第七步支付确认时，仅读 `orderStatusText` 判断"是否仍为待支付"分支，不展示

**响应示例**：

```json
{
  "orderCode": "TxT481UfeA37s0h7K-...",
  "orderStatusText": "送件中",
  "orderSuggestion": "骑手已到达取件点，正在取件中。骑手当前距离收件点xxkm，预计xx月xx日 xx:xx到达收件点。如需联系骑手，请致电xxxxxxx。"
}
```

---

<a id="mcp_get_place_suggestion"></a>
## 7. get_place_suggestion（地址搜索）

> 🛑 **LLM 不直调**。由 `resolve-address` 命令内部封装（含地址簿匹配 + SUG 识别 + POI 分类）。LLM 只调 `resolve-address sender|receiver <keyword> [region]`。
