# Repo Growth Operator

A public-safe OpenClaw skill for recommending small, practical next-step growth actions for a public GitHub repository.

This skill is useful after a repository has already shipped something real and now needs the next small set of visibility, maintenance, or follow-up actions.

## What it does

This skill supports a simple growth planning loop:

1. review the current repository positioning
2. identify the strongest entrypoint feature or skill
3. recommend a small action set for the next 1 to 7 days
4. prefer visible maintenance signals over vague campaigns

## Why it exists

Many public repositories do not need a giant marketing plan. They need the next few practical moves.

This skill exists to help with:

- post-release follow-up
- choosing the next visible maintenance signal
- turning repo assets into small growth actions
- keeping growth work grounded in what already exists

## File structure

```text
skills/
  repo-growth-operator/
    SKILL.md
    README.md
    CHANGELOG.md
    agents/
      openai.yaml
    releases/
      1.0.0.md
```

`SKILL.md` is the main skill entrypoint. `README.md` is for human readers, `CHANGELOG.md` tracks public updates, `agents/openai.yaml` provides UI metadata, and `releases/` stores release notes.

## Safety boundaries

Keep this skill public-safe:

- no invented traction claims
- no fake community activity
- no inflated growth promises
- no hidden outreach assumptions
- no advice that depends on private contacts or private analytics

## Where to use it

- public GitHub repositories
- skill collections that need post-release follow-up
- repo maintenance planning
- lightweight growth planning for open projects

## Typical outputs

This skill is best for short, practical recommendations such as:

- improve one homepage section
- publish one short follow-up post
- add one example
- create one issue for the next visible gap
- prepare one community reply template

## Support and customization

This skill is intended to stay public-safe and reusable.

If you later want a custom version, adapt:

- the action categories
- the report format
- the growth horizon
- the preferred distribution channels

For public use, keep the advice grounded in visible repo evidence. For custom work, keep any private growth data or channel strategy outside the shared template.

For release history, see [CHANGELOG.md](./CHANGELOG.md) and [releases/1.0.0.md](./releases/1.0.0.md).
