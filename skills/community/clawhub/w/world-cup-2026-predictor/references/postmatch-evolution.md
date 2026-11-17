# Post-Match Review And Controlled Evolution

Use this reference after a match, when scheduling a result check, or when evaluating a model challenger. The active model changes only after repeated, independently validated evidence.

## Data Directory

Runtime data is separate from the installed skill. Resolution order is:

1. `--data-dir`
2. `FOOTBALL_FORECASTER_DATA_DIR`
3. `~/.football-forecaster`

The directory may contain:

| Path | Purpose |
| --- | --- |
| `forecasts.jsonl` | Immutable forecast snapshots. |
| `completed.jsonl` | Idempotent settled review records. |
| `profiles/*.json` | Versioned promoted profiles with bound evidence. |
| `active-profile.json` | Atomic pointer to the champion and its parent. |
| `evolution/candidates.json` | Candidate parameters and selected challenger. |
| `evolution/evaluation.json` | Samples, chronological split, and holdout metrics. |
| `evolution/decision.json` | Passed and failed promotion gates. |

Do not store runtime ledgers inside the skill folder. An upgrade may replace installed package files.

## Verified Result Contract

A final result needs either one official source or two reputable, independent sources that agree. Record source name, URL, and observation time. Do not finalize a postponed, abandoned, suspended, live, or conflicting result.

Keep each scope explicit:

```json
{
  "status": "final",
  "event_id": "event-id",
  "score_90m": {"home": 1, "away": 1},
  "score_after_extra_time": {"home": 3, "away": 1},
  "penalties": null,
  "qualified": "Home Team",
  "sources": [{"name": "Official", "official": true, "observed_at": "2026-07-13T06:00:00+00:00", "url": "https://example.test/result"}]
}
```

`score_90m` settles 1X2, Asian handicap, totals, BTTS, and exact score. Qualification uses the declared advancement result. Never substitute an after-extra-time score for a missing 90-minute score.

## Review Workflow

1. Load the archived forecast snapshot, including `raw_match`, `as_of`, `event_id`, and `input_fingerprint`.
2. Verify the final result and periods.
3. Run `postmatch_review.py` with `--language en` or `--language zh`.
4. Report right, wrong, push/unsettled, closing movement, cause evidence, calibration impact, and evolution status.
5. Append the completed record idempotently.
6. Schedule retries rather than guessing when the result is not final.

Cause tags require evidence. The final score alone cannot prove lineup impact, news impact, market manipulation, or model error. A correct prediction receives the same audit as an incorrect one.

## Post-Match Timing

`postmatch_alerts.py` uses absolute-time arithmetic:

| Match type | First check |
| --- | --- |
| League, group, friendly | Kickoff +135 minutes |
| Single-leg or two-leg knockout | Kickoff +165 minutes |

If the result is not final, retry every 15 minutes at most four times. The generated prompt must invoke `$world-cup-2026-predictor`, use verified sources, preserve result periods, run the review script, and answer in the user's language.

## Independent Samples

One event is one independent sample. T-3h10, T-2h10, T-1h10, and T-10min snapshots remain useful diagnostics, but they do not count as four matches. The latest valid pre-kickoff snapshot is the primary evolution record.

Records are invalid for evolution when replay input is missing or changed, `as_of` is missing or not before kickoff, result settlement is invalid, metrics are non-finite, or source evidence is quarantined.

## Champion-Challenger Procedure

1. Require 100 valid distinct completed matches overall.
2. Require 30 holdout matches in each affected eligible bucket.
3. Group every snapshot for an event into the same chronological fold.
4. Select from deterministic one-coordinate `-5%` and `+5%` candidates on older records.
5. Replay the champion and selected challenger on the newest 30 distinct matches.
6. Promote only if every gate passes.

The gates are:

| Gate | Requirement |
| --- | --- |
| 1X2 Brier | At least 1% relative improvement. |
| 1X2 log loss | No regression. |
| Totals and BTTS | No regression when each market has at least 30 observations. |
| Eligible bucket Brier | No more than 2% regression. |
| Calibration error | No more than 0.005 regression. |
| Integrity | No conflicts, malformed metrics, changed replay input, or stale lineage. |

Tier D stays at zero. Structural rules such as de-vigging, deduplication, period separation, and source minimums are not tunable.

## Profile Activation And Rollback

An `evaluate` run is deterministic and does not create a versioned profile. A successful `promote` run writes candidate, evaluation, and decision audits before atomically changing `active-profile.json`.

The promoted artifact binds its parent, creation time, training cutoff, training and holdout record ids, metrics, one-coordinate parameter diff, promotion decision, and SHA-256 evidence fingerprint. Tampered evidence, path traversal, conflicting profile ids, stale parents, and concurrent activation fail closed.

Rollback changes only the active pointer; it does not delete a profile. The automatic rollback rule requires at least 30 new distinct matches and regression in both Brier score and log loss. `--mode rollback` remains an explicit operator recovery action.

## Bilingual Status

Keep state ids stable for automation and localize their explanations:

| State | English | 中文 |
| --- | --- | --- |
| `model_unchanged` | Model unchanged | 模型不变 |
| `challenger_pending` | Challenger pending | 挑战模型待验证 |
| `champion_promoted` | Champion promoted | 冠军模型已晋升 |
| `champion_rolled_back` | Champion rolled back | 冠军模型已回滚 |

Always preserve probability language. No review, calibration score, promotion, or rollback guarantees the next result or any profit.
