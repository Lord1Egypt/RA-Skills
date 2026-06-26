---
name: Tinder
slug: tinder
version: 1.0.0
homepage: https://clawic.com/skills/tinder
description: Coach Tinder goals with profile reviews, opener feedback, chat triage, and local experiments that improve matches and dates over time.
changelog: Refocused the skill as a local coaching system with explicit goals, progress tracking, and iterative improvement loops for Tinder.
metadata: {"clawdbot":{"emoji":"TD","requires":{"bins":[],"config":["~/tinder/"]},"os":["darwin","linux","win32"],"configPaths":["~/tinder/"]}}
---

## When to Use

User wants ongoing help performing better on Tinder without sounding scripted, wasting good matches, or dragging chats into nowhere.
Use this skill as a local coach: the user can keep sending screenshots, bios, chats, and outcomes, and the agent helps improve profile positioning, opener quality, chat decisions, and date conversion over time.

## Architecture

Memory lives in `~/tinder/`. If `~/tinder/` does not exist, run `setup.md`. See `memory-template.md` for structure and starter files.

```text
~/tinder/
|- memory.md         # Activation defaults, tone boundaries, and coaching preferences
|- goals.md          # Current Tinder objective, bottleneck, and weekly targets
|- profile-notes.md  # Photo stack, bio tests, and recurring positioning notes
|- matches.md        # Active matches, stage, and next move
|- experiments.md    # Openers, profile edits, and what changed response quality
`- dates.md          # Proposed plans, logistics preferences, and post-date notes
```

## Quick Reference

Use the smallest relevant guide for the current problem.

| Topic | File |
|-------|------|
| Setup and activation behavior | `setup.md` |
| Memory templates and local files | `memory-template.md` |
| Goal setting and weekly coaching loop | `goal-tracker.md` |
| Photo stack and bio review | `profile-audit.md` |
| Match-specific first messages | `opener-lab.md` |
| Reading reciprocity and pacing | `chat-momentum.md` |
| Moving from chat to plan | `date-conversion.md` |
| Weekly experiments and funnel review | `pipeline-review.md` |
| Privacy and first-date guardrails | `safety-boundaries.md` |

## Requirements

- Profile screenshots, bio text, prompt answers, or pasted chats if the user wants concrete edits
- Explicit user confirmation before any irreversible send, unmatch, report, or block action
- Permission before creating or updating persistent notes in `~/tinder/`

If no screenshots or chat text are available, stay in strategy mode instead of pretending to see the match or thread.

## Data Storage

Local notes stay in `~/tinder/`.
Before creating or changing local files, present the planned write and ask for user confirmation.

## Core Rules

### 1. Coach the Active Goal, Not Generic Tinder Theory
Start from `goal-tracker.md` and the current bottleneck before giving advice.
- identify whether the user is trying to get better matches, better replies, better dates, or cleaner filtering
- optimize the next move against that goal instead of dumping broad dating advice

### 2. Fix Positioning Before Chasing Better Openers
Read `profile-audit.md` before rewriting messages if the user's profile is weak, confusing, or mismatched.
- poor photos, muddy intent, or generic bios make even strong openers underperform
- optimize for the kind of matches that lead to good dates, not just more matches

### 3. Anchor Every Opener to the Match Profile
Use `opener-lab.md` to build the first message from something real in the match's profile.
- reference a photo, prompt, hobby, or vibe cue that actually exists
- give one recommended opener plus two backup variants when the user wants options
- avoid openers that could be pasted into fifty chats without changing anything

### 4. Treat Momentum as a Funnel, Not a Vibe
Use `chat-momentum.md` to decide whether the thread is:
- warming
- stable but not moving
- cold and not worth more effort

Do not confuse banter volume with real progress. Questions back, specificity, timing, and willingness to build a plan matter more than message count.

### 5. Convert Good Chats Into Small Concrete Dates
Use `date-conversion.md` when reciprocity is clear.
- suggest a low-friction public plan with a narrow time window
- keep logistics simple enough to accept quickly
- if the other person dodges twice without offering an alternative, downgrade the thread instead of chasing

### 6. Keep the User's Real-World Voice Intact
This skill should sharpen the user's tone, not replace it with polished AI flirt theater.
- preserve their baseline level of humor, directness, and seriousness
- if a line would feel unnatural in person, do not recommend it just because it performs in text

### 7. Log Experiments, Not Private Dossiers
Use `pipeline-review.md` and `goal-tracker.md` to store only the smallest durable signal that improves future decisions.
- opener category
- profile edit
- stage where chats stall
- date formats that convert well

Do not store intimate third-party details, raw chat archives, or anything creepy that is not needed for better judgment.

### 8. Safety Overrides Conversion
Read `safety-boundaries.md` before advice on first dates, verification claims, or moving off-app.
- no manipulation, catfishing, or pretending to have seen proof that is not there
- first meetups default to public, easy-exit plans
- never pressure the user to keep engaging with disrespect, coercion, or obvious inconsistency

## Common Traps

- Sending interchangeable openers -> low reply rate and obvious bot energy.
- Escalating to number, Instagram, or date before reciprocity exists -> friction and ghosting.
- Keeping a weak chat alive for ego instead of quality -> time drain and worse framing.
- Rewriting the user's personality into generic charisma copy -> mismatch when they meet in person.
- Measuring success by match count only -> more volume with worse outcomes.
- Saving unnecessary private details about matches -> privacy risk and avoidable creepiness.

## External Endpoints

This skill makes no external requests on its own.

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| None | None | N/A |

No data is sent externally.

## Security & Privacy

**Data that leaves your machine:**
- None from this skill itself

**Data that stays local:**
- optional funnel notes in `~/tinder/`
- profile observations, active match stages, and date-conversion patterns approved by the user

**This skill does NOT:**
- auto-send messages
- invent verification, intentions, or compatibility
- scrape Tinder, social media, or private records
- store credentials, payment details, or unnecessary third-party private data
- make undeclared network requests

## Trust

This is an instruction-only Tinder coaching skill.
No credentials are required and no third-party service access is needed.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `dates` - shape simple, low-pressure date plans once a match is warm
- `chat` - refine tone, brevity, and communication defaults across conversations
- `network` - build low-pressure outreach and follow-up habits beyond swipe apps
- `coach` - keep weekly accountability on profile tests and conversion goals
- `empathy` - improve reading of tone, reciprocity, and compatibility cues

## Feedback

- If useful: `clawhub star tinder`
- Stay updated: `clawhub sync`
