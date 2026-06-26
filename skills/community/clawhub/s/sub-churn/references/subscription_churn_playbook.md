# Subscription churn and dunning playbook

Load when `sub-churn` needs depth. Use by section.

---

## 1. Activity signals (voluntary churn prediction)

| Signal | Interpretation |
|--------|----------------|
| Declining logins / usage | Value not felt; risk of "too expensive" |
| Increased skips or pauses | Price or timing stress |
| Support themes: billing confusion | Fix copy before discounting |
| Spike in "too expensive" in exit survey | Test **downgrade** and **pause** before blanket discount |

---

## 2. Payment failure (involuntary churn)

- Track **attempt count**, **error code** (insufficient funds vs expired card vs fraud).  
- **Soft decline** → retry schedule varies by processor; align messaging to **update card** not blame.  
- **Hard decline** → fewer retries; faster human outreach for high-LTV.

---

## 3. Dunning timing (illustrative—match platform)

| Attempt | Typical offset | Message intent |
|---------|----------------|----------------|
| 1 | Hours 0–24 | Friendly heads-up, fix payment |
| 2 | 24–72h | Urgency + how to avoid interruption |
| 3 | Pre-suspension | Final notice + support line + pause/downgrade if allowed |

Always state **timezone** and **exact policy** from the merchant's stack.

---

## 4. Incentives guardrails

- Prefer **pause** or **downgrade** over **permanent price cut** when margin is tight.  
- If offering **one month off**, cap **eligibility** (once per 12 months) to avoid training delays.  
- Document **finance approval** for any compensation.

---

## 5. Downgrade design

- Preserve **core value** so the tier still feels honest.  
- Name tiers clearly (**Lite / Standard / Pro**).  
- Show **feature diff** in 3 bullets max in email.

---

## 6. Merge fields checklist

`{{first_name}}`, `{{plan_name}}`, `{{amount}}`, `{{next_retry_date}}`, `{{update_payment_url}}`, `{{downgrade_url}}`, `{{pause_url}}`, `{{support_email}}`
