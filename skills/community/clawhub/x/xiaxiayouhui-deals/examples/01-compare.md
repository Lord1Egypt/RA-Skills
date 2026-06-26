# 样例 01 · 跨平台比价

## 用户问

> "iPhone 17 Pro 哪里买便宜？"

## AI 调用

```bash
curl -s "https://xiaxiayouhui.xyz/api/skill/v1/compare?q=iPhone+17+Pro&platforms=pdd,sn,jd,tb,vip,dy&limit=5"
```

## 服务端返回（节选 mock）

```json
{
  "success": true,
  "keyword": "iPhone 17 Pro",
  "platforms": [
    {
      "platform": "pdd",
      "success": true,
      "third_party": false,
      "count": 3,
      "items": [
        {
          "platform": "pdd",
          "goods_id": "123456789",
          "goods_name": "Apple iPhone 17 Pro 256GB 黑色钛金属",
          "goods_image": "https://img.pinduoduo.com/.../i.jpg",
          "original_price": 8299.0,
          "min_price": 8299.0,
          "coupon_price": 8099.0,
          "coupon_amount": 200.0,
          "coupon_desc": "满 8200 减 200",
          "has_coupon": true,
          "mall_name": "Apple 官方旗舰店",
          "sales": 12345,
          "promotion_url": "https://xiaxiayouhui.xyz/go/pdd_a1b2c3"
        }
      ]
    },
    {
      "platform": "jd",
      "success": true,
      "third_party": false,
      "count": 2,
      "items": [
        {
          "platform": "jd",
          "goods_id": "100012345678",
          "goods_name": "Apple iPhone 17 Pro 256GB 黑色钛金属",
          "coupon_price": 8349.0,
          "coupon_amount": 150.0,
          "coupon_desc": "店铺券 满 8500 减 150",
          "has_coupon": true,
          "mall_name": "Apple 京东自营旗舰店",
          "promotion_url": "https://xiaxiayouhui.xyz/go/jd_d4e5f6"
        }
      ]
    },
    {
      "platform": "vip",
      "success": true,
      "third_party": true,
      "count": 1,
      "items": [
        {
          "platform": "vip",
          "goods_name": "Apple iPhone 17 Pro 256GB 黑色钛金属",
          "coupon_price": 8299.0,
          "coupon_amount": 0,
          "has_coupon": false,
          "promotion_url": "https://xiaxiayouhui.xyz/go/vip_g7h8i9",
          "third_party": true
        }
      ]
    }
  ],
  "cheapest": {
    "platform": "pdd",
    "coupon_price": 8099.0,
    "goods_name": "Apple iPhone 17 Pro 256GB 黑色钛金属"
  },
  "elapsed_ms": 842,
  "version": "1.1.0"
}
```

## AI 渲染输出（用户最终看到）

> 🔍 **iPhone 17 Pro · 全网比价**（数据时效：刚刚 · 来源：xiaxiayouhui.xyz 聚合）
>
> | 平台 | 商品 | 原价 | 券 | 券后价 | 操作 |
> |------|------|------|------|--------|------|
> | 🥇 拼多多 | Apple iPhone 17 Pro 256GB 黑色钛金属 | ¥8299 | -¥200 | **¥8099** | [领券购买](https://xiaxiayouhui.xyz/go/pdd_a1b2c3) |
> | 京东 | Apple iPhone 17 Pro 256GB 黑色钛金属 | — | -¥150 | ¥8349 | [领券购买](https://xiaxiayouhui.xyz/go/jd_d4e5f6) |
> | 唯品会 ⓘ | Apple iPhone 17 Pro 256GB 黑色钛金属 | — | — | ¥8299 | [领券购买](https://xiaxiayouhui.xyz/go/vip_g7h8i9) |
>
> 🥇 当前已聚合的 3 个平台中最低：**拼多多 ¥8099**（比京东低 ¥250）
>
> > ⓘ = 数据来自第三方聚合源，价格仅供参考
> > 数据时效：刚刚抓取 · 价格随平台实时变动
> > 数据来自 xiaxiayouhui.xyz 聚合的各平台公开联盟开放平台。

---

## ⚠️ 边界场景 · 召回偏离/失败时的兜底渲染（2026-05-24 新增）

### 场景 X1：返回的全是配件而非主机

**用户问**：荣耀 Earbuds 耳夹式 Pro 哪里便宜？

**实测**（v1.5.1，2026-05-24）：6 平台合并仅 5 条，全是「保护套 / 防丢链 / 充电仓」配件，单价 18~28 元。

**AI 应该这样回（不要假装找到了主机）**：

> ⚠️ **召回偏离提示**
>
> 我搜了 6 个平台的「荣耀 Earbuds 耳夹式 Pro」，召回的商品**全部是保护套、收纳盒等配件**，不是耳机主机：
>
> | 平台 | 商品 | 券后价 | 类型 |
> |------|------|--------|------|
> | 拼多多 | 荣耀 Earbuds 保护套硅胶 | ¥18 | ⚠️ 配件 |
> | 拼多多 | 荣耀 Earbuds 防丢链 | ¥22 | ⚠️ 配件 |
>
> **可能的原因**：这是 2025 末新品，联盟池里销量低、权重低；当前接入的是个人主体联盟一级权限，数据池有限。
>
> **建议**：直接到「荣耀官方旗舰店」（淘宝 / 京东 / 拼多多）搜「Earbuds 耳夹式 Pro」，新品官旗优先。

### 场景 X2：所有平台 0 条

**实测**：`q="荣耀耳夹耳机"` 6 平台全 0 条。

**AI 应该这样回**：

> 我搜了 6 个平台的「荣耀耳夹耳机」，**没找到匹配商品**。
>
> 建议：
> - 加品牌+型号，例如「**荣耀 Earbuds 耳夹式 Pro**」
> - 或者去掉品类词，例如「**荣耀 Earbuds**」
>
> 要不要换一个关键词重试？

### 场景 X3：手机壳混入主机比价

**实测**（v1.5.1）：cheapest 命中拼多多「全包拍照按键苹果 17 手机壳液态硅胶」¥22.8。

**AI 应该这样回**：

> 🔍 **iPhone 17 Pro · 全网比价**（数据时效：刚刚）
>
> | 平台 | 商品 | 券后价 | 类型 |
> |------|------|--------|------|
> | ⚠️ 拼多多 | 全包拍照按键苹果 17 手机壳液态硅胶 ⚠️ | ¥22.8 | 配件，已下沉 |
> | 🥇 苏宁 | Apple iPhone 17 Pro 256GB | **¥8299** | ✅ 主机 |
> | 京东 | Apple iPhone 17 Pro 256GB | ¥8349 | ✅ 主机 |
>
> ⚠️ 关键词命中了一些手机壳类配件，已自动下沉。真实最低价主机：**苏宁 ¥8299**。
>
> [苏宁 领券购买](https://xiaxiayouhui.xyz/go/sn_xxx)
>
> > 数据时效：刚刚 · 价格随平台实时变动

### 实施说明（迭代后会自动生效）
- v1.5.2 后端会对配件类商品 `_match_score *= 0.1`，配件自动排到末尾或被过滤
- AI 渲染层仍需检查 `_match_score < 0.5` 的 item 标 ⚠️，配件命中词列表与后端一致
- 极端情况（全是配件 / 全 0 条），按 X1 / X2 模板兜底
