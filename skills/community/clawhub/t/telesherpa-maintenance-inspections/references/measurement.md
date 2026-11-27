# Measurement of a paid test run

How a **fresh agent's** build of this skill on a **pay-per-use** account is measured.
The run follows [acceptance-scenario.md](acceptance-scenario.md); this file defines
what is logged and how. One run is a sample — claim "an agent builds this alone"
only after a second run by another agent with comparable numbers.

## 1. Preconditions

| Item | Rule |
|---|---|
| Billing model | `onto_credit_balance` → `billing_model` is pay-per-use. Flat accounts book nothing; a run on them measures nothing. |
| Credit cap | approved before the start; default **2 × the estimate** you derive from the live price table (section 3). Reaching the cap = stop and ask. |
| Run id | `<date>-<agent name>-<n>`, plus the object prefix `TEST-A-`; every log row carries the run id. |
| Price table | `onto_credit_pricing` read at the start, saved with date and time (Europe/Berlin). That table wins. |
| Clock | all times in Europe/Berlin with zone label; tool times in UTC are converted. |
| Fresh agent | no memory of earlier runs; it gets only this skill, the platform skill, the shift-planning skill (for reuse) and the intake answers. |

## 2. Stop criteria

- **3 consecutive failed attempts** at the same step → stop and ask; log the step.
- Credit cap reached, or a single phase above 2 × its estimate → stop and ask.
- Any stop point of [SKILL.md](../SKILL.md) (missing type, platform fault, unclear
  intake) → stop, file the service request, log the wait.
- HTTP 402 is **not** a failure of the agent if the top-up follows at once; log
  it as an intervention of kind `credits` only if a human had to act.

## 3. Credits per phase

Read `onto_credit_balance` of the **manager account** before and after each
phase. The difference is the phase cost. Also count the calls by price key to
explain the difference.

Estimates below are **order-of-magnitude only**, because reuse of an existing
master / team door changes the scope price. Derive a cap from the live table
before you start; then fill the actuals.

| Phase | Main costs (live keys) | Provisional estimate |
|---|---|---|
| 0 | new scopes at the volume price; property definitions; reads | the live price of the scopes you actually create, plus a small margin for reads and definitions |
| 1 | people / assets / service orders (`create_object`), links (`create_link`) | log after the first batch; twelve duties plus assets and one site is the ExampleWorks size |
| 2 | view, form, function, trigger and action definition writes, browser form saves (record inspection, report defect), reads | count the writes and form saves you actually run |
| Total | | set the cap at twice the sum you calculated from the live table |

Log operating costs of a live workspace only after you have measured a
pay-per-use period; do not invent a monthly figure.

Template:

| Run id | Phase | Account | Balance before | Balance after | Spent | Calls by key | Estimate | Δ to estimate | Note |
|---|---|---|---|---|---|---|---|---|---|
| | 0 | manager | | | | | | | |
| | 1 | manager | | | | | | | |
| | 2 | manager | | | | | | | |

## 4. Time and interventions

Log wall-clock time per phase (Europe/Berlin), waits, and every human
intervention (kind: `credits`, `intake`, `login`, `other`).

## 5. After the run

Quote: total spent, cap, number of accepted steps (of 17), number of passed
negative tests (of 2), interventions, and whether existing shift-planning scopes
were reused. Do not publish live balances, account names or identifiers.
