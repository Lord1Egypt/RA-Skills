<a id="order-workflow-main"></a>
## 订单流程

适用于以下用户诉求：
- 查询订单
- 取消订单
- 查询司机位置

### 路由规则

- 用户要查看订单状态、订单进度、订单详情：进入 [订单查询流程](#order-query-flow)
- 用户要取消当前订单：进入 [取消订单流程](#order-cancel-flow)
- 用户要查看司机位置、司机实时位置、司机到哪了：进入 [司机位置查询流程](#driver-location-flow)

<a id="order-query-flow"></a>
### 订单查询流程

**步骤：**

1. 先告知用户将为其查询当前订单状态。
2. 调用工具查询订单详情：
   ```
  python3 ./scripts/tms_takecar.py query-order
   ```
   （脚本内部会自动查询进行中的订单 ID）
3. 解析 `query-order` 返回的 `result.body`：
  - 退出码为 `5` 或 `code != 0` 或 HTTP 错误 → 按 [异常处理流程](./error_handling.md#error-handling-main) 处理
  - `code == 0` → 提取 `data` 字段，按下方模板回复用户
4. **禁止编造**订单信息，所有字段均来自工具返回。
5. **❌ 禁止回复模版以外的内容**

**回复模板：**

```markdown
📋 订单状态：{statusDesc}

📍 {startName} → {endName}
🧾 订单号：{orderId}

🚗 车辆信息
  {brand} {model}（{color}）
  车牌：{plate}

👤 司机信息
  {driver.name}　{driver.phone}

💰 费用
  预估：约 {estimatePrice} 元
```

**字段说明：**
- `statusDesc`：直接来自 `data.statusDesc`，是后端返回的可读描述。
- 司机和车辆字段来自 `data.driver` 和 `data.vehicle`；若这两组字段均为空（订单还未被接受），则省略「🚗 车辆信息」和「👤 司机信息」两行。
- `estimatePrice` 来自 `data.estimatePrice`；行程已结束时用 `data.cost.totalAmount` 替代，并改为「实际费用：{totalAmount} 元」。

<a id="order-cancel-flow"></a>
### 取消订单流程

1. 先告知用户将为其查询是否存在进行中的订单并进行取消。
2. 默认先调用取消订单工具查询取消费：
  ```
  python3 ./scripts/tms_takecar.py cancel-order [--reason <reason>]
  ```
  （脚本内部会自动查询进行中的订单 ID；若无订单则返回错误码 `5`）
3. 解析取消结果：
  - 退出码为 `5` 或 HTTP 错误 → 按 [异常处理流程](./error_handling.md#error-handling-main) 处理。
  - CLI 返回 `mode == cancel_fee_required` → 按「待确认模板」告知用户取消费用，并等待用户确认。
  - CLI 返回 `mode == cancelled` → 按「免取消费自动取消成功模板」回复用户。
  - 其他情况视为取消失败，按「取消失败模板」回复用户，并按 [异常处理流程](./error_handling.md#error-handling-main) 处理。
4. 用户明确确认承担取消费用后，再调用：
  ```
  python3 ./scripts/tms_takecar.py cancel-order --confirm [--reason <reason>]
  ```
5. 解析第二次取消结果：
  - `code != 0` 或 HTTP 错误 → 按 [异常处理流程](./error_handling.md#error-handling-main) 处理。
  - `code == 0` → 按「确认后取消成功模板」回复用户。
6. **❌ 禁止回复模版以外的内容**

**待确认模板：**

```markdown
🚕 已查询到进行中的订单，请确认是否取消：

- 💰 取消费用：{amount_yuan} 元

如需继续取消，我将按你的确认执行。
```

**免取消费自动取消成功模板：**

```markdown
✅ 订单已取消

- 📣 结果：本次取消无需支付取消费，已为你直接取消
```

**确认后取消成功模板：**

```markdown
✅ 订单取消成功

- 📣 结果：已按你的确认完成取消
- 💰 取消费用：{amount_yuan} 元
```

**取消失败模板：**

```markdown
❌ 订单取消失败，你可以到**腾讯出行服务小程序**进行进一步操作

- 📣 原因：{message}
```

说明：
- 待确认模板中的 `amount_yuan` 来自第一次 `cancel-order` 返回的 `amount / 100`。
- 默认第一次 `cancel-order` 直接返回 `mode == cancelled` 时，表示无需支付取消费，agent 不需要再次向用户确认。
- 成功模板不再依赖旧字段 `successMessage`，以 `cancel-order` 或 `cancel-order --confirm` 返回成功为准。
- **❌ 禁止回复模版以外的内容**

<a id="driver-location-flow"></a>
### 司机位置查询流程

1. 先告知用户将为其查询司机位置。
2. 调用司机位置接口：
  ```bash
  python3 ./scripts/tms_takecar.py query-driver-location
  ```
  （脚本内部会自动查询进行中的订单 ID；若无订单则返回错误码 `5`）
3. 解析 [`query-driver-location`](./api-contract.md#cmd_query_driver_location) 的 `result.body`：
  - 退出码为 `5` 或 `code != 0` 或 HTTP 错误 → 按 [异常处理流程](./error_handling.md#error-handling-main) 处理。
  - `code == 0` 且 `data.driverLocation` 非空 → 已成功获取司机位置，按下方模板回复用户
  - `code == 0` 且 `data.driverLocation` 为空 → 检查 `data.orderStatus`：
    - 若 `orderStatus` 属于 `2`（等待接驾）、`3`（司机已到达）、`4`（行程开始）→ 返回相应状态说明
    - 若 `orderStatus` 不属于以上状态 → 按订单状态告知用户无法查询司机位置（如订单已完成、已取消等）
4. **❌ 禁止回复模版以外的内容**

**司机位置回复模板：**

```markdown
🚕 司机接驾中

- 📋 订单状态：{orderStatus描述}
- 📏 司机距离：{eda} 米
- ⏱️ 预计到达时间：约 {eta} 分钟
```

**orderStatus 状态描述对照：**
| orderStatus | 描述 | 是否可查询司机位置 |
|---|---|---|
| 2 | 等待接驾（司机已接单） | ✅ 可查询 |
| 3 | 司机已到达 | ✅ 可查询 |
| 4 | 行程开始（行程中） | ✅ 可查询 |
| 其他 | 订单未派单/已完成/已取消等 | ❌ 无法查询 |

**字段说明：**
- `orderStatus`：来自 [`query-driver-location`](./api-contract.md#cmd_query_driver_location) 返回的 `data.orderStatus`
- `eda`、`eta`：来自 `query-driver-location` 的 `data.eda`（单位米）、`data.eta`（单位分钟）
- `location`：来自 `query-driver-location` 的 `data.driverLocation.location`，格式 `longitude,latitude`；模板中的 `{location_longitude}` 和 `{location_latitude}` 由该字段拆分得到
- `locationTime`、`direction` 可用于补充说明，但不要求在模板中强制展示
