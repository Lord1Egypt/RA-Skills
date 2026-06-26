# World Meeting Coordination Skill

Find and rank cross-timezone meeting windows as **Optimal**, **Stretch**, and **Avoid** with Telegram-friendly output formatting.

## What it does

- Computes candidate windows across a day anchored to a reference timezone
- Converts each slot to participant local times using `zoneinfo` (DST-aware)
- Scores each slot by local-hour comfort bands
- Outputs readable blocks with:
  - 24h + 12h times
  - `+1 day` marker when local date rolls forward
  - italicized reasons for Stretch/Avoid
  - spacer lines that render well in Telegram

## Usage

### First-time onboarding (automatic on first interactive run)

On first interactive run, the skill asks 3 questions and stores config at:

`~/.openclaw/skills/world-meeting-coordination-skill/config.json`

Manual commands:

```bash
python3 scripts/meeting_windows.py --setup
python3 scripts/meeting_windows.py --show-settings
```

### Chat setup phrase + intent matching

Canonical phrase:

- `Run world meeting skill setup`

Also treat these as setup/settings intent:

- "set up meeting skill"
- "configure world meeting"
- "update my meeting hours"
- "set my scheduling preferences"
- "change my timezone for meeting windows"
- "show my meeting settings"

### Natural-language prompt examples

- "Find the best meeting windows for Chicago, London, and Tel Aviv on March 6, anchored to Chicago time. Return Optimal, Stretch, and Avoid windows with reasons."
- "Find overlap windows for San Francisco, New York, and Berlin on 2026-04-12 in Pacific time, 60-minute meetings."
- "Give me top 3 windows for Chicago, Paris, and Singapore tomorrow in Chicago time, with +1 day markers where needed."

### CLI example

```bash
python3 scripts/meeting_windows.py \
  --date 2026-03-06 \
  --anchor America/Chicago \
  --zones "Chicago=America/Chicago,London=Europe/London,Tel Aviv=Asia/Jerusalem"
```

Optional flags:

- `--duration` meeting length in minutes (default: `60`)
- `--step` slot step in minutes (default: `60`)
- `--top` number of results per category (default: `3`)
- `--my-name` participant name key to apply personal hours to
- `--my-hours` personal preferred hours (e.g. `09:00-17:00`)
- `--hours` per-participant hours map (e.g. `Chicago=09:00-17:00,London=08:30-17:30`)

Example with only your hours known:

```bash
python3 scripts/meeting_windows.py \
  --date 2026-03-10 \
  --anchor America/Chicago \
  --zones "Chicago=America/Chicago,London=Europe/London,Bangalore=Asia/Kolkata" \
  --my-name Chicago --my-hours "09:00-17:00"
```

## Repository workflow

- **Development source (git):**
  - `/home/pi/.openclaw/workspace/projects/world-meeting-coordination-skill`
- **Skill path during development:**
  - `/home/pi/.openclaw/workspace/skills/world-meeting-coordination-skill` (symlink)

This project is intentionally **not mirrored into `apps/`**.
Release/install validation should happen via ClawHub installation path.

## Publish

After changes, run smoke test, then publish a version:

```bash
./tests/test_smoke.sh
clawhub publish . --slug world-meeting-coordination-skill --name "World Meeting Coordination Skill" --version <x.y.z> --changelog "..."
```

## Smoke test

```bash
./tests/test_smoke.sh
```

## Notes

- Current engine is local `zoneinfo` based (no external API credentials required).
- Backlog for profile-based participant/company hours is tracked in GitHub issues and private local notes.
