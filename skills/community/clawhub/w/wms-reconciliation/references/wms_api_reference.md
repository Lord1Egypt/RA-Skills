# WMS OpenAPI 接口参考（对接适配参考）

> **声明**：本文档由本技能作者基于对目标 WMS 系统 OpenAPI 的**实际接口调用测试**自行整理，非官方文档转载。
> 文中出现的接口端点名称、字段名、签名算法等均属**功能性技术信息**，引用目的仅为说明本技能的对账逻辑与对接方式。
> 所提及的系统名称及其商标归其各自所有者所有，本技能与该系统无任何隶属、背书或合作关系。

## 请求格式

- **请求方式**: POST
- **Content-Type**: application/json
- **Base URL**: 由仓库方提供，通常为 `https://{tenant}.系统域名.com/api/open/erp`

## 签名方法

```
Signature = MD5( MD5(jsonBody) + appSecret )
```

- `jsonBody`: 请求体JSON字符串（紧凑格式，无多余空格）
- `appSecret`: 仓库方提供的密钥

### 请求头

| Header | 说明 |
|--------|------|
| Content-Type | application/json |
| AppKey | 仓库方提供的AppKey |
| Signature | 按上述方法计算的签名 |

## 请求体公共参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| requestTimestamp | int (秒级) | 是 | **必须为秒级整数时间戳**，非毫秒、非字符串 |
| source | string | 否 | 可选参数，不传即可 |
| warehouseId | string | 是 | 仓库ID |
| cursor | string | 否 | 分页游标，从上一次响应中获取 |
| pageSize | int | 否 | 每页条数，默认50 |

## 核心API端点

### 1. 出库单查询

- **URI**: `/order/search_order_page`
- **用途**: 核对出库费、包装费
- **关键请求参数**: warehouseId, gmtCreateFrom, gmtCreateTo, cursor, pageSize
- **关键返回字段**:

| 字段 | 类型 | 说明 |
|------|------|------|
| orderId | string | WMS系统订单ID |
| platformOrderSn | string | 业务单号（平台订单号） |
| logisticsNo | string | 运单号 |
| logisticsCompany | string | 物流公司 |
| stage | string | 订单状态。`has_out_storage`=已出库 |
| gmtOutStorage | datetime | 出库时间 |
| waybillOssUrl | string | 面单PDF链接（不为空证明运单已生成） |
| holdUpStatus | int | 拦截状态。0=正常，3=有拦截 |
| closedReason | string | 关闭原因（为空=未关闭） |
| outStorageFee | string | 出库费 |
| packagingCost | string | 包装费（WMS系统记录值） |
| weight | number | 称重重量 |
| goodsCount | int | 商品件数 |

### 2. 退货单查询

- **URI**: `/warehouse_return_order/search_page`
- **用途**: 核对退件处理费
- **关键请求参数**: warehouseId, gmtCreateFrom, gmtCreateTo, cursor, pageSize
- **关键返回字段**:

| 字段 | 类型 | 说明 |
|------|------|------|
| warehouseReturnOrderId | string | 退货单ID |
| returnSn | string | RMA单号（业务单号） |
| platformOrderSn | string | 关联出库单业务单号 |
| trackingNo | string | 运单号 |
| tab | string | 状态。`finished`=已完成 |
| gmtSign | datetime | 签收时间 |
| gmtFinish | datetime | 完成时间 |
| gmtCreate | datetime | 创建时间 |
| goodsSkuList | array | 退货商品明细列表 |

**goodsSkuList 子字段**:

| 字段 | 类型 | 说明 |
|------|------|------|
| goodsSkuOuterId | string | 商品SKU编码 |
| signQuantity | int | 签收数量 |
| inStorageQuantity | int | **入库数量**（>0代表已实际入库） |
| inStorageGoodQuantity | int | 好品入库数量 |
| inStorageBadQuantity | int | 坏品入库数量 |
| discardQuantity | int | 销毁数量 |

### 3. 商品SKU查询

- **URI**: `/goods/search_goods_sku_page`
- **用途**: 验证仓租费涉及的SKU是否存在
- **关键返回字段**: goodsSkuOuterId, goodsSkuName, barcode等

### 4. 仓库列表

- **URI**: `/warehouse/search_warehouse_page`
- **用途**: 获取仓库ID
- **关键返回字段**: warehouseId, warehouseName

### 5. 备货单查询

- **URI**: `/replenishment_order/search_page`
- **用途**: 备货单查询
- **关键返回字段**: replenishmentOrderId, platformOrderSn等

## 分页机制

使用**游标分页**（cursor-based pagination）：

1. 第一次请求不传cursor
2. 响应中返回`cursor`字段
3. 下一次请求将上一次的cursor传入
4. 当cursor为null或空时，表示已获取全部数据

响应结构：
```json
{
  "result": "success",
  "data": {
    "list": [...],
    "total": 60,
    "cursor": "下一页游标"
  }
}
```

## 已知限制

1. **无财务明细端点**: OpenAPI不提供财务/账单明细查询接口，只能通过业务单据间接验证收费合理性
2. **无物流轨迹查询**: 无法查询运单的物流轨迹，"运单最终完成"以WMS系统内的出库状态为准
3. **库存查询可能返回空**: 库存查询接口对某些仓库可能返回0条（当前无库存时）
4. **时间范围过滤**: 使用`gmtCreateFrom`和`gmtCreateTo`按创建时间过滤，格式为 `YYYY-MM-DD HH:MM:SS`

## 常见问题

### requestTimestamp错误

**原因**: 时间戳格式不正确
**解决**: 必须使用 `int(time.time())` 获取秒级整数时间戳，不能用毫秒、字符串或datetime

### source可选值不在预期范围之内

**原因**: source参数值不在允许列表中
**解决**: source是可选参数，不传即可。如需传递，必须使用允许值列表中的值

### API返回空HTML而非JSON

**原因**: 端点URI不正确
**解决**: 确认使用正确的端点URI（如`/order/search_order_page`而非`/goods/detail`）
