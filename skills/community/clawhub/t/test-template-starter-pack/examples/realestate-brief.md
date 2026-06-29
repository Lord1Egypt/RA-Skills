# Real Estate CRM Agent (Example Brief)

Vertical: Real estate agent CRM + lead management
Market: 1.5M+ real estate agents in US alone, high-ticket transactions
Pricing: $0 (free) → $299/mo (Pro) → $499/mo (Business) → $999/mo (Enterprise)

## Seed Data

```python
SEED_DATA = {
    "entities": [
        {"id": "1", "name": "Sarah Johnson", "email": "sarah@realtor.com", "phone": "+15125551234", "tier": "pro", "region": "Austin, TX"},
        {"id": "2", "name": "Mike Chen", "email": "mike@brokerage.com", "phone": "+15125556789", "tier": "business", "region": "Austin, TX"},
    ],
    "slots": [
        {"id": "p1", "address": "123 Main St, Austin TX 78701", "price": 425000, "beds": 3, "baths": 2, "sqft": 1800, "status": "active"},
        {"id": "p2", "address": "456 Oak Ave, Austin TX 78702", "price": 650000, "beds": 4, "baths": 3, "sqft": 2400, "status": "active"},
        # ... 18 more properties in MLS mock
    ],
    "templates": [
        {"intent": "listing_inquiry", "template": "📋 {address} — {beds}bd/{baths}ba, {sqft}sqft. Listed at ${price:,}. Viewings: {schedule_link}"},
        {"intent": "valuation", "template": "Estimated value for {address}: ${low_estimate:,}–${high_estimate:,}. Based on {comps_count} comparable sales."},
        {"intent": "follow_up", "template": "Hi {client_name}, still interested in {address}? Price dropped to ${new_price:,}."},
    ],
}
```

## Intent Patterns

```python
INTENT_PATTERNS = {
    "listing_search": ["find house", "show me listings", "properties in", "busco casa", "ищу квартиру"],
    "valuation": ["what's my home worth", "valuate", "estimate", "value of", "cuánto vale"],
    "schedule_viewing": ["tour", "viewing", "visit", "ver la casa", "осмотр"],
    "offer_submit": ["make offer", "offer price", "bid", "oferta"],
    "faq": ["how does", "what is", "help", "explain", "cómo", "как"],
}
```

## Routing Rules

```python
ROUTING_RULES = {
    "free": {"max_leads_per_month": 5, "lead_scoring": False, "follow_up": False, "crm_sync": False},
    "pro": {"max_leads_per_month": 999999, "lead_scoring": True, "follow_up": True, "crm_sync": True, "analytics": True},
    "business": {"max_leads_per_month": 999999, "lead_scoring": True, "follow_up": True, "crm_sync": True, "analytics": True, "team_management": True, "white_label": True},
    "enterprise": {"unlimited": True, "lead_scoring": True, "follow_up": True, "crm_sync": True, "analytics": True, "team_management": True, "white_label": True, "api_access": True, "custom_branding": True},
}
```

## Pricing Tiers

```python
PRICING_TIERS = {
    "free": {"price": 0, "currency": "USD", "features": "5 leads/mo, basic intake, mock CRM"},
    "pro": {"price": 299, "currency": "USD", "features": "Unlimited leads, lead scoring, automated follow-up, CRM sync, analytics"},
    "business": {"price": 499, "currency": "USD", "features": "Multi-agent routing, white-label, priority support, team management"},
    "enterprise": {"price": 999, "currency": "USD", "features": "Unlimited, white-label, API access, dedicated instance, custom branding"},
}
```

## Follow-Up Sequences

```python
FOLLOW_UP_SEQUENCES = {
    "new_lead": [
        {"delay_hours": 1, "message": "Thanks for your interest in {address}! Would you like to schedule a viewing?"},
        {"delay_days": 3, "message": "Still thinking about {address}? It's getting interest — let me know!"},
        {"delay_days": 7, "message": "Price drop alert: {address} now ${new_price:,}. Good time to make an offer."},
    ],
    "post_viewing": [
        {"delay_hours": 4, "message": "How was the viewing? Any questions about the property?"},
        {"delay_days": 2, "message": "I can prepare a comparative market analysis for {address} if you're considering an offer."},
    ],
    "inactive_agent": [
        {"delay_days": 30, "message": "No new leads in 30 days? Try our lead-gen integration."},
    ],
}
```

## Result

- 63/63 tests pass
- MLS mock with 20 properties
- Multi-language: EN + ES + RU
- Lead scoring (budget × urgency × pre-approval status)
- Deploy time: 2 minutes (swap bot token)
