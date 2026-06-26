---
name: email-marketing
description: Email marketing automation for campaigns, newsletters, and customer engagement. Use when creating email sequences, drip campaigns, promotional emails, or customer retention workflows. Includes templates, scheduling, and analytics.
---

# Email Marketing

## Overview

Complete email marketing automation skill. Create campaigns, manage subscriber lists, design email templates, schedule sends, and track performance.

## Features

- Campaign creation and management
- Email templates (promotional, welcome)
- Subscriber list management
- Basic analytics
- E-commerce integration support

## Quick Start

### Create and Send Campaign

```bash
python scripts/email_campaign.py --action create --name "Spring Sale" --template promotional --list customers
```

### Send Campaign

```bash
python scripts/email_campaign.py --action send --name "Spring Sale"
```

### Add Subscriber

```bash
python scripts/email_campaign.py --action add-subscriber --list customers --email user@example.com
```

## Scripts

### email_campaign.py

Create and send email campaigns.

**Actions:**
- `create` - Create new campaign
- `send` - Send campaign to list
- `add-subscriber` - Add subscriber to list

**Arguments:**
- `--action` - Action to perform
- `--name` - Campaign name
- `--template` - Email template
- `--list` - Subscriber list
- `--email` - Subscriber email (for add-subscriber)
- `--dry-run` - Simulate without sending

## Email Templates

### Promotional Template

```
Subject: 🎉 {{offer}} - Limited Time Only!

Hi {{first_name}},

Great news! We're offering {{discount}} on {{product_category}}.

✨ What you get:
• Benefit 1
• Benefit 2
• Benefit 3

⏰ Offer expires: {{expiry_date}}

[Shop Now] {{shop_link}}

Questions? Reply to this email!

Best,
{{store_name}} Team

---
Taobao: {{taobao_link}}
Douyin: {{douyin_link}}
```

### Newsletter Template

```
Subject: {{month}} {{year}} - {{highlight}}

Hello {{first_name}},

Here's what's new this {{month}}:

## Highlights
- Update 1
- Update 2
- Update 3

## Featured Products
{{product_showcase}}

## Tips & Tricks
{{content_tip}}

Stay tuned for more!

{{store_name}}
```

### Welcome Series (5 emails)

**Day 1:** Welcome + Brand Story
**Day 3:** Best Sellers Showcase
**Day 7:** Customer Reviews
**Day 14:** Special Offer
**Day 30:** Feedback Request

## Subscriber Lists

### List Segments

- `all_subscribers` - Everyone
- `customers_active` - Purchased in last 90 days
- `customers_vip` - High-value customers
- `prospects` - Never purchased
- `inactive` - No engagement in 6 months

### Import Subscribers

```csv
email,first_name,last_name,source,signup_date
customer@example.com,John,Doe,taobao,2026-01-15
```

## E-commerce Integration

### Taobao/Douyin Customer Sync

```bash
# Sync recent buyers to email list
python scripts/sync_customers.py \
  --store taobao \
  --days 30 \
  --list recent_buyers
```

### Abandoned Cart Recovery

```bash
# Send reminder to customers with pending orders
python scripts/abandoned_cart.py \
  --hours 24 \
  --discount 5
```

### Post-Purchase Followup

```bash
# Thank you + review request
python scripts/post_purchase.py \
  --delay 7 \
  --request-review true
```

## Analytics

### Campaign Metrics

```bash
python scripts/campaign_stats.py --campaign spring_sale
```

Output:
- Sent count
- Open rate
- Click rate
- Unsubscribe rate
- Conversion rate

### A/B Testing

```bash
python scripts/ab_test.py \
  --campaign spring_sale \
  --variant-a subject_a.txt \
  --variant-b subject_b.txt \
  --split 50
```

## Best Practices

1. **Personalization** - Use recipient name, purchase history
2. **Timing** - Send during business hours (9-11 AM, 2-4 PM)
3. **Frequency** - Don't spam (1-2 emails/week max)
4. **Mobile optimization** - Keep subject < 40 chars
5. **Clear CTA** - One primary action per email
6. **Unsubscribe** - Always include unsubscribe link
7. **Compliance** - Follow anti-spam laws (CAN-SPAM, GDPR)

## Compliance

- Include physical mailing address
- Provide clear unsubscribe option
- Honor unsubscribe within 10 days
- Don't use deceptive subject lines
- Keep records of consent

## Troubleshooting

- **Low open rates**: Test different subject lines, send times
- **High bounce rate**: Clean email list, verify addresses
- **Spam complaints**: Review content, reduce frequency
- **Low click rate**: Improve CTA, make links prominent
