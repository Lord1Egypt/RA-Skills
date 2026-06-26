# SMS Compliance Guide — TCPA, CTIA, and Platform Requirements

## Overview

SMS marketing in the United States operates under two overlapping compliance frameworks: the Telephone Consumer Protection Act (TCPA) — a federal statute with private right of action — and the CTIA Messaging Principles and Best Practices, a carrier-enforced industry standard. Non-compliance with TCPA carries statutory damages of $500–$1,500 per message sent to non-consenting recipients. Non-compliance with CTIA guidelines results in carrier filtering, sender ID suspension, or number blacklisting.

This guide covers the compliance requirements most relevant to ecommerce SMS use cases.

---

## TCPA Core Requirements

### Express Written Consent
Before sending promotional SMS messages, you must obtain prior express written consent. This means:
- The subscriber must actively opt in (pre-checked boxes do not count)
- The consent must be documented with a timestamp and source
- The consent disclosure must clearly state the subscriber will receive autodialed marketing messages
- Consent cannot be a condition of purchase

**Acceptable consent collection methods:**
- Checkout opt-in checkbox with clear disclosure language
- Pop-up keyword opt-in (e.g., "Text SAVE to 12345")
- Paper sign-up with opt-in language and subscriber signature
- Double opt-in confirmation flow (best practice, not required)

**Not sufficient for promotional SMS:**
- Purchase history
- Email opt-in (separate consent required for SMS)
- Account creation without explicit SMS consent

### Transactional vs. Promotional Classification

| Message type | Consent required | Promotional content allowed |
|---|---|---|
| **Transactional** — order confirmation, shipping update, delivery notification | Implied from purchase | No — adding discounts or CTAs to transactional messages violates TCPA |
| **Promotional** — flash sale, cart abandonment with incentive, win-back, loyalty | Prior express written consent required | Yes |
| **Mixed** — shipping update that includes a discount code | Requires promotional consent level | Avoid — split into separate messages |

### Opt-Out Requirements
- Every promotional message must include a clear opt-out mechanism
- "Reply STOP to opt out" is the standard language — STOP is a carrier-recognized keyword
- You must process opt-outs within 10 business days (TCPA requirement)
- Most SMS platforms process opt-outs automatically and in real time — verify this is configured

### Quiet Hours
Federal TCPA regulations prohibit calls (and by extension, SMS) to residential numbers before 8am or after 9pm in the recipient's local time zone. Most carrier guidelines recommend a tighter window of 9am–8pm. Best practice for ecommerce is 10am–8pm subscriber local time.

---

## Platform-Specific Compliance Requirements

### Postscript
- Opt-out footer is appended automatically — do NOT include "Reply STOP" in your message body
- Footer format: "Reply STOP to opt out. Msg&data rates may apply."
- Footer length: approximately 43 characters (not counted against your 160-character body budget)
- Business identification: configured in Postscript sender settings — confirm brand name is set
- Frequency cap: Postscript recommends no more than 4–6 promotional sends per month

### Attentive
- Opt-out footer appended automatically using Attentive's Two-Tap opt-out system
- Body character limit for clean single-segment: 140 characters (Attentive reserves 20 for footer margin)
- Business ID: set in sender profile
- Attentive applies its own content review on campaign sends — allow 24 hours for review on large sends

### Klaviyo SMS
- Opt-out language: "Reply STOP to unsubscribe. Msg&data rates may apply."
- Klaviyo appends footer; do not duplicate in message body
- Klaviyo uses A2P 10DLC registration — ensure brand and campaign registration is complete before sending
- Character budget recommendation: target 130 characters for body to ensure clean single segment

### Omnisend
- Opt-out appended automatically
- Recommend 130-character body budget for single-segment safety
- Omnisend supports multi-language opt-out for international sends — configure per target market

---

## Campaign-Specific Compliance Flags

### Flash Sales and Promotional Sends
- ✓ Ensure all recipients on the send list have provided express written consent for promotional SMS
- ✓ No superlative claims without substantiation ("best prices anywhere" requires backup)
- ✓ Discount percentage or dollar amount must match actual calculation at checkout
- ✓ Expiration time must be accurate — false urgency with fake countdown timers is an FTC concern separate from TCPA

### Abandoned Cart Recovery
- ✓ Promotional consent is required even for cart abandonment — the TCPA does not create a "cart abandonment exception"
- ✓ If including a discount code, this is a promotional message — transactional-only consent is insufficient
- ✓ Configure suppression for purchasers — sending cart abandonment after purchase is a top opt-out driver
- ✓ CTIA recommends no more than 3 messages in an abandonment sequence

### Win-Back Campaigns
- ✓ Subscribers inactive for 12+ months require consent re-verification before re-adding to promotional flows
- ✓ Win-back messages to lapsed subscribers should include an easy opt-out in the first line
- ✓ Do not reactivate subscribers who previously opted out — maintain a permanent suppression list

### Transactional Messages (Order Confirmations, Shipping Updates)
- ✓ Must be genuinely informational — no discount codes, no CTAs to shop more
- ✓ Can include a link to the order status page — this is transactional
- ✓ Cannot include "While you wait, check out our sale" — this adds promotional content to a transactional message
- ✓ Requires implied consent from transaction — but best practice is to capture explicit SMS consent at checkout

---

## International Compliance Notes

SMS compliance outside the US is governed by different frameworks:
- **Canada:** CASL (Canada's Anti-Spam Legislation) — requires express or implied consent; implied consent has a 2-year limit for business relationships
- **EU/UK:** GDPR and Privacy and Electronic Communications Regulations — prior explicit consent required; legitimate interest does not cover marketing SMS
- **Australia:** Spam Act 2003 — express or inferred consent required; 3-year inferred consent window from transaction

For international sends, consult legal counsel for jurisdiction-specific requirements. This guide covers US domestic sends only.
