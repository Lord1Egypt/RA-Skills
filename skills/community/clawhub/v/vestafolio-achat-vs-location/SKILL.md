---
name: vestafolio-achat-vs-location
version: 1.2.3
description: Compare final net wealth between buying a primary residence with a mortgage and renting while investing savings, over a chosen horizon, using Vestafolio's simulator API, after asking the simulator's questions (available savings first, market assumptions, purchase scenario, rent scenario). Use when a user asks whether to buy or rent, "acheter ou louer", "est-ce rentable d'acheter ma résidence principale", rent vs buy break-even, or what owning really costs versus renting in France.
---

# Acheter vs louer (Vestafolio)

## Required workflow

For a request within this simulator's scope:

1. Reuse answers already supplied. Ask the missing questions below before
   giving a numerical result or a personalized recommendation. Example values
   and schema defaults are not the user's answers. City, property type,
   condition and surface only help suggest missing assumptions; they are not
   required when the user supplies the corresponding rates, notary fees and
   annual property tax. With complete calculation inputs, proceed to the API.
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

Compares the final net wealth of buying a primary residence with a mortgage
versus staying a tenant and investing the savings, simulated month by month
over a chosen horizon: loan amortization, property appreciation, rent
increases, taxe foncière (indexed at 3 %/year) and capitalization of invested
savings. The model below is the one coded in the simulator; use it to
explain, and the API to compute.

## When to use

- "Should I buy or keep renting?" / "Acheter ou louer ma résidence
  principale ?"
- "After how many years does buying beat renting?" (break-even questions)
- Testing sensitivity to property appreciation, investment returns, rent
  growth or horizon

## When NOT to use

- Buy-to-let / rental-investment profitability — use
  vestafolio-rentabilite-locative
- Sizing the loan or its payment alone — use vestafolio-capacite-emprunt or
  vestafolio-credit-immobilier
- Choosing where to invest the savings themselves — use vestafolio-pea-vs-cto

## Questions to ask before calling the API

The simulator asks these inputs, in this order, and starts with the savings
on purpose: they bound the loan share and the works budget. Ask only for
missing calculation inputs in French; reuse explicit values without asking
for confirmation. Collect descriptive details only when needed to suggest a
missing assumption, then let the user confirm that assumption.

« Hypothèses de marché »

1. « Épargne disponible actuellement » (gate) → `availableSavings`. It funds
   the apport, the notary fees and the works in the buy scenario and is fully
   invested in the rent scenario.
2. « Ville » — not sent to the API; the simulator uses it to suggest the
   appreciation, rent-increase and taxe foncière assumptions below. Ask it
   when the user has no own assumptions.
3. « Appréciation immobilière » → `propertyAppreciation` (%/an). Simulator
   suggestions by city for a horizon ≤ 5 / ≤ 10 / > 10 years: Paris 1,5 /
   2,5 / 3 ; Lyon 2 / 2,5 / 2,8 ; Marseille 2,5 / 2,8 / 2,5 ; Bordeaux 1,8 /
   2,2 / 2,5 ; Toulouse 2,2 / 2,5 / 2,5 ; Nice 2 / 2,3 / 2,5 ; Nantes 2 /
   2,5 / 2,8 ; Strasbourg 1,8 / 2,2 / 2,5 ; Montpellier 2,2 / 2,5 / 2,5 ;
   Lille 2 / 2,3 / 2,5 ; Rennes 2,2 / 2,5 / 2,8 ; Grenoble 1,5 / 2 / 2,2 ;
   Rouen 1,5 / 2 / 2,2 ; Toulon 2 / 2,3 / 2,5 ; Angers 2 / 2,3 / 2,5 ; other
   city 1,5 / 2 / 2,2. Present the suggestion and let the user confirm.
4. « Rendement placements » → `investmentReturn` (%/an) and
   `investmentReturnBuy`: the website uses one rate for both scenarios, so
   send the same value in both fields unless the user explicitly wants the
   owner's leftover savings invested differently.
5. « Horizon de projection » → `horizonYears` (1 to 30 on the site).

« Scénario Achat »

6. « Type de bien » (Appartement / Maison), « État » (Ancien / Neuf) and
   « Surface » — not sent to the API. Skip these questions when
   `notaryFeePercent` and `taxeFonciereAnnual` are already supplied.
   Otherwise, they drive the notary-fee suggestion
   (7,5 % ancien, 2,5 % neuf) and the taxe foncière estimate (per m² per
   year, appartement / maison: Paris 15-35 / 20-45 ; Lyon 12-25 / 15-30 ;
   Marseille 10-22 / 12-28 ; Bordeaux 14-28 / 16-32 ; Toulouse 11-24 /
   14-28 ; Nice 13-30 / 18-40 ; Nantes 12-24 / 14-28 ; Strasbourg 10-22 /
   12-26 ; Montpellier 11-24 / 14-28 ; Lille 13-28 / 16-32 ; Rennes 11-23 /
   13-27 ; Grenoble 10-22 / 12-26 ; Rouen 12-25 / 14-28 ; Toulon 11-24 /
   14-30 ; Angers 10-20 / 12-24 ; other 8-20 / 10-25).
7. « Prix du bien » → `purchasePrice`.
8. « Part empruntée » → `loanAmount` = price × share. Simulator rule: « Un
   apport minimum équivalent à 10% de la valeur du bien est exigé. Votre
   apport + frais de notaire ne peuvent excéder l'épargne disponible. » So
   the website limits the loan share to 90 % of the price. Its cash budget
   must cover apport + notary fees + works. A savings constraint limits the
   cash contribution; it is not a maximum borrowing capacity. These website
   controls are distinct from the API validation described below.
9. « Taux crédit » → `loanRate` and « Durée emprunt » → `loanYears`.
10. « Frais de notaire » → `notaryFeePercent` (percent of the price; 7,5 for
    an ancien, 2,5 for a neuf — chain vestafolio-frais-notaire for an exact
    figure).
11. « Taxe foncière annuelle » → `taxeFonciereAnnual` (indexed at 3 %/year by
    the simulation).
12. « Travaux » → `travaux`, paid cash. Must not exceed savings − apport −
    notary fees (« Maximum autorisé »); above it the website freezes the
    simulation and the API returns a validation error with the ceiling.

« Scénario Location »

13. « Loyer mensuel » → `monthlyRent` (equivalent housing).
14. « Augmentation annuelle du loyer » → `rentIncreaseRate` (%/an; simulator
    suggestion by city: Paris 2,5 ; Lyon 2,3 ; Marseille 2 ; Bordeaux 2,2 ;
    Toulouse 2,1 ; Nice 2,4 ; Nantes 2,3 ; Strasbourg 2 ; Montpellier 2,2 ;
    Lille 2 ; Rennes 2,3 ; Grenoble 1,8 ; Rouen 1,8 ; Toulon 2 ; Angers 2 ;
    other 1,8).

## Model as coded in the simulator

- Buy scenario: the apport (price − loan), the notary fees and the works are
  taken from the savings once; whatever remains is invested at
  `investmentReturnBuy`. The owner pays the mortgage (constant annuity, no
  insurance) and the taxe foncière indexed at 3 %/year from year 1.
- Rent scenario: the full savings are invested at `investmentReturn`; rent
  grows at `rentIncreaseRate` from year 2.
- Effort d'épargne: each year, whichever side has the lower housing outflow
  (mensualités + taxe foncière for the owner, rent for the tenant) invests
  the difference. Savings earn interest from year 2; an effort saved in year
  N earns interest from N+1.
- Property value = price in year 1, then appreciates each year. Intermediate
  years value the stake as property value × repaid share of the loan; at the
  horizon the stake is the sale proceeds (property value − outstanding
  principal).
- Net wealth (buy) = stake − cumulated taxe foncière − cumulated loan
  interest + investment portfolio. Net wealth (rent) = portfolio − cumulated
  rents.
- `recommendation` = `buy` when the difference is strictly positive, else
  `rent`; `breakEvenYear` = first year where the buy wealth reaches the rent
  wealth (null if never). The website words it « L'achat génère X € de
  plus » / « La location génère X € de plus ».

## How to call the API

Always fetch the canonical input schema first (fields, bounds, defaults):

```
GET https://www.vestafolio.com/api/tools/v1/achat-vs-location
```

Then POST the user's parameters (all amounts in euros, rates in percent):

```bash
curl --fail-with-body --silent --show-error --max-time 30 -X POST https://www.vestafolio.com/api/tools/v1/achat-vs-location \
  -H 'Content-Type: application/json' \
  -d '{
    "availableSavings": 80000,
    "propertyAppreciation": 3,
    "investmentReturn": 6,
    "investmentReturnBuy": 6,
    "horizonYears": 20,
    "purchasePrice": 300000,
    "loanAmount": 255000,
    "loanRate": 3.5,
    "loanYears": 20,
    "notaryFeePercent": 7.5,
    "taxeFonciereAnnual": 1500,
    "travaux": 0,
    "monthlyRent": 1200,
    "rentIncreaseRate": 2.5
  }'
```

Note the input constraints: `loanAmount` must not exceed `purchasePrice`, and
`travaux` must fit within savings after apport and notary fees (the response's
`maxTravauxBudget` gives the ceiling). Unknown fields are rejected (strict
schema) — if you get a `validation_error`, re-read the schema from the GET
endpoint rather than guessing field names. For invalid user values, explain
which supplied field was rejected and ask the user to correct it. Do not
invent a financing ceiling or substitute a new loan amount. For example,
`loanAmount > purchasePrice` calls for clarification of those two amounts,
not an unsolicited borrowing-capacity calculation. Only describe a numerical
limit if it was returned by the tool, and keep its field and meaning intact.

## Interpreting the output

- `buyWealth` / `rentWealth` / `difference` — final net wealth of each
  scenario and their gap (positive difference = buying wins)
- `recommendation` — "buy" or "rent" at the chosen horizon
- `breakEvenYear` — highlight it when the user's horizon is close to it
  (moving before break-even favours renting)
- `monthlyPayment` — the mortgage payment (hors assurance) driving the
  monthly-effort comparison
- `buyDetails` / `rentDetails` — decomposition (property value, remaining
  loan, cumulated interest and taxe foncière, portfolios,
  additionalSavingsInvested); use it to explain WHY one side wins, like the
  site's « Détails Achat » / « Détails Location » blocks
- `yearlyData` / `cashflowData` — year-by-year wealth curves and outflows,
  for "what if I sell after N years" follow-ups
- `maxTravauxBudget` — the works ceiling for the given savings

## Caveats

- Sensitive to assumptions: the recommendation can flip with 1-2 points of
  propertyAppreciation or investmentReturn — present a sensitivity check, not
  a verdict.
- Not modeled: assurance emprunteur, copropriété charges and maintenance,
  selling costs, capital-gains rules, tax on investment returns.
- Estimates, not financial advice — say so.
- Interactive simulator, if useful to the user:
  https://www.vestafolio.com/simulateurs/achat-vs-location
