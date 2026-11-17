# Engine Labels — Author Notes

This document is for **skill authors**, not for the agents that use the skill.
It describes the archetype classification used by `chess-helper.js` and the
heuristics that produce it. The agent-facing `SKILL.md` intentionally keeps
the vocabulary short; authors hacking on the helper should read this first.

Authoritative design references: `planning/054-chess-strategy-skill.md`
(original design) and issue #555 (archetype classification v2, which replaced
the original move-surface label scheme).

## Goals

- Labels are **plaintext prose**, not structured tags. The output is read by
  LLM agents making a move choice; describing a move in words nudges the agent
  toward stylistic judgement instead of mechanical "pick #1" behaviour.
- Labels are **measured from the position**, not guessed from the move's
  surface features. v1.0.0's original scheme labelled `e2e4` "aggressive"
  because it was a pawn landing on a centre square; that was replaced (#555)
  because it never looked at the resulting position, so a persona choosing
  off those labels was choosing off noise.
- Labels are **deterministic** given a FEN and flag set. All randomness in the
  engine is disabled (`randomness: 0`). The agent invokes via `exec`, so every
  invocation is a fresh process.

## Classification: two measured axes

Each candidate is classified on:

1. **Soundness** — `deltaCp`, the centipawn loss vs. the engine's best move.
   **Caveat (demonstrated, not hypothetical):** the vendored engine's root
   loop searches non-first root moves with a zero window, so `analysis` mode
   returns loose fail-low *bounds* for every non-best candidate — a
   mate-losing move can report a ~90 cp delta. The helper therefore
   cross-checks: the reply probe's best-reply score IS an exact full-window
   PV score, so a probe-implied delta (candidate's best-reply score minus the
   best candidate's, same level) **overrides the main delta when larger by
   `PROBE_DELTA_TRUST_MARGIN_CP` (100)**. The margin keeps low-level probe
   noise from reclassifying sound moves; the override catches gross
   understatement (hung pieces, hung mates).
2. **Sharpness** — whether the candidate forces the issue, combined from
   three signals in priority order (`assessSharpness`):
   - **check** — the candidate gives check (from post-move `exportJson()`).
   - **mate-threat / threat** — null-move probe: flip the side to move in the
     post-candidate FEN (a "pass") and re-search from the mover's side. The
     swing is `nullBest + bestReplyScore` (both from probes at the same
     level, so per-level eval offsets cancel). The raw swing carries a
     position-dependent tempo baseline — the engine's side-to-move bonus
     counts once in each probe — measured at ~90 cp in the starting position
     and ~230 cp in typical middlegames. The test is therefore **relative**:
     a candidate is a threat when its swing exceeds the **median swing of the
     candidate set** by `THREAT_SWING_ABOVE_MEDIAN_CP` (150). The mate test
     uses `nullBest` alone (≥ `MATE_SCORE_THRESHOLD` = the mover mates given
     a free move) — **never the swing**, which also crosses the threshold
     when `bestReplyScore` is mate-scale, i.e. the *opponent* mates after the
     candidate (that is the hangs-mate case below, and conflating the two was
     a real polarity bug caught in review).
   - **forcing** — reply probe: analyse the post-candidate position and count
     opponent replies within `SAFE_REPLY_BAND_CP` (100) of the best reply.
     At most `SHARP_MAX_SAFE_REPLIES` (2) safe replies = forcing. Note this
     signal only fires on truly forced positions; empirically the reply-eval
     spread does NOT discriminate merely-sharp moves with this engine (after
     Ng5 in the Italian, level-3/4 probes score most replies flat because the
     punishment is beyond the probe horizon). The null-move probe is the
     signal that catches those.

The null-move probe is skipped when the candidate gives check (passing with
the king en prise is not a searchable position) — the check signal already
covers it.

## Archetype mapping (`classifyArchetype`)

| Condition | Archetype |
| --- | --- |
| candidate mates | `mate` ("delivers mate") |
| best move mates, candidate doesn't | `misses-mate` |
| opponent mates after the candidate (probe best reply ≥ mate scale) and at least one candidate doesn't hang mate | `hangs-mate` ("allows a forced mate"); its eval renders as `#-mate` |
| deltaCp ≤ 30, sharp | `aggressive` |
| deltaCp ≤ 30, quiet | `solid` |
| 30 < deltaCp ≤ 150, sharp | `speculative` |
| 30 < deltaCp ≤ 150, quiet | `conservative` |
| 150 < deltaCp ≤ 300 | `dubious` |
| deltaCp > 300 | `losing` |

Thresholds are named constants at the top of `chess-helper.js`
(`SOUND_DELTA_CP`, `SPECULATIVE_DELTA_CP`, `LOSING_DELTA_CP`,
`SAFE_REPLY_BAND_CP`, `SHARP_MAX_SAFE_REPLIES`,
`THREAT_SWING_ABOVE_MEDIAN_CP`, `PROBE_DELTA_TRUST_MARGIN_CP`) and are
expected to be tuned empirically after fleet testing (#339).

The hangs-mate flag is only applied when at least one candidate does *not*
hang mate — if every move loses to mate, the game is lost and relative deltas
are all the output has left to say.

Secondary descriptors appended after the archetype, in order: `stalemates
opponent — forces a draw`, `gives check`, `captures material`, `castles`.
Candidate #1 gets a `clearly best` prefix when it leads #2 by ≥ 150 cp
(`CLEARLY_BEST_GAP_CP`) and is not a mate line.

## Style guide line (`buildStyleGuide`)

Maps persona vocabulary to candidate numbers so a weak model can pick without
chess understanding:

- `bold/attacking` — aggressive + speculative candidates.
- `solid/positional` — solid + conservative candidates.
- `avoid` — dubious, losing, misses-mate, hangs-mate.
- Empty buckets are omitted; if candidate #1 mates, the whole line collapses
  to `style guide: mate on the board — play 1`.

## Phase classifier

Implemented in `detectPhase(status)` — unchanged from v1:

- `endgame` if `fullMove >= 40` or non-king piece count ≤ 7.
- `opening` if `fullMove <= 14` (and not endgame).
- `middlegame` otherwise.

Phase no longer shapes the label vocabulary (archetypes are phase-independent);
it still controls opening eval suppression (±30 cp hidden — showing an eval
there implies false precision) and the assessment sentence wording.

## Assessment sentence

`buildAssessment(phase, bestScoreCp, isMate, sideToMove)` — unchanged from v1:

- If `isMate` is set, emit "forced win for <side>" or "losing for <side> —
  opponent has a forced win".
- Otherwise the wording scales by phase and magnitude; it reports from **the
  side to move's** perspective, matching the sign convention of the engine's
  `bestScore` output.

## Cost profile

Per invocation: 1 main analysis (level from `--depth`/`--movetime`) + up to
2 probes per candidate (reply probe + null-move probe) at
`min(level, PROBE_LEVEL_CAP=3)`. Each probe is a fresh stateless
`engine.ai()` call (fresh Game/TT — nothing is shared between probes) and
measures ~20–40 ms on a modern CPU; a full 5-candidate CLI invocation
measured ~0.2 s end to end. Trivial against the 7-minute turn floor.

## Engine gotchas

- `Game.move()` returns a BoardConfig with stale check/mate/stalemate flags in
  js-chess-engine v2.4.6; only `exportJson()` and `ai()` recompute them. Watch
  for regressions on engine upgrades.
- Root-move scores in `analysis` mode are loose bounds for non-best root
  moves **today** (zero-window root search — the classic MultiPV pitfall);
  that is why the probe-delta override exists. If the engine ever gains exact
  root scores in analysis mode, the override becomes redundant (but harmless)
  and `PROBE_DELTA_TRUST_MARGIN_CP` could be retired — re-validate against
  the fixture positions in the test suite before changing it.

## Future vocabulary work

Keep the set small until there's evidence an agent acts differently in
response to a new label. Candidates for post-fleet expansion:

- Named tactical motifs ("forks", "pins", "skewers") — needs a pattern
  scanner on the pre/post boards.
- Positional labels ("passed pawn", "outpost", "weakens king safety") —
  requires square-scanning heuristics.

## Testing philosophy

The test suite under `../__tests__/chess-helper.test.mjs` exercises:

- Argument parsing (happy path + every validation branch)
- Phase classifier on hand-constructed piece maps
- `classifyArchetype` / `assessSharpness` / `median` / `flipSideToMove` /
  `describeCandidate` / `buildStyleGuide` on synthetic inputs (no engine call)
- End-to-end `analyze()` on fixture FENs: opening, Italian (Ng5 must classify
  aggressive while quiet development does not), late middlegame, K+P vs K,
  mate-in-1 (including "misses the forced mate" and the mate style guide),
  stalemate, invalid FEN

Engine-backed tests assert **structural** properties (phase label, presence
of archetype words, `#mate` markers, candidate count matches `--multipv`)
rather than exact evals — exact scores shift with engine tuning; the
classification structure shouldn't.
