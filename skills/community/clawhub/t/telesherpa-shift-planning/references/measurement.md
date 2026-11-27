# Measurement of a paid test run

How a **fresh agent's** build of this skill on a **pay-per-use** account is measured.
The run follows [acceptance-scenario.md](acceptance-scenario.md); this file defines
what is logged and how. One run is a sample — claim "an agent builds this alone" only
after a second run by another agent with comparable numbers.

## 1. Preconditions

| Item | Rule |
|---|---|
| Billing model | `onto_credit_balance` → `billing_model` is pay-per-use. Flat accounts book nothing; a run on them measures nothing. |
| Credit cap | approved before the start; default **2 × the estimate** (section 3). Reaching the cap = stop and ask. |
| Run id | `<date>-<agent name>-<n>`, plus the object prefix `TEST-A-`; every log row carries the run id. |
| Price table | `onto_credit_pricing` read at the start, saved with date and time (Europe/Berlin). |
| Clock | all times in Europe/Berlin with zone label; tool times in UTC are converted. |
| Fresh agent | no memory of earlier runs; it gets only this skill, the platform skill and the intake answers of [intake.md](intake.md). |

## 2. Stop criteria

- **3 consecutive failed attempts** at the same step (same goal, any error) → stop and
  ask; log the step.
- Credit cap reached, or a single phase above 2 × its estimate → stop and ask.
- Any stop point of [SKILL.md](../SKILL.md) (missing type, missing tool, platform
  fault, unclear intake) → stop, file the service request, log the wait.
- HTTP 402 on a staff account is **not** a failure of the agent if the top-up follows
  at once; log it as an intervention of kind `credits` only if a human had to act.

## 3. Credits per phase

Read `onto_credit_balance` of the **manager account and every staff account** before
and after each phase. The difference is the phase cost. Also count the calls by price
key (from the price table) to explain the difference.

Estimates — definition calls have no price key, so read your balance before and after to see what your run actually cost:

| Phase | Main costs | Estimate (credits) |
|---|---|---|
| 0 | three scopes at the volume price 100 + 80 + 80 = 260; reads | ~270 |
| 1 | ~33 shifts × (from-template run 20 + object 10 + links ~25 + publish run 20 ≈ 75) plus master objects and templates; open shift + staff instead ≈ 90–95 per shift | ~2,600 |
| 2 | requests (~55 each incl. links) and decisions (~75–80 for a swap incl. link moves), 4 requests, 3 absences | ~600 |
| 3 | account setup, transfers, staff reads; notifications free | ~100 (+ staff balances transferred, not spent) |
| 4 | staff records (5 × ~35), clocking 2 × 20, corrections 23 × 20 | ~700 |
| Total | | ~4,260 ≈ 43 EUR |

Cost per action (rule of thumb; your statement is the truth): 20 per action run + 10 per created object
+ 5 per link + 5 per comment effect (estimate) + 25 per `replace_link` (remove 20 +
create 5). Use it to explain the difference to the estimate.

Running costs of a business in operation (monthly) are not part of this file yet; they
will be documented after a measured pay-per-use test run.

Template:

| Run id | Phase | Account | Balance before | Balance after | Spent | Calls by key (`action` n, `create_object` n, `create_link` n, `read` n, …) | Estimate | Δ to estimate | Note |
|---|---|---|---|---|---|---|---|---|---|
| | 0 | manager | | | | | 110 | | |
| | 1 | manager | | | | | 2,600 | | |
| | 2 | manager | | | | | | | |
| | 2 | staff S1 | | | | | | | |
| | … | | | | | | | | |

Transfers to staff accounts are moved money, not spent money: log them separately
(`ontouser_team_transfer`, amount, key) and subtract nothing twice.

## 4. Model tokens and costs

Logged by the environment that runs the agent, not by the platform.

| Run id | Phase | Part (planning / configuration / test) | Model calls | Input tokens | Output tokens | Model cost (EUR) | Source (reported / estimate) |
|---|---|---|---|---|---|---|---|
| | 0 | planning | | | | | |
| | 0 | configuration | | | | | |
| | 0 | test | | | | | |

If the environment reports no tokens, fill "estimate" and say how it was estimated.
Never mix model cost and platform credits in one number; add them only in the
summary (section 8).

## 5. Planning vs. configuration vs. test

Every log entry is assigned to exactly one part:

| Part | Counts | Does not count |
|---|---|---|
| **Planning** | reading this skill, the platform skill and the intake; reads to understand the state (lists, `onto_type_show`, `onto_actiondef_list`, `onto_interface_show`); thinking and writing the plan | any write call |
| **Configuration** | every write call: scopes, types, properties, actions, forms, functions, triggers, views, start cards, accounts, rights, transfers, business objects | reads for checking |
| **Test** | smoke tests, acceptance steps, read-backs after writes, browser checks, negative tests | fixes (they are configuration) |

Time and tokens are split by the same rule. A write made during a test (e.g. a staff
clock-in) is **test**, but its credits are still logged in section 3.

## 6. Human interventions

A human intervention is any moment a human had to act or decide for the run to go on.

| Kind | Examples |
|---|---|
| `question` | the agent asked something the intake should have answered |
| `correction` | a human pointed out a wrong result or a wrong plan |
| `login` | browser login, code, captcha, password |
| `credits` | top-up, cap raised, payment |
| `platform` | operator or support action, service request answered |
| `browser check` | a human looked at a rendered view because the agent could not |

| Run id | Phase | Time (Europe/Berlin) | Kind | What | Waiting time (min) | Human effort (min) | Avoidable? (skill gap / platform gap / no) |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

## 7. Duration and failed attempts

| Run id | Phase | Start | End | Duration planning | Duration configuration | Duration test | Waiting (async, human) | Failed attempts (400 / 402 / 403 / timeout / wrong result) | Steps with 3 failures |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | |

Failed attempt = a call that returned an error **or** a write whose read-back did not
match the intended result. Log each with the step number, the error text and the fix.

| Run id | Step | Call | Error / wrong result | Fix | Attempts |
|---|---|---|---|---|---|
| | | | | | |

Waiting for asynchronous triggers (up to 5 minutes) is waiting time, not a failure.

## 8. Summary per run

| Run id | Credits total | Platform EUR | Model EUR | Total EUR | Duration total | Planning / configuration / test (%) | Interventions (n, min) | Failed attempts (n) | Acceptance passed (steps / negatives) |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | |

Verification items for every run:
- definition calls (properties, actions, views, triggers, functions, start cards)
  book no credits — the build is free;
- triggers and notifications booked nothing (confirmed before; re-check);
- staff accounts paid only their own action runs.
