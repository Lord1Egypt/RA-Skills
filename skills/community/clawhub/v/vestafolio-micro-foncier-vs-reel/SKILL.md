---
name: vestafolio-micro-foncier-vs-reel
version: 1.2.1
description: Compare unfurnished rental taxation between micro-foncier and régime réel with déficit foncier using Vestafolio's simulator API, after asking the simulator's questions (unfurnished or not, gross rents, six charge lines, TMI, prior deficit). Use when a user asks "micro-foncier ou régime réel", how location nue rental income is taxed in France, about the 30 % abattement, the 15 000 € micro-foncier ceiling, déficit foncier imputation on global income, or which regime saves more tax on revenus fonciers.
---

# Micro-foncier vs régime réel (Vestafolio)

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

Compares the taxation of an unfurnished rental (location nue) under the
micro-foncier (flat 30 % abattement) and the régime réel (real charges and
déficit foncier), with the recommended regime, annual savings and the
break-even charges level. The rules below are the ones coded in the
simulator; use them to explain, and the API to compute.

## When to use

- "Micro-foncier ou régime réel ?" / "Which regime for my unfurnished rental income?"
- Questions about the 30 % abattement, the 15 000 € micro-foncier ceiling, or
  déficit foncier (creation, imputation, carry-forward)
- Estimating tax on revenus fonciers given real charges and loan interest

## When NOT to use

- Furnished rentals (LMNP) — use vestafolio-lmnp-fiscalite
- Property capital gains on sale (use vestafolio-impot-plus-value)
- Non-French rental income

## Questions to ask before calling the API

The simulator opens with a gate, then three tabs. Ask or confirm each in
French; do not assume a default for a question marked (gate).

1. « Votre bien est-il loué vide (non meublé) ? » (gate) — « Oui, location
   nue (vide) » / « Non, location meublée ». For a meublé the site refuses to
   compute and redirects to the LMNP simulator: switch to
   vestafolio-lmnp-fiscalite.
2. Tab « Revenus » — « Loyers bruts annuels » → `annualRent` (« Seuil
   micro-foncier : 15 000 € »; above it the site warns « Vous dépassez le
   seuil du micro-foncier »).
3. Tab « Charges » → `charges`: « Intérêts d'emprunt » `loanInterest`,
   « Taxe foncière » `propertyTax`, « Charges de copropriété » `condoFees`
   (non-recoverable), « Assurance PNO » `insurance`, « Frais de gestion »
   `managementFees`, « Travaux et réparations » `repairs`. Ask for each; the
   site's defaults (3 000 € interest, 1 200 € tax, 1 800 € copropriété…) are
   placeholders, not the user's figures. The site shows the charges ratio and
   the break-even (30 % of rents) next to them.
4. Tab « Situation fiscale » — « Tranche marginale d'imposition (TMI) »
   (gate) → `marginalTaxRate`, one of 0, 11, 30, 41, 45 (estimate it with
   vestafolio-impot-revenu if unknown), and « Déficit foncier antérieur » →
   `existingDeficit` (« Déficit foncier des années précédentes reportable sur
   les revenus fonciers pendant 10 ans. », 0 if none).

## Rules and rates as coded in the simulator (2025-2026)

- Micro-foncier: abattement 30 %, eligible while rents ≤ 15 000 €; taxable =
  70 % of rents.
- Régime réel: result = rents − the six charges. A prior deficit is imputed
  on a positive result (the remainder stays carried forward). When the
  result is negative, the deficit created is imputed on global income up to
  the loan-interest amount and at most 10 700 €; the rest is carried forward
  against future revenus fonciers for 10 years, and the taxable income is 0.
  The imputed part yields a saving of (TMI + 17,2 %) × amount, added to the
  réel net income.
- Both regimes: impôt = taxable × TMI; prélèvements sociaux 17,2 % on the
  taxable income.
- `breakEvenCharges` = 30 % of the rents: above it the réel taxes less.
- Recommendation: `regime_reel` when micro-foncier is ineligible, when the
  réel total tax is lower, or when a deficit is imputable on global income;
  otherwise `micro_foncier`. `annualSavings` = micro tax − réel tax, floored
  at 0.
- Site wording: « Régime réel obligatoire — Vos loyers dépassent le seuil de
  15 000 €. », « Régime réel recommandé / Micro-foncier recommandé — Économie
  de X/an » or « Régime le plus avantageux pour votre situation » when the
  saving is 0 (deficit case or tie).

## How to call the API

Always fetch the canonical input schema first (fields, bounds, defaults):

```
GET https://www.vestafolio.com/api/tools/v1/micro-foncier-vs-reel
```

Then POST the user's parameters (all amounts annual and in euros, TMI in
percent):

```bash
curl --fail-with-body --silent --show-error --max-time 30 -X POST https://www.vestafolio.com/api/tools/v1/micro-foncier-vs-reel \
  -H 'Content-Type: application/json' \
  -d '{
    "annualRent": 12000,
    "charges": {
      "loanInterest": 3000,
      "propertyTax": 1200,
      "condoFees": 1800,
      "insurance": 300,
      "managementFees": 0,
      "repairs": 500
    },
    "marginalTaxRate": 30,
    "existingDeficit": 0
  }'
```

Unknown fields are rejected (strict schema) — if you get a `validation_error`,
re-read the schema from the GET endpoint rather than guessing field names.

## Interpreting the output

- `recommendation` — `micro_foncier` or `regime_reel`; `microFoncier.isEligible`
  tells whether the réel was imposed by the 15 000 € ceiling
- `annualSavings` — yearly tax saved by the réel vs micro (0 if micro wins or
  when the réel is chosen for its deficit)
- `breakEvenCharges` — the charges level above which the réel becomes more
  advantageous; useful to explain the tipping point
- Per-regime blocks (`microFoncier`, `reel`): `deductions`, `taxableIncome`,
  `incomeTax`, `socialContributions`, `totalTax`, `netIncome`, `effectiveRate`
- `reel.deficit` — `resultBeforeDeficit`, `existingDeficitUsed`, `created`,
  `usedAgainstIncome` (« Imputé sur autres revenus ») and `carriedForward`
  (« Reporté sur années suivantes », which includes the unused prior deficit)

## Caveats

- Rules as coded for 2025-2026; ceilings and rates change with finance laws.
  Estimates, not tax advice — say so.
- The déficit foncier imputation is a one-year simplification: when a deficit
  is at stake, advise the user to confirm the split between global income and
  carry-forward with their accountant.
- Opting for the réel commits the taxpayer for several years in real life —
  the simulator compares a single year with constant figures.
- Interactive simulator, if useful to the user:
  https://www.vestafolio.com/simulateurs/micro-foncier-vs-reel
