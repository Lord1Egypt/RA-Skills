---
name: socialconductor
description: >
  Manage your SocialConductor AI comment automation bots from any chat app.
  Control Facebook, Instagram, YouTube, and TikTok — check status, pause or
  resume AI replies, view comment logs, manage leads, block users, post
  manual replies, regenerate AI replies, view analytics, manage prompts,
  control drafts and approvals, teach the AI, manage vacation mode, and
  access the viral vault. After a one-time 30-second browser setup per
  platform, all bot control and reply posting runs fully server-side —
  no ongoing browser access needed.
summary: >
  AI-powered social media comment automation for Facebook, Instagram, YouTube,
  and TikTok. Control your bots via chat — pause, resume, view logs, manage
  leads, block users, post manual replies, regenerate replies, analytics,
  AI teaching, drafts, vacation mode, viral vault, and advanced settings.
tags:
  - social-media
  - automation
  - facebook
  - instagram
  - youtube
  - tiktok
  - comments
  - ai-replies
  - marketing
  - saas
version: "2.0.0"
metadata:
  openclaw:
    emoji: "🤖"
    homepage: https://podium.socialconductor.ai
    always: false
---

# SocialConductor — Facebook, Instagram, YouTube & TikTok

Control your SocialConductor AI comment bots from WhatsApp, Slack, Telegram, or iMessage.

## Platforms

| Platform | Status | Dashboard |
|----------|--------|-----------| 
| 👥 Facebook / Instagram | ✅ Live | podium.socialconductor.ai |
| 📺 YouTube | ✅ Live | studio.socialconductor.ai |
| 🎵 TikTok | ✅ Live | violin.socialconductor.ai |

Each platform uses its own API key. You can connect one, two, or all three —
commands are prefixed by platform so OpenClaw always knows which bot you mean.

> ⚠️ **Safety notice:** This skill controls live social media accounts.
> Commands that post replies, block/unblock users, enable/disable the bot,
> or toggle simulation mode take effect immediately on real accounts.
> Only install this skill on accounts you own and control.
> Keep simulation mode on until you have tested your setup.
> Always use explicit platform-prefixed commands (e.g. `block facebook user @username`)
> rather than bare commands to avoid accidental triggering.

---

## Cross-Platform Core Features

These commands work on all three platforms. Prefix with `facebook`, `youtube`, or `tiktok`.

### Drafts & Approvals

| Say this | What happens |
|----------|-------------|
| show my [platform] pending drafts | View pending AI replies awaiting approval |
| approve all pending [platform] drafts | Bulk approve all pending AI replies |

### Analytics & Insights

| Say this | What happens |
|----------|-------------|
| show my [platform] daily analytics | Daily stats, reply counts, trends |
| show [platform] performance insights | Gemini-powered page performance summary |
| show [platform] enhanced analytics | Deep engagement and quality metrics |
| show [platform] sentiment trend | Daily sentiment breakdown over last 30 days |
| show [platform] ab stats | A/B prompt variant performance comparison |
| show commenter profile for @username on [platform] | Full 90-day history for a commenter |
| show comment detail for [comment_id] on [platform] | Full context, vibe, gate details for a comment |
| show [platform] ai insights | AI-generated performance insights via Gemini |

### AI Teaching & Prompt Control

| Say this | What happens |
|----------|-------------|
| show [platform] teaching examples | View star (good) and bad example lists |
| add this comment to [platform] teaching examples | Add an example to train AI tone |
| show [platform] prompt | View current A/B system prompts |
| update [platform] prompt | Update system prompt A and/or B |
| generate [platform] magic prompt | Auto-generate prompt from page profile via API |
| show [platform] advanced settings | View all advanced AI configuration |
| update [platform] advanced settings | Update one or more advanced settings |

### Scheduling & Tools

| Say this | What happens |
|----------|-------------|
| show my [platform] friends list | View friends / subscribed channels |
| turn on [platform] vacation mode | Configure away mode scheduling |
| open the [platform] viral vault | View top-performing viral comment examples |
| register push token for [platform] | Register device for push notifications |
| show [platform] skill manifest | View this platform's full API capability list |

---

## Facebook / Instagram — Account Requirements

> ⚠️ **Facebook requires a Business or Professional Creator account.**
> A personal Facebook profile will not work. Before connecting, make sure you have:
>
> - A **Facebook Page** (not a personal profile) set up at [business.facebook.com](https://business.facebook.com)
> - Your Page linked to a **Business Manager** or configured as a **Professional Creator Page**
> - Admin or Editor role on the Page
>
> Instagram automation is available if your Instagram account is connected to
> your Facebook Page as a **Professional (Creator or Business) Instagram account**.
> A standard personal Instagram account will not work.

## Facebook / Instagram — Setup (first time only)

Say:

> connect my facebook page

OpenClaw registers you and sends a browser link. Open it, log in with Facebook
(~30 seconds), close the tab. All Facebook and Instagram commands are now active.

> **Important:** Before the bot can post live replies, you must accept the
> SocialConductor terms of service at
> **https://podium.socialconductor.ai/terms** — takes 30 seconds.
> Until you do, the bot runs in simulation mode (replies are generated but
> not posted). You will see a `terms_required` error in chat as a reminder.

### Facebook / Instagram Trial

New accounts get a **7-day free trial** with up to 30 AI replies per day.
After the trial, visit podium.socialconductor.ai/upgrade to subscribe.

## Facebook / Instagram — Commands

> ⚠️ **These commands take immediate effect on your live social accounts.**
> Actions such as posting replies, blocking users, enabling/disabling the bot,
> and toggling simulation mode affect real customer-facing pages the moment
> they are confirmed. Use simulation mode while testing, and only run
> destructive commands (block, enable/disable, simulation mode off) when
> you explicitly intend to.

| Say this | What happens |
|----------|-------------|
| check my facebook bot | Mode, plan, trial status, daily usage, last 3 replies |
| pause my facebook bot | Hold ON — AI replies stop immediately |
| resume my facebook bot | Hold OFF — AI replies resume |
| show recent facebook comments | Last 5 log entries |
| show posted facebook comments | Only successfully posted replies |
| show facebook skipped comments | Comments the bot filtered (gate skips) |
| show my facebook leads | Lead-flagged comments (price, buy, how much…) |
| reply to facebook comment abc123 saying Great question! | Posts manual reply — posts immediately |
| regenerate facebook reply for comment abc123 | Re-runs AI on that comment with current settings |
| block facebook user @username | Adds @username to Facebook block list — requires platform prefix to avoid ambiguity |
| unblock facebook user @username | Removes @username from Facebook block list |
| show blocked facebook users | Lists all blocked accounts |
| facebook simulation mode on | Replies generated but not posted — safe testing mode |
| facebook simulation mode off | ⚠️ Bot posts live replies — confirm before running |
| enable facebook bot | ⚠️ Turns on auto-reply to live accounts |
| disable facebook bot | Turns off auto-reply |
| turn on viral intelligence | Enables Reaction-Weighted Intelligence |
| show my facebook pages | All connected pages with status and plan |
| connect my facebook page | Get a one-time browser link |

## Facebook / Instagram — Reviews (FB only)

| Say this | What happens |
|----------|-------------|
| show facebook reviews | Recent Google/FB business reviews |
| show facebook review drafts | Pending AI-drafted review replies |
| reply to review [id] saying [text] | Post or update a review reply |
| generate reply for review [id] | AI-generates a review reply |
| feedback on review reply [id] | Submit thumbs-up/down on an AI review reply |
| show facebook reviews analytics | Review response rate and sentiment stats |
| show facebook reviews settings | View review reply configuration |
| update facebook reviews settings | Update review reply configuration |

## Facebook / Instagram — Security

| Say this | What happens |
|----------|-------------|
| show facebook security audits | Recent prompt-injection / system-leak attempts caught by filters |

## Facebook / Instagram — Webhook Base URL
https://podium.socialconductor.ai/api/openclaw/

---

## YouTube — Account Requirements

> ⚠️ **YouTube requires an active YouTube channel.**
> A Google account alone is not enough — you must have created a YouTube channel
> at [youtube.com](https://youtube.com) before connecting. The channel can be
> a standard creator channel; no special business setup is required.

## YouTube — Setup (first time only)

Say:

> connect my youtube channel

OpenClaw registers you and sends a browser link. Open it, sign in with Google
(30 seconds), close the tab. All YouTube commands are now active.

## YouTube — Commands

> ⚠️ **These commands take immediate effect on your live YouTube channel.**
> Posting replies, enabling/disabling the bot, and toggling simulation mode
> affect your real channel the moment they are confirmed. Use simulation
> mode while testing.

| Say this | What happens |
|----------|-------------|
| check my youtube bot | Mode, plan, daily usage, last 3 replies |
| pause my youtube bot | Hold ON — replies stop |
| resume my youtube bot | Hold OFF — replies resume |
| show recent youtube comments | Last 5 log entries |
| show posted youtube comments | Only successfully posted replies |
| show youtube skipped comments | Comments the bot filtered |
| show youtube leads | Lead-flagged comments |
| reply to youtube comment abc123 saying Great question! | Posts manual reply |
| regenerate youtube reply for comment abc123 | Re-runs AI on that comment with current settings |
| show my youtube videos | Video polling status |
| show stale youtube videos | Videos with no recent activity |
| reactivate youtube video abc123 | Resumes polling that video |
| youtube simulation mode on | Replies generated but not posted |
| youtube simulation mode off | Bot posts for real |
| enable youtube bot | Turns on auto-reply |
| disable youtube bot | Turns off auto-reply |
| fast youtube response mode | Sets delay to fast |
| aggressive youtube response mode | Sets delay to aggressive |
| conservative youtube response mode | Sets delay to conservative |
| show youtube reviews settings | View YouTube community/reviews settings |
| update youtube reviews settings | Update YouTube community/reviews settings |

## YouTube — Webhook Base URL
https://studio.socialconductor.ai/api/openclaw/

---

## TikTok — Account Requirements

> ✅ **TikTok works with standard creator accounts.**
> No business account or special setup is required — any normal TikTok creator
> account can connect. Just make sure your account is active and can post/comment.

## TikTok — Setup (first time only)

Say:

> connect my tiktok account

OpenClaw registers you and sends a browser link. Open it on your phone or
computer, scan the TikTok QR code, close the tab. All TikTok commands are now active.

> **QR note:** TikTok login requires a QR code scanned in a real browser.
> OpenClaw sends you a link — it cannot embed the QR in chat.
> The link expires in 15 minutes.

### TikTok Trial

New accounts get a **7-day free trial** with up to 30 AI replies per day.
After the trial, visit violin.socialconductor.ai/upgrade to subscribe.
Expired trial channels are automatically removed from polling.

## TikTok — Commands

> ⚠️ **These commands take immediate effect on your live TikTok account.**
> Posting replies, blocking users, enabling/disabling the bot, and toggling
> simulation mode affect your real account the moment they are confirmed.
> Use simulation mode while testing, and always include the `tiktok` prefix
> on block/unblock commands to avoid ambiguity.

| Say this | What happens |
|----------|-------------|
| check my tiktok bot | Mode, plan, trial status, daily usage, last 3 replies |
| pause my tiktok bot | Hold ON — replies stop |
| resume my tiktok bot | Hold OFF — replies resume |
| show recent tiktok comments | Last 5 log entries |
| show posted tiktok comments | Only successfully posted replies |
| show tiktok skipped comments | Comments the bot filtered |
| show tiktok leads | Lead-flagged comments |
| reply to tiktok comment abc123 saying Great video! | Posts manual reply via Playwright — posts immediately |
| check tiktok reply status [job_id] | Poll status of an async Playwright reply job |
| regenerate tiktok reply for comment abc123 | Re-runs AI on that comment with current settings |
| block tiktok user @username | Adds @username to TikTok block list — requires platform prefix to avoid ambiguity |
| unblock tiktok user @username | Removes @username from TikTok block list |
| show blocked tiktok users | Lists all blocked accounts |
| show my tiktok videos | Video polling status |
| show stale tiktok videos | Videos with no recent activity |
| reactivate tiktok video abc123 | Resumes polling that video |
| connect my tiktok account | Get a QR code browser link |
| tiktok simulation mode on | Replies generated but not posted — safe testing mode |
| tiktok simulation mode off | ⚠️ Bot posts live replies — confirm before running |
| enable tiktok bot | ⚠️ Turns on auto-reply to live accounts |
| disable tiktok bot | Turns off auto-reply |
| fast tiktok response mode | Sets reply delay to fast |
| aggressive tiktok response mode | Sets reply delay to aggressive |
| conservative tiktok response mode | Sets reply delay to conservative |

## TikTok — Webhook Base URL
https://violin.socialconductor.ai/api/openclaw/

---

## Auth & Privacy

**API Keys:** The environment variables (`SC_FB_API_KEY`, `SC_YT_API_KEY`, `SC_TIKTOK_API_KEY`) are **SocialConductor-issued API keys** generated from your SocialConductor dashboard. They are *not* your native Meta, Google, or TikTok passwords or OAuth tokens. You only need to provide the keys for the specific platforms you wish to automate.

**Registration & Data Privacy:** When you run a `connect` command, OpenClaw sends only a secure, anonymous identifier (`{"openclaw_user_id": "..."}`) to the SocialConductor API via `POST /api/openclaw/register` to generate your one-time browser link. **No chat history, personal data, or agent context is transmitted during this registration phase.**

Tokens are stored locally by OpenClaw and sent as `Authorization: Bearer <key>` on every call. Keys are SHA-256 hashed before server-side storage — the plaintext is never saved remotely.

| Platform | Register endpoint |
|----------|-------------------|
| Facebook / Instagram | https://podium.socialconductor.ai/api/openclaw/register |
| YouTube | https://studio.socialconductor.ai/api/openclaw/register |
| TikTok | https://violin.socialconductor.ai/api/openclaw/register |

---

## Full API Route Reference

All routes require `Authorization: Bearer <key>` except `/register`.

### Core (all platforms)

| Method | Route | Description |
|--------|-------|-------------|
| POST | /api/openclaw/register | Register OpenClaw user, get API key |
| POST | /api/openclaw/link_token | Get one-time browser OAuth link |
| GET | /api/openclaw/status | Bot status, plan, usage, recent replies |
| POST | /api/openclaw/hold | Pause or resume AI replies |
| GET | /api/openclaw/logs | Comment activity log |
| POST | /api/openclaw/reply | Post a manual reply |
| POST | /api/openclaw/regenerate | Regenerate AI reply for a comment |
| GET | /api/openclaw/leads | Lead-flagged comments |
| GET | /api/openclaw/videos | Video polling status |
| POST | /api/openclaw/reactivate | Reactivate a stale video (YT/TT) |
| GET | /api/openclaw/drafts | Pending draft replies |
| POST | /api/openclaw/approve_bulk | Bulk approve drafts |
| GET,POST | /api/openclaw/settings | Get/update bot settings |
| GET,POST | /api/openclaw/live_settings | Get/update live-mode settings |
| POST | /api/openclaw/register_push_token | Register device push notification token |
| GET | /api/openclaw/skill_manifest | Platform API capability manifest |

### Analytics

| Method | Route | Description |
|--------|-------|-------------|
| GET | /api/openclaw/analytics | Daily stats and reply counts |
| GET | /api/openclaw/analytics/enhanced | Deep engagement and quality metrics |
| GET | /api/openclaw/insights | Gemini-powered performance summary |
| GET | /api/openclaw/ai_insights | AI-generated page insights |
| GET | /api/openclaw/ab_stats | A/B prompt variant performance |
| GET | /api/openclaw/sentiment_trend | Daily sentiment breakdown |
| GET | /api/openclaw/commenter_profile | 90-day profile for a specific commenter |
| GET | /api/openclaw/comment_detail | Full context and gate info for a comment |

### AI Teaching & Prompts

| Method | Route | Description |
|--------|-------|-------------|
| GET | /api/openclaw/examples | Star and bad example lists |
| POST | /api/openclaw/teach | Add a teaching example |
| GET,POST | /api/openclaw/prompt | View/update A/B system prompts |
| POST | /api/openclaw/magic_prompt | Auto-generate prompt from page profile |
| GET,POST | /api/openclaw/advanced | View/update advanced AI settings |

### Tools & Features

| Method | Route | Description |
|--------|-------|-------------|
| GET | /api/openclaw/friends | Friends / subscribed channels list |
| POST | /api/openclaw/vacation | Configure vacation/away mode |
| GET | /api/openclaw/viral_vault | Top-performing viral comment examples |

### Facebook / Instagram Only

| Method | Route | Description |
|--------|-------|-------------|
| GET | /api/openclaw/pages | All connected pages with status and plan |
| GET | /api/openclaw/blocked | Blocked user list |
| POST | /api/openclaw/block | Block a user |
| POST | /api/openclaw/unblock | Unblock a user |
| GET | /api/openclaw/security_audits | Prompt-injection / system-leak audit log |
| GET | /api/openclaw/reviews | Business reviews |
| GET | /api/openclaw/reviews/drafts | Pending AI-drafted review replies |
| POST,PUT,DELETE | /api/openclaw/reviews/\<id\>/reply | Post, update, or delete a review reply |
| POST | /api/openclaw/reviews/\<id\>/generate | AI-generate a review reply |
| POST | /api/openclaw/reviews/\<id\>/feedback | Thumbs-up/down on a review reply |
| GET | /api/openclaw/reviews/analytics | Review response rate and sentiment |
| GET,POST | /api/openclaw/reviews/settings | View/update review reply configuration |

### TikTok Only

| Method | Route | Description |
|--------|-------|-------------|
| GET | /api/openclaw/blocked | Blocked user list |
| POST | /api/openclaw/block | Block a user |
| POST | /api/openclaw/unblock | Unblock a user |
| POST | /api/openclaw/qr_start_link | Start a TikTok QR login session |
| GET | /api/openclaw/qr_poll_link | Poll QR login completion status |
| GET | /api/openclaw/reply_status/\<job_id\> | Poll async Playwright reply job status |

### YouTube Only

| Method | Route | Description |
|--------|-------|-------------|
| GET,POST | /api/openclaw/reviews_settings | YouTube community/reviews settings |

---

## Error Reference

| Error code | Meaning |
|------------|---------|
| `unauthorized` | API key missing or invalid |
| `trial_expired` | 7-day trial ended — upgrade at the platform's /upgrade page |
| `no_page` | Platform not linked yet — say "connect my facebook/tiktok/youtube account" |
| `terms_required` | Terms of service not accepted — visit podium.socialconductor.ai/terms |
| `rate_limited` | Platform rate-limited this channel — bot resumes automatically |
| `reply_failed` | Reply attempt failed — check dashboard for details |

---

## 📱 iOS App — SocialConductor for iPhone

Manage your bots natively from your iPhone. The SocialConductor iOS app gives
you a full mobile dashboard for all three platforms. After the one-time OAuth setup, everything runs server-side — no ongoing browser access needed.

**Download:** [SocialConductor on the App Store](https://apps.apple.com/us/app/socialconductor/id6764723628)

**Requirements:** iOS 15.1 or later · Free · 31.7 MB

**What's in the app:**
- Unified mobile dashboard for Facebook/Instagram, YouTube, and TikTok
- Real-time comment logs, leads, and reply management
- AI Insights and analytics with enhanced graphs
- Chat history with context and reply viewer
- Pull-to-refresh comment logs
- Live streaming support for Facebook, YouTube, and TikTok
- Push notifications for new comments and replies
- Multiple themes: Glass, AMOLED, Dark Pro, and Slate Clean
- Demo mode for evaluating features before connecting accounts

The app and the OpenClaw chat interface share the same backend — changes made
in one are immediately reflected in the other.

---

## Support

- Email: support@socialconductor.ai
- iOS App: https://apps.apple.com/us/app/socialconductor/id6764723628
- Facebook Dashboard: https://podium.socialconductor.ai
- YouTube Dashboard: https://studio.socialconductor.ai
- TikTok Dashboard: https://violin.socialconductor.ai
