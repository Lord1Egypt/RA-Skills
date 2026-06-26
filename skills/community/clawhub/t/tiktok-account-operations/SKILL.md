---
name: tiktok-account-operations
description: Operating doctrine for TikTok account automation — careful, value-adding creator pattern with role separation, business-suite based DM/comment ops, human-like UI flow (cliclick + nested reply textbox), strict anti-shadowban quotas, and recovery patterns. Use this for any scheduled TikTok activity (cron, agent, recurring task) where account safety, FYP eligibility and long-term reach matter more than raw output.
---

# TikTok Account Operations

This skill is the operating doctrine for every TikTok automation run on a brand, professional or personal account.

**The goal is not to comment fast. The goal is to operate TikTok like a careful human contributor: stable browser, correct context, useful action, no shadowban risk, no FYP throttling.**

Drop-in for any niche (legal, medical, software, finance, creator, ecommerce). Replace the placeholders in section 0 with your own values.

---

## 0. Configure for your brand

Before running anything, fill these placeholders in your local copy or your agent's memory:

| Placeholder | Example | Your value |
|---|---|---|
| `<BRAND_NAME>` | "Acme Studio" | — |
| `<BRAND_DOMAIN>` | "acme.studio" | — |
| `<TIKTOK_HANDLE>` | "@acmestudio" | — |
| `<TIKTOK_BUSINESS_ACCOUNT>` | yes/no (Business Suite requires Business or Creator account) | — |
| `<BROWSER_PROFILE>` | "tiktok-live" | — |
| `<BROWSER_PORT>` | "18801" | — |
| `<NICHE_KEYWORDS>` | "lost license OR speeding ticket" | — |
| `<PRIMARY_CTA>` | "WhatsApp / form / app link — pick ONE" | — |
| `<WORKSPACE_DIR>` | "~/.openclaw/workspace/tiktok-<brand>" | — |

All shell snippets below assume an [OpenClaw](https://openclaw.ai) browser CLI bound by CDP, but the doctrine works with any browser-automation stack (Playwright, Puppeteer, Chrome MCP). Swap the CLI calls for your own.

### Quick config (copy-paste YAML)

If your agent reads config from YAML, drop this in `<WORKSPACE_DIR>/config.yaml`:

```yaml
brand:
  name: <BRAND_NAME>
  domain: <BRAND_DOMAIN>

tiktok:
  handle: <TIKTOK_HANDLE>            # e.g. "@acmestudio"
  business_account: true             # required for /business-suite/ UI
  browser_profile: <BROWSER_PROFILE> # e.g. "tiktok-live"
  browser_port: <BROWSER_PORT>       # e.g. 18801

discovery:
  niche_keywords: <NICHE_KEYWORDS>

cta:
  primary: <PRIMARY_CTA>             # one channel only — e.g. "wa.me/<digits>"

workspace:
  dir: <WORKSPACE_DIR>               # e.g. "~/.openclaw/workspace/tiktok-acme"

alerts:
  channel: telegram | slack | discord
  webhook: <YOUR_WEBHOOK_URL>

schedule:
  timezone: Europe/Paris             # everything else is relative to this
  windows:
    dm_check:      "0,15,30,45 9-22 * * *"     # every 15 min, 9am-10pm
    comment_check: "3,18,33,48 9-22 * * *"     # offset by 3 min so they never overlap
    browser_health: "0 * * * *"                # hourly
    daily_recap:   "21:00"
```

### Compatibility

The skill is markdown — it works wherever an agent reads `SKILL.md`:

| Stack | Skill install path |
|---|---|
| [Claude Code](https://claude.ai/code) | `~/.claude/skills/tiktok-account-operations/` |
| [OpenClaw](https://openclaw.ai) | `~/.openclaw/skills/tiktok-account-operations/` |
| ClawHub-published | one-click install via [clawhub.ai](https://clawhub.ai) |
| Cursor / Copilot CLI | drop `SKILL.md` into your project's `.cursorrules` or `AGENTS.md` |
| Any LLM agent reading markdown rules | concatenate `SKILL.md` into your system prompt |

---

## 1. Browser architecture

### Physical profile

A single browser profile per account, attached to TikTok's Business Suite:

- `<BROWSER_PROFILE>` (CDP direct, attached to `http://127.0.0.1:<BROWSER_PORT>`)

User data dir: `~/.openclaw-browser-profiles/<BROWSER_PROFILE>`.

Use it through the OpenClaw browser CLI:

```bash
openclaw browser --browser-profile <BROWSER_PROFILE> status
openclaw browser --browser-profile <BROWSER_PROFILE> tabs
openclaw browser --browser-profile <BROWSER_PROFILE> navigate https://www.tiktok.com/business-suite/messages
openclaw browser --browser-profile <BROWSER_PROFILE> snapshot --limit 160
openclaw browser --browser-profile <BROWSER_PROFILE> click <ref>
openclaw browser --browser-profile <BROWSER_PROFILE> evaluate --fn "<async function>"
```

### The Business Suite is the canonical surface

Most TikTok operational pages (Messages, Comments, Analytics, Posts) live under:

- `https://www.tiktok.com/business-suite/messages`
- `https://www.tiktok.com/business-suite/comments`
- `https://www.tiktok.com/business-suite/analytics`
- `https://www.tiktok.com/business-suite/posts`

Critical UI fact: **`/business-suite/messages` and `/business-suite/comments` render their content inside iframes**, not in the main DOM. Many `document.querySelector(...)` calls will silently miss the actual content unless you traverse the right iframe. See §9.

### Roles (mental separation, single physical profile)

#### Role: `tk-post`

Account cockpit. Use for direct account action.

Use for:
- DM replies in `/business-suite/messages`
- Comment replies in `/business-suite/comments` (nested reply only — see §9)
- Original video uploads (separate publishing flow, usually via mobile or Creator Studio)
- Profile checks
- Analytics snapshots

Default page: `https://www.tiktok.com/business-suite/messages`

Mental model: act as the account. Protect it. Do not clutter it.

#### Role: `tk-engage`

Search and discovery radar. Use to find what deserves action.

Use for:
- Keyword searches across the public feed
- Monitoring `#niche` hashtags
- Inspecting a candidate creator's recent posts before replying
- Trend / sound discovery

Default page: `https://www.tiktok.com/search?q=<NICHE_KEYWORDS_URL_ENCODED>&t=video`

Mental model: discover, qualify, decide. Do not act impulsively from discovery.

#### Role: `tk-stealth`

Quiet maintenance bay. Use for low-noise maintenance.

Use for:
- Saving / liking videos for inspiration
- Following peer creators (cap follows — see §7)
- Quiet profile observation
- Sound library curation

Default page: `https://www.tiktok.com/foryou`

Mental model: maintain quietly. No noisy engagement.

### Operational law

- `tk-post` = act as the account
- `tk-engage` = discover what to react to
- `tk-stealth` = maintain quietly
- Stability matters more than speed
- After every run, navigate back to the role's default page (resting state)

Never collapse all workflows into chaotic browsing.

---

## 2. Session check (run first on every cron)

```bash
openclaw browser --browser-profile <BROWSER_PROFILE> status
openclaw browser --browser-profile <BROWSER_PROFILE> evaluate --fn "async () => { try { const r = await fetch('https://www.tiktok.com/api/user/detail/self/', {credentials:'include'}); const d = await r.json(); return {ok: d.statusCode === 0, uniqueId: d.userInfo?.user?.uniqueId || null}; } catch(e) { return {ok:false, error:String(e)}; } }"
```

- If `status` is `stopped`: report the blockage in your alert channel and stop. Never relaunch Chrome from inside a cron — that's a user-side action.
- If `ok` is `false` or `uniqueId` is `null`: login expired. Stop and report.

For Business Suite specifically, navigate to `/business-suite/messages` after the API check — if the page redirects to the public web feed or to a login screen, the Business account session is expired even though the API succeeded.

---

## 3. Phase gating (algorithm trust)

TikTok has no karma counter, but it has a strong **trust gradient**: brand-new or recently-warned accounts get throttled on the FYP and on DM volume. Run in two phases:

- **Phase A** (account < 30 days OR last 14 days had ≥ 1 "Community Guidelines" notice): zero brand-mentioning DMs and zero outbound comment replies. The account is allowed to post videos and react to incoming DMs only.
- **Phase B** (account ≥ 30 days, no recent warning, ≥ 500 followers): all crons authorized.

Always read `<WORKSPACE_DIR>/memory/tiktok-state.md` at start (last line = current phase) AND verify via `/business-suite/posts` (looks for a "limited" banner near the post list).

A Daily Metrics Recap cron appends a snapshot every night and pings your alert channel explicitly when the account crosses Phase A → Phase B.

### Manual override (advanced)

You can force Phase B before the 30-day threshold by appending a line `YYYY-MM-DD - phase=B (manual override)` to `tiktok-state.md`. The override line takes priority over the threshold. Use when:

- You have an established brand on other platforms and an audited account history (imported followers, verified domain) and want immediate brand-aware posting.
- You accept the risk of harder shadowban triggers in the first 30 days. The auto-freeze on 2 successive comment removals (see §11) still applies.

Document the decision in `tiktok-learnings.md`.

---

## 4. Qualification of an inbound DM or comment

A DM or comment is repliable only if **all** of:

- The conversation thread has at least one message from the user (not a pure share/forward).
- The message is in a language you can answer in (otherwise: skip, do not auto-translate).
- The message is a real question or qualified intent in your domain (not a vent, not a meme, not a request for free expert-grade work).
- Phase B authorized for brand-mentioning replies (see §3).
- The same user has not been sent a templated reply in the last 7 days (`tiktok-reply-log.md`).
- Not a competitor or a troll on first read of the user's recent posts.

If any check fails: skip. Document why in the recap.

### Read the full context before answering

For DMs: read **the entire conversation** (`[data-e2e="chat-item"]`), not just the latest message. People often add critical context across 2-3 messages.

For comments: read the parent video caption AND the comment thread up to the target comment. A reply that ignores the obvious context reads as a bot.

---

## 5. Reply templates

### Phase A (warming, NO brand mention)

- 1-3 sentences, conversational, genuinely helpful.
- Match the comment / DM tone.
- Never expert-grade advice (medical, legal, financial).
- Never link to anything.
- Never sign with anything that hints at a profession.

Example structure (comment):
```
[Direct answer or empathy hook]. [One concrete tip from common sense].
```

### Phase B (brand-aware, expert)

Default mode = **pedagogical**, not promotional.

DM reply structure (≤ 6000 chars but aim for ≤ 600):
```
[Acknowledge the situation in 1 sentence, neutral tone.]

[General rule / framework in 2-3 short paragraphs. No exact quote of statute. No price.]

[Concrete next step — point to <PRIMARY_CTA>. NEVER list multiple channels.]
```

Comment reply structure (≤ 200 chars):
```
[1 line of contextual acknowledgement]. [Indirect signal — "feel free to DM us" / "form on bio" — never paste a URL].
```

### Brand link policy

**ZERO outgoing links inside DMs or comments themselves.** TikTok actively dampens reach for posts containing third-party URLs in any user-visible text. Indirect signaling only:

- Bio link in your profile is the only authorized URL surface.
- Comment / DM body: never paste a URL, never paste a brand name in a way that triggers the "may be unsafe" toast.
- Never paste an external URL in a video caption either — the FYP penalty is real.
- Maximum 1 indirect mention per reply (e.g. "we have an app for that" — no name).

### The encoding trap (critical — see §9 for the full story)

If your sending path uses `cliclick t:'...'` for comment posting, **strip all accented characters and emoji** from the rendered string before sending. The macOS keystroke path silently drops or replaces non-ASCII characters in some locales. Replace `é → e`, `à → a`, `' → '`, `…  → ...` etc. before the type call.

Forbidden in any reply:
- Any URL on `<BRAND_DOMAIN>` (and `www.`, subdomains, shorteners).
- "DM me", "click my profile", "check our site", "more info here", phone numbers, email addresses (in the reply body — bio is the only authorized URL surface).
- Brand name in the comment body (Phase A) or more than once (Phase B).
- Promises ("you will win", "guaranteed", "in 24h I'll fix it").
- Quoting specific past client / customer cases.
- Emojis (encoding trap + sober tone in regulated fields).

---

## 6. Original posting cadence

Posting cadence is **outside the scope of the live operational crons** described in §9 (those handle reactive DM + comment replies). The recommended rhythm for an account in Phase B is:

- **3-5 short videos / week** (15-45 s), one idea per video, hook in the first 1.5 s.
- **1 longer video / week** (45-90 s) explaining one concept end-to-end.
- **Avoid burst posting** (3+ videos within 6 h) — TikTok throttles the burst.
- **Respect the sound policy**: original sounds and verified-license sounds only. Copyrighted commercial tracks on a Business account = silent mute on the FYP.

Hashtag discipline:
- 3-5 hashtags per video, max.
- 1 broad (#fyp, #foryou) + 2-3 niche (#yourdomain).
- Never use banned or shadowbanned hashtags — re-check the `<WORKSPACE_DIR>/memory/tiktok-hashtag-state.md` registry monthly.

Apply a posting calendar in `<WORKSPACE_DIR>/memory/tiktok-ideas.md`. Run a Weekly Planning cron that picks the next 5-7 hooks from `tiktok-ideas.md` and confirms none of them duplicates a post in `tiktok-post-log.md` over the last 30 days.

---

## 7. Quotas (hard limits)

| Action | Limit |
|--------|-------|
| Replies (DM) per 24 h | 30 max |
| Replies (DM) per Reply Pass run | 4 max |
| Replies (comment) per 24 h | 40 max |
| Replies (comment) per Reply Pass run | 6 max |
| Outbound first-contact DMs / day | 0 (Phase A) — 5 (Phase B, only if user opted-in) |
| Follow / day | 20 max (Phase B), 5 max (Phase A) |
| Unfollow / day | 20 max |
| Actions in same video thread | min 30 min apart |
| Actions globally (any) | min 1 min apart |
| Same opening phrase across replies | never (see §8) |

Quota tracking: read `tiktok-reply-log.md` at the start of every run, count entries with timestamps in the last 24 h, abort early if quotas already met.

### Cron interleaving

To avoid two crons hammering the Business Suite at the same time:

- **DM Check** runs at `:00, :15, :30, :45`.
- **Comment Check** runs at `:03, :18, :33, :48` (offset by 3 min).

Never fuse the two into one cron — a single long-running cron is more likely to hit a TikTok soft block.

---

## 8. Anti-spam triggers (words and patterns to avoid)

### Content

| Avoid | Use instead |
|-------|-------------|
| "DM me", "check my profile", "link in bio" | (bio link does the work — don't point at it) |
| `<BRAND_NAME>` repeated > 1 time in same reply | (mention once, max) |
| "free consultation", "first call free" | (no marketing language) |
| Phone number, email, URL | (never in body) |
| Emojis | (regulated / sober fields — drop them. Also: encoding trap on macOS — see §9) |
| All caps for emphasis | (use italics sparingly, prefer plain text) |
| Bit.ly / tinyurl / shorteners | (TikTok flags shorteners aggressively) |

### Behavioral

- Replying within 30 s of comment creation → bot-like, wait ≥ 2 min.
- Same opening phrase across multiple replies → flagged (vary openings).
- > 6 actions in 10 min → temporary rate limit.
- Posting > 3 videos within 6 h → burst penalty on the FYP.
- Following > 25 users / day → 24 h action block.
- Mass-mentioning users (`@user @user @user` in a single reply) → spam classifier triggers.
- Mass-DMing identical messages → near-instant temporary ban.

---

## 9. Human-like UI flow (the only thing that actually works)

TikTok's Business Suite ships heavy front-end protections: iframes everywhere, two stacked textboxes after a "Reply" click, IME-aware focus management, and a non-trivial composer that ignores synthetic events. The only flow that survives is **physical-input simulation** — real mouse clicks via `cliclick` on macOS (or `xdotool` on Linux), real keystrokes, real dwells. This is the TikTok equivalent of Reddit's reCAPTCHA dodge: not a bypass, just real human signals.

### DM send flow (validated)

URL: `https://www.tiktok.com/messages?lang=<your-lang>` (redirects to `business-suite` if Business account, with an iframe wrapping the conversation pane).

1. **Pre-flight session check** (see §2). Confirm `uniqueId` is not null.
2. **Navigate to `/messages?lang=<lang>`**. Wait for the redirect to complete (≥ 1.5 s dwell).
3. **Detect iframe** via JS: `document.querySelectorAll('iframe').length > 0`. If yes, scope all subsequent queries to that iframe.
4. **List unread conversations**: query `[data-e2e="chat-list-item"]` (within iframe).
5. For each unread:
   a. Click the conversation tile.
   b. **Read all visible messages** `[data-e2e="chat-item"]` — full context before answering.
   c. Qualify the lead (see §4).
   d. Draft the reply (≤ 6000 chars).
6. **Send the reply** (the sequence below is the only one validated end-to-end):
   ```
   1. subprocess.run(["pbcopy"], input=msg.encode("utf-8"))
   2. Page.bringToFront via CDP
   3. Compute the textbox's screen coordinates (see §9.3)
   4. cliclick c:X,Y                                     ← MANDATORY physical click in textbox
   5. time.sleep(0.5)
   6. osascript -e 'tell app "System Events" to keystroke "v" using command down'
   7. time.sleep(1)                                      ← wait for the Send button to become enabled
   8. Compute screen coords of [data-e2e="message-send"]
   9. cliclick c:screenX,screenY
   10. Verify textbox is empty
   ```

The **physical click on step 4 is non-negotiable**: without it, the macOS clipboard paste lands in whichever frame currently has focus, which is rarely the message textbox.

### Comment reply flow (nested — validated)

URL: `https://www.tiktok.com/business-suite/comments`.

Structure of the page:
- Video list **in the main DOM** on the left, with a badge "N nouveaux commentaires" / "N new comments" per video.
- Selected video pane on the right, with **two iframes**: `iframe[0]` = messages (always present in background), `iframe[1]` = comments.

1. Scan the video list in the main DOM, regex `/(\d+) (nouveau|new)/` (not "Aucun" / "No").
2. For each video with new comments:
   a. Click the video tile.
   b. Wait 2 s for `iframe[1]` to load.
   c. Read `[data-e2e="comment-level-1"]` + usernames `[data-e2e="comment-username-1"]`.
   d. Qualify the comment (see §4).
   e. **Click `[data-e2e="comment-reply-1"]`** of the target comment via JS scoped to `iframe[1]`. Wait 1.5 s.
3. **The two-textbox trap**: after clicking "Reply", two textboxes exist on the page:
   - **INLINE textbox** (small `vpY`) = the nested reply textbox **← USE THIS ONE**.
   - **GENERAL textbox** (large `vpY` near the bottom) = the page-level "Add a comment" box. Posting here creates a *new* top-level comment, not a reply.
4. Always pick the textbox with the **smallest** `vpY`. Sample selector:
   ```python
   textboxes = [...]  # all contenteditable nodes with their viewport coords
   inline_tb = min(textboxes, key=lambda t: t['vpY'])

   post_btns = [b for b in all_post_btns if not b['disabled']]
   closest = min(post_btns, key=lambda b: abs(b['vpY'] - inline_tb['vpY']))
   ```
5. **Type the message** (not paste) for comments:
   ```
   1. Compute screen coords of inline_tb
   2. cliclick c:X,Y                  ← physical click in INLINE textbox
   3. time.sleep(0.5)
   4. cliclick t:'message_ascii_only' ← TYPE, do not paste
   5. time.sleep(1)
   6. Compute screen coords of the closest enabled comment-post button
   7. cliclick c:X,Y
   ```
6. **Verify the reply landed under the parent comment** — re-snapshot and look for your username in the immediate children of the parent.

### 9.3 Computing screen coordinates from viewport

The browser CLI returns viewport coordinates (`vpX`, `vpY`) inside the page. To click via `cliclick`, you need screen coordinates:

```
screenX = window.screenX + viewportX
screenY = window.screenY + (outerHeight - innerHeight) + viewportY
```

The `(outerHeight - innerHeight)` term accounts for the Chrome top bar. On a typical macOS setup with the default Chrome chrome: `chrome_bar ≈ 87`.

You can fetch these via:

```js
const m = { sX: window.screenX, sY: window.screenY, ih: window.innerHeight, oh: window.outerHeight };
```

### What does NOT work (and why)

| Method | Why it fails |
|---|---|
| `document.execCommand('insertText', false, msg)` | Visually empties the textbox after typing but the message never reaches the send pipeline (TikTok's composer reads from a controlled React state, not from the DOM). |
| `cliclick kd:cmd t:v ku:cmd` | Types the literal letter "v" instead of pasting (the cmd keydown is released before the t:v fires). |
| `cliclick kp:return` to send | TikTok's composer ignores the Enter key in DMs and comments; you must click the send button. |
| `osascript ... keystroke "v" using command down` for comments | Pastes into the **page-level** focus, which is rarely the inline reply textbox after a "Reply" click. Use `cliclick t:'...'` for comments. |
| Picking the GENERAL textbox (largest `vpY`) for a nested reply | Posts a top-level comment instead of a nested reply. |

### Exit codes (recommended convention for your script)

| Code | Meaning | Recap action |
|------|---------|--------------|
| 0 | DM / comment sent, verified | `status: ok`, log the reply |
| 1 | Fatal error (UI ref missing, iframe absent, send button never enabled) | `status: error`, attach screenshot |
| 2 | Soft block / "Tap to retry" toast | `status: blocked`, stop, alert user |
| 3 | Session / login KO | `status: blocked`, alert user to re-login |
| 4 | Comment posted but landed in wrong textbox (top-level instead of nested) | `status: partial`, mark for manual cleanup |

### Gotchas (real ones, costly to discover)

- **The `cliclick t:` accent encoding trap**: `cliclick t:'message'` on macOS drops or replaces accented characters in some locales (notably `fr_FR.UTF-8`). Strip accents and emoji from the rendered message before typing. Same family of bug as Reddit's `LC_NUMERIC` trap, different symptom: instead of dwells failing silently, characters disappear from the visible reply.
- **iframe focus drift**: clicking inside the iframe via JS does not always give focus to the inner document. Always do a physical `cliclick` after navigating, before pasting/typing.
- **Two iframes on the comments page**: `iframe[0]` is the messages background, `iframe[1]` is the comments. Always scope queries to `iframe[1]` on `/business-suite/comments`.
- **The "Send" button has multiple instances**: pick the one with the smallest absolute `vpY` distance from your textbox, and verify it is `enabled` before clicking.
- **Cron timeout**: bump per-job timeout to **at least 1200 s** for posting crons — a 120 s default will kill a successful flow.
- **Save debug artifacts**: screenshots + page snapshots at each step in a scratch dir (e.g. `/tmp/<your-namespace>/tiktok/`). They are gold when a comment silently lands in the wrong box.

### When the UI changes

TikTok ships UI changes regularly. When the `data-e2e` attributes start returning null on selectors that used to work:

1. Take a manual snapshot via your browser CLI.
2. Inspect the new attribute names.
3. Update the selector map.
4. Re-test on your own account's most recent post (safe, low traffic) before re-enabling the live cron.

---

## 10. Hashtag / sound state management

File: `<WORKSPACE_DIR>/memory/tiktok-hashtag-state.md`

For each hashtag used in `<NICHE_KEYWORDS>`:

- Last 5 videos that used it + reach (views, watch-time %).
- Shadowban check (search the hashtag in incognito — does your video appear?).
- Banned / sensitive flag (cross-check with [hashtagsforlikes](https://hashtagsforlikes.co) or similar — keep a manual override list).

File: `<WORKSPACE_DIR>/memory/tiktok-sound-state.md`

For each sound used:

- Original or licensed (Business accounts can ONLY use commercial-license sounds).
- Reach with that sound vs your baseline.
- Sound ID / link.

Update at the end of every posting run.

---

## 11. Recovery & blockers

| Issue | Action |
|-------|--------|
| `status: stopped` | Report in recap: "Chrome <BROWSER_PROFILE> stopped, user action required (relaunch Chrome on port <BROWSER_PORT>)". Stop. |
| Session API returns `ok: false` | Report login expired. Stop. |
| Business Suite redirects to `/login` | Same as login expired. Stop. |
| HTTP 429 from `/api/user/detail/self/` | Stop the run, report "rate limited", wait next scheduled run. |
| Captcha / "puzzle" challenge | Stop. Never attempt to solve. Report for user action. |
| "Tap to retry" toast after sending | Soft block. Pause the role for ≥ 1 h. Report. |
| Comment posted but lands as a top-level (not a reply) | Auto-flag for human cleanup. Pause comment cron for 30 min. |
| Comment removed by TikTok < 10 min after publish | Auto-freeze the entire comment cron for 6 h. Append cause to `tiktok-learnings.md`. |
| `evaluate` returns null with no error | Likely off-tiktok.com page → navigate first, retry once. |
| Account banner "your account is at risk of restriction" | Flip to Phase A immediately. Disable all reply crons until manual review. |

---

## 12. Mandatory recap (alert channel + memory)

At the end of each cron:

**Alert channel (Telegram / Slack / Discord) — final run message**:
```
[Job name] — [status: ok|partial|blocked|skipped]
DMs handled: [N or "—"]
Comments handled: [N or "—"]
Hot leads: [list short OR "—"]
Phase: [A|B]
Blockers: [text OR "—"]
Next action: [1 line]
```

**Memory** — append to `<WORKSPACE_DIR>/memory/tiktok-recaps.md`:
```
## YYYY-MM-DD HH:MM TZ — <job-id> — status: <status>
- Job: <description>
- Phase: A|B
- DMs sent: <N>
- Comments sent: <N>
- Hot leads: <list or "—">
- Blockers: <text or "—">
- Next useful action: <1 line>
```

If no action was taken: say so clearly (`no DM/comment sent, reason`).

---

## 13. Memory files inventory

Located at: `<WORKSPACE_DIR>/memory/`

| File | Purpose | Update cadence |
|------|---------|----------------|
| `tiktok-recaps.md` | Per-run logs (mandatory append) | Every cron run |
| `tiktok-post-log.md` | Videos published (URL, hook, date, views, watch %) | Each posting run |
| `tiktok-reply-log.md` | Replies sent (target user, type DM/comment, URL, date, removed?) | Each reply pass |
| `tiktok-state.md` | Daily phase + warning flags + follower count | Daily Metrics Recap |
| `tiktok-hashtag-state.md` | Per-hashtag reach + shadowban check | After any posting run |
| `tiktok-sound-state.md` | Per-sound reach + license info | After any posting run |
| `tiktok-ideas.md` | Content backlog for new videos | Weekly Planning + ad hoc |
| `tiktok-learnings.md` | Patterns observed (what got reach / removed) | Weekly Planning + ad hoc |
| `tiktok-alerts-sent.md` | Anti-doublon log for hot-lead alerts (one row per user) | Each alert |

---

## 14. Account identity guardrails

This account exists to be **useful in public** with the brand as a *background* signal.

- The handle can carry the brand if your brand is the operating identity (legal/medical/B2B). Personal accounts: keep it neutral.
- Profile bio: one short generic line + the single `<PRIMARY_CTA>` link. No phone, no email in the bio.
- Never reply to a DM that asks for expert-grade advice on a specific case — direct the person to `<PRIMARY_CTA>` via a standard polite reply.
- Never share private case details, names, or numbers — even if the user shares theirs first.
- Never reuse strict templates from your CRM as TikTok content (they read as marketing).
- Never promise an outcome.
- Never charge or solicit payment via TikTok DM.

If someone asks "are you a bot?": answer once with a sober, ambiguous line (`"I'm part of the team — happy to help"`) and stop. Do not confirm AI use — and never lie outright if pressed.

---

## 15. Phase A → Phase B transition

When the Daily Metrics Recap detects (account_age_days ≥ 30) AND (last_warning_days_ago > 14) AND (followers ≥ 500):

1. Append to `tiktok-state.md`: `YYYY-MM-DD - phase=A - PHASE_B_THRESHOLD_REACHED`.
2. Send a distinct alert: `🎉 TikTok account in Phase B — enable comment-reply + outbound-DM crons (jobs.json: flip enabled=true)`.
3. Do **NOT** auto-flip the crons (manual user action — reduces risk of premature B-phase posting).

Once Phase B is enabled by the user:
- First week: cap reply pass at **2 replies/run** (not the full 6) — soft ramp.
- Keep posting cadence steady (no burst).
- Once 14 days in Phase B without warning: full doctrine quotas (§7).

---

## 16. Stability discipline

- Read the UI before clicking.
- One click → verify with a snapshot.
- Do not stack clicks.
- Close stale tabs at the end of every run.
- Return to the role's default page when done.
- Never silently fake a successful action — always verify the reply landed in the right thread / textbox.

**Better silence than spam. Better a blockage report than a fake success.**

---

## 17. First-run checklist

Before enabling any cron, run through this checklist:

- [ ] Section 0 placeholders filled in your local copy / agent memory.
- [ ] TikTok account is **Business** or **Creator** (Business Suite UI requires it).
- [ ] Profile bio is one short line + a SINGLE `<PRIMARY_CTA>` link.
- [ ] Browser profile launched at `http://127.0.0.1:<BROWSER_PORT>` and logged in.
- [ ] `/api/user/detail/self/` returns `ok:true` and a non-null `uniqueId` (login verified).
- [ ] `<WORKSPACE_DIR>/memory/` directory exists with the 9 memory files (see §13) — empty is fine, scripts append.
- [ ] Alert channel (Telegram / Slack / Discord) webhook tested with a "hello" message.
- [ ] `cliclick` installed (`brew install cliclick`) and macOS Accessibility permission granted to the terminal that runs the cron.
- [ ] Phase A confirmed: account < 30 d OR < 500 followers OR recent warning → only inbound-DM cron enabled.
- [ ] At least 14 days of organic posting (one video/day, no automation) **before** enabling reply crons, even if Phase B-eligible by metrics.

A bash one-liner to init the memory files:

```bash
mkdir -p "<WORKSPACE_DIR>/memory" && cd "$_" && touch tiktok-recaps.md tiktok-post-log.md tiktok-reply-log.md tiktok-state.md tiktok-hashtag-state.md tiktok-sound-state.md tiktok-ideas.md tiktok-learnings.md tiktok-alerts-sent.md
```

---

## 18. FAQ

**Q: Do I need OpenClaw to use this skill?**
A: No. OpenClaw browser CLI is the example stack — the doctrine works with Playwright, Puppeteer, Chrome MCP, or any CDP-capable tool. The `cliclick` step in §9 is macOS-specific; on Linux replace with `xdotool`; on Windows use the `SendInput` win32 API or a wrapper like AutoHotkey.

**Q: Can I use this skill for multiple TikTok accounts?**
A: Yes — clone the workspace dir per account. Each account gets its own `memory/` and its own browser profile. Use a different `<BROWSER_PORT>` per account so they don't collide.

**Q: Does this work with the official TikTok API (Display / Content Posting)?**
A: Partially. The official API covers video upload and basic profile reads but does NOT cover comment-reply or DM-reply — exactly the surfaces this skill operates on. The UI flow in §9 is the only reliable path until TikTok ships an official DM/comment-reply API.

**Q: What about TikTok Shop / Affiliate / Live?**
A: Out of scope. This skill covers DMs, comment replies, and FYP-eligible organic posting only. Shop and Live have separate UI and separate sanction patterns.

**Q: How does this interact with the "Action blocked" toasts?**
A: Treat them as soft blocks (exit code 2 in §9). Pause the role for ≥ 1 h, alert the user, do not retry inside the same cron run. If the toast says "we'll let you know when you can do this again", flip the account to Phase A and require a manual re-evaluation.

**Q: Can I run multiple crons in parallel?**
A: Within one account, no — the cron interleave in §7 (3-minute offset) is there because the Business Suite session can only handle one operation at a time without producing inconsistent UI state. Across accounts, yes, but use different browser profiles and different `<BROWSER_PORT>`.

**Q: What if my account is banned or shadowbanned?**
A: Stop everything. Do not appeal automatically — TikTok's appeal flow is sensitive to repeated automated submissions. Manual review only. Document the exact last 20 actions in `tiktok-learnings.md` so the post-mortem can identify the trigger.
