# YumFu v1.6.0 — Dynamic Daily Evolution 🌍

## Highlights

This release introduces **Dynamic Daily Evolution**, a new system that keeps each YumFu world moving even while the player is offline.

Instead of hardcoded canned events, YumFu now:
- reads the player's current save
- reads the selected world setting
- infers plausible off-screen developments
- sends **one short in-world daily update with image**
- writes the result to a **safe sidecar state** without mutating the main active-play save

## What's New

### Dynamic Daily Evolution MVP
- Added sidecar-safe daily evolution architecture
- Added per-player daily evolution cron creation helpers
- Added runtime preparation + apply pipeline
- Added sidecar state load/save helpers
- Added language-aware daily evolution context building
- Added re-entry context so `/yumfu continue` can pull the player naturally back into the current scene

### Safe Sidecar Design
- Main save remains canonical for active play
- Daily evolution writes to `memory/yumfu/evolution/{universe}/user-{id}.json`
- Daily updates can add pressure, hooks, rumor threads, and soft world movement
- Avoids risky direct mutation of player saves during offline progression

### World-Agnostic Onboarding
- Any YumFu world can now ask after `/yumfu start`:
  - enable daily evolution? yes / no
- Added a unified post-start activation handler
- Per-player cron metadata is stored in sidecar state

### Language-Aware Re-entry
- Added recent-language detection for Chinese/English preference
- Added continue-time re-entry helpers so the game can resume in the player's natural language style

### Core YumFu Guarantees Reaffirmed
- Every active game turn should still generate **exactly one primary image**
- Every turn should still be logged for storybook/session replay
- Telegram story text stays paired with the image
- Daily evolution must not dilute the original YumFu visual-narrative loop

## New Scripts

- `scripts/set_daily_evolution.py`
- `scripts/load_daily_evolution.py`
- `scripts/daily_evolution_prepare.py`
- `scripts/apply_daily_evolution.py`
- `scripts/run_daily_evolution.py`
- `scripts/run_daily_evolution_job.py`
- `scripts/create_daily_evolution_cron.py`
- `scripts/disable_daily_evolution_cron.py`
- `scripts/enable_daily_evolution.py`
- `scripts/handle_daily_evolution_choice.py`
- `scripts/detect_recent_language.py`
- `scripts/build_reentry_context.py`
- `scripts/render_continue_reentry.py`

## Why This Matters

YumFu is no longer just a reactive chat RPG.
It can now feel like a **living world**:
- the world shifts while you're away
- you receive one visual story hook per day
- returning to the game feels easier and more natural

## Release Focus

**Main theme of v1.6.0:**
> Dynamic Daily Evolution / 每日进展世界演进

This is the headline feature of the release.
