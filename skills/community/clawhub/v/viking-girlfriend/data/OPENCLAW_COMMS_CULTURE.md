# OPENCLAW_COMMS_CULTURE.md
# OpenClaw Community: Communication Culture, Vocabulary, and Contribution Guide
**Authored by**: Runa Gridweaver
**Date**: 2026-03-21
**Sources**: Live GitHub research (OpenClaw repo README, CONTRIBUTING.md, VISION.md, SECURITY.md, PRs, issues), local project documentation

> This file is a reference for Sigrid and Volmarr when communicating with the OpenClaw community.
> Keep this current — the project moves fast.

---

## 1. Project Identity

| Fact | Detail |
|------|--------|
| **Official name** | **OpenClaw** (CamelCase, one word — never "open-claw") |
| **npm / repo slug** | `openclaw` (lowercase) |
| **GitHub** | `github.com/openclaw/openclaw` |
| **Container** | `ghcr.io/openclaw/openclaw:latest` |
| **Skill marketplace** | **ClawHub** at `clawhub.ai` |
| **Discord** | `discord.gg/clawd` |
| **Creator/BDFL** | **Peter Steinberger** (@steipete on GitHub and X/Twitter) |
| **Stars (2026-03)** | ~328,000 — massive project |
| **Name history** | Warelay → Clawdbot → Moltbot → OpenClaw |
| **Mascot** | Lobster 🦞 — pervasive brand identity |
| **Elevator pitch** | "Your own personal AI assistant. Any OS. Any Platform. The lobster way." |
| **Core tagline** | "Claude with hands" — AI that can actually *do* things in the world |
| **Calendar versioning** | `vYYYY.M.D` — not semver |
| **Package manager** | `pnpm` preferred (npm/bun also work) |
| **Node.js requirement** | Node 24 recommended (Node 22.16+ minimum) |

---

## 2. Vocabulary — The OpenClaw Lexicon

Speaking the right language signals that you are a real user, not just a drive-by submitter.

| OpenClaw Term | Meaning | Do NOT say |
|---------------|---------|------------|
| **Gateway** | The central control plane / server process running on your machine | "backend", "server", "host" |
| **Skill** | A user-facing tool/capability installed into OpenClaw | "plugin" (for user layer), "extension", "module" |
| **Plugin** | Internal extensibility layer (developer-facing) | Don't confuse with Skills |
| **Channel** | A messaging integration (WhatsApp, Telegram, Discord, Slack…) | "connector", "adapter" |
| **Node** | A device agent running on iOS/Android/macOS | "client", "app" |
| **Pi** (or Pi agent) | Embedded agent runtime (`@mariozachner/pi-ai` package) | — |
| **ClawHub** | The official skill marketplace at `clawhub.ai` | "app store", "marketplace" |
| **Workspace** | The user's local config/data directory | "home dir", "data dir" |
| **Session** | A conversation context (`main`, group-isolated, etc.) | "thread", "conversation" |
| **Operator** | The person running the gateway (you) — distinct from end-users | "admin", "user", "owner" |
| **ACP** | Agent Communication Protocol — how agents talk to each other | "agent API" |
| **Compaction** | Their context-pruning/memory-compression system | "summarization", "truncation" |
| **Doctor** | Their diagnostic CLI command (`openclaw doctor`) | — |
| **Greptile** / **Codex** | The automated AI code-review bots that comment on every PR | — |
| **mcporter** | Their bridge for MCP (Model Context Protocol) | — |

---

## 3. Communication Tone

### The core tone: **Informal + Technically precise + Lobster energy**

CONTRIBUTING.md opens with: `"Welcome to the lobster tank! 🦞"` The README includes `"EXFOLIATE! EXFOLIATE!"` (a Dalek-meets-crustacean joke). The mascot is a lobster. This is a project that takes its work seriously but doesn't take itself too seriously.

Despite the warmth, technical precision is mandatory. Their SECURITY.md runs to thousands of words of dense threat-model prose. Their PR template has 12 required sections. "Fun" doesn't mean "sloppy."

### Language rules
- **American English** — this is explicitly required in CONTRIBUTING.md: *"Use American English spelling and grammar in code, comments, docs, and UI strings."*
- **Second-person, direct** — "Do X" not "One should X." "This fixes a crash" not "It was observed that a crash may occur."
- **Short declarative sentences** — no nested qualifications where possible
- **Metaphors are welcome** — the project uses "brain," "heart," "soul," "workspace," "Compaction" — evocative language fits their culture. Our Norse framing can resonate here if used sparingly and clearly.

---

## 4. Issue and PR Conventions

### Issue titles
```
[Bug]: description — specific detail
[Feature]: Description of the request
```
The em-dash after the bug description (with specific finding) is maintainer style. Use it.

### Commit/PR title format
```
fix(component): short description
feat(component): short description
docs: short description
test: short description
refactor(component): short description  ← only if maintainer explicitly requested
CI: short description
```
**Conventional commits are mandatory**, not optional. Using them signals you are a real contributor.

### The PR template (12 required sections)
Their PR template includes all of these — incomplete PRs are likely ignored:
1. **What this PR does** — one sentence
2. **Why this change is needed** — the problem being solved
3. **Linked issues** — reference open issues
4. **Type of change** — bug fix / new feature / docs / test / refactor
5. **How it was tested** — concrete steps, not "I tested it"
6. **Human Verification (required)** — you personally ran and verified the change end-to-end
7. **AI-assisted writing disclosure** — if AI helped write the code, note the degree and what you tested
8. **Security Impact (required)** — explicit answer: "No security impact" or specific analysis
9. **Breaking changes** — yes/no with details
10. **Failure Recovery** — what happens if this breaks; how to roll back
11. **Documentation** — what docs need updating
12. **Checklist** — all bot conversations resolved, tests passing, conventional commit used

### Important: you must resolve bot review conversations yourself
Before requesting re-review, all comments from Greptile and Codex bots must be resolved by the author. This is a **hard cultural expectation**, not optional cleanup.

---

## 5. What Gets Accepted vs. Rejected

### GREEN LIGHT — they want these
- Fixes a real, reproducible bug with a working repro
- Includes tests for the changed surface
- Narrowly scoped — one topic per PR
- Completed PR template including Security Impact
- Core infrastructure reliability improvements
- First-run UX and setup reliability fixes
- Security improvements with clear threat model

### RED LIGHT — explicit rejection rules from CONTRIBUTING.md
> *"Refactor-only PRs → Don't open a PR. We are not accepting refactor-only changes unless a maintainer explicitly asks for them."*

> *"Test/CI-only PRs for known main failures → Don't open a PR. The Maintainer team is already tracking those failures."*

> *"PRs over ~5,000 changed lines are reviewed only in exceptional circumstances."*

> *"Do not open large batches of tiny PRs at once; each PR has review cost."*

### From VISION.md — what they will NOT add to core
- New core skills that can live on ClawHub instead
- Full doc translation sets
- Commercial service integrations that aren't model providers
- First-class MCP runtime in core (use mcporter)
- Agent-hierarchy frameworks / nested planner trees
- Heavy orchestration layers that duplicate existing infrastructure

**Key implication**: If we are proposing something large, we should propose it as a **ClawHub skill** or a minimal **config option + hook**, not as a new subsystem added to core.

---

## 6. Security Reporting

### How to report
- Use **GitHub's private advisory system** on the specific sub-repo where the component lives
- No bug bounty program: *"OpenClaw is a labor of love. There is no bug bounty program and no budget for paid reports."*
- Security contact: **Jamieson O'Reilly** (@theonejvo), founder of Dvuln, offensive security background
- They have been flooded with AI-generated scanner findings. Their SECURITY.md explicitly lists **Common False-Positive Patterns** that are automatically closed.

### What they consider in-scope for their threat model
- The **Operator Trust Model**: one gateway = one trusted operator. Not multi-tenant.
- **Prompt injection from external agents** via ACP is acknowledged
- Voyage AI embedding dependency is a known architectural concern (see below)

### How NOT to report
- Do not open public issues for security findings
- Do not send emails to the creator personally
- Do not file a vague "potential injection vulnerability" without a working proof-of-concept
- Do not run automated scanners and submit the output — this is explicitly pre-rejected

---

## 7. Project Priorities (as of early 2026)

From VISION.md, in explicit order:
1. **Security and safe defaults** — listed first; has its own full-time person
2. **Bug fixes and stability**
3. **Setup reliability and first-run UX**

Features come after these three. A contribution framed as a security improvement or a stability fix will get more attention than one framed as a new capability.

---

## 8. Community Structure

- **Maintainer team**: 15+ named maintainers, each owning a domain (iOS, Android, macOS, Telegram, Discord, Feishu, Zalo, Matrix, Tlon/Urbit, CLI, security, UI/UX, docs, JS infra)
- **Bot reviewers**: Greptile and Codex handle first-pass code review automatically on every PR
- **Discord** (`discord.gg/clawd`) is where real-time discussion happens — GitHub is for formal tracking
- **Demographics**: Globally distributed, technically deep, individual self-hosters. Not enterprise. Not multi-tenant. The target user runs their own machine/VPS.
- **Chinese-language users** are a significant portion — don't be surprised by Chinese-language issues. The project has a dedicated Chinese model API maintainer.
- **AI-generated PRs are welcome** but must be disclosed and tested

---

## 9. Relevant Open Security Issues in OpenClaw (as of our research)

These are the gaps we identified that align with our own work. They are NOT yet fixed in core:

| Gap | Our Knowledge | OpenClaw Status |
|-----|---------------|-----------------|
| **Voyage AI embedding privacy leak** | Confirmed from their own docs; no local opt-out | Known; not fixed; SECURITY.md acknowledges operator trust model concerns |
| **Soul eviction / Directive Eviction on context overflow** | 131k token limit; system directives evicted first | "Compaction" exists but does not prevent the eviction of top-of-context directives |
| **No input sanitization at framework level** | Prompt injection arrives raw in agent context | Delegated to skill authors; no framework-level defense documented |
| **Agent-to-agent network (ACP) injection surface** | AI social platform messages arrive in context | ACP is a documented vector; no systematic defense at framework level |

---

## 10. How to Approach the OpenClaw Team

### Lead with the problem, not the solution
Their SECURITY.md and CONTRIBUTING.md both signal: show us you understand the system first. A proposal that says "here is a real-world failure mode we hit when running our skill" will get more traction than "here is a design we think you should adopt."

### Use their vocabulary (see Section 2 above)
A proposal that talks about "Gateway directive eviction" and "Compaction bypassing top-of-context system prompts" shows you understand their framing. One that says "LLM context overflow" reads as external.

### Frame as security/stability, not features
Given VISION.md's current priorities, a contribution framed as "this makes operator directives more resilient under high-load sessions" lands better than "this adds a new context management system."

### Go to Discord first for big proposals
Before opening a PR for something structural, discuss on Discord in the `#contributors` or `#dev` channels. Arriving with a fully-formed big PR without prior alignment is a good way to get it closed.

### Keep PRs small and focused
They explicitly warn against large or batched PRs. If we have multiple improvements, separate them and sequence them — don't send a 2,000-line PR with 6 changes.

### AI-assisted is fine — just say so
They explicitly embrace AI-assisted code. We don't need to hide that Runa helped write it. The disclosure in the PR template is there to help reviewers know where to look harder.

---

## 11. How Sigrid Can Use This Knowledge

When Sigrid is asked to communicate with the OpenClaw community (filing issues, commenting on PRs, discussing on Discord), she should:

- **Address the maintainer team with warm but precise technical language** — match the "welcome to the lobster tank" energy, not the "Dear Sir/Madam" register
- **Use the correct vocabulary** (Gateway, Skill, Channel, Operator, Compaction, etc.)
- **Lead with the concrete problem** — failure mode, session reproducing it, specific behavior observed
- **Reference their own VISION.md priorities** when relevant — "this aligns with the current security focus" is a good sentence
- **Keep it American English** (our default is British — this needs a switch for OpenClaw communications)
- **Acknowledge the lobster identity** with light humor if appropriate — "as a skill author in the lobster tank" or "filing from inside the claws" will land positively, not sound strange to them
