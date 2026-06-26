# 小智回收开放平台 API 参考文档

## 认证方式

使用微信小程序码授权登录。

**授权流程：**

1. 调用小程序码接口获取图片 URL，下载保存为本地图片
2. 用户用微信扫描小程序码，跳转小程序完成授权
3. 轮询 token 接口获取 admtoken
4. 将 token 传入下单接口 Header

**设备下单 Header：** `token`
**衣服询价：** 无需认证
**衣服下单 Header：** `jr_sso_token`

具体实现见 `scripts/create_order.py`。

## 小程序码接口

- **接口地址：** `POST https://api.bearhome.cn/api/product/product/fuwu/codePic`
- **Content-Type：** `application/json`

### 请求参数

```json
{
    "scene": "sendCode=23423423421113",
    "path": "userPages/login/index",
    "appletType": 4,
    "appType": 0
}
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `scene` | string | 小程序码参数，格式 `sendCode=<sendCode>` |
| `path` | string | 小程序页面路径，固定 `userPages/login/index` |
| `appletType` | int | 小程序类型，固定 `4` |
| `appType` | int | 应用类型，固定 `0` |

### 响应格式

```json
{
    "statusCode": 200,
    "data": "https://file.juranguanjia.com/qrcode/2026/06-16/xxx.jpg",
    "errorInfo": null
}
```

`data` 字段为小程序码图片 URL，需二次下载获取图片文件。

## Token 轮询接口

- **接口地址：** `https://api.bearhome.cn/hsapi/recovery/order/recoverComm/auth/getTokenByCode`
- **请求方式：** `GET`
- **参数：** `sendCode`（URL query 参数）

### 响应格式

授权等待中：
```json
{
    "statusCode": -1,
    "data": null,
    "errorInfo": "获取失败"
}
```

授权成功：
```json
{
    "statusCode": 200,
    "data": "admtoken_string",
    "errorInfo": null
}
```

---

## 一、设备品类（device）

### 创建回收订单

- **接口地址：** `https://papi.bearhome.cn/hs/app/order/open/used`
- **请求方式：** `POST`
- **Content-Type：** `application/json`
- **认证 Header：** `jr_sso_token`

#### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 联系人姓名 |
| `mobile` | string | 是 | 联系电话 |
| `prov_name` | string | 是 | 省份 |
| `city_name` | string | 是 | 城市 |
| `area_name` | string | 是 | 区/县 |
| `address` | string | 是 | 详细地址 |
| `item_brand` | string | 是 | 设备品牌 |
| `item_cates` | string | 是 | 设备品类 |
| `item_model` | string | 是 | 设备型号 |
| `sale_item_name` | string | 是 | 售卖商品名称（通常与 item_cates 一致） |
| `price` | string | 是 | 回收价格，默认 `0.01` |
| `source` | int | 是 | 来源渠道，默认 `172` |
| `remark` | string | 否 | 备注信息 |

#### 请求示例

```json
{
    "remark": "测试回收订单",
    "source": 172,
    "prov_name": "上海市",
    "city_name": "上海市",
    "area_name": "杨浦区",
    "price": "0.01",
    "address": "上海市上海市杨浦区测试用,请忽略！",
    "item_cates": "电视",
    "mobile": "15303126903",
    "item_brand": "小米",
    "sale_item_name": "电视",
    "item_model": "小米3代",
    "name": "赵先生"
}
```

---

## 二、衣服品类（clothing）

### 1. 询价接口

- **接口地址：** `https://api.bearhome.cn/hsapi/recovery/order/recoverOrder/queryPrice`
- **请求方式：** `POST`
- **Content-Type：** `application/json`
- **认证：** 无需

#### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `source` | int | 是 | 来源渠道，固定 `172` |
| `goodsType` | int | 是 | 商品类型，固定 `1` |
| `categoryId` | int | 是 | 品类ID，固定 `2767` |
| `provName` | string | 是 | 省份名称 |
| `cityName` | string | 是 | 城市名称 |
| `areaName` | string | 是 | 区县名称 |

#### 请求示例

```json
{
    "source": 172,
    "goodsType": 1,
    "categoryId": 2767,
    "provName": "山东省",
    "cityName": "潍坊市",
    "areaName": "高密市"
}
```

#### 响应示例

```json
{
    "statusCode": 200,
    "data": 0.60,
    "errorInfo": null
}
```

`data` 字段为单价（元/kg），总价 = 单价 × 重量。

---

### 2. 创建衣服回收订单

- **接口地址：** `https://api.bearhome.cn/hsapi/recovery/order/recoverOrder/createOrder`
- **请求方式：** `POST`
- **Content-Type：** `application/json`
- **认证 Header：** `jr_sso_token`

#### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 联系人姓名 |
| `mobile` | string | 是 | 联系电话 |
| `provId` | int | 是 | 省份行政编码 |
| `provName` | string | 是 | 省份名称 |
| `cityId` | int | 是 | 城市行政编码 |
| `cityName` | string | 是 | 城市名称 |
| `areaId` | int | 是 | 区县行政编码 |
| `areaName` | string | 是 | 区县名称 |
| `address` | string | 是 | 详细地址 |
| `source` | int | 是 | 来源渠道，固定 `172` |
| `inExpress` | int | 是 | 上门方式，固定 `2` |
| `inExpressTime` | string | 是 | 上门时间，格式 `YYYY-MM-DD HH:MM:SS` |
| `price` | float | 是 | 总价（单价 × 重量） |
| `detail` | string | 否 | 订单备注 |
| `orderItems` | array | 是 | 订单商品列表 |

##### orderItems 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `goodsType` | int | 是 | 固定 `1` |
| `itemCates` | string | 是 | 固定 `衣服` |
| `itemCatesId` | int | 是 | 固定 `2767` |
| `itemName` | string | 是 | 固定 `衣服` |
| `itemPrice` | float | 是 | 单价（来自询价接口） |
| `itemWeight` | float | 是 | 重量（kg） |

#### 请求示例

```json
{
    "address": "北苑路北",
    "areaId": 110105,
    "areaName": "朝阳区",
    "cityId": 110100,
    "cityName": "北京市",
    "inExpress": 2,
    "inExpressTime": "2026-06-16 16:00:00",
    "mobile": "15711111111",
    "name": "彭先生",
    "orderItems": [
        {
            "goodsType": 1,
            "itemCates": "衣服",
            "itemCatesId": 2767,
            "itemName": "衣服",
            "itemPrice": 0.60,
            "itemWeight": 11
        }
    ],
    "price": 6.6,
    "provId": 110000,
    "provName": "北京",
    "source": 172,
    "detail": "订单备注"
}
```

---

## 三、行政编码参考

衣服品类下单需使用 GB/T 2260 行政编码：

| 地区 | provId | cityId | areaId |
|------|--------|--------|--------|
| 北京市/北京市/朝阳区 | 110000 | 110100 | 110105 |
| 北京市/北京市/海淀区 | 110000 | 110100 | 110108 |
| 上海市/上海市/浦东新区 | 310000 | 310100 | 310115 |
| 广东省/广州市/天河区 | 440000 | 440100 | 440106 |
| 广东省/深圳市/南山区 | 440000 | 440300 | 440305 |

如需查找完整编码，脚本内置了主要城市的映射表，或可通过 `--prov-id` / `--city-id` / `--area-id` 手动指定。
