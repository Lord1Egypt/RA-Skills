---
name: reddit-account-operations
description: Operating doctrine for Reddit account automation — careful, helpful, non-spam contributor pattern with role separation, post qualification, quotas, anti-spam triggers and recovery. Use this for any scheduled Reddit activity (cron, agent, recurring task) where account safety, sub-mod tolerance and long-term reputation matter more than raw output.
---

# Reddit Account Operations

This skill is the operating doctrine for every Reddit automation run on a brand, professional or personal account.

**The goal is not to comment fast. The goal is to operate Reddit like a careful, helpful human contributor: stable browser, correct context, useful action, no spam, no reputational risk.**

Drop-in for any niche (legal, medical, software, finance, creator, ecommerce). Replace the placeholders in section 0 with your own values.

---

## 0. Configure for your brand

Before running anything, fill these placeholders in your local copy or your agent's memory:

| Placeholder | Example | Your value |
|---|---|---|
| `<BRAND_NAME>` | "Acme Studio" | — |
| `<BRAND_DOMAIN>` | "acme.studio" | — |
| `<REDDIT_USERNAME>` | "u/AcmeAlex" | — |
| `<BROWSER_PROFILE>` | "reddit-live" | — |
| `<BROWSER_PORT>` | "9223" | — |
| `<NICHE_KEYWORDS>` | "retrait permis OR contester amende" | — |
| `<TARGET_SUBS>` | "r/conseiljuridique, r/AskFrance" | — |
| `<WORKSPACE_DIR>` | "~/.openclaw/workspace/reddit-<brand>" | — |

All shell snippets below assume an [OpenClaw](https://openclaw.ai) browser CLI bound by CDP, but the doctrine works with any browser-automation stack (Playwright, Puppeteer, Chrome MCP). Swap the CLI calls for your own.

### Quick config (copy-paste YAML)

If your agent reads config from YAML, drop this in `<WORKSPACE_DIR>/config.yaml`:

```yaml
brand:
  name: <BRAND_NAME>
  domain: <BRAND_DOMAIN>

reddit:
  username: <REDDIT_USERNAME>        # e.g. "u/AcmeAlex"
  browser_profile: <BROWSER_PROFILE> # e.g. "reddit-live"
  browser_port: <BROWSER_PORT>       # e.g. 9223

discovery:
  niche_keywords: <NICHE_KEYWORDS>   # e.g. "retrait permis OR contester amende"
  target_subs:
    - r/<sub-1>
    - r/<sub-2>

workspace:
  dir: <WORKSPACE_DIR>               # e.g. "~/.openclaw/workspace/reddit-acme"

alerts:
  channel: telegram | slack | discord
  webhook: <YOUR_WEBHOOK_URL>
```

### Compatibility

The skill is markdown — it works wherever an agent reads `SKILL.md`:

| Stack | Skill install path |
|---|---|
| [Claude Code](https://claude.ai/code) | `~/.claude/skills/reddit-account-operations/` |
| [OpenClaw](https://openclaw.ai) | `~/.openclaw/skills/reddit-account-operations/` |
| ClawHub-published | one-click install via [clawhub.ai](https://clawhub.ai/alexbloch-ia/reddit-account-operations) |
| Cursor / Copilot CLI | drop `SKILL.md` into your project's `.cursorrules` or `AGENTS.md` |
| Any LLM agent reading markdown rules | concatenate `SKILL.md` into your system prompt |

---

## 1. Browser architecture

### Physical profile

A single browser profile is used per account:

- `<BROWSER_PROFILE>` (CDP direct, attached to `http://127.0.0.1:<BROWSER_PORT>`)

User data dir: `~/.openclaw-browser-profiles/<BROWSER_PROFILE>`.

Use it through the OpenClaw browser CLI:

```bash
openclaw browser --browser-profile <BROWSER_PROFILE> status
openclaw browser --browser-profile <BROWSER_PROFILE> tabs
openclaw browser --browser-profile <BROWSER_PROFILE> navigate https://www.reddit.com/
openclaw browser --browser-profile <BROWSER_PROFILE> snapshot --limit 160
openclaw browser --browser-profile <BROWSER_PROFILE> click <ref>
openclaw browser --browser-profile <BROWSER_PROFILE> type <ref> "text"
openclaw browser --browser-profile <BROWSER_PROFILE> press Enter
openclaw browser --browser-profile <BROWSER_PROFILE> evaluate --fn "<async function>"
```

`evaluate --fn` is the primary API tool: it runs JS in the active tab and returns the function's value as JSON. Use it for `/api/me.json`, `/api/comment`, `/api/submit`, `/api/selectflair`, `/r/<sub>/rising.json`, `/search.json`.

### Roles (mental separation, single physical profile)

#### Role: `red-post`

Account cockpit. Use for direct account action.

Use for:
- original informative posts (text/self)
- replies on threads
- inbox/notifications check
- profile checks
- karma snapshots
- flair application

Default page: `https://www.reddit.com/user/<REDDIT_USERNAME without u/>`

Mental model: act as the account. Protect it. Do not clutter it.

#### Role: `red-engage`

Search and discovery radar. Use to find what deserves action.

Use for:
- keyword searches across target subs
- monitoring rising/new posts in target subreddits
- finding qualified candidates for replies
- competitor observation
- trend discovery

Default page:
`https://www.reddit.com/search/?q=<NICHE_KEYWORDS_URL_ENCODED>&type=link&t=day&sort=new`

Mental model: discover, qualify, decide. Do not post impulsively from discovery.

#### Role: `red-stealth`

Quiet maintenance bay. Use for low-noise maintenance.

Use for:
- subscribing to relevant subreddits
- saving posts for later study
- reading without interacting
- sub-state observation (flair requirements, karma requirements, mod messages)

Default page: `https://www.reddit.com/`

Mental model: maintain quietly. No noisy engagement.

### Operational law

- `red-post` = act as the account
- `red-engage` = discover what to react to
- `red-stealth` = maintain quietly
- stability matters more than speed
- after every run, navigate back to the role's default page (resting state)

Never collapse all workflows into chaotic browsing.

---

## 2. Login verification (run first on every cron)

```bash
openclaw browser --browser-profile <BROWSER_PROFILE> status
openclaw browser --browser-profile <BROWSER_PROFILE> evaluate --fn "async () => { const d = await (await fetch('/api/me.json',{credentials:'include'})).json(); return {name: d.data?.name || null, link_karma: d.data?.link_karma ?? null, comment_karma: d.data?.comment_karma ?? null, total_karma: d.data?.total_karma ?? null, modhash: !!d.data?.modhash}; }"
```

- If `status` is `stopped`: report the blockage in your recap channel and stop. Do not attempt to relaunch Chrome from inside a cron — that's a user-side action.
- If `name` is `null`: login expired. Stop and report.

---

## 3. Phase gating (karma)

Reddit's spam filters and most sub auto-mods judge new accounts harshly. Run in two phases:

- **Phase A** (karma < 100): only karma-builder + ops crons run. Any brand-mentioning cron must check karma at start and abort with `"phase A, karma=X, skip"` if karma < 100.
- **Phase B** (karma ≥ 100): all crons authorized.

Always read `<WORKSPACE_DIR>/memory/reddit-karma-log.md` at start (last line = current state) AND verify via `/api/me.json`.

A Daily Metrics Recap cron appends a snapshot every night and pings your alert channel explicitly when karma crosses 100 for the first time.

### Manual override (advanced)

You can force Phase B before karma ≥ 100 by appending a line `YYYY-MM-DD - karma=X - phase=B (manual override)` to `reddit-karma-log.md`. The override line takes priority over the threshold. Use when:

- You have an established brand and want immediate brand-aware posting despite low karma.
- You accept the risk of more automod removals on early posts (auto-freeze on 2 removals still applies — see §10).

Document the decision in `reddit-learnings.md` so future runs know why the threshold was bypassed.

---

## 4. Qualification of a post for reply

A post is repliable only if **all** of:

- Age ≤ 24h (use `created_utc`)
- Comment count < 200
- Score positive (≥ 1, accept controversial-but-genuine)
- Not flagged `removed` or `locked`
- Question is a real question in your domain (not a vent, not a meme, not a request for free work)
- No more than 1 expert-like reply already in top 10 comments (check for domain markers in flairs/body)
- Subreddit is not in freeze state (see `reddit-subs-state.md`)
- Your account has not interacted with this thread before (`reddit-reply-log.md`)
- Phase A: no domain-expert reply at all — only general helpful Phase A comments in Phase A subs.

If any check fails: skip. Document why in the recap.

---

## 5. Reply templates

### Phase A (karma builder, NO brand mention)

- 1-3 sentences, conversational, genuinely helpful
- Match the sub's tone
- Never expert-grade advice (medical, legal, financial)
- Never link to anything
- Never sign with anything that hints at a profession

Example structure:
```
[Direct answer or empathy hook]. [One concrete tip from common sense]. [Soft close optional].
```

### Phase B (brand-aware, expert)

Default mode = **pedagogical**, not promotional.

Structure:
```
[Acknowledge the situation in 1 sentence, neutral tone.]

[General rule / framework in 2-3 sentences. Cite a source only if essential. No promise.]

[Concrete next step the OP can take themselves: deadline, document to gather, official portal, command to run.]

[Optional: if the case is complex, mention that a specialist can review the OP's situation. No brand name in the comment body.]
```

Brand link policy — **ZERO outgoing links to `<BRAND_DOMAIN>` (or any owned domain) in any reply or post.** Indirect signaling only (mention a profession, never a brand name or URL). Reddit's automod and most subs flag self-promo aggressively — a single brand URL is enough to get a thread removed or trigger a sub ban.

- The username profile is your only allowed brand signal (curious readers click through; no need to push).
- No link in the comment body, not even in a trailing line.
- No link in a footer / signature block.
- No mention of the brand by name.

Forbidden in any reply:
- Any URL on `<BRAND_DOMAIN>` (and all variants: `www.`, subdomains, shorteners).
- "Contact me", "DM me", "check our site", "more info here", phone numbers, email addresses.
- Brand name in the comment body.
- Promises ("you will win", "it's certain", "guaranteed results").
- Quoting specific past client/customer cases.
- Asking the OP to DM you.

---

## 6. Informative post structure (regular cadence, e.g. Tue + Fri)

Target sub: pick one from `<TARGET_SUBS>` based on:
1. Sub karma requirement satisfied
2. Sub freeze state (skip if frozen)
3. Topic relevance (consult `reddit-ideas.md` and rotate)
4. Last 14 days have NOT seen you post in that sub (cross-check `reddit-post-log.md`)

Format:
```
Title: [Question-form or "Guide:" prefix, ≤ 100 chars]

Body (markdown):
**Context** : [1 paragraph framing the problem people face]

**The rule / framework** : [2-3 paragraphs of plain-language explanation: sources, deadlines, mechanics]

**What to do concretely**:
1. [Action 1]
2. [Action 2]
3. [Action 3]

**Takeaway** : [1 paragraph summary]

---
*[Generic role tag, e.g. "Specialist in <field>"]. I don't take case-specific questions in public comments — for a precise situation, a 1:1 review with a qualified professional works better.*
```

**ZERO brand link** in the body, in the title, or in the closing block. The closing line is an indirect role mention only — no name, no URL, no contact info. Reddit treats brand domains as self-promo; a single URL is usually enough for automod removal in legal/medical/financial subs.

Apply flair if the sub requires one. If no relevant flair exists, skip the sub.

---

## 7. Quotas (hard limits)

| Action | Limit |
|--------|-------|
| Replies / 24h (Phase B) | 3 max |
| Replies / Reply Pass run | 1-2 max |
| Informative posts / week | 2 max |
| Informative posts / day | 1 max |
| Subscribes / week | 5 max |
| Actions in same sub | min 6h apart |
| Actions globally | min 30 min apart |
| Karma builder comments / run | 1-2 max |
| Karma builder comments / day | 3 max |

Quota tracking: read `reddit-reply-log.md` and `reddit-post-log.md` at start of every run, count entries with timestamps in the last 24h / 7d, abort early if quotas already met.

---

## 8. Anti-spam triggers (words and patterns to avoid)

### Comment/post content

| Avoid | Use instead |
|-------|-------------|
| "DM me", "contact me", "check our site", "more info here" | (just don't ask, don't link) |
| `<BRAND_NAME>` in the comment body | (no brand name in body) |
| "free consultation", "free first call" | (no marketing) |
| Phone number, email | (never) |
| Emojis | (most professional/legal/medical subs are sober) |
| All caps for emphasis | (use italics/bold sparingly) |
| **Any URL on `<BRAND_DOMAIN>`** (and `www.`, subdomains, shorteners) | **never**, in any reply or post |
| Multiple external links of any kind | max 1 *external* link total per post (never in replies) |
| bit.ly / tinyurl / shorteners | banned — Reddit flags these as spam directly |

### Behavioral triggers

- Same content cross-posted < 7 days apart → spam detection
- ≥ 2 links in a single comment → auto-removed
- New account (karma < 100) posting in large subs → auto-removed
- Replying within 60s of post creation → looks bot-like, wait ≥ 5 min
- Same opening phrase across multiple replies → flagged
- > 3 actions in 30 min → temporary rate limit

---

## 9. Human-like posting flow (anti-CAPTCHA)

Reddit's `/api/submit` endpoint is gated behind **reCAPTCHA Enterprise Invisible** (sitekey `6LfirrMoAAAAAHZOipvza4kpp_VtTwLNuXVwURNQ` at the time of writing). Posting purely via API will fail silently or get blocked. The reliable path is a **human-like UI flow** through the browser CLI: dwells, slow typing, reading pauses — enough behavioral signal to score above reCAPTCHA's threshold and let the post through.

### Flow

1. **Pre-flight session check** — `/api/me.json` returns a non-null `name`.
2. **Navigate to the sub feed** — let it load (≥ 1.5 s dwell).
3. **Human scroll** — scroll the sub feed for 4-7 s to simulate reading.
4. **Navigate to `/r/<sub>/submit`** — wait for composer ready.
5. **Find the title field via UI ref** (the localized label, e.g. "Title" / "Titre"), **type slowly** (50-120 ms/key with jitter), then 0.8-1.5 s pause.
6. **Find the body field via UI ref** ("Body" / "Champ de texte du corps de la publication"), type slowly, 0.8-1.5 s pause.
7. **Review pause** — 3-7 s simulating proof-reading.
8. **Re-snapshot the UI** — the Publish button transitions `disabled → enabled` once the fields are filled, so its ref **changes**. Always re-snapshot before clicking.
9. **Click Publish once**, then wait for redirect to `/comments/<id>/` (≤ 30 s).

Total flow: **~6 minutes per post**. Slower is the point — speed is what trips the captcha.

### Exit codes (recommended convention for your script)

| Code | Meaning | Recap action |
|------|---------|--------------|
| 0 | Published, URL on stdout | `status: ok`, log post URL |
| 1 | Fatal error (UI ref missing, empty body) | `status: error`, attach screenshot |
| 2 | CAPTCHA visible mid-flow | `status: blocked`, fall back to "draft to alert channel for manual publish" |
| 3 | Session / login KO | `status: blocked`, alert user to re-login |

### Gotchas (real ones, costly to discover)

- **`LC_NUMERIC` trap on macOS**: locales like `fr_FR.UTF-8` format decimals as `0,123` instead of `0.123`. `sleep` and `awk` reject the comma → all dwells fall back to 0 → typing becomes instant → captcha fires immediately. **Force `LC_ALL=C` in any helper that does fractional-second math.** First time this bites you, you'll think your script is correct because no error is raised; the post just gets removed.
- **Re-snapshot before clicking Publish**: the Publish button's UI ref changes when it transitions from disabled to enabled. Stale refs = wrong click target.
- **Localize the field labels**: the labels `Title` / `Body` / `Publish` are localized server-side based on the account language. Either pin the account UI to English or maintain a label-map (FR/EN/etc.) and try both in `find_ref_named`.
- **Cron timeout**: bump the per-job timeout to **at least 1200 s** for posting crons — a 60-120 s default will kill a successful flow.
- **Save debug artifacts**: screenshots + page snapshots at each step in a scratch dir (e.g. `/tmp/<your-namespace>/reddit-post/`). They are gold when a post silently fails.
- **Reply Pass doesn't need this** — replies use a different code path and do not currently trigger reCAPTCHA Enterprise. Only top-level *post* creation is gated.

### When the UI changes

Reddit ships UI changes regularly. When `find_ref_named` starts returning null on labels that used to work:

1. Take a manual snapshot via your browser CLI.
2. Inspect the new label string for Title / Body / Publish.
3. Update the label map.
4. Re-test on `r/test` (safe, no consequence) before re-enabling the live posting cron.

---

## 10. Sub state management

File: `<WORKSPACE_DIR>/memory/reddit-subs-state.md`

For each sub, track:
- Last action timestamp (any reply or post)
- Last 5 actions and their outcome (live / removed / locked)
- Karma requirement observed
- Flair required (yes/no/list)
- Freeze state (yes if 2 last actions were removed → unfreeze date = removal date + 7 days)
- Mod messages received (any DM from /r/[sub] mods → flag for human review)

Update at the end of every run that touched the sub.

---

## 11. Recovery & blockers

| Issue | Action |
|-------|--------|
| `status: stopped` | Report in recap: "Chrome <BROWSER_PROFILE> stopped, user action required (relaunch Chrome on port <BROWSER_PORT>)". Stop. |
| `name: null` from /api/me.json | Report login expired. Stop. |
| HTTP 429 | Stop the run, report "rate limited", wait next scheduled run. |
| HTTP 403 on POST | Likely modhash expired — re-fetch from /api/me.json once, retry once. If still 403: report and stop. |
| Captcha / challenge page | Stop. Never attempt to solve. Report for user action. |
| `result.json.errors` contains `RATELIMIT`, `DOMAIN_BANNED`, `BAD_CAPTCHA`, `SUBREDDIT_NOEXIST`, `USER_BLOCKED` | Translate the error in the recap, do not retry, freeze the sub if it's a sub-level error. |
| Comment posted but not visible in user profile after 5 min | Possible shadowban. Flag for human verification (open profile in incognito). |
| Post removed by automod < 30 min after publish | Auto-freeze sub for 7 days. Append to `reddit-learnings.md`. |
| `evaluate` returns null with no error | Page is not on reddit.com → navigate first, retry once. |

---

## 12. Mandatory recap (alert channel + memory)

At the end of each cron:

**Alert channel (Telegram / Slack / Discord) — final run message**:
```
[Job name] — [status: ok|partial|blocked|skipped]
Public actions: [list short OR "no post/reply"]
Links: [URLs of new comments/posts]
Karma: link_karma=X comment_karma=Y total=Z
Blockers: [text OR "—"]
Next action: [1 line]
```

**Memory** — append to `<WORKSPACE_DIR>/memory/reddit-recaps.md`:
```
## YYYY-MM-DD HH:MM TZ — <job-id> — status: <status>
- Job: <description>
- Phase: A|B
- Karma: link=X comment=Y total=Z
- Actions: <list or "no action — reason">
- Subs touched: <list>
- Links: <URLs>
- Blockers: <text or "—">
- Next useful action: <1 line>
```

If no action was taken: say so clearly (`no post/reply/follow/subscribe performed, reason`).

---

## 13. Memory files inventory

Located at: `<WORKSPACE_DIR>/memory/`

| File | Purpose | Update cadence |
|------|---------|----------------|
| `reddit-recaps.md` | Per-run logs (mandatory append) | Every cron run |
| `reddit-post-log.md` | Informative posts (sub, URL, date, score) | Each informative post run |
| `reddit-reply-log.md` | Replies sent (thread URL, comment URL, sub, date, removed?) | Each reply pass |
| `reddit-karma-log.md` | Daily karma snapshot + phase | Daily Metrics Recap |
| `reddit-subs-state.md` | Per-sub freeze, flair, karma req | After any sub-touching action |
| `reddit-ideas.md` | Content backlog for informative posts | Weekly Planning + ad hoc |
| `reddit-learnings.md` | Patterns observed (what got upvoted / removed) | Weekly Planning + ad hoc |

---

## 14. Account identity guardrails

This account exists to be **useful in public** with the brand as a *background* signal.

- The username should be intentionally neutral — do not advertise the brand in the handle
- Profile bio: a short generic line, no firm name, no contact info
- Never reply to a DM that asks for expert-grade advice — direct the person to the brand contact page via a standard polite reply
- Never share private case details, names, or numbers
- Never reuse strict templates from your CRM / case management as Reddit content
- Never promise an outcome
- Never charge or solicit payment via Reddit

If anyone DMs about hiring you: reply once with a neutral line (`"the studio takes inquiries via <BRAND_DOMAIN>/contact"`) and stop.

---

## 15. Phase A → Phase B transition

When the Daily Metrics Recap detects `total_karma ≥ 100`:

1. Append to `reddit-karma-log.md`: `YYYY-MM-DD - karma=X - PHASE_B_THRESHOLD_REACHED`
2. Send a distinct alert: `🎉 Reddit karma ≥ 100 — enable Phase B (jobs.json: keyword-monitor-* + reply-pass-* + informative-post-* + subscribe-growth — flip enabled=true)`
3. Do NOT auto-flip the crons (manual user action — reduces risk of premature B-phase posting)

Once Phase B is enabled by the user:
- First week: 1 reply/day max (not the full 3) — soft ramp
- Keep karma builder running for 2 more weeks in parallel
- Once total_karma ≥ 250: disable karma builder, keep only Phase B crons

---

## 16. Stability discipline

- Read the UI before clicking
- One click → verify with a snapshot
- Do not stack clicks
- Close stale tabs at the end of every run
- Return to the role's default page when done
- Never silently fake a successful action — always verify via API or UI confirmation

**Better silence than spam. Better a blockage report than a fake success.**

---

## 17. First-run checklist

Before enabling any cron, run through this checklist:

- [ ] Section 0 placeholders filled in your local copy / agent memory.
- [ ] Reddit account created with **neutral username** (no brand in the handle).
- [ ] Profile bio is one short generic line — no firm name, no contact info.
- [ ] Browser profile launched at `http://127.0.0.1:<BROWSER_PORT>` and logged in.
- [ ] `/api/me.json` returns a non-null `name` (login verified).
- [ ] `<WORKSPACE_DIR>/memory/` directory exists with the 7 memory files (see section 13) — empty is fine, scripts append to them.
- [ ] Alert channel (Telegram / Slack / Discord) webhook tested with a "hello" message.
- [ ] Phase A confirmed: `total_karma < 100` → only karma-builder + ops crons enabled.
- [ ] At least 2 weeks of organic activity (subscribes, low-stakes comments) **before** enabling brand-mentioning crons, even if karma ≥ 100.

A bash one-liner to init the memory files:

```bash
mkdir -p "<WORKSPACE_DIR>/memory" && cd "$_" && touch reddit-recaps.md reddit-post-log.md reddit-reply-log.md reddit-karma-log.md reddit-subs-state.md reddit-ideas.md reddit-learnings.md
```

(The GitHub repo ships an `init-memory.sh` script that does the same interactively.)

---

## 18. FAQ

**Q: Do I need OpenClaw to use this skill?**
A: No. OpenClaw browser CLI is the example stack — the doctrine works with Playwright, Puppeteer, Chrome MCP, or any CDP-capable tool. Swap the CLI calls.

**Q: Can I use this skill for multiple Reddit accounts?**
A: Yes — clone the workspace dir per account. Each account gets its own `memory/` and its own browser profile. Do not cross-link accounts in any reply.

**Q: What if my niche has only one relevant sub and it's strict?**
A: Run Phase A on adjacent subs (low-stakes, high-volume) to build karma, then start Phase B on the niche sub with the longest possible runway. Some niche subs also require 90+ days of account age regardless of karma.

**Q: Is shadowban detection reliable?**
A: Partially. The "comment posted but invisible in incognito after 5 min" check catches most shadowbans, but Reddit also does **community-specific shadowbans** that don't fire that signal. Track per-sub upvote ratios over time as a backup signal.

**Q: Can I run multiple crons in parallel?**
A: Yes, but respect the global "30 min apart" rule across all crons. A lock file at `<WORKSPACE_DIR>/.lock` is the cleanest way to enforce it.

**Q: What if my account is suspended?**
A: Stop everything. Do not appeal automatically. Manual review only. Document the suspension in `reddit-learnings.md` with the exact last action before suspension.
