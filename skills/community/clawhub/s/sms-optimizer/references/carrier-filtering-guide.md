# Carrier Filtering Guide — Deliverability Optimization for Ecommerce SMS

## Overview

Carrier filtering is the automated process by which mobile carriers (T-Mobile, Verizon, AT&T, and others) screen outbound SMS messages and suppress delivery of content that matches spam or fraud patterns. Unlike email spam filters, carrier filtering happens at the network layer — filtered messages fail silently, with no bounce notification, and your platform analytics will show "delivered to carrier" even when the subscriber never received the message.

Understanding filtering patterns is essential for ecommerce SMS because promotional copy naturally overlaps with spam patterns. This guide covers known filtering triggers and ecommerce-specific avoidance techniques.

---

## How Carrier Filtering Works

Carriers use a combination of:
1. **Keyword matching** — messages containing known spam trigger words
2. **Pattern matching** — structural patterns (excessive punctuation, ALL CAPS runs, specific URL patterns)
3. **Velocity analysis** — high-volume sends from unregistered numbers trigger review
4. **Engagement signals** — high opt-out rates or low reply rates on a number train filters over time
5. **URL reputation** — links to known spam domains or generic shorteners

The most important deliverability investment an ecommerce brand can make is **A2P 10DLC registration** (Application-to-Person, 10-digit long code). This assigns your business a vetted long code that carriers treat with elevated trust and a higher message-per-second throughput.

---

## Spam Trigger Words to Avoid

### High-Risk — Avoid in All Ecommerce SMS

| Trigger phrase | Safer alternative |
|---|---|
| FREE | [specific offer, e.g., "complimentary shipping"] |
| WINNER / YOU WON | [specific prize description] |
| CLICK HERE | "Shop now" or "See it here" |
| GUARANTEED | "Backed by [X]-day return policy" |
| 100% FREE | "No cost to you" or specify exact offer |
| ACT NOW | Specific deadline ("ends tonight at midnight") |
| LIMITED TIME OFFER | "Ends [specific date/time]" |
| URGENT | Specific time-based language |
| RISK-FREE | "[X]-day return, no questions asked" |
| CASH | Specify actual payment method or offer |

### Medium-Risk — Use Sparingly, with Context

| Pattern | Risk level | Guidance |
|---|---|---|
| ALL CAPS words | Medium-High | Maximum 1 word in caps if used for emphasis; prefer title case |
| Multiple exclamation points | Medium | Maximum 1 per message; placed at natural emphasis point |
| Dollar signs ($) | Low-Medium | Fine with specific amounts; avoid "$$$$" patterns |
| Percent signs (%) | Low | Standard use is fine; avoid stacking with other triggers |
| "You've been selected" | High | Never use — common fraud pattern |
| "Congratulations" | Medium | Fine in genuinely earned context (e.g., loyalty milestone) |

### Context-Dependent Phrases

These phrases are fine in ecommerce promotional SMS but can trigger filters when combined with other signals:

- "Exclusive" — acceptable when not combined with urgency spam patterns
- "Deal" — acceptable when specific; "BEST DEAL" in caps is riskier
- "Offer" — standard commercial language; fine in moderate use
- "Save" — acceptable; "SAVE NOW" in caps is riskier
- "Discount" — fine with specific amount; avoid "MASSIVE DISCOUNT"

---

## URL and Link Guidance

### Domains That Cause Carrier Filtering

The following shortener domains are flagged by carrier filtering systems and will significantly reduce deliverability:

- bit.ly
- tinyurl.com
- t.co (Twitter — fine for Twitter; not for SMS)
- ow.ly
- goo.gl (deprecated but still seen)
- rb.gy
- cutt.ly
- Any newly registered shortener domain (< 6 months old)

### Recommended Link Approaches

**Best: Branded short domain**
Register a short version of your brand domain (e.g., brand.co, brand.shop) and use it for SMS links. Carriers treat branded domains with higher trust.

**Good: Platform-native link shortening**
Postscript, Attentive, and Klaviyo all provide their own tracked link shortening. These use the platform's registered domain, which carriers trust more than generic shorteners.

**Acceptable: Full original URL**
Using your actual domain URL (yourstore.com/sale) is fully acceptable but longer. If character budget allows, this is reliable.

**Never: Generic shorteners or newly registered domains**
Do not use bit.ly, tinyurl, or similar. Do not create a "custom" shortener domain that was registered last month.

---

## Structural Patterns That Trigger Filtering

### Message Structure Red Flags

1. **Multiple ALL CAPS words in sequence** — "BIG SALE TODAY ONLY" will likely be filtered
2. **Excessive punctuation** — "Sale ends tonight!!!!!" triggers pattern matching
3. **Symbol stacking** — "$$$ off now $$$" or "🔥🔥🔥🔥🔥" emoji chains
4. **No opt-out mechanism** — Messages with no STOP path are filtered by carriers even if they pass content checks
5. **No business identification** — Anonymous sender messages with no identifiable brand flag fraud patterns
6. **Very short messages with only a link** — "Check this out: [link]" with no context is a classic phishing pattern

### Character Length and Segment Splitting

When a message exceeds 160 characters (GSM-7 encoding), it splits into multiple segments. Multi-segment messages:
- Cost more (billed per segment)
- Are more likely to be filtered (multi-part messages from commercial senders face stricter scrutiny)
- Can arrive out of order on some carrier networks
- Reduce the "glanceability" of the message

Always target single-segment messages (≤160 GSM-7 characters) for promotional ecommerce SMS.

**Note on emoji characters:** Emoji use MMS/Unicode encoding which reduces the single-segment limit from 160 to 70 characters per segment. To stay single-segment with emoji, your total message (including emoji) must be under 160 characters, but be aware that the encoding overhead means some platforms count certain emoji as 2 characters.

---

## Volume and Cadence Signals

Carrier filtering also responds to behavioral signals at the sender number level:

| Signal | Impact | Guidance |
|---|---|---|
| Opt-out rate > 3% per send | High | Review copy quality; reduce send frequency |
| Reply rate < 0.5% | Medium | Low engagement signals low-quality list |
| Complaint rate > 0.1% | High | Carriers receive complaint signals; high rates trigger number review |
| Sudden 10x volume spike | Medium | Sends that spike suddenly on a number trigger velocity filtering |
| High bounce rate | High | Clean list regularly; old numbers become spam traps |

### Recommended Frequency by Campaign Type

| Campaign type | Maximum frequency |
|---|---|
| Promotional (flash sales, seasonal) | 4–6 sends per month |
| Abandoned cart | 1–3 messages per abandonment event |
| Win-back | 1–2 messages per lapsed subscriber per quarter |
| Transactional (orders, shipping) | Unlimited (event-triggered) |
| Welcome series | 2–3 messages over 7 days |

---

## Pre-Send Deliverability Checklist

Before launching any SMS campaign:

- [ ] A2P 10DLC brand and campaign registration is active and approved
- [ ] Sender number has been warmed up with compliant sends over at least 30 days
- [ ] Message body contains no spam trigger words from the High-Risk list
- [ ] No ALL CAPS runs of more than 1 word
- [ ] No generic shortener domains in link
- [ ] Opt-out mechanism is present and functional
- [ ] Business identification is configured in sender profile
- [ ] Message is under 160 characters including link placeholder
- [ ] Suppression list applied (opt-outs, recent purchasers, frequency caps)
- [ ] Send time is within 9am–8pm subscriber local time
