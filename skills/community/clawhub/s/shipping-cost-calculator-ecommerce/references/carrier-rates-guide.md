# Carrier Rates & Surcharge Reference

Quick reference for US domestic carrier pricing structures. Use for estimation — actual rates depend on negotiated contracts.

---

## USPS (United States Postal Service)

### Services
| Service | Speed | Weight Limit | Best For |
|---|---|---|---|
| Ground Advantage | 2–5 days | 70 lbs | Light packages, budget shipping |
| Priority Mail | 1–3 days | 70 lbs | Standard ecommerce default |
| Priority Mail Express | 1–2 days | 70 lbs | Urgent / perishable |
| Media Mail | 2–8 days | 70 lbs | Books, media only |

### Rate Structure
- Zone-based pricing (Zones 1–9)
- Commercial pricing available via USPS.com or shipping platforms
- **DIM factor: 166** (more generous than UPS/FedEx)
- No residential surcharge
- No fuel surcharge on retail rates

### Typical Ranges (Commercial, 2024-2025)
| Weight | Zone 1–2 | Zone 3–4 | Zone 5–6 | Zone 7–8 |
|---|---|---|---|---|
| 1 lb | $4.50–5.50 | $5.00–6.50 | $6.50–8.00 | $8.00–10.00 |
| 3 lbs | $6.00–7.50 | $7.00–9.00 | $9.00–12.00 | $12.00–15.00 |
| 5 lbs | $8.00–10.00 | $9.50–12.00 | $12.00–16.00 | $16.00–20.00 |

---

## UPS

### Services
| Service | Speed | Best For |
|---|---|---|
| Ground | 1–5 days | Standard ecommerce |
| 3 Day Select | 3 days | Mid-tier speed |
| 2nd Day Air | 2 days | Premium speed |
| Next Day Air | 1 day | Urgent |

### Rate Structure
- Zone-based pricing
- **DIM factor: 139** (stricter than USPS)
- **Residential surcharge: ~$4.50–6.00/package**
- **Fuel surcharge: 12.5–14.5%** (varies quarterly)
- Peak surcharges (Oct–Jan): $1.50–6.50/package

### Key Surcharges
| Surcharge | Amount | Trigger |
|---|---|---|
| Residential delivery | $4.50–6.00 | Ship to home address |
| Delivery area (extended) | $3.50–5.00 | Rural or remote ZIP |
| Additional handling (weight) | $15.00+ | > 50 lbs |
| Additional handling (size) | $15.00+ | Longest side > 48 in |
| Large package | $40.00+ | Length + girth > 130 in |

---

## FedEx

### Services
| Service | Speed | Best For |
|---|---|---|
| Ground / Home Delivery | 1–5 days | Standard ecommerce |
| Express Saver | 3 days | Mid-tier speed |
| 2Day | 2 days | Premium speed |
| Priority Overnight | 1 day | Urgent |

### Rate Structure
- Zone-based pricing (similar to UPS)
- **DIM factor: 139**
- **Residential surcharge: ~$4.50–6.00/package**
- **Fuel surcharge: 12.5–14.5%** (varies monthly)
- Peak surcharges similar to UPS

---

## Regional Carriers

| Carrier | Coverage | Best For | Typical Savings vs National |
|---|---|---|---|
| OnTrac | Western US | Zone 1–4 in West | 20–40% |
| LSO (Lone Star Overnight) | TX, surrounding states | Texas-based sellers | 15–30% |
| Spee-Dee | Upper Midwest | MN, WI, IA area | 20–35% |
| GLS US | National (expanding) | Lightweight parcels | 10–25% |
| Amazon Shipping | Select markets | Amazon sellers | Varies |

---

## 3PL / Fulfillment Fee Reference

Common fulfillment center fee structures:

| Fee Type | Typical Range | Notes |
|---|---|---|
| Receiving | $25–45/pallet or $0.25–0.50/unit | Inbound processing |
| Storage | $8–25/pallet/month | Varies by season |
| Pick & pack | $2.00–4.00/order + $0.50–1.00/item | Base + per-item |
| Standard packaging | $0.50–2.00/order | Box, filler, tape |
| Custom inserts | $0.25–1.00/insert | Marketing materials |
| Shipping label | $0.10–0.25/label | Included by some 3PLs |
| Return processing | $3.00–6.00/return | Inspection + restock |

### Amazon FBA Fee Reference
| Size Tier | Dimensions | Weight | Fulfillment Fee |
|---|---|---|---|
| Small standard | ≤ 15×12×0.75 in | ≤ 16 oz | $3.22–3.40 |
| Large standard | ≤ 18×14×8 in | ≤ 20 lbs | $4.00–7.00+ |
| Small oversize | ≤ 60×30 in | ≤ 70 lbs | $9.00–15.00+ |
| Large oversize | ≤ 108 in longest | ≤ 150 lbs | $90.00+ |

---

## DIM Weight Calculator

```
DIM weight (lbs) = (Length × Width × Height in inches) / DIM factor

DIM factors:
- UPS / FedEx: 139
- USPS: 166
- DHL eCommerce: 139

Billable weight = max(actual weight, DIM weight)
```

### DIM Weight Red Flags
Products where DIM weight commonly exceeds actual weight:
- Pillows, cushions, pet beds
- Lamp shades, light fixtures
- Large electronics packaging (lots of foam)
- Seasonal decor (wreaths, artificial trees)
- Apparel in retail boxes (not poly mailers)

**Fix:** Use poly mailers instead of boxes where possible, right-size packaging, consider flat-pack design.

---

## Surcharge Calendar (Typical)

| Period | Carrier | Surcharge Type | Typical Amount |
|---|---|---|---|
| Oct 1 – Jan 15 | UPS, FedEx | Peak / demand surcharge | $1.50–6.50/pkg |
| Nov 20 – Dec 24 | All | Holiday volume surcharge | Additional $1–3/pkg |
| Year-round | UPS, FedEx | Fuel surcharge | 12–15% of base rate |
| Year-round | UPS, FedEx | Residential delivery | $4.50–6.00/pkg |
| Varies | All | Delivery area surcharge | $2.50–5.00/pkg |

---

## Confidence Levels

When using rate data in models, tag every input:

| Level | Symbol | Meaning | Example |
|---|---|---|---|
| Confirmed | ✅ | From actual invoices or contracts | Last month's UPS invoice |
| Estimated | ⚠️ | From rate calculators or quotes | FedEx online rate estimate |
| Assumed | ❓ | Published rate card or industry avg | USPS retail rate table |
