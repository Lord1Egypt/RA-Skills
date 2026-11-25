# Acceptance

Walk every line. A checked template without an evidence-backed consumer adaptation is incomplete.

## Weights

- The inventory query ran on the live Account Events before anything was weighed, and its rows
  were shown to the operator.
- The repeats query ran too, and every one-off signal type it returned (a round, a job post) was
  shown to the operator before it was weighed.
- Every key in `signals` matches a `signal_type` or model slug from the inventory, or a feed this
  deploy adds. None was invented.
- The operator approved each weight and half-life, and the reasoning for the strongest one is
  recorded under `## Decisions`.

## Project

- The agent installed and read `cargo-project` before adapting.
- `account_events` and `accounts` are each declared once in the project, as `unifyAccountEvents`
  and `unifyAccounts`, and the plan shows them adopted, not created.
- Every additional column live on either model before the deploy is in its declaration, and the
  plan removes none.
- The watched accounts model unifies into Unify Accounts, and both feeds watch it on its domain
  column, with a `dailyLeadLimit`.
- `readiness_contribution` on Account Events reads the clock (`Date.now()`), decays by half-life,
  and returns 0 for unweighed types and for events past the horizon.
- `readiness_score` on Unify Accounts is the `SUM` of `computed__readiness_contribution` over the
  relationship Account Events generates, and `readiness_stage` is computed from the two
  thresholds.
- The fundraising feed delivers one lead per company.
- The three crons run in order: Account Events, Unify Accounts, the play.
- The play filters on `readiness_stage = ready_now` only, uses `changeKinds: ["added"]`, posts to one Slack
  channel id, and ships disabled.
- This skill declares no agent and no `defineContext`.
- `node --import tsx evals/contract.mjs`, `cargo-ai project types`, `cargo-ai project check` and
  `cargo-ai project plan` pass.

## Guided handoff

- Every substantive message names the current phase and ends with a `Next step` containing one
  concrete decision, what it unlocks, and what stays blocked.
- The weights phase ends on approving `signals`; the build phase on deploying with the play
  disabled at a stated feed estimate; the pilot on approving the thresholds and enabling the play.
- Nothing was deployed or enabled before its approval.

## Results

- After the first rebuilds, every account with a weighed event inside the horizon has a
  `readiness_score` and a `readiness_stage`.
- The thresholds came from the pilot distribution, and the top ten accounts were read by hand.
- The first account to cross the line was posted once, with its score and signals.
- The report gives the distribution, the top accounts, events and credits per feed against the
  estimate, and one recommended next step.

## Repository isolation

- This is one root skill. Supporting Markdown lives under `references/`, and no nested `SKILL.md`
  exists.
- No relative import leaves the skill folder.
- The template contains no credential, deployment command, customer data, or hard-coded price.
