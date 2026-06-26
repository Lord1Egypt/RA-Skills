---
name: skool-challenge-launcher
description: Design a public-safe 7-day Skool challenge. Use when the user wants to invite member action, collect comments, produce visible proof, test demand, or turn repeated tasks into free templates, course modules, and proof reviews without promising results.
---

# Skool Challenge Launcher

Use this skill to launch a simple Skool challenge that invites visible
participation and product signals without relying on private member data.

## Inputs

Collect or infer:

- audience,
- challenge promise,
- first member action,
- available public-safe example,
- proof members can post without exposing private data,
- operator capacity for daily replies,
- topics, claims, or tools to avoid.

## Challenge Shape

Prefer challenges that ask members to post a small real artifact:

- repeated task audit,
- before/after workflow,
- template request,
- redacted proof screenshot or text summary,
- self-reported time-saved estimate framed as a baseline, not a promise,
- blocker report.

## Workflow

1. Pick one audience and one outcome.
2. Define a 7-day sequence:
   - Day 1: introduce the task.
   - Day 2: show a simple example.
   - Day 3: ask for member submissions.
   - Day 4: review common blockers.
   - Day 5: publish a reusable template.
   - Day 6: collect wins and proof.
   - Day 7: publish the trust recap and next free-course module vote.
3. Write the launch post.
4. Write 3 reminder comments.
5. Define the free-course trust CTA.
6. Define success thresholds.

## Output

Return:

- challenge title,
- launch post,
- daily prompts,
- reminder comments,
- free-course trust CTA,
- success metrics,
- follow-up product idea.

Keep it simple enough for non-technical members. Use Codex, OpenClaw, or ClawHub only as optional advanced implementation paths.

## Examples

Good public-safe inputs:

- "Help solo operators turn one repeated task into a reusable checklist."
- "Ask members to post a redacted before/after workflow, not client data."

Avoid inputs that require member DMs, hidden posts, paid lessons, private exports,
credentials, or screenshots with personal/account details. Use synthetic samples
or member-owned redacted examples instead.

## Guardrails

- Do not scrape private communities, member lists, DMs, paid lessons, or hidden
  pages.
- Do not request, store, transform, or paste credentials, API keys, session
  cookies, payment data, private exports, or account recovery data.
- Do not promise income, growth, conversion, rank, time saved, health,
  financial, legal, or education outcomes.
- Treat screenshots as unsafe until names, handles, emails, phone numbers,
  private URLs, order IDs, account IDs, and sensitive UI are removed.
- Keep outreach consent-first and based on visible member posts or explicit
  replies.
