# Run

Inventory, deploy, pilot, set the lines, enable and report. Nothing in this repository deploys.

## Phase handoffs

Every message names the current phase and ends with `Next step`. A phase-boundary handoff carries
the evidence the operator needs, one concrete approval request, what approval unlocks, and what
stays blocked. An in-progress update says `No action needed` and names the next checkpoint.

## Inventory

What Account Events already holds, before anything is weighed. Read-only and free:

```sql
SELECT
  model_slug,
  event_name,
  JSON_VALUE(properties, '$.signal_type') AS signal_type,
  COUNT(*) AS events,
  COUNT(DISTINCT account_id) AS accounts,
  MAX(occurred_at) AS latest
FROM object.account_events
GROUP BY 1, 2, 3
ORDER BY events DESC
```

```sh
cargo-ai storage query execute "<the query>"
```

Each row is a candidate key for `signals` in `infra/settings.ts`: the `signal_type` when it is set
(Cargo Signals events), the `model_slug` when it is not (first-party models). The score uses the
same rule. A model the team expects and does not see here does not unify as an account event yet.

Then the repeats: the same signal, on the same account, on the same day.

```sql
SELECT signal_type, copies, COUNT(*) AS account_days
FROM (
  SELECT
    account_id,
    COALESCE(JSON_VALUE(properties, '$.signal_type'), model_slug) AS signal_type,
    TIMESTAMP_TRUNC(CAST(occurred_at AS TIMESTAMP), DAY) AS day,
    COUNT(*) AS copies
  FROM object.account_events
  GROUP BY 1, 2, 3
)
WHERE copies > 1
GROUP BY 1, 2
ORDER BY account_days DESC
```

The score sums rows, so every copy counts. For a type that happens many times a day (sessions,
activity) that is the point. For a one-off signal (a round, a job post) a copy is the same event
delivered twice, and an account with six copies of one round scores it six times; the feed settings
stop new copies, not the ones already in the history. Go through the one-off types with the
operator before weighing them: the fix is at the source that wrote them twice, never an edit to
Account Events.

## Deploy, play disabled

1. `node --import tsx evals/contract.mjs` from this skill's folder, against the adapted resources.
2. `cargo-ai project types`, then `cargo-ai project check`, then `cargo-ai project plan` from the
   project root. Inspect every resource.
3. Confirm the plan shows `account_events` and `accounts` adopted (updates, not creates) with their
   schedules, `account_events` gaining `readiness_contribution` and `accounts` gaining
   `readiness_score` and `readiness_stage`, **and neither losing a column**. Then the feeds on a
   watchlist of the accounts model, the two segments, and the play with `isEnabled: false` and
   `changeKinds: ["added"]`. A column removal on either unify model means a live column was not
   carried into the declaration: stop and add it.
   If the deploy stops on "no relationship between id on this model and account_id", Account Events
   has never synced in this workspace: sync it once (`cargo-ai storage run create --model-uuid <accountEventsUuid>`) and deploy
   again.
4. Read each feed's current per-event price (`cargo-ai connection integration get cargoSignals`) and
   give the operator the estimate described in SKILL.md, _What it costs_.
5. Deploy only on the operator's yes.

Resolve `workspaceUuid` from `cargo-ai whoami` and resource UUIDs from `cargo.state.json`. Links are
`https://app.getcargo.io/workspaces/<workspaceUuid>/<models|plays|segments>/<uuid>`.

## Pilot

The feeds deliver over the first days. Once Account Events (:00) and Unify Accounts (:10) have
rebuilt, read the distribution:

```sql
SELECT computed__readiness_stage AS stage, COUNT(*) AS accounts,
  MIN(metric__readiness_score) AS min_score, MAX(metric__readiness_score) AS max_score
FROM object.accounts
WHERE metric__readiness_score > 0
GROUP BY 1
```

the top of the list:

```sql
SELECT id, domain, metric__readiness_score AS score, computed__readiness_stage AS stage
FROM object.accounts
ORDER BY metric__readiness_score DESC
LIMIT 20
```

and, for any account, the events behind its score:

```sql
SELECT occurred_at, COALESCE(JSON_VALUE(properties, '$.signal_type'), model_slug) AS signal,
  computed__readiness_contribution AS contribution
FROM object.account_events
WHERE account_id = '<id>' AND computed__readiness_contribution > 0
ORDER BY contribution DESC
```

Check by hand:

- every weighed type in `signals` has events with a contribution above 0; one that never does has
  no events
- the top ten read right to someone who knows the accounts. When they do not, change the weights
  (`weights.md`, _Checking them_), not the threshold
- an account with only old events sits below one with the same events fresh
- one round is one event: an account whose top contributions are the same signal on the same day
  is a feed delivering per contact (`maxLeadsPerCompany`) or two feeds carrying one type

## Set the lines

Pick `readyThreshold` so `ready_now` holds the number of accounts the team can act on in a week,
and `warmingThreshold` at about one fresh mid-weight signal below it. Edit `infra/settings.ts`,
plan, deploy, and read the distribution again at the next rebuild. A threshold set before the pilot
is a guess: on one workspace the defaults put several hundred accounts in `ready_now`.

## Enable

Set `isEnabled: true` on the play, plan, and deploy. From the next tick, every account entering
`ready_now` is posted once. The accounts already in `ready_now` are not posted
(`changeKinds: ["added"]`); if the team wants them, execute the play once by hand.

Storage SQL lags a sync by a few minutes (the result says `"isRefreshing": true`), so an empty
result straight after a deploy is the lag, not a failed model.

## Report

- the stage distribution and the thresholds chosen
- the top five accounts with the events behind their score
- events delivered per feed over the pilot, and actual credits against the estimate
- direct Cargo links to Unify Accounts, the two segments and the play

End with one recommended `Next step`:

- the top is one signal type: lower its weight or filter its feed
- a hot account scores low: its events are missing from Account Events; find the model
- a healthy list: sequence `ready_now_accounts`, or add the account-scoring fit gate

## Complete when

- the inventory was run, and every weighed key matches it or a feed this deploy added
- the plan showed the play disabled, and the operator approved the deploy and the feed estimate
- the thresholds were set from the pilot distribution, and the top ten were read by hand
- the play is enabled and the first ready account was posted once
- the report gave the distribution, the top accounts, actual credits and one next step
