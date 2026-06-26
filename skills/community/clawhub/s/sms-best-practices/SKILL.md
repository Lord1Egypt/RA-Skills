---
name: sms-best-practices
description: Provides SMS compliance, formatting, and delivery best practices for the Sendly API. Covers TCPA compliance, quiet hours, opt-out handling, E.164 phone formatting, message segmentation, and carrier verification. Applies when building SMS features that must be compliant and deliverable.
---

# SMS Best Practices

## Phone number formatting

Always use E.164 format: `+{country_code}{number}` with no spaces, dashes, or parentheses.

| Input | E.164 | Valid? |
|---|---|---|
| (415) 555-1234 | +14155551234 | After formatting |
| 415-555-1234 | +14155551234 | After formatting |
| +14155551234 | +14155551234 | Yes |
| 4155551234 | +14155551234 | Need country code |

## Message types and compliance

**transactional**: OTP codes, order confirmations, appointment reminders, account alerts, shipping updates. Allowed 24/7. The recipient has an existing relationship with the sender.

**marketing**: Promotions, sales, newsletters, product announcements. Subject to:
- Quiet hours: 9pm–8am in the recipient's local timezone
- Prior express written consent required (TCPA)
- Must include opt-out instructions

Misclassifying marketing as transactional violates TCPA and can result in fines up to $1,500 per message.

## Opt-out handling

Sendly automatically handles opt-outs. When a recipient replies STOP, UNSUBSCRIBE, CANCEL, END, or QUIT:
- The number is added to the opt-out list
- Future sends to that number return `opted_out` error
- An `opt_out.created` webhook event fires

Do not attempt to send to opted-out numbers. Check `message.status` for `opted_out` errors.

Opt-out status is checked automatically when sending — the API returns an `opted_out` error if the recipient has unsubscribed.

## Quiet hours

Marketing messages are blocked during quiet hours (9pm–8am recipient local time). Sendly enforces this automatically — the API returns `quiet_hours_violation` if you attempt a marketing send during quiet hours.

Transactional messages are exempt from quiet hours.

## Message segmentation

SMS messages are limited to 160 characters (GSM-7 encoding) or 70 characters (UCS-2 for emoji/Unicode). Longer messages are split into segments:

| Encoding | Single segment | Multi-segment per part |
|---|---|---|
| GSM-7 (ASCII) | 160 chars | 153 chars |
| UCS-2 (emoji/Unicode) | 70 chars | 67 chars |

Each segment costs credits separately. Keep messages concise.

## SHAFT content filtering

Sendly blocks messages containing prohibited content categories (SHAFT):
- **S**ex/adult content
- **H**ate speech
- **A**lcohol
- **F**irearms
- **T**obacco/drugs

Messages flagged by SHAFT filtering return `content_violation` error.

## Credit costs

- US/CA: 2 credits ($0.02) per message segment
- International: varies by destination (see country requirements)
- 1 credit = $0.01

Check balance: `GET /api/v1/credits`

## Carrier verification

To send SMS in the US/CA, your toll-free number must be verified by carriers. This requires:
- Business name and address
- Website URL (use hosted business pages if you don't have one)
- Use case description
- Sample messages

Verification takes 1–5 business days. Use sandbox mode (`sk_test_*` keys) while waiting.

## Common errors

| Error | Cause | Fix |
|---|---|---|
| `invalid_phone_number` | Not E.164 format | Format as +{country}{number} |
| `insufficient_credits` | Balance too low | Purchase credits at sendly.live |
| `quiet_hours_violation` | Marketing during 9pm–8am | Use transactional type or wait |
| `opted_out` | Recipient unsubscribed | Do not retry — respect opt-out |
| `content_violation` | SHAFT filter triggered | Revise message content |
| `not_verified` | Number not carrier-verified | Complete verification at sendly.live |

## Full reference

- Compliance docs: https://sendly.live/docs/concepts/compliance
- Quiet hours: https://sendly.live/docs/quiet-hours
- Country requirements: https://sendly.live/docs/country-requirements
- Opt-out handling: https://sendly.live/docs/how-to/handle-opt-outs
