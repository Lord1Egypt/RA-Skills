<!--
FAQ.md - Scaffold Frequently Asked Questions

WHAT THIS IS: Answers to the most common questions new Scaffold buyers hit.
If you're stuck on something, check here first.
-->

# FAQ.md - Common Questions

---

**"My agent forgot what we talked about yesterday."**

This is the memory system working as designed - AI agents don't have persistent memory between sessions. What *does* persist is whatever got written to files. If something important wasn't captured to MEMORY.md or a daily log during the session, it's gone. The fix: make sure your agent has the habit of writing to `memory/YYYY-MM-DD.md` during sessions. See AGENTS.md (Memory section) for the full rules.

---

**"My agent asks the same questions every session."**

Two causes: (1) The first-session setup wasn't completed - run through `FIRST-SESSION.md` to fill in USER.md, IDENTITY.md, and MEMORY.md properly. (2) The agent isn't reading its files at startup - check AGENTS.md, the "Every Session" section should have 5 startup steps. If your agent skips them, remind it explicitly: *"Read your startup files before we begin."*

---

**"How do I know if my agent is actually doing anything during heartbeats?"**

Check `memory/YYYY-MM-DD.md` (today's daily log) - your agent should be logging heartbeat activity there. You can also check `memory/heartbeat-state.json` to see timestamps of last checks. If there's nothing in the logs, your agent is probably replying HEARTBEAT_OK without doing any real work. Fix: tell it explicitly what to check in `HEARTBEAT.md`.

---

**"Can I use a different AI provider?"**

Yes - Scaffold is provider-agnostic. OpenClaw supports Anthropic, OpenAI, Google, Groq, Mistral, DeepSeek, and local models via Ollama. See `MULTI-MODEL-ROUTING.md` for the full routing strategy and per-provider notes. Run `openclaw models list` to see exactly what's available in your setup.

---

**"What's the difference between SOUL.md and AGENTS.md?"**

SOUL.md is character - who the agent *is*: personality, principles, how it communicates. AGENTS.md is protocol - how the agent *operates*: delegation rules, memory hygiene, safety limits. Think of SOUL.md as the person and AGENTS.md as the job description. Change SOUL.md to adjust personality; change AGENTS.md to adjust behavior. See `DECISIONS.md` for the full rationale.

---

**"My API costs seem high - how do I reduce them?"**

The biggest lever is model routing. If your heartbeat is running on a premium model, switch it to a Tier 1 model - same output for routine checks, ~$11/month savings. See `MULTI-MODEL-ROUTING.md` TL;DR (first section) for the quick wins. Also check `MEMORY.md` line count - if it's over 80 lines, bloated context is inflating every API call.

---

**"How do I add new skills?"**

Skills extend what your agent can do (weather, TTS, web search, etc.). Install via ClawhHub: `clawhub install [skill-name]`. Your agent can also search for skills: *"Search ClawhHub for a skill that does X."* See OpenClaw docs for the full skills system. The Scaffold package itself is a skill available on ClawhHub at `scaffold-workspace`.

---

**"Is my personal data safe?"**

Scaffold is local-first by default - your workspace files live on your machine, not a cloud server. The only data that leaves your machine is what gets sent to AI model APIs (Anthropic, OpenAI, etc.) in the context of each request. No Scaffold infrastructure sees your data. If you're on a VPS, you own that server. Standard hygiene: don't store credentials in workspace files, use `.gitignore` if you push to a repo, and review OpenClaw's security docs.

---

**"Something broke and I don't know where to start."**

Check in this order: (1) `memory/active-tasks.md` - is there a known issue logged? (2) Today's daily log `memory/YYYY-MM-DD.md` - any error patterns? (3) `openclaw gateway status` - is the gateway running? (4) SETUP-GUIDE.md Section 9 (Common Mistakes) - is your issue on the list? Still stuck: open an issue on the GitHub repo at github.com/scaffoldworkspace.

---

**"Does Scaffold increase my API costs?"**

Honest answer: a little, offset by a lot.

The behavioral files (AGENTS.md, SOUL.md, HOOKS.md, etc.) load as context every session - roughly 3,000–5,000 extra tokens of overhead. The heartbeat fires every 60 minutes, adding sessions that otherwise wouldn't exist. Ballpark: $3–5/month in infrastructure overhead.

What Scaffold saves: the model routing in `MULTI-MODEL-ROUTING.md` routes cheap routine work (heartbeats, briefings, grocery lists, cron jobs) to Tier 1 models instead of your expensive default model. That's roughly a 10x cost reduction on those tasks. Annual savings for a typical setup: $480–660/year.

Net: a few dollars a month in overhead, a few hundred a year in savings.

---

**"Is Scaffold responsible for actions my agent takes?"**

Scaffold provides structure, guardrails, and best practices. What access you grant your agent and how you configure it is your call. Start Conservative if you're unsure - that's what it's there for.

---

*More questions? Open an issue at github.com/scaffoldworkspace.*
