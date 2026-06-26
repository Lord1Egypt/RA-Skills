---
name: SMS Optimizer
description: Craft compelling, policy-safe SMS messages for flash sales, order updates, and retention campaigns that drive clicks without triggering opt-outs.
---

# SMS Optimizer

SMS marketing delivers open rates above 90% and click-through rates that dwarf email, but ecommerce brands consistently struggle with two problems: writing messages that feel valuable rather than spammy within the 160-character constraint, and staying compliant with TCPA, CTIA, and carrier filtering rules that can get your number blacklisted. SMS Optimizer solves both by generating high-converting SMS copy that respects character limits, includes required compliance elements, and uses proven psychological triggers calibrated to your specific campaign type.

## Solves

1. **Copy feels spammy or low-value** — messages triggering opt-outs at above 3% per send because they lead with discount pressure rather than genuine value
2. **Carrier filtering blocking delivery** — messages using known spam triggers (ALL CAPS, excessive punctuation, prohibited shorteners) that get flagged before reaching subscribers
3. **Character count overruns** — copy that exceeds 160 characters once compliance footer and tracking link are included, causing messages to split into two billable segments
4. **Compliance gaps** — missing opt-out language, missing business identification, or transactional messages that include promotional angles prohibited under TCPA
5. **Weak A/B test coverage** — sending only one copy variant when small hook changes can shift click-through by 20–40%
6. **Platform mismatch** — copy that doesn't account for platform-specific footer formatting in Postscript, Attentive, or Klaviyo SMS
7. **Sequence pacing errors** — sending too frequently or at sub-optimal times, burning subscriber goodwill before the customer lifecycle matures

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| **Message opening** | Personalized hook referencing behavior or segment | Benefit-first generic opener | Brand name first with no hook |
| **Character allocation** | Hook 60 + offer 50 + CTA 20 + link/footer reserved | Hook 80 + offer 50 + link/footer reserved | Entire 160 used for copy, no room for link or footer |
| **Urgency language** | Specific deadline ("ends midnight EST") | Relative urgency ("today only") | Vague urgency ("limited time") or no urgency |
| **CTA style** | Single clear action verb ("Shop now", "Claim it") | Two-option CTA ("Shop or reply STOP") | No CTA or passive phrasing |
| **Emoji usage** | 1–2 emojis that match brand voice and reinforce message | 3 emojis, non-redundant | 4+ emojis or emojis duplicating words already written |
| **Compliance footer** | Platform-native opt-out via append setting | Manual "Reply STOP to opt out" at end | No opt-out language or opt-out buried mid-message |
| **Send timing** | 10am–12pm or 6pm–8pm subscriber local time | 9am–10am or 5pm–6pm local | Before 9am, after 9pm, or platform default without review |
| **Link domain** | Branded short domain (e.g. brand.co/spring) | Trusted full URL | bit.ly, tinyurl, or other generic shorteners |

## Workflow

### Step 1 — Gather campaign inputs
Collect all required inputs before writing a single character: campaign type, product or offer details, SMS platform, brand voice preference, and the link destination. If any required input is missing, ask before proceeding. Incomplete inputs produce copy that fails compliance checks or requires full rewrites.

### Step 2 — Calculate character budget
Before writing copy, calculate available characters:
- Total budget: 160 characters (single segment)
- Reserve for tracking link placeholder: 23 characters (standard short URL length)
- Reserve for platform compliance footer: check platform-specific footer length from the Compliance Guide reference
- Available for copy: 160 – link – footer
- If budget is under 70 characters, flag to the user that the message will need a multi-segment format

### Step 3 — Draft primary message
Write the primary message using the character budget from Step 2. Apply the following structure:
- Hook (first 10–15 characters): behavior-triggered or benefit-first opening
- Offer (middle section): specific product, discount, or action — never vague
- CTA (last 10–15 characters before link): single action verb, present tense
- Link placeholder: `[LINK]` notation so the user can see where the tracking URL fits
- Do NOT include the compliance footer in the draft — this is appended automatically by the platform

### Step 4 — Draft A/B variant
Write a second version of the same message with a materially different hook angle. Do not just swap one word — change the psychological approach entirely (e.g., primary uses urgency, variant uses social proof; or primary uses discount framing, variant uses curiosity framing). Both variants must fit the character budget.

### Step 5 — Run compliance check
Before presenting output, check every compliance item in the SMS Quality Checklist (assets/sms-quality-checklist.md). Pay particular attention to:
- Transactional vs. promotional classification (mixing these violates TCPA)
- Business identification presence
- No prohibited claim language for the product category
- Platform-specific opt-out format matches user's stated platform

### Step 6 — Assemble output
Present the full output package in this structure:
1. Primary Message with exact character count
2. A/B Variant with exact character count
3. Character Budget Breakdown (hook / offer / CTA / link / footer allocation)
4. Compliance Checklist confirmation with any flags raised
5. Send Timing Recommendation for the campaign type
6. If a sequence was requested: Cadence Recommendation with intervals and priority ordering

### Step 7 — Deliver sequence (if applicable)
For multi-message sequences (cart abandonment, welcome series, win-back), deliver messages in send order with recommended delay intervals between each. Label each message with its position (Message 1 of 3) and its behavioral trigger (e.g., "Sends 1 hour after cart abandonment if no purchase").

## Examples

### Example 1 — Flash sale SMS

**Inputs:**
- Campaign type: Flash sale
- Offer: 30% off all skincare bundles with code SPRING30, free shipping over $50, ends midnight EST
- Platform: Postscript
- Brand voice: Friendly and casual, 1–2 emojis max
- Link: ourstore.com/spring-sale

**Character budget:**
- Total: 160
- Link placeholder: 23 (Postscript standard short link)
- Postscript footer: appended automatically (not counted in message body)
- Available for copy: 137 characters

**Primary Message (134 characters):**
```
Spring drop is here 🌸 30% off skincare bundles ends midnight — grab yours before it's gone [LINK]
```
Character count: 97 + link = 120 ✓ (17 buffer for personalization prefix if added)

**A/B Variant (curiosity hook):**
```
Your skin's going to thank you for this one 💚 SPRING30 = 30% off bundles today only [LINK]
```
Character count: 88 + link = 111 ✓

**Character Budget Breakdown:**
- Hook: 21 characters ("Spring drop is here 🌸")
- Offer: 55 characters ("30% off skincare bundles ends midnight")
- CTA + link setup: 21 characters ("grab yours before it's gone")
- Link placeholder: 23 characters
- Footer: platform-appended (not in body count)
- Total body: 120/160 ✓

**Compliance Checklist:**
- ✓ Business identified (covered by Postscript sender profile — confirm sender name is set)
- ✓ Opt-out language: platform-appended automatically
- ✓ No prohibited discount claim language for skincare
- ✓ No generic shortener domain
- ✓ Under 160 characters (single segment)
- ✓ Promotional classification: correct for flash sale

**Send Timing Recommendation:** Tuesday–Thursday, 10am–12pm subscriber local time for highest open rates on promotional sends.

---

### Example 2 — Abandoned cart recovery sequence

**Inputs:**
- Campaign type: Abandoned cart recovery (3-message sequence)
- Offer: Items in cart, 10% off first order code SAVE10 if purchased within 24 hours
- Platform: Klaviyo SMS
- Brand voice: Minimal, no emoji, professional
- Link: checkout URL (dynamic, inserted by platform)

**Message 1 of 3 — 1 hour after abandonment (reminder only, no discount):**
```
You left something behind. Your cart is saved and ready when you are. [LINK]
```
Character count: 68 + link = 91 ✓
Note: No discount in Message 1 — preserves margin for subscribers who convert without incentive.

**Message 2 of 3 — 6 hours after abandonment (soft incentive):**
```
Still thinking it over? Use SAVE10 for 10% off your order — good for the next 24 hours. [LINK]
```
Character count: 88 + link = 111 ✓

**Message 3 of 3 — 22 hours after abandonment (urgency + final offer):**
```
Last call: SAVE10 expires in 2 hours. Don't leave 10% off on the table. [LINK]
```
Character count: 72 + link = 95 ✓

**Cadence Recommendation:**
- Message 1: 1 hour post-abandonment
- Message 2: 6 hours post-abandonment (only if no purchase after Message 1)
- Message 3: 22 hours post-abandonment (only if no purchase after Message 2)
- Stop sequence immediately on purchase — configure suppression list in Klaviyo

## Common Mistakes

1. **Including the compliance footer in the character count** — Postscript and Attentive append footers automatically. If you write "Reply STOP to opt out" in your message body AND the platform appends it, your subscribers receive duplicate opt-out language and the message splits across two segments.

2. **Using bit.ly or tinyurl links** — Generic URL shorteners are flagged by carrier filtering algorithms and dramatically reduce deliverability. Use branded short domains or the platform's built-in link shortener.

3. **Writing urgency without specifics** — "Limited time offer" is a spam trigger phrase in carrier filtering systems. "Ends tonight at 11:59pm EST" is specific, credible, and passes filtering.

4. **Sending transactional messages with promotional angles** — Shipping notifications with a discount code appended violate TCPA transactional message rules. Keep transactional and promotional content in separate sends with separate consent paths.

5. **Ignoring subscriber local time** — Sending at 8am platform time when half your list is in PST means sending at 5am. Most SMS platforms support send-time optimization or time zone bucketing — use it.

6. **Not reserving characters for the link** — Writing exactly 160 characters of copy with no room for the tracking link forces the platform to either truncate your message or create a second segment, doubling cost.

7. **Using ALL CAPS for urgency** — ALL CAPS is one of the most reliable carrier filtering triggers. Use italics equivalents ("flash sale"), exclamation points sparingly, or time-specificity to convey urgency instead.

8. **Testing only one variant** — A single copy test wastes send volume. Always prepare two variants with materially different hooks. Even a 5% CTR improvement on a 10,000-subscriber list compounds significantly over an annual send calendar.

9. **Forgetting suppression lists** — Sending promotional SMS to subscribers who already purchased during the same campaign window is the fastest way to drive opt-outs. Always configure active-purchaser suppression before campaign launch.

10. **Writing for desktop reading** — SMS is consumed on mobile lock screens in 2–3 seconds. Long sentences, complex punctuation, and multi-clause offers all hurt mobile readability. Write for a lock screen glance, not a full read.

## Resources

- `references/output-template.md` — Standard output format for all SMS Optimizer deliverables
- `references/compliance-guide.md` — TCPA, CTIA, and platform-specific compliance requirements by campaign type
- `references/carrier-filtering-guide.md` — Known spam trigger words, prohibited link domains, and carrier filtering avoidance techniques
- `assets/sms-quality-checklist.md` — 40-point quality checklist covering copy, compliance, character budget, and deliverability
