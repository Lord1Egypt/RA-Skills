# Creator Payments + CPM Report Template

Use this format for Slack-ready creator payout queue reports with org-wide CPM context.

## Instructions

- Sort upcoming payouts by current in-progress payout amount descending.
- List up to Top 10 creators. If fewer than 10 creators exist, list all of them and add a total creators line.
- Use Creator Hub upcoming payout links filtered by both creator and campaign:
  `https://viral.app/app/creator-hub/payouts/upcoming?creatorIds=<orgCreatorId>&campaigns=<campaignId>`
- Compare each payout row against the most recent completed payout window for the same creator and campaign when available.
- Use `⬆️ / ⬇️ / ➡️ / 🆕` for payout row trends.
- Keep payout amounts exact, for example `$898.00`.
- For the KPI section, compare the current period against the immediately previous equal-length period.
- Use compact numbers for view totals, for example `16.71M`.
- Format Effective CPM and Paid CPM to 4 decimals.
- Format Spend per video to 2 decimals.
- If both paid CPM values are `0`, say `no paid payouts in this comparison window`.
- Keep separators and spacing between sections.

## Template (copy this block and replace placeholders)

**📅 Upcoming payout window:** `{{WINDOW_START}} → {{WINDOW_END}}`
**↔️ KPI comparison:** `{{CURRENT_PERIOD_START}} → {{CURRENT_PERIOD_END}}` vs `{{PREV_PERIOD_START}} → {{PREV_PERIOD_END}}`
**Trend basis for payout rows:** `{{WINDOW_START}} → {{WINDOW_END}}` partial vs `{{PREV_WINDOW_START}} → {{PREV_WINDOW_END}}` completed

----------------------------------

### 💸 Upcoming Creator Payouts (Top by amount)

🥇 [{{CREATOR_1_NAME}}]({{CREATOR_1_LINK}}) — **{{CREATOR_1_AMOUNT}}** {{CREATOR_1_TREND}} ({{CREATOR_1_DELTA}})

🥈 [{{CREATOR_2_NAME}}]({{CREATOR_2_LINK}}) — **{{CREATOR_2_AMOUNT}}** {{CREATOR_2_TREND}} ({{CREATOR_2_DELTA}})

🥉 [{{CREATOR_3_NAME}}]({{CREATOR_3_LINK}}) — **{{CREATOR_3_AMOUNT}}** {{CREATOR_3_TREND}} ({{CREATOR_3_DELTA}})

:four: [{{CREATOR_4_NAME}}]({{CREATOR_4_LINK}}) — **{{CREATOR_4_AMOUNT}}** {{CREATOR_4_TREND}} ({{CREATOR_4_DELTA}})

:five: [{{CREATOR_5_NAME}}]({{CREATOR_5_LINK}}) — **{{CREATOR_5_AMOUNT}}** {{CREATOR_5_TREND}} ({{CREATOR_5_DELTA}})

:six: [{{CREATOR_6_NAME}}]({{CREATOR_6_LINK}}) — **{{CREATOR_6_AMOUNT}}** {{CREATOR_6_TREND}} ({{CREATOR_6_DELTA}})

:seven: [{{CREATOR_7_NAME}}]({{CREATOR_7_LINK}}) — **{{CREATOR_7_AMOUNT}}** {{CREATOR_7_TREND}} ({{CREATOR_7_DELTA}})

:eight: [{{CREATOR_8_NAME}}]({{CREATOR_8_LINK}}) — **{{CREATOR_8_AMOUNT}}** {{CREATOR_8_TREND}} ({{CREATOR_8_DELTA}})

:nine: [{{CREATOR_9_NAME}}]({{CREATOR_9_LINK}}) — **{{CREATOR_9_AMOUNT}}** {{CREATOR_9_TREND}} ({{CREATOR_9_DELTA}})

:keycap_ten: [{{CREATOR_10_NAME}}]({{CREATOR_10_LINK}}) — **{{CREATOR_10_AMOUNT}}** {{CREATOR_10_TREND}} ({{CREATOR_10_DELTA}})

{{#if TOTAL_CREATORS_LINE}}
:keycap_ten: Total creators in window — **{{TOTAL_CREATORS}}**
{{/if}}

----------------------------------

### 📊 CPM Snapshot (Org-wide KPIs)

- **Current Effective CPM:** **{{CURRENT_EFFECTIVE_CPM}}** {{EFFECTIVE_CPM_TREND}} ({{EFFECTIVE_CPM_DELTA}})
- **Previous Effective CPM:** **{{PREV_EFFECTIVE_CPM}}**
- **Current Paid CPM:** **{{CURRENT_PAID_CPM}}** {{CURRENT_PAID_CPM_NOTE}}
- **Previous Paid CPM:** **{{PREV_PAID_CPM}}**

----------------------------------

### 🎯 Volume & Efficiency Indicators

- **Eligible views:** **{{ELIGIBLE_VIEWS}}** {{ELIGIBLE_VIEWS_TREND}} ({{ELIGIBLE_VIEWS_DELTA}})
- **Eligible videos:** **{{ELIGIBLE_VIDEOS}}** {{ELIGIBLE_VIDEOS_TREND}} ({{ELIGIBLE_VIDEOS_DELTA}})
- **Published videos:** **{{PUBLISHED_VIDEOS}}** {{PUBLISHED_VIDEOS_TREND}} ({{PUBLISHED_VIDEOS_DELTA}})
- **Spend per video:** **{{SPEND_PER_VIDEO}}** {{SPEND_PER_VIDEO_TREND}} ({{SPEND_PER_VIDEO_DELTA}})

----------------------------------

### ✅ Next action

- **Total upcoming payout:** **{{TOTAL_UPCOMING_PAYOUT}}**
- **Upcoming payout window end:** **{{WINDOW_END}}**
- **Ask:** {{NEXT_ACTION}}

---

## Optional compact version

Use this when Felix wants a shorter paste-ready Slack block:

```md
**📅 Upcoming payout window:** `{{WINDOW_START}} → {{WINDOW_END}}`
**↔️ KPI comparison:** `{{CURRENT_PERIOD_START}} → {{CURRENT_PERIOD_END}}` vs `{{PREV_PERIOD_START}} → {{PREV_PERIOD_END}}`

1. **[{{CREATOR_1_NAME}}]({{CREATOR_1_LINK}})** — {{CREATOR_1_AMOUNT}} {{CREATOR_1_TREND}} ({{CREATOR_1_DELTA}})
2. **[{{CREATOR_2_NAME}}]({{CREATOR_2_LINK}})** — {{CREATOR_2_AMOUNT}} {{CREATOR_2_TREND}} ({{CREATOR_2_DELTA}})
3. **[{{CREATOR_3_NAME}}]({{CREATOR_3_LINK}})** — {{CREATOR_3_AMOUNT}} {{CREATOR_3_TREND}} ({{CREATOR_3_DELTA}})

- **Effective CPM:** {{CURRENT_EFFECTIVE_CPM}} ({{EFFECTIVE_CPM_DELTA}})
- **Eligible views:** {{ELIGIBLE_VIEWS}} ({{ELIGIBLE_VIEWS_DELTA}})
- **Published videos:** {{PUBLISHED_VIDEOS}} ({{PUBLISHED_VIDEOS_DELTA}})
- **Spend per video:** {{SPEND_PER_VIDEO}} ({{SPEND_PER_VIDEO_DELTA}})
- **Total upcoming payout:** {{TOTAL_UPCOMING_PAYOUT}}
```
