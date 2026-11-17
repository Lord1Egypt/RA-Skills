# Analytics — read the numbers, then act

A campaign without analysis is a coin toss. This file: where the numbers are, what
"good" looks like, and — the important part — what to change when a metric is off.

## Where the numbers live

| Data | Endpoint / place |
|---|---|
| Core campaign stats (sent, delivered, opened, clicked, unsubscribed, marked spam) | `GET /campaigns/{id}` |
| Breakdown by recipient country | `GET /campaigns/{id}/countries` |
| Clicks per link | `GET /campaigns/{id}/referrals` |
| One subscriber in one campaign (did they get/open/click it) | `GET /campaigns/{id}/email/{email}` |
| One subscriber across campaigns | `GET /emails/{email}/campaigns` |
| Dashboard-only extras | statistics by recipient **domain** (Gmail vs Outlook vs ...), by device/browser, **click map** on the email body, error breakdown, CSV/PDF export |
| Real-time events | webhooks — [webhooks.md](webhooks.md) |

Remember: opens/clicks exist only if tracking was enabled on the campaign
(`stats.opens/clicks`). Opens are undercounted in general (image blocking, Apple
Mail privacy) — treat open rate as a *trend* metric, compare campaign-to-campaign,
not as an absolute truth.

## Reference ranges (rough, industry-dependent)

| Metric | Healthy ballpark | Alarm |
|---|---|---|
| Delivery rate | ≥ 98% | < 95% |
| Open rate | 20–35% (opt-in list) | < 10% |
| Click rate (of delivered) | 2–5% | < 0.5% |
| Click-to-open | 10–20% | — |
| Unsubscribe | < 0.3% per campaign | > 1% |
| Spam complaints | < 0.05–0.1% | ≥ 0.2% |
| Hard bounces | < 1–2% | > 3–5% |

## The playbook: metric off → what to change

**Low open rate**
- Subject + sender name are the levers: test variants (A/B), be specific, no
  clickbait. (Copy itself → `sendpulse-template-skill`.)
- Wrong audience: were you mailing the inactive segment? Switch to engaged segments
  ([segmentation.md](segmentation.md)).
- Send time: try best-time sending or timezone sending.
- Check the **domain breakdown**: if one provider (e.g. Gmail) is far below the
  others, that's a reputation/placement problem at that provider, not a content
  problem — tighten list hygiene, warm that audience with your most engaged users.

**Opens fine, clicks low**
- The email doesn't pay off the subject's promise, or the CTA is weak/buried. Use
  the **click map** to see where attention actually went; one clear primary CTA
  above the fold usually wins.
- Check `referrals`: if all clicks are on the unsubscribe/footer links — content
  mismatch with the audience.

**High unsubscribes**
- Frequency too high or audience too broad. Segment; cut cadence for less engaged
  users; make content match what they signed up for.
- Spike right after an import → the imported list didn't expect your emails —
  review its origin.

**Spam complaints climbing**
- Most serious signal — provokes blocks. Stop sending to weak segments, mail only
  recent openers for a while, ensure the unsubscribe link is prominent (people mark
  spam when they can't find it), re-check consent for every list source. See
  [list-building.md](list-building.md).

**High hard bounces**
- Dirty list: validate with Email Verifier, remove invalid addresses, use double
  opt-in for new signups. Bounced addresses get error statuses and are excluded
  automatically — don't re-import them.

**Delivery < ~98%**
- Look at the error breakdown in the dashboard (mailbox full vs rejected vs
  invalid). Systematic rejections at one domain → reputation with that provider.

## Habits to build into the user's process

1. **Fixed post-campaign review**: for every campaign compare open/click/unsub/spam
   against the account's own rolling averages — trends beat absolutes.
2. **One experiment per campaign** (subject style, send time, segment) — otherwise
   you can't attribute the change. A/B tests formalize this.
3. **UTM everything** (`stats.utm_campaign` + tagged links) so email traffic and
   conversions are visible in web analytics — clicks are a means, revenue/actions
   are the goal.
4. **Act on inactivity**: recipients with no opens in ~90 days go to the
   reactivation track, then get dropped. Shrinking the list this way *raises* every
   other metric and protects deliverability.
5. Export/archive campaign reports if the team needs history beyond the dashboard.
