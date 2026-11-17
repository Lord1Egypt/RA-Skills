---
name: vestafolio-impot-plus-value
version: 1.2.1
description: Compute French real-estate capital gains tax (impôt sur la plus-value immobilière) with holding-period abatements using Vestafolio's simulator API, after asking the simulator's questions (prices, dates, résidence principale, investissement locatif, régime réel LMNP and amortissements, frais d'acquisition and travaux method). Use when a user asks "plus-value immobilière", how much tax they owe when selling a property or résidence secondaire in France, about the abattement pour durée de détention, the 22/30-year exemptions, LMNP amortization reintegration, or whether to sell now or wait.
---

# Impôt sur la plus-value immobilière (Vestafolio)

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

Computes the tax due on a French property sale: gross and net capital gain,
acquisition-fee and renovation deductions, holding-period abatements, IR at
19 %, prélèvements sociaux at 17,2 %, the high-gain surtax, exemptions, and
the savings from postponing the sale by one year. The rules below are the
ones coded in the simulator; use them to explain, and the API to compute.

## When to use

- "Combien d'impôt sur ma plus-value immobilière ?" / "How much tax if I sell my French property?"
- Questions about the abattement pour durée de détention, or the 22-year (IR)
  and 30-year (PS) exemptions
- Selling a résidence secondaire, a rental, or an LMNP au régime réel
  (amortization reintegration since 2025)
- "Should I sell now or wait a year?" decisions

## When NOT to use

- Capital gains on securities/shares (PFU territory — not this simulator)
- Professional sellers or companies at IS (only particulier and SCI à l'IR are
  modeled)
- Non-French property or non-French tax situations

## Questions to ask before calling the API

The simulator asks these inputs, in this order (card « Paramètres de la
vente »). Ask or confirm each in French; stop early when a gate makes the
rest irrelevant.

1. « Prix d'achat » → `purchasePrice` and « Prix de vente » → `salePrice`.
2. « Date d'achat » → `purchaseDate` and « Date de vente » → `saleDate`
   (YYYY-MM-DD; the sale must be after the purchase; the site defaults the
   sale to today). The holding period is derived from them in whole years
   (the day of the month is ignored).
3. « Résidence principale » (gate) → `isMainResidence` (« Exonération totale
   si oui »). If Oui, the sale is fully exempt: send the flag and skip the
   remaining questions.
4. Only if Non: « Investissement locatif » (gate) → `isRentalInvestment`
   (« Active le traitement spécifique LMNP lors de la revente »). Only if
   Oui: « Régime réel » (gate) → `isRealRegime` (« Si non, le calcul
   standard de plus-value s'applique »). Only if Oui: « Somme totale des
   amortissements à date » → `totalAmortization` (« En LMNP au réel, la
   totalité des amortissements déjà déduits est réintégrée dans la
   plus-value brute. »); the site requires an amount strictly above 0.
5. Only when the gross gain is positive — « Frais déductibles »:
   « Frais d'acquisition » → `acquisitionFeesMethod`: « Forfait 7.5% » =
   `forfait`, « Montant réel » = `reel` (then `acquisitionFeesReal`, the
   documented amount), « Aucun » = `none`. « Travaux » → `renovationMethod`:
   « Forfait 15% » = `forfait` (only available from 5 full years of holding;
   otherwise it yields 0), « Montant réel (justificatifs) » = `reel` (then
   `renovationReal`), « Aucun » = `none`.
6. `sellerType`: the website always uses `particulier`; the API also accepts
   `sci_ir`, which follows the same rules. Send `particulier` unless the user
   sells through a SCI à l'IR.

## Rules and rates as coded in the simulator (2025-2026)

- Standard case: net gain = sale price − purchase price − acquisition fees
  (7,5 % forfait or documented) − works (15 % forfait from 5 years, or
  documented), floored at 0.
- LMNP au régime réel (`isRentalInvestment` and `isRealRegime`): acquisition
  fees are added to the acquisition price instead of being deducted, the
  works are subtracted from the sale price only from 5 years of holding, and
  the amortization deducted during the rental is added back to the gain.
- Abattement IR: 6 % per year from the 6th to the 21st year, 4 % for the
  22nd, so full exemption at 22 years. Abattement PS: 1,65 % per year from
  the 6th to the 21st year, 1,60 % for the 22nd, 9 % per year from the 23rd
  to the 30th, full exemption at 30 years.
- Tax: 19 % IR on the gain after the IR abatement, 17,2 % PS on the gain
  after the PS abatement, plus the surtax on the IR base above 50 000 €
  (2 % to 6 % by bands, with smoothing at each band entry).
- Full exemptions: résidence principale, sale price ≤ 15 000 €, holding of
  30 years or more. From 22 years the IR is exempt and only PS remain.
- `savingsIfWait1Year` = current tax − tax if the sale happened one year
  later (the site suggests waiting when it exceeds 100 €).

## How to call the API

Always fetch the canonical input schema first (fields, bounds, defaults):

```
GET https://www.vestafolio.com/api/tools/v1/impot-plus-value
```

Then POST the user's parameters (amounts in euros, dates as `YYYY-MM-DD`
strings — `saleDate` must be after `purchaseDate`):

```bash
curl --fail-with-body --silent --show-error --max-time 30 -X POST https://www.vestafolio.com/api/tools/v1/impot-plus-value \
  -H 'Content-Type: application/json' \
  -d '{
    "purchasePrice": 200000,
    "salePrice": 280000,
    "purchaseDate": "2015-01-01",
    "saleDate": "2026-06-01",
    "isMainResidence": false,
    "isRentalInvestment": true,
    "isRealRegime": true,
    "totalAmortization": 45000,
    "acquisitionFeesMethod": "forfait",
    "renovationMethod": "reel",
    "renovationReal": 20000,
    "sellerType": "particulier"
  }'
```

Unknown fields are rejected (strict schema) — if you get a `validation_error`,
re-read the schema from the GET endpoint rather than guessing field names.
`acquisitionFeesReal` / `renovationReal` are required with the `reel`
methods.

## Interpreting the output

- `totalTax` — the key decision figure (IR + PS + surtax); `netProceeds` is
  the gain kept after tax, `effectiveTaxRate` the levy on the gross gain
- `grossCapitalGain` vs `netCapitalGain` — before/after acquisition-fee and
  renovation deductions; in LMNP réel also `transferProceeds`,
  `acquisitionPriceUsed` (« Prix d'acquisition corrigé ») and
  `amortizationReintegration`
- `irAbatementRate` / `psAbatementRate` and the corresponding amounts — how
  the holding period shrank the taxable base; `holdingPeriodYears` /
  `holdingPeriodMonths`
- `yearsUntilIRExemption` / `yearsUntilPSExemption` and `savingsIfWait1Year`
  — highlight these for "sell now or wait" questions
- `abatementSchedule` — the full 0-to-30-year abatement table by holding
  duration
- `exemptions` / `isFullyExempt` — applicable exemption reasons (French labels)

## Caveats

- Rules as coded for 2025-2026; rates and abatement schedules change with
  finance laws. Estimates, not tax advice — say so.
- The forfait options (7,5 % fees, 15 % works) are simulator conventions the
  user may or may not be entitled to; actual documented amounts can differ.
- Interactive simulator, if useful to the user:
  https://www.vestafolio.com/simulateurs/impot-plus-value
