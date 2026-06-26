<a id="order-workflow-main"></a>
## 订单流程

适用于查询订单详情（含骑手位置/送达进度）、取消订单。

### 路由规则

- 看订单状态/详情 / 看骑手位置 / 看送到哪了 → [订单详情查询流程](#order-query-flow)
- 取消当前订单 → [取消订单流程](#order-cancel-flow)

> 💡 `runerrand_query_order_detail` 返回的 `orderSuggestion` 已经是后端大模型生成的完整订单描述，**包含订单状态、骑手姓名/电话、当前位置、预计送达时间等所有用户关心的信息**。因此订单查询和骑手追踪**统一走同一个流程、调用同一个工具、展示同一个字段**，无需拆分。

### 订单号（orderCode）来源

> 🛑 **核心原则：只信服务端已校验过的 orderCode，不信任 LLM 对话记忆。**
>
> 支付完成/取消成功/中途退出之后，session.json 会被 `state clear` 清空。此时 LLM 上下文里可能还留着旧 orderCode，但这个 orderCode 对应的订单**很可能已结束**（已完成/已取消/已退款）——再去调 `runerrand_precancel_order` 或 `runerrand_query_order_detail` 只会得到误导性结果。

**按以下优先级获取 orderCode**：

1. **用户当前消息明确提供**（如"查 BX123456"）——最高优先级，用户的权威主动输入
2. **`python3 ./scripts/tms_delivery.py state get orderCode` 读 session.json**
   - `status==ok && value` 非空 → 使用该 orderCode（§0 reconcile 已校验其与服务端一致）
   - `status==empty`（session 已被清空） → ❗️**一律跳到下方"空快照兜底流程"**，❌ 禁止从 chat history 里捡旧 orderCode
   - value 为 null → 当前会话从未下单，按"空快照兜底流程"处理
3. **上下文中最近一次 `runerrand_book_order` 的返回值** —— 仅在 session.json 中同样存在该 orderCode 时才使用（用于下单成功→支付确认这一段连续流程，session 尚未 clear）
4. 都取不到 → 询问用户，让用户提供订单号

<a id="empty-session-fallback"></a>
**空快照兜底流程（session 被 clear 之后）**：

```
用户发起 查单/取消/查骑手 意图
  ↓
state get orderCode 返回 status==empty 或 value==null
  ↓
🛑 禁止从 chat history/回忆 中提取旧 orderCode
  ↓
按下方模板回复用户，请其明示操作对象：
```

**模板（session 为空时查单/取消的追问）**：
```markdown
本次会话暂无订单快照。请提供要操作的订单号，或告诉我是否要新下单。

- 如果要查/取消最近一笔订单，请回复订单号（格式形如 Tx...）
- 如果想新寄东西，直接描述需求即可（如「从公司寄到XX」）
```

**❌ 禁止的替代方案**：
- ❌ 从 chat history "回忆"最近一次的 orderCode 当真理使用
- ❌ 调用 `runerrand_query_going_order` 来"找回"订单号（§0 之后该接口**全局禁用**，由 `bootstrap` 独占）
- ❌ 直接用旧 orderCode 调 `runerrand_precancel_order`/`runerrand_query_order_detail`（订单可能已终结，返回值失去意义）

> ⚠️ **禁止为了查订单号而调用 `runerrand_query_going_order`**。该接口全局只在 Quick Start §1.3 调用一次，其他场景一律按上面的优先级读取或询问用户。

---

<a id="order-query-flow"></a>
### 订单详情查询流程

> 🛑 **核心约束**：`runerrand_query_order_detail` 返回体中 skill **只读 `orderSuggestion` 一个字段直接展示**，禁止读取/拼装其他字段（spName / riderName / riderPhone / deliveryTime / totalFee 等）。详见 [api-contract.md §6](./api-contract.md#mcp_query_order_info)。
>
> 本流程同时适用于：查询订单状态、查看骑手位置、查看送达进度。`orderSuggestion` 里这些信息都已包含，无需拆流程、无需调第二个工具。

**步骤**：

1. 按上方"订单号来源"规则确定 `orderCode`。若 `state get orderCode` 返回空，**按 [空快照兜底流程](#empty-session-fallback) 向用户追问订单号，不得从 chat history 捡旧值**。
2. 查询详情：
   ```bash
   python3 ./scripts/tms_delivery.py mcp-call runerrand_query_order_detail '{"orderCode": "<orderCode>"}'
   ```
3. 按下方模板回复用户。

**❌ 禁止编造订单信息，所有字段均来自工具返回。**
**❌ 禁止回复模版以外的内容**
**❌ 禁止展示 orderSuggestion 以外的任何字段**（尤其禁止把 riderName / riderPhone / spName 等单独拎出来拼成"骑手信息""服务商信息"等板块——这些已在 orderSuggestion 里）
**❌ 用户问的字段在整个 `runerrand_query_order_detail` 返回体中不存在或为空**（如取件码/收件码/取货码等）→ 按 [§ 用户追问订单详情中不存在的字段](#missing-field-handling) 直接告知没有，禁重复查询、禁编造

**回复模板**：

```markdown
📋 跑腿订单详情

{orderSuggestion}

💬 如需取消，请发送「取消跑腿」
```

> `orderSuggestion` 是后端大模型生成的完整订单状态描述（含订单状态、骑手位置、预计送达、联系方式），**直接原样展示**，skill 无需也不允许读取其他字段拼装。

<a id="missing-field-handling"></a>
#### 用户追问订单详情中不存在的字段

**判定依据**：以 `runerrand_query_order_detail` **整个返回体的所有字段**（如 `orderCode` / `orderStatusText` / `orderSuggestion` 以及未来可能新增的字段）为准——**不是只看 `orderSuggestion`**。

**判定规则**：
- 用户询问某项信息（典型如：**取件码 / 收件码 / 取货码 / 验证码 / 配送码 / 实时定位 GPS 经纬度 / 骑手照片 / 详细路径轨迹 / 派送轨迹** 等）
- 在工具返回的 JSON 里**逐字段扫一遍**：是否有任一字段（不限于 `orderSuggestion`）能直接、明确给出该信息
- **整个返回体里都找不到，或对应字段为空字符串/null** → 视为"没有该信息"
- **绝对禁止编造、估算、或从其他字段拼凑**（不要把 `orderCode` 当取件码、不要把 `orderStatusText` 里的字眼解读成验证码等）

**首次回复**（明确告知没有，单句即可，不展开解释为什么）：

```markdown
抱歉，本订单没有「取件码」这项信息。
```

**用户追问/不接受**（如"再查一下"、"应该有的吧"、"帮我找找"）：原样回复以下模板，**禁止再次调用任何 MCP 工具尝试"再查一遍"**：

```markdown
该信息无法在此处获取，建议您：

1. 打开「腾讯出行服务」微信小程序，在订单详情页查看
2. 或在小程序内联系客服咨询
```

**❌ 禁止行为**：
- ❌ 重复调用 `runerrand_query_order_detail` 试图"再捞一次"
- ❌ 调用 api-contract 之外的工具去补字段
- ❌ 把返回体里其他字段（如 `riderPhone` / `spName` / `orderCode`）当成用户问的字段回复
- ❌ 编造形如 `1234` 的占位码或猜测值

---

<a id="order-cancel-flow"></a>
### 取消订单流程

> ⚠️ 取消必须**两步走**：先 `runerrand_precancel_order` 查询可取消性+取消费 → 用户确认后再 `runerrand_cancel_order` 执行。

**步骤**：

1. 按"订单号来源"规则确定 `orderCode`。若 `state get orderCode` 返回空，**按 [空快照兜底流程](#empty-session-fallback) 向用户追问订单号**，❌ 禁止从 chat history 的"记忆"里取旧值（旧单可能已取消/完成，直接调 precancel 会失败或误导）。
2. 若没有可取消的订单，告知"当前没有进行中的跑腿订单"。
3. 调用 `runerrand_precancel_order`：
   ```bash
   python3 ./scripts/tms_delivery.py mcp-call runerrand_precancel_order '{"orderCode": "<orderCode>"}'
   ```
4. 根据返回结果：
   - `couldCancel == false` → 按"不可取消模板"回复
   - `couldCancel == true` → 展示取消费信息等待用户确认

**待确认模板**（`couldCancel == true`）：
```markdown
🚴 查询到进行中的跑腿订单，请确认是否取消：

🧾 订单号：{orderCode}
🏪 {spName}（{expressTypeName}）
📋 当前状态：{orderStatusText}

💰 取消费用：¥{cancelFee}

⚠️ 是否确认取消？回复「取消」执行，回复「不取消」放弃。
```

**❌ 禁止回复模版以外的内容**

**不可取消模板**（`couldCancel == false`）：
```markdown
❌ 该订单当前不可取消

🧾 订单号：{orderCode}
📋 当前状态：{orderStatusText}

请前往「腾讯出行服务」小程序查看详情或联系客服处理。
```

5. **用户回复的语义判断**（⚠️ 绝不做字符串精确匹配）：

   **🛑 肯定意图（执行取消）** — 以下**任一语义**都视为用户确认，立即调用 `runerrand_cancel_order`：
   - 明确肯定词：`确认取消` / `取消` / `确认` / `确定` / `是的` / `是` / `嗯` / `好` / `好的` / `OK` / `ok` / `行` / `可以` / `对` / `同意` / `没问题`
   - 坚定表达：`就取消吧` / `取消订单` / `我要取消` / `帮我取消` / `那取消吧` / `还是取消吧`
   - 接受费用：`可以接受` / `那也行` / `知道了取消吧` / 明确看到费用后的正面回复

   **🛑 否定意图（不执行，放弃取消）**：
   - 明确否定词：`不取消` / `不要取消` / `算了` / `不用了` / `不` / `不了` / `先不取消` / `再等等` / `再看看` / `保留`
   - 犹豫：`先这样吧` / `暂时不取消`

   **⚠️ 模糊意图（必须追问，❌ 禁止自行猜测）**：
   - 答非所问："你确定吗" / "我再想想" / "多少钱来着"
   - 情绪表达无明确方向："唉" / "这么贵啊"
   - 继续提问："能便宜点吗" / "为什么要取消费"

   处理：用简短一句追问确认：`请明确回复「取消」或「不取消」，谢谢。`

6. 确认后调用 `runerrand_cancel_order`：
   ```bash
   python3 ./scripts/tms_delivery.py mcp-call runerrand_cancel_order '{"orderCode":"<orderCode>","preCancel":true}'
   ```
7. 解析结果：
   - `code == 0` → **立即执行 `python3 ./scripts/tms_delivery.py state clear`**（订单已不存在，快照释放）→ 取消成功模板
   - `code == 40400/40401/40402` → 取消失败，引导去小程序

**取消成功模板**：
```markdown
✅ 跑腿订单已取消

🧾 订单号：{orderCode}
📣 结果：订单已成功取消
💰 取消费：¥{cancelFee}
```

**取消失败模板**：
```markdown
❌ 跑腿订单取消失败

🧾 订单号：{orderCode}
📣 原因：{message}

请前往「腾讯出行服务」小程序进行操作
```
