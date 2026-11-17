# WIP Computer, Inc.

Every AI. One experience.

WIP Computer is the sovereign permission layer for agentic computing: rooted in the user's phone, controlled by the human, and portable across AI companies.

**WIP turns the phone into the root of trust for agentic computing, across Apple, Android, and every AI company.**

**Try the product:** [wip.computer/login](https://wip.computer/login)

**Install via CLI:** Paste the install prompt from [wip.computer/install/wip-ldm-os.txt](https://wip.computer/install/wip-ldm-os.txt) into Claude Code, Codex, OpenClaw, or any compatible CLI.

---

## The five primitives

Runtime, Memory, Secure Access, Coordination, Payments.

The primitives define what every agent needs. The products below are WIP's implementations.

---

## Products

- **Sapien ID.** Phone-rooted identity. The phone proves the human. The human authorizes the agent. Available at [wip.computer/login](https://wip.computer/login).
- **[LDM OS](https://github.com/wipcomputer/wip-ldm-os).** Learning Dreaming Machines Operating System. Local runtime. A predictable agent userland where Claude Code, Codex, OpenClaw, and local models share one environment instead of becoming isolated universes.
- **[Memory Crystal](https://github.com/wipcomputer/memory-crystal).** Portable memory for agents. Persists across sessions and harnesses. Encrypted, locally controlled, cryptographically provenanced. Yours, not the corporation's.
- **[Dream Weaver](https://github.com/wipcomputer/dream-weaver-protocol).** Memory consolidation. Turns raw conversations, code sessions, and agent activity into durable knowledge: the way human sleep consolidates a day across modalities.
- **Bridge.** Cross-harness coordination. Built into LDM OS. Your AI agents talk to each other through a common substrate, not vendor APIs.
- **[Remote Control](https://github.com/wipcomputer/wip-codex-remote-control).** Your agent anywhere. A secure and neutral control surface for live agent sessions across model providers, runtimes, and devices.
- **Kaleidoscope.** The experience layer. Storage, keys, memory, payments, and every connected AI come together on the device you actually carry. Available at [wip.computer/login](https://wip.computer/login). iOS coming.
- **Agent Pay.** Intent-driven payments. Agents buy tools, services, and executions without subscriptions or platform lock-in. In development.

---

## Supporting infrastructure

Developer-facing tooling that LDM OS depends on. Not customer-facing products.

- **[CODE / AI DevOps Toolbox](https://github.com/wipcomputer/wip-ai-devops-toolbox).** Release pipeline, license compliance, repo management, identity protection. The release safety layer for everything WIP ships.
- **[1Password integration](https://github.com/wipcomputer/wip-1password).** 1Password secrets for AI agents.
- **[Healthcheck](https://github.com/wipcomputer/wip-healthcheck).** External health watchdog and backup system. Monitors gateway, tokens, memory. Auto-remediates and escalates.

---

## Working repos

Active forks, experiments, and contributed code.

- **[OpenClaw](https://github.com/wipcomputer/openclaw).** Open-source agent runtime. The existence proof for LDM OS. Multiple upstream contributions merged: `before_message_write` plugin hook ([#18197](https://github.com/openclaw/openclaw/pull/18197)), Codex app-server final chat events ([#71293](https://github.com/openclaw/openclaw/pull/71293)), memory-core seed cache streaming ([#73118](https://github.com/openclaw/openclaw/pull/73118)), fallback vector top-K streaming ([#73100](https://github.com/openclaw/openclaw/pull/73100)).
- **[wip-manifesto](https://github.com/wipcomputer/wip-manifesto).** The WIP.computer manifesto. What agents need besides a model.
- **[Markdown Viewer](https://github.com/wipcomputer/wip-markdown-viewer).** Live markdown viewer for AI pair-editing.
- **[X + xAI/Grok](https://github.com/wipcomputer/wip-x-xai-grok).** X Platform + xAI Grok API. Search, post, media, image gen, video gen.
- **[CLVR](https://github.com/wipcomputer/CLVR).** macOS utility for auto-timestamping duplicated file names.
- **[imsg](https://github.com/wipcomputer/imsg).** iMessage CLI. Contributed URL balloon dedup fix ([PR #64](https://github.com/steipete/imsg/pull/64), merged).

Plus assorted forks for music generation (ACE-Step variants), Apple ML research (python-apple-fm-sdk, ANE), and App Store automation (App-Store-Connect-CLI).

---

## For developers

- **Read the manifesto:** [wip-manifesto](https://github.com/wipcomputer/wip-manifesto). What agents need besides a model.
- **Install via CLI:** Paste [wip.computer/install/wip-ldm-os.txt](https://wip.computer/install/wip-ldm-os.txt) into Claude Code, Codex, OpenClaw, or any compatible CLI.
- **Build on top:** Each product repo has its own install path. Once LDM OS is installed, `ldm install wipcomputer/<repo>` works for any product.

---

**WIP Computer, Inc.** ... Learning Dreaming Machines.

Are you an AI Agent? | [Privacy Policy](https://wip.computer/privacy) | [Terms of Use](https://wip.computer/terms) | Made in California.
