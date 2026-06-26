# Viral Thread Writer

**Turn any idea, article, or URL into a high-engagement Twitter/X thread in seconds.**

Stop staring at a blank screen. Viral Thread Writer takes what you know and transforms it into a scroll-stopping thread — complete with a hook, numbered tweets, and a CTA that actually converts.

---

## What it does

- 🪝 **Scroll-stopping hook tweet** — engineered to make people stop, read, and click "show more"
- 🔢 **Numbered body tweets** — one clear idea per tweet, structured for maximum readability and retention
- 📣 **Closing CTA tweet** — a natural, compelling prompt that drives follows and retweets
- ✍️ **Two tone modes** — switch between **Professional** (authoritative, data-driven) and **Casual/Conversational** (punchy, relatable, first-person)
- 📐 **5–10 tweet threads** — generates the right length for your content, or you specify exactly how many tweets you want
- 📊 **Thread stats block** — character counts per tweet, tone applied, estimated read time, and thread theme at a glance

---

## Who it's for

- **Content creators & newsletters writers** who want to repurpose long-form content into X threads without the hours of manual work
- **Solopreneurs & indie hackers** building an audience on X alongside their product or service
- **Marketers & brand strategists** who need consistent, on-brand social content produced quickly
- **Coaches & consultants** who have deep expertise but find social writing time-consuming or unnatural
- **Startup founders** who want to build in public and share insights without a dedicated content team

---

## Installation

```bash
npx clawhub install tetsuakira-vk/viral-thread-writer
```

Once installed, the skill is available inside Claude Code. Open your project, invoke the skill, and start generating threads immediately.

---

## Usage

### Example 1 — Thread from a raw idea

**Input:**
```
Write a casual thread about why most people never finish side projects.
```

**Output (excerpt):**
```
🧵 THREAD PREVIEW
─────────────────────────────────

[HOOK — Tweet 1]
Most side projects don't die because of lack of time.
They die because of one mistake you're probably making right now.
Here's what I wish someone told me earlier 🧵
(Characters: 187/280)

─────────────────────────────────

[Tweet 2]
2/ You started with the exciting part.
The idea, the name, the tech stack, the logo.
That dopamine hit felt like progress.
It wasn't.
Real progress is the boring middle — and nobody prepares you for it.
(Characters: 203/280)

─────────────────────────────────

[CTA — Final Tweet]
If this resonated, RT to share it with someone stuck in the graveyard of half-built projects 🔁
I write threads like this every week — follow along so you don't miss the next one.
(Characters: 181/280)

─────────────────────────────────

📊 THREAD STATS
• Total tweets: 7
• Tone: Casual/Conversational
• Estimated read time: ~42 seconds
• Thread theme: Why side projects fail and how to think differently about finishing
```

---

### Example 2 — Thread from pasted article text

**Input:**
```
[Paste a 600-word blog post about compound interest principles applied to skill-building]
Tone: professional
```

**Output (excerpt):**
```
[HOOK — Tweet 1]
A 1% improvement every day sounds trivial.
Over one year, it makes you 37 times better.
Most professionals ignore this entirely. Here is why compound skill-building is the highest-leverage investment you can make: 🧵
(Characters: 216/280)

[Tweet 2]
2. Compound interest is intuitive when applied to money.
We understand it in finance because the numbers are visible.
Applied to skills, the returns are invisible for months — which is exactly why most people quit before they compound.
(Characters: 234/280)
```

---

### Example 3 — Specifying thread length and audience

**Input:**
```
Write a 5-tweet professional thread about the importance of email list building for creators.
Target audience: YouTube creators just starting out.
```

The skill will produce a tight, focused 5-tweet thread calibrated specifically for early-stage YouTubers, in a professional register, with a hook, three body tweets, and a CTA.

---

## Requirements

- **Claude Code** with [ClawHub](https://clawhub.dev) installed
- **Node.js 18+** (required for the `npx clawhub` installer)
- No external APIs, browser access, or additional configuration required — works entirely within your Claude Code session

---

## Licence

MIT — free to use, modify, and distribute. See [LICENSE](./LICENSE) for full terms.

---

## Get Pro Version

The free version covers the core workflow. The **Pro version** unlocks:

- Thread series mode: chain 3 related threads into a campaign
- Platform variants: auto-generate LinkedIn and Instagram carousel versions of the same thread
- Engagement analytics prompt: suggests what to post in replies to boost reach
- A/B hook generator: 5 alternative hook tweets to test
- Evergreen repurposing: rewrites thread as a newsletter section and a blog intro

**[$19 — Get the Pro version →](https://whop.com/promptclaw-pro/viral-thread-writer-pro/)**

One-time payment. Lifetime access. No subscription.

