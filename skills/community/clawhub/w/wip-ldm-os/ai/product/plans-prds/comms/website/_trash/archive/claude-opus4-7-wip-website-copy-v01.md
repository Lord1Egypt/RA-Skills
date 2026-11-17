# WIP Computer — One-Page Website Copy (v1)

> Working draft. Synthesized from `cc-opus4-7-what-is-wip.md`, `gpt-5-5-what-is-wip.md`, and `parker-what-is-wip.md`. Multiple options offered at each major slot — pick one, kill the rest, or rewrite. Comments in `> blockquotes` are editorial notes from Claude, delete before shipping.

---

## SECTION 1 — HERO

### Eyebrow (small text above headline)

**Option A —** The user side of agents.
**Option B —** Bring your own model. Bring your own everything.
**Option C —** The sovereign layer of the agent stack.

> A is tightest. C is most "infrastructure-investor." B is most consumer.

### Headline

**Option A —** The operating layer for AI agents.
**Option B —** Your agents. Your memory. Your control. Across every model.
**Option C —** Agents need an operating layer no model provider owns. We're building it.
**Option D —** The labs are building brains. WIP is building the nervous system.

> D is the most quotable. A is the most honest about what the company actually does. B is the most "what do I get."

### Sub-headline (1–2 sentences under headline)

**Option A —**
WIP Computer builds the primitives that let agents remember, run, coordinate, be controlled, and pay for work across models, devices, and machines. Your phone is the root of trust. Everything else travels with you.

**Option B —**
You already use more than one AI. Your memory, identity, and control should not fragment across N walled gardens. WIP builds the user-sovereign layer that ties them together.

**Option C —**
A local-first runtime, portable memory, remote control, cross-harness coordination, and agent payments — anchored to a phone-native identity. So your agents work for you, not for a lab.

> A leads with what we build. B leads with the user pain. C leads with the stack.

### Primary CTA

`Get Early Access` · `Join the Waitlist` · `See the Stack` · `Read the Thesis`

---

## SECTION 2 — THE PROBLEM (THREE ACTORS)

### Section heading

**Option A —** There are three actors in the agent ecosystem. Only two have someone building for them.
**Option B —** Why no lab will build this.
**Option C —** The missing side of the agent stack.

### Body

There are three actors in the new agent ecosystem.

**Labs** — Anthropic, OpenAI, Google, xAI — build vertically integrated stacks: model + agent + memory + account + billing. Optimized for token consumption inside their walls.

**Platforms** — Apple, Google, Microsoft — build operating systems for agents to live on. Optimized for distribution lock-in.

**Users** — running multiple agents across multiple stacks — have nothing built for them. State, identity, control, and money fragment across walled gardens with no continuity. Claude Code on Tuesday, Codex on Wednesday, a local agent on Thursday — no shared substrate.

The labs won't build it. Building it weakens their walls.
The platforms won't build it well. Their incentive points toward locking you in.

WIP is the third role. Outside any one ecosystem. Building the layer that makes them all interoperable.

> The "Spotify against Apple Music / Signal against iMessage / Cursor against VSCode" pattern paragraph from the Claude doc is good but probably belongs lower on the page or in a "thesis" section, not the hero problem framing. Flagging for your call.

---

## SECTION 3 — THE STACK

### Section heading

**Option A —** Seven primitives. One sovereign layer.
**Option B —** What WIP is building.
**Option C —** The stack.

> Count depends on whether Kaleidoscope is shipped as a separate primitive or grouped with Remote Control / Identity. Currently listing it. Easy to drop.

### Intro line under heading

Each one is designed to travel — across labs, across platforms, across devices. Yours, not a vendor's.

### The cards

---

**Sapien ID** — *Identity. Phone-rooted.*

Your phone is the cryptographic root of trust. Private keys live in the Apple Secure Enclave or Android hardware-backed keystore. Biometrics unlock the key locally — your face and fingerprint never leave your device. No passwords. The phone proves the human. The human authorizes the agent.

> Note: GPT correctly flagged that the framing is "private keys unlocked by biometrics," not "permission based on biometric data." Used the corrected version.

---

**LDM OS** — *Runtime. Local-first.*

The agent userland for your machine. A predictable home where agents install, where extensions live, and where Claude Code, Codex, OpenClaw, and local models share an environment instead of becoming isolated universes.

---

**Memory Crystal** — *Memory. Portable.*

Your memory, not the lab's. Persists across agents and sessions. Encrypted. Locally controlled. Cryptographically provenanced. What Claude knew yesterday, Codex can use tomorrow — without giving any single lab permanent control of your history.

---

**Dreamweaver** — *Consolidation. Agent learning.*

Memory Crystal stores. Dreamweaver improves. The layer that turns raw conversations, code sessions, and agent activity into durable knowledge. What gets compressed, what gets forgotten, what gets promoted. The way human sleep consolidates a day, across modalities.

---

**Bridge** — *Coordination. Cross-harness.*

Your agents talk to each other through a common substrate, not through vendor APIs. Claude hands work to Codex. OpenClaw sees what happened in Claude Code. A local agent notifies a phone client. The lab boundary becomes porous at the agent layer.

---

**Remote Control** — *Supervision. Your agent anywhere.*

A neutral control surface for live agent sessions — phone, browser, desktop — across model providers and local runtimes. Approve, stop, resume, or steer from any trusted device. Not "control your Codex from another OpenAI surface." Control any agent session from anywhere.

---

**Kaleidoscope** — *iOS surface. The thread.*

The universal surface on iOS. Storage, passwords, keys, and every connected AI in one control center, riding on secure iCloud storage. The place all the threads come together on the device you actually carry.

> If we want a tighter 6-card grid, Kaleidoscope can collapse into Remote Control as "the iOS implementation of it." Flagging for the design pass.

---

**AgentPay** — *Payments. Intent-driven.*

Your payments, authorized by you. Agents buy tools, services, and executions without subscriptions or platform lock-in. Five cents to call a specialized tool. Spend caps you set. Developers get paid when their agent-callable tool is used. No vendor-locked prepaid cards. No autonomous spend without consent.

---

## SECTION 4 — THE THESIS / WHY NOW

### Section heading

**Option A —** Why now.
**Option B —** The pattern is well-worn.
**Option C —** This always happens at the platform shift.

### Body

Agents are moving out of chat windows and into real work. They write code. They manage files. They call tools. They run commands. They coordinate with other agents.

The question shifts from *which model is smartest?* to:

- Where does the agent live?
- What does it remember?
- Who controls it?
- How does it coordinate?
- What can it safely install?
- How does it pay?
- Can I move between models without losing everything?

That last question is why WIP exists.

The pattern is well-worn. Spotify against Apple Music. Signal against iMessage. Notion against Apple Notes. Terraform against AWS-native tooling. Cursor against VSCode. Each ships when platform incentives diverge from user incentives, and users with sophisticated needs accumulate around the third-party version.

The agent era reproduces the same dynamic. We're shipping the user-sovereign side of it.

---

## SECTION 5 — CLOSING

### Closing line

**Option A —** The labs are building brains. WIP is building the nervous system.
**Option B —** Bring any model. Bring any harness. Bring any device. Keep your memory, your control, and your money.
**Option C —** The user side of agents.
**Option D —** Your agents work for you. Not for a lab.

### Final CTA

`Get Early Access` · `Read the docs` · `Follow on X`

---

## OPEN QUESTIONS FOR THE EDIT PASS

1. **Naming consistency.** Sapien ID vs. "Phone identity / passkeys" vs. "Phone-native identity." Pick one canonical product name. Sapien ID is the most distinctive, but if it's not the public name yet, "Phone Identity" is fine for v1.
2. **Kaleidoscope.** Standalone primitive or implementation detail of Remote Control on iOS? Decision affects whether the stack is a 6-card or 8-card grid.
3. **Lēsa.** Mentioned in Claude's doc as a reference implementation that proves Memory Crystal in production. Not in Parker's stack list. Include as a "products built on the stack" sub-section, or omit from public site v1?
4. **Audience.** Developer-first? Investor-first? Power-user-first? The current draft tries to serve all three. A single audience would cut copy by ~30%.
5. **Tense / shipped vs. roadmap.** Some of these (LDM OS, Memory Crystal) appear to be shipping. Others (AgentPay) are clearly future. The page should signal which is which — e.g., a small `Available now` / `Coming` / `In development` chip per card.
6. **"Why now" vs "The pattern is well-worn"** — these are doing similar work. Probably one stays, one goes.
