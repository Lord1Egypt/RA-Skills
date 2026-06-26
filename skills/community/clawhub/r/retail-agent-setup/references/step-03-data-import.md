# Step 03 — Data Import & Auto-Structuring

## Goal
Ingest raw store data in any format, parse it into structured knowledge-base entries,
and score completeness. The agent should be able to answer real questions after this step.

---

## Accepted Input Methods

### Method A: File Upload
Accept any of these formats. For each, use the corresponding parse script.

| Format | Content Type | Script |
|--------|-------------|--------|
| `.xlsx` / `.xls` / `.csv` | Product catalog, price list, staff list, promo table | `scripts/parse_products.py` |
| `.pdf` | Policy docs, training manuals, brand guides | `scripts/parse_policy.py` |
| `.docx` / `.doc` | Policy docs, FAQs, procedures | `scripts/parse_policy.py` |
| Image (`.jpg`/`.png`) | Printed price lists, handwritten policies | Use `image` tool to OCR then feed to `parse_policy.py` |
| `.txt` | Any plain text | Direct ingestion — no script needed |

### Method B: API Connection
If systems from Step 01 have ✅ API status, configure a live connector:
- Provide API credentials (key/secret or OAuth)
- Run a test fetch to validate connection
- Set sync schedule (real-time webhook / hourly / daily)
- Document in `systems_inventory.api_connections`

### Method C: Paste / Type
For short content (< 500 words): accept pasted text directly. Parse inline.
Best for: store hours, a few FAQs, simple return policy.

---

## Structuring Rules by Data Type

### Product Entries
Each product entry should be normalized to this schema:

```json
{
  "sku": "string",
  "name": "string",
  "category": "string",
  "subcategory": "string",
  "description": "string",
  "price": number,
  "sale_price": number | null,
  "variants": [
    { "attribute": "size", "values": ["S","M","L","XL"] },
    { "attribute": "color", "values": ["红","白","黑"] }
  ],
  "tags": ["string"],
  "suitable_for": ["string"],
  "stock_status": "live_api | static_count | unknown",
  "images": ["url_or_path"]
}
```

**Inference rules** (apply when fields are missing):
- No description → generate from name + category + tags (flag as AI-generated for review)
- No category → infer from name using retail taxonomy
- No variants → set `variants: []`

### Policy Entries
Each policy is stored as a structured rule block:

```json
{
  "policy_id": "return_7day",
  "title": "7天无理由退货政策",
  "keywords": ["退货", "退款", "7天", "无理由"],
  "conditions": ["购买后7天内", "商品未使用", "保留吊牌"],
  "process": ["联系客服 → 提供订单号 → 寄回商品 → 3个工作日退款"],
  "exceptions": ["促销商品不适用", "定制品不适用"],
  "effective_date": "2024-01-01",
  "source_doc": "退换货政策.pdf"
}
```

### Promotion Entries
```json
{
  "promo_id": "summer2024",
  "title": "夏日大促",
  "type": "discount | bundle | gift | threshold",
  "rules": "满300减50",
  "applicable_to": ["全场", "夏季新品"],
  "excluded": ["已打折商品"],
  "start_date": "2024-07-01",
  "end_date": "2024-07-31",
  "stackable": false
}
```

### FAQ Entries
```json
{
  "faq_id": "faq_001",
  "question": "如何查询会员积分？",
  "answer": "可以通过微信公众号→会员中心→我的积分查询，或者告诉门店员工您的手机号查询。",
  "category": "membership",
  "keywords": ["积分", "会员", "查询", "余额"]
}
```

---

## Auto-Structuring Workflow

1. **Detect file type** — check extension + content
2. **Run appropriate script** or OCR
3. **Normalize to schema** — fill what's there, mark blanks as `null`
4. **Infer missing fields** — apply inference rules above
5. **Flag low-confidence entries** — entries with >3 null required fields
6. **Present summary** — show entry count, field coverage, flagged items
7. **Prompt for gap-filling** — show the top 3 most impactful missing fields

---

## Gap-Filling Prompts

After parsing, prompt the user to fill critical gaps:

| Gap | Prompt |
|-----|--------|
| No product descriptions | "I found [N] products without descriptions. Can you describe a few key ones, or share a product brochure?" |
| No return policy | "I don't have a return/exchange policy yet. Can you paste or upload yours?" |
| No current promotions | "What promotions or discounts are currently running?" |
| No staff/escalation contact | "Who should I escalate urgent issues to? Name + WeChat/phone?" |
| No store hours | "What are your store hours?" |

---

## Completeness Score

Run `scripts/score_knowledge.py` after import. Score is 0–100:

| Score | Meaning | Recommendation |
|-------|---------|----------------|
| 80–100 | Ready | Proceed to Step 04 |
| 60–79 | Usable | Proceed, but schedule gap-fill session |
| 40–59 | Partial | Fill top 3 gaps before proceeding |
| < 40 | Too sparse | Stop; collect more data before continuing |

Score is displayed as:
```
Knowledge Base Score: 72/100
✅ Products (85%)   ✅ Policies (90%)   ⚠️ Promotions (40%)
❌ Staff (0%)       ✅ Store Info (100%)  ⚠️ FAQs (55%)
```
