---
name: vestafolio-lmnp-fiscalite
version: 1.2.1
description: Compare LMNP furnished-rental taxation between micro-BIC and régime réel with amortization using Vestafolio's simulator API, after asking the simulator's questions (furnished or not, rents, type of meublé, purchase price, notary fees, furniture, works, TMI, annual charges). Use when a user asks "LMNP micro-BIC ou réel", how furnished rental income is taxed in France, about the 50 % / 30 % abattement, meublé de tourisme thresholds, building/furniture amortization, or which LMNP regime saves more tax.
---

# LMNP : micro-BIC vs régime réel (Vestafolio)

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

Compares the taxation of a location meublée non professionnelle (LMNP) under
the micro-BIC (flat abattement) and the régime réel (real charges plus
amortization), with the recommended regime, annual and 10-year savings, and a
10-year amortization schedule. The rules below are the ones coded in the
simulator; use them to explain, and the API to compute.

## When to use

- "LMNP micro-BIC ou réel ?" / "Which tax regime for my furnished rental?"
- Questions about the micro-BIC abattement and thresholds, or meublé de
  tourisme classé vs non classé
- Estimating amortization (immeuble, mobilier, travaux) and its tax effect

## When NOT to use

- Unfurnished (nue) rentals — use vestafolio-micro-foncier-vs-reel
- Professional furnished landlords (LMP) — only LMNP is modeled
- Capital gains on the sale of the LMNP property (use
  vestafolio-impot-plus-value)

## Questions to ask before calling the API

The simulator opens with a gate, then one form. Ask or confirm each in
French; do not assume a default for a question marked (gate).

1. « Votre bien est-il loué meublé ? » (gate) — « Oui, location meublée » /
   « Non, location nue (vide) ». For a location nue the site refuses to
   compute and redirects to the micro-foncier simulator: switch to
   vestafolio-micro-foncier-vs-reel. (Reminder shown by the site: « Une
   location meublée doit comporter au minimum les équipements définis par le
   décret n°2015-981. »)
2. « Loyers annuels » → `annualRent` (charges comprises).
3. « Type de location » (gate) → `propertyType`: « Meublé classique
   (abattement 50%) » = `standard`, « Meublé tourisme classé (abattement
   50%) » = `tourisme_classe`, « Meublé tourisme non classé (abattement
   30%) » = `tourisme_non_classe`. It sets the micro-BIC threshold: 83 600 €
   for the first two, 15 000 € for the last.
4. « Prix d'achat (hors crédit) » → `purchasePrice`, « Frais notaire » →
   `notaryFees`, « Mobilier » → `furnitureCosts`, « Travaux » →
   `renovationCosts` (the amortization bases).
5. « Tranche marginale (TMI) » → `marginalTaxRate`, one of 0, 11, 30, 41, 45
   (estimate it with vestafolio-impot-revenu if unknown).
6. « Charges annuelles » (the site opens this section by default) →
   `charges`: « Intérêts emprunt » `loanInterest`, « Taxe foncière »
   `propertyTax`, « Copropriété » `condoFees`, « Assurance PNO »
   `insurance`, « Gestion » `managementFees`, « Comptable » `accounting`,
   « Entretien » `entretien`. Ask for each; use 0 when the user has none.

## Rules and rates as coded in the simulator (Loi de Finances 2025)

- Micro-BIC: abattement 50 % (standard, tourisme classé) or 30 % (tourisme
  non classé); eligible while the rents are at or below the threshold
  (83 600 € or 15 000 €). Above it the réel is imposed.
- Régime réel: result before amortization = rents − all charges;
  amortization = (purchase price + notary fees) × 85 % / 30 years (the 15 %
  land share is not amortizable) + furniture / 7 years + works / 10 years;
  it is only used up to the positive result (never creates a deficit), the
  excess is carried forward.
- Both regimes: impôt = taxable income × TMI; prélèvements sociaux 18,6 % on
  the taxable income; net income = rents − charges − taxes (amortization is
  non-cash).
- Recommendation: `reel` when micro-BIC is ineligible, otherwise the regime
  with the strictly lower total tax (a tie recommends micro-BIC);
  `annualSavings` = absolute tax gap, `tenYearSavings` = × 10 with constant
  figures.
- Site wording: « Vos loyers dépassent le seuil Micro-BIC (…). Le régime
  réel est obligatoire. », « Économie annuelle : X / Sur 10 ans : Y », or
  « Les deux régimes sont équivalents pour votre situation. »

## How to call the API

Always fetch the canonical input schema first (fields, bounds, defaults):

```
GET https://www.vestafolio.com/api/tools/v1/lmnp-fiscalite
```

Then POST the user's parameters (all amounts annual and in euros, TMI in
percent):

```bash
curl --fail-with-body --silent --show-error --max-time 30 -X POST https://www.vestafolio.com/api/tools/v1/lmnp-fiscalite \
  -H 'Content-Type: application/json' \
  -d '{
    "annualRent": 15000,
    "propertyType": "standard",
    "purchasePrice": 200000,
    "notaryFees": 16000,
    "furnitureCosts": 8000,
    "renovationCosts": 10000,
    "marginalTaxRate": 30,
    "charges": {
      "loanInterest": 4000,
      "propertyTax": 1200,
      "condoFees": 1800,
      "insurance": 200,
      "managementFees": 0,
      "accounting": 500,
      "entretien": 300
    }
  }'
```

Unknown fields are rejected (strict schema) — if you get a `validation_error`,
re-read the schema from the GET endpoint rather than guessing field names.

## Interpreting the output

- `recommendation` — `micro_bic` or `reel`; check `microBic.isEligible` /
  `eligibilityReason` to say whether the réel was imposed
- `annualSavings` and `tenYearSavings` — lead with these when answering
  "which regime"
- Per-regime blocks (`microBic`, `reel`): `taxableIncome`, `incomeTax`,
  `socialContributions`, `totalTax`, `netIncome`, `effectiveRate`
- `details` — abattement and threshold in micro-BIC; charges, per-asset
  amortization (`buildingAmort`, `furnitureAmort`, `renovationAmort`),
  `usedAmort` vs `carriedAmort` in réel (the site shows « X d'amortissements
  reportés (revenu déjà à 0) »)
- `amortizationSchedule` — 10-year plan (furniture stops after year 7);
  a large `cumulativeCarried` means the réel advantage persists beyond year 10

## Caveats

- Rules as coded per the Loi de Finances 2025; thresholds and abattements
  change with finance laws. Estimates, not tax advice — say so.
- Assumes constant rents and charges over the 10-year projection; accounting
  fees for the réel are an input, not automatic.
- Amortization deducted au réel is reintegrated into the capital gain on sale
  (since 2025) — point users to vestafolio-impot-plus-value for exit planning.
- Interactive simulator, if useful to the user:
  https://www.vestafolio.com/simulateurs/lmnp-fiscalite
