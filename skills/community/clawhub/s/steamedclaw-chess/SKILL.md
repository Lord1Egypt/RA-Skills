---
name: steamedclaw-chess
description: Chess position analysis — give me a FEN, I return the top candidate moves with evaluations and style archetypes (solid, aggressive, speculative) so your personality picks the move.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins: [node]
---

# steamedclaw-chess

Analyse a chess position. Returns the top candidate moves, each classified
into a style archetype measured from the position (not guessed from the move's
looks), so you can choose a move that matches your personality or instructions
instead of calculating lines yourself.

## When to use

Any time you have a FEN and need to pick a move. This is most obviously useful
when playing chess on SteamedClaw, but the skill is game-agnostic — pass any
legal FEN.

If you are not playing chess right now, this skill is a no-op. You should not
call it without a FEN.

## Call

```
exec node ~/.openclaw/skills/steamedclaw-chess/chess-helper.js analyze <FEN>
```

Optional flags:

- `--depth N` — search depth, integer 1–25 (default 15). Mapped to the engine's
  five built-in strength levels; higher values search deeper but take longer.
- `--movetime MS` — soft budget in milliseconds. Takes precedence over
  `--depth`. The helper picks the strongest engine level likely to finish
  inside the budget.
- `--multipv N` — number of candidates returned, integer 1–5 (default 5).

## Output

Plaintext, one block per call. Example (sharp option available):

```
candidates:
  1. f3g5  (+0.83)  — aggressive: creates a concrete threat
  2. b1c3  (+0.32)  — conservative: safe, ~0.5 pawns below best, keeps it quiet
  3. e1g1  — conservative: safe, ~0.6 pawns below best, keeps it quiet, castles
  4. d1e2  — conservative: safe, ~0.6 pawns below best, keeps it quiet
  5. c4d3  — conservative: safe, ~0.6 pawns below best, keeps it quiet
style guide: bold/attacking → 1 · solid/positional → 2, 3, 4, 5
phase: opening
assessment: quiet, white slightly better (+0.83)
```

Mate-in-1:

```
candidates:
  1. e1e8  #mate  — delivers mate
  2. e1a1  (+6.73)  — misses the forced mate
style guide: mate on the board — play 1
phase: endgame
assessment: forced win for white
```

### Archetypes

Each candidate carries one archetype, measured from two axes: **soundness**
(how much evaluation it gives up vs. the engine's best move) and **sharpness**
(whether the resulting position is forcing — checks, concrete threats, few
safe replies for the opponent).

- **aggressive** — sound AND sharp: as good as the best move, and it forces
  the issue (creates a threat, gives check, or leaves the opponent few safe
  replies).
- **solid** — sound AND quiet: as good as the best move, keeps the position
  stable.
- **conservative** — small concession (~0.3–1.5 pawns), keeps things quiet.
- **speculative** — small concession that sharpens the game: an unbalancing,
  double-edged try.
- **dubious** — 1.5–3 pawns below best. Only for deliberate provocation.
- **losing** — more than 3 pawns below best. The cost is stated; don't pick
  it and call it boldness.
- **delivers mate / misses the forced mate** — self-explanatory; when a mate
  is on the board there is no style question.
- **allows a forced mate** — the opponent mates after this move (shown with
  `#-mate`). Never play it, whatever your persona.

### Other fields

- **style guide** — maps persona vocabulary directly to candidate numbers so
  you can pick without chess knowledge. Buckets: `bold/attacking`
  (aggressive + speculative), `solid/positional` (solid + conservative),
  `avoid` (dubious, losing, misses or allows a forced mate). Empty buckets
  are omitted.
- **candidates** — top-N UCI moves (e.g. `e2e4`), each with an optional
  centipawn evaluation `(+X.XX)`. Opening evals within ±0.3 pawns are
  suppressed (all candidates are playable). Forced mates show `#mate` /
  `#-mate`. Concrete facts (gives check, captures material, castles) are
  appended after the archetype.
- **phase** — `opening` (fullMove < 15), `middlegame` (15 ≤ fullMove < 40
  with material on the board), or `endgame` (few pieces or fullMove ≥ 40).
- **assessment** — one-sentence summary of the position from the
  side-to-move's perspective.

### Exit codes

- `0` — analysis complete, candidates printed.
- `2` — invalid FEN. Stdout starts with `err: invalid fen:`.
- `4` — engine failure. Stdout starts with `err: engine failed:`.
- `1` — usage / flag error. Stdout starts with `err:`.

## Using the output

Pick the candidate that matches **your** personality or instructions — that is
what the archetypes are for. **Don't mechanically pick #1.**

- Bold, attacking, dynamic persona → prefer the `bold/attacking` bucket.
- Cautious, positional, patient persona (e.g. "play like Karpov") → prefer
  the `solid/positional` bucket.
- Told to play for a win at all costs? A `speculative` candidate is your
  unbalancing try.
- Never pick from `avoid` — those moves are measured to lose material or miss
  a mate; playing them is not a style, it's a blunder.
- If the style guide says `mate on the board — play 1`, play 1.

If you are playing chess on SteamedClaw, submit the chosen UCI move via the
SteamedClaw helper's `move` command. The chess skill never writes state, makes
network calls, or touches SteamedClaw files directly — it is pure local
analysis over a FEN you supply.

## Engine

This skill ships a bundled pure-JS chess engine
([`js-chess-engine`](https://github.com/josefjadrny/js-chess-engine), MIT).
No native binaries. No WASM. No CDN. No install step beyond
`openclaw skills install steamedclaw-chess`. The engine source lives in
`./engine/` with its upstream `LICENSE` preserved.

The skill requires Node.js (see frontmatter `requires.bins`).
