# Segmentation — send to the right people, not to everyone

Blasting the whole base is the #1 beginner mistake: it inflates unsubscribes and
spam complaints and buries deliverability. A segment answers "who exactly should get
this email?".

## Built-in presets (available out of the box)

| Preset | Who | Typical use |
|---|---|---|
| **New subscribers** | Added within ~the last month | Welcome/onboarding content |
| **Active** | Opened your emails recently (last ~3 months) | Your best audience — promos, launches |
| **Inactive** | Haven't opened recent campaigns / no opens for months | Reactivation campaigns ONLY — never regular promos |

These three cover most beginner needs. Start here before building custom conditions.

## Custom segments — what you can filter on

Conditions combine with **AND/OR** across three groups:

1. **System fields**
   - `email` / `email_domain` / `email_local` (string): equals, not-equals,
     contains, starts-with, ends-with, not-contains. Example: `email_domain equals
     gmail.com` for a Gmail-only test.
   - `email_added` (date): greater/less/equal/between. Example: subscribed in the
     last 14 days.
2. **Your variables** — string comparisons for `string` vars; ranges
   (greater/less/between) for `number` and `date` vars. This is why typing your
   variables matters: `last_order_date` as `date` lets you build "no purchase in 90
   days".
3. **Engagement stats** — opened since a date (`opens_by_date`), NOT opened since a
   date (`no_opens_by_date`), was sent to since a date (`sent_by_date`). This powers
   activity-based segments.

Note: you cannot segment on subscriber *status* — unsendable statuses are excluded
automatically anyway.

## Using segments in campaigns

- Dashboard: build/save the segment on the address book, pick it when creating the
  campaign. Saved segments have IDs → pass `segment_id` when creating a campaign via
  API (`POST /campaigns`).
- A segmented campaign targets **exactly one address book**.
- The segment is evaluated at send time — counts can differ from what you saw when
  saving it. Timezone-aware evaluation is used for scheduled sends.
- **Dynamic lists** (`"use_dynamic_list": true`, paid plans): the campaign also goes
  to contacts who *enter* the segment/book after creation — useful for "everyone who
  signs up this week gets the promo".

## Segment recipes (copy-paste mental models)

| Goal | Segment |
|---|---|
| Welcome chain by hand | `email_added` within last 7 days |
| Promo to engaged users | opens within last 90 days (preset "Active") |
| Reactivation | no opens in 90+ days AND was sent to in that period |
| Win-back buyers | variable `last_order_date` < today−90d (needs a `date` variable) |
| Local event | variable `city equals Berlin` |
| Deliverability probe | `email_domain equals gmail.com` (watch domain stats after) |
| VIP early access | tag `VIP` (tags are Pro+; or a `number` variable `ltv greaterthan X`) |

## Strategy rules to give users

- **Inactive ≠ audience for promos.** Send inactive users only reactivation content
  ("still want to hear from us?"), at low frequency; drop those who don't respond.
  Mailing the inactive segment regularly is how complaint rates blow up.
- **Frequency-split**: your most active openers can happily receive more; everyone
  else less. Two segments, two cadences.
- Feed segmentation with data at import time (source, signup date, purchase data as
  typed variables) — you can't segment on data you never stored. See
  [address-books.md](address-books.md).
- After sending to a segment, compare its stats against your averages
  ([analytics.md](analytics.md)) — segments are hypotheses, stats are the answer.
