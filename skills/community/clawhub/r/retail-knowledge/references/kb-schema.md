# Knowledge Base Schema Reference

Full schema for the knowledge base populated by `retail-agent-setup` Step 03.

---

## Top-Level Structure

```json
{
  "products": [],
  "policy_entries": [],
  "promotions": [],
  "faqs": [],
  "store_info": {},
  "membership": {},
  "meta": {}
}
```

---

## products[]

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `sku` | string | ✅ | Unique product identifier |
| `name` | string | ✅ | Display name |
| `category` | string | ✅ | Top-level category |
| `subcategory` | string | — | Sub-category |
| `description` | string | ✅ | Full product description (key for Q&A) |
| `price` | number | ✅ | Regular retail price (CNY) |
| `sale_price` | number\|null | — | Active discount price; null if no active sale |
| `variants` | array | — | Size/color/etc. variants (see below) |
| `tags` | string[] | — | Search tags, keywords |
| `suitable_for` | string[] | — | Target audience descriptors |
| `stock_status` | string | — | `"live_api"` / `"daily_sync"` / `"static_count"` / `"unknown"` |
| `stock_qty` | number\|null | — | Quantity (null if live API) |
| `images` | string[] | — | Image URLs or local paths |

**variants item:**
```json
{ "attribute": "size", "values": ["S", "M", "L", "XL"] }
{ "attribute": "color", "values": ["红色", "白色", "黑色"] }
```

---

## policy_entries[]

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `policy_id` | string | ✅ | Unique ID (e.g., `"return_7day"`) |
| `title` | string | ✅ | Human-readable policy name |
| `type` | string | ✅ | `"return"` / `"warranty"` / `"promotion"` / `"faq"` / `"general"` |
| `keywords` | string[] | — | Lookup keywords |
| `conditions` | string[] | — | Conditions that must be met |
| `process` | string[] | — | Step-by-step process |
| `full_text` | string | ✅ | Complete policy text (LLM reads this for nuance) |
| `exceptions` | string[] | — | Explicit exclusions |
| `effective_date` | string\|null | — | ISO date when policy took effect |
| `source_doc` | string | — | Source filename |

---

## promotions[]

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `promo_id` | string | ✅ | Unique ID |
| `title` | string | ✅ | Promotion name |
| `type` | string | ✅ | `"discount"` / `"bundle"` / `"gift"` / `"threshold"` |
| `rules` | string | ✅ | Human-readable rule (e.g., "满300减50") |
| `applicable_to` | string[] | — | Applicable product scopes |
| `excluded` | string[] | — | Excluded items/categories |
| `start_date` | string | — | ISO date |
| `end_date` | string | — | ISO date; null = ongoing |
| `stackable` | boolean | — | Can stack with other promotions |
| `calculation_formula` | string | — | Machine-readable formula for `promotion-engine` skill |

---

## faqs[]

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `faq_id` | string | ✅ | Unique ID |
| `question` | string | ✅ | Canonical question text |
| `answer` | string | ✅ | Full answer |
| `category` | string | — | Domain category |
| `keywords` | string[] | — | Lookup keywords |
| `source_doc` | string | — | Source filename |

---

## store_info{}

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Store/brand name |
| `address` | string | Full address |
| `hours` | string | Business hours (human-readable) |
| `phone` | string | Customer service phone |
| `wechat_mp` | string | WeChat Official Account name |
| `mini_program` | string | Mini Program name |
| `parking` | string | Parking guidance (optional) |
| `transit` | string | Nearest transit (optional) |

---

## membership{}

| Field | Type | Description |
|-------|------|-------------|
| `enabled` | boolean | Whether membership system is active |
| `levels` | array | Tier definitions (name, threshold, benefits) |
| `points_rules` | string | How points are earned (e.g., "每消费1元得1积分") |
| `query_method` | string | How customers check their balance |
| `expiry_rules` | string | Point expiration policy |

---

## meta{}

| Field | Description |
|-------|-------------|
| `store_id` | Unique store identifier |
| `vertical` | Retail vertical (apparel/beauty/etc.) |
| `last_updated` | ISO timestamp of last KB update |
| `kb_score` | Last completeness score (0–100) |
| `agent_role` | Configured role ID |
