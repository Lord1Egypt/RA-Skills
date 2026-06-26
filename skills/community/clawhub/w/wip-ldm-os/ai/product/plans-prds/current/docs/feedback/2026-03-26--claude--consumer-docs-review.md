# Claude Feedback: Consumer Docs Review

**Date:** 2026-03-26
**Source:** Claude (external review)
**Context:** Review of docs.wip.computer after full read of all pages

## What is working

- Voice is excellent. Direct, zero filler, respects the reader.
- "Your AIs" framing instead of "agents" is smart for target audience.
- Architecture page is the standout. Sovereignty principles, 1:1 rule, directory structure.
- Local-first page is sharp. Open core vs source-available vs local-first table is a clean kill shot.
- Install-via-paste-into-your-AI flow is genuinely novel as distribution mechanism.
- Licensing section is one of the better dual-license explanations in OSS docs.

## What needs work

### 1. Homepage undersells the product
The one-liner is vague. "You use Claude Code, GPT, OpenClaw...they don't share memory" setup should be on the homepage, not buried one click in.

### 2. Audience confusion
Docs oscillate between consumer and developer. Universal Installer and Interfaces pages are dev-facing but sit alongside consumer pages. Need "For Users" / "For Developers" split.

### 3. Redundancy
Bullet list (Personality, Memory, Ownership, Teamwork, Compatibility, Payments) appears verbatim on 3+ pages. Seven Ways table appears twice. DRY it up or vary the framing.

### 4. Agent Pay is a ghost
Listed as "Coming Soon" repeatedly with no dedicated page, no 402 model explanation. Either stub page or drop from feature lists until ready.

### 5. LUME page too thin
Says "evolving specification" and links out. Feels like a placeholder compared to every other feature page.

### 6. Skills and Apps section sparse
Nav links to it but needs more content or should fold into LDM OS section.

### 7. No positioning or comparison page
Someone discovering WIP doesn't know how it compares to MemGPT/Letta, LangGraph, or Claude built-in memory. A positioning page would do a lot of work.

### 8. Karpathy quote dependency
Strong anchor on Universal Installer page but framing collapses if tweet is deleted. Concept should stand on its own.

## Small things

- Bridge page mentions ACP-Client and ACP-Comm with no links or context
- ldm sessions is CC-specific but reads like a general command
- Licensing section is well-written

## Bottom line

"The substance is strong. The architecture is real and well-thought-out. The docs just need editorial tightening: a clearer homepage hook, audience segmentation, deduplication, and filling the placeholder gaps. Right now it reads like accurate internal documentation that got published rather than docs written for someone encountering WIP for the first time."
