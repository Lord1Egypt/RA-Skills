# Skill Discoverability Guide

Use this guide when improving a skill for any agent ecosystem or registry.

## Core model

Most skill systems discover skills through some combination of:

- exact-name match
- keyword match on metadata
- semantic retrieval from descriptions and examples
- trust signals such as popularity, quality, or past success

Design for all four. Do not rely on only one.

## The main discovery fields

Usually worth optimizing first:

- `name`
- frontmatter `description`
- `display_name`
- short description
- default prompt
- tags or categories
- example prompts

## Naming rules

Good names are:

- literal
- short
- scoped
- easy to type
- ASCII-safe

Prefer:

- platform or domain
- artifact or object
- action or outcome

Examples:

- `tiktok-content-creation-compliance`
- `render-deploy`
- `linear-issue-management`

Avoid:

- vague branding
- jokes
- clever metaphors
- names that hide the platform or task

## Description rules

The frontmatter description is often the most important trigger surface.

A good description usually contains:

- who the skill is for
- what the skill does
- what artifacts it accepts
- what output or decision it produces
- the contexts that should trigger it

Put the strongest trigger terms in the first sentence.

## Query coverage

Include:

- primary terms: the exact nouns users search for
- action terms: review, create, fix, deploy, analyze, compare
- synonyms: policy and compliance, script and caption, deploy and publish
- edge cases: only if they are truly supported

Do not stuff unrelated keywords just to broaden reach. Broader is not better if routing quality drops.

## Example prompts

Example prompts help both humans and agent retrieval systems understand the intended use cases.

Good example prompts:

- match realistic user wording
- cover the main artifacts
- show the edge cases the skill truly handles
- stay short enough to scan

Example prompt pattern:

- `Check whether this TikTok Shop video is compliant`
- `Compare this exported ad against the product listing image`
- `Rewrite this skill description so agents can find it more easily`

## Scope discipline

Discoverability improves when scope is believable.

Prefer:

- one job done well
- one output shape
- one clear domain

Avoid:

- claiming the skill handles every platform
- mixing unrelated tasks in one skill
- promising legal, security, or policy certainty when the skill only gives guidance

## Trust signals

Even when ranking is mostly semantic, agents and registries often favor skills that look reliable.

Improve trust by:

- using official or primary sources when the skill depends on policy or APIs
- stating boundaries clearly
- defining output format
- keeping packaging clean
- avoiding stale or contradictory metadata

## Publish checklist

Before publishing, check:

- name is literal and searchable
- description includes domain, task, inputs, and outputs
- short description is concise and specific
- default prompt demonstrates the real use case
- examples cover common and edge-case requests
- no agent-locked wording appears unless required
- files and metadata agree with each other
- the skill validates cleanly

## Anti-patterns

- name is catchy but non-descriptive
- description explains philosophy instead of triggers
- metadata says one thing and SKILL.md says another
- examples are too generic to guide routing
- scope is so broad that another agent cannot trust the match
- listing promises platform support the skill does not actually have
