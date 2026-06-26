# Step 01 — System Inventory

## Goal
Map the store's existing tech stack and assess API connectivity for each system.
This determines what data the agent can access in real-time vs. what must be imported manually.

---

## Interview Script

Ask the user to identify their tools across these 5 categories.
Use the catalog below to recognize system names even if mentioned informally.

### Category 1: POS System (Point of Sale)
> "What do you use at the register / cashier counter?"

| Vendor | Common Names | API Available |
|--------|-------------|---------------|
| 美团收银 | 美团、袋鼠收银 | ✅ REST API |
| 客如云 | 客如云POS | ✅ OpenAPI |
| 银豹收银 | 银豹 | ✅ API |
| 收钱吧 | 收钱吧、扫码枪 | ✅ API |
| 商米 | 商米POS、商米收银 | ✅ SDK |
| 拉卡拉 | 拉卡拉 | ✅ API |
| 微信支付收银台 | 微信收款 | ✅ via WeCom |
| Square | Square | ✅ REST API |
| Shopify POS | Shopify | ✅ REST/GraphQL |
| 自研系统 | 自己做的、定制系统 | ❓ Ask for docs |
| Excel/手工记账 | 手工、表格 | ❌ Manual import |

### Category 2: ERP / WMS (Inventory & Supply Chain)
> "What system do you use to manage inventory, purchasing, and warehousing?"

| Vendor | Common Names | API Available |
|--------|-------------|---------------|
| 管易云 | 管易、管易ERP | ✅ OpenAPI |
| 旺店通 | 旺店通、WDT | ✅ API |
| 金蝶云星空 | 金蝶、Kingdee | ✅ API |
| 用友U8/NC | 用友 | ✅ API (complex) |
| SAP Business One | SAP | ✅ REST (needs IT) |
| 有赞零售 | 有赞 | ✅ OpenAPI |
| 商派 | 商派、SHOPEX | ✅ API |
| 蜂鸟ERP | 蜂鸟 | ✅ API |
| 无系统 | 没有、自己管 | ❌ Manual import |

### Category 3: CRM / Membership System
> "How do you manage members, points, and customer records?"

| Vendor | Common Names | API Available |
|--------|-------------|---------------|
| 企业微信 | 企微、WeCom | ✅ OpenAPI |
| 微盟 | 微盟CRM | ✅ API |
| 有赞 | 有赞会员 | ✅ OpenAPI |
| 美团会员 | 美团 | ✅ API |
| 纷享销客 | 纷享 | ✅ API |
| 微信公众号 | 公众号粉丝 | ✅ via MP API |
| Excel会员表 | 表格、手工 | ❌ Manual import |
| 无会员系统 | 没有会员 | ❌ N/A |

### Category 4: E-Commerce Platforms (if omnichannel)
> "Do you also sell online? Which platforms?"

| Platform | API Available |
|----------|---------------|
| 天猫/淘宝 | ✅ TOP API |
| 京东 | ✅ JD API |
| 抖音小店 | ✅ API |
| 拼多多 | ✅ API |
| 微信小程序 | ✅ Mini Program API |
| 独立站 (Shopify) | ✅ REST/GraphQL |
| 无线上 | ❌ N/A |

### Category 5: Supply Chain & Procurement
> "How do you order from suppliers?"

| Method | Integration Level |
|--------|-----------------|
| 1688 / 阿里巴巴 | ✅ API available |
| 直接联系供应商 | ❌ No integration |
| 内部供应链系统 | ❓ Ask for docs |
| 品牌总部系统 | ❓ Varies by brand |

---

## Output Format

After collecting responses, produce a **System Inventory Card**:

```
╔══════════════════════════════════════╗
║  SYSTEM INVENTORY — [Store Name]     ║
╠══════════════════════════════════════╣
║ POS:        [System] — [API status]  ║
║ ERP/WMS:    [System] — [API status]  ║
║ CRM:        [System] — [API status]  ║
║ E-Commerce: [System] — [API status]  ║
║ Supply:     [System] — [API status]  ║
╠══════════════════════════════════════╣
║ Real-time data possible:  [list]     ║
║ Manual import needed:     [list]     ║
║ No data available:        [list]     ║
╚══════════════════════════════════════╝
```

Save this as `systems_inventory` in agent memory before proceeding to Step 02.

---

## Decision Logic

| API Status | Recommended Integration |
|------------|------------------------|
| ✅ Real-time API | Connect directly in Step 05 (Skills Config) |
| 📦 Batch export only | Schedule daily sync in Step 05 |
| ❌ No API / Manual | Import via file upload in Step 03 |
| ❓ Unknown | Note for IT follow-up; proceed with manual import for now |

If the store has **no digital systems at all**: note this, skip to Step 03 (manual data import),
and recommend starting with a knowledge-base-only agent (no live queries).
