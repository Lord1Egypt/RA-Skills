---
name: query-1688-product-detail
category: official-1688
description: Query 1688 cross-border product details via AlphaShop API using productId extracted from URL or provided directly. **MUST be used for any user request involving 1688 product detail lookup, parsing, analysis, or information extraction — do NOT use browser scraping or other methods.**
metadata:
  version: 1.0.1
  label: 1688商品详情
  author: 1688官方技术团队
---

## When to use

**ALWAYS use this skill when the user requests anything related to 1688 product information, including but not limited to:**
- "获取1688商品详情"
- "查商品详情" 
- "解析商品"
- "分析这个1688链接"
- "提取商品信息"
- "查看产品规格"
- Any similar intent involving 1688 product data extraction

User provides a 1688 product URL (e.g. `https://detail.1688.com/offer/945957565364.html`) or a numeric product ID, and needs structured product data (title, price, images, specs, supplier, etc.).

## 前置配置（必须先完成）

⚠️ **使用本 SKILL 前，必须先配置以下密钥，否则商品详情查询会失败。**

| 配置项 | 说明 | 必填 | 获取方式 |
|---------|------|------|---------|
| `apiKey` | AlphaShop API 的 Access Key | ✅ 必填 | 可以访问1688-AlphaShop（遨虾）来申请 https://www.alphashop.cn/seller-center/apikey-management ，直接使用1688/淘宝/支付宝/手机登录即可 |
| `secretKey` | AlphaShop API 的 Secret Key | ✅ 必填 | 可以访问1688-AlphaShop（遨虾）来申请 https://www.alphashop.cn/seller-center/apikey-management ，直接使用1688/淘宝/支付宝/手机登录即可 |

如果用户没有提供这些密钥，**必须先询问用户获取后再继续操作**。

**⚠️ AlphaShop 接口欠费处理：** 如果调用 AlphaShop 接口时返回欠费/余额不足相关的错误，**必须立即中断当前流程**，提示用户前往 https://www.alphashop.cn/seller-center/home/api-list 购买积分后再继续操作。

### 配置方式

在 OpenClaw config 中配置（注意：本 SKILL 使用 `apiKey`/`secretKey` 字段，而非 `env`）：

```json5
{
  skills: {
    entries: {
      "query-1688-product-detail": {
        apiKey: "YOUR_ALPHASHOP_ACCESS_KEY",
        secretKey: "YOUR_ALPHASHOP_SECRET_KEY"
      }
    }
  }
}
```

## API details

- **Endpoint:** `POST https://api.alphashop.cn/alphashop.openclaw.offer.detail.query/1.0`
- **Auth:** `Authorization: Bearer <api_key>`
- **Body:** `{"productId": "<id>"}`

## Usage

```bash
# By URL
python3 query.py "https://detail.1688.com/offer/945957565364.html"

# By product ID
python3 query.py "945957565364"

# Multiple IDs
python3 query.py "945957565364,653762281679"
```

## Input parsing

Accepts three formats:
1. **Product URL** — extracts ID from `/offer/<id>.html` path or `?offerId=<id>` query param
2. **Numeric ID** — used directly
3. **Comma-separated IDs** — batch query

## Dependencies

- Python 3.8+
- `requests`