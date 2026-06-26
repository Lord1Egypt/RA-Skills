# Glance — Real-Time AI Coworker Activity

See what your team's AI coworkers are working on and detect file-level
collisions using `ox glance`.

## Usage

```bash
ox glance [--since <duration>] [--until <duration>]
```

**Defaults:** since last checkpoint (or 4 hours if no checkpoint).

**Duration formats:** `3d`, `7d`, `24h`, `1w`, or ISO date `2026-04-20`.

## Output structure

`ox glance` returns JSON. Key fields:

### `authors[]`

Each active coworker with:
- Name and agent type
- Recent murmurs (WIP updates)
- Files they're touching
- Session activity

### `conflicts[]`

File-level collision detection. Each entry lists:
- The file path
- Which coworkers are touching it
- Overlap type (concurrent modification risk)

Surface these as **warnings** when non-empty:
> "You and [coworker] are both touching `internal/auth/handler.go` —
> consider coordinating."

### `overlap[]`

Pairs of coworkers with overlapping file activity. Useful for
identifying who should coordinate.

### `patterns[]`

Detected activity patterns across the team (e.g., concentrated work
in one package, distributed changes across many files).

### `velocity`

Conflict velocity over time — trend of how many file overlaps are
occurring. Rising velocity suggests coordination is needed.

### `stats`

Totals: `totalMurmurs`, `totalSessions`, `totalAuthors`,
`totalConflicts`, `wipCount`, `fileChangeCount`.

## Workflow

1. Run `ox glance` (or with `--since` for a wider window).
2. Parse the JSON output.
3. Synthesize into an actionable narrative:
   - **Active coworkers:** who's working, on what
   - **Collision warnings:** files with multiple editors
   - **Coordination suggestions:** who should talk to whom
   - **Activity patterns:** where work is concentrated

4. If the user wants more detail on specific murmurs:
   ```bash
   ox murmur list
   ```

## Examples

```bash
# Default: since last checkpoint
ox glance

# Last 3 days
ox glance --since 3d

# Specific window
ox glance --since 2026-04-18 --until 2026-04-22
```
