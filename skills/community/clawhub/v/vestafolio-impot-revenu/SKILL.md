---
name: vestafolio-impot-revenu
version: 1.2.1
description: Compute French income tax (impôt sur le revenu) with the 2026 progressive barème, quotient familial and décote using Vestafolio's simulator API, after asking the simulator's questions (revenu net imposable, situation familiale, déclaration commune, enfants à charge, handicap, garde alternée, parent isolé, réductions). Use when a user asks "combien d'impôt vais-je payer", how much income tax they owe in France, their TMI (marginal tax rate), taux moyen, parts fiscales, or the tax impact of marriage, PACS or children.
---

# Impôt sur le revenu (Vestafolio)

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

Computes French income tax on the progressive barème for a household: bracket
by bracket detail, number of parts fiscales, quotient familial ceiling, décote,
réductions/crédits, net tax, marginal rate (TMI) and effective rate. The
rules below are the ones coded in the simulator; use them to explain, and the
API to compute.

## When to use

- "Combien d'impôt sur le revenu vais-je payer ?" / "How much income tax will I owe in France?"
- Questions about TMI, taux moyen, tranches d'imposition, parts fiscales
- Estimating the tax effect of marriage/PACS, children, résidence alternée or parent isolé
- Estimating a household TMI for another Vestafolio skill (micro-entreprise,
  SASU vs EURL) exactly as the simulators do

## When NOT to use

- Non-French tax residents (the barème is France-specific)
- Social contributions (prélèvements sociaux), CEHR, or flat-taxed (PFU)
  investment income — the API computes barème income tax only
- Rental-income regime choices (use vestafolio-micro-foncier-vs-reel or
  vestafolio-lmnp-fiscalite)

## Questions to ask before calling the API

The simulator's simple mode asks these questions, in this order (card
« Votre situation »). Ask or confirm each in French; do not assume a default
for a question marked (gate).

1. « Revenu net imposable (annuel) » → `revenuNetImposable`: the declarant's
   income after the 10 % abattement for frais professionnels (or frais
   réels). If the user only knows their declared salary, apply the abattement
   the simulator's detailed mode applies: 10 % of the salary, floored at
   509 € and capped at 14 555 € per person, or the frais réels instead when
   the user opts for them (« Transport, repas, formation... »). Say which
   figure you used.
2. « Situation familiale » (gate) → `familySituation`: « Célibataire » =
   `celibataire`, « Marié(e) / Pacsé(e) » = `marie_pacse`, « Divorcé(e) » =
   `divorce`, « Veuf/Veuve » = `veuf`.
3. Only if `marie_pacse`: « Déclaration commune » (gate) → `jointDeclaration`
   (default Oui). Only if Oui: « Revenu brut du conjoint » → `partnerIncome`.
   The API expects the partner's net imposable income: the simulator applies
   the same 10 % abattement (509 € to 14 555 €) to the gross figure it asks
   for, so do the same before sending. For any other situation send
   `jointDeclaration: false` and `partnerIncome: 0`.
4. « Nombre total d'enfants à charge » → `numberOfChildren`.
5. Only if children > 0 — « Parmi ces enfants (un même enfant peut appartenir
   à plusieurs catégories, il n'est jamais compté deux fois dans le total) » :
   « En situation de handicap » → `numberOfChildrenDisabled` and « En garde
   alternée » → `sharedCustodyChildren`. Only if both are > 0: « À la fois en
   situation de handicap et en garde alternée » →
   `sharedCustodyChildrenDisabled`, at least max(0, handicap + alternée −
   total) and at most the smaller of the two counts (the API enforces it).
6. Only for célibataire, divorcé(e) or veuf(ve) with at least one child:
   « Parent isolé » (gate) → `singleParent` (« +0.5 part supplémentaire »,
   case T). The API rejects it with `marie_pacse`.
7. « Réductions et crédits d'impôt » → `reductionsCredits` (dons, emploi à
   domicile, etc.; total annual amount, 0 if none).

Income the API does not model (simulator « Mode détaillé »): the website
also accepts dividends, interest, plus-values mobilières and revenus fonciers
and taxes them outside the barème. Reproduce it when needed: dividends and
interest at PFU cost 31,4 % flat; with the barème option 60 % of dividends
and 100 % of interest and standard plus-values are added to the taxable
income and 18,6 % prélèvements sociaux are due on the gross amounts; PEA
gains after 5 years bear 18,6 % PS only; assurance-vie gains after 8 years
bear 17,2 % PS on the whole gain plus 7,5 % IR after a 4 600 € abattement
(9 200 € for a joint declaration); revenus fonciers enter the barème at 70 %
(micro-foncier), 50 % or 70 % (LMNP forfait) or gross − charges floored at
−10 700 € (réel), minus prior deficits, floored at 0, with 17,2 % PS (nu) or
18,6 % (meublé). Total levy = barème `netTax` + those amounts.

## Rules and rates as coded in the simulator (2026 barème on 2025 income)

- Brackets applied to the quotient familial: 0 % up to 11 600 €, 11 % to
  29 579 €, 30 % to 84 577 €, 41 % to 181 917 €, 45 % above; tax per part ×
  number of parts.
- Parts: 1, or 2 for a joint marie_pacse declaration, or 2 for a veuf with
  children. Children in one ranking (exclusive custody first): 0,5 part each
  for ranks 1-2 and 1 part from rank 3; in résidence alternée 0,25 (ranks
  1-2) and 0,5 (rank 3+). Disabled children add 0,5 part (0,25 when also in
  alternate custody). Parent isolé adds 0,5 part, or 0,25 when all children
  are in alternate custody.
- Quotient familial ceiling: the advantage is capped at 1 807 € per extra
  half-part; for a parent isolé the first child's full part is capped at
  4 262 € (2 131 € when all children are in alternate custody). When the cap
  bites, complementary reductions of up to 1 801 € per invalidity half-part
  (900,50 € per quarter-part) and 2 011 € for a veuf with dependants are
  given back, never below the uncapped tax.
- Décote: applies when gross tax is below 1 982 € (single) or 3 277 € (joint
  couple); décote = 897 € (single) or 1 483 € (couple) − 45,25 % of the gross
  tax, limited to the tax itself.
- Réductions and crédits are subtracted after the décote; net tax floors at 0.
- `marginalRate` is the bracket of the quotient familial; `effectiveRate` =
  net tax / total income.

## How to call the API

Always fetch the canonical input schema first (fields, bounds, defaults):

```
GET https://www.vestafolio.com/api/tools/v1/impot-revenu
```

Then POST the user's parameters (all amounts in euros):

```bash
curl --fail-with-body --silent --show-error --max-time 30 -X POST https://www.vestafolio.com/api/tools/v1/impot-revenu \
  -H 'Content-Type: application/json' \
  -d '{
    "revenuNetImposable": 40000,
    "familySituation": "marie_pacse",
    "jointDeclaration": true,
    "partnerIncome": 31500,
    "numberOfChildren": 2,
    "numberOfChildrenDisabled": 0,
    "sharedCustodyChildren": 0,
    "sharedCustodyChildrenDisabled": 0,
    "singleParent": false,
    "reductionsCredits": 0
  }'
```

Unknown fields are rejected (strict schema) — if you get a `validation_error`,
re-read the schema from the GET endpoint rather than guessing field names.
Cross-field rules also return `validation_error`: sub-counts above the total,
overlap outside its feasible range, `singleParent` with `marie_pacse`.

## Interpreting the output

- `netTax` — the key figure: net income tax due for the year (also given
  monthly as `monthlyTax`); the simulator shows it as « Impôt net à payer »
- `marginalRate` (TMI) — as a decimal (0.30 = 30 %); do not confuse it with
  `effectiveRate`, the average rate in percent, which is always lower
- `numberOfParts` and `quotientFamilial` — how the household splits income;
  `qfCeiling` shows how much QF advantage the cap clawed back (simulator:
  « Plafonnement du QF »)
- `brackets` — per-bracket detail (bounds multiplied by parts), useful to
  explain "why is my TMI 30 %"
- `decote`, `reductions` — adjustments between gross and net tax
- `incomeAfterTax` / `monthlyNetIncome` — what remains after income tax

## Caveats

- Rules as coded for the 2026 barème (2025 income); rates change with finance
  laws. Estimates, not tax advice — say so.
- Excludes prélèvements sociaux, the CEHR surtax and PFU-taxed investment
  income unless you add them as described above: the real total levy can be
  higher.
- Remind users the input is revenu net imposable, not gross salary.
- Interactive simulator, if useful to the user:
  https://www.vestafolio.com/simulateurs/impot-revenu
