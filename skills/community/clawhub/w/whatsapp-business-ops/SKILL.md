---
name: whatsapp-business-ops
description: Run WhatsApp Business outbound without losing quality score — 24h window, approved templates, duplicate guard. Use when answering inbound leads or sending follow-ups from a cron.
metadata: {"clawdbot":{"emoji":"💬","requires":{"bins":["curl"]},"homepage":"https://clawhub.ai/alexbloch-ia/whatsapp-business-ops"}}
---

# WhatsApp Business Management

**WhatsApp is not a discovery channel — it is a conversion channel.** The goal is not to send fast: it is one qualified hand-off per opt-in lead, no unsolicited bulk, no duplicate send. Reference BSP: Whatchimp (Meta Business Partner); any BSP works.

## Access, data, and network — read before running

**Every access is opt-in — each one stays off until you fill its placeholder in `## Configure`. The default is no network.**

| Access | Why | Default |
|---|---|---|
| BSP API token (`<WA_API_KEY>`) | Send/read messages | None — no network call without it |
| CRM sheet ID (`<CRM_SHEET_ID>`) | One row per lead | None — CRM writes skipped |
| Alert channel / webhook (`<ALERT_CHAT_PRIMARY>`) | **Leaves your machine.** Posts lead name + phone to Telegram/Slack/Discord | None — recap stays local |
| Local workspace (`<WORKSPACE_DIR>/memory/`) | State + duplicate guard | Local files only |

**Personal data persisted, in full:** display name, case type, free-text situation, conversation timestamps, template-send log, alert log, per-run recaps. **Phone numbers are stored raw ONLY in `wa-crm-state.md`** (the system-of-record mirror); every duplicate register and the blacklist key on `sha256(phone)[0:12]`. That is lead PII on disk — `## Data minimization and retention` is doctrine, not an appendix. Scope the API token to the one business number; never reuse a full-account token.

## When to Use

| Trigger | Action |
|---|---|
| "answer the whatsapp leads" | `wa-inbound` run — §Flow, free-form only inside open window |
| "send the first message to new leads" | `wa-outbound` run — approved template only |
| "relance the cold leads" | `wa-followup` run — cadence table |
| "quality score dropped" / "number got paused" | Stop outbound. `## Troubleshooting`, last two rows. Human review |
| "am I talking to a bot?" (asked by a lead) | Answer honestly, immediately — `## Identity` |

## Configure

| Placeholder | Example | Your value |
|---|---|---|
| `<BRAND_NAME>` | "Acme Studio" | — |
| `<WA_BUSINESS_NUMBER>` | "+1 555 0000" | — |
| `<WA_PHONE_NUMBER_ID>` | numeric ID from your BSP | — |
| `<WA_API_KEY>` | scoped to one number | — |
| `<WA_TEMPLATE_FIRST_CONTACT>` / `_FOLLOWUP_SOFT` / `_FOLLOWUP_HARD` / `_CLOSING` | Meta-approved template IDs | — |
| `<CRM_SHEET_ID>` | Sheet/Airtable ID | — (omit → no CRM write) |
| `<ALERT_CHAT_PRIMARY>` | alert chat ID | — (omit → local recap only) |
| `<WORKSPACE_DIR>` | "~/.openclaw/workspace/whatsapp-acme" | — |

```yaml
# <WORKSPACE_DIR>/config.yaml
whatsapp:
  phone_number_id: <WA_PHONE_NUMBER_ID>
  base_url: https://app.whatchimp.com/api/v1   # swap host for another BSP
templates:
  first_contact: <WA_TEMPLATE_FIRST_CONTACT>
  followup_soft: <WA_TEMPLATE_FOLLOWUP_SOFT>
  followup_hard: <WA_TEMPLATE_FOLLOWUP_HARD>
  closing: <WA_TEMPLATE_CLOSING>
crm: { sheet_id: <CRM_SHEET_ID>, tab: "Leads" }
alerts: { primary_chat: <ALERT_CHAT_PRIMARY>, channel: telegram }
retention: { lead_days: 90, recap_days: 30, template_log_days: 30 }
inbound_pipeline:
  shared_queue_file: <WORKSPACE_DIR>/../shared/leads-whatsapp.json
schedule:  # dm_check "*/2 9-22 * * *" · add_contacts "*/5 9-22 * * *" · follow_up "0 10 * * *"
  timezone: Europe/Paris
```

## The 24h window — the central law

After **any** message a user sends you, you have **24 h** to reply in free-form. After 24 h of user silence, only **Meta-approved templates**, each billed as a new conversation. Free-form to a cold conversation → API rejection or a marketing-conversation bill + a quality hit; exit code 2, always skipped. Check window state **before every outbound send**:

```bash
curl -s "https://app.whatchimp.com/api/v1/whatsapp/get/conversation" \
  -d "apiToken=<WA_API_KEY>" -d "phone_number_id=<WA_PHONE_NUMBER_ID>" \
  -d "phone_number=<DIGITS>" -d "limit=1"
# Output: {"status":1,"data":[{"sender":"user","created_at":"2026-07-16T09:12:04Z"}]}
# sender="user" and < 24h old  → free text OK. Otherwise → template.
```

Session check first on every cron:

```bash
curl -s "https://app.whatchimp.com/api/v1/whatsapp/subscriber/list" \
  -d "apiToken=<WA_API_KEY>" -d "phone_number_id=<WA_PHONE_NUMBER_ID>" \
  -d "limit=1" -d "offset=1"
# Output: {"status":1,"data":[...]}   401/403 → stop+alert · 429 → stop, wait next run
```

Timeout > 10 s → BSP down: **one retry, then stop and alert. Never retry in a loop.** A 200 OK carrying `status=0` is a failure, not a send.
Never send a "test" message to a real lead — use a dedicated test number. Never auto-rotate an API token from inside a cron; rotation is a human action.

## Phase gating and quotas

Meta assigns each number a tier: **T1** 1k uniques/24h · **T2** 10k · **T3** 100k · **T4** unlimited. New numbers start at T1. Tiers rise on volume + quality, and fall — or the number gets paused — when quality drops.

| Condition | Phase | Outbound |
|---|---|---|
| Tier 1 **or** quality yellow/red | **A** | Inbound replies + approved-template follow-ups. ≤ 50 first-contact/day |
| Tier 2+ **and** quality green, no drop in 14 d | **B** | Full doctrine, first week capped at 50% of Phase B max |

Read `memory/wa-state.md` at start of every run. Phase B is a **manual flip**, never automatic. Any quality drop → revert to A immediately.

| Action (hard limits) | Phase A | Phase B |
|---|---|---|
| Inbound replies / cron run | 20 | 50 |
| First-contact templates / 24 h | 50 | 500 |
| Follow-up templates / 24 h | 20 | 200 |
| Unique recipients / 24 h | 800 (under T1's 1000 cap) | tier cap − 10% |
| Conversations / cron run | 30 | 80 |
| Same user — outbound spacing | min 24 h between any two outbound |

Follow-up cadence: J+1 soft · J+3 soft · J+7 hard · J+15 hard · J+20 closing → `status=lost`. **Stop after the closing template.** Continuing past J+20 is ban-risk territory.

## Duplicate guard — the most important section

Quality-score collapse is dominated by duplicate template sends. Three registers, read **before** every outbound action:

| Register | Row format | Rule |
|---|---|---|
| `wa-alerts-sent.md` | `{"phone_hash":"<sha256:12>","qualified_date":"YYYY-MM-DD"}` | Phone present → **never** alert twice |
| `wa-template-log.md` | `{"phone_hash":"<sha256:12>","template_id":"<ID>","sent_at":"<ISO>","result":"ok\|error"}` | Same (phone, template) in last 24 h → SKIP |
| `wa-crm-state.md` | one row per phone, never two | Only `wa-outbound` appends; every other cron UPDATEs |

> **If in doubt, SKIP.** It is always better to skip than to send a duplicate. This one rule is the difference between a number that stays Tier 2 for years and one paused in 30 days.

Alert **only** when a lead replies AND qualifies — never after a first template send. Alerting on first contact generates dozens of false alerts and trains the human team to ignore the channel.

## Data minimization and retention

The registers above hold lead PII — a regulated store, not logs.

| Rule | Concretely |
|---|---|
| Minimize | Store phone + name + case type + status. Never store ID numbers, health details, case documents, or payment data in memory files — keep those in the system of record. |
| Mask | Key the duplicate registers on `sha256(phone)[0:12]`, not the raw number. Lookups work identically; a leaked log exposes nothing. |
| Restrict | `chmod 700 <WORKSPACE_DIR>/memory`. One number = one workspace. Never share `wa-template-log.md` across numbers or brands. |
| Retain | Leads 90 d after last contact, recaps 30 d, template log 30 d — then delete. Prune at the start of the daily run, not "someday": `find "<WORKSPACE_DIR>/memory" -name 'wa-recaps.md' -mtime +30 -delete` (silent — pruned, not archived). |
| Alert payload | Name + case type + phone only. Never paste conversation transcripts into the alert channel — it leaves your machine and is usually a wider audience than the case file. |
| Erase | On an opt-out or deletion request: purge every register, add the hash to `wa-blacklist.md`, confirm to the lead. Blacklist stores hashes only. |
| Sensitive niches | Legal, medical, financial: confirm with your DPO/counsel before any cron writes lead data. This skill does not make that call for you. |

## Identity — disclose, never dodge

**If a lead asks whether they are talking to a bot, a human, or an AI: say so plainly, in the same message, and offer the human.**

```
You're talking to <BRAND_NAME>'s automated assistant. I can take your details
now and a specialist will call you back — or I can pass you to them right away.
```

No ambiguity, no pivot, no "I'm part of the team". Honest disclosure is not a cost here: a lead who discovers the automation later is a complaint, a block, and a quality-score hit. Blocks and reports are exactly what Meta measures. **Disclosure is account safety.** Escalate to a human — stop the automated replies for that thread and alert — when the lead asks for a human, asks twice about identity, or raises anything the templates do not cover.

## Reply rules (free-form, inside open window)

- Match tone. Short messages. **One ask per message.** Reassuring on stressful topics, never dramatizing. Reread the full visible history before composing.
- **Never**: definitive price quotes (soft "starting at" only if asked) · outcome guarantees · confidential client info · documents/PDFs to non-clients · anything outside the brand's scope.

Skeletons: **A** greeting + "how can we help" · **B** empathy + one contextual question · **C** hand-off: `Thank you for these details. A specialist from <BRAND_NAME> will call you back. Could you confirm your name and the best time to reach you?`

Classify every thread before drafting — `case type` is what the alert payload and the recap carry. Structure below, questions are yours:

| Case type | Signal | Action |
|---|---|---|
| **A** — high urgency | Pending deadline, acute problem | Ask date, location, urgency → collect contact → qualified |
| **B** — mid intent | Ongoing situation, no deadline | 5-7 contextual questions → collect contact → qualified |
| **C** — out of scope | Not what the brand does | Redirect to the right channel. **Never force qualification** |
| **D** — existing client | Phone-match in `wa-clients-known.md` | Answer with empathy, redirect to the standard client support line. **Never paste the prospect CTA** — a paying client who gets a sales pitch blocks, and a block is a quality hit |

**"Too many questions" failsafe** — after 5 questions with no contact info, switch: *"To answer precisely, a specialist needs to call you back. Could you confirm your name + best time?"* This converts more question-only threads than any other tactic.

Qualification requires: thread open · not blacklisted · not already "qualified — awaiting callback" · no auto-reply in the last 60 s (anti-cascade). Any check fails → skip.

## Flow

### wa-inbound (every 2 min)
```
1. Session check. 2. subscriber/list unseen_count>0 — if 0 unread → STOP.
3. Per unread (≤20 A / ≤50 B): get/conversation limit=20 → if last sender="bot" SKIP
   → qualify → draft → normalize encoding → POST /whatsapp/send → verify status=1.
4. If qualified: check wa-alerts-sent.md → if absent, alert primary chat, append hash.
   UPDATE the CRM row (wa-inbound never APPENDs). 5. Recap.
```

### wa-outbound (every 5 min)
```
1. Session check. 2. Read shared queue, filter status="pending" — if 0 → STOP.
3. Per lead: template-log 24h check → subscriber/create → POST /whatsapp/send/template
   template_id=<WA_TEMPLATE_FIRST_CONTACT> → verify status=1 → queue status="first_message_sent"
   → APPEND CRM row (only cron that appends) → append template log.
4. Never alert from this cron. 5. Recap.
```

### wa-followup (daily 10:00)
```
1. Session check. 2. CRM: status in {first_message_sent, follow_up_sent}, idle at a J+N mark.
3. Per candidate: template-log check → send cadence template → update CRM + log. 4. Recap.
```

### WhatsApp Web via Playwright — gray area, not recommended
Running Playwright against `web.whatsapp.com` is **outside WhatsApp's Business Terms** and risks a permanent number ban. It is documented here only as a read-only contingency while BSP approval is pending, and it is **not recommended for production**. Requires an explicit human decision per incident — an agent must not choose this path on its own. Sessions rotate the QR link unpredictably (daily manual re-login); no template sends are possible; quality score still applies at the number level. If a login challenge or automation check appears: **stop and hand the session to a human.** Never tune timing to avoid a detection check. Migrate back to the BSP API as soon as approval lands.

## Exit codes

| Code | Meaning | Recap |
|---|---|---|
| 0 | Sent, or nothing to do (zero unread) | `status: ok` |
| 1 | Fatal (API 5xx, JSON parse fail) | `status: error`, alert |
| 2 | 24h-window violation attempted → skipped | `status: skip`, log |
| 3 | Auth fail (401/403) | `status: blocked`, alert now |
| 4 | Duplicate-guard SKIP | `status: ok` |

## Output Format — mandatory recap

Every run ends with this, verbatim, to the alert channel and appended to `memory/wa-recaps.md`:

```
[Job name] — [status: ok|partial|blocked|skipped]
Inbound replies: [N or "—"]
Templates sent: [N or "—"]
Qualified leads: [count + first names only]
Phase / Tier: [A|B / Tier 1|2|3|4]
Quality score: [green|yellow|red]
Blockers: [text OR "—"]
Next action: [1 line]
```

Filled instance:

```
wa-inbound 10:32 — status: ok
Inbound replies: 7
Templates sent: —
Qualified leads: 2 (Marc, Lina)
Phase / Tier: A / Tier 1
Quality score: green
Blockers: —
Next action: human callbacks due before 12:00
```

**Better silence than spam. Better a blockage report than a fake success.** Never fake a successful send.

## Troubleshooting

| Symptom | Root cause | Fix |
|---|---|---|
| 200 OK, message never delivered | `phoneNumberID` vs `phone_number_id` — BSP casing differs **per endpoint**. No error is raised, so you'll believe your code is right | Check casing per endpoint. Verify `status=1` in the body, not just HTTP 200 |
| Send rejected for unknown reason | Leading `+` in the number. `33612345678` works, `+33612345678` often does not | Strip `+` before every call |
| Accents vanish in delivered messages | Some BSPs munge non-ASCII silently | Roundtrip test once (send accented → fetch back). If it munges: strip accents, emojis, typographic quotes, em-dashes before send |
| Message body shows an empty slot | Template variable `{{1}}` sent with no parameter — silently renders blank | Pass every slot explicitly |
| Templates sent from the wrong number | Multiple bots on one BSP account, active bot not verified | Verify active bot before the first send of every cron |
| "outside 24h window" error | Free-form on a closed conversation | Switch to template, retry once |
| Inbound message seen after 24 h | Webhook latency — the window closed while nothing errored, so no alarm fired | Reopen with a template: **UTILITY category if one exists, MARKETING otherwise** (different billing and Meta tolerance). Explain the delay in a variable slot. Log in `wa-incidents.md`, audit webhook latency |
| "template not approved" | Meta rejected or paused it | Stop using it. Pick the fallback template. Never re-approve by editing content post-approval |
| Quality score yellow → red overnight | Score lags hours, not minutes — one bad run degrades it for 1-2 days | Yellow: flip to Phase A, audit template content. Red: inbound only, alert, manual review of 7 days |
| Number paused by Meta | Usually: outbound to non-opted-in leads, duplicate templates, or content drift | Stop everything. Review last 200 actions. Appeal via BSP. **Never** spin up a second number to get around it — Meta cross-checks businesses |

## Memory files

`memory/`: `wa-state.md` (phase/tier/quality) · `wa-alerts-sent.md` · `wa-template-log.md` · `wa-crm-state.md` · `wa-blacklist.md` (hashes) · `wa-clients-known.md` · `wa-recaps.md` · `wa-learnings.md` · `wa-incidents.md`. Shared: `../shared/leads-whatsapp.json` (written by upstream social agents, read by `wa-outbound`).

```bash
mkdir -p "<WORKSPACE_DIR>/memory" && chmod 700 "$_" && cd "$_" && for f in wa-recaps wa-state \
  wa-alerts-sent wa-template-log wa-crm-state wa-blacklist wa-clients-known wa-learnings \
  wa-incidents; do [ -f "$f.md" ] || : > "$f.md"; done
mkdir -p "<WORKSPACE_DIR>/../shared" && Q="<WORKSPACE_DIR>/../shared/leads-whatsapp.json"
[ -f "$Q" ] || echo '[]' > "$Q"   # wa-outbound reads this at step 2 — absent = first run crash
# Output: (silent, idempotent) — existing files are never truncated
```

## First-run checklist

- [ ] Placeholders filled; token scoped to one number.
- [ ] BSP account approved, business number verified by Meta, ≥3 templates approved.
- [ ] `memory/` exists, `chmod 700`, retention values set in `config.yaml`.
- [ ] Alert channel tested with "hello" — and confirmed as an acceptable destination for lead names.
- [ ] Opt-in pipeline documented: how each lead consented, and where that proof lives.
- [ ] Phase A confirmed, quality green.
- [ ] Human team review: who reads alerts, callback SLA, escalation path, who handles deletion requests.

## Scope

**This skill ONLY:** operates a WhatsApp Business number through a BSP API you own · sends free-form inside an open 24h window and Meta-approved templates outside it · contacts leads who opted in on another channel · qualifies and hands off to a human · keeps a masked, retention-bounded local state to avoid duplicates.

**This skill NEVER:** sends unsolicited bulk or non-opted-in outbound · sends free-form to a cold conversation · hides or denies the automation when a lead asks · adapts timing or behavior to slip past an automated check — when one appears, it stops and a human takes over · stores case documents or special-category data in memory files · retains lead data past the configured window · creates a second number to work around a Meta pause · rotates tokens or restarts infrastructure by itself.

Meta's WhatsApp Business Terms, the WhatsApp Business Messaging Policy, and your jurisdiction's privacy law are binding constraints on every run in this document. Where this doctrine and those rules disagree, those rules win.
