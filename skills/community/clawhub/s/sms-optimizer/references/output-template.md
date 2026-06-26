# SMS Optimizer — Output Template

Use this template for every SMS Optimizer deliverable. Fill in all sections. Do not omit sections — if a section is not applicable, write "N/A — [reason]" so the user understands why.

---

## Campaign Summary

| Field | Value |
|---|---|
| Campaign type | [flash sale / abandoned cart / win-back / shipping / welcome / loyalty / review request] |
| Platform | [Postscript / Attentive / Klaviyo SMS / Omnisend / other] |
| Offer / trigger | [brief description] |
| Brand voice | [tone notes] |
| Messages requested | [1 / sequence of N] |

---

## Message 1 [of N]

**Trigger / send time:** [behavioral trigger or scheduled send time]

### Primary Message

```
[Full message text — include [LINK] placeholder where tracking URL goes]
```

**Character count:** [N] characters + [23] link = [total] / 160 ✓ or ⚠️ [flag if over]

---

### A/B Variant

```
[Alternative message with different hook angle]
```

**Character count:** [N] characters + [23] link = [total] / 160 ✓ or ⚠️

**Hook angle difference:** [Explain how the variant hook differs from primary — e.g., "Primary uses urgency, variant uses social proof"]

---

### Character Budget Breakdown

| Element | Characters |
|---|---|
| Hook | [N] |
| Offer details | [N] |
| CTA | [N] |
| Link placeholder | 23 |
| Compliance footer | Platform-appended (not in body) |
| **Total** | **[N] / 160** |

---

### Compliance Checklist

- [ ] Business identified (sender name set in platform profile)
- [ ] Opt-out language present (platform-appended or manually included)
- [ ] No prohibited claim language for product category
- [ ] No generic shortener domains (bit.ly, tinyurl, etc.)
- [ ] Under 160 characters including link placeholder
- [ ] Correct message classification (promotional vs. transactional)
- [ ] Active subscriber consent path confirmed
- [ ] Platform-specific footer format applied

**Flags raised:** [List any compliance issues found, or "None"]

---

### Send Timing Recommendation

**Best window:** [Day and time range in subscriber local time]
**Rationale:** [Brief reason — e.g., "Mid-morning promotional window for highest open rates"]

---

## [Repeat Message blocks for sequences]

---

## Sequence Cadence (if applicable)

| Message | Trigger | Delay | Suppression condition |
|---|---|---|---|
| Message 1 | [behavioral trigger] | [0h / Xh after trigger] | [purchase, opt-out, etc.] |
| Message 2 | No purchase after Msg 1 | [Xh after trigger] | Purchase, opt-out |
| Message 3 | No purchase after Msg 2 | [Xh after trigger] | Purchase, opt-out |

**Important:** Configure purchase suppression on all sequence steps. Sending promotional messages to subscribers who already converted is a primary driver of opt-outs.

---

## Notes and Warnings

[List any flags, limitations, or recommendations not covered above — e.g., "TCPA consent path should be verified for win-back contacts who have been inactive more than 12 months"]
