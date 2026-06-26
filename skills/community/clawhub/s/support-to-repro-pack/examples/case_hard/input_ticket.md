From: sarah@globalfinance.co.uk
To: support@platform.io
Subject: URGENT - Payment processing failures since migration

Hi,

We migrated to your v3 API last night using the migration guide. Since then about 30% of our payment transactions are failing with different errors. This is costing us real money - we process about $2M daily.

Errors we're seeing:
- Some get HTTP 422 with "invalid_currency_format"
- Some get HTTP 500 with no body
- A few timeout completely after 30s

This only happens for GBP and EUR transactions. USD works fine.

Our setup:
- API key: sk_live_TESTKEY000000000demo
- Webhook endpoint: https://hooks.globalfinance.co.uk/stripe-webhook
- Server: AWS eu-west-1, running Node 18
- Using your SDK v3.2.0

I've attached our server logs. Our CTO James Wilson (james.wilson@globalfinance.co.uk, +44-20-7946-0958) wants an update by EOD.

Payment IDs that failed:
- pay_1OxR2FAcme123abc (GBP, £5,000)
- pay_1OxR3GAcme456def (EUR, €12,350)
- pay_1OxR4HAcme789ghi (GBP, £890)

Our Stripe customer ID: cus_Oxr5ijklmnop

Thanks,
Sarah Thompson
Head of Engineering
Global Finance Ltd
Company registration: 08765432
VAT: GB123456789
