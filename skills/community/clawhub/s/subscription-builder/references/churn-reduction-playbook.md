# Churn Reduction Playbook

## Churn Types

**Voluntary churn** -- subscriber actively cancels (product dissatisfaction, over-accumulation, price sensitivity, brand switching). Addressable through onboarding, communication, and retention offers.

**Involuntary churn** -- subscription lapses from payment failure (expired card, insufficient funds). Accounts for 20-40% of total churn. Addressable through dunning management. Easiest to fix.

---

## Proactive Retention

### Early-warning signals

| Signal | Risk threshold | Data source |
|--------|---------------|-------------|
| Skip frequency | 2+ consecutive skips | Subscription platform |
| Email engagement drop | No opens in 45+ days | ESP |
| Support ticket sentiment | Complaint keywords | Help desk |
| Portal inactivity | No login in 60+ days | Subscription platform |
| Frequency extensions | Lengthened interval 2+ times | Subscription platform |
| Low product rating | Rating 2 or below | Post-delivery survey |

### Interventions by risk level

**Low risk (1 signal):** Usage tips email, subtle frequency adjustment prompt. No discounts.

**Medium risk (2 signals):** Personalized email from brand founder or CS team. Product swap suggestion. Highlight unused self-service features.

**High risk (3+ signals):** Direct CS outreach. One-time retention incentive (free bonus product or small discount). Prioritize any open support tickets.

### Category-specific tactics

- **Supplements:** Dosage reminders, wellness streak notifications, seasonal formulation tips
- **Coffee:** Monthly subscriber pick with tasting notes, brew guides, "surprise me" rotation option
- **Skincare:** Routine-building content, virtual consultations at 3-month mark, seasonal adjustments
- **Pet food:** Feeding guidelines by breed/age, pet birthday treats, weight management tips

---

## Cancellation Save Flow

### Architecture

**Screen 1 -- Reason collection (required):**
Too much product / Too expensive / Trying different brand / No longer need / Not satisfied with quality / Delivery schedule issue / Other

**Screen 2 -- Reason-matched offer:**

| Reason | Save offer |
|--------|-----------|
| Too much product | Skip next 1-2 orders |
| Too expensive | Smaller size option or prepay discount |
| Trying different brand | Swap to alternative product in catalog |
| No longer need | Pause for 30/60/90 days |
| Not satisfied | Free replacement or refund on last order |
| Delivery schedule | Adjust frequency |

**Screen 3 -- Fallback:** X% off next order if Screen 2 declined.

**Screen 4 -- Confirmation:** Process cancellation, issue comeback code valid 60 days.

### Rules
- Maximum 3 offers before processing cancellation
- Visible "cancel now" link on every screen -- no dark patterns
- Log all interactions for analysis
- Rate-limit: do not repeat same offer within 90 days for returning save-flow visitors

### Benchmarks
- Overall save rate: 15-20% (good), 25-35% (great)
- Skip/pause acceptance: 25-35% (good), 40-50% (great)
- Discount acceptance: 10-15% (good), 18-25% (great)

---

## Win-Back Sequences

| Timing | Content | Goal |
|--------|---------|------|
| Day 7 | Reason-specific email addressing cancellation cause, 1-click reactivation link | Catch quick regret |
| Day 21 | Value content -- subscriber success story, new products since cancellation | Rebuild interest |
| Day 45 | Reactivation offer: X% off next 3 orders, 14-day deadline | Convert with urgency |
| Day 75 | Final attempt with strongest offer | Last dedicated outreach |
| Day 90+ | Move to general marketing list | End win-back sequence |

**Benchmarks:** Total win-back recovery rate 8-15% of cancelled subscribers. Reactivated subscriber 90-day retention: 55-65%.

---

## Dunning Management

| Event | Timing | Action |
|-------|--------|--------|
| Initial failure | Day 0 | Smart retry (different time of day) |
| Retry 1 | Day 1 | Retry + email with direct payment update link |
| Retry 2 | Day 3 | Retry + email emphasizing subscription at risk |
| Retry 3 | Day 5 | Retry + SMS (if opted in) |
| Final | Day 7 | Last retry + "subscription pauses tomorrow" email |
| Paused | Day 8 | Pause subscription + reactivation email |

**Best practices:**
- Use Visa Account Updater / Mastercard ABU for automatic card updates (recovers 15-25% of involuntary churn)
- Send from a human name, not no-reply
- Deep-link to payment update page, not generic login
- Never retry more than 4 times total
- Target: recover 50-70% of initially failed payments

---

## Monthly Churn Review

1. Total churn rate (voluntary + involuntary)
2. Churn by signup cohort (recent cohorts churning faster = acquisition quality issue)
3. Churn by cancellation reason (rank by volume to identify systemic issues)
4. Save flow conversion by offer type
5. Dunning recovery rate
6. Win-back reactivation count

**Red flags:** Monthly voluntary churn >12%, order-2 drop-off >30%, dunning recovery <30%, "not satisfied" as top cancellation reason (>25%).
