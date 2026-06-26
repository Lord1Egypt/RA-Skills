# Multi-Channel Strategy Guide for Win-Back Campaigns

This guide covers how to deploy email, SMS, and paid ads as coordinated channels in a win-back campaign. It addresses channel selection by segment, timing and sequencing across channels, platform-specific best practices, and cross-channel orchestration.

---

## Channel Selection Framework

Not every segment warrants every channel. Use this matrix to determine which channels to activate for each segment tier.

| Segment Tier | Email | SMS | Paid Ads | Rationale |
|---|---|---|---|---|
| Tier 1: Champions at Risk | Yes (5-6 touches) | Yes (1-2 touches) | Yes (retargeting) | Maximum investment justified by high revenue potential and reactivation probability |
| Tier 2: Loyal Lapsed | Yes (3-4 touches) | Conditional (1 touch, only if prior SMS engagement) | Yes (retargeting, lower budget) | Strong ROI potential; SMS only where consent and engagement history support it |
| Tier 3: Occasional Defectors | Yes (2-3 touches) | No | No | Email-only keeps costs low; ad spend unlikely to be ROI-positive |
| Tier 4: One-and-Done | Yes (1-2 touches) | No | No | Minimal investment; test vs. holdout to validate any ROI |
| Tier 5: Sunset | Yes (1 touch -- sunset email) | No | No | Final permission confirmation only |

**Decision rule:** Add a channel only when the incremental cost is justified by the incremental reactivation revenue it is expected to generate. SMS adds approximately $0.02-0.05 per message; paid ads add $0.50-2.00 per reached user. These costs must be weighed against the segment's predicted reactivation rate and AOV.

---

## Email Strategy

### Role in the Win-Back Sequence

Email is the backbone of every win-back campaign. It carries the primary narrative arc, delivers the richest content, and has the lowest marginal cost per send. Every segment receives email; the number of touches and personalization depth vary by tier.

### Best Practices

**Subject lines for lapsed audiences:**
- Avoid generic "We miss you" in every email. Use it once at most.
- Reference specific products or categories: "Your favorite [Product Name] is still here"
- Create curiosity: "A lot has changed since your last visit"
- Urgency without false scarcity: "Your 15% off expires Friday"
- Test emoji vs. no emoji -- lapsed audiences often respond differently than active subscribers.

**Sender and preheader:**
- Use a personal sender name for Tier 1 ("Sarah from [Brand]") and brand name for lower tiers.
- Preheader text should complement, not repeat, the subject line.
- Consider a dedicated sending subdomain for win-back to isolate deliverability impact.

**Content and design:**
- Keep emails concise. Lapsed customers have low engagement intent -- long emails increase the chance they scan and delete.
- Lead with one clear CTA per email. Do not present 5 product categories and 3 offers simultaneously.
- Include dynamic product blocks showing items the customer previously purchased or browsed, or top sellers in their preferred categories.
- Touch 1 should never include a discount. Lead with product value, newness, or emotional connection.
- Progressive disclosure of incentives across the sequence: no offer, then free shipping, then percentage off, then best offer with deadline.

**Deliverability management for lapsed sends:**
- Segment deeply lapsed contacts (6+ months no engagement) from recently lapsed contacts and send separately.
- Ramp sending volume to deeply lapsed segments over 2-3 days: 10% on Day 1, 25% on Day 2, remaining on Day 3.
- Monitor bounce rates, spam complaint rates, and inbox placement rates after each send. Pause if spam complaints exceed 0.08% or bounce rate exceeds 3%.
- Use engagement-based sending: within each batch, prioritize contacts who have opened or clicked any email in the last 180 days.
- Consider re-permission campaigns for contacts with zero engagement in 12+ months before including them in the win-back flow.

**Timing:**
- Send-time optimization (STO) is particularly valuable for win-back, since you may not have recent engagement data to inform timing. Use your ESP's STO feature if available.
- Minimum 4-5 days between email touches. 7 days is safer for lower-tier segments.
- Avoid sending win-back emails during major promotional periods (Black Friday, holiday sales) when inbox competition is highest.

---

## SMS Strategy

### Role in the Win-Back Sequence

SMS serves as a high-attention, time-sensitive complement to email. It is most effective for delivering urgent, concise offers to customers who have previously engaged with SMS. SMS should never be the primary win-back channel -- it is too expensive and too intrusive for broad deployment.

### Best Practices

**Compliance (non-negotiable):**
- Verify explicit SMS opt-in consent for every recipient. Email consent does not equal SMS consent.
- Include opt-out instructions in every message ("Reply STOP to unsubscribe").
- Respect quiet hours: no messages before 9am or after 9pm in the recipient's local time zone. Some jurisdictions have stricter windows.
- Maintain records of consent date, source, and language for every subscriber.
- Under TCPA, penalties for non-compliant SMS messages range from $500 to $1,500 per message. This is not a risk to take casually.

**Message construction:**
- Target 160 characters or fewer to avoid multi-segment messages (which double your cost).
- Lead with the value proposition or offer, not the brand name.
- Include a trackable short link. Use branded short domains where possible (e.g., brand.link/winback).
- Personalize with first name and, if possible, a product reference.
- Create genuine urgency: "48-hour window" or "ends tonight" -- but only if the deadline is real.

**Example messages by touch purpose:**

*Check-in (no offer):*
> Hey [Name], your [Product] restock might be due. Tap to reorder: [link]. Reply STOP to opt out.

*Incentive delivery:*
> [Name], we saved you 15% off your next order. Use code WELCOME15 -- expires in 48hrs: [link]. Reply STOP to unsub.

*Final urgency:*
> Last chance, [Name]. Your 20% off expires at midnight: [link]. Reply STOP to opt out.

**Frequency and placement in sequence:**
- Maximum 2 SMS messages in any win-back sequence, regardless of segment tier.
- Place SMS touches between email touches to create a multi-channel surround effect, not on the same day as an email.
- Best SMS placement is typically mid-sequence (after 1-2 emails have established context) and for the strongest offer.

---

## Paid Ads Strategy

### Role in the Win-Back Sequence

Paid ads (primarily Meta and Google) serve as ambient reinforcement. They keep the brand visible to lapsed customers who may not be opening emails, and they create a multi-touchpoint experience that increases perceived campaign importance. Paid ads rarely drive direct conversions in isolation for win-back -- their value is in supporting email and SMS conversion.

### Platform-Specific Guidance

#### Meta (Facebook / Instagram)

**Audience setup:**
- Upload lapsed customer segments as Custom Audiences via CSV or, preferably, server-side API (Conversions API / CAPI).
- Match rates for email-based audiences typically range from 50-70%. Phone number matching improves rates to 60-80%.
- Create separate ad sets for each win-back segment tier to control budget allocation and messaging.
- Exclude recently converted customers using a dynamic exclusion audience updated daily or via real-time CAPI events.

**Creative recommendations:**
- Use carousel ads showcasing products from the customer's preferred categories.
- Include social proof (review counts, star ratings, UGC photos) -- lapsed customers may need reassurance that the brand is still worth their attention.
- Video ads (15-30 seconds) showing new products or brand story updates outperform static images for win-back on Meta.
- Ad copy should acknowledge the relationship: "It's been a while" or "See what's new" rather than generic prospecting language.

**Budget and bidding:**
- Set frequency caps at 3-5 impressions per user per week. Higher frequency for win-back leads to ad fatigue and negative sentiment.
- Allocate 60-70% of ad budget to Tier 1 and Tier 2 segments.
- Use cost-per-click (CPC) bidding rather than impressions-based bidding to optimize for engagement.
- Typical budget: $0.50-1.50 per reached lapsed customer over the campaign duration.

#### Google Ads

**Customer Match:**
- Upload lapsed customer lists to Google Customer Match for search and display remarketing.
- Match rates are typically lower than Meta (40-60%), depending on whether customers use Gmail.
- Use Customer Match for search campaigns targeting branded and category keywords -- when a lapsed customer searches for your brand or product category, your ad appears with a win-back message.

**Display remarketing:**
- Run display ads across Google Display Network targeting your uploaded customer list.
- Use responsive display ads with multiple headlines and images for automated optimization.
- Set frequency caps at 3 impressions per user per day on display.

**YouTube (optional):**
- For brands with video assets, YouTube retargeting to lapsed customer lists can be effective for brand re-awareness.
- Use non-skippable 15-second ads or skippable 30-second ads with the key message in the first 5 seconds.

### Cross-Platform Coordination

- Align ad creative themes with the current email/SMS touch in the sequence. If Touch 3 is offering free shipping, the ads running during that period should reinforce free shipping.
- Stagger ad activation: start paid ads 2-3 days after the first email touch so customers have already been re-exposed to the brand before seeing ads.
- Pause ads for customers who convert, using platform-specific exclusion audiences updated at least daily.

---

## Cross-Channel Orchestration

### Suppression Logic

Real-time cross-channel suppression is critical to avoid post-conversion annoyance and wasted spend.

| Event | Email Action | SMS Action | Paid Ads Action | Target Latency |
|---|---|---|---|---|
| Purchase | Exit flow immediately | Exit flow immediately | Add to exclusion audience | < 1 hour (email/SMS), < 4 hours (ads) |
| Email unsubscribe | Exit email flow | No change | No change | Immediate |
| SMS opt-out (STOP) | No change | Exit SMS flow | No change | Immediate |
| Spam complaint | Exit email flow | Consider removal | No change | Immediate |
| Hard bounce | Remove from email | No change | No change | Immediate |

### Orchestration Architecture

**Option A: ESP as orchestration layer (simpler)**
- Use your ESP (Klaviyo, Iterable, Braze) as the central orchestration engine.
- ESP triggers email sends directly and fires webhooks/API calls to SMS and ad platforms for audience updates.
- Pros: single workflow view, lower technical complexity.
- Cons: ad platform audience updates may have higher latency (hours vs. minutes).

**Option B: CDP as orchestration layer (more robust)**
- Use a Customer Data Platform (Segment, mParticle, Rudderstack) to manage audience membership and distribute events to all channels.
- CDP receives purchase events in real-time and updates ESP, SMS platform, and ad platform audiences simultaneously.
- Pros: fastest suppression, single source of truth for customer state.
- Cons: requires CDP infrastructure, higher cost, more complex setup.

**Recommendation:** For most ecommerce brands under $50M revenue, Option A is sufficient. Invest in Option B when you have the engineering resources and the campaign scale to justify it.

### Timing Coordination

A typical multi-channel sequence timeline for a Tier 1 segment:

```
Day 0:  Email Touch 1 (no offer)
Day 2:  Paid ads begin (brand awareness creative)
Day 5:  SMS Touch 1 (check-in, no offer)
Day 8:  Email Touch 2 (new arrivals / recommendations)
Day 10: Paid ads rotate to product-focused creative
Day 14: Email Touch 3 (free shipping offer)
Day 17: SMS Touch 2 (15% off, 48hr deadline)
Day 21: Email Touch 4 (best offer, urgency)
Day 24: Paid ads rotate to offer-focused creative
Day 30: Email Touch 5 (final offer + sunset warning)
Day 35: Paid ads end. Sunset email if no conversion.
```

**Key principles:**
- Never send email and SMS on the same day.
- Align ad creative rotation with the current email offer stage.
- Allow at least 48 hours after an SMS touch before sending the next email (give the SMS time to drive its own conversion).
- End paid ads 1-3 days after the final email/SMS touch to capture any delayed responders.

---

## Channel Performance Benchmarks

Use these as starting reference points. Actual performance varies significantly by brand, vertical, and audience quality.

| Metric | Email | SMS | Paid Ads (Meta) | Paid Ads (Google) |
|---|---|---|---|---|
| Open / View Rate | 15-25% (lapsed) | 85-95% | N/A | N/A |
| Click / CTR | 1.5-4% | 8-15% | 0.8-2% | 1-3% (display), 3-8% (search) |
| Conversion Rate | 0.5-2% | 1-4% | 0.3-1% | 0.5-2% (display), 2-5% (search) |
| Cost per Send/Impression | $0.001-0.005 | $0.02-0.05 | $0.01-0.05 (CPM basis) | $0.30-1.50 (CPC) |
| Unsubscribe / Opt-out | 0.5-2% | 1-3% | N/A | N/A |

**Note:** SMS conversion rates appear high because SMS audiences are pre-qualified (opted in, previously engaged). This does not mean SMS is "better" than email -- it reaches a smaller, more engaged subset.
