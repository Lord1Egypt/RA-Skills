# List building & hygiene — the asset behind every metric

Every number in [analytics.md](analytics.md) is downstream of list quality. This
file is what to tell users about growing and maintaining the list.

## The one law

**Send only to people who asked for it.** Purchased, scraped, harvested, or
"partner-shared" lists:

- are full of dead addresses (→ hard bounces) and spam traps,
- generate complaints from people who never heard of you,
- get campaigns held up, books blocked, and eventually the account restricted,
- and are illegal to mail in most jurisdictions (GDPR, CAN-SPAM, CASL...).

There is no workaround, and helping to find one is not this skill's job. If a user
arrives with a bought list, the honest advice is: don't import it; build a real
list instead (below), and validate anything old before touching it.

## Growing the list properly

- **Subscription forms** — SendPulse has a built-in form builder that writes
  straight into an address book (Forms in the dashboard). Put forms on the site,
  blog, checkout.
- **Double opt-in by default** (`confirmation: "force"` on the add-subscriber call,
  or in form settings): the subscriber confirms by clicking a link. Slightly
  smaller list, dramatically better quality, provable consent. See
  [address-books.md](address-books.md).
- **Set expectations at signup** — what content, how often. Emails that match the
  promise don't get complaints.
- **Record provenance** — a `source` variable (`webinar-2026-07`, `checkout`,
  `blog-form`) on every import. When a segment misbehaves in stats, provenance
  tells you which source to fix; and if the service asks about list origin, you
  have the answer ready.
- **Lead magnets, not bribes**: content people want beats "win an iPhone" — prize
  hunters unsubscribe and complain.

## Keeping it clean (recurring, automate what you can)

1. **Validate before importing** anything old, exported, or doubtful — SendPulse
   **Email Verifier** flags invalid/risky addresses. Importing first and "seeing
   what bounces" damages sender reputation — the exact thing you can't buy back.
2. **Let statuses work**: unsubscribed/bounced/complained addresses are excluded
   automatically. Never re-import them to force delivery.
3. **Mirror opt-outs from your app** to SendPulse the moment they happen
   (book-level unsubscribe or the account blacklist — see
   [api-reference.md](api-reference.md)).
4. **Sunset the inactive**: no opens in ~90 days → reactivation track (2–3
   attempts) → remove. A smaller engaged list outperforms a big cold one on every
   metric and keeps you out of spam folders.
5. **Watch the post-import stats**: a fresh source whose first campaign shows high
   bounces/complaints is a bad source — stop using it.

## Unsubscribe is a feature, not a leak

- Every campaign email must contain a working unsubscribe link (the template skill
  puts `{{unsubscribe_url}}` in the footer; also a legal requirement).
- Make it easy to find — people who can't find unsubscribe press "spam" instead,
  which costs you far more.
- SendPulse supports unsubscribe pages and category-based preferences (opt down
  instead of opt out) — offer "less often" as an option for bigger senders.
- Re-subscription must be the subscriber's own action (confirmation), not a bulk
  status flip.

## Quick self-audit for an existing list (walk a user through it)

- [ ] Do I know where every address came from? (if no → add `source` going forward,
      treat unknown cohorts cautiously)
- [ ] Was consent explicit? (pre-ticked boxes and "they're my customers so..." are
      weak consent)
- [ ] When did each cohort last hear from me? (>6–12 months of silence → run a
      gentle reactivation before regular campaigns, expect losses)
- [ ] Bounce rate of the last campaign under ~2%? (no → verify the list)
- [ ] Are complaints under ~0.1%? (no → shrink to engaged segments and fix
      frequency/content match)
