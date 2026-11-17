---
name: vestafolio-interets-composes
version: 1.2.1
description: Project compound-interest growth of an investment with initial capital and monthly contributions using Vestafolio's simulator API, after asking the simulator's questions (initial capital, monthly contribution, duration, annual return, compounding frequency). Use when a user asks about intérêts composés, compound interest projections, how much recurring savings will grow over N years, or wants a year-by-year table of invested amounts versus gains.
---

# Intérêts composés (Vestafolio)

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

Projects the final value of an investment with an initial capital and monthly
contributions, at a chosen compounding frequency, returning total invested,
gains and a year-by-year evolution table.

## When to use

- "Combien vaudront mes intérêts composés dans 20 ans ?" / "How much will
  300 €/month grow to?"
- Producing a year-by-year invested-vs-gains table that matches the Vestafolio
  website exactly — you could do this math yourself, but the API guarantees a
  consistent table (same rounding, same compounding) as the simulator the user
  may open

## When NOT to use

- Anything involving French taxation of the gains (use vestafolio-pea-vs-cto)
- Loan amortisation or real-estate projections (other Vestafolio skills)

## Questions to ask before calling the API

The simulator asks these five inputs, in this order (card « Paramètres »).
Ask or confirm each in French; there is no conditional question.

1. « Capital initial » → `initialAmount`.
2. « Versement mensuel » → `monthlyContribution`.
3. « Durée » → `years` (the site allows 1 to 50).
4. « Rendement annuel » → `annualRate` (nominal percent; the site allows 0 to
   20).
5. « Capitalisation des intérêts » → `compoundingPeriod`: « Mensuelle » =
   `monthly`, « Trimestrielle » = `quarterly`, « Annuelle » = `yearly`.

## Model as coded in the simulator

- The nominal annual rate is divided by the number of periods per year (12,
  4 or 1); each period the balance grows by that rate and the contributions of
  the period (monthly amount × months in the period) are added at the end of
  it. No effective-rate conversion is made.
- `totalInvested` = initial + monthly × 12 × years; `gains` = total − invested.
- `yearlyEvolution` rounds invested, gains and total to the euro per year,
  starting with year 0.
- No tax and no fees: pure pre-tax compounding.

## How to call the API

Always fetch the canonical input schema first (fields, bounds, defaults):

```
GET https://www.vestafolio.com/api/tools/v1/interets-composes
```

Then POST the user's parameters (amounts in euros, rate in percent):

```bash
curl --fail-with-body --silent --show-error --max-time 30 -X POST https://www.vestafolio.com/api/tools/v1/interets-composes \
  -H 'Content-Type: application/json' \
  -d '{
    "initialAmount": 10000,
    "monthlyContribution": 300,
    "years": 20,
    "annualRate": 7,
    "compoundingPeriod": "monthly"
  }'
```

Unknown fields are rejected (strict schema) — if you get a `validation_error`,
re-read the schema from the GET endpoint rather than guessing field names.

## Interpreting the output

- `total` — final value (« Capital final »); `totalInvested` — sum of all
  contributions; `gains` — the compounding effect (« Plus-values »)
- `yearlyEvolution` — rounded per-year `invested`, `gains`, `total` (year 0 is
  the starting point); ideal for tables and "after N years" follow-ups
- The site also shows the gain as a percent of the invested amount

## Caveats

- Assumes a constant return and constant contributions — real returns vary.
- Pre-tax: no fiscalité applied (chain vestafolio-pea-vs-cto for the net
  result). Estimates, not investment advice — say so.
- Interactive simulator, if useful to the user:
  https://www.vestafolio.com/simulateurs/interets-composes
