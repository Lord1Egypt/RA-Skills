# 样例 02 · 链接 / 口令解析

## 场景 A · 拼多多链接（v1 已支持）

### 用户操作
粘贴链接：

```
https://mobile.yangkeduo.com/goods.html?goods_id=123456789
```

### AI 调用

```bash
curl -s "https://xiaxiayouhui.xyz/api/skill/v1/parse-link?url=https%3A%2F%2Fmobile.yangkeduo.com%2Fgoods.html%3Fgoods_id%3D123456789"
```

### 服务端返回（mock）

```json
{
  "success": true,
  "platform": "pdd",
  "goods_id": "123456789",
  "goods_name": "Apple iPhone 17 Pro 256GB 黑色钛金属",
  "original_price": 8299.0,
  "min_price": 8299.0,
  "coupon_price": 8099.0,
  "coupon_amount": 200.0,
  "coupon_desc": "满 8200 减 200",
  "has_coupon": true,
  "mall_name": "Apple 官方旗舰店",
  "promotion_url": "https://xiaxiayouhui.xyz/go/pdd_a1b2c3",
  "same_item_compare": {
    "available": true,
    "cheapest": {
      "platform": "sn",
      "coupon_price": 7999.0,
      "promotion_url": "https://xiaxiayouhui.xyz/go/sn_x9y8z7"
    }
  },
  "version": "1.1.0"
}
```

### AI 渲染输出

> 🔗 **链接解析结果**（数据时效：刚刚）
>
> **Apple iPhone 17 Pro 256GB 黑色钛金属**（拼多多 · Apple 官方旗舰店）
>
> | 项 | 值 |
> |---|---|
> | 原价 | ¥8299 |
> | 隐藏券 | -¥200（满 8200 减 200）|
> | 券后价 | **¥8099** |
> | 操作 | [领券购买](https://xiaxiayouhui.xyz/go/pdd_a1b2c3) |
>
> 💡 **同款比价**：苏宁 ¥7999（比当前低 ¥100）→ [跳到苏宁](https://xiaxiayouhui.xyz/go/sn_x9y8z7)
>
> > 数据时效：刚刚 · 同款匹配仅供参考，请确认型号一致后再下单

---

## 场景 B · 京东链接（v1 待支持）

### 用户操作
粘贴：

```
https://item.jd.com/100012345678.html
```

### AI 调用

```bash
curl -s "https://xiaxiayouhui.xyz/api/skill/v1/parse-link?url=https%3A%2F%2Fitem.jd.com%2F100012345678.html"
```

### 服务端返回（当前阻塞）

```json
{
  "success": false,
  "platform": "jd",
  "platform_supported": false,
  "error": "京东链接解析正在路上，请用关键词搜索",
  "fallback_suggestion": {
    "action": "compare",
    "params": { "q": "<请用户提供商品关键词>" }
  },
  "version": "1.1.0"
}
```

### AI 应该怎么回复用户

> 京东链接解析功能正在路上 🚧
>
> 你可以告诉我商品关键词（比如商品名 / 品牌 / 型号），我帮你跨平台比价：
>
> 例如："iPhone 17 Pro" 或 "AirPods 4 主动降噪版"

---

## 场景 C · 淘口令（v1 待支持）

### 用户输入

```
￥XYZABC123￥
```

### AI 调用

```bash
curl -s "https://xiaxiayouhui.xyz/api/skill/v1/parse-link?url=%EF%BF%A5XYZABC123%EF%BF%A5"
```

### 服务端返回（待支持）

```json
{
  "success": false,
  "platform": "tb",
  "platform_supported": false,
  "error": "淘口令解析正在路上",
  "version": "1.1.0"
}
```

### AI 应该怎么回复用户

> 淘口令解析正在路上 🚧
>
> 你可以打开淘宝 App 自动识别口令后，把商品名复制给我，我帮你跨平台比价。
