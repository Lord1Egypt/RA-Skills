# Return Reduction Playbook

Reusable frameworks for diagnosing and reducing e-commerce return rates. Adapt to the specific category and data.

---

## Return reason taxonomy

Standardize return reasons into these categories for consistent tracking:

| Code | Reason | Description |
|------|--------|-------------|
| SIZE | Size / fit issue | Too small, too large, inconsistent sizing |
| QUAL | Quality below expectation | Feels cheap, poor stitching, flimsy |
| DESC | Not as described | Color, material, or feature doesn't match listing |
| DMGD | Damaged / defective | Arrived broken, DOA, manufacturing defect |
| CHGM | Changed mind | Impulse purchase, found better option, no longer needed |
| COMP | Compatibility issue | Doesn't fit device, wrong connector, incompatible model |
| DUPE | Duplicate / wrong item | Ordered wrong one, received wrong item |
| LATE | Arrived too late | Missed the occasion, no longer relevant |
| OTHR | Other | Catchall — review periodically and split into new codes |

If the store doesn't track structured reasons, mine them from:
- Support ticket tags / free-text
- 1–3 star review text
- Return form comments

---

## Benchmark return rates by category

Use these as orientation — actual rates vary by price point, audience, and channel.

| Category | Typical return rate | Main driver |
|----------|--------------------:|-------------|
| Fashion / apparel | 20–30% | Fit and color |
| Shoes | 25–35% | Fit |
| Electronics | 5–10% | Feature mismatch, compatibility |
| Beauty / skincare | 5–8% | Shade, sensitivity, scent |
| Home / furniture | 8–12% | Size in space, color vs. room |
| Jewelry / accessories | 10–15% | Size, quality perception |
| Food / beverage | 2–5% | Taste, freshness, allergen |
| Pet | 8–12% | Sizing, palatability |

---

## PDP fix checklist (by return reason)

### SIZE — Fit / size issues

- [ ] Size guide with body measurements (not just S/M/L)
- [ ] "Fits like" or "true to size / runs small / runs large" label
- [ ] Model stats on lifestyle photos (height, weight, size worn)
- [ ] Flat-lay with ruler or common-object scale reference
- [ ] Fit-finder quiz (if >15% size returns)

### DESC — Not as described

- [ ] Natural-lighting product photos (no heavy filters)
- [ ] Multiple angles including close-ups of texture / material
- [ ] Accurate color name (avoid "ocean" for blue — also state "blue")
- [ ] Material composition with touch descriptor ("soft brushed cotton," "rigid canvas")
- [ ] Weight in oz / grams for items where heft matters
- [ ] "What you get" section for bundles / kits

### QUAL — Quality below expectation

- [ ] Close-up shots of stitching, hardware, finish
- [ ] Material comparison ("vs. fast fashion: double-stitched seams, 200gsm fabric")
- [ ] Verified-buyer photos showing product after use
- [ ] Set expectations honestly — don't overpromise on durability claims

### COMP — Compatibility

- [ ] Compatibility checker or dropdown ("select your device model")
- [ ] Clear spec table with connector type, dimensions, supported models
- [ ] "Works with / does not work with" callout box
- [ ] Cross-reference with common confusion points in reviews

### DMGD — Damaged / defective

- [ ] Review packaging adequacy (bubble wrap, rigid box for fragile items)
- [ ] QC checkpoint before shipping
- [ ] "If your item arrives damaged" instant-resolution flow in CS

---

## Policy optimization patterns

### Exchange-first flow
Instead of straight refund, offer exchange as the default option with a small incentive (free express shipping on exchange). Retains the revenue and often solves the customer's real problem.

### Threshold-based free returns
Free returns above a cart value (e.g. orders > $75). Below that, customer pays a flat return-shipping fee. Discourages bracket-ordering on low-AOV items without punishing loyal customers.

### Shortened window for seasonal / trend items
30-day return window for standard; 14-day for final-sale or seasonal items. Reduces "closet returns" in fashion.

### Serial returner segmentation
Flag accounts with 3+ returns in 90 days. Options:
- Show a gentle nudge ("We noticed you've returned a few items — can we help you find the right fit?")
- Require return reason + photo
- Exclude from free-return benefit after threshold

### "Try before you buy" as a controlled alternative
If bracket-ordering is common, consider a formal try-on program with a deposit. Gives the customer what they want while making the cost visible.

---

## Measurement framework

### Primary metrics
- **Return rate** = returns initiated / orders shipped (by product, category, reason)
- **Return cost per unit** = (return shipping + restocking + lost resale) / returns
- **Net revenue after returns** = gross revenue − return costs

### Secondary metrics
- **Reason-code mix** — track shifts after PDP changes
- **Time-to-return** — shorter times suggest immediate disappointment; longer times suggest "changed mind"
- **Repeat returner rate** — % of customers with 2+ returns in 90 days

### A/B testing return-rate changes
1. Pick top 3–5 offender products.
2. Apply PDP fix to treatment group; keep control unchanged.
3. Measure return rate over 30–60 days (need enough order volume for signal).
4. Success = return rate drops > 2 pp (percentage points) with stable or improved conversion.

---

## Cost estimation formula

Rough per-return cost:

```
return_cost = return_shipping + restocking_labor + (original_price × lost_resale_pct)
```

- **return_shipping**: $5–$12 (depending on size/weight, prepaid vs. customer-paid)
- **restocking_labor**: $2–$5 per item
- **lost_resale_pct**: 0% (resellable as new) to 50%+ (opened beauty, worn apparel)

Multiply by monthly return volume for total monthly cost.
