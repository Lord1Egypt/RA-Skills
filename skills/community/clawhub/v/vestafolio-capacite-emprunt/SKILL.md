---
name: vestafolio-capacite-emprunt
version: 1.2.1
description: Estimate the maximum mortgage a French household can borrow from income, existing charges and the HCSF 35 % debt ratio using Vestafolio's simulator API, after asking the simulator's questions (net household income, fixed charges, rate, duration, insurance rate). Use when a user asks how much they can borrow, "combien puis-je emprunter", borrowing capacity (capacité d'emprunt), taux d'endettement, or what property budget their salary allows.
---

# Capacité d'emprunt (Vestafolio)

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

Estimates the maximum amount a household can borrow for a property purchase
from its net monthly income, existing charges, the envisaged loan rate and
duration, and the maximum debt ratio (taux d'endettement). The formula below
is the one coded in the simulator; use it to explain, and the API to compute.

## When to use

- "How much can I borrow with a 4 000 € salary?" / "Combien puis-je emprunter
  avec 4 000 € par mois ?"
- Questions about capacité d'emprunt, taux d'endettement or the HCSF 35 % rule
- Sizing a property budget before searching (combine with
  vestafolio-frais-notaire for the full acquisition cost)

## When NOT to use

- Computing the payment of an already-sized loan — use
  vestafolio-credit-immobilier
- Buy vs rent decisions — use vestafolio-achat-vs-location
- Rental-investment profitability — use vestafolio-rentabilite-locative

## Questions to ask before calling the API

The simulator asks these five inputs, in this order (card « Vos revenus et
charges »). Ask or confirm each in French.

1. « Revenus mensuels nets » → `monthlyIncome` (« Incluez tous les revenus du
   foyer »: net monthly income before tax of all borrowers).
2. « Charges mensuelles existantes » → `monthlyCharges` (« Uniquement les
   charges fixes : crédits en cours, pensions alimentaires, loyers.
   N'incluez pas les dépenses courantes (alimentation, loisirs...). »).
3. « Taux d'emprunt » → `rate` (percent; the site allows 0 to 10).
4. « Durée du prêt » → `years` (the site allows 5 to 25).
5. « Taux d'assurance emprunteur » → `insuranceRate` (« Taux annuel moyen :
   0,25% à 0,40% selon l'âge et l'état de santé »).
6. `debtRatio` — the website does not ask it and always applies the 35 %
   HCSF norm. Keep 35 unless the user explicitly wants to test another ratio.

## Formula as coded in the simulator

- Maximum payment (crédit + assurance) = income × debtRatio / 100 − charges.
  With no income, or charges already above the ratio, everything is 0.
- Insurance is computed on the initial borrowed capital: monthly insurance =
  loan × insuranceRate / 100 / 12, and sits inside the maximum payment.
- Maximum loan = maximum payment / (annuity factor of the monthly rate over
  years × 12 + monthly insurance rate) — the annuity formula inverted.
- `currentDebtRatio` = (charges + maximum payment) / income: by construction
  it equals the ratio (35 %) whenever something can be borrowed.
- Site disclaimer: « Calcul basé sur un taux d'endettement maximal de 35%
  (règles HCSF). Le montant final dépendra de l'analyse de votre dossier par
  la banque. »

## How to call the API

Always fetch the canonical input schema first (fields, bounds, defaults):

```
GET https://www.vestafolio.com/api/tools/v1/capacite-emprunt
```

Then POST the user's parameters (all amounts in euros, rates in percent):

```bash
curl --fail-with-body --silent --show-error --max-time 30 -X POST https://www.vestafolio.com/api/tools/v1/capacite-emprunt \
  -H 'Content-Type: application/json' \
  -d '{
    "monthlyIncome": 4000,
    "monthlyCharges": 300,
    "rate": 3.5,
    "years": 20,
    "insuranceRate": 0.3,
    "debtRatio": 35
  }'
```

Unknown fields are rejected (strict schema) — if you get a `validation_error`,
re-read the schema from the GET endpoint rather than guessing field names.

## Interpreting the output

- `maxLoan` — the headline number: maximum borrowable capital in euros
- `maxMonthlyPayment` — the payment ceiling implied by the debt ratio,
  insurance included (the site shows it as « Mensualité »)
- `monthlyInsurance` — estimated insurance share of that payment
- `currentDebtRatio` — debt ratio reached at that payment, in percent; only
  informative when existing charges already exceed the ratio
- To translate maxLoan into a property budget, add the apport and subtract
  frais de notaire (vestafolio-frais-notaire). The site also shows how the
  capacity moves with the duration (5 to 25 years) and with a rate
  negotiated 0,5 or 1 point lower — offer those variants.

## Caveats

- An estimate, not a bank pre-approval: banks also weigh reste à vivre, job
  stability, saut de charges and can derogate from the 35 % HCSF norm for a
  share of their production.
- Insurance modeled at a flat rate on initial capital; real quotes vary with
  age and health.
- Not financial advice — say so.
- Interactive simulator, if useful to the user:
  https://www.vestafolio.com/simulateurs/capacite-emprunt
