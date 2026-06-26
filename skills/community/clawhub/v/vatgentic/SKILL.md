---
name: vatgentic
description: Instant EU VAT validation with Lightning Bitcoin. 10 sats per lookup. No subscriptions.
license: MIT
metadata:
  openclaw:
    emoji: "⚡"
    os: ["linux", "darwin", "win32"]
    requires:
      bins: ["curl", "jq", "python3"]
  clawhub:
    category: "finance"
    tags: ["vat", "lightning", "bitcoin", "validation", "eu", "api"]
---

# VatGentic ⚡ Instant VAT Validation

**Lightning-fast EU VAT validation. Lightning payments.**

Validate any EU VAT number in seconds. Get company name, address, and validity status.

**10 sats per validation** (~$0.01). No subscriptions. No signup.

---

## Requirements

⚠️ **You need Lightning Bitcoin to use this service.**

- Pay via Lightning Network (Bitcoin's payment layer)
- Fast, global, no credit cards
- Perfect for AI agents and automation

## Quick Start

### 1. Set the API endpoint

```bash
export VATGENTIC_API_URL="https://fair-earwig.pikapod.net"
```

### 2. Validate a VAT number

```python
import requests
import os

# Submit VAT number
response = requests.post(
    f"{os.environ['VATGENTIC_API_URL']}/vat/request",
    json={"vatNumber": "LU26375245", "amountSats": 10}
)
data = response.json()

# Output: Lightning invoice details
print(data)
```

### 3. Pay the Lightning invoice

```python
# Invoice from response:
# - bolt11: Lightning invoice string
# - checkout_link: Browser payment
# - amount_sats: 10

# Pay with any Lightning wallet
```

### 4. Get your result

After payment completes, poll for the result:

```python
# Poll for completion
import time
for _ in range(15):
    status = requests.get(f"{os.environ['VATGENTIC_API_URL']}/vat/status/{data['request_id']}")
    result = status.json()
    if result['status'] == 'completed':
        print(result['vat_result'])
        break
    time.sleep(2)
```

---

## API Reference

### Request Validation

**POST** `/vat/request`

```bash
curl -X POST $VATGENTIC_API_URL/vat/request \
  -H "Content-Type: application/json" \
  -d '{"vatNumber": "LU26375245"}'
```

**Response:**
```json
{
  "request_id": "vat_1776348560582_abc123",
  "status": "pending_payment",
  "amount_sats": 10,
  "bolt11": "lnbc100n1p5xyz...",
  "checkout_link": "https://pay.example.com/i/abc123"
}
```

### Check Status

**GET** `/vat/status/{request_id}`

```bash
curl $VATGENTIC_API_URL/vat/status/vat_1776348560582_abc123
```

**Response (completed):**
```json
{
  "status": "completed",
  "vat_result": {
    "valid": true,
    "country_code": "LU",
    "company_name": "Example S.à r.l.",
    "company_address": "123 Rue Example, Luxembourg"
  }
}
```

---

## Pricing

**10 sats per validation** (~$0.01 USD)

Lightning Network only. Fast, private, global.

---

## Example: Agent Integration

```python
import requests, os, time

def validate_vat(vat_number):
    """Validate VAT and return company details."""
    url = os.environ['VATGENTIC_API_URL']
    
    # Submit request
    resp = requests.post(f'{url}/vat/request', 
                         json={'vatNumber': vat_number})
    req = resp.json()
    
    # Pay invoice (manual or automated via Lightning wallet)
    print(f"Pay {req['amount_sats']} sats: {req['checkout_link']}")
    
    # Wait for completion
    for _ in range(15):
        status = requests.get(f"{url}/vat/status/{req['request_id']}")
        result = status.json()
        if result['status'] == 'completed':
            return result['vat_result']
        time.sleep(2)
    
    raise TimeoutError("Validation timeout")

# Use it
company = validate_vat("LU26375245")
print(f"✅ Valid: {company['valid']}")
print(f"📦 {company['company_name']}")
```

---

## Supported Countries

All 27 EU member states:
- Austria (AT), Belgium (BE), Bulgaria (BG), Croatia (HR)
- Cyprus (CY), Czech Republic (CZ), Denmark (DK), Estonia (EE)
- Finland (FI), France (FR), Germany (DE), Greece (EL)
- Hungary (HU), Ireland (IE), Italy (IT), Latvia (LV)
- Lithuania (LT), Luxembourg (LU), Malta (MT), Netherlands (NL)
- Poland (PL), Portugal (PT), Romania (RO), Slovakia (SK)
- Slovenia (SI), Spain (ES), Sweden (SE)

---

## What You Get

Each validation returns:
- ✅ Validity status (valid/invalid)
- ✅ Company name (if registered)
- ✅ Company address (if registered)
- ✅ VAT number format verification
- ✅ Country code

Data source: Official EU VIES database.

---

## Why Lightning?

- ⚡ **Instant** - Results in seconds, not days
- 🌍 **Global** - No geographic restrictions
- 💰 **Micropayments** - Pay per use, no subscriptions
- 🤖 **Agent-friendly** - Machines can pay machines

---

## Support

Docs: https://docs.vatgentic.com  
Status: https://status.vatgentic.com  
Contact: support@vatgentic.com

---

*VatGentic — VAT validation for the Bitcoin era ⚡*
