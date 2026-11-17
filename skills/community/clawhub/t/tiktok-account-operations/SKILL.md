---
name: tiktok-account-operations
description: Run a TikTok Business account from cron — inbound DM/comment replies, quotas, phase gates, stop-on-block. Use when scheduling TikTok replies. Trigger on "tiktok dm", "tiktok reply".
metadata: {"clawdbot":{"emoji":"🎵","requires":{"bins":["cliclick","openclaw"]},"homepage":"https://clawhub.ai/skills/tiktok-account-operations"}}
---

# TikTok Account Operations

**The goal is not to reply fast. The goal is to operate one account you own with the care of a real contributor — under TikTok's Terms of Service and Community Guidelines, inside its published limits, and stopped the moment a platform control fires.**

## Access this skill requires — read before anything else

This skill drives a **logged-in browser and your operating system's input layer**. That is a large amount of power: grant it deliberately, per item, and revoke it when the account is not being operated. Beyond `cliclick`, the snippets assume the OpenClaw browser CLI over CDP plus the macOS built-ins `pbcopy` and `osascript`.

| Access | Why it is needed | If you decline |
|---|---|---|
| Logged-in TikTok browser profile (CDP on `127.0.0.1:<BROWSER_PORT>`) | Business Suite has no DM/comment-reply API; the UI is the only surface | Skill is unusable — no fallback |
| macOS **Accessibility** permission on the cron's terminal (`cliclick`) | TikTok's composer reads React controlled state and ignores synthetic events; only real clicks/keystrokes reach it | Skill is unusable. **This permission lets that terminal click and type anywhere on your machine, not just in TikTok.** Use a dedicated low-privilege user session |
| Clipboard (`pbcopy` + ⌘V) | Only reliable path for multi-line DM bodies | Use the typing path (§ Sending), ASCII only |
| Screenshots / DOM snapshots to a scratch dir | Post-mortem when a reply lands in the wrong box | Skip — you lose debuggability, nothing else |
| Alert webhook (Telegram/Slack/Discord) | Run recaps and blocker alerts | **Leave it unset — this is the default.** Recaps then stay local |

**Network egress: off by default.** The only outbound call this skill makes beyond tiktok.com is the alert webhook, and only if you set `alerts.webhook`. Recaps sent there contain the account handle, counts, and lead usernames — do not point it at a channel wider than your operators.

**Data persisted locally**, nowhere else — `<WORKSPACE_DIR>/memory/`, 9 files. Anything holding a third-party identifier is bounded; nothing here accumulates forever, and **you never store personal details a user sent you**.

| File | Holds | Retention |
|---|---|---|
| `tiktok-recaps.md` · `tiktok-reply-log.md` | Run recaps · username + type + timestamp **only — never DM bodies** | **Prune at 90 days** |
| `tiktok-alerts-sent.md` | A **hash of the username**, not the handle — dedupes lead alerts without keeping who | **Prune at 90 days** |
| `tiktok-post-log.md` · `tiktok-state.md` · `tiktok-hashtag-state.md` · `tiktok-sound-state.md` · `tiktok-ideas.md` · `tiktok-learnings.md` | Your own posts, phase, warnings, follower count, per-hashtag/sound counters, content ideas, causes of removals | Counters and your own content only — no third-party identifiers |

## When to use

| You say | The skill does |
|---|---|
| "check TikTok DMs" | Session check → inbound reply pass, ≤4 per run (§ Sending) |
| "reply to new comments" | Comment pass on `/business-suite/comments`, ≤6 per run |
| "my reply didn't post" | § Troubleshooting — two-textbox trap first |
| "TikTok blocked my account" / captcha appeared | **Stop. Hand to a human.** No retry, no workaround (§ Stop conditions) |
| "am I shadowbanned" | Hashtag state check + Phase A flip |
| "DM this list of people" | **Out of scope.** This skill replies; it does not prospect |

## Configure

| Placeholder | Example |
|---|---|
| `<BRAND_NAME>` / `<TIKTOK_HANDLE>` | "Acme Studio" / "@acmestudio" |
| `<BROWSER_PROFILE>` / `<BROWSER_PORT>` | "tiktok-live" / "18801" |
| `<PRIMARY_CTA>` | one channel only — bio link |
| `<NICHE_KEYWORDS>` | "lost license OR speeding ticket" |
| `<WORKSPACE_DIR>` | "~/.openclaw/workspace/tiktok-acme" |

```yaml
# <WORKSPACE_DIR>/config.yaml
tiktok:    { handle: <TIKTOK_HANDLE>, business_account: true, browser_profile: <BROWSER_PROFILE>, browser_port: <BROWSER_PORT> }
cta:       { primary: <PRIMARY_CTA> }
discovery: { niche_keywords: <NICHE_KEYWORDS> }
alerts:    { webhook: null }             # null = no network egress. Opt in explicitly.
schedule:  { timezone: Europe/Paris,
             dm_check:       "0,15,30,45 9-22 * * *",  # every 15 min
             comment_check:  "3,18,33,48 9-22 * * *",  # +3 min — the two must never overlap
             browser_health: "0 * * * *", daily_recap: "0 21 * * *" }  # recap carries the phase gate — do not drop it
```

Any CDP stack (Playwright, Puppeteer, Chrome MCP) works — swap the calls. Init the memory files:

```bash
mkdir -p "<WORKSPACE_DIR>/memory" && cd "$_" && for f in recaps post-log reply-log state hashtag-state sound-state ideas learnings alerts-sent; do [ -f "tiktok-$f.md" ] || touch "tiktok-$f.md"; done
# Output: (silent, idempotent — existing files are never truncated)
```

## Roles — one profile, three intents

| Role | Intent | Default page | Writes to TikTok? |
|---|---|---|---|
| `tk-post` | Act as the account: reply to inbound DMs and comments | `/business-suite/messages` | **Yes** |
| `tk-engage` | Discover and qualify what deserves a reply | `/search?q=<NICHE_KEYWORDS>&t=video` | No |
| `tk-observe` | **Read-only.** Look at the FYP, peer profiles, sounds. Nothing is sent, nothing is written, no account state changes | `/foryou` | No |

`tk-observe` only reads — that is its definition, not a precaution. A workflow under it that wants to send, follow, or like is in the wrong role; move it to `tk-post` and spend its quota. After every run, return to the role's default page.

## Session check — first call of every cron

```bash
openclaw browser --browser-profile <BROWSER_PROFILE> status
# Output: {"state":"running","port":18801}
openclaw browser --browser-profile <BROWSER_PROFILE> evaluate --fn "async () => { const r = await fetch('https://www.tiktok.com/api/user/detail/self/', {credentials:'include'}); const d = await r.json(); return {ok: d.statusCode === 0, uniqueId: d.userInfo?.user?.uniqueId || null}; }"
# Output: {"ok":true,"uniqueId":"acmestudio"}
```

`state: stopped`, `ok:false`, or `uniqueId:null` → report the blocker and exit. Never relaunch Chrome from inside a cron; that is a user-side action. Then navigate to `/business-suite/messages`: a redirect to the public feed or `/login` means the Business session is expired even when the API call succeeded.

## Phase gate

| Phase | Condition | Authorized |
|---|---|---|
| **A** | Account < 30 days **OR** a Community Guidelines notice in the last 14 days **OR** < 500 followers | Post videos; reply to **inbound** DMs only, no brand mention. Nothing else |
| **B** | ≥ 30 days, no notice for 14 days, ≥ 500 followers | Full quotas below |

The gate has **no manual override** — the 30 days are how long TikTok takes to trust the account, and skipping them is the most reliable way to get it restricted. Read the phase from the last line of `tiktok-state.md`, confirm against `/business-suite/posts` (a "limited" banner near the post list = Phase A, immediately). The `daily_recap` cron detects A → B and **alerts and stops**: flipping the crons on is a human action. First week in B: cap at 2 replies/run.

## Quotas — hard limits

| Action | Limit |
|---|---|
| DM replies / 24 h · / run | 30 · 4 |
| Comment replies / 24 h · / run | 40 · 6 |
| **Outbound first-contact DMs** | **0.** This skill replies to people who wrote first — it never opens a thread. Unsolicited DM campaigns are out of scope and against TikTok's spam policy |
| Follow / day | 20 (Phase B) · 5 (Phase A) — TikTok blocks the action for 24 h past ~25/day |
| Unfollow / day | 20 |
| Two actions in the same video thread | ≥ 30 min apart |
| Any two actions | ≥ 1 min apart — bursts past ~6 actions/10 min hit a rate limit |

Read `tiktok-reply-log.md` at the start of every run, count the last 24 h, and **abort early** when a quota is already met. The two platform thresholds above are quoted so the ceiling is verifiable, not so you can walk up to it: these quotas sit deliberately below them and the account never approaches them.

## Qualification — every check must hold, or skip and say why in the recap

| Check | Fails when | Action |
|---|---|---|
| Real message | It is a share, forward, or a language you cannot answer natively | Skip |
| Genuine intent in your domain | A vent, a meme, a request for free expert work | Skip |
| Not a repeat | A templated reply went to the same user < 7 days ago (`tiktok-reply-log.md`) | Skip |
| Phase | Reply mentions the brand while in Phase A | Reply without the mention, or skip |
| **Full context read first** | The whole DM thread (`[data-e2e="chat-item"]`), or caption + comment thread, was not read | Read it, or skip — a reply that ignores obvious context is not a useful reply |

## Reply content

**Phase A**: 1–3 sentences, conversational, no brand, no link, no profession hint, never expert-grade advice (medical, legal, financial). **Phase B** — pedagogical, not promotional. DM ≤ 600 chars, comment ≤ 200:

```
[Acknowledge the situation in one neutral sentence.]
[General framework, 2-3 short paragraphs. No statute quote. No price.]
[One next step — <PRIMARY_CTA> only. Never list two channels.]
```

Filled instance (comment): `Six months is the usual window for that kind of request, not two weeks — the delay you're seeing is normal. Happy to point you in the right direction if you want to reach out.`

**Zero outgoing links in DM or comment bodies** — the bio link is the only authorized URL surface (TikTok dampens reach on third-party URLs in user-visible text, captions included), and max one indirect brand mention per reply. Also forbidden: shorteners, phone numbers, emails, "DM me" / "link in bio", guaranteed outcomes, past client cases, payment solicitation, emojis (encoding trap — see § Troubleshooting), identical text across users (spam under TikTok's rules, and the fastest route to a temporary ban).

**If asked "are you a bot?" — answer honestly and stop.** `"Yes, replies on this account are assisted by automation, and a human on the <BRAND_NAME> team reads everything. What can I help with?"` Then flag the thread for a human. Never claim to be a person, never give an evasive answer. Someone who asks is entitled to a straight answer, and misleading them protects nothing.

## Posting cadence (outside the reply crons)

3–5 short videos/week (15–45 s, one idea, hook in 1.5 s) + 1 longer (45–90 s). No burst (3+ in 6 h). 3–5 hashtags: 1 broad + 2–3 niche. **Sounds: original or commercially licensed only** — a copyrighted track on a Business account is a licensing breach and gets muted on the FYP. Update state at the end of every posting run:

| File | One entry per | Fields |
|---|---|---|
| `tiktok-hashtag-state.md` | Hashtag | Last 5 videos that used it + reach (views, watch-time %) · banned/sensitive flag · manual override list |
| `tiktok-sound-state.md` | Sound | Original or licensed · sound ID / link · reach with that sound vs your baseline |

**Shadowban check** (this is how you notice a control already fired, per § Stop conditions — not how you get around one): search the hashtag in a private/incognito window. Your video does not appear → flip to Phase A and alert a human.

## Sending — the UI mechanics

TikTok's Business Suite composer reads from React controlled state and renders inside iframes. Synthetic events never reach the send pipeline, so real input is a **transport requirement, not a disguise**: it is how you reach a composer that ignores `dispatchEvent`. It does nothing to hide the automation, and must not be used to try. **What does NOT work** — each is the obvious first attempt, and each fails quietly:

| Method | Why it fails |
|---|---|
| `cliclick kd:cmd t:v ku:cmd` | Types the literal letter "v" — the cmd keydown is released before `t:v` fires. Use `osascript` for ⌘V |
| `cliclick kp:return` to send | The composer ignores the Enter key in DMs and comments. You must click the send button |
| `execCommand('insertText')` | Visually fills the textbox, never reaches the send pipeline — the send button stays disabled |

### DM send (validated)

Session check → navigate `/messages?lang=<lang>`, wait ≥ 1.5 s for the redirect → `document.querySelectorAll('iframe').length > 0`, scope every query to that iframe → list unread `[data-e2e="chat-list-item"]`, click the tile, read **all** `[data-e2e="chat-item"]`, qualify, draft. Then:

```
1. pbcopy ← message on the clipboard, UTF-8       2. Page.bringToFront (CDP)
3. screen coords of the textbox (see below)
4. cliclick c:X,Y  ← physical click. Non-negotiable: without it the paste lands
                     in whatever frame holds focus, rarely the textbox
5. sleep 0.5    6. osascript -e 'tell app "System Events" to keystroke "v" using command down'
7. sleep 1 ← the Send button enables asynchronously
8. screen coords of [data-e2e="message-send"] → cliclick c:X,Y    9. verify the textbox is empty
```

### Comment reply (nested)

Left pane = video list in the **main DOM**, badge `/(\d+) (nouveau|new)/`. Right pane = **two iframes**: `iframe[0]` messages (background), `iframe[1]` comments — always scope to `iframe[1]`. Click the video tile → wait 2 s → read `[data-e2e="comment-level-1"]` → qualify → click `[data-e2e="comment-reply-1"]` → wait 1.5 s. **Two textboxes now exist.** The inline (nested) one has the *smallest* `vpY`; the large one at the bottom posts a new top-level comment instead.

```python
inline_tb = min(textboxes, key=lambda t: t["vpY"])          # nested reply box
post_btn  = min([b for b in post_btns if not b["disabled"]],
                key=lambda b: abs(b["vpY"] - inline_tb["vpY"]))
```

Then: `cliclick c:` on `inline_tb` → sleep 0.5 → `cliclick t:'ascii_only_message'` (**type, do not paste** — the ⌘V path targets page-level focus) → sleep 1 → `cliclick c:` on `post_btn`. Re-snapshot and confirm your username appears under the parent comment.

### Viewport → screen coordinates

```js
const m = { sX: window.screenX, sY: window.screenY, ih: window.innerHeight, oh: window.outerHeight };
// screenX = sX + vpX
// screenY = sY + (oh - ih) + vpY      // (oh - ih) = Chrome top bar, ≈ 87 on default macOS
```

### Exit codes

| Code | Meaning | Recap |
|---|---|---|
| 0 | Sent and verified | `status: ok`, log the reply |
| 1 | Fatal (ref missing, iframe absent, send never enabled) | `status: error` + screenshot |
| 2 | Soft block / "Tap to retry" | `status: blocked`, stop, alert |
| 3 | Session / login KO | `status: blocked`, alert to re-login |
| 4 | Landed top-level instead of nested | `status: partial`, flag for manual cleanup |

## Stop conditions — a platform control means hands off the keyboard

**When TikTok challenges you, you stop. You do not adapt, retry, slow down, or route around it.** A control that fires is the platform telling you it does not consent to what is happening; the only correct response is a human looking at why. Anything else turns a doctrine that claims to protect the account into the thing that loses it.

| Signal | Action |
|---|---|
| Captcha / puzzle challenge | **Stop the run. Never attempt to solve it, never re-present it, never hand it to a solver.** Alert a human, who completes it manually or decides not to |
| HTTP 429 / rate limited | Stop. Wait for the next scheduled run. Do not shorten the interval, do not retry |
| "Tap to retry" toast | Soft block. Pause the role ≥ 1 h. Report |
| "Action blocked" / "we'll let you know when you can do this again" | Flip to Phase A. Disable reply crons. Manual review before re-enabling |
| Banner: "your account is at risk of restriction" | Phase A immediately. All reply crons off until a human reviews |
| Comment removed by TikTok < 10 min after publish | Auto-freeze the comment cron 6 h. Append the cause to `tiktok-learnings.md` |
| Comment landed top-level | Flag for human cleanup. Pause comment cron 30 min |
| Account banned or shadowbanned | Stop everything. **Do not auto-appeal** — automated appeals are themselves abuse. Human, manual, once |

## Troubleshooting

| Issue | Cause | Fix |
|---|---|---|
| Reply posted as a top-level comment | Two textboxes exist after clicking "Reply"; you took the general one | Take the smallest `vpY` (§ Sending), re-verify against the parent's children |
| Accents vanished or turned to garbage in a sent comment | `cliclick t:'…'` silently drops/substitutes non-ASCII in some locales (`fr_FR.UTF-8`). **No error is raised** — the script looks correct, the reply looks illiterate | Strip accents and emoji before typing: `é→e`, `'→'`, `…→...` |
| Paste landed somewhere else entirely | iframe focus drift — a JS click inside an iframe does not always focus the inner document | A physical `cliclick` after every navigation, before every paste or type |
| `evaluate` returns null, no error | The tab is off tiktok.com | Navigate first, retry once |
| Cron dies mid-send, no error | Default job timeout — a 120 s default kills a flow that was working | Posting crons need **≥ 1200 s** |
| Selectors that worked yesterday return null | TikTok shipped a UI change | Snapshot manually, read the new `data-e2e` names, update the selector map, test against your own most recent post, then re-enable the cron |

## Output format — mandatory recap, to `tiktok-recaps.md` and (only if set) the webhook

```
## YYYY-MM-DD HH:MM TZ — <job-id> — status: ok|partial|blocked|skipped
- Phase: A|B
- DMs sent: <N>   Comments sent: <N>
- Hot leads: <list or "—">
- Blockers: <text or "—">
- Next useful action: <1 line>

# ── filled instance ──
## 2026-07-16 14:15 CEST — dm-check — status: blocked
- Phase: B
- DMs sent: 1   Comments sent: 0
- Hot leads: @marie_l (asked about the 6-month window)
- Blockers: captcha on 2nd conversation — run stopped, human needed
- Next useful action: solve the challenge manually in the tiktok-live profile, then re-enable dm_check
```

No action taken → say so and why. **Never fake a successful action.** Better silence than spam; better a blocker report than a false success.

## First run

- [ ] Placeholders filled; account is Business or Creator; bio = one line + a single `<PRIMARY_CTA>` link.
- [ ] Browser profile up on `<BROWSER_PORT>`, session check returns a non-null `uniqueId`; `memory/` initialized (9 files).
- [ ] `cliclick` installed; you have read § Access and accept what Accessibility grants that terminal.
- [ ] `alerts.webhook` left null unless you want recaps leaving the machine.
- [ ] Phase A confirmed; inbound-DM cron only.
- [ ] **≥ 14 days of organic, hand-posted content before any reply cron** — even if the metrics say Phase B.

## Scope

**This skill ONLY:**
- Operates **one account you own and control**, under TikTok's Terms of Service and Community Guidelines.
- Replies to DMs and comments from people who contacted the account first.
- Enforces quotas that sit deliberately below the platform's own limits.
- Stops and alerts a human on any captcha, block, warning, or ban.
- Persists local logs (usernames, counts, timestamps) and sends nothing off-machine unless you set a webhook.
- Discloses the automation honestly to anyone who asks.

**This skill NEVER:**
- Bypasses, solves, or works around a captcha, a rate limit, a block, or any anti-abuse control — when one fires, the run ends and a human decides.
- Tunes timing, dwell, or phrasing to look organic to a detector. Real input is used because the composer requires it, and for no other reason.
- Sends unsolicited or first-contact DMs, bulk-identical messages, or engagement it did not earn.
- Claims to be human, denies automation, or answers evasively when asked.
- Operates an account you do not own, buys or borrows engagement, or automates appeals.
- Runs unattended past a stop condition, or fakes a success it cannot verify.
