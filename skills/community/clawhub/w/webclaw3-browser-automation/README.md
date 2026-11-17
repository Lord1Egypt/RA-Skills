# webclaw3 — Browser Automation & Web Scraping for AI Agents

**English** | [中文](./README.zh-CN.md)

> Teach your AI agent browser tasks once — run free forever.

**It runs in *your* Chrome, with *your* logins.** No fresh headless browser to re-authenticate, no passwords handed to anyone, no login wall blocking the page you need. Setup is 3 steps, about 5 minutes.

Every time you ask an AI agent to do something in a browser, you pay in tokens — and the result is flaky: it works today, fails tomorrow with nothing changed. webclaw3 turns one successful exploration into a reusable **skill**, so a task you run every day stops costing you every day.


## The cost problem

A single "go look at this site" task costs millions of tokens. Here's a real API bill for one browser task:


- Prompt 2.3M × $3/MTok = $6.90 | Completion 20.5K × $15/MTok = $0.31 | Cache 2.1M × $0.30/MTok = $0.63
- With cache-hit variance: **~$2–$3+ per task** on Sonnet
- On Opus ($5/$25) the same task runs **$5–$8+**; complex multi-step exploration easily exceeds $10

Run it daily and that's **$90+ a month** — for the exact same steps, re-thought from scratch every time. On top of that, you've got 3 everyday headaches:

- **It burns cash daily.** Same site, same steps, millions of tokens every single time — like hiring someone who forgets everything overnight.
- **It's unreliable.** AI browsing is inherently flaky; a task succeeds now and fails next time just because elements loaded in a different order.
- **It needs babysitting.** You pay AND watch it run, ready to re-run at any moment.

## How it works

The fix: **explore once, distill it into a skill, rerun it for free.** Everything happens on your own machine, inside the agent you already use (Claude Code, workbuddy, qoderwork).

**① Explore — figure out what you actually want.** Just point in a rough direction; the agent drives your real browser with this skill. Requirements are discovered by trying: watch the real output and adjust scope, filters, fields — until you can say *"this is exactly it."*

**② Distill — one sentence turns it into a skill.** Say *"distill this into a skill."* The agent confirms the final requirements with you, then **webclaw3** re-explores the site with your local Chrome login state, generates the skill, and validates it with varied parameters — tens of minutes in the background, all on your own machine.

**③ Run daily — deterministic and ~free.** The generated skill is a plain script: **zero or near-zero tokens**, millisecond response, identical results every run. Schedule it, rerun it any time.

**④ Repair — also free.** When the site redesigns and a skill breaks, hand the error to your local agent; it fixes the skill locally, no charge.

| | Raw AI | With a skill |
|---|---|---|
| Simple task (one-off) | $2 ~ $3 | $0 |
| Complex task (one-off) | $5 ~ $10+ | $0 |
| Daily task, per month | $60 ~ $300 | $0 |
| Reliability | Hit or miss | Deterministic, consistent every time |

## Quickstart

You never leave your agent's chat — Claude Code, workbuddy, or qoderwork all work. Everything below is things you *say*; the agent runs the commands.
> Works with any agent: [Claude Code](docs/claude-code.md) · [workbuddy](docs/workbuddy.md) · [qoderwork](docs/qoderwork.md)

**1. One-time setup.** Two small things first:

- **Install the Chrome extension** (a few clicks only you can do, once): download [wc3-chrome](https://github.com/fatmind/wc3-chrome), open `chrome://extensions`, enable **Developer mode** → **Load unpacked** → pick the `extension/` directory.
- **Log into [webclaw3.com](https://webclaw3.com) and grab your Access Key**: it's your account key — it meters skill generation and unlocks the **site-knowledge base** (site structures others have already explored, making your generation faster and sturdier). Bonus: contributing the sites you explore earns points you can redeem for generation quota — earlier is better, see [Pricing](#pricing).

Then say to your agent:

```
Install webclaw3 (https://github.com/fatmind/webclaw3) for me, then check the environment
```

The agent clones this repo into your skills directory, starts the local services, and walks you through the basic configuration (paste the Access Key you just got, etc.). One thing worth knowing: webclaw3 drives *your* browser with *your* login state — passwords never go through anyone.

**2. Explore.** Describe a task roughly and let the agent run it for real:

```
Show me what's on the download trending list at SkillHub (https://skillhub.cn/)
```

Adjust as you watch (`add downloads and rating to each item` / `top 10 is enough`) until it's exactly what you want. Only once you're happy is it worth distilling — so you never pay for that run, in money or time, again.

**3. Distill.** Say:

```
Distill that into a skill — I want to run it every day
```

webclaw3 tidies up your requirements, and on your OK generates locally. Generation takes tens of minutes in the background — the agent polls progress, validates, and installs the skill automatically.

**4. Run it daily:**

```
/skillhub-trending run today's list
```

or schedule it (`run skillhub-trending every morning at 8`). Runs locally, fast, stable, zero or near-zero tokens.

**5. Something broke:** also just one sentence:

```
skillhub-trending failed — webclaw3, fix it for me
```

webclaw3 repairs it locally.

## Pricing

- **Generating a skill**: 10 free per account, failures don't count
- **Daily runs**: free — skills execute on your machine
- **Repairs**: free — fixed locally
- **Contribute site knowledge, earn points**: what gets sent back is the site's page structure — **never any user information**. Contributions accumulate points you can redeem for generation quota, with revenue sharing for contributors planned. Earlier is better: sites are finite, first come first served

Details on [webclaw3.com](https://webclaw3.com).

## Learn more

- Per-agent guides: [Claude Code](docs/claude-code.md) · [workbuddy](docs/workbuddy.md) · [qoderwork](docs/qoderwork.md)
- How the skill itself works: [docs/webclaw3-intro.md](docs/webclaw3-intro.md)

## License

MIT
