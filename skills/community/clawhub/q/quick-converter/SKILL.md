---
name: Quick Converter
description: Fast offline unit/time/currency/crypto conversions — ideal for quick everyday math in agent chats.
version: 1.0.0
tags: [utility, productivity, conversion, no-api, lightweight, india]
homepage: https://github.com/nihalmehta007
emoji: "🔄"
metadata:
  openclaw:
    requires: []          # no deps, no env vars
    files: []
---

# Quick Converter

Use this skill anytime for instant, no-internet conversions like:
- "convert 183 cm to feet"
- "50000 INR to USD right now"
- "how many hours until 9 PM IST tomorrow"
- "25°C to Fahrenheit"
- "0.1 BTC approximate in INR"

Relies on built-in formulas + approximate rates (updated March 2026). Always notes when values are estimates — great for casual use, but advise checking live sources for money/trading.

## Available Actions

### convert_units
**Description:** Length, weight, temperature, area, volume, speed, etc.
**Trigger phrases:** convert X Y to Z, how many Z in X, X in Z units
**Arguments:**
- from_value: number - numeric amount
- from_unit: string - e.g. cm, kg, celsius, km/h, liters
- to_unit: string - target unit

**Examples:**
User: 170 cm to feet and inches  
→ call convert_units from_value=170 from_unit=cm to_unit=feet → "≈5 feet 6.93 inches (170 / 30.48 ≈ 5.577 ft)"

User: 100 kg to pounds  
→ "≈220.46 lb (100 × 2.20462)"

**Common factors (agent uses these):**
- Length: 1 inch = 2.54 cm, 1 foot = 30.48 cm, 1 m = 3.28084 ft
- Weight: 1 kg = 2.20462 lb, 1 lb = 0.453592 kg
- Temp: °F = (°C × 9/5) + 32, °C = (°F - 32) × 5/9
- Others: 1 km = 0.621371 mi, 1 L = 0.264172 gal, etc.

### convert_currency
**Description:** Approximate fiat conversions (INR-focused + major pairs)
**Trigger phrases:** X INR to USD, Y dollars in rupees, Z euros to INR
**Arguments:**
- amount: number
- from_code: string (ISO3: INR, USD, EUR, GBP…)
- to_code: string

**Approximate rates (mid-March 2026):**
- 1 USD ≈ 92.2 INR
- 1 EUR ≈ 106.8 INR
- 1 GBP ≈ 127 INR (rough; check live for accuracy)
- 1 USD ≈ 0.87 EUR (inverse where needed)

**Examples:**
User: 50000 INR to USD  
→ ≈542.30 USD (using 1 USD ≈ 92.2 INR) — rate approximate as of March 2026

**Note:** Static estimates only. For banking/trading, always verify with live source (e.g., RBI, Google, Wise).

### convert_crypto
**Description:** Rough BTC/ETH estimates to USD/INR
**Trigger phrases:** 0.05 BTC in INR, 1000 USD worth of ETH approx
**Arguments:**
- amount: number
- from_asset: string (BTC, ETH, USD, INR…)
- to_asset: string

**Approximate rates (mid-March 2026):**
- 1 BTC ≈ $69,000 USD ≈ 63.6 lakh INR (69,000 × 92.2)
- 1 ETH ≈ $2,040 USD ≈ 1.88 lakh INR

**Examples:**
User: 0.1 BTC to INR  
→ ≈6.36 lakh INR (0.1 × 69,000 × 92.2) — very approximate

**Note:** Crypto volatile; these are rough snapshots — use exchanges for real prices.

### time_until
**Description:** Time delta to future date/time/event (IST default, Ahmedabad/Gujarat context)
**Trigger phrases:** how long until 10 PM IST, hours to Diwali 2026, time left till weekend
**Arguments:**
- target_time: string - natural lang like "9pm IST tomorrow", "Diwali 2026", "next Monday 9am"
- from_now: boolean - default true (calculate from current IST)

**Examples:**
User: how many hours until 10 PM IST?  
→ call time_until target_time="10 PM IST" → (computes delta from now)

Known events:
- Diwali 2026 main day (Lakshmi Puja): November 8, 2026

**Note:** Agent uses current time (~March 10, 2026 IST) + standard calendar logic.

## Best Practices & Tips
- Show formula/math for transparency (e.g. "50000 / 92.2 ≈ 542.30")
- Round money to 2 decimals, large numbers sensibly (e.g. lakh/crore for INR)
- Currency/crypto: Always prefix with "approximate as of March 2026"
- If ambiguous (e.g. "dollars" → assume USD?), clarify with user
- Zero-risk, super-fast skill — perfect default utility for any OpenClaw agent!

Install & use — feedback welcome for v1.2 (more units, better holidays, etc.) 🚀