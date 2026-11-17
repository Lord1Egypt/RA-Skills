---
name: vestafolio-credit-immobilier
version: 1.2.1
description: Compute French mortgage monthly payments (insurance included), total interest and the full amortization schedule using Vestafolio's simulator API, after asking the simulator's questions (amount borrowed, annual rate, duration, insurance rate). Use when a user asks about mortgage payments, loan cost, "quelle mensualité pour un crédit immobilier", "combien coûte un prêt de 250 000 €", amortization tables (tableau d'amortissement), or assurance emprunteur cost.
---

# Crédit immobilier (Vestafolio)

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

Computes the monthly payment (assurance emprunteur included), the total cost of
credit, total interest, total insurance and the complete month-by-month
amortization schedule for a fixed-rate French mortgage with constant payments.
The conventions below are the ones coded in the simulator.

## When to use

- "What would my monthly payment be for a 250 000 € loan over 20 years?" /
  "Quelle mensualité pour 250 000 € sur 20 ans ?"
- "How much interest will I pay in total?" / "Combien coûte mon crédit ?"
- Requests for a tableau d'amortissement (principal vs interest split per month)
- Estimating the impact of the insurance rate (assurance emprunteur) on payments

## When NOT to use

- "How much CAN I borrow given my income?" — use vestafolio-capacite-emprunt
- Buy vs rent decisions — use vestafolio-achat-vs-location
- Notary/closing costs of the purchase — use vestafolio-frais-notaire

## Questions to ask before calling the API

The simulator asks these four inputs, in this order (card « Paramètres du
prêt »). Ask or confirm each in French.

1. « Montant emprunté » → `principal` — the capital borrowed, not the
   property price (apport and notary fees are outside this tool).
2. « Taux annuel » → `annualRate` (nominal percent; the site allows 0 to 15).
3. « Durée » → `durationYears` (the site allows 5 to 25).
4. « Taux assurance » → `insuranceRate` (annual percent of the initial
   capital; 0 if the user wants the payment hors assurance).

## Conventions as coded in the simulator

- Fixed-rate, constant-payment loan: the crédit part of the payment follows
  the standard annuity formula on the monthly rate (annualRate / 12); at 0 %
  it is principal / months.
- Assurance emprunteur on the initial capital: monthly insurance = principal
  × insuranceRate / 100 / 12, constant over the whole loan.
- `monthlyPayment` includes the insurance; `totalPayment` = monthly payment ×
  months; `totalInterest` = total payment − principal − total insurance.
- The site also shows « Coût du crédit » = interest + insurance and
  « Surcoût » = that cost as a percent of the principal.

## How to call the API

Always fetch the canonical input schema first (fields, bounds, defaults):

```
GET https://www.vestafolio.com/api/tools/v1/credit-immobilier
```

Then POST the user's parameters (all amounts in euros, rates in percent):

```bash
curl --fail-with-body --silent --show-error --max-time 30 -X POST https://www.vestafolio.com/api/tools/v1/credit-immobilier \
  -H 'Content-Type: application/json' \
  -d '{
    "principal": 250000,
    "annualRate": 3.5,
    "durationYears": 20,
    "insuranceRate": 0.3
  }'
```

Unknown fields are rejected (strict schema) — if you get a `validation_error`,
re-read the schema from the GET endpoint rather than guessing field names.

## Interpreting the output

- `monthlyPayment` — total monthly payment, insurance included; say so, and
  give the split `monthlyPaymentWithoutInsurance` + `monthlyInsurance`
- `totalPayment` — total cost of the credit over the full duration
- `totalInterest` / `totalInsurance` — the two cost components beyond the
  capital; useful to show what the loan really costs
- `schedule` — full monthly amortization table (month, payment, principal,
  interest, remainingBalance); use it for "how much will I still owe after N
  years" follow-ups rather than recomputing

## Caveats

- Estimates, not a loan offer — the actual TAEG also includes frais de dossier,
  garantie and other fees not modeled here.
- Fixed rate and constant insurance on initial capital assumed; banks may quote
  insurance on capital restant dû, which is cheaper over time.
- Not financial advice — say so.
- Interactive simulator, if useful to the user:
  https://www.vestafolio.com/simulateurs/credit-immobilier
