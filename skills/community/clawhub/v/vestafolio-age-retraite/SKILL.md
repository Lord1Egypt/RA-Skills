---
name: vestafolio-age-retraite
version: 1.2.1
description: Simulate early retirement (FIRE) financed by invested capital for a French saver using Vestafolio's simulator API, after asking the simulator's questions (current situation, mortgage, target age, complementary income, lifestyle at retirement). Use when a user asks "à quel âge puis-je arrêter de travailler", "quand serai-je financièrement indépendant", at what age they can retire early, how much capital they need for FIRE, whether their savings will last, or how part-time income and expense cuts change their retirement age.
---

# Âge de retraite anticipée / FIRE (Vestafolio)

## Required workflow

For a request within this simulator's scope:

1. Reuse answers already supplied. Ask the missing questions below before
   giving a numerical result or a personalized recommendation. Example values
   and schema defaults are not the user's answers.
2. Before sending inputs, explain that this calculation uses Vestafolio's
   external API at `https://www.vestafolio.com`, summarize the fields and
   values to be sent, and obtain the user's agreement. Existing explicit
   approval for this destination and data scope is sufficient; do not ask
   again for calls it already covers. Installing or selecting the skill alone
   is not approval to transmit personal data. If the user declines, do not
   POST; offer the simulator link for manual use without prefilled inputs.
3. Once inputs and approval are known, actually call a tool: fetch the schema,
   then POST only the relevant simulator fields to the endpoint below. Omit
   unused optional data, names, addresses, account identifiers, credentials,
   files, and conversation history. No authentication is needed. Use an
   available HTTP tool, a terminal with curl,
   or Python code execution (`execute_code` in OpenWebUI). Python can use
   `urllib.request`; in browser-based Pyodide use `await pyfetch(...)` from
   `pyodide.http`. A Python environment does not need a shell to call the API.
4. Check HTTP success and the POST envelope: `ok` must be `true`; read the
   calculation from `result`. Ground the answer in that output, state relevant
   assumptions and limits. Offer the simulator link when useful for checking
   assumptions or exploring alternatives; respect requests for no links.

Writing a code block is not execution. Do not substitute mental arithmetic,
remembered tax rules, or the worked example for a tool result. If execution
or network access is unavailable, or the API fails, say the calculation could
not be completed and provide the simulator link; do not invent its result or
recommendation. A schema GET alone is not a completed simulation.

## Response language

Reply in French whenever the user speaks or writes in French.

Simulates a capital-funded early retirement: year-by-year accumulation of
savings until the target retirement age (salary, expenses, mortgage,
investment returns), then withdrawals through retirement up to a life
expectancy of 86, with the required capital, goal status and improvement
levers. The model below is the one coded in the simulator; use it to
explain, and the API to compute.

## When to use

- "À quel âge puis-je arrêter de travailler ?" / "At what age can I retire early?"
- FIRE questions: capital needed, whether current savings + monthly surplus
  suffice, how long the capital lasts
- "What if I work 2 more years / cut expenses / keep a side gig?" follow-ups

## When NOT to use

- Statutory French pension rights (trimestres, âge légal, pension amounts) —
  this is a pure capital-drawdown simulation
- Choosing an investment envelope (use vestafolio-pea-vs-cto)
- Non-capital questions like budgeting alone

## Questions to ask before calling the API

The simulator asks these inputs, in this order. Ask or confirm each in
French; do not assume a default for a question marked (gate).

« Situation actuelle »

1. « Épargne disponible actuellement » → `currentSavings` (invested capital
   today).
2. « Salaire net mensuel » → `monthlyNetSalary`.
3. « Autres revenus (mensuel) » → `otherMonthlyIncome` (« Revenus locatifs,
   freelance, etc. »). Counted before retirement only — income kept after
   retirement must be entered again in question 11.
4. « Augmentation annuelle des revenus » → `annualSalaryIncrease` (%, applies
   to salary and other income).
5. « Dépenses mensuelles courantes » → `currentMonthlyExpenses` (« Ne pas
   inclure de crédit immobilier »).
6. « Mensualité de prêt immobilier » → `monthlyMortgagePayment` and, if it is
   > 0 (gate), « Nombre d'années restantes pour le prêt » →
   `remainingMortgageYears` (the site refuses a payment without a duration).
   The mortgage keeps being paid after retirement until it ends.
7. « Âge actuel » → `currentAge`.

« Projection »

8. « Âge de départ souhaité » (gate) → `desiredRetirementAge`, at least the
   current age (the API clamps it; the site shows an error).
9. « Rendement annuel des investissements avant fiscalité » →
   `annualInvestmentReturn` (%).
10. « Revenu complémentaire » (gate) → `hasPartTimeActivity` (Oui/Non; the
    site defaults to Oui with 600 €, so ask).
11. Only if Oui: « Revenu complémentaire (mensuel) » → `partTimeMonthlyIncome`
    (« Loyers perçus, pension, temps partiel »), « Hausse annuelle des
    revenus » → `annualPartTimeIncomeIncrease` (%), « Âge auquel ces revenus
    cessent » → `partTimeIncomeEndAge` (at least the retirement age; the API
    clamps it). If Non, send `partTimeMonthlyIncome: 0`.
12. « Maintien du niveau de vie » (gate) → `maintainLifestyle`. Only if Non:
    « Dépenses mensuelles courantes révisées » → `revisedMonthlyExpenses`
    (monthly expenses targeted at retirement). If Oui, send the current
    expenses in `revisedMonthlyExpenses` as well.

## Model as coded in the simulator

- Before retirement, each year: income = (salary + other income) × 12 grown
  by `annualSalaryIncrease` since today; expenses = current expenses × 12
  inflated at 3 %/year since today; mortgage = payment × 12 while years
  remain; net savings are added to the capital, which earns
  `annualInvestmentReturn` on the opening balance. A negative net saving is
  withdrawn grossed-up for tax.
- In retirement, each year until age 86: expenses (current or revised) × 12
  inflated at 3 %/year since today, plus the remaining mortgage, minus the
  complementary income (grown by its own rate since today, while the age is
  below `partTimeIncomeEndAge`); the shortfall is withdrawn from the capital
  grossed-up so that 31,4 % (PFU majoré: 12,8 % IR + 18,6 % PS) is paid on
  the withdrawal; a surplus is saved.
- `objectiveReached` = the capital never goes negative until 86 and the
  capital at retirement is at least `capitalNecessary` (the smallest capital
  that survives until 86, found by bisection).
- `sustainableUntilAge` extends the drawdown to 120 (`…IsCapped` when it
  lasts that long).
- `improvement` levers when the goal is missed, each on its own: extra work
  years to the first achievable retirement age (null if none before 86), the
  monthly expense cut that would make the goal reachable, or the number of
  years of a 800 €/month complementary income.

## How to call the API

Always fetch the canonical input schema first (fields, bounds, defaults):

```
GET https://www.vestafolio.com/api/tools/v1/age-retraite
```

Every field has a default, so a minimal call with just the user's key numbers
works — but confirm the defaults match their situation (notably the 600 €
complementary income). Then POST (amounts in euros, rates in percent):

```bash
curl --fail-with-body --silent --show-error --max-time 30 -X POST https://www.vestafolio.com/api/tools/v1/age-retraite \
  -H 'Content-Type: application/json' \
  -d '{
    "currentSavings": 120000,
    "monthlyNetSalary": 3500,
    "otherMonthlyIncome": 0,
    "annualSalaryIncrease": 1,
    "currentMonthlyExpenses": 1800,
    "monthlyMortgagePayment": 800,
    "remainingMortgageYears": 10,
    "currentAge": 40,
    "desiredRetirementAge": 53,
    "annualInvestmentReturn": 7,
    "hasPartTimeActivity": true,
    "partTimeMonthlyIncome": 600,
    "annualPartTimeIncomeIncrease": 1,
    "partTimeIncomeEndAge": 65,
    "maintainLifestyle": false,
    "revisedMonthlyExpenses": 1600
  }'
```

Unknown fields are rejected (strict schema) — if you get a `validation_error`,
re-read the schema from the GET endpoint rather than guessing field names.

## Interpreting the output

- `objectiveReached` — the headline verdict (site badge « Objectif atteint »
  / « Objectif non atteint »)
- `capitalAtRetirement` vs `capitalNecessary` — projected capital at the
  target age vs the capital actually required; `completionPercent` is their
  ratio (« Progression vers le capital nécessaire »)
- `sustainableUntilAge` — « Vous pouvez vivre de votre rente jusqu'à » N ans
  (« et + » when `sustainableUntilAgeIsCapped`)
- `improvement` — relay the levers as the site does (« Âge de départ
  atteignable », « Réduction de vos dépenses mensuelles », « 800 €/mois en
  revenu complémentaire »), saying « Non atteignable avec ce seul levier »
  for a null value
- `preRetirementProjection` / `retirementProjection` — year-by-year series
  for "what happens at age N" follow-ups; `minClosingCapital` below zero
  pinpoints when savings run out; the first retirement year with
  complementary income gives the monthly transition balance the site shows
- `inputs` — the normalized values actually used (ages clamped)

## Caveats

- Constant assumptions (returns, salary growth, 3 % expense inflation, flat
  31,4 % tax on withdrawals) — real sequences of returns and future tax law
  will differ. Estimates, not financial advice — say so.
- Ignores statutory pension income; from the légal retirement age onward the
  real situation is usually better than simulated.
- Interactive simulator, if useful to the user:
  https://www.vestafolio.com/simulateurs/age-retraite
