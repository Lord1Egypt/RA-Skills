# Test-Template Vertical Builder — Step-by-Step Guide

**Build a production-ready Telegram AI agent for any vertical in ~10-15 minutes.**

---

## Overview

The `_test-template.py` pattern is:

```
Intent Classification → Lead Scoring → Agent Routing → CRM → Follow-up Pipeline → Analytics → Tier Gating → Error Handling
```

You fill in 7 sections. The engine handles the rest.

---

## Step 1: Define Your Vertical

Pick ONE clear job-to-be-done:
- Tax automation for self-employed
- Real estate agent CRM
- Dental appointment booking
- Legal intake screening
- E-commerce order tracking
- Healthcare patient triage

**Anti-pattern:** Don't try to build a "general business agent." Pick narrow + deep.

---

## Step 2: Fill in SEED_DATA

Open `_test-template.py`, find the `SEED_DATA` dictionary. Fill in:

```python
SEED_DATA = {
    "entities": [
        # Your mock records — clients, patients, properties, agents
        {"id": "1", "name": "Example Client", "email": "...", "phone": "...", "tier": "free"},
    ],
    "slots": [
        # Calendar/appointment slots
        {"id": "s1", "time": "09:00", "day": "mon-fri", "available": True},
    ],
    "templates": [
        # Message templates per intent
        {"intent": "booking", "template": "Your appointment confirmed for {time}!"},
    ],
}
```

---

## Step 3: Fill in INTENT_PATTERNS

Map user messages to intents:

```python
INTENT_PATTERNS = {
    "booking": ["записаться", "запись", "appointment", "book"],
    "pricing": ["сколько стоит", "цена", "price", "cost"],
    "cancel": ["отменить", "отмена", "cancel"],
    "faq": ["как", "что", "how", "what"],
}
```

3-5 intents is the sweet spot for MVP. Add more after validation.

---

## Step 4: Fill in ROUTING_RULES

Map tier to agent persona:

```python
ROUTING_RULES = {
    "free": {"max_items_per_month": 5, "response_delay": "standard", "support_level": "self-serve"},
    "pro": {"max_items_per_month": 100, "response_delay": "priority", "support_level": "dedicated"},
    "business": {"max_items_per_month": 1000, "response_delay": "instant", "support_level": "white-glove"},
}
```

---

## Step 5: Fill in PRICING_TIERS

Define subscription plans:

```python
PRICING_TIERS = {
    "free": {"price": 0, "currency": "USD", "features": ["5 bookings/mo", "basic CRM"]},
    "pro": {"price": 29, "currency": "USD", "features": ["100 bookings/mo", "lead scoring", "analytics"]},
    "business": {"price": 99, "currency": "USD", "features": ["unlimited", "CRM + follow-up", "priority support"]},
}
```

Pricing anchor: charge 1-3% of the value you save. A dental practice that recovers $3K/mo in no-shows will happily pay $49-99/mo.

---

## Step 6: Fill in FOLLOW_UP_SEQUENCES

Define nurture/reminder pipelines per intent:

```python
FOLLOW_UP_SEQUENCES = {
    "no_show": [
        {"delay_hours": 1, "message": "We missed you! Reschedule?"},
        {"delay_hours": 24, "message": "Still need that appointment?"},
    ],
    "inactive": [
        {"delay_days": 30, "message": "Haven't seen you in a while!"},
    ],
}
```

---

## Step 7: Run the Tests

```bash
python3 _test-template.py
```

All 27 core engine tests should pass. Then add 5-10 vertical-specific tests for your intents:

```python
def test_booking_intent():
    result = classify_intent("хочу записаться на завтра")
    assert result == "booking"
```

---

## From Template to Production

1. **Template passes 27/27** → Your foundation is solid
2. **Add vertical-specific tests** → 5-10 intent tests, all pass
3. **Swap mock stores for real APIs** → Replace SEED_DATA with external CRM, calendar, payment gateway
4. **Wire to OpenClaw handler** → Connect Telegram/Discord/WhatsApp webhook
5. **Deploy** → 2 minutes to production: register bot token, set webhook URL, done

---

## Real Examples Built With This Template

### SelfBot (RU Tax Assistant)
- 12/12 tests pass
- Intents: invoice, expense, tax-calc, receipt, bank-parse, reminder, faq
- Tiers: Free ₽0 → Pro ₽499/mo → Business ₽990/mo
- Built in ~30 minutes (pre-template). Would take ~10-15 min with template.

### Real Estate CRM Agent
- 63/63 tests pass
- Intents: listing-search, valuation, schedule-viewing, offer-submit, faq
- Tiers: Free → Agent → Broker → Enterprise
- MLS mock with 20 properties, multi-language (EN+ES+RU)

---

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Too many intents | Start with 3-5. 10+ intents = scope creep |
| Generic seed data | Use real-looking names, prices, addresses |
| No tier gating | Freemium works. Make the free tier too good → no upgrades |
| No follow-up sequences | The money is in the follow-up, not the first interaction |
| No error handling | Test edge cases: empty input, unicode, concurrent requests |

---

**Next step:** Copy `_test-template.py`, fill in 7 sections, run `python3 _test-template.py`. If 27/27 pass, you have a working vertical agent.
