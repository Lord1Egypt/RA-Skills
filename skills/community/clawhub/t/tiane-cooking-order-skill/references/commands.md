# 命令参考

本文档定义天鹅到家做饭钟点工 Skill 调用研发 CLI 的命令、入参、出参与主链路。所有执行必须以研发 CLI 文档为准；不得使用本文档未列出的命令名或参数。

## 执行方式

```bash
sh dist/run.sh <command> [args...]
```

## 主链路

```text
login
-> get_address_list / poi_search
-> product_query
-> inventory_time_slot
-> create_order
```

## 登录

### login

确认登录态。

```bash
sh dist/run.sh login
```

出参处理：

- 输出 `✅ 已登录`：继续后续流程。
- 否则执行 `login --force` 重新发起授权。

### login --force

重新获取授权链接。

```bash
sh dist/run.sh login --force
```

出参处理：

- 输出 `AUTH_LINK: <url>`：展示授权链接，让用户打开并完成授权。
- CLI 会把 `requestId`、`createdAt`、`expireAt`、`expiresInMs` 和本地 `sessionSavedAt` 写入授权 session 文件。

### confirm_auth

用户完成授权后确认授权结果。

```bash
sh dist/run.sh confirm_auth
```

出参处理：

- 授权成功：继续当前中断步骤。
- 授权失败、超时、取消：重新执行 `login --force`。
- 本地轮询窗口优先按 `sessionSavedAt + expiresInMs` 计算；服务端返回授权过期时，以服务端结果为准。

## 地址

### get_address_list

查询用户地址列表。

```bash
sh dist/run.sh get_address_list
```

出参使用：

- 从返回中读取可用地址。
- 后续必须保存并使用以下字段：
  - `cityId`
  - `poiname`
  - `doorNumber`
  - `gdLocation`

展示规则：

- 只向用户展示地址、门牌、联系人和脱敏电话。
- 不向用户展示字段名、JSON、坐标、Token 或接口路径。

### poi_search

当用户提供新地址或需要验证地址搜索时使用。

```bash
sh dist/run.sh poi_search --address-key-word 望京 --city-id 1
```

入参：

| 参数 | 必填 | 说明 |
|---|---|---|
| `--address-key-word` | 是 | 用户提供的地址关键词 |
| `--city-id` | 是 | 城市 ID，北京为 `1` |

出参使用：

- 成功标准：`code=0`，返回 `poiAddressList`。
- 从可用 POI 中读取后续下单需要的地址信息。

## 商品与规格

### product_query

查询商品与规格，获取可用 `specId`。

```bash
sh dist/run.sh product_query --service-id <serviceId> --city-id <cityId>
```

入参：

| 参数 | 必填 | 说明 |
|---|---|---|
| `--service-id` | 是 | 研发或商品查询确认的服务项 ID |
| `--city-id` | 是 | 地址返回或用户确认的城市 ID |

出参使用：

- 成功时返回中应包含 `products`。
- 必须从 `products` 中读取可用 `specId`，不得猜测规格 ID。
- 如果返回为空，说明当前 `serviceId + cityId` 组合暂无可用结果，需要更换一组可用业务参数。

## 库存时段

### inventory_time_slot

查询可预约库存时段。

```bash
sh dist/run.sh inventory_time_slot \
  --service-id <serviceId> \
  --city-id <cityId> \
  --gd-location <lng,lat> \
  --spec-id <specId> \
  --num 1
```

入参：

| 参数 | 必填 | 说明 |
|---|---|---|
| `--service-id` | 是 | 已确认服务项 ID |
| `--city-id` | 是 | 已确认城市 ID |
| `--gd-location` | 是 | 已确认地址坐标 |
| `--spec-id` | 是 | `product_query` 返回的规格 ID |
| `--num` | 是 | 数量，默认 `1` |
| `--query-stock-date` | 否 | 指定查询库存日期，格式 `yyyy-mm-dd` |

出参使用：

- 成功标准：`code=0`，`data.availableSlots` 中有可预约日期和可选开始时间范围。
- `data.availableSlots` 的 key 是可约日期，格式 `yyyy-MM-dd`；value 是当天可选开始时间范围列表。
- `data.inventorySummary` 是库存摘要，只用于辅助理解，不作为可选时间来源。
- `07:00-20:00` 表示当天 07:00 到 20:00 之间每 30 分钟一个可选开始时间，首尾都可选。
- 范围结束时间不是服务结束时间；服务结束时间需要用用户选择的开始时间加已选规格时长计算。
- 只能展示接口返回的可预约开始时间范围，不得编造时间。
- 用户选择具体开始时间后，必须保存已确认的日期和开始时间，用于下单。

出参示例：

```json
{
  "code": 0,
  "data": {
    "availableSlots": {
      "2026-06-10": [
        "07:00-20:00"
      ]
    },
    "inventorySummary": "已查询可约时间，起始日期 2026-06-10；最早可约 2026-06-10 07:00"
  }
}
```

## 下单

### create_order

创建订单。该命令会真实创建订单，必须在用户已确认订单预览后才能执行。

```bash
sh dist/run.sh create_order \
  --service-id <serviceId> \
  --city-id <cityId> \
  --poiname "<poiname>" \
  --door-number "<doorNumber>" \
  --gd-location <lng,lat> \
  --date <yyyy-mm-dd> \
  --time <HH:mm> \
  --spec-id <specId> \
  --num 1 \
  --user-price <price> \
  --remark "<remark>"
```

入参：

| 参数 | 必填 | 说明 |
|---|---|---|
| `--service-id` | 是 | 已确认服务项 ID |
| `--city-id` | 是 | 已确认城市 ID |
| `--poiname` | 是 | 已确认地址主地址 |
| `--door-number` | 是 | 已确认门牌号 |
| `--gd-location` | 是 | 已确认地址坐标 |
| `--date` | 是 | 已确认库存时段对应的日期，格式 `yyyy-mm-dd` |
| `--time` | 是 | 已确认库存时段对应的开始时间，格式 `HH:mm`，分钟只能是 `00` 或 `30` |
| `--spec-id` | 是 | 已确认规格 ID |
| `--num` | 是 | 数量，默认 `1` |
| `--user-price` | 是 | `product_query` 返回的选中规格 `price` |
| `--remark` | 否 | 用户主动提供的备注；没有备注时不传 |

CLI 会把 `--date` 和 `--time` 组合为生单接口入参 `serviceTime`，格式为 `yyyy-MM-dd HH:mm`。

出参展示：

- 订单号，如返回中存在。
- 支付链接，如返回中存在。
- 待支付金额，如返回中存在。
- 必须提示用户支付有效期或“如果未支付，订单可能自动取消”。
