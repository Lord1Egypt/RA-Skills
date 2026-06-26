# SEO Product Auditor — Setup Guide

## Step 1 — API scopes needed

If you already have the Shopify Product Uploader or Order & Returns Manager installed,
you likely have these already. Check and add any missing ones:

Go to Shopify Admin → Settings → Apps → your custom app → Configure Admin API scopes.

| Scope | Why it's needed |
|-------|----------------|
| `read_products` | Fetch product titles, descriptions, tags, images for auditing |
| `write_products` | Push rewritten titles, descriptions, tags, image alt text, and product metafields |
| `write_metafields` | Explicit metafield write access — add only if you receive a 403 when updating SEO meta title or description |

Note: `read_content`, `write_content`, `read_metaobjects`, and `write_metaobjects`
are not the correct scopes for product metafields. Use `write_products` as the
primary scope — it covers `global.title_tag` and `global.description_tag` on
API versions 2023-04 and later. Add `write_metafields` only if needed.

---

## Step 2 — Configure the skill

If you've already set up the Shopify Product Uploader, the skill will reuse your
existing store credentials automatically.

If this is your first skill, send your OpenClaw bot:
```
Set my store for SEO audit:
Store: my-store-name
Token: shpat_xxxxxxxxxxxxxxxxxxxx
Store name: The Wool House
```

---

## Step 3 — Run your first audit

```
audit my store
```

The skill will scan all products, score them against 10 SEO criteria, and show you
the worst-performing listings with a prioritised fix list.

For large stores (500+ products), allow 3–5 minutes for the initial scan.

---

## Step 4 — Fix the worst listings

```
fix top 10
```

Reviews proposed changes before pushing. Nothing is updated without your confirmation.

---

## WooCommerce setup

Send:
```
Set my WooCommerce for SEO audit:
Platform: woocommerce
Domain: mystore.co.uk
Consumer key: ck_xxxxxxxxxxxxxxxxxxxx
Consumer secret: cs_xxxxxxxxxxxxxxxxxxxx
Store name: My Store Name
```

Note: WooCommerce SEO metafields (title, description) require the Yoast SEO plugin.
If Yoast is installed, meta updates will be flagged but must be applied via the Yoast
REST API or wp-admin — not directly via the WooCommerce REST API.

---

## Scoring explained

Each product is scored out of 100 across 10 criteria:

| Criterion | Max | Quick guide |
|-----------|-----|-------------|
| Title length | 15 | Aim for 40–70 characters |
| Keyword in title | 10 | Primary keyword in first 40 chars |
| Description length | 15 | 150–300 words is the sweet spot |
| Keyword in description | 10 | Keyword in the first sentence |
| Tags | 10 | 5–10 tags, not 0–2 |
| Images | 15 | 3+ images per product |
| SEO meta title | 10 | Set it — most stores haven't |
| SEO meta description | 10 | Set it — most stores haven't |
| Image alt text | 5 | Helps accessibility and image search |
| UK English | — | Flag only — fixed on rewrite |

**Score bands:**
- 85–100 ✅ Good
- 65–84  🟡 Fair
- 40–64  🟠 Weak
- 0–39   🔴 Poor — fix immediately

---

## Troubleshooting

**"Products not loading"**
→ Check `read_products` scope is enabled on your Shopify custom app.

**"SEO meta title/description shows as not set even though I set it in Shopify"**
→ Some themes store SEO data in theme metafields rather than the global namespace.
The skill looks in `global.title_tag` and `global.description_tag` — if your
theme uses different keys, the skill may not detect them. Run a manual check
in Shopify Admin → Products → [product] → Search engine listing preview.

**"Tags are being replaced instead of added"**
→ This should not happen — the skill reads existing tags before writing and
merges them. If it occurs, reply "undo tags on [product]" and the skill will
restore the previous tags from the audit memory.

**"Audit is taking a long time"**
→ Shopify rate limits to 2 API requests/second on Basic plan. A store with 500
products and individual metafield fetches will take approximately 8–10 minutes.
This is normal. The skill will report progress as it goes.

**"WooCommerce SEO meta not updating"**
→ WooCommerce REST API does not natively support Yoast SEO fields. Update these
directly in wp-admin → Products → [product] → Yoast SEO panel.
