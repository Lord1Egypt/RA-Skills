---
name: claude-email-marketing-skill
description: Give Claude deep expertise in email marketing strategy, deliverability, automation, copywriting, and ESP selection
triggers:
  - "help me with email marketing"
  - "write an email campaign"
  - "fix my email deliverability"
  - "set up email authentication"
  - "create a welcome email sequence"
  - "improve my email open rates"
  - "choose an email service provider"
  - "segment my email list"
---

# Claude Email Marketing Skill

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

This skill provides Claude with opinionated, practitioner-level expertise in email marketing. It covers authentication (SPF, DKIM, DMARC), list building, segmentation, copywriting, automation sequences, deliverability optimization, metrics analysis, and ESP selection.

## What This Skill Does

Transforms Claude into an email marketing expert who can:

- **Diagnose deliverability issues** and provide specific fixes for spam folder problems
- **Write high-converting email copy** with effective subject lines and CTAs
- **Design automation sequences** (welcome series, abandoned cart, re-engagement)
- **Configure email authentication** (SPF, DKIM, DMARC records)
- **Segment audiences** and recommend personalization strategies
- **Evaluate ESPs** using a five-factor framework
- **Interpret email metrics** and suggest optimization tactics
- **Ensure compliance** with CAN-SPAM, GDPR, CASL, CCPA

## Installation

### For Claude Code

1. Clone the repository:

```bash
git clone https://github.com/jacquescorbytuech/email-marketing-skill.git
```

2. Add the skill path to your `.claude/settings.json`:

```json
{
  "skills": [
    "/absolute/path/to/email-marketing-skill/email-marketing"
  ]
}
```

3. Restart Claude Code or reload the project.

### For Claude.ai Projects

1. Navigate to the repository and open `email-marketing/SKILL.md`
2. Copy the entire contents
3. Create a new project at [claude.ai](https://claude.ai)
4. Paste the skill content into the project's custom instructions

### For API Integrations

Include the contents of `email-marketing/SKILL.md` in your system prompt:

```python
import anthropic
import os

with open('email-marketing/SKILL.md', 'r') as f:
    email_skill = f.read()

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=4096,
    system=email_skill,
    messages=[
        {"role": "user", "content": "Help me fix my email deliverability issues"}
    ]
)
```

## Skill Structure

The skill is organized into focused modules:

- **`authentication.md`** — SPF, DKIM, DMARC setup and troubleshooting
- **`list-building.md`** — Lead magnets, opt-in strategies, subscriber tracking
- **`segmentation-and-data.md`** — Dynamic/static segments, data hygiene, GDPR compliance
- **`copywriting.md`** — Subject lines, email structure, CTAs, spam trigger words
- **`automation-and-sequences.md`** — Trigger-based workflows, sequence design
- **`deliverability.md`** — Inbox placement, IP warming, spam folder recovery
- **`esp-and-reference.md`** — Provider comparison, legislation reference, glossary

## Common Usage Patterns

### Deliverability Troubleshooting

```
"My emails are going to spam. I'm sending from sendgrid.net, 
my open rate dropped from 22% to 3% last week, and Gmail is 
the worst performer. What's wrong?"
```

Claude will diagnose:
- Shared IP reputation issues
- Authentication gaps (likely missing DMARC)
- Engagement-based filtering triggers
- Provide step-by-step remediation

### Writing Email Sequences

```
"Create a 5-email welcome sequence for new SaaS trial users. 
Product is a project management tool, trial is 14 days, 
main friction point is CSV import complexity."
```

Claude generates:
- Day 0: Welcome + quick win (create first project)
- Day 2: CSV import guide (addresses friction)
- Day 5: Feature showcase (collaboration tools)
- Day 10: Social proof (case study)
- Day 13: Conversion push (upgrade CTA)

### Authentication Setup

```
"Walk me through setting up SPF, DKIM, and DMARC for my domain 
example.com. I'm using Postmark for transactional email and 
Mailchimp for marketing."
```

Claude provides:
- Exact DNS records for both services
- Conflict avoidance strategies
- Testing and validation steps
- DMARC policy recommendations

### ESP Selection

```
"I need an ESP for a 50k subscriber ecommerce list. 
Heavy personalization, abandoned cart is critical, 
budget is $500/month. Compare options."
```

Claude evaluates:
- Klaviyo (ecommerce-native, strong on abandoned cart)
- Drip (automation-focused, good personalization)
- ActiveCampaign (budget-friendly, solid features)
- Provides pricing, feature comparison, recommendation

### Segmentation Strategy

```
"I have purchase history, email engagement data, and 
product category preferences. How should I segment?"
```

Claude recommends:
- RFM segmentation (Recency, Frequency, Monetary)
- Engagement-based tiers (active, warming, cold)
- Category affinity segments
- Automated vs. static segment uses

## Configuration Examples

### Setting Up DMARC Monitoring

```dns
_dmarc.example.com. IN TXT "v=DMARC1; p=none; rua=mailto:dmarc@example.com; ruf=mailto:dmarc-forensic@example.com; fo=1"
```

- `p=none` — Monitor mode (start here)
- `rua` — Aggregate reports
- `ruf` — Forensic reports
- `fo=1` — Report if either SPF or DKIM fails

### Klaviyo Abandoned Cart Flow (API)

```javascript
// Track cart abandonment event
fetch('https://a.klaviyo.com/api/track', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    token: process.env.KLAVIYO_PUBLIC_API_KEY,
    event: 'Abandoned Cart',
    customer_properties: {
      $email: 'customer@example.com'
    },
    properties: {
      $value: 129.99,
      items: [
        { product_name: 'Widget', sku: 'WID-001', price: 49.99 },
        { product_name: 'Gadget', sku: 'GAD-002', price: 80.00 }
      ]
    }
  })
});
```

Trigger 3-email sequence:
1. 1 hour: "Forgot something?"
2. 24 hours: 10% discount code
3. 72 hours: Last chance + free shipping

### Mailchimp Merge Tags for Personalization

```html
<!DOCTYPE html>
<html>
<body>
  <h1>Hi *|FNAME|*,</h1>
  <p>Based on your interest in *|INTEREST_CATEGORY|*, we thought you'd like:</p>
  
  *|IF:PURCHASE_COUNT > 0|*
    <p>Welcome back! Your last order was *|LAST_PRODUCT|*.</p>
  *|ELSE:|*
    <p>First-time customers get 15% off with code WELCOME15</p>
  *|END:IF|*
  
  <a href="*|PRODUCT_URL|*">Shop Now</a>
</body>
</html>
```

### SendGrid Suppression Group Setup

```bash
curl -X POST https://api.sendgrid.com/v3/asm/groups \
  -H "Authorization: Bearer $SENDGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Product Updates",
    "description": "New features and product announcements",
    "is_default": false
  }'
```

Users can unsubscribe from this category without leaving all emails.

## Troubleshooting

### "My open rates seem inflated"

Apple Mail Privacy Protection (MPP) pre-loads images:
- Opens are less reliable for engagement measurement
- Focus on clicks, conversions, and reply rates instead
- Segment out Apple Mail users for accurate baseline

### "Gmail sends everything to Promotions tab"

This is normal for marketing email:
- DMARC alignment improves Primary tab odds
- Personalization and plain text help
- Don't fight it—optimize for Promotions tab success
- Use annotations (JSON-LD) for richer previews

### "Spam score is high but I'm not spamming"

Common triggers:
- ALL CAPS subject lines
- Excessive exclamation marks!!!
- Spammy words: "free," "act now," "limited time"
- Large images, no text
- Broken HTML or missing plain-text version
- No physical address in footer (CAN-SPAM violation)

### "Authentication records aren't validating"

```bash
# Check SPF
dig example.com TXT | grep "v=spf1"

# Check DKIM (replace 'selector' with your actual selector)
dig selector._domainkey.example.com TXT

# Check DMARC
dig _dmarc.example.com TXT
```

Common issues:
- SPF record exceeds 10 DNS lookups (use `include` sparingly)
- DKIM selector mismatch between ESP and DNS
- DMARC record has syntax errors (use validator)

## Advanced Patterns

### Re-engagement Workflow Logic

```
IF subscriber hasn't opened in 90 days:
  → Send "We miss you" email with preference center
  
  IF opens: 
    → Move to "warming" segment
  ELSE IF clicks:
    → Move to "active" segment
  ELSE (after 30 more days):
    → Send final "Stay or go?" email
    
    IF no action:
      → Suppress (don't send marketing, keep in database)
```

### Sunset Policy Implementation

```sql
-- Example query for sunset suppression
SELECT email 
FROM subscribers 
WHERE last_open_date < DATE_SUB(NOW(), INTERVAL 180 DAY)
  AND last_click_date < DATE_SUB(NOW(), INTERVAL 180 DAY)
  AND signup_date < DATE_SUB(NOW(), INTERVAL 270 DAY);
```

Protects sender reputation by excluding chronically unengaged subscribers.

## Best Practices from the Skill

- **Always use double opt-in** for cold audiences (lead magnets, ads)
- **Single opt-in acceptable** for warm contexts (checkout, account creation)
- **Start DMARC at `p=none`**, move to `p=quarantine` after monitoring
- **Warm IPs gradually** — double send volume every 3-5 days
- **Segment on engagement first**, demographics second
- **Test subject lines** with 10% A/B split before full send
- **Include plain-text version** of every HTML email
- **Unsubscribe link required** in every marketing email (legal + deliverability)
- **Clean your list quarterly** — remove hard bounces, suppress unengaged
- **Track UTM parameters** for every link to measure campaign ROI

## Compliance Quick Reference

| Regulation | Applies To | Key Requirement |
|------------|-----------|-----------------|
| CAN-SPAM | US recipients | Physical address, unsubscribe link, honor opt-outs within 10 days |
| GDPR | EU recipients | Explicit consent, right to erasure, data processing agreements |
| CASL | Canadian recipients | Express consent required, must identify sender |
| CCPA | California residents | Right to opt-out of data sale, privacy policy disclosure |

## Example Queries for Claude

```
"My bounce rate is 8% — is that normal?"
"Write 10 subject line variations for a webinar reminder"
"Compare Sendinblue vs Mailgun for transactional email"
"How do I set up a product recommendation sequence?"
"What's a good click-to-open rate for ecommerce?"
"Create a sunset policy for inactive subscribers"
"Why are my emails rendering badly in Outlook?"
```

## Resources

The skill references real-world scenarios, ESP-specific quirks, and regulatory requirements. When Claude has this skill active, it will:

- Provide specific DNS records, not generic templates
- Recommend ESPs based on actual use case (not affiliate links)
- Give opinionated guidance ("do this, not that") where appropriate
- Reference actual spam filter behavior (Gmail, Outlook, Yahoo)
- Calculate realistic metrics and benchmarks by industry

---

**Maintenance**: This skill is based on the MIT-licensed repository. Contributions welcome at [github.com/jacquescorbytuech/email-marketing-skill](https://github.com/jacquescorbytuech/email-marketing-skill).
