---
name: skill-pay
description: Add credit-based payments to any OpenClaw skill. Register paid skills, charge users per call, track earnings, and withdraw USDC. Use when a user wants to monetize a skill, set up payments for agent services, check credit balances, register as a builder, or integrate pay-per-use into their agent workflow.
---

# SkillPay — Credits for the Agent Economy

Universal payment system for OpenClaw skills. Builders register paid skills, users buy credits, skills charge per call.

## Setup

API base: `https://skillpay.gpupulse.dev/api/v1`

## For Users (Buyers)

### Register
```bash
curl -X POST "$BASE/user/register" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-agent", "email": "optional@email.com"}'
```
Returns `sp_usr_...` API key (save it, shown once).

### Buy Credits
```bash
curl -X POST "$BASE/user/deposit" \
  -H "Authorization: Bearer sp_usr_..." \
  -H "Content-Type: application/json" \
  -d '{"amount": 100}'
```

### Check Balance
```bash
curl "$BASE/user/balance" -H "Authorization: Bearer sp_usr_..."
```

## For Builders (Sellers)

### Register as Builder
```bash
curl -X POST "$BASE/builder/register" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-company", "wallet_address": "SolanaWalletAddress"}'
```
Returns `sp_bld_...` API key.

### Register a Paid Skill
```bash
curl -X POST "$BASE/builder/skill/register" \
  -H "Authorization: Bearer sp_bld_..." \
  -H "Content-Type: application/json" \
  -d '{"slug": "my-skill", "name": "My Skill", "description": "Does something useful", "price_credits": 10}'
```

### Check Earnings
```bash
curl "$BASE/builder/earnings" -H "Authorization: Bearer sp_bld_..."
```

### Withdraw
```bash
curl -X POST "$BASE/builder/withdraw" \
  -H "Authorization: Bearer sp_bld_..." \
  -H "Content-Type: application/json" \
  -d '{"amount": 50}'
```

## Integration (The Key Part)

Add this to your skill's code to charge per call:

```python
import requests

def charge_user(user_key, skill_slug="my-skill"):
    resp = requests.post("https://skillpay.gpupulse.dev/api/v1/pay", json={
        "user_key": user_key,
        "skill_slug": skill_slug
    })
    if resp.status_code == 200:
        return True  # paid, execute skill
    elif resp.status_code == 402:
        return False  # insufficient credits
    return False
```

## Browse Skills

```bash
curl "$BASE/skills"  # no auth needed — public catalog of all paid skills
```

## Platform Fee

2.5% on every transaction. Builder sets price in credits, receives 97.5%.

## Credit Ratio

1 USDC = 1 credit (adjustable per skill type).
