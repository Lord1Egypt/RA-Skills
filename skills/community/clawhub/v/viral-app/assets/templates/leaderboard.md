# Leaderboard Report Template

Use this format for weekly reports posted in Slack.

## Instructions

- Always use **Top 10** for all three sections.
- Use **analytics account links** (not creator links).
- Use **period + previous period** for trend comparison.
- Keep **compact numbers** (for example `1.4M`, `180K`).
- Use the emoji style:
  - `🥇` `🥈` `🥉` for ranks 1-3
  - `:four:` `:five:` `:six:` `:seven:` `:eight:` `:nine:` `:keycap_ten:` for ranks 4-10
  - Trend: `⬆️` / `⬇️` / `➡️` / `🆕` where applicable
- Add separators and spacing between sections.

## Link format to use

- Accounts section (views + engagement):
  `https://viral.app/app/analytics/accounts?accounts=<orgAccountId>&viewMode=all`
- Video section (detail links):
  `https://viral.app/app/analytics/videos/<platform>/<platformVideoId>`

---

## Template

Copy this block and replace placeholders.

```md
**📅 Period:** `{{PERIOD_START}} → {{PERIOD_END}}`
**↔️ Comparison period:** `{{PREV_PERIOD_START}} → {{PREV_PERIOD_END}}`

----------------------------------

### 🏆 Top Accounts by Views Gained (7d)

🥇 [{{NAME_1}}](https://viral.app/app/analytics/accounts?accounts={{ORG_ACCOUNT_ID_1}}&viewMode=all) — **{{VIEWS_1}}** {{TREND_EMOJI_1}} ({{DELTA_1}})

🥈 [{{NAME_2}}](https://viral.app/app/analytics/accounts?accounts={{ORG_ACCOUNT_ID_2}}&viewMode=all) — **{{VIEWS_2}}** {{TREND_EMOJI_2}} ({{DELTA_2}})

🥉 [{{NAME_3}}](https://viral.app/app/analytics/accounts?accounts={{ORG_ACCOUNT_ID_3}}&viewMode=all) — **{{VIEWS_3}}** {{TREND_EMOJI_3}} ({{DELTA_3}})

:four: [{{NAME_4}}](https://viral.app/app/analytics/accounts?accounts={{ORG_ACCOUNT_ID_4}}&viewMode=all) — **{{VIEWS_4}}** {{TREND_EMOJI_4}} ({{DELTA_4}})

:five: [{{NAME_5}}](https://viral.app/app/analytics/accounts?accounts={{ORG_ACCOUNT_ID_5}}&viewMode=all) — **{{VIEWS_5}}** {{TREND_EMOJI_5}} ({{DELTA_5}})

:six: [{{NAME_6}}](https://viral.app/app/analytics/accounts?accounts={{ORG_ACCOUNT_ID_6}}&viewMode=all) — **{{VIEWS_6}}** {{TREND_EMOJI_6}} ({{DELTA_6}})

:seven: [{{NAME_7}}](https://viral.app/app/analytics/accounts?accounts={{ORG_ACCOUNT_ID_7}}&viewMode=all) — **{{VIEWS_7}}** {{TREND_EMOJI_7}} ({{DELTA_7}})

:eight: [{{NAME_8}}](https://viral.app/app/analytics/accounts?accounts={{ORG_ACCOUNT_ID_8}}&viewMode=all) — **{{VIEWS_8}}** {{TREND_EMOJI_8}} ({{DELTA_8}})

:nine: [{{NAME_9}}](https://viral.app/app/analytics/accounts?accounts={{ORG_ACCOUNT_ID_9}}&viewMode=all) — **{{VIEWS_9}}** {{TREND_EMOJI_9}} ({{DELTA_9}})

:keycap_ten: [{{NAME_10}}](https://viral.app/app/analytics/accounts?accounts={{ORG_ACCOUNT_ID_10}}&viewMode=all) — **{{VIEWS_10}}** {{TREND_EMOJI_10}} ({{DELTA_10}})

----------------------------------

### 🔥 Top Accounts by Engagement Rate (7d weighted)

🥇 [{{NAME_1_E}}](https://viral.app/app/analytics/accounts?accounts={{ORG_ACCOUNT_ID_1_E}}&viewMode=all) — **{{ER_1}}** {{TREND_EMOJI_1_E}} ({{ER_DELTA_1}})

🥈 [{{NAME_2_E}}](https://viral.app/app/analytics/accounts?accounts={{ORG_ACCOUNT_ID_2_E}}&viewMode=all) — **{{ER_2}}** {{TREND_EMOJI_2_E}} ({{ER_DELTA_2}})

🥉 [{{NAME_3_E}}](https://viral.app/app/analytics/accounts?accounts={{ORG_ACCOUNT_ID_3_E}}&viewMode=all) — **{{ER_3}}** {{TREND_EMOJI_3_E}} ({{ER_DELTA_3}})

:four: [{{NAME_4_E}}](https://viral.app/app/analytics/accounts?accounts={{ORG_ACCOUNT_ID_4_E}}&viewMode=all) — **{{ER_4}}** {{TREND_EMOJI_4_E}} ({{ER_DELTA_4}})

:five: [{{NAME_5_E}}](https://viral.app/app/analytics/accounts?accounts={{ORG_ACCOUNT_ID_5_E}}&viewMode=all) — **{{ER_5}}** {{TREND_EMOJI_5_E}} ({{ER_DELTA_5}})

:six: [{{NAME_6_E}}](https://viral.app/app/analytics/accounts?accounts={{ORG_ACCOUNT_ID_6_E}}&viewMode=all) — **{{ER_6}}** {{TREND_EMOJI_6_E}} ({{ER_DELTA_6}})

:seven: [{{NAME_7_E}}](https://viral.app/app/analytics/accounts?accounts={{ORG_ACCOUNT_ID_7_E}}&viewMode=all) — **{{ER_7}}** {{TREND_EMOJI_7_E}} ({{ER_DELTA_7}})

:eight: [{{NAME_8_E}}](https://viral.app/app/analytics/accounts?accounts={{ORG_ACCOUNT_ID_8_E}}&viewMode=all) — **{{ER_8}}** {{TREND_EMOJI_8_E}} ({{ER_DELTA_8}})

:nine: [{{NAME_9_E}}](https://viral.app/app/analytics/accounts?accounts={{ORG_ACCOUNT_ID_9_E}}&viewMode=all) — **{{ER_9}}** {{TREND_EMOJI_9_E}} ({{ER_DELTA_9}})

:keycap_ten: [{{NAME_10_E}}](https://viral.app/app/analytics/accounts?accounts={{ORG_ACCOUNT_ID_10_E}}&viewMode=all) — **{{ER_10}}** {{TREND_EMOJI_10_E}} ({{ER_DELTA_10}})

----------------------------------

### 🎬 Top 10 Videos (all platforms)

🥇 [{{NAME_1_V}}](https://viral.app/app/analytics/videos/{{PLATFORM_SLUG_1}}/{{PLATFORM_VIDEO_ID_1}}) ({{PLATFORM_NAME_1}}) — **{{VIEWS_V1}}** | **{{ER_V1}} ER** {{TREND_EMOJI_V1}} ({{DELTA_V1}})

🥈 [{{NAME_2_V}}](https://viral.app/app/analytics/videos/{{PLATFORM_SLUG_2}}/{{PLATFORM_VIDEO_ID_2}}) ({{PLATFORM_NAME_2}}) — **{{VIEWS_V2}}** | **{{ER_V2}} ER** {{TREND_EMOJI_V2}} ({{DELTA_V2}})

🥉 [{{NAME_3_V}}](https://viral.app/app/analytics/videos/{{PLATFORM_SLUG_3}}/{{PLATFORM_VIDEO_ID_3}}) ({{PLATFORM_NAME_3}}) — **{{VIEWS_V3}}** | **{{ER_V3}} ER** {{TREND_EMOJI_V3}} ({{DELTA_V3}})

:four: [{{NAME_4_V}}](https://viral.app/app/analytics/videos/{{PLATFORM_SLUG_4}}/{{PLATFORM_VIDEO_ID_4}}) ({{PLATFORM_NAME_4}}) — **{{VIEWS_V4}}** | **{{ER_V4}} ER** {{TREND_EMOJI_V4}} ({{DELTA_V4}})

:five: [{{NAME_5_V}}](https://viral.app/app/analytics/videos/{{PLATFORM_SLUG_5}}/{{PLATFORM_VIDEO_ID_5}}) ({{PLATFORM_NAME_5}}) — **{{VIEWS_V5}}** | **{{ER_V5}} ER** {{TREND_EMOJI_V5}} ({{DELTA_V5}})

:six: [{{NAME_6_V}}](https://viral.app/app/analytics/videos/{{PLATFORM_SLUG_6}}/{{PLATFORM_VIDEO_ID_6}}) ({{PLATFORM_NAME_6}}) — **{{VIEWS_V6}}** | **{{ER_V6}} ER** {{TREND_EMOJI_V6}} ({{DELTA_V6}})

:seven: [{{NAME_7_V}}](https://viral.app/app/analytics/videos/{{PLATFORM_SLUG_7}}/{{PLATFORM_VIDEO_ID_7}}) ({{PLATFORM_NAME_7}}) — **{{VIEWS_V7}}** | **{{ER_V7}} ER** {{TREND_EMOJI_V7}} ({{DELTA_V7}})

:eight: [{{NAME_8_V}}](https://viral.app/app/analytics/videos/{{PLATFORM_SLUG_8}}/{{PLATFORM_VIDEO_ID_8}}) ({{PLATFORM_NAME_8}}) — **{{VIEWS_V8}}** | **{{ER_V8}} ER** {{TREND_EMOJI_V8}} ({{DELTA_V8}})

:nine: [{{NAME_9_V}}](https://viral.app/app/analytics/videos/{{PLATFORM_SLUG_9}}/{{PLATFORM_VIDEO_ID_9}}) ({{PLATFORM_NAME_9}}) — **{{VIEWS_V9}}** | **{{ER_V9}} ER** {{TREND_EMOJI_V9}} ({{DELTA_V9}})

:keycap_ten: [{{NAME_10_V}}](https://viral.app/app/analytics/videos/{{PLATFORM_SLUG_10}}/{{PLATFORM_VIDEO_ID_10}}) ({{PLATFORM_NAME_10}}) — **{{VIEWS_V10}}** | **{{ER_V10}} ER** {{TREND_EMOJI_V10}} ({{DELTA_V10}})
```
