---
name: reddit-account-operations
description: Run a Reddit account within sub rules, not into automod or shadowban — karma phases, quotas, removal recovery. Use when posting from a cron or agent. Trigger on "post to reddit", "reddit bot", "automod removed my post", "reddit shadowban", "karma requirement".
metadata: {"clawdbot":{"emoji":"🛡️","homepage":"https://openclaw.ai","repository":"https://github.com/AlexBloch-IA/reddit-account-operations"}}
---

# Reddit Account Operations

**The goal is not to comment fast. The goal is to operate Reddit like a careful, helpful human contributor: stable browser, correct context, useful action, no spam, no reputational risk.**

Reddit's Content Policy and each subreddit's rules bind this skill. Where they conflict with a quota below, they win.

## Access, data and network — read before running

| What | Detail |
|---|---|
| Browser | A logged-in Chrome profile you control, via CDP on `127.0.0.1:<BROWSER_PORT>`. The agent acts as your real account. |
| Credentials | None stored by the skill. Session cookies live in the browser profile; `modhash` is read from `/api/me.json` per run. |
| Public writes | Posts and replies are public and attributed to `<REDDIT_USERNAME>`. Irreversible in practice. |
| Persisted locally | `<WORKSPACE_DIR>/memory/` — run recaps, post/reply URLs, karma counts, per-sub state, ideas, learnings. Plain markdown, never encrypted. |
| Retention | You own it. Default: prune entries older than 90 days; keep `reddit-learnings.md` if you want long memory. Delete the dir to erase all history. |
| Network egress | **None by default.** Webhooks are opt-in. If you set `alerts.webhook`, run status, post/reply URLs, karma and blocker text **leave your machine** to Telegram/Slack/Discord and are stored by that provider. Leave it empty to keep everything local. |
| Human approval | Recommended for every top-level post. Required whenever this doc says STOP. |

## When to Use

| Trigger | Action |
|---|---|
| "post to reddit" / cron fires | §Login check → §Phase gate → §Post structure |
| "reply to this thread" | §Qualification → §Reply templates → §Quotas |
| "automod removed my post" | §Recovery → freeze sub 7 days → log |
| "did I get shadowbanned" | §Recovery, shadowban row → human verification |
| CAPTCHA or challenge appears | **STOP. Hand to a human.** §Challenges |
| "is karma high enough" | §Phase gating |

## Configure for your brand

| Placeholder | Example | Your value |
|---|---|---|
| `<BRAND_NAME>` | "Acme Studio" | — |
| `<BRAND_DOMAIN>` | "acme.studio" | — |
| `<REDDIT_USERNAME>` | "u/AcmeAlex" | — |
| `<BROWSER_PROFILE>` | "reddit-live" | — |
| `<BROWSER_PORT>` | "9223" | — |
| `<NICHE_KEYWORDS>` | "contester amende OR retrait permis" | — |
| `<TARGET_SUBS>` | "r/conseiljuridique, r/AskFrance" | — |
| `<WORKSPACE_DIR>` | "~/.openclaw/workspace/reddit-acme" | — |

```yaml
# <WORKSPACE_DIR>/config.yaml
reddit:
  username: <REDDIT_USERNAME>
  browser_profile: <BROWSER_PROFILE>
  browser_port: <BROWSER_PORT>
discovery:
  niche_keywords: <NICHE_KEYWORDS>
  target_subs: [r/<sub-1>, r/<sub-2>]
workspace:
  dir: <WORKSPACE_DIR>
alerts:
  channel: telegram | slack | discord
  webhook: ""        # empty = no network egress (default)
```

```bash
# Idempotent memory init — creates only what is missing
mkdir -p "<WORKSPACE_DIR>/memory" && cd "$_" && for f in recaps post-log reply-log karma-log subs-state ideas learnings; do [ -f "reddit-$f.md" ] || : > "reddit-$f.md"; done
# Output: (silent) — 7 files in <WORKSPACE_DIR>/memory/
```

Snippets assume the OpenClaw browser CLI bound by CDP; any CDP stack works (Playwright, Puppeteer, Chrome MCP) — swap the calls.

## Roles (mental separation, one physical profile)

| Role | Purpose | Default resting page |
|---|---|---|
| `red-post` | Act as the account: posts, replies, inbox, karma, flair | `/user/<REDDIT_USERNAME without u/>` |
| `red-engage` | Discover and qualify: searches, rising/new in target subs | `/search/?q=<NICHE_KEYWORDS>&type=link&t=day&sort=new` |
| `red-observe` | Read-only maintenance: subscribe, save, read, observe sub rules | `/` |

Never collapse the three into chaotic browsing. After every run, navigate back to the role's resting page.

## Login check (first step of every run)

```bash
openclaw browser --browser-profile <BROWSER_PROFILE> status
# Output: running  (if "stopped" → report and STOP; relaunching Chrome is a user action)

openclaw browser --browser-profile <BROWSER_PROFILE> evaluate --fn "async () => { const d = await (await fetch('/api/me.json',{credentials:'include'})).json(); return {name: d.data?.name ?? null, link_karma: d.data?.link_karma ?? null, comment_karma: d.data?.comment_karma ?? null, total_karma: d.data?.total_karma ?? null, modhash: !!d.data?.modhash}; }"
# Output: {"name":"AcmeAlex","link_karma":42,"comment_karma":318,"total_karma":360,"modhash":true}
# name: null → login expired → report and STOP
```

## Phase gating (karma)

| Phase | Condition | Authorized |
|---|---|---|
| A | `total_karma < 100` | Karma-builder + ops crons only. Brand-mentioning crons abort with `"phase A, karma=X, skip"`. |
| B | `total_karma ≥ 100` | All crons. First week: 1 reply/day, not 3. Karma-builder stays on 2 more weeks. |
| B (forced) | Manual override line in `reddit-karma-log.md` | Established brands accepting more early removals. Auto-freeze on removal (§Recovery) still applies. Document why in `reddit-learnings.md`. |

Karma gates exist because a new account should contribute to a community before it promotes anything. The phases mirror that intent — they are not a way to unlock a gate faster. Karma-builder comments must be independently useful to the thread they are in; if a comment only exists to move the counter, don't post it. Turn karma-builder off at `total_karma ≥ 250` because the account has a real history by then, not because a threshold cleared. Karma is not the only gate: some subs require 90+ days of account age regardless, and some ban automation outright — if a sub forbids automation or requires a karma the account lacks, you don't go there.

Read `reddit-karma-log.md` (last line = state) **and** verify via `/api/me.json`. Crossing 100 alerts the user; **never auto-flip crons** — the user enables Phase B by hand.

## Qualification of a post for reply

Repliable only if **all** hold — any check fails → skip, and say why in the recap:

- Age ≤ 24h (`created_utc`) · comments < 200 · score ≥ 1 · not `removed`/`locked`
- Real question in your domain — not a vent, a meme, or a request for free work
- ≤ 1 expert-like reply already in the top 10 comments
- Sub not frozen (`reddit-subs-state.md`) and never touched before on this thread (`reddit-reply-log.md`)
- Phase A: no domain-expert reply at all — general helpful comments only

## Reply and post templates

**Phase A** (karma builder, no brand): 1-3 sentences, conversational, sub's tone, never expert-grade advice (medical/legal/financial), never a link, never a professional signature.

**Phase B** (brand-aware, pedagogical — not promotional):

```
[Acknowledge the situation in 1 sentence, neutral tone.]
[General rule / framework in 2-3 sentences. Cite a source only if essential. No promise.]
[Concrete next step the OP can take alone: deadline, document to gather, official portal.]
[Optional: if the case is complex, note a specialist can review it. No brand name.]
```

Informative post (regular cadence, e.g. Tue + Fri) — pick a sub whose karma requirement is met, that is not frozen, and where you have not posted in 14 days:

```
Title: [Question-form or "Guide:" prefix, ≤ 100 chars]

**Context**: [1 paragraph framing the problem people face]
**The rule / framework**: [2-3 paragraphs, plain language: sources, deadlines, mechanics]
**What to do concretely**: 1. [Action] 2. [Action] 3. [Action]
**Takeaway**: [1 paragraph]

---
*[Generic role tag, e.g. "Specialist in <field>"]. I don't take case-specific questions in public comments.*
```

Apply the sub's required flair; if no relevant flair exists, skip the sub.

**Brand link policy — ZERO outgoing links to `<BRAND_DOMAIN>` (or any owned domain) in any reply or post**, body or footer. The single exception is a DM the user initiated, where one neutral pointer is allowed — see §Identity guardrails. One brand URL is enough for automod removal or a sub ban in legal/medical/financial subs. Your username profile is the only allowed brand signal.

## Quotas (hard limits)

| Action | Limit |
|---|---|
| Replies / 24h (Phase B) | 3 max |
| Replies / Reply Pass run | 1-2 max |
| Informative posts / week · / day | 2 max · 1 max |
| Subscribes / week | 5 max |
| Actions in same sub | min 6h apart |
| Actions globally | min 30 min apart |
| Karma builder comments / run · / day | 1-2 max · 3 max |

Count entries in `reddit-reply-log.md` and `reddit-post-log.md` at start of every run; abort early if a quota is already met.

Parallel crons share the global limit: take `<WORKSPACE_DIR>/.lock` at run start, release it at exit. Without the lock, the 30-min rule is unenforceable across jobs — two crons violate it silently.

## Anti-spam triggers

| Avoid | Use instead |
|---|---|
| "DM me", "contact me", "check our site", "more info here" | don't ask, don't link |
| `<BRAND_NAME>` in the body · "free consultation" | no brand name, no marketing |
| Phone number, email | never |
| Emojis · ALL CAPS | sober tone; bold/italic sparingly |
| **Any URL on `<BRAND_DOMAIN>`** (incl. `www.`, subdomains) | **never**, in any reply or post |
| bit.ly / tinyurl / shorteners | banned — Reddit spam-flags them directly |
| ≥ 2 links in one comment | max 1 external link per post, none in replies |

Behavioral: Reddit's published limits and most sub rules forbid reposting the same content < 7 days apart, and more than 3 actions in 30 min. Write each reply for its own thread — a copy-pasted opener is spam whether or not anything flags it. Wait ≥ 5 min after a post is created before replying: below that you have not read it. The quotas above exist to keep your account inside these rules and to keep the sub readable — **not** to defeat a detection system.

## Automation challenges — STOP, don't adapt

**When Reddit shows a CAPTCHA, a challenge page, or any anti-automation control, the run ends. A human publishes by hand.**

This is the doctrine, not a limitation of it. A challenge is Reddit stating that it wants a human for this action. Tuning an agent to look human enough to get past it is a Content Policy violation, it puts the account you are trying to protect at risk of permanent suspension, and it breaks on the next Reddit update. Stopping costs one post; being caught evading costs the account. This skill therefore does **not** describe how to satisfy, score against, solve, or route around any CAPTCHA, bot-detection or anti-automation control. If a control fires — most often on top-level post creation — follow the table below: the run ends and a human publishes.

| Situation | Action |
|---|---|
| CAPTCHA / challenge page mid-flow | Exit 2 → `status: blocked` → send the drafted title+body to the alert channel → human publishes |
| `BAD_CAPTCHA` in `result.json.errors` | Same. Do not retry. |
| Gate fires on every post for a week | Posting from this account is not viable unattended. Move to human-published drafts. |

The skill does not ship a posting script. If you wrap the submit call in one, have it exit with these codes so the recap below can be filled mechanically — `result.json` here is Reddit's POST response as your wrapper saved it.

| Code | Meaning | Recap action |
|---|---|---|
| 0 | Published, URL on stdout | `status: ok`, log post URL |
| 1 | Fatal error (UI ref missing, empty body) | `status: error`, attach screenshot |
| 2 | Challenge or CAPTCHA visible | `status: blocked`, draft to alert channel for manual publish |
| 3 | Session / login KO | `status: blocked`, alert user to re-login |

## Recovery & blockers

| Issue | Cause | Fix |
|---|---|---|
| `status: stopped` | Chrome not running | Report "relaunch Chrome on port `<BROWSER_PORT>`". STOP. |
| `name: null` from `/api/me.json` | Session expired | Report login expired. STOP. |
| HTTP 429 | Rate limited | Stop the run, report, wait for the next scheduled run. |
| HTTP 403 on POST | `modhash` expired | Re-fetch from `/api/me.json` once, retry once. Still 403 → report and STOP. |
| `RATELIMIT`, `DOMAIN_BANNED`, `SUBREDDIT_NOEXIST`, `USER_BLOCKED` in `result.json.errors` | Sub- or account-level refusal | Translate in the recap, no retry, freeze the sub if sub-level. |
| Comment invisible in profile after 5 min | Possible shadowban | Flag for human check (open profile in incognito). Track per-sub upvote ratios — community-level shadowbans don't fire this signal. |
| Post removed by automod < 30 min after publish | Sub rules or filter | Auto-freeze the sub 7 days. Append to `reddit-learnings.md`. |
| `evaluate` returns null, no error | Page not on reddit.com | Navigate first, retry once. |
| UI refs return null on labels that worked | Reddit shipped a UI change or the account language changed the labels | Re-snapshot, update the label map, re-test on `r/test` before re-enabling the cron. |
| Click on Publish does nothing / hits the wrong target | The Publish button's UI ref changes when it flips disabled → enabled once the fields are filled | Re-snapshot after filling the body, click the fresh ref. Never reuse a ref captured before the form was complete. |
| Posting cron killed mid-flow | 60-120 s default job timeout | Raise the per-job timeout well above the default — a UI publish flow plus verification takes minutes. |
| Account suspended | — | Stop everything. No automatic appeal. Human review only. Log the last action taken. |

## Mandatory recap

Alert channel (only if `alerts.webhook` is set — this message leaves your machine):

```
[Job name] — [status: ok|partial|blocked|skipped]
Public actions: [list short OR "no post/reply"]
Links: [URLs of new comments/posts]
Karma: link_karma=X comment_karma=Y total=Z
Blockers: [text OR "—"]
Next action: [1 line]
```

Filled instance:

```
reply-pass-evening — status: partial
Public actions: 1 reply in r/conseiljuridique
Links: https://reddit.com/r/conseiljuridique/comments/1a2b3c/_/kx9f2p1
Karma: link_karma=42 comment_karma=319 total=361
Blockers: informative-post skipped — CAPTCHA at publish, draft sent for manual posting
Next action: human publishes the draft; re-check sub freeze Thursday
```

Append the same block to `<WORKSPACE_DIR>/memory/reddit-recaps.md` with a `## YYYY-MM-DD HH:MM TZ — <job-id>` heading, plus Phase and subs touched. If nothing happened, say so: `no post/reply/subscribe performed, reason`.

## Memory files

| File | Purpose | Cadence |
|---|---|---|
| `reddit-recaps.md` | Per-run log (mandatory append) | Every run |
| `reddit-post-log.md` | Posts: sub, URL, date, score | Each post run |
| `reddit-reply-log.md` | Replies: thread URL, comment URL, sub, date, removed? | Each reply pass |
| `reddit-karma-log.md` | Daily karma snapshot + phase | Daily |
| `reddit-subs-state.md` | Per-sub freeze, flair, karma req, mod messages | After any sub-touching action |
| `reddit-ideas.md` | Content backlog | Weekly |
| `reddit-learnings.md` | What got upvoted / removed | Weekly + ad hoc |

All plain markdown under `<WORKSPACE_DIR>/memory/`. Nothing else is written; nothing is uploaded unless a webhook is set.

## Identity guardrails

- Neutral username, no brand in the handle. Bio: one generic line, no firm name, no contact info.
- **If anyone asks whether the account is automated or an AI, answer honestly and hand the thread to a human.** No ambiguous replies, no denial.
- Never give expert-grade advice in DMs — reply once with a neutral pointer to `<BRAND_DOMAIN>/contact` (the only place a brand URL is allowed: a DM the user started, never a public reply or post) and stop.
- Never share private case details, never promise an outcome, never solicit payment via Reddit.
- Never silently fake a successful action — verify via API or UI, or report the blockage.

**Better silence than spam. Better a blockage report than a fake success.**

## First-run checklist

- [ ] Placeholders filled; `alerts.webhook` set only if you accept the egress described above.
- [ ] Reddit account has a neutral username and a generic bio.
- [ ] Browser profile logged in; `/api/me.json` returns a non-null `name`.
- [ ] `<WORKSPACE_DIR>/memory/` exists with the 7 files.
- [ ] Read the rules of every sub in `<TARGET_SUBS>`. Some ban automation outright — drop those.
- [ ] Phase A confirmed (`total_karma < 100`) → only karma-builder + ops crons enabled.
- [ ] ≥ 2 weeks of organic activity before any brand-mentioning cron, even at karma ≥ 100.
- [ ] A human is on call to publish drafts when a challenge blocks a post.

## Scope

**This skill ONLY:** drives one logged-in Reddit profile you own; qualifies threads before replying; enforces karma phases and hard quotas; posts and replies within Reddit and subreddit rules; writes markdown logs under `<WORKSPACE_DIR>/memory/`; sends an opt-in recap webhook; stops and reports on any blocker.

**This skill NEVER:** solves, scores against, or works around a CAPTCHA, challenge, or bot-detection control; tunes timing or behavior to avoid being identified as automated; denies or obscures automation when asked; creates or operates multiple accounts to amplify one voice; votes, brigades, or bypasses a subreddit ban, mod removal, or rate limit; posts brand links; DMs unsolicited; publishes without the account owner's authority; or claims success it did not verify.
