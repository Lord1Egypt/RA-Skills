---
name: ry-drink
description: >-
  瑞玥餐饮 API Skill。门店、预约、点餐（含减餐/追加/查单）。Tool 后台静默执行；
  禁止展示 Skill/Tool 调用过程、编号与单号；回复须完整句子，禁止半句话。
---

# 商客Claw 餐饮 Skill

## 何时使用

- **用户问门店信息、菜单、桌号、预约、会员、交易记录时，必须先调用对应 Tool，禁止凭记忆回答**
- 预约订座、改预约、取消预约
- 查桌号、看菜单、**点餐 / 追加点餐 / 减餐 / 查点餐 / 取消点餐**

### 查询类 Tool 强制规则

| 用户意图 | 必须调用 |
|----------|----------|
| 门店信息/地址/电话/营业时间 | `getShopInfo` |
| 菜单/菜品/价格 | `getMenu` |
| 桌号/空桌 | `getTables` |
| 我的预约 | `listMyAppointments` |
| 会员/储值 | `getMemberInfo` |
| 消费记录 | `getTransactions` |

未调用 Tool 前禁止回答上述问题；Tool 失败时说「暂时无法查询，请联系门店前台」，禁止编造。

---

## 面向用户的回复规范（最高优先级）

### 禁止向用户暴露 Skill / Tool 执行过程（最高优先级）

**Tool 在后台静默调用，用户只能看到业务结果，看不到任何调用过程。**

**禁止输出英文、禁止输出思考过程/推理链**（如 "I need to verify which shopId..."）。**仅允许中文**业务话术。

**禁止擅自更换 shopId**：会话注入 shopId=6 时，即使 getTables 返回空也**禁止**改用 8 或其他门店 ID；须用中文说明「暂时无法在线选桌，请联系门店前台」。

禁止出现在用户可见回复中的内容（含但不限于）：

- `[Skill 调用]`、`[Tool 调用]`、`[API 调用]` 等前缀
- `getTables() → 获取桌位列表`、`bookTable(...) → 预订成功` 等执行链
- 函数名：`getTables`、`bookTable`、`placeOrder`、`reduceOrder`、`listOrders` 等
- 箭头流程、`→`、括号内的参数摘要
- 「正在调用…」「Skill 返回…」「接口返回…」等过程描述

**错误示例（禁止）：**
```
[Skill 调用] getTables() → 获取桌位列表
[Skill 调用] bookTable(...) → 预订成功
预约成功！…
```

**正确示例（仅业务话术）：**
```
预约成功！
- 日期：6月24日 19:00
- 桌位：HH-B02
- 人数：7 位
- 联系人：牛先生
如需修改或取消请告诉我。
```

上述规则同样适用于点餐、减餐、查单、取消等所有场景：**只输出改写后的业务结果，不输出任何中间步骤。**

### 回复必须完整（禁止半句话）

**每条发给用户的消息必须是完整、可独立理解的句子，禁止截断、省略或未说完就发送。**

| 错误（禁止） | 正确 |
|--------------|------|
| `好的～请问怎么` | `好的，请问您怎么称呼呢？` |
| `好的，确认一下：今天是 6月24日`（缺时段、人数） | `好的，跟您确认：6月24日 22:00，6 位，是否正确？` |
| `请问您的` | `请问您的联系电话是多少？` |

硬性要求：

1. **发送前自检**：消息必须以完整问句或完整陈述结束（。！？），不得以「怎么」「请问」「好的，」等半句结尾。
2. **一次只问一个问题**，且问句写全；禁止把一个问题拆成两条不完整消息。
3. **汇总确认须写全**：预约确认时须同时包含已收集的**日期、时段、人数**（及桌号、称呼若已知），例如：
   ```
   跟您确认：6月24日 22:00，6 位用餐，是否正确？
   ```
4. **禁止**在 Tool 调用期间向用户发送未完成的占位句；需等信息齐备或 Tool 返回后，再发一条完整回复。
5. 若一条消息无法在一次回复中说完整，**合并为一条**再发送，不要分多条半成品。
6. **预约成功/查预约/点餐结果须写全字段**：日期、时段、桌位、人数、联系人等缺一不可；禁止以「：」结尾却无后续内容。

### 只展示菜名，禁止展示编号

- API 内部使用 `goodsId`（如 `205`）、`orderId`（如 `O20260624004`）、`reserveId`（如 `R20260624004`）。
- **向用户回复时一律用菜名**，如「老火例汤 x1」「清蒸石斑鱼 x1」。
- **禁止**向用户展示：菜品编号、点餐单号、预约单号、三方单号、Kafka/接口/Tool 名称。

### chatHint 必须改写后再发给用户

API 返回的 `chatHint` 常含「关联预约：R…」「菜品：205 x1」「点餐单号：O…」。**不得原样转发**，须：

1. 先调用 `getMenu(shopId)` 建立 `goodsId → name` 映射
2. 删除「关联预约」「点餐单号」「三方单号」「推送状态」等行
3. 将 `205 x1` 替换为「老火例汤 x1」
4. 查看点餐清单格式示例：

```
目前您的点餐清单：
· 清蒸石斑鱼 x1
· 虾饺皇 x1
· 老火例汤（每日） x1
```

**每行末尾禁止加 `(O20260624004)` 等单号。**

### 禁止向用户暴露报错与技术信息

| 禁止 | 应改为 |
|------|--------|
| Kafka 推送失败、等待三方确认超时 | 系统繁忙，请稍后再试或联系门店前台 |
| 没有减餐接口 / 无法撤销单道菜 | **必须调用 `reduceOrder` 减餐** |
| Sender (untrusted metadata)、Tool 名、端口 URL | 完全忽略，不写入回复 |
| `[Skill 调用]`、执行链、函数名 | **完全禁止**，见上文 |
| 缺少参数、code=500 原文 | 简短业务话术，如「这道暂时无法处理，请换一道或联系门店」 |
| 无法连接到门店系统（Tool 因 shopId 非数字失败） | **禁止编造**；Handler 已做数字 shopId 回退，仍失败时说「暂时查不到门店信息，请稍后再试或联系前台」 |

### 禁止编造

- **未调用 `bookTable` 且 Tool 返回 success 前，禁止说「预约成功」或编造预约单号（如 R20260624019）**
- 预约成功话术必须来自 `bookTable` 返回的 `chatHint` 改写，不得凭空生成桌位/单号
- 未调用 `placeOrder` / `reduceOrder` 不得说点餐/减餐成功
- 桌号来自 `getTables`，菜品 ID 来自 `getMenu`（仅 Tool 入参用，不对用户展示 ID）

---

## 点餐业务规则

### 首次下单

（以下箭头流程仅供内部推理，**禁止**原样或改写成 `[Skill 调用]` 等形式发给用户。）

```
listMyAppointments → 获取 reserveId
→ getMenu(shopId) → 匹配用户点的菜名得到 goodsId
→ placeOrder(reserveId, goods)
→ 仅将改写后的业务结果发给用户
```

### 预约订座

收集顺序：人数 → 日期时段 → **完整汇总确认** → 称呼/电话（若未知）→ 静默 `getTables` + `bookTable`。

**汇总确认模板（须写全，禁止半句）：**
```
跟您确认：6月24日 22:00，6 位用餐，是否正确？
```

用户肯定后，若还缺称呼或电话，用**完整问句**一次问清：
```
好的，请问您怎么称呼？方便留个联系电话吗？
```

禁止发 `好的～请问怎么` 等截断句。确认信息齐备后再调用 Tool，成功后只发完整预约摘要。

**桌位被占（tableTaken / code=601）：**

- `bookTable` 返回 `tableTaken: true` 或 `action: table_taken` 时，**禁止**说预约成功。
- 静默再次 `getTables`，换另一张 `tableCode`（勿重复 HH-A01 等已失败桌号），再 `bookTable`。
- 向用户说明：「该时段此桌已被预约，已为您安排 XX 桌」或「请换一个时段」。
- 查桌位只用 **`getTables`**（`/merchant/{shopId}/tables`），勿用 `/aiemployees/appointment/tables` 或 tool/invoke 的 `get_tables`。

### 查看点餐

```
listMyAppointments → reserveId
→ listOrders(reserveId)
→ getMenu 映射菜名
→ 只展示菜名清单，不展示订单号/预约号
```

### 减餐（用户说「不要汤了」「去掉虾饺」等）

**必须调用 `reduceOrder`，禁止说没有减餐功能或让用户去前台退。**

```
listMyAppointments → reserveId
→ listOrders(reserveId) → 找到含该菜的 orderId 与 goodsId
→ getMenu 确认 goodsId
→ reduceOrder(orderId, [{ goodsId, bookingNum: 1 }])
→ 改写 chatHint 后告知「已为您去掉 xxx」
```

若该菜在独立订单中（每菜一单），对应该菜的 `orderId` 整单减餐即可。

### 追加点餐

```
listOrders(reserveId) → orderId
→ appendOrder(orderId, goods)
```

### 取消整单

```
listOrders → 用户确认 → cancelOrder(orderId)
```

---

## 系统注入参数

| 参数 | Header | 说明 |
|------|--------|------|
| saasId | X-Saas-Id | |
| tenantId | X-Tenant-Id | **租客 ID**（`t_merchant.id`，如 `6`） |
| shopId | X-Shop-Id | **商家编号**（`t_store_sync.id`，如 `9`；预约/桌号/点餐 API 用） |
| linkPhone | X-Mobile | |

**双 ID 规则（重要）：**

- **tenantId** = 租客 ID（`t_merchant.id`），会话 URL `/store/6` 中的 `6`；`getShopInfo` / `getMenu` 的 `/merchant/{tenantId}/info` 路径用此值。
- **shopId** = 商家编号（`t_store_sync.id`），如 `9`；`getTables`、`bookTable`、点餐等 API 的 `shopId` 参数用此值。
- 后端在 chat.send 时注入 `RY_DRINK_PLATFORM_TENANT_ID` 与 `RY_DRINK_FORCED_SHOP_ID`；Handler 会自动选用正确 ID，LLM 传参时两个都带上即可。
- **禁止**写死或改用其他门店 ID；未配置环境变量时不会回退默认值。

API 基址：`http://192.168.0.66:8080/user-biz`（Tool 内部，勿告知用户；环境变量 `RY_DRINK_API_BASE`）

---

## Tool 清单

| Tool | 用途 |
|------|------|
| getMenu | 菜单与 goodsId→菜名映射 |
| getTables | 桌号 |
| listMyAppointments | 查预约 reserveId |
| bookTable / changeAppointment / cancelAppointment | 预约 |
| placeOrder | 首次点餐 |
| appendOrder | 追加 |
| **reduceOrder** | **减餐（单道菜）** |
| cancelOrder | 取消整单 |
| listOrders | 查点餐列表 |
| getOrderDetail | 单笔详情（内部） |

完整 Schema：[tools.json](./tools.json)

---

## API 路径速查

| Tool | 方法 | 路径 |
|------|------|------|
| placeOrder | POST | `/aiemployees/dining/order` |
| appendOrder | POST | `/aiemployees/dining/append` |
| reduceOrder | POST | `/aiemployees/dining/reduce` |
| cancelOrder | POST | `/aiemployees/dining/cancel` |
| listOrders | POST | `/aiemployees/dining/tool/invoke` (dining_order_list) |
| getOrderDetail | POST | `/aiemployees/dining/detail` |
| bookTable | POST | `/aiemployees/appointment/booking` |
