# Carrier Rate Comparison Guide

## Carrier Selection Decision Tree

```
Package weight?
├── ≤ 1 lb (16 oz)
│   ├── Residential address → USPS Ground Advantage (no residential surcharge)
│   └── Commercial address → USPS Ground Advantage or UPS SurePost
│
├── 1–5 lbs
│   ├── Zone 1–3 → Regional carrier OR UPS/FedEx Ground
│   ├── Zone 4–6 → UPS/FedEx negotiated ground OR USPS Priority Mail (if 2-day needed)
│   └── Zone 7–8 → UPS/FedEx Ground (USPS Priority Mail may be competitive here)
│
├── 5–20 lbs
│   ├── Zone 1–4 → Regional carrier (often 20–30% cheaper)
│   └── Zone 5–8 → UPS/FedEx Ground (negotiate volume discount)
│
└── 20+ lbs
    ├── Single package → UPS/FedEx Ground (freight pricing kicks in at 150 lbs)
    └── Multiple packages to same address → Consider LTL consolidation
```

---

## Carrier Overview

### USPS Ground Advantage
**Best for:** Lightweight packages (<16 oz) to residential addresses

**Advantages:**
- No residential delivery surcharge (saves $4.90–5.55 vs. UPS/FedEx)
- No fuel surcharge for most commercial accounts
- Competitive rates for lightweight packages
- Delivery to PO Boxes and APO/FPO addresses

**Disadvantages:**
- No guaranteed delivery windows (2–8 business days typically)
- Limited real-time tracking updates
- Package size limits: 108" length + girth combined

**Best rate bracket:** 0.5–16 oz, Zone 1–8

---

### USPS Priority Mail
**Best for:** 1–3 day delivery, medium-weight packages where speed matters

**Advantages:**
- Guaranteed 1–3 day delivery
- No residential surcharge
- Free packaging materials from USPS
- Competitive on Zones 7–8 for 1–5 lb packages

**Disadvantages:**
- More expensive than Ground Advantage for non-urgent deliveries
- DIM factor is higher (166 vs. 139 for UPS/FedEx) — actually advantageous for lighter items in larger boxes

**Best rate bracket:** 1–5 lbs, when 2-day delivery required, or Zone 7–8 mid-weight

---

### UPS Ground
**Best for:** 5–70 lb packages, commercial addresses, when tracking and reliability are critical

**Advantages:**
- Strong commercial delivery network
- UPS My Choice consumer delivery notifications reduce failed deliveries
- Reliable tracking and claims process
- Volume discount program up to 50%+ off list at high volume

**Disadvantages:**
- Residential delivery surcharge: ~$5.15/package
- Fuel surcharge: 15–20% of base rate (fluctuates)
- DIM factor: 139 (charges DIM weight for all packages)

**Negotiation potential:** 10–40% off list rates depending on volume and relationship

---

### UPS SurePost
**Best for:** B2C residential delivery, lightweight packages (1–10 lbs)

How it works: UPS transports to destination post office; USPS makes final delivery. Eliminates the residential delivery surcharge.

**Advantages:**
- No residential delivery surcharge
- Cheaper than UPS Ground for residential lightweight packages

**Disadvantages:**
- 1–2 day slower than UPS Ground
- Tracking handoff from UPS to USPS creates gaps
- Not ideal for time-sensitive deliveries

---

### FedEx Ground / Home Delivery
**Best for:** B2C residential delivery, high-volume shippers, comparable to UPS

**Notes:**
- FedEx Home Delivery = residential, Mon–Sat delivery
- FedEx Ground = commercial, Mon–Fri
- Similar rate structure to UPS; negotiate both simultaneously to leverage competition

**Negotiation tip:** Get a quote from UPS, show it to FedEx, and vice versa. Carriers compete directly for volume.

---

### Regional Carriers
**Best for:** Zone 1–3 deliveries in their coverage area

| Carrier | Coverage Region | Advantage vs. UPS/FedEx |
|---------|----------------|------------------------|
| OnTrac | Western U.S. | 15–30% cheaper, often faster for intra-region |
| LaserShip / LSO | Eastern U.S. | Competitive for residential delivery |
| Spee-Dee Delivery | Midwest | Strong Midwest coverage, no residential surcharge |
| CDL Last Mile | Southeast | Competitive for last-mile residential |
| GSO (Golden State) | California | California-focused, cheaper than national carriers |

**How to access:** Most regional carriers require a direct contract OR you can access them via multi-carrier platforms (EasyPost, ShipBob, ShipStation) without a direct account.

---

## Rate Shopping Platforms

| Platform | Monthly Cost | Key Feature |
|---------|-------------|-------------|
| EasyPost | Usage-based | API-first, connects 100+ carriers |
| ShipStation | $9–229/month | UI-friendly, multi-carrier routing rules |
| Shippo | Usage-based | Simple API, pre-negotiated USPS rates |
| ShipBob | 3PL + rates | Full fulfillment + discounted carrier rates |
| Pirateship | Free | Deep USPS Commercial Plus rates |

---

## Current Rate Benchmarks (approximate, subject to change)

*Note: These are representative published/commercial rates as of mid-2026. Actual rates vary by account volume, zone, and negotiated discounts. Always get live quotes from your carrier portal.*

### USPS Ground Advantage (2 lbs)
| Zone | Rate |
|------|------|
| Zone 1–2 | ~$7.20 |
| Zone 4 | ~$8.85 |
| Zone 6 | ~$10.40 |
| Zone 8 | ~$12.10 |

### UPS Ground (2 lbs, list rates — no residential surcharge included)
| Zone | Rate |
|------|------|
| Zone 1–2 | ~$8.40 |
| Zone 4 | ~$9.95 |
| Zone 6 | ~$12.70 |
| Zone 8 | ~$15.80 |

*Add: Residential surcharge ~$5.15, Fuel surcharge ~15–18% of base*

### FedEx Home Delivery (2 lbs, list rates — residential, fuel not included)
| Zone | Rate |
|------|------|
| Zone 1–2 | ~$8.55 |
| Zone 4 | ~$10.10 |
| Zone 6 | ~$12.90 |
| Zone 8 | ~$16.00 |

---

## Carrier Negotiation Playbook

### Preparation
1. Pull 12 months of shipping invoices — volume by carrier, weight tier, zone, and service level
2. Calculate your residential % and surcharge totals separately
3. Prepare a "competitive quote" from the rival carrier (real quote, not bluffed)

### Negotiating with UPS / FedEx
1. Request a meeting with your account rep (not phone — in-person or video call)
2. Show your volume data: "We shipped [N] packages last year, [N]% growth expected"
3. Ask for: base rate discount by weight bracket, residential surcharge reduction, fuel surcharge cap, and waived address correction fees
4. Common opening gambit: "We're evaluating both UPS and FedEx for next year. Here's what the other carrier has offered us."
5. Get all discounts in writing in a contract (not just a verbal commitment)

### Volume Thresholds for Negotiating Power
| Annual Shipping Spend | Realistic Discount Range |
|----------------------|------------------------|
| $10,000–50,000 | 5–15% off list |
| $50,000–200,000 | 15–30% off list |
| $200,000–1M | 25–40% off list |
| $1M+ | 35–55% off list (with strong rep relationship) |
