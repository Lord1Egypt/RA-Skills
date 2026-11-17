# workout-claw

> Local-first gym workout tracker. CLI + skill manifest, designed for LLM agent invocation. No cloud account, no daemon, no DB.

`workout-claw` is a tiny CLI that logs gym sessions to plain JSON files on disk. It's built to be invoked by an LLM agent (Claude, GPT, etc.) through a SKILL.md contract — but it's perfectly usable from a terminal directly. Sister project to [`nutrition-claw`](https://github.com/Pita/nutrition-claw).

## 30-second demo

```bash
$ workout-claw log "pullups 4x10@bw, incline-db-press 4x12@20, bench 4x10@60, triceps-pushdown 4x12@40" --cardio "incline-walk 20min @4.5kmh i6"

logged:
  date: 2026-05-15
  session_id: MWDxpbQE
  muscle_group: chest
  time: 17:00
  exercises_count: 4
  total_sets: 16
  total_volume_kg: 5280
exercises:
  - name: pullups
    muscle: back              # ← auto-tagged per-exercise, not just session-level
    sets: 4
    reps_per_set: 10
    weight: bw
  - name: bench
    muscle: chest
    sets: 4
    reps_per_set: 10
    weight: 60
  ...
```

```bash
$ workout-claw pr bench
exercise: bench
estimated_1rm_kg: 80           # ← Epley: 60 kg × (1 + 10/30)
from_set:
  date: 2026-05-15
  weight_kg: 60
  reps: 10

$ workout-claw volume --muscle back --weeks 4
muscle: back
totals:
  volume_kg: 0                 # ← bodyweight contributes 0 to kg volume (v0.4 will fix)
  sets: 4
  reps: 40
  days_trained: 1              # ← pullups on chest day correctly counted as back work
```

## Why it exists

The [`workout-logger`](https://clawhub.ai/skills/workout-logger) skill on ClawHub describes a beautiful conversational UX for logging workouts — but it's a stub. No CLI, no datastore, no PR tracking. Your workouts land as plain-text journal entries you can't query.

`workout-claw` is the missing implementation: it gives the agent a real backing CLI to invoke, with structured JSON storage you can `cat`, `jq`, or `git diff`. The agent handles natural-language input ("log my chest workout: bench four sets of ten at 60"); the CLI handles deterministic state.

This is the same split you find with `nutrition-claw`: the skill manifest is the contract, the CLI is the engine, plain JSON is the source of truth.

## Install

```bash
git clone <repo>
cd workout-claw
npm install
npm run build
npm link                       # symlinks workout-claw to your PATH
```

Requires Node ≥ 20.

For OpenClaw integration:

```bash
mkdir -p ~/.openclaw/workspace/skills/workout-claw
cp SKILL.md ~/.openclaw/workspace/skills/workout-claw/SKILL.md
systemctl --user restart openclaw-gateway.service
```

(Symlinks are rejected as a security measure — copy the file. `npm run openclaw:sync` does this in one command.)

## Commands

```
workout-claw log <exercises>           # parse fitdown-style input, append session
workout-claw history [--muscle X] [--exercise Y] [--weeks N]
workout-claw pr <exercise>             # Epley 1RM estimate
workout-claw volume --muscle X [--weeks N]   # cross-day volume rollup
workout-claw summary [--date YYYY-MM-DD]
workout-claw last                      # most recent session across all dates
workout-claw delete <session-id>
workout-claw edit <session-id>         # opens session JSON in $EDITOR
```

### Input syntax (fitdown-inspired)

```
<exercise> <sets>x<reps>@<weight>
```

- Multi-word exercise names use dashes (`incline-db-press`) or spaces (`bench press`; stored with dashes)
- Bodyweight: `pullups 4x10@bw`
- Unit suffix: `bench 3x8@60kg` or `bench 3x8@135lb` (lb is converted and stored as kg)
- Uneven sets: `bench 8,8,6@60` (per-set reps, one weight) or `bench 8@60,6@65` (per-set reps and weights)
- Multiple exercises in one call: comma-separated

Examples:

```bash
workout-claw log "squat 5x5@100, leg-press 4x10@200, leg-curl 3x12@40" --muscle legs
workout-claw log "deadlift 1x5@140" --note "PR attempt — felt strong"
workout-claw log "" --cardio "run 5km 24min"     # cardio-only session
```

### Optional flags on `log`

| Flag | Meaning |
|---|---|
| `--muscle <g>` | back \| legs \| chest \| shoulders \| arms \| core \| cardio (default: inferred from the exercises, or from the optional weekday split in `~/.workout-claw/config.json`) |
| `--cardio "<entry>"` | e.g. `"incline-walk 20min @4.5kmh i6"` — minutes, speed, incline |
| `--note "<text>"` | free-text annotation |
| `--date YYYY-MM-DD` | date to log under (default: today, local time; invalid dates are rejected) |
| `--time HH:MM` | override (default: now) |

### Optional weekday split

By default the session's muscle group is inferred from the exercises you logged (most sets wins). If you follow a fixed split, create `~/.workout-claw/config.json`:

```json
{ "split": { "mon": "back", "wed": "legs", "fri": "chest" } }
```

On those weekdays the configured group is used; `--muscle` always wins. No split ships with the package.

## Data safety

Day files are written to a temp file and renamed into place, so a crash cannot leave a half-written log. A day file that is not valid JSON is never treated as empty: commands fail with a `corrupt JSON` error and leave the file untouched.

## Data shape

One JSON file per day at `~/.workout-claw/logs/YYYY-MM-DD.json`. Array of sessions (typically one per day, but multi-session days are supported).

```json
[
  {
    "id": "MWDxpbQE",
    "time": "17:00",
    "muscle_group": "chest",
    "exercises": [
      {
        "name": "bench",
        "muscle": "chest",
        "sets": [
          { "reps": 10, "weight_kg": 60 },
          { "reps": 10, "weight_kg": 60 },
          { "reps": 10, "weight_kg": 60 },
          { "reps": 10, "weight_kg": 60 }
        ]
      }
    ],
    "cardio": [
      { "type": "incline-walk", "minutes": 20, "speed_kmh": 4.5, "incline": 6 }
    ],
    "notes": "..."
  }
]
```

The `muscle` field per exercise is **auto-inferred at log time** via a keyword lookup (`src/lib/exercise-map.ts`). Sessions logged in earlier versions without this field are enriched on read.

## Architecture

Three layers, separable:

1. **`SKILL.md`** — the agent-facing contract. Describes triggers, when to invoke, which flags to use. No code.
2. **`workout-claw` CLI** — TypeScript/Node binary. Parses input, computes PRs and volume, writes JSON.
3. **`~/.workout-claw/logs/*.json`** — the data. Diffable, queryable, portable.

The agent (e.g., a Claude Code skill) reads `SKILL.md`, decides to invoke the CLI, calls it via Bash, parses the YAML output, and relays a friendly summary to the user. The CLI is stateless and non-interactive (except `edit`, which spawns `$EDITOR`).

## Roadmap

Shipped:
- ✅ v0.1 — `log`, `history`, `pr`, `summary` (per-day JSON, fitdown input, Epley 1RM)
- ✅ v0.2 — `last`, `delete`, `edit`
- ✅ v0.3 — per-exercise muscle tags, `volume` command for cross-day rollups
- ✅ v0.4.0 — reliability: atomic writes, fail-on-corrupt, flexible input, `--date` validation (see [`CHANGELOG.md`](./CHANGELOG.md))

Backlog (see [`TODO.md`](./TODO.md)):
- next — bodyweight-adjusted volume (so `@bw` exercises contribute to total kg lifted)
- next — `progress <exercise>` curve (top-N 1RMs over time)
- next — RPE per set: `bench 4x10@60r8`

## License

MIT.

## Credits

Built on the architectural pattern established by [Peter Martischka's `nutrition-claw`](https://github.com/Pita/nutrition-claw). The fitdown syntax is borrowed from [`datavis-tech/fitdown`](https://github.com/datavis-tech/fitdown) — `bench: 4x10@60` is a genuinely elegant format for both humans and LLMs to read and write.
