---
name: world-cup-2026-predictor
description: Use for English or Chinese football match forecasts, pre-kickoff alerts, post-match review, and controlled self-evolution from multi-book odds, line movement, 1X2/moneyline, European odds, Asian handicap, Hong Kong/Malay/Indo water, totals, BTTS, exact score, qualification, lineup/news, 盘口, 赔率, 欧赔, 亚盘, 港赔, 马来盘, 印尼盘, 大小球, 临场盘, 比分预测, 赛后复盘, and 模型进化.
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "⚽"
---

# World Cup 2026 Predictor

Use this skill to produce a disciplined, probability-based football forecast from market structure and fresh news. Keep the output analytical: no guarantees, no profit claims, no certainty language, and no claim that a bookmaker knows the result.

The canonical invocation name stays `world-cup-2026-predictor`. The skill now covers football broadly, including international tournaments and club matches, while preserving bilingual response matching.

## Language Policy

Use the same language as the user in the response.

- English input -> English response.
- Chinese input -> Chinese response.
- Mixed input -> use the dominant language and keep market terms that are clearest in their original form.
- Do not duplicate every paragraph in both languages. Write one response in the user's language.

## Intake Gate

Before calculating:

1. Confirm the exact teams, competition, kickoff time and timezone, venue when relevant, and whether the match has started.
2. Confirm the match type: `league_or_group`, `single_leg_knockout`, `two_leg_first`, `two_leg_second`, or `friendly`. A second leg also requires the aggregate score and applicable tiebreak rules.
3. Collect at least three independent underlying bookmakers; five or more are preferred. An aggregator and its displayed bookmaker are one source, not two.
4. Record the source, underlying bookmaker, market, period, line, selection, explicit odds format, observed timestamp, and snapshot for every quote.
5. Link the schedule/competition source, odds sources, and every material lineup or news source.

If match identity is ambiguous, required context is missing, or the match has already started, abstain from a new pre-match forecast.

## Forecast Workflow

1. Deduplicate quotes by underlying bookmaker before counting sources.
2. Convert declared formats to decimal and implied probability. Reject ambiguous formats rather than guessing.
3. Remove each bookmaker's margin, then build the weighted, de-vigged consensus described in `references/consensus-model.md`.
4. Keep opening separate and compare Opening, T-3h10, T-2h10, T-1h10, and T-10min snapshots when available. Never relabel a nearby quote as a missing checkpoint.
5. Fit one coherent 90-minute score distribution from 1X2, totals, and BTTS. Use Asian handicap and exact-score markets as margin/consistency checks.
6. Keep 90-minute and qualification/to-advance probabilities separate. Qualification may include extra time and penalties.
7. Classify news as confirmed hard information, credible but unconfirmed reporting, or public narrative. Do not add a hidden probability adjustment; check whether later prices confirm the news.
8. Compare the new result with prior analysis. State what changed, what stayed the same, and whether the conclusion improved or was revised.
9. Score evidence quality and abstain when the evidence gate fails.

If a bundled script rejects malformed odds, missing formats, aggregator provenance, or unsupported live-only input, catch that validation error at the response layer. Name the missing/invalid field and return `no forecast edge` or `观望`; never expose a traceback and never guess a replacement value. When `actionable_forecast` is false, probabilities may be described only as diagnostics, not as a pick.

## Evidence Rules

- Require the market type, selection, and odds format before interpreting any number.
- Convert every price to a fair probability before comparing books.
- Remove bookmaker margin before building consensus.
- Use de-vigged consensus, not raw price averages.
- Treat opening lines as a separate reference point, not a substitute for current data.
- Prefer fresh quotes close to kickoff. Older data must be labeled as such.
- If the current picture depends on one book, one feed, or one rumor, do not publish a betting edge.

## Market Coverage

- 90-minute result: home/draw/away or moneyline.
- Qualification or to-advance: only for advancement, extra time, or penalties.
- Asian handicap: cover risk, not winner truth.
- Totals and BTTS: goal-shape and score-shape evidence.
- Exact score: consistency check, not the primary anchor.

Keep 90-minute and qualification markets separate. A team can be weak in 90 minutes and still credible to advance.

## Consistency Rules

- Asian handicap, totals, BTTS, and exact score must agree with the same fitted score distribution.
- If they disagree, explain the conflict instead of averaging it away.
- A stronger 1X2 favorite with a weak handicap is a narrow-win signal, not a blowout signal.
- A qualification favorite with a weak 90-minute price implies extra-time or penalty risk.
- Do not treat one market family as independent evidence if it is derived from the same underlying prices.

## News Rules

- Mark news as `confirmed` only when it comes from official or clearly attributable sources.
- Mark it as `unconfirmed` when it is rumor, preview, opinion, or unsupported reporting.
- Include source links for news that affects the forecast.
- If news is weak or unverified, keep it separate from the market read and lower confidence.

## Rolling Alert Workflow

When the user requests rolling pre-kickoff updates, create exactly four alerts per match unless the user explicitly requests a different schedule:

| Offset | Purpose |
| --- | --- |
| T-3h10 | Establish the fresh multi-book baseline and compare with opening. |
| T-2h10 | Recheck consensus movement, news, and source quality. |
| T-1h10 | Recheck likely/confirmed lineup information and flip triggers. |
| T-10min | Produce the final pre-match update, leaving the requested 10-minute decision window. |

Every alert prompt must invoke `$world-cup-2026-predictor`, refresh current sources, read prior analysis, and answer in the user's language. Use `scripts/kickoff_alerts.py --minutes-before 190 130 70 10` to generate exact local times. If automation tools are available, create the alerts; otherwise return the four exact times and prompts. A user who explicitly asks only for the final alert may use the default T-10min mode.

## Post-Match Review And Evolution

Review correct and incorrect forecasts with the same discipline and in the same language as the user. A correct pick is not proof that its explanation was valid, and a wrong pick is not permission to chase the latest result.

1. Fetch one official final result or two reputable independent sources that agree.
2. Keep `score_90m`, `score_after_extra_time`, `penalties`, and the qualifier separate. Never settle a 90-minute market with an extra-time or penalty result.
3. Join the verified result to the exact archived forecast by event id and `input_fingerprint`. Reject missing or changed replay input.
4. Settle 1X2, qualification, Asian handicap, totals, BTTS, and correct score in their declared periods. Quarter lines may be `half_win` or `half_loss`; pushes stay pushes.
5. Review both right and wrong calls, closing movement, evidence-backed causes, calibration impact, and unresolved evidence. Never invent a cause from the final score.
6. Write the completed record once. Postponed, abandoned, suspended, conflicting, or otherwise non-final results remain pending and never enter learning data.

Use these user-facing labels:

| User language | Required review labels |
| --- | --- |
| English | Final result, Right, Wrong, Unsettled/push, Causes, Calibration, Evolution status, Probability reminder |
| Chinese | 最终赛果、判断正确、判断错误、未结算/走盘、原因证据、校准影响、模型状态、概率提醒 |

### Evolution Safety Gates

One completed match never changes the active profile. Eligibility requires at least 100 distinct matches overall and 30 distinct matches in every affected bucket. Four alert snapshots from one event count as one independent match, and only the latest valid pre-kickoff record is primary.

Use grouped chronological walk-forward evaluation: older events select one-coordinate `-5%` or `+5%` challengers, and the newest 30 distinct events form the holdout. All snapshots from one event stay in one fold. Tier D remains zero.

Promotion requires every gate: 1% relative Brier improvement, no log-loss regression, no totals or BTTS regression when each has at least 30 observations, a 2% bucket regression cap, and a 0.005 calibration-error tolerance. Invalid records, source conflicts, missing fingerprints, non-finite metrics, or stale parent profiles fail closed. Pick accuracy is diagnostic, not a promotion gate.

Use these state ids and explain them in the user's language:

| State | Meaning |
| --- | --- |
| `model_unchanged` | Fewer than 100 distinct matches, no eligible bucket, or no validated improvement. |
| `challenger_pending` | A challenger exists, but one or more holdout or regression gates are pending or failed. |
| `champion_promoted` | Every promotion gate passed and the versioned profile was atomically activated. |
| `champion_rolled_back` | A manual rollback was performed, or 30 new distinct matches showed both Brier and log-loss regression against the parent. |

Do not perform a per-match profile update. Automatic rollback evidence requires 30 new distinct matches and both primary metrics to worsen; `--mode rollback` is also an explicit operator recovery command. Keep every promoted profile, its parent, record ids, metrics, parameter diff, decision, and integrity fingerprint.

### Reproducible Commands

```bash
python3 scripts/forecast.py --input examples/multi-book-match.json --data-dir ~/.football-forecaster --pretty
python3 scripts/postmatch_review.py --forecast examples/forecast-snapshot.json --result examples/completed-match.json --language en --data-dir ~/.football-forecaster --pretty
python3 scripts/calibrate.py --input ~/.football-forecaster/completed.jsonl --pretty
python3 scripts/evolve.py --completed ~/.football-forecaster/completed.jsonl --data-dir ~/.football-forecaster --mode evaluate --pretty
python3 scripts/evolve.py --completed ~/.football-forecaster/completed.jsonl --data-dir ~/.football-forecaster --mode promote --pretty
python3 scripts/evolve.py --data-dir ~/.football-forecaster --mode rollback --pretty
python3 scripts/postmatch_alerts.py --input matches.json --timezone Asia/Hong_Kong --retry-count 4
```

Use `--language zh` for a Chinese review. Read `references/postmatch-evolution.md` before creating post-match automation, interpreting evolution gates, or changing a model profile.

## Required Output

Use the same language as the user and include:

1. Data timestamp, timezone, match type, and current alert offset.
2. A compact conclusion table: 90-minute result probabilities, qualification when applicable, Asian handicap, total, BTTS, and a three-level score ladder.
3. Source coverage: raw sources, deduped independent bookmakers, formats, freshness, and missing checkpoints.
4. What changed, what stayed unchanged, and whether the previous forecast is retained or revised.
5. No-vig 90-minute probabilities and a separately labeled qualification probability.
6. Asian handicap, totals, BTTS, and exact-score consistency or conflict.
7. Confirmed lineup/news versus unconfirmed reporting and public narrative, with links.
8. A bookmaker/capital read grounded in observable prices and movement, without alleging manipulation.
9. Confidence as evidence quality, all abstention reasons, and exact flip triggers.
10. A concise betting-window note that never promises profit or accuracy.

When the evidence is insufficient, output `no forecast edge` in English or `观望` in Chinese instead of forcing a pick.

### Non-Actionable Output

When validation fails, a bundled script raises an input error, or `actionable_forecast` is false, replace the normal conclusion table with only:

1. Match, timestamp, and `no forecast edge` / `观望` status.
2. Stable reason category: `invalid_odds_format`, `missing_underlying_bookmaker`, `insufficient_books`, `invalid_context`, `stale_near_kickoff`, `already_started`, or `unsupported_live_state`.
3. The invalid or missing field and the evidence needed for a new run.
4. The next relevant checkpoint, if kickoff has not passed.

Do not output a recommended 1X2, qualification, Asian handicap, total, BTTS, or score pick in this mode. Diagnostic probabilities may be shown only when the user explicitly asks for them, and must remain labeled non-actionable.

## Confidence and Safety

- Three independent underlying books are the operational minimum for a full forecast; five are preferred.
- Near kickoff, no quote within 60 minutes triggers abstention.
- Ambiguous identity, severe disagreement, malformed markets, duplicated sources, or a started match without an in-play state model triggers abstention.
- Confidence describes evidence quality, not outcome certainty or value. A likely winner can still offer no demonstrated pricing edge.
- Never guarantee a result, encourage chasing losses, present betting as income, or place a bet for the user.

## Bundled References

- `references/source-policy.md`
- `references/consensus-model.md`
- `references/market-rules.md`
- `references/odds-formats.md`
- `references/postmatch-evolution.md`

Use these references before answering when source quality, consensus math, market interpretation, odds conversion, settlement, or evolution matters. Use `scripts/forecast.py` for reproducible probabilities and `scripts/calibrate.py` only on completed JSONL records; source-weight changes remain locked until the distinct-match floors and every promotion gate are met.
