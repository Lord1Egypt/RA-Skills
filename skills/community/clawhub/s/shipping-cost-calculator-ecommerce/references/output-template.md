# Shipping Cost Output Template

Structure every shipping cost analysis with this format:

---

## Assumptions

| Input | Value | Source | Confidence |
|---|---|---|---|
| Package weight (actual) | X.X lbs | [Actual / Estimated] | ✅ / ⚠️ / ❓ |
| Package dimensions | L×W×H in | [Actual / Estimated] | ✅ / ⚠️ / ❓ |
| DIM factor | XXX | [Carrier standard] | ✅ |
| Billable weight | X.X lbs | [Calculated] | ✅ / ⚠️ |
| Carrier / service | [Name] | [Actual / Estimated] | ✅ / ⚠️ / ❓ |
| Fuel surcharge | X.X% | [Current period] | ✅ / ⚠️ |
| Pick-pack cost | $X.XX | [Actual / Estimated] | ✅ / ⚠️ / ❓ |
| Packaging materials | $X.XX | [Actual / Estimated] | ✅ / ⚠️ / ❓ |
| AOV | $XX.XX | [Actual / Estimated] | ✅ / ⚠️ / ❓ |
| Return rate | X.X% | [Actual / Estimated] | ✅ / ⚠️ / ❓ |
| Return label cost | $X.XX | [Actual / Estimated] | ✅ / ⚠️ / ❓ |
| Zone distribution | [See breakdown] | [Actual / Estimated] | ✅ / ⚠️ / ❓ |

---

## Per-Order Delivery Cost

```
Carrier base rate (weighted avg):       $XX.XX
+ Residential surcharge:                $XX.XX
+ Fuel surcharge (X.X%):                $XX.XX
+ Peak surcharge (if applicable):       $XX.XX
= Total carrier cost:                   $XX.XX
+ Pick-pack labor:                      $XX.XX
+ Packaging materials:                  $XX.XX
+ Label / handling:                     $XX.XX
+ Insurance:                            $XX.XX
──────────────────────────────────────────────
= Delivery cost per order:              $XX.XX
+ Return drag (X% × $X.XX):            $XX.XX
+ Reship drag:                          $XX.XX
──────────────────────────────────────────────
= True total shipping cost/order:       $XX.XX  (XX.X% of AOV)
```

---

## Zone Breakdown

| Zone | % of Orders | Carrier Cost | Total Delivery Cost | Margin After Shipping | Flag |
|---|---|---|---|---|---|
| Zone 1–2 | XX% | $X.XX | $X.XX | XX% | [OK / Watch / Risk] |
| Zone 3–4 | XX% | $X.XX | $X.XX | XX% | [OK / Watch / Risk] |
| Zone 5–6 | XX% | $X.XX | $X.XX | XX% | [OK / Watch / Risk] |
| Zone 7–8 | XX% | $X.XX | $X.XX | XX% | [OK / Watch / Risk] |
| Weighted Average | 100% | $X.XX | $X.XX | XX% | — |

---

## Policy Impact Analysis

| Shipping Policy | Revenue from Shipping | Cost Absorbed | CM Impact | AOV Effect |
|---|---|---|---|---|
| Calculated (current) | $X.XX/order | $0 | Baseline | Baseline |
| Flat $X.XX | $X.XX/order | $X.XX/order | -X.X% | ~0% |
| Free over $XX | $X.XX blended | $X.XX blended | -X.X% | +X.X% |
| Free all orders | $0 | $X.XX/order | -X.X% | +X.X% |

### Threshold Scenarios

| Threshold | % Orders Qualifying | Blended Shipping Cost | Margin Impact | Verdict |
|---|---|---|---|---|
| $35 | XX% | $X.XX | -X.X% | [Viable / Tight / Risky] |
| $50 | XX% | $X.XX | -X.X% | [Viable / Tight / Risky] |
| $75 | XX% | $X.XX | -X.X% | [Viable / Tight / Risky] |
| $99 | XX% | $X.XX | -X.X% | [Viable / Tight / Risky] |

---

## Carrier Comparison (if applicable)

| Carrier / Option | Zone 2 | Zone 4 | Zone 6 | Zone 8 | Weighted Avg | Savings |
|---|---|---|---|---|---|---|
| Current | $X.XX | $X.XX | $X.XX | $X.XX | $X.XX | — |
| Option B | $X.XX | $X.XX | $X.XX | $X.XX | $X.XX | $X.XX/order |
| Option C | $X.XX | $X.XX | $X.XX | $X.XX | $X.XX | $X.XX/order |

---

## Decision

**Recommendation:** [Absorb / Set threshold / Pass through / Repackage / Switch carrier]

**Rationale:**
- [Key reason 1 based on the numbers]
- [Key reason 2]

**Actions:**
- [Specific next step 1]
- [Specific next step 2]

**Risk flags:**
- [Any warnings: DIM weight issue, zone concentration, seasonal surcharges, etc.]
