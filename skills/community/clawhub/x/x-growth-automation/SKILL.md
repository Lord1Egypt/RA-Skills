---
name: x-growth-automation
description: Set up a reusable X/Twitter growth automation system with OpenClaw, Bird CLI, X API, optional source branching, optional community CTA, dry-run/live rollout, anti-repetition controls, and niche-specific posting policy. Use when a user wants to build, clone, publish, or customize an autonomous X growth workflow, especially if they ask to install the system from GitHub/ClawHub, configure cadence (including high-volume modes like 10/day), define niches, add/disable reply automation, localize for a specific language, or connect external editorial feeds into X.
---

# X Growth Automation

Build a **separate, reusable X automation project** for the user. Do not assume their current production project should be modified. Prefer creating a fresh folder unless they explicitly target an existing repo.

## Core workflow

1. **Ask setup questions first** using `references/setup-questionnaire.md`.
2. **Choose safe rollout mode** using `references/rollout-modes.md`.
3. **Scaffold a clean project** with `scripts/scaffold_x_growth_project.py`.
4. **Fill configs** based on the user's answers.
5. **Keep publish disabled by default** unless the user explicitly asks for live publishing.
6. **If enabling live publish**, keep caps, slot scheduling, and fallback rules explicit.

## What this skill should help build

A reusable X automation system with these layers:
- discovery via Bird CLI
- selection/scoring layer
- draft generation layer
- optional LLM-first approval layer
- optional source branching from an external editorial feed
- optional community CTA logic
- slot-based publishing via X API
- dry-run-first rollout

## Non-negotiable safety defaults

- Create the project in a **new folder** unless the user clearly says otherwise.
- Treat Bird as **read/discovery first**.
- Treat X API as **write/publish layer**.
- Default new installs to **dry-run**.
- If the user wants aggressive automation, still keep daily/monthly caps in config.
- Never silently copy private tokens, links, handles, or niche assumptions from another project.
- Treat reply automation as a higher-risk lane than normal posts; disable by default unless explicitly requested.
- In live mode, require clear logging for posted / skipped / failed outcomes.
- Use idempotent slot keys that do not depend on mutable draft text (prevent same-source repost loops).
- Add anti-repetition guardrails (for example last-48h similarity checks + source de-dup).

## Ask these questions before scaffolding

Read `references/setup-questionnaire.md` and ask only the missing items.
Do not dump all questions at once if the user already answered some.

Minimum set to unblock setup:
- niche/topic focus
- posting language
- dry-run or live
- daily target range
- monthly hard cap
- Bird available?
- X API available?
- source branching wanted?
- community CTA wanted?

## After answers are clear

Run the scaffold script:

```bash
python3 scripts/scaffold_x_growth_project.py --path <target-dir> --profile-json '<json>'
```

The JSON may include fields like:
- `project_name`
- `language`
- `niche_summary`
- `daily_min`
- `daily_max`
- `monthly_cap`
- `community_enabled`
- `community_link`
- `reply_cta_enabled`
- `reply_cta_style`
- `source_branching_enabled`
- `source_branching_label`
- `bird_enabled`
- `x_api_enabled`
- `live_publish`

## Recommended setup behavior

### If user says “install this system for me”
- Ask the setup questions.
- Scaffold a fresh project.
- Fill the config files.
- Keep publish disabled unless they explicitly approve live mode.
- Explain where they should place credentials.

### If user says “can we adapt this to my niche?”
- Ask for niche, audience, tone, and content pillars.
- Update topic/search/watch-account config.
- Update crosspost/reply policy if needed.

### If user says “make it more aggressive”
- Increase cadence and caps explicitly.
- Keep hard caps documented.
- Confirm whether replies should include CTA or not.
- Do not remove quality gates unless asked.
- Keep reply-specific safeguards even in aggressive mode: target validation, skip-on-failure, and per-day caps.

### If user says “I want community integration”
- Ask whether the external community/feed is:
  - source-of-truth content feed
  - CTA destination only
  - both
- Configure source branching and reply CTA rules separately.
- Never assume the community platform is Telegram unless the user explicitly says so.

## File customization order

After scaffolding, customize in this order:
1. `config/publish-policy.json`
2. `config/publish-slots.json` (if slot-based cadence is used)
3. `config/topics.json`
4. `config/budget-policy.json`
5. `config/draft-diversity.json` (or equivalent prompt/diversity controls)
6. `.env.example`
7. `docs/operator-notes.md`
8. prompts if the user wants a distinct tone

## When to enable live mode

Enable live mode only when all of these are true:
- credentials are present
- the user explicitly wants live publish
- cadence/caps are set
- reply policy is defined
- source branching behavior is defined
- the user understands what will auto-post

## Publish strategy guidance

Use explicit profiles and encode them in config:

- **Conservative:** 2-5/day, reply lane optional, 0-2 core
- **Balanced:** 4-7/day, reply lane optional, 2-4 core
- **High-volume:** 10/day = 1 news crosspost + 1 special crosspost + 8 core posts

If the user chooses high-volume mode:
- keep monthly cap explicit
- disable reply lane unless there is a clear reason to keep it
- enforce anti-repetition guardrails (recent-post similarity + source de-dup)
- distribute core slots through the day (avoid burst clustering)

If the user wants a different mix, encode it in config rather than burying it in prose.

## Resources

### scripts/
- `scaffold_x_growth_project.py` creates a clean generic project scaffold.

### references/
- `setup-questionnaire.md` contains the installation interview.
- `rollout-modes.md` explains dry-run vs live rollout choices.
