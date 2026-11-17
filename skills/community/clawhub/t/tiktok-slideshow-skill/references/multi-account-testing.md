# Warm-up, cadence, many accounts and the hook log

Slideshows are cheap, so the advantage comes from volume with discipline: many hooks, a log that
tracks installs, and the habit of dropping what loses.

## Warm up new accounts

Commonly recommended by operators running slideshow accounts:

- **7 to 14 days of normal use before the first post:** 30 to 60 minutes a day scrolling,
  liking and following in the account's niche, from the phone the account will post from.
- **Inbox drafts for the first weeks** (`MEDIA_UPLOAD`), so the user adds a sound and publishes
  from the app.
- **A few non-promotional slideshows** in the niche before the first app mention.

Nobody can guarantee an account won't be limited. Say so.

## Cadence

Operators who report results post **1 to 3 slideshows per account per day** once an account is
warmed up; a few a week is too slow to learn from. Start at 1 a day, go up when the account is
stable. Batch the work: one session writes 10 to 20 hooks and renders a week of slideshows, the
user confirms the batch once.

## Several accounts

WoopSocial's free plan covers 2 social accounts; more need a paid plan.

1. **Each account has a clear angle:** students, night-shift workers, a language. The angle
   decides the hooks.
2. **Each account gets its own variants.** Never the identical slideshow on several accounts: it
   looks like spam and the accounts compete with each other.
3. **Stagger posting times.**
4. **Honest personas only.** Accounts may have an angle; they don't invent people or stories.

Batch table (times in the user's timezone, converted to UTC for `scheduledFor`):

| Account | Angle | Hook | Format | When | Mode |
|---|---|---|---|---|---|
| @app_students | students | "study apps the night before finals:" | relatable | Tue 18:00 | TikTok inbox draft |
| @app_nightshift | nurses | "sleeping at 9am after a night shift:" | tension | Tue 21:00 | TikTok inbox draft |

## Attribution: know which account drives installs

Daily downloads next to several posts a day across several accounts can't tell you which hook
drove them. Set up three things before scaling:

1. **A tracked bio link per account:** an App Store campaign link (`ct=` token in App Store
   Connect), a Play Store referrer, or a landing page link with UTM tags per account.
2. **A "where did you hear about us?" question** in onboarding, with TikTok as an option.
3. **Read results per account per week**, not per post. Per-post views still rank the hooks;
   installs judge the account and its angle.

## The hook log (`hooks.md`)

One line per post, filled when it goes out and updated after 48 to 72 hours. Downloads come from
the user's App Store, Play Console, RevenueCat or analytics, per day.

```
| Date | Account | Format | Hook | Views | Shares | Saves | Downloads that day | Collected |
|---|---|---|---|---|---|---|---|---|
| [date] | @app_students | relatable | study apps the night before finals: | [n] | [n] | [n] | [n] | [date] |
```

A missing number means "not reported", not zero. Never estimate downloads from views.

## Reading the log

Compare with the same account's usual numbers, not with viral posts elsewhere. Use installs per
account per week (from the tracked bio link) for the downloads column of this matrix.

| Views | Downloads | Do |
|---|---|---|
| High | High | Scale: 2 to 3 variants of the hook, try it on a second account |
| High | Low | The hook works, the app slide or call to action doesn't: fix the reveal, caption and bio link |
| Low | High | The idea converts: keep the slideshow, test new hooks |
| Low | Low | Retire after two tries, change the format |

Small numbers are noisy. Don't call a winner from one post on a new account.

## Weekly rhythm

1. Update `hooks.md` with last week's metrics and the user's daily downloads.
2. Read the matrix; pick what scales and what retires.
3. Write 10 to 20 new hooks; render the next batch.
4. Confirm the batch once and schedule it.
