---
name: vestafolio-rentabilite-locative
version: 1.2.1
description: Compute gross and net rental yield and monthly cash-flow for a French buy-to-let investment from acquisition cost, rent and annual charges using Vestafolio's simulator API, after asking the simulator's questions (price, notary fees, works, rent, taxe foncière, copropriété, other charges, management fees, vacancy). Use when a user asks about rental profitability, "quelle rentabilité locative", rendement brut vs net, cash-flow of an investissement locatif, or whether a rental property is a good deal.
---

# Rentabilité locative (Vestafolio)

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

Computes the gross and net rental yield and the average monthly cash-flow
(excluding financing) of a buy-to-let investment, from the total acquisition
cost (price, frais de notaire, travaux), the rent and the annual charges
(taxe foncière, copropriété, gestion, vacance locative). The formulas below
are the ones coded in the simulator.

## When to use

- "Is 900 € rent on a 200 000 € flat a good deal?" / "Quelle rentabilité pour
  ce bien ?"
- Questions about rendement brut vs rendement net, or cash-flow of an
  investissement locatif
- Estimating the impact of vacancy, management fees or charges on profitability

## When NOT to use

- Buying a primary residence vs renting — use vestafolio-achat-vs-location
- Loan payments for financing the purchase — use vestafolio-credit-immobilier
- Computing the notary fees input precisely — use vestafolio-frais-notaire first

## Questions to ask before calling the API

The simulator asks these nine inputs, in this order. Ask or confirm each in
French; there is no conditional question.

« Acquisition »

1. « Prix d'achat » → `purchasePrice`.
2. « Frais de notaire » → `notaryFees` (euros; the site's 16 000 € default is
   not derived from the price — chain vestafolio-frais-notaire for a real
   figure, roughly 7-8 % in the ancien, 2-3 % in the neuf).
3. « Travaux et ameublement » → `renovationCost`.
4. « Loyer mensuel » → `monthlyRent` (hors charges).

« Charges annuelles »

5. « Taxe foncière » → `propertyTax` (€/an).
6. « Charges de copropriété » → `condoFees` (€/an, non-recoverable share).
7. « Autres charges » → `otherCharges` (« Assurance PNO, entretien, etc. »).
8. « Frais de gestion » → `managementFeesPercent` (percent of the rent
   collected; the site allows 0 to 15; 0 for self-management).
9. « Vacance locative » → `vacancyWeeks` (« Période sans locataire (en
   semaines par an) », 0 to 52).

## Formulas as coded in the simulator

- Total acquisition cost = price + notary fees + works; both yields are a
  percent of this total, not of the price alone.
- Gross yield = 12 × monthly rent / acquisition cost (no vacancy).
- Vacancy loss = gross rent × weeks / 52; rent after vacancy = gross rent −
  vacancy loss; management fees = that rent × percent.
- Annual charges = taxe foncière + copropriété + other charges + management
  fees. Net rent = rent after vacancy − annual charges.
- Net yield = net rent / acquisition cost; monthly cash-flow = net rent / 12,
  before any loan or tax.
- Site disclaimer: « Ce calcul ne prend pas en compte le financement ni la
  fiscalité. »

## How to call the API

Always fetch the canonical input schema first (fields, bounds, defaults):

```
GET https://www.vestafolio.com/api/tools/v1/rentabilite-locative
```

Then POST the user's parameters (all amounts in euros, rates in percent):

```bash
curl --fail-with-body --silent --show-error --max-time 30 -X POST https://www.vestafolio.com/api/tools/v1/rentabilite-locative \
  -H 'Content-Type: application/json' \
  -d '{
    "purchasePrice": 200000,
    "notaryFees": 16000,
    "renovationCost": 5000,
    "monthlyRent": 900,
    "propertyTax": 1200,
    "condoFees": 1800,
    "otherCharges": 300,
    "managementFeesPercent": 8,
    "vacancyWeeks": 2
  }'
```

Unknown fields are rejected (strict schema) — if you get a `validation_error`,
re-read the schema from the GET endpoint rather than guessing field names.

## Interpreting the output

- `grossYield` vs `netYield` — always present both; the gap shows how much
  charges and vacancy eat into the headline number. Net yield is the decision
  metric.
- `monthlyCashFlow` — average monthly net rental income before any loan;
  negative means charges exceed rents even without financing
- `annualNetRent` (after vacancy), `netRent`, `annualCharges`, `vacancyLoss`
  — the components behind the net yield, useful to explain what to optimize
- `totalAcquisitionCost` — the denominator of both yields

## Caveats

- Excludes financing (mensualités) and taxation of rental income — a positive
  cash-flow here can turn negative once a loan and impôts are added; chain
  vestafolio-credit-immobilier and vestafolio-micro-foncier-vs-reel or
  vestafolio-lmnp-fiscalite.
- Estimates with constant rent and charges; not investment advice — say so.
- Interactive simulator, if useful to the user:
  https://www.vestafolio.com/simulateurs/rentabilite-locative
