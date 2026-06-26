---
name: "OPC电商公开接口 Skills"
description: >-
  仅用于OPC电商(众合鼎富)商品查询、下单与品物志（已发布商品故事）阅读。通过 curl 调用：
  1) 查询所有在售商品（无参数）
  2) 按商品名+数量下单（可多商品），并收集手机号/收货人/地址。
  3) 查询已发布的品物志故事列表（可选店铺/商品筛选）
  4) 按故事标题读取正文（可选商品名/店铺名消歧）
metadata: {"clawdbot":{"emoji":"🛍️","requires":{"bins":["curl"]}}}
---

# 众合鼎富电商公开接口（仅本项目）

## 接口

- 查询商品（无参数）  
  `GET https://tools.gangzheng.tech/public/products/search`

- 下单（按商品名，可多商品）  
  `POST https://tools.gangzheng.tech/public/orders/reserve`

- 品物志 · 已发布故事列表（可选 `shopId` 或 `shopName` 或 `productId`；均不传为全部）  
  `GET https://tools.gangzheng.tech/public/chronicles/list`

- 品物志 · 按标题读正文（必填 `title`；同名多篇时加 `productName` 或 `shopName`）  
  `GET https://tools.gangzheng.tech/public/chronicles/detail`

---

## 对话执行规则

1. 用户要看商品时，先查商品接口并返回结果；展示时带上 **品物志** 字段：`publishedStoryCount`（已发布故事篇数）。
2. 当某商品 `publishedStoryCount > 0` 时，在回复中自然引导一句，例如：「这款商品有品物志（商品故事），要不要读一篇了解一下？」若用户同意，再调用品物志列表或详情接口。
3. 用户完成下单、接口返回成功后，若订单里涉及的商品在之前的商品查询中有 `publishedStoryCount > 0`，可同样轻量引导是否品读品物志（不强迫）。
4. 用户说“买某商品”但未给数量时，必须追问数量。
5. 支持多商品输入（如“鲜肉饺子2份，三鲜水饺1份”）。
6. 下单前必须收集并确认：
   - 手机号 `phone`
   - 收货人`consignee`
   - 收货地址 `address`
7. 严格以接口返回为准，不虚构“下单成功”；品物志仅展示 **已发布** 内容，未发布的故事对用户不可见。

> 不需要注册账号，直接下单。

---

## 1) 查询在售商品

### curl

```bash
curl -s "https://tools.gangzheng.tech/public/products/search"
```

### 返回字段（data 每项）

- `productName`：商品名
- `unitPrice`：单价字符串（例：`¥28元/盒`）
- `stock`：库存
- `shopName`：店铺名
- `publishedStoryCount`：品物志 · **已发布** 商品故事篇数（可为 0）

---

## 2) 下单（按商品名）

### 请求体

```json
{
  "items": [
    { "productName": "鲜肉饺子", "quantity": 2 },
    { "productName": "三鲜水饺", "quantity": 1 }
  ],
  "phone": "13800138000",
  "consignee": "张三",
  "address": "广州市天河区体育西路1号"
}
```

### curl

```bash
curl -s -X POST "https://tools.gangzheng.tech/public/orders/reserve" \
  -H "Content-Type: application/json" \
  -d '{
    "items":[
      {"productName":"鲜肉饺子","quantity":2},
      {"productName":"三鲜水饺","quantity":1}
    ],
    "phone":"13800138000",
    "consignee":"张三",
    "address":"广州市天河区体育西路1号"
  }'
```

### 成功示例

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "orderNo": "20260422153030123000001",
    "totalAmount": 84.00,
    "message": "下单成功"
  }
}
```

### 失败示例（库存不足）

```json
{
  "code": 500,
  "msg": "商品「鲜肉饺子」库存不足",
  "data": null
}
```

---

## 3) 品物志 · 已发布故事列表

仅返回 **已发布**（对外可见）的故事目录。

### 查询参数（均可选）

- `productId`：商品 ID，只返回该商品的故事（优先级最高）
- `shopId`：店铺 ID，只返回该店下商品的故事
- `shopName`：店铺名称（与商品查询里的 `shopName` 一致），只返回该店下商品的故事；若与 `shopId` 同时传，以 `shopId` 为准
- 以上都不传：返回全部店铺、全部商品的已发布故事

### curl 示例

```bash
# 全部已发布故事
curl -s "https://tools.gangzheng.tech/public/chronicles/list"

# 某店铺（将 1 换成实际 shopId）
curl -s "https://tools.gangzheng.tech/public/chronicles/list?shopId=1"

# 某店铺（按名称，需与在售商品数据中的店铺名一致）
curl -s -G "https://tools.gangzheng.tech/public/chronicles/list" --data-urlencode "shopName=袁小妹饺子"

# 某商品（将 1 换成实际 productId，可先由商品查询对应名称再在后台或列表中确认 id）
curl -s "https://tools.gangzheng.tech/public/chronicles/list?productId=1"
```

### 返回字段（data 每项）

- `shopName`：店铺名称
- `productName`：商品名称
- `storyTitle`：故事标题
- `publishTime`：发表时间（ISO 日期时间）

---

## 4) 品物志 · 按标题读正文

### 查询参数

- `title`（必填）：故事标题，须与已发布记录 **完全一致**
- `productName`（可选）：商品名称，用于同名标题多篇时缩小范围
- `shopName`（可选）：店铺名称，用于同名标题多篇时缩小范围

若仅 `title` 且存在多篇同名已发布故事，接口会报错，需补充 `productName` 或 `shopName`。

### curl 示例

```bash
curl -s -G "https://tools.gangzheng.tech/public/chronicles/detail" \
  --data-urlencode "title=故事一·传家之志" \
  --data-urlencode "productName=鲜肉饺子"
```

### 返回字段（data）

- `title`：标题
- `content`：正文（HTML，与后台富文本一致）

---

## Notes

- 查询接口固定返回“在售且有库存”商品。
- 下单时服务端会校验在售与库存并自动扣库存。
- 同名商品若存在多个在售记录，接口会返回错误提示需进一步区分。
- 品物志列表与详情仅包含 **已发布** 故事；`publishedStoryCount` 与列表统计一致。
