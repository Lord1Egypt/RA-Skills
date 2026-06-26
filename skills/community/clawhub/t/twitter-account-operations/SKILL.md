---
name: twitter-account-operations
description: Operating doctrine for X/Twitter account automation — stable Chrome sessions, role separation (post / engage / stealth), human-like interaction, careful posting, reply discipline, recovery patterns. Use this for any scheduled X activity (cron, agent, recurring task) where account safety and long-term reputation matter more than raw output.
---

# X / Twitter Account Operations

This skill is the operating doctrine for every X/Twitter automation run on a brand, professional or personal account.

**The goal is not to click fast. The goal is to operate Chrome like a careful human operator: stable browser, correct context, useful action, no spam, no reputational risk.**

Drop-in for any niche (legal, medical, software, finance, creator, ecommerce). Replace the placeholders in section 0 with your own values.

---

## 0. Configure for your brand

Before running anything, fill these placeholders in your local copy or your agent's memory:

| Placeholder | Example | Your value |
|---|---|---|
| `<BRAND_NAME>` | "Acme Studio" | — |
| `<BRAND_DOMAIN>` | "acme.studio" | — |
| `<X_HANDLE>` | "@AcmeStudio" | — |
| `<BROWSER_PROFILE>` | "x-live" | — |
| `<BROWSER_PORT>` | "9222" | — |
| `<NICHE_KEYWORDS>` | "retrait permis OR contester amende" | — |
| `<WORKSPACE_DIR>` | "~/.openclaw/workspace/twitter-<brand>" | — |

All shell snippets below assume an [OpenClaw](https://openclaw.ai) browser CLI bound by CDP, but the doctrine works with any browser-automation stack (Playwright, Puppeteer, Chrome MCP). Swap the CLI calls for your own.

### Quick config (copy-paste YAML)

If your agent reads config from YAML, drop this in `<WORKSPACE_DIR>/config.yaml`:

```yaml
brand:
  name: <BRAND_NAME>
  domain: <BRAND_DOMAIN>

x:
  handle: <X_HANDLE>                 # e.g. "@AcmeStudio"
  browser_profile: <BROWSER_PROFILE> # e.g. "x-live"
  browser_port: <BROWSER_PORT>       # e.g. 9222

discovery:
  niche_keywords: <NICHE_KEYWORDS>   # e.g. "retrait permis OR contester amende"

workspace:
  dir: <WORKSPACE_DIR>               # e.g. "~/.openclaw/workspace/twitter-acme"

alerts:
  channel: telegram | slack | discord
  webhook: <YOUR_WEBHOOK_URL>

schedule:
  timezone: Europe/Paris             # everything else is relative to this
  windows:
    morning_post:   "09:00"
    noon_post:      "12:30"
    evening_post:   "18:00"
    reply_passes:   ["11:00", "15:00", "19:30"]
    metrics_recap:  "21:30"
```

### Compatibility

The skill is markdown — it works wherever an agent reads `SKILL.md`:

| Stack | Skill install path |
|---|---|
| [Claude Code](https://claude.ai/code) | `~/.claude/skills/twitter-account-operations/` |
| [OpenClaw](https://openclaw.ai) | `~/.openclaw/skills/twitter-account-operations/` |
| ClawHub-published | one-click install via [clawhub.ai](https://clawhub.ai/alexbloch-ia/twitter-account-operations) |
| Cursor / Copilot CLI | drop `SKILL.md` into your project's `.cursorrules` or `AGENTS.md` |
| Any LLM agent reading markdown rules | concatenate `SKILL.md` into your system prompt |

---

## 1. Browser architecture

### Physical profile

The active browser profile is:

- `<BROWSER_PROFILE>` (CDP direct profile attached to `http://127.0.0.1:<BROWSER_PORT>`)

Use it through the OpenClaw browser CLI when the cron has no browser tool:

```bash
openclaw browser --browser-profile <BROWSER_PROFILE> status
openclaw browser --browser-profile <BROWSER_PROFILE> tabs
openclaw browser --browser-profile <BROWSER_PROFILE> open https://x.com/notifications
openclaw browser --browser-profile <BROWSER_PROFILE> snapshot --limit 160
openclaw browser --browser-profile <BROWSER_PROFILE> click <ref>
openclaw browser --browser-profile <BROWSER_PROFILE> type <ref> "text"
openclaw browser --browser-profile <BROWSER_PROFILE> press Enter
```

The profiles `tw-post`, `tw-engage`, and `tw-stealth` below are **operating roles**, not necessarily separate physical profiles. With one physical profile, keep the same separation by workflow, tab discipline, and resting page.

### Role: `tw-post`

Main account cockpit. Use for direct account action.

Use for:
- original posts
- threads
- replies sent from the account
- notifications
- DMs if enabled
- profile checks
- metrics visible on profile or analytics
- result posts

Default page: `https://x.com/notifications`

Mental model: act as the account. Protect it. Do not clutter it.

### Role: `tw-engage`

Search and discovery radar. Use to find what deserves action.

Use for:
- keyword searches
- live searches
- monitoring public conversations
- finding potential replies
- competitor observation
- news or trend discovery

Default page:
`https://x.com/search?q=<NICHE_KEYWORDS_URL_ENCODED>&f=live`

Mental model: discover, qualify, decide. Do not post impulsively from discovery.

### Role: `tw-stealth`

Quiet maintenance bay. Use for low-noise maintenance.

Use for:
- following cleanup
- list or account curation
- quiet profile review
- non-public maintenance

Default page: `https://x.com/home`

Mental model: maintain quietly. No noisy engagement.

### Operational law

- `tw-post` = act as the account
- `tw-engage` = discover what to react to
- `tw-stealth` = maintain quietly
- stability matters more than speed

Never collapse all workflows into chaotic browsing.

---

## 2. Human-like browser behavior

### Open the right page first

Do not begin from a random existing tab.

Examples:
- notifications check → `https://x.com/notifications`
- keyword monitor → live search URL
- reply pass → search or candidate conversation first, then account action
- original post → clean composer flow
- metrics recap → profile or analytics
- result publish → site result page first, then clean X composer

### Let the page load

After opening a page:
- wait for visible content
- confirm the session is logged in
- confirm the UI is interactive
- only then act

Never click or type into half-loaded pages.

### Read before acting

First real action is observation.

Before any public action:
- read the page
- understand the thread or notification
- check whether the brand can add real value
- check reputational risk

### Click carefully

Click once. Then verify.

After each click, confirm:
- the expected panel opened
- the expected thread loaded
- the composer is active if needed
- no wrong account or wrong tab is active

No stacked clicks. No impatient double-clicking.

### Type carefully

Before submitting:
- focus the field
- paste or type once
- verify the full text appeared
- verify spacing, links, and media
- verify the tone is brand-safe

### Keep one task per tab

Each tab needs one purpose.

When done:
- close extra tabs
- close stale composers
- return to a resting page

Safe resting page: `https://x.com/notifications`

### Protect the account

Never publish just because a cron fired.

If the slot is weak:
- use a stronger fallback
- draft locally
- or do nothing

Quality protects the brand.

---

## 3. Cron-by-cron guide

### Weekly Planning

Role: no browser required first. Use `tw-engage` only if checking live topics.

Goal: plan a credible week of content.

Interaction style:
1. Read local memory, post log, reply log, ideas, learnings.
2. Use your site pages as source priority.
3. If browsing X, use search/discovery discipline.
4. Produce a plan, not spam.

Avoid:
- inventing performance data
- planning too many posts
- weak angles

### Notifications Check

Role: `tw-post`

First page: `https://x.com/notifications`

Goal: detect mentions, questions, useful replies, high-signal followers.

Interaction style:
1. Open notifications.
2. Wait until feed is usable.
3. Read before acting.
4. Reply only if useful, safe, and on-topic.
5. Like only when appropriate.
6. Inspect profiles before follow-back.

Avoid:
- replying to everything
- generic filler
- expert-grade advice on a precise personal case
- escalating polemics

### Keyword Monitor (morning / midday / evening)

Role: `tw-engage`

First page: live search URL with brand keywords.

Goal: identify qualified public conversations.

Interaction style:
1. Open live search.
2. Scan newest relevant posts.
3. Open promising items only.
4. Evaluate freshness, source, relevance, and fit.
5. Capture candidates.
6. Do not force action if nothing is strong.

Avoid:
- treating stale content as urgent
- replying to trolls
- posting from raw impulse
- using `tw-post` for casual discovery unless only one physical profile exists

### Reply Pass (midday / afternoon / evening)

Role: discovery in `tw-engage`, public action in `tw-post`.

First page: candidate conversation or live search.

Goal: send at most 2 useful replies per run.

Interaction style:
1. Review candidate conversations.
2. Read full visible context.
3. Draft concise, useful, prudent reply.
4. Check: no promise, no exact advice, no aggressive CTA.
5. Publish only if value is clear.
6. Log the reply.

Avoid:
- generic replies
- repeating the same CTA
- giving a private consultation in public
- engaging hostile threads

### Original Post — Morning

Role: `tw-post`

First page: clean composer flow.

Goal: publish one practical, answer-first post.

Interaction style:
1. Read post log and ideas first.
2. Choose a fresh topic.
3. Draft locally before composer.
4. Open composer only when copy is ready.
5. Paste once.
6. Verify final text.
7. Publish.
8. Confirm the post went live.
9. Update post log.

Avoid:
- duplicate topics
- weak filler
- posting without final verification

### Original Post — Noon

Role: `tw-post`

Goal: publish a sober news / myth-vs-reality / threshold / deadline post.

Interaction style:
- same as morning
- verify any factual claim before posting
- if the source is weak, do not publish

Avoid:
- sensationalism
- uncertain claims
- clickbait

### Original Post — Evening

Role: `tw-post`

Goal: publish a practical case study, common mistake, or field-specific tip.

Interaction style:
- draft locally
- anonymize everything
- avoid identifiable client/customer facts
- publish only if useful

Avoid:
- exposing client/case details
- implying guaranteed results
- emotional pressure tactics

### Thread Generator (Tue / Fri)

Role: `tw-post`

First page: clean composer/thread flow.

Goal: publish one pedagogical thread from existing site content.

Interaction style:
1. Select a source page or article.
2. Draft full thread locally.
3. One idea per tweet.
4. Verify prudence and readability.
5. Open composer.
6. Build thread carefully.
7. Check order before publishing.
8. Publish once.
9. Confirm live thread.
10. Update post log.

Avoid:
- building directly in browser without local fallback
- losing thread text
- publishing if composer is unstable

### Result / Win Publish

Role: `tw-post`

Goal: publish a short, sober, anonymized post if a new result page exists on `<BRAND_DOMAIN>`.

Interaction style:
1. Check the site first.
2. Confirm the result is public.
3. Draft a cautious post.
4. Do not add private details.
5. Publish only if the result is new and appropriate.

Avoid:
- duplicating old results
- overclaiming
- promising the same outcome to others

### Daily Metrics Recap

Role: `tw-post` if metrics require profile or analytics.

First page: profile, then analytics only if usable.

Goal: capture real daily observations and recommendations.

Interaction style:
1. Review post log and reply log.
2. Open profile if needed.
3. Record visible metrics only.
4. If analytics is broken, say so.
5. Do not invent numbers.

Avoid:
- fake metrics
- strategy claims unsupported by visible data

---

## 4. Recovery and failure handling

### Browser down

1. Restart only the affected profile.
2. Reopen its default page.
3. Confirm logged-in state.
4. Confirm UI interactivity.
5. Resume only after checks pass.

### Browser frozen

1. Reload expected page once.
2. If still broken, restart browser profile.
3. Reopen default page.
4. Check interactivity.
5. If still broken, report exact blocker.

### `tw-post` / account cockpit unstable

Treat as critical.

Do not post, reply, DM, like, or follow until stable.

Recovery:
1. Stop public action.
2. Close stale composer if possible.
3. Restart browser profile if needed.
4. Open notifications.
5. Confirm simple navigation works.
6. Continue only if stable.

### Too many tabs

1. List tabs.
2. Keep the necessary working tab.
3. Close duplicate or stale tabs.
4. Return to resting page.

### Page loaded but unusable

1. Verify failure is real.
2. Refresh once.
3. If still broken, record blocker.
4. Use fallback if available.
5. Never hallucinate state.

### Composer stuck

1. Stop adding inputs.
2. Inspect once.
3. Close composer cleanly if possible.
4. Retry one clean time only.
5. If still broken, save locally and abort.

### Cron cannot safely complete

1. Stop.
2. Preserve browser stability.
3. Report exact blocker.
4. Do not fake completion.

---

## 5. Anti-patterns

Never:
- mix all workflows chaotically
- guess without reading the UI
- leave cluttered tabs
- force posts when the slot is weak
- reply generically
- use noisy engagement during maintenance
- act like a script
- publish expert-grade advice on a specific personal case
- promise a result
- denigrate anyone
- post at night (off-brand windows)
- invent analytics

---

## 6. Final doctrine

Choose the correct role.
Open the correct page.
Let the UI load.
Read before acting.
Click once.
Verify the result.
Recover cleanly when broken.
Leave the browser cleaner than you found it.

`tw-post` = act as the account.
`tw-engage` = discover what to react to.
`tw-stealth` = maintain quietly.

**Stability matters more than speed.**

---

## 7. First-run checklist

Before enabling any cron, run through this checklist:

- [ ] Section 0 placeholders filled in your local copy / agent memory.
- [ ] X account profile bio is brand-aligned but not aggressively promotional.
- [ ] Browser profile launched at `http://127.0.0.1:<BROWSER_PORT>` and logged in.
- [ ] Loading `https://x.com/notifications` from your profile renders the feed (= session OK).
- [ ] `<WORKSPACE_DIR>/memory/` directory exists with the memory files used by your crons (post log, reply log, ideas, learnings, recaps).
- [ ] Alert channel (Telegram / Slack / Discord) webhook tested with a "hello" message.
- [ ] At least 1 week of manual posting before letting automation drive the account — establishes a baseline tone and avoids day-1 algorithmic flags.

A bash one-liner to init the memory files:

```bash
mkdir -p "<WORKSPACE_DIR>/memory" && cd "$_" && touch x-recaps.md x-post-log.md x-reply-log.md x-ideas.md x-learnings.md x-metrics-log.md
```

(The GitHub repo ships an `init-memory.sh` script that does the same interactively.)

---

## 8. Reply skeletons (drop-in templates)

These are *skeletons*, not finished replies — fill the brackets, then humanize.

### Skeleton A — Answer-first (most replies)

```
[Direct answer in 1 sentence, no hedging].

[1-2 sentences of reasoning or the underlying rule].

[Optional: 1 concrete next step the OP can take themselves].
```

### Skeleton B — Empathy + redirect (sensitive topic)

```
That's a tough spot.

[1 sentence that validates without overclaiming "I know what you're going through"].

The general framework here is [...]. A specialist in [...] can review your specific situation.
```

### Skeleton C — Correction (politely)

```
Small precision: [the corrected fact, sourced if possible].

[Why it matters in 1 sentence].

(Not blaming OP — common confusion).
```

### What to never paste verbatim

- Anything with `[bracket]` placeholders still in it (final read-through is mandatory).
- The exact same skeleton more than twice in a 7-day window — vary the structure.

---

## 9. FAQ

**Q: Do I need OpenClaw to use this skill?**
A: No. OpenClaw browser CLI is the example stack — the doctrine works with Playwright, Puppeteer, Chrome MCP, or any CDP-capable tool. Swap the CLI calls.

**Q: Can I use this skill for multiple X accounts?**
A: Yes — clone the workspace dir per account. Each account gets its own `memory/` and its own browser profile. Use a different `<BROWSER_PORT>` per account so they don't collide.

**Q: How does this interact with X API rate limits?**
A: The skill is browser-driven, not API-driven — you're not consuming X API quota. You are, however, subject to X's behavioral throttling on the UI side, which is exactly why the doctrine caps actions per role and per minute.

**Q: Should I post threads or single tweets?**
A: Default to single tweets. Run a thread once per week max (Tue or Fri) when you have actual depth worth a thread. Threads-for-the-sake-of-threads get under-engaged.

**Q: What about X Premium / Blue / verification?**
A: Orthogonal. The doctrine doesn't change. Verified accounts get slightly more leeway on rate limits but also more visibility for any misstep — so the discipline matters more, not less.

**Q: What if X bans/suspends my account?**
A: Stop everything. Do not appeal automatically. Manual review only. Document the suspension in `x-learnings.md` with the exact last 5 actions before suspension.
