# 订单状态文件 `~/.config/tms-takecar/state.json`

> 每次进入叫车流程时创建，用于临时存储当前订单状态。

## JSON 模版

```json
{
  "pickup": [],
  "dropoff": [],
  "estimate": null,
  "userPreferLabels": [],
  "orderId": null
}
```

## 字段说明

### `pickup` / `dropoff`

- 类型：数组
- 元素结构：与 `poi-search` 的 `result.body.items[]` 单项字段保持一致
- 元素字段：
  - `name`
  - `address`
  - `longitude`
  - `latitude`
  - `poiid`
  - `citycode`
  - `point_name`
  - `point_longitude`
  - `point_latitude`

写入规则：
1. 每次执行 `poi-search --scene 1/2`，脚本会向对应数组追加候选。
2. 追加时按 `poiid` 去重：已存在则覆盖，不存在则新增。
3. `scene=0` 不写 state。

收敛规则：
1. 用户确定具体地点后，必须执行 `select-poi --poiid <id> --scene <1|2>`。
2. `select-poi` 成功后，对应数组只保留 1 条（被选中的 `poiid`），其余删除。

### `estimate`

- 来源：`estimate-price` 成功后写入
- 关键字段：
  - `estimate.estimateKey`
  - `estimate.distance`
  - `estimate.estimateTime`
  - `estimate.products[]`
  - `estimate.userPreferLabels`

### `orderId`

- 来源：`create-order` 成功后写入

## 下游请求体取值映射（脚本自动构造）

### `estimate-price`

前置条件：
1. `pickup` 数组长度必须为 1（已完成 `select-poi --scene 1`）。
2. `dropoff` 数组长度必须为 1（已完成 `select-poi --scene 2`）。

取值映射：
- `cityCode` <- `pickup[0].citycode`
- `destCityCode` <- `dropoff[0].citycode`
- `fromLat` <- `pickup[0].point_latitude`
- `fromLng` <- `pickup[0].point_longitude`
- `fromName` <- `pickup[0].name`
- `fromAddress` <- `pickup[0].address`
- `toId` <- `dropoff[0].poiid`
- `toLat` <- `dropoff[0].point_latitude`
- `toLng` <- `dropoff[0].point_longitude`
- `toName` <- `dropoff[0].name`
- `toAddress` <- `dropoff[0].address`

### `create-order`

前置条件：
1. `pickup` 和 `dropoff` 均已收敛为单条候选。
2. `estimate.estimateKey` 非空。
3. `estimate.products` 中至少一项 `userSelect=1`。

取值映射：
- 地址相关字段同 `estimate-price`
- `estimateKey` <- `estimate.estimateKey`
- `productStr` <- 由 `estimate.products` 中 `userSelect=1` 自动构造
- `userPreferLabels` <- `estimate.userPreferLabels`

## 联动清理规则

- `select-poi` 成功后统一清空：
  - `estimate = null`
  - `userPreferLabels = []`
  - `orderId = null`
- `create-order --price-estimate-keys` 若提供该参数，会在发起请求前更新 `estimate.products[].userSelect`；若同时提供 `--user-prefer-labels`，也会更新 `estimate.userPreferLabels`。两者均为可选，不传时保留 state 原值。
