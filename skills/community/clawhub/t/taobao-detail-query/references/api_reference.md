# API 参考文档

## 接口信息

本技能通过调用第三方API服务提供商 **EarlyData (mi.earlydata.com)** 来获取淘宝/天猫商品的详情数据。

**API 配置信息:**
- **API Endpoint:** `https://mi.earlydata.com/detail`
- **API 版本:** 6.0

---

## 请求参数

### `get_tb_detail`

查询淘宝/天猫商品详情。

- `itemId` (string, **必需**): 商品ID
- `v` (string, **必需**): API版本号，固定为 `6.0`

---

## 返回结果

### 成功响应

返回商品详情数据，包含以下字段：

- `success` (boolean): 请求是否成功
- `data` (object): 商品详情数据
  - `title` (string): 商品标题
  - `price` (number): 商品价格
  - `monthSales` (number): 月销量
  - `totalSales` (number): 总销量
  - `images` (array): 商品图片列表
  - `sku` (array): SKU规格信息
  - `shopName` (string): 店铺名称
  - `shopId` (string): 店铺ID
  - 其他商品属性...

### 错误响应

- `success` (boolean): `false`
- `code` (string): 错误代码
- `message` (string): 错误描述

---

## 数据隐私与安全

1. 本技能仅发送商品ID到API服务器以获取商品信息数据
2. API调用使用HTTPS加密传输
3. 不会收集或存储用户的个人信息
4. 查询结果仅包含商品详情数据

---

## 技术实现

- 使用Python `requests`库进行HTTP请求
- 自动解析淘宝/天猫商品链接中的商品ID
- 处理网络异常和API错误响应

---

## 支持

如果您需要更换API服务提供商或使用自定义API配置，请联系 marketing@earlydata.com 获取支持。