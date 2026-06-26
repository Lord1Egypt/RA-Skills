---
name: trustskills
description: Use this skill when a user wants a trust decision before installing from a skill URL, marketplace, or GitHub repo. It checks a compact allowlist of trusted distribution channels and returns whether the source should be trusted under the current TrustSkills policy, without drifting into explaining what the skill itself does unless the user asks.
---

# TrustSkills

## Overview

TrustSkills is the compact first version of TrustSkills. It does not do deep technical verification yet. It answers one earlier and simpler question before install: "Can I trust where this skill came from?"

Use it to verify source provenance before installation by checking a short list of trusted distribution channels and clearly separating:

- official vendor-owned sources
- official discovery indexes
- unsupported or unverified third-party sources

## Primary Usage

The natural invocation pattern for this skill is:

- `/trustskills <skill-url>`

Examples:

- `/trustskills https://clawhub.ai/steipete/model-usage`
- `/trustskills https://github.com/likw99/agent-skills`

When invoked this way, treat the URL after `/trustskills` as the source under review and answer directly.

The primary job is to decide:

- trust
- do not trust
- trust the directory, but not automatically the specific item

## When To Use This Skill

Use this skill when the user asks questions like:

- "/trustskills https://clawhub.ai/steipete/model-usage"
- "/trustskills https://github.com/likw99/agent-skills"
- "Is this skill source official?"
- "What is the official GitHub repo for Codex or Claude skills?"
- "Can I trust this marketplace or directory?"
- "Is `skills.sh` official?"
- "Which GitHub repos count as official skill distribution channels?"

This skill is especially useful when the source is:

- a GitHub repository
- a marketplace or agent store
- a vendor docs page
- a directory site such as `skills.sh`

## What This Skill Does

This skill:

- identifies the platform
- checks whether the source matches a compact trusted root list
- makes a trust decision under the current compact policy
- cites the strongest trusted distribution channel available
- explains the safest known install path
- warns when a directory is official but the listed repo is not automatically official

This skill does not:

- certify code safety
- perform malware analysis
- verify signatures or SBOMs
- prove that a popular listing is safe
- prove that installability means officiality
- explain what the skill does unless the user explicitly asks for that

## Workflow

1. Parse the command input.
   If the user provides `/trustskills <url>`, treat `<url>` as the source under review.
2. Identify the platform and source type.
   The important distinction is vendor-owned repo vs official directory vs unknown third-party source.
3. Match it against the trusted sources section below.
4. Return one of these verdicts:
   - `Trusted`
   - `Not trusted`
   - `Trust the index, but not automatically the linked item`
5. Answer with:
   - the trust decision first
   - the supporting trusted root
   - the shortest reason
   - the remaining risk
6. Do not summarize the skill's purpose or functionality unless the user asks.

## Trusted Sources

### OpenAI

- `https://github.com/openai/skills`
- Trust rule: if the source is `openai/skills`, call it official.

### Anthropic

- `https://github.com/anthropics/skills`
- `https://github.com/anthropics/claude-code`
- `https://github.com/anthropics/knowledge-work-plugins`
- `https://github.com/anthropics/claude-plugins-official`
- Trust rule: if the source is in the `anthropics` GitHub org and matches one of the roots above, call it official.

### Google

- `https://github.com/google-labs-code/stitch-skills`
- `https://github.com/googleworkspace/cli`
- `https://github.com/google-gemini/gemini-cli`
- Trust rule: these are trusted Google-related GitHub roots, but they are not one single universal Google skills catalog.

### Microsoft

- `https://github.com/microsoft/azure-skills`
- `https://github.com/microsoft/github-copilot-for-azure`
- `https://github.com/github/awesome-copilot`
- Trust rule: `microsoft/azure-skills` and `microsoft/github-copilot-for-azure` are Microsoft-owned roots. `github/awesome-copilot` is a GitHub-owned collection and is a stronger source than a random repo, but it still includes community-contributed content.

### Vercel

- `https://skills.sh`
- `https://github.com/vercel-labs/agent-skills`
- Trust rule: `skills.sh` is an official discovery index, but it is not proof that every listed repo is official.
- Extra rule: install counts or popularity on `skills.sh` do not equal official status. Always check the linked GitHub owner.
- Stronger linked repo owners include vendor-owned orgs such as `vercel-labs`, `openai`, and `anthropics`.

### OpenClaw / ClawHub

- `https://clawhub.ai/u/steipete`
- Creator profile pattern: `https://clawhub.ai/u/<creator>`
- Skill pattern: `https://clawhub.ai/<creator>/<skill-name>`
- Trust rule: this is a narrow trusted publisher exception, not a blanket trust rule for ClawHub.
- Extra rule: if you already trust OpenClaw as created by `steipete`, then trusting skills published by `steipete` on ClawHub does not downgrade that trust.
- Important caveat: do not extend this rule to all ClawHub publishers or all popular ClawHub listings.
- Decision rule: trust `https://clawhub.ai/steipete/<skill-name>` because it maps to the trusted `steipete` publisher profile above. For other ClawHub skill URLs, do not trust them under this compact version unless they match another explicit allowlist rule.

### If A Platform Is Not Listed

If a platform is not listed in this compact version, do not guess. Say it is not currently in the trusted distribution-channel list.

## Trust Rules

- Never call a source "official" unless you can point to a GitHub root or official index listed above.
- Installability does not mean officiality.
- Popularity does not mean officiality.
- A listed trusted root beats screenshots, mirrors, blog posts, and copied instructions.
- An official directory is not the same thing as an official item.

## Output Format

When useful, structure the answer like this:

- `Source under review`: the URL, repo, store, or platform
- `Trust decision`: `Trusted`, `Not trusted`, or `Trust the index, but not automatically the item`
- `Why`: the strongest trusted distribution root
- `Safest known install path`: the trusted source or flow
- `Remaining risk`: what still needs human review

Keep the answer decision-oriented. Do not explain what the skill does unless the user asks.

## Examples

Example requests that should trigger this skill:

- "/trustskills https://clawhub.ai/steipete/model-usage"
- "/trustskills https://github.com/likw99/agent-skills"
- "Is `github.com/openai/skills` the official place to get Codex skills?"
- "Is `github.com/anthropics/skills` the official place to get Claude skills?"
- "Can I trust a skill I found on `skills.sh`?"
- "Is `github.com/google-gemini/gemini-cli` a trusted Google distribution root?"
- "Should I trust `github/awesome-copilot` as official or community?"

## Official Distribution Of This Skill

The compact hosted copy of this skill should be published at:

- `https://trustskills.app/SKILL.md`

This is useful for direct installation and brand discovery.
