# Core Trajectory Self-Evolution Algorithm

Updated: 2026-04-14

Chinese version:

- `trajectory-self-evolution-core-algorithm.md`

This note answers one concrete question: how does Finance Journal currently model the "trajectory self-evolution" problem?

The short version:

> The current implementation does not treat trading as a full reinforcement learning environment. It treats a compressed signature of each closed trade trajectory as a context-aware ranking problem, then uses bandit-style metrics to decide which historical paths should be reused first and which recurring risks should be suppressed first.

The main code entry points are:

- `finance_journal_core/analytics.py`
- `finance_journal_core/app.py`
- `finance_journal_core/cli.py`

## 1. Problem Definition

The most stable unit of data in the current system is not an intraday state-action sequence. It is a closed trade record with:

- entry / exit facts
- planned zones and execution deviation
- market stage
- environment tags
- logic tags / pattern tags
- emotion notes / mistake tags
- post-exit reviews and feedback

So "trajectory" currently means:

- a soft-structured summary of one trade
- a set of reviewable context conditions
- a set of measurable outcome signals

It does not yet mean:

- high-frequency state sequences
- continuous action sequences
- a fully defined MDP for direct policy optimization

That makes the current version better suited for:

1. matching similar historical paths
2. summarizing advantage zones and risk patterns
3. using bandit-style ranking for reminders

rather than jumping straight to offline RL.

## 2. Why This Is Called "Self-Evolution"

"Self-evolution" here does not mean that the system trades automatically on behalf of the user. It means a three-step loop:

1. turn each trade into a structured sample
2. extract reusable paths and risk genes from those samples
3. push those historical signals back when a similar setup appears again

So the system behaves more like a personal decision mirror:

- strong paths are surfaced earlier
- recurring risks are intercepted earlier
- every new trade feeds the historical pool again

## 3. Core Modeling Objects

### 3.1 Path arm

The system compresses one closed trade into a path signature using `_quality_path_components(...)`:

- first logic tag -> `逻辑=...`
- first pattern tag -> `形态=...`
- market stage -> `阶段=...`
- up to two environment tags -> `环境=...`
- if positive execution discipline exists, one extra component such as `纪律=买点在计划内` or `纪律=卖点在计划内`

Only trades with at least two components become valid path arms.

This object answers:

- "Under what combinations of conditions do I usually perform well?"

### 3.2 Gene arm

The system also treats single-dimension features as gene arms via `_token_specs(...)`:

- `logic:*`
- `pattern:*`
- `stage:*`
- `environment:*`
- `mistake:*`
- `emotion:*`
- `execution:*`
- `review:*`
- `review_feedback:*`

This object answers:

- "Which single features help repeatedly?"
- "Which single features repeatedly lead to losses or distorted execution?"

## 4. How Samples Enter the Statistics

`build_evolution_report(...)` only processes trades that satisfy:

- `status == "closed"`
- `actual_return_pct` is not empty

For each trade, the report extracts:

- `pnl = actual_return_pct`
- `alpha = timing_alpha_pct`
- `holding = holding_days`
- `effective = _is_effective_trade(trade)`

The definition of an "effective trade" is intentionally conservative:

- return must be positive
- if `timing_alpha_pct` exists, alpha must not be negative

So the system is not only checking whether the trade made money. It also checks whether the execution was at least not worse than the timing reference.

## 5. How Paths and Genes Are Aggregated

Each path bucket or gene bucket accumulates:

- `returns`
- `alphas`
- `holding_days`
- `wins`
- `losses`
- `effective_count`

Then `_bucket_summary(...)` produces:

- `sample_size`
- `win_rate_pct`
- `avg_actual_return_pct`
- `avg_timing_alpha_pct`
- `avg_holding_days`
- `effective_count`
- `loss_count`
- `positive_edge_score`

`positive_edge_score` is a heuristic composite score:

```text
positive_edge_score =
    win_rate_pct
    + avg_actual_return_pct * 2
    + avg_timing_alpha_pct
    + effective_count * 8
    - loss_count * 5
```

It is not a probability model. It is a practical ranking signal that compresses:

- win rate
- return
- timing quality
- count of effective executions

into one sortable number.

## 6. What Qualifies as a Quality Path or a Risk Gene

### 6.1 Quality path

A path enters `quality_paths` only if:

- `sample_size >= min_samples`
- `win_rate_pct >= 60`
- `avg_actual_return_pct > 0`

So the current implementation is not chasing one-off outliers. It first asks whether the path:

- repeats across samples
- has a reasonable win rate
- has positive average return

### 6.2 Reusable positive gene

A gene enters `reusable_genes` if one of these is true:

- it is an explicitly positive token, such as:
  - `execution:buy_in_plan`
  - `execution:sell_in_plan`
  - `review:good_exit`
  - `review_feedback:discipline_kept`
  - `review_feedback:good_exit_confirmed`
- or it is not hard-coded as positive, but its statistics still satisfy:
  - `win_rate_pct >= 60`
  - `avg_actual_return_pct > 0`

### 6.3 Risk gene

The following tokens are treated as direct risk-side candidates:

- all `mistake:*`
- `execution:buy_off_plan`
- `execution:sell_off_plan`
- `review:sell_fly`
- `review_feedback:sell_fly_confirmed`
- emotion-side tokens such as:
  - `急躁`
  - `慌张`
  - `冲动`
  - `上头`
  - `贪心`
  - `害怕`

Also, even if a token is not explicitly marked as risky, it still falls into the risk side when its average return is negative.

## 7. Why Bandit Instead of RL

### 7.1 The current data looks like one-shot decision feedback

The current dataset can reliably answer:

- how a given path behaved under a certain context
- whether a certain feature is historically more positive or negative

But it still cannot reliably answer:

- why action A was chosen instead of B at an exact moment
- what continuous state transitions followed that action
- how the path would have unfolded under a counterfactual action

So the current problem is naturally much closer to:

- contextual bandit
- hybrid bandit
- case-based ranking

than to a complete MDP.

### 7.2 How the current bandit metrics are computed

`_bandit_metrics(...)` transforms each path or gene summary into bandit-style scores.

It first builds a conservative Beta posterior:

```text
posterior_alpha = 1 + win_count + max(effective_count - win_count, 0)
posterior_beta  = 1 + loss_count
posterior_mean  = posterior_alpha / (posterior_alpha + posterior_beta)
```

Then it adds an exploration bonus:

```text
exploration_bonus =
    sqrt(2 * log(total_samples + 2) / (sample_size + 1))
```

It also folds return and alpha into a reward component:

```text
reward_component =
    max(avg_actual_return_pct, 0) / 20
    + max(avg_timing_alpha_pct, 0) / 25
```

The main ranking scores are:

```text
ucb_score =
    posterior_mean
    + 0.35 * exploration_bonus
    + reward_component

conservative_score =
    posterior_mean
    - 0.2 * exploration_bonus
    + 0.5 * reward_component
```

For risk arms, one extra score is computed:

```text
risk_penalty_score =
    max(-avg_actual_return_pct, 0) / 12
    + loss_count / sample_size
    + 0.2 * exploration_bonus
```

These scores serve different intents:

- `posterior_mean`: conservative historical success estimate
- `ucb_score`: who to review first
- `conservative_score`: who is safer to reuse
- `risk_penalty_score`: what should be suppressed first

## 8. How the Reminder Layer Works

`build_evolution_reminder(...)` does not produce direct buy or sell signals. It first performs context matching.

The query is transformed into tokens:

- `logic:*`
- `pattern:*`
- `environment:*`
- `stage:*`

Then those tokens are matched against the components of `quality_paths`:

- overlap `>= 2` means a strong match
- overlap `>= 1` with at most 2 query tokens means a weak match

Matched paths are ranked by:

1. `overlap_count`
2. `ucb_score`
3. `positive_edge_score`

At the same time, the reminder layer also:

- matches positive genes -> "reusable reminders"
- matches risk genes -> "risk reminders"
- extracts recurring discipline / emotion / mistake / review problems -> "habit risk reminders"

So the final output is not "buy" or "sell". It is:

1. which historical path is worth reviewing first
2. which recurring problem should be suppressed first
3. which reflective question should be asked before execution

## 9. What the System Is Actually Optimizing

The current algorithm is not trying to optimize an autonomous profit-maximizing policy. It is optimizing something more realistic:

- increase the chance of reusing strong historical behavior
- expose discipline / emotion / mistake risks earlier
- provide bounded reminders even when the data is still incomplete

So the system behaves more like:

- a personal experience ranker
- a recurring-risk interception layer
- a conversational review assistant

rather than an automated trading engine.

## 10. Current Boundaries

The present implementation has clear limits:

1. "trajectory" is still a trade-level compression, not an intraday sequence
2. path components are intentionally sparse and only use summary fields such as the first logic tag or first pattern tag
3. `positive_edge_score` and the risk scores are heuristics, not formal significance tests
4. bandit outputs rank reminders; they do not execute policy
5. with a very small sample size, any "advantage path" is only weak evidence

## 11. What Is Needed Before Upgrading to Offline RL

If trajectory self-evolution is later upgraded into a real trajectory policy, the system will need at least:

- intraday state snapshots
- action sequences such as add, trim, take-profit, stop-loss, cancel
- finer-grained reward definitions
- explicit constraints for cost, drawdown, and position limits
- a sufficiently long and diverse offline trajectory library

Only then does it make sense to seriously consider:

- Decision Transformer
- IQL
- other conservative offline RL routes

## 12. Bottom Line

In one sentence:

> Finance Journal currently defines the trajectory self-evolution problem as a personal decision augmentation problem built on trade-level trajectory signatures, bandit-style ranking, and reminder-first outputs.

That is why the current system emphasizes:

- recording each trade completely
- preserving emotion / mistake / review signals
- making the next decision more reviewable than the previous one

instead of packaging the framework as an automated strategy engine.
