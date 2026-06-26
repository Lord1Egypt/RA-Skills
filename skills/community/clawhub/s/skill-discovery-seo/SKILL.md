---
name: skill-discovery-seo
description: Improve a skill package so AI agents can find, select, and trust it across registries and ecosystems, including Codex, Claude-style agents, OpenClaw, and other skill-based tools. Use when creating, renaming, packaging, publishing, or refining a skill; writing metadata, names, descriptions, tags, listings, or example prompts; or trying to improve skill discoverability, skill SEO, trigger accuracy, semantic matching, and install or selection confidence.
---

# Skill Discovery SEO

## Overview

Improve a skill's discoverability for both humans and AI agents. Focus on triggerable names, dense metadata, realistic example prompts, clear scope, and packaging decisions that help registries and meta-skills choose the right skill reliably.

Load [references/discoverability-guide.md](references/discoverability-guide.md) before rewriting metadata or publish copy.

## Workflow

### 1. Identify the discovery surface

Check which fields the registry or agent ecosystem will likely index:
- skill `name`
- frontmatter `description`
- `display_name`
- short description
- default prompt
- tags or categories
- example prompts
- listing copy or repository summary

If the platform is unknown, assume most systems use a mix of exact text match, semantic retrieval, and usage or trust signals.

### 2. Tighten the trigger language

Rewrite the discovery fields so they answer four questions fast:
- what domain is this for
- what job does it do
- what inputs does it accept
- what output or decision does it produce

Prefer literal wording over branding, slogans, or clever titles.

### 3. Expand query coverage without bloating

Include the main phrases a user or agent would search for:
- primary nouns such as platform, artifact, or file type
- major verbs such as review, check, create, revise, deploy, or analyze
- important synonyms such as policy and compliance, or caption and script
- edge-case phrases only if the skill truly handles them

Do not keyword-stuff. Add only terms that improve routing accuracy.

### 4. Check trust and scope

Make sure the skill:
- has a narrow, believable scope
- states boundaries clearly
- promises outputs it can actually deliver
- avoids agent-specific assumptions unless truly required

If the skill claims too much, narrow it until another agent could select it confidently.

### 5. Produce a publish-ready pack

Return:
- recommended skill name
- frontmatter description
- `display_name`
- short description
- default prompt
- optional tags
- 3 to 8 realistic example prompts
- one short note on what not to claim in the listing

## Output Rules

- Keep names literal, ASCII-safe, and easy to type.
- Put the highest-signal trigger terms early in the description.
- Match the wording users would naturally use, not internal jargon.
- Keep agent-specific wording out of general-purpose skills unless the skill is actually tied to one ecosystem.
- Prefer one strong promise over many weak ones.
