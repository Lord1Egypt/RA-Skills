---
name: site-profile
description: Short alias for external-site-profile-learning. Use this when investigating, adding, validating, or debugging external website profiles for the 99idea Playwright browser demo.
license: Proprietary session artifact for local Copilot use
---

# Site profile skill

This is the short public alias for:

- `external-site-profile-learning`

Also available as simpler aliases:

- `profile`
- `站点配置`

Use this skill when you want to:

- add a new external site profile
- debug why a site works heuristically but fails under Gemini
- classify whether a site should be generic, blocked, special, or config-driven
- validate a site in both heuristic and Gemini modes

## Primary guidance

Follow the same workflow as the full skill:

1. probe the site
2. classify the UI pattern and failure mode
3. add a data-only profile when justified
4. validate heuristic and Gemini flows
5. keep special/rate-limited sites out of the default regression matrix
6. use grouped regression runs when debugging popup-heavy or heavy-page sites

## Key rules

- Prefer URL or title verification for external sites.
- Prefer exact selectors over broad selectors.
- If a profile exists, normalize generated `type` and `click` steps back to the profile selectors.
- Treat login walls, hidden inputs, duplicate controls, and anti-bot behavior as different problem types.
- Prefer grouped validation commands such as `validate:external:core`, `validate:external:popup`, and `validate:external:heavy` for targeted debugging.

## Quick invocation template

You do not need to use only `/site-profile`.

Reliable invocation patterns include:

1. `/site-profile`
2. `use the site-profile skill`
3. a natural-language request that clearly asks to turn an already-proven flow into a stable reusable profile

Use prompts like:

```text
Use /site-profile to turn this site into a stable external profile, then validate both heuristic and Gemini planning.
```

```text
使用 /site-profile 把这个网站沉淀成稳定 profile，并分别验证 heuristic 和 Gemini 两条链路。
```

```text
Please turn this already-working site flow into a stable reusable profile and validate both heuristic and Gemini modes.
```

## Output contract

The skill output should always include:

1. failure class or site class
2. exact selectors chosen and why
3. verification mode and expected signal
4. validation commands run (or planned)
5. final status: stable / blocked / special-case

## Pointer

For the full detailed playbook, also see:

- `skills/external-site-profile-learning/SKILL.md` in this repository
