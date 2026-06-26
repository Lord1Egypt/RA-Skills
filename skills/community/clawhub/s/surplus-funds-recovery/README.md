# Surplus Funds Recovery System

Turn unclaimed government funds into passive income with this complete automation system.

## The Business Model

- Property foreclosures create surplus funds (sale price > taxes owed)
- Previous owners usually don't know this money exists
- You find it, contact them, file claims, earn 20-30% finder's fee
- Example: $223K surplus → $56K fee in ~30 minutes of work

## What's Included

- Automated county record scanning (Fulton County GA)
- Skip-tracing integration (Intelius/TrueCaller APIs)
- SMS outreach templates with compliance safeguards
- Digital signature capture (RabbitSign/DocuSign)
- Auto-populated claim form generation
- Payment tracking & split calculation
- Full audit trail for compliance

## ROI Example

- 1 case/week = $290K/year (mostly passive after filing)
- Cost per case: $3-5 (skip trace + SMS)
- Your fee: 20-30% of surplus amounts

## Quick Start

```bash
# Configure your business
export BUSINESS_NAME="Your Recovery Business"
export YOUR_FEE_PERCENT=25
export YOUR_PHONE="+1-XXX-XXX-XXXX"

# Run automated scan
npm run scan-fulton --min-amount 10000

# Review flagged high-value cases
cat surplus-cases.json | jq '.[] | select(.amount > 50000)'

# Auto-skip-trace and send compliant SMS
node scripts/skip-trace-owner.js --case CASE-123
node scripts/send-sms-campaign.js --case CASE-123 --template standard
```

## Requirements

- Termux (Android) or Linux environment
- Node.js v16+
- OpenClaw agent system
- API keys: Intelius, Twilio, RabbitSign

## Support

Email: support@cod3black.agency
