---
name: vestafolio-pea-vs-cto
version: 1.2.1
description: Compare PEA, CTO (compte-titres) and assurance-vie net-of-tax outcomes for a French investor using Vestafolio's simulator API, after asking the simulator's questions (initial capital, monthly contribution, TMI, holding period, expected return, assurance-vie fees). Use when a user asks which investment envelope to choose, about PEA vs CTO taxation, flat tax (PFU) on investments, assurance-vie abattement, the 150 000 € PEA ceiling, or where to invest monthly savings in France.
---

# PEA vs CTO vs Assurance-vie (Vestafolio)

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

Computes the net-after-tax capital of the same investment plan (initial amount +
monthly contributions) held in a PEA, a CTO or an assurance-vie, with
year-by-year projections, break-even years, warnings and a recommendation.
The rules below are the ones coded in the simulator; use them to explain,
and the API to compute.

## When to use

- "Should I invest through a PEA or a CTO?" / "PEA ou assurance-vie ?"
- Comparing net outcomes of French investment envelopes over N years
- Questions about the PEA 150 000 € ceiling, PFU, or assurance-vie abattement

## When NOT to use

- Non-French tax residents (the rules are France-specific)
- Real-estate investing (use the immobilier skills instead)
- Pure compound-interest math without tax (use vestafolio-interets-composes)

## Questions to ask before calling the API

The simulator asks these inputs, in this order (card « Paramètres
d'investissement »). Ask or confirm each in French before computing.

1. « Capital initial » → `initialInvestment`. Simulator warning above
   150 000 €: « Le plafond de versement PEA est de 150 000 €. L'excédent
   devra être placé en CTO. »
2. « Versement mensuel » → `monthlyContribution`.
3. « Tranche marginale d'imposition (TMI) » (gate) → `marginalTaxRate`, one
   of « 0% (jusqu'à 11 600 €) », « 11% (de 11 601 € à 29 579 €) », « 30% (de
   29 580 € à 84 577 €) », « 41% (de 84 578 € à 181 917 €) », « 45% (au-delà
   de 181 917 €) » — the bounds are the quotient familial per part. It only
   drives the CTO barème option, so ask it before comparing PEA and CTO.
4. « Durée de détention » (gate) → `holdingPeriodYears` (1 to 50). Below 5
   years the simulator warns « Avant 5 ans, le PEA perd son avantage fiscal »
   and switches to the « Horizon court : fiscalité identique » verdict.
5. « Rendement annuel estimé » → `annualReturn` (percent, 0 to 15 on the
   site).
6. « Frais de gestion assurance vie » → `avManagementFees` (percent per year;
   simulator helper: « Courtiers en ligne : 0,5-0,8%. Banques : 0,8-1,5%. »).
7. `isCouple` — the web simulator does not ask it and always uses the single
   4 600 € assurance-vie abattement; the API accepts it. Ask « Êtes-vous en
   couple soumis à imposition commune ? » whenever the horizon is 8 years or
   more (the abattement doubles to 9 200 €), and say that the website assumes
   a single declarant.

## Rules and rates as coded in the simulator (2026)

- Gross capital: monthly compounding of `annualReturn` / 12 on the initial
  amount and the monthly contributions; the assurance-vie compounds at
  return − fees.
- PEA: 18,6 % prélèvements sociaux on gains; before 5 years also 12,8 % IR
  (PFU 31,4 % in total).
- CTO: 18,6 % PS plus the cheaper of 12,8 % IR (PFU) or gains × TMI (barème
  option, no abattement) — at TMI 0 % the CTO equals the PEA after 5 years
  and `taxSavings` is 0.
- Assurance-vie: before 8 years 12,8 % IR + 17,2 % PS (30 %); from 8 years,
  17,2 % PS on the whole gain and 7,5 % IR on the gain above the abattement
  (4 600 €, 9 200 € with `isCouple`), 12,8 % instead of 7,5 % when the
  contract value exceeds 150 000 €.
- PEA ceiling: 150 000 € of total contributions (initial + monthly × 12 ×
  years). Above it the `allocation` block splits the plan into a PEA up to
  the ceiling and a CTO for the surplus (`combinedCapitalNet`) and a warning
  is issued.
- `breakEvenYears`: first year ≥ 5 where the PEA net value beats the CTO;
  `avBreakEvenYears`: first year ≥ 8 where the assurance-vie beats the CTO.
- `recommendation` is rule-based, not a net-capital ranking: `both` (PEA +
  CTO) when the horizon is under 5 years or the ceiling is exceeded,
  otherwise `pea`; it never returns `cto` or `av`. The website states the
  same: from 5 years « le PEA permet une économie de X par rapport au CTO
  (18,6% PS vs PFU 31,4%) » (or « le PEA et le CTO sont équivalents » when
  `taxSavings` is 0) and, from 8 years, « L'assurance vie bénéficie aussi
  d'un abattement après 8 ans, mais les frais de gestion réduisent
  l'avantage ». It then highlights the envelope with the highest net
  capital — compare `capitalNet` of the three yourself and say which is
  highest.
- Warnings (French, in `warnings`): total contributions above the ceiling,
  horizon under 5 years (PEA taxed like the CTO), horizon under 8 years
  (assurance-vie at PFU 30 %, abattement only after 8 years).

## How to call the API

Always fetch the canonical input schema first (fields, bounds, defaults):

```
GET https://www.vestafolio.com/api/tools/v1/pea-vs-cto
```

Then POST the user's parameters (all amounts in euros, rates in percent):

```bash
curl --fail-with-body --silent --show-error --max-time 30 -X POST https://www.vestafolio.com/api/tools/v1/pea-vs-cto \
  -H 'Content-Type: application/json' \
  -d '{
    "initialInvestment": 10000,
    "monthlyContribution": 300,
    "holdingPeriodYears": 10,
    "annualReturn": 7,
    "marginalTaxRate": 30,
    "avManagementFees": 0.6,
    "isCouple": false
  }'
```

Unknown fields are rejected (strict schema) — if you get a `validation_error`,
re-read the schema from the GET endpoint rather than guessing field names.
`marginalTaxRate` must be exactly 0, 11, 30, 41 or 45.

## Interpreting the output

- `pea`, `cto`, `av` — `capitalFinal`, `totalGains`, `taxOnGains`,
  `socialContributions`, `totalTax`, `capitalNet` (the comparison figure),
  `effectiveTaxRate`
- `taxSavings` — PEA tax saving versus the CTO (negative if the CTO wins);
  `avSavingsVsCTO` — CTO net minus assurance-vie net
- `allocation` — the PEA + CTO split when `exceedsCeiling` is true; present
  `combinedCapitalNet` instead of `pea.capitalNet` in that case, as the site
  does
- `recommendation`, `breakEvenYears`, `avBreakEvenYears` — see the rules
  above; highlight the 5-year and 8-year thresholds when the horizon is near
- `projections` — year-by-year net values, for "what if I stop after N years"
- `warnings` — relay them in French

## Caveats

- Rules as coded for 2026 (18,6 % PS on PEA and CTO, 17,2 % on the
  assurance-vie); rates change with finance laws. Not tax advice — say so.
- The simulation assumes constant returns and contributions, and a lump-sum
  withdrawal at the end of the horizon.
- The website also reminds users that a PEA only holds European equities and
  eligible funds, that a CTO has no ceiling, and that the assurance-vie adds
  a 152 500 € per-beneficiary transmission abattement not modeled here.
- Interactive simulator, if useful to the user:
  https://www.vestafolio.com/simulateurs/pea-vs-cto
