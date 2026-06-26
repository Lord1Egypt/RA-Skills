# SMS Quality Checklist

Use this checklist before finalizing any SMS Optimizer output. A message should pass all items marked REQUIRED before being delivered to the user. Items marked RECOMMENDED represent best practices that significantly improve performance.

---

## Category 1 — Character Budget (REQUIRED)

- [ ] Message body is under 160 GSM-7 characters
- [ ] Link placeholder ([LINK]) is included in body count as 23 characters
- [ ] Compliance footer is NOT included in body count (platform-appended)
- [ ] If emojis are used, total message including emoji is still under 160 characters
- [ ] Character count is stated explicitly in output
- [ ] A/B variant also meets character budget independently

---

## Category 2 — Compliance Fundamentals (REQUIRED)

- [ ] Business is identifiable from sender profile (not anonymous)
- [ ] Opt-out mechanism is present: platform-appended OR manually written (never both)
- [ ] Message classification is stated: promotional OR transactional (not mixed)
- [ ] No transactional message contains discount codes or shop CTAs
- [ ] For promotional messages: express written consent path is noted
- [ ] For win-back/lapsed subscribers: consent re-verification requirement noted

---

## Category 3 — Carrier Filtering Avoidance (REQUIRED)

- [ ] No High-Risk spam trigger words present (see carrier-filtering-guide.md)
- [ ] No ALL CAPS runs of 2+ consecutive words
- [ ] No generic shortener domains (bit.ly, tinyurl, etc.)
- [ ] No excessive punctuation (no more than 1 exclamation point)
- [ ] No emoji chains of 3 or more consecutive identical emoji
- [ ] Link domain is branded, platform-native, or full original URL
- [ ] Message is not a bare link with minimal surrounding text

---

## Category 4 — Copy Quality (RECOMMENDED)

- [ ] Hook is in the first 15 characters and creates reason to read
- [ ] Offer is specific (dollar amount or percentage, not vague "savings")
- [ ] CTA is a single action verb in present tense
- [ ] Urgency is time-specific (not "limited time" — use "ends [date/time]")
- [ ] Message reads naturally on a mobile lock screen in 3 seconds
- [ ] No jargon or internal brand terminology requiring explanation
- [ ] Emoji (if used) reinforce the message rather than repeating words already written
- [ ] Sentence length is short — average under 10 words per sentence

---

## Category 5 — A/B Test Coverage (RECOMMENDED)

- [ ] A/B variant is provided for every message in the output
- [ ] Variant uses a materially different hook angle (not just a word swap)
- [ ] Hook angle difference is explicitly labeled in output
- [ ] Both variants meet the same character budget and compliance requirements
- [ ] Variant does not conflict with primary on offer terms

---

## Category 6 — Platform Configuration (RECOMMENDED)

- [ ] Platform is identified in campaign summary
- [ ] Footer format matches stated platform's requirements
- [ ] Character budget accounts for platform-specific footer length
- [ ] A2P 10DLC registration status is flagged for review if not confirmed
- [ ] Suppression list application is noted (purchasers, opt-outs, frequency caps)

---

## Category 7 — Send Timing (RECOMMENDED)

- [ ] Send timing recommendation is included
- [ ] Recommended window is within 9am–8pm subscriber local time
- [ ] Day of week guidance is included for promotional sends
- [ ] For sequences: cadence table with delays and suppression conditions is included
- [ ] For sequences: "stop on purchase" suppression is explicitly noted

---

## Category 8 — Sequence Logic (if applicable) (REQUIRED for sequences)

- [ ] Messages are numbered and ordered correctly
- [ ] Each message has a behavioral trigger or delay stated
- [ ] Suppression condition for each step is defined
- [ ] Incentive escalation (if used) is logical: Msg 1 no incentive → Msg 2 soft incentive → Msg 3 stronger incentive
- [ ] Total sequence length does not exceed CTIA recommendation for the campaign type
- [ ] Exit conditions (purchase, opt-out) are noted for each step

---

## Category 9 — Flags and Disclaimers (REQUIRED when applicable)

- [ ] Any compliance concerns are flagged clearly in output
- [ ] TCPA note is included if win-back or long-lapsed subscribers are involved
- [ ] "Not legal advice" disclaimer is present for compliance-heavy outputs
- [ ] Platform-specific instructions are accurate for the stated platform version
- [ ] Any assumed inputs (brand voice, platform behavior) are noted as assumptions

---

**Checklist score guide:**
- All REQUIRED items pass + 80%+ RECOMMENDED items pass → Deliver output
- Any REQUIRED item fails → Fix before delivering
- Less than 60% of RECOMMENDED items pass → Note gaps explicitly in output
