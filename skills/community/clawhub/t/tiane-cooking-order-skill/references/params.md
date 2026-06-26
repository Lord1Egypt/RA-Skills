# 参数说明

本文档定义天鹅到家做饭钟点工 Skill 的参数收集、展示和传递规范。研发 CLI 文档是最高优先级；本文只解释如何把用户信息映射到研发 CLI 要求的入参。

## 登录态

所有业务命令执行前必须先确认登录态：

```bash
sh dist/run.sh login
```

未登录或登录失效时，必须先完成 `login --force` 和 `confirm_auth`，不得继续查询地址、商品、库存或下单。

Agent 不展示、不记录、不要求用户手动提供 Token。

## 业务参数来源

| 参数 | 来源 | 用途 |
|---|---|---|
| `serviceId` | 研发提供或商品配置确认 | `product_query`、`inventory_time_slot`、`create_order` |
| `cityId` | 地址返回或用户确认城市，北京常用 `1` | 地址搜索、商品、库存、下单 |
| `poiname` | `get_address_list` 或 `poi_search` 返回 | 下单地址主地址 |
| `doorNumber` | `get_address_list` 或用户补充门牌 | 下单门牌号 |
| `gdLocation` | `get_address_list` 或 `poi_search` 返回 | 库存、下单坐标，格式 `<lng,lat>` |
| `specId` | `product_query` 返回 | 库存、下单规格 |
| `date` | `inventory_time_slot` 返回的可约日期和用户选择确认 | 下单日期，格式 `yyyy-mm-dd` |
| `time` | 用户在可约开始时间范围内选择确认 | 下单开始时间，格式 `HH:mm` |
| `num` | 默认 `1` | 库存、下单数量 |

不得猜测 `serviceId`、`specId`、`gdLocation`、`date`、`time`。这些参数必须来自研发 CLI 返回或用户明确提供并经 CLI 验证。

## 地址参数

### 地址列表

查询地址：

```bash
sh dist/run.sh get_address_list
```

从返回里拿后续必需字段：

```text
cityId
poiname
doorNumber
gdLocation
```

展示给用户时只展示可读信息：

```text
① {地址}-{门牌号}
　　{联系人} · {脱敏电话}
```

### 地址搜索

用户提供新地址或地址关键词时：

```bash
sh dist/run.sh poi_search --address-key-word <关键词> --city-id <cityId>
```

成功标准：

- `code=0`
- 返回 `poiAddressList`

从 `poiAddressList` 中选择地址后，仍需确认或补齐门牌号。

## 规格参数

规格 ID 必须通过商品查询获得：

```bash
sh dist/run.sh product_query --service-id <serviceId> --city-id <cityId>
```

成功时从 `products` 中读取可用 `specId`。如果 `products` 为空，不得继续库存查询或下单；需要更换可用业务参数。

给用户展示规格时，应展示用户可理解的信息，例如服务时长、菜数、价格；不得展示 `specId`。

默认规格文案：

```text
请选择本次做饭服务规格：

1. 2 小时（2-4 个菜，适合1-2人）
2. 3 小时（4-6 个菜，适合2-3人）
3. 4 小时（5-8 个菜，适合3-5人）

请回复数字。如果有其他菜数要求，请直接告诉我，如：8个菜。
```

如果 `product_query` 返回的规格、菜数或价格与默认文案不同，必须以接口返回为准。

## 库存时段参数

查询库存：

```bash
sh dist/run.sh inventory_time_slot \
  --service-id <serviceId> \
  --city-id <cityId> \
  --gd-location <lng,lat> \
  --spec-id <specId> \
  --num 1
```

可选指定日期：

```bash
sh dist/run.sh inventory_time_slot \
  --service-id <serviceId> \
  --city-id <cityId> \
  --gd-location <lng,lat> \
  --spec-id <specId> \
  --num 1 \
  --query-stock-date <yyyy-mm-dd>
```

出参处理：

- 成功标准：`code=0`，`data.availableSlots` 中有可预约日期和可选开始时间范围。
- 只能展示 `data.availableSlots` 返回的可约开始时间范围，不得编造时间。
- `data.inventorySummary` 只作为库存摘要，不作为可选时间来源。
- `07:00-20:00` 表示当天 07:00 到 20:00 之间每 30 分钟一个可选开始时间，首尾都可选。
- 范围结束时间不是服务结束时间；服务结束时间 = 用户选择的开始时间 + 已选规格时长。
- 用户选择具体开始时间后，保存已确认的日期和开始时间作为下单入参。
- 仅接受整点或半点开始时间；如果用户给出其他分钟，必须提示改选整点或半点。

展示模板：

```text
请选择上门时间：

1. {日期} 可约开始时间：{开始时间范围}
2. {日期} 可约开始时间：{开始时间范围}

请直接告诉我具体开始时间，例如“8点”“10点半”。
```

## 下单参数

下单命令：

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

下单前必须已经确认：

- 服务项
- 规格
- 服务地址
- 门牌号
- 服务时间
- 费用，必须取自 `product_query` 返回的选中规格 `price`
- 备注，如用户主动提供

用户主动提供备注时，下单命令必须携带 `--remark`；没有备注时不传。

CLI 会把 `--date` 和 `--time` 组合为生单接口入参 `serviceTime`，格式为 `yyyy-MM-dd HH:mm`。

## 订单确认卡片字段

生成卡片时必须包含：

```text
服务名称：{服务名称}
城市：{城市}
服务地址：{服务地址}
规格：{服务时长/菜数}
服务时间：{时间}
服务费用：{费用}
备注：{备注；没有备注时不展示本行}
```

确认卡片展示后不得自动生单。必须等用户明确回复“确认”后，才能执行 `create_order`。

## 城市参数

当前常用北京 `cityId=1`。如果用户提到其他城市，必须先通过地址返回或研发可用业务参数确认城市 ID，不得自行猜测。
