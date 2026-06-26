<a id="error-handling-main"></a>
## 异常处理流程

### 1. 处理原则

异常流程用于处理工具调用失败、参数缺失、环境不一致等非主流程场景。出现异常时先停止当前主流程，进入对应修复流程；修复完成后返回主流程继续。

### 2. MCP 调用错误

| 错误类型 | 判断条件 | 处理动作 |
|----------|----------|----------|
| 网络错误 | 连接超时/拒绝 | 提示网络异常，引导重试 |
| 鉴权失败 | 鉴权相关错误 | 切换到 [Quick Start](./quick-start-workflow.md#quick-start-main) 重新配置 token |
| 参数错误 | code == 10001 | 对照 [api-contract.md](./api-contract.md) 修正入参 |
| 服务器异常 | code == 10000 | 提示"服务暂时不可用，请稍后重试" |
| 业务失败 | code == 40000 | 展示 message |

### 3. 业务错误码

**询价**：

| code | 说明 | 处理 |
|------|------|------|
| 40100 | 询价失败 | 展示 message，引导重试 |
| 400502 | 暂无可用预估结果 | "当前时段/地址暂无可接单的运力，建议换个时间或调整地址再询价" |
| 500200 | 起终点距离过远 | "超出跑腿配送范围，建议改用快递服务" |
| 500201 | 该地址暂不支持 | "起点或终点地址暂不支持跑腿配送，请更换地址后重试" |
| 500202 | 当前城市无可用运力 | "该城市暂未开通跑腿服务" |

**下单**：

| code | 说明 | 处理 |
|------|------|------|
| 40200 | 下单失败（通用） | 展示 message |
| 40201 | 需在小程序完成支付分授权 | "请先前往「微信」-「我」-「服务」-「出行服务」完成支付分授权" |
| 40202 | 存在未完成订单 | "您有一笔未完成的跑腿订单，请先处理。发送「查跑腿」查看详情" |
| 400310 | 进行中订单数量超限 | 展示 message 里的具体笔数（如"已有 2 笔进行中订单"），引导发送「查跑腿」查看详情 |
| 40203 | 存在未豁免的取消费订单 | "您有待处理的取消费订单，请前往小程序处理" |
| 40205 | 询价已过期 | **静默重询 + 二次让用户确认**，❌ 禁止静默代下单（详见 §5） |
| 40206 | 重复下单 | "请勿重复下单，发送「查跑腿」查看现有订单" |
| 40207-40211 | 风控拦截 | 展示 message，引导联系客服 |

**订单查询**：

| code | 说明 | 处理 |
|------|------|------|
| 40300 | 查询订单失败 | 提示稍后重试 |
| 40301 | 当前没有进行中的订单 | "当前没有进行中的跑腿订单" |
| 40302 | 无符合的用户数据 | "未找到您的跑腿订单记录" |

**取消订单**（两步流程：先 precancel 再 cancel）：

| code | 说明 | 处理 |
|------|------|------|
| 40400 | 取消订单失败 | 展示 message，引导去小程序 |
| 40401 | 获取取消规则失败 | 提示稍后重试 |
| 40402 | 确认取消订单失败 | 展示 message，引导去小程序 |

`runerrand_precancel_order` 特殊处理：
- `couldCancel == false` → 按不可取消模板回复，引导去小程序
- `couldCancel == true` → 展示 `cancelFee`（元），用户确认后再调 `runerrand_cancel_order`

**骑手追踪**：通过 `runerrand_query_order_detail` 实现，直接展示 `orderSuggestion`。

### 4. Token 失效处理

任意 MCP 调用返回鉴权错误时：
1. 中断当前流程
2. 切换到 [Quick Start](./quick-start-workflow.md#quick-start-main) 修复
3. 修复完成后返回用户原始意图对应流程

Quick Start §1.3 通过 `runerrand_query_going_order` 验证 token，失效时提示用户重新获取，从 [Quick Start §1.3](./quick-start-workflow.md#qs-check-ongoing) 重新校验。

### 5. 询价过期重试（⚠️ 下单前必须用户二次确认）

**🛑 触发来源有两处**：
1. **主路径（推荐）**：下单前调用 `select-sku` 返回 `status: "expired"`（即询价已超过 3 分钟新鲜窗口，或 `estimate_at` 缺失/时钟异常）
2. **兜底路径**：`runerrand_book_order` 返回 `code == 40205` / `510008`（预估价格已失效）

两条路径**处理流程完全一致**（三步强制），目的都是"重询价 + 让用户按新报价再确认"。主路径的优势是**把判断提前到用户刚选完序号时**，避免拿到"新 recordId + 旧 skuId"的易错组合。

**🚫 绝对禁止**：
- ❌ 禁止静默重新询价后**直接用旧 skuId / 新 estimatePriceRecordId 代用户下单**
- ❌ 禁止跳过"让用户看新报价"这一步
- ❌ 禁止把错误信息直接抛给用户（如"下单失败：询价已过期"）
- ❌ 禁止告诉用户"请重新报价"后就不管了

**为什么必须二次确认**：
- 价格可能已变化（优惠券、动态定价、时段差异） —— 旧 skuId ¥16.70，重询可能变成 ¥18.50
- 服务商可能下线 —— 旧 skuId 在新报价里可能根本不存在
- 预计送达时间可能变化 —— 高峰期 vs 平峰期差距大
- **用户最初只确认过旧那一笔报价，新报价必须让 TA 再看一遍再按确认**

**✅ 正确处理流程（三步强制）**：

```
STEP 1：静默重询价（用户不可见）—— 一条命令搞定
  python3 ./scripts/tms_delivery.py re-estimate

  该命令自动完成：
    ✅ 作废旧的 estimatePriceRecordId / skuMap / selectedSkuId / estimate_at
    ✅ 跳过 step3-entry 断言（允许 estimatePriceRecordId 非空进入）
    ✅ 调 MCP 询价 + 自动写入新的 estimatePriceRecordId + estimate_at
    ✅ v1.3.2+：自动生成并落盘新的 skuMap + display_rows（LLM 无需再手动 set skuMap）

  🚫 禁止改用 run-estimate：step3-entry 会因 estimatePriceRecordId 非空断言失败
  🚫 禁止手动调 mcp-call runerrand_estimate_price '{}'：参数为空会被服务端拒绝

  命令返回值已包含 reply_template（已含警示语 + markdown 表格），
  LLM 直接原样贴给用户即可，❌ 禁止再用编号嵌套列表，❌ 不输出任何内部状态文字给用户

STEP 2：原样贴出 reply_template（必须可见！）
  - reply_template 已含「⚠️ 报价已刷新」警示 + 完整 markdown 表格
  - 如果用户之前选过的服务商在新报价中仍存在，可在表格后追加一句"您之前选择的是 N 号"作辅助提示
  - ❌ 禁止静默代下单
  - ❌ 禁止改写表格成嵌套列表

STEP 3：等待用户重新选择（必须！）
  - 收到用户回复的新序号 → 调 `select-sku <新序号>`（已内嵌 skuId 落盘 + TTL 预检）
  - select-sku 返回 `status: ok` → 调用 runerrand_book_order
  - 收到用户"取消 / 算了" → 走 [用户中途退出](./delivery-workflow.md#delivery-exit-flow)
```

**❌ 绝对禁止偷懒静默重下单**：

```
（❌ 错误：静默自动重下单）
[内部] 收到 40205 → 自动重询 → 拿新 estimatePriceRecordId + 同一个旧 skuId → 重新 book_order → 成功 → 展示"下单成功"

这是严重违规：用户看到的"下单成功"对应的可能是比预期贵的订单。
```

**❌ 常见错误心态（每次看到 40205 都要警惕）**：
- "反正用户之前选过了，我自动重下一次省事" → ❌ 价格可能变了
- "新旧 skuId 一样就直接重下" → ❌ 仍然违规，价格仍可能变
- "重询后报价一模一样就不用确认了" → ❌ 仍然违规，这是信任边界问题，不是数值问题
- "只有价格变了才确认" → ❌ 规则简单好执行，任何 40205 都要走二次确认

> ✅ 硬约束：`book_order` 返回 40205 → 必走"重询 + 展示新报价 + 等用户按新序号" 三步，不管价格是否变化、不管旧 skuId 是否还在。

### 6. 用户中途退出（主动终止）

**触发**：用户在下单流程（第零步~第五步）中表达放弃（"算了/不寄了/退出/先不弄"）。

**处理**：
1. 执行 `python3 ./scripts/tms_delivery.py state clear` 释放 session.json 快照
2. **不调用任何 MCP 工具**（此时无订单，无需 `runerrand_cancel_order`）
3. 按 [中途退出模版](./delivery-workflow.md#delivery-exit-flow) 回复用户
4. 返回流程选择器等待下一个意图

**特殊情况**：已走到第六步（已有 orderCode）后用户说"取消" → 走 [取消订单流程](./order-workflow.md#order-cancel-flow)。

### 7. 进行中订单拦截

当用户想下新单但 Quick Start §1.3 返回有进行中订单时：
1. 按 [Quick Start §1.3.1](./quick-start-workflow.md#qs-block-on-ongoing) 模版展示现有订单
2. 禁止进入下单/询价流程
3. 引导用户先查询/取消现有订单
