---
name: vestafolio-frais-notaire
version: 1.2.1
description: Compute French notary fees (frais de notaire) for a property purchase — DMTO transfer taxes, notary emoluments, débours, CSI, optional mortgage fees — by department and ancien/neuf/terrain using Vestafolio's simulator API, after asking the simulator's questions (price, type of property, département, primo-accédant, hypothèque). Use when a user asks about closing costs, "combien de frais de notaire", droits de mutation, or ancien vs neuf fee differences.
---

# Frais de notaire (Vestafolio)

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

Computes the frais de notaire for a French property purchase — droits de
mutation (DMTO), notary emoluments, débours, contribution de sécurité
immobilière and optional mortgage registration fees — under the 2026 barème,
with department-specific DMTO rates, a primo-accédant flag and an optional
ancien vs neuf comparison. The rates below are the ones coded in the
simulator; use them to explain, and the API to compute.

## When to use

- "How much are notary fees on a 250 000 € flat?" / "Quels frais de notaire
  pour 250 000 € ?"
- Questions about droits de mutation (DMTO), émoluments, or why fees differ
  between ancien and neuf (VEFA)
- Budgeting the full acquisition cost on top of the purchase price
- Department-specific questions and primo-accédant purchases (résidence
  principale)

## When NOT to use

- Loan payments or borrowing capacity — use vestafolio-credit-immobilier or
  vestafolio-capacite-emprunt
- Rental profitability (it takes notary fees as an input) — use
  vestafolio-rentabilite-locative

## Questions to ask before calling the API

The simulator asks these inputs, in this order (card « Paramètres de
l'achat »). Ask or confirm each in French; do not assume a default for a
question marked (gate).

1. « Prix d'achat » → `purchasePrice`.
2. « Type de bien » (gate) → `acquisitionType`: « Ancien (7-8%) » =
   `ancien`, « Neuf (2-3%) » = `neuf` (VEFA or less than 5 years),
   « Terrain » = `terrain`.
3. « Département » → `department` (code, e.g. « 75 - Paris », « 2A -
   Corse-du-Sud », « 971 - Guadeloupe »; the valid codes are in the GET
   schema). It changes the result for ancien and terrain only; for neuf the
   DMTO is a flat rate.
4. Only if not neuf: « Primo-accédant (résidence principale) » (gate) →
   `isPrimoAccedant`. Simulator helper: « La majoration départementale à 5 %
   ne s'applique pas ; certains départements votent un taux réduit dédié
   (hors abattements locaux spécifiques, non modélisés) ». The flag only
   affects the ancien; for a terrain it is accepted but has no effect.
5. « Inclure les frais d'hypothèque » (gate) → `includeMortgage` (« Frais
   d'inscription du prêt au registre foncier »). Only if Oui: « Montant du
   prêt » → `mortgageAmount` (required by the API in that case). Say Non for
   a caution/garantie bancaire, which is not modeled.
6. `compareNeuf`: the website shows the « Comparaison Ancien vs Neuf » card
   automatically for an ancien. Send `true` for an ancien purchase to
   reproduce it (the comparison ignores the mortgage option on both sides).

## Rules and rates as coded in the simulator (barème 2026)

- Ancien and terrain: droit départemental + taxe communale 1,20 % + frais
  d'assiette et de recouvrement of 2,37 % of the droit départemental. The
  droit départemental is 5,00 % in most departments (loi de finances 2025,
  April 2025 to April 2028), 4,50 % in Hautes-Alpes (05), Alpes-Maritimes
  (06), Ardèche (07), Charente (16), Drôme (26), Lozère (48), Oise (60),
  Saône-et-Loire (71), Guadeloupe (971) and Mayotte (976), 4,50 % in
  Hautes-Pyrénées (65) and 3,80 % in Indre (36). Total DMTO ≈ 6,32 % at
  5,00 %, 5,81 % at 4,50 %, 5,09 % at 3,80 %.
- Primo-accédant (ancien only): the droit départemental is capped at 4,50 %;
  Hautes-Pyrénées (65) apply 3,80 % and Savoie (73) 4,00 % to them.
- Neuf: taxe de publicité foncière of 0,715 % of the price instead of the
  DMTO, whatever the department.
- Émoluments du notaire (HT): 3,87 % up to 6 500 €, 1,596 % to 17 000 €,
  1,064 % to 60 000 €, 0,799 % above, plus 20 % TVA.
- Débours: 800 € + 200 € per full 100 000 € of price. Contribution de
  sécurité immobilière: 0,10 % of the price.
- Hypothèque (when included): 0,70 % taxe de publicité foncière + 0,05 % CSI
  + 0,33 % émoluments HT (plus TVA) of the loan amount.
- Local abatements (e.g. Calvados) and negotiated emolument rebates are not
  modeled.

## How to call the API

Always fetch the canonical input schema first (fields, bounds, defaults —
including the list of valid department codes):

```
GET https://www.vestafolio.com/api/tools/v1/frais-notaire
```

Then POST the user's parameters (all amounts in euros):

```bash
curl --fail-with-body --silent --show-error --max-time 30 -X POST https://www.vestafolio.com/api/tools/v1/frais-notaire \
  -H 'Content-Type: application/json' \
  -d '{
    "purchasePrice": 250000,
    "acquisitionType": "ancien",
    "department": "75",
    "isPrimoAccedant": true,
    "includeMortgage": true,
    "mortgageAmount": 200000,
    "compareNeuf": true
  }'
```

Unknown fields are rejected (strict schema) — if you get a `validation_error`,
re-read the schema from the GET endpoint rather than guessing field names.

## Interpreting the output

- `fees.total` and `fees.percentage` — headline numbers: total fees in euros
  and as a percent of the price; the site also shows « Coût total
  acquisition » = price + fees
- `fees` breakdown — `droitsMutation`, `emolumentsNotaire` (TTC),
  `debours`, `contributionSecurite`, `fraisHypotheque`, `tva`; use it to
  explain that most of the "frais de notaire" are taxes, not the notary's
  remuneration
- `fees.breakdown` — `droitsDepartement`, `droitsCommune`, `fraisPrefecture`
  (the frais d'assiette et de recouvrement), `emolumentsHT`, `emolumentsTVA`
- `comparison` (when `compareNeuf` is true) — `ancien` and `neuf` fee blocks
  plus `savings` (« Économie dans le neuf »)

## Caveats

- Estimates under the barème 2026 as coded; the exact amount is fixed by
  the notary at signing (provision then final settlement). Departments can
  still change their DMTO rate until April 2028 — the per-department table
  follows the DGFiP list applicable on 1 June 2026.
- Not tax or legal advice — say so.
- Interactive simulator, if useful to the user:
  https://www.vestafolio.com/simulateurs/frais-notaire
