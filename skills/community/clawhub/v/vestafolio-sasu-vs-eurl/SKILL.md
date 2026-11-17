---
name: vestafolio-sasu-vs-eurl
version: 1.2.1
description: Compare SASU (président assimilé salarié) and EURL (gérant TNS) net director income for a French solo entrepreneur using Vestafolio's simulator API, after asking the simulator's questions (revenue, deductible charges, capital social, TMI, PFU vs barème, salary level per structure). Use when a user asks "SASU ou EURL", which company structure pays more, about cotisations sociales assimilé salarié vs TNS, dividend taxation in an EURL, or optimal salary vs dividendes split.
---

# SASU vs EURL (Vestafolio)

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

Computes, for the same annual revenue, the total net income of the director in
a SASU (président assimilé salarié) versus an EURL at IS (gérant TNS):
cotisations sociales, impôt sur les sociétés, impôt sur le revenu, dividend
taxation, alerts and a recommendation with the annual net-income gap. The
rules below are the ones coded in the simulator; use them to explain, and the
API to compute.

## When to use

- "SASU ou EURL ?" / "Which structure should I pick for my solo business?"
- Comparing assimilé-salarié vs TNS social charges on the same revenue
- Questions about dividend taxation in an EURL (TNS on dividends above 10 % of
  capital social) or the salary/dividend mix

## When NOT to use

- Choosing among all legal forms including micro-entreprise (use
  vestafolio-choisir-regime for orientation first)
- Micro-entreprise regime comparisons (use vestafolio-micro-entreprise)
- Multi-partner companies (SARL/SAS) — the tool models a solo entrepreneur

## Questions to ask before calling the API

The simulator collects these inputs in this order (card « Paramètres de votre
activité »). Ask or confirm each one in French; do not assume a default for a
question marked (gate).

1. « Chiffre d'affaires annuel » → `targetRevenue` (euros HT prévisionnels).
2. « Charges déductibles » → `chargesDeductibles` (« Frais professionnels :
   loyer, matériel, déplacements, etc. Déduites avant le calcul du
   résultat. »). Must stay below the revenue.
3. « Capital social » → `capitalSocial` (« En EURL, les dividendes au-delà de
   10% du capital sont soumis aux cotisations TNS. »). Ask it whenever
   dividends are expected in the EURL: it moves the TNS threshold.
4. « Connaissez-vous votre TMI ? » (gate)
   - Oui: « Tranche marginale d'imposition (TMI) » → `marginalTaxRate`, one
     of 0, 11, 30, 41, 45. Send the same value as `sasuMarginalTaxRate` and
     `eurlMarginalTaxRate`.
   - Non: ask « Autres revenus du foyer », « Situation » (Célibataire /
     Marié(e) / Pacsé(e)) and « Enfants à charge ». The simulator then
     estimates one TMI per structure. Before those calls, explain that the
     household inputs and each structure's salary will also be sent to
     `https://www.vestafolio.com/api/tools/v1/impot-revenu`. Include both calls
     in the user's approval scope, or obtain agreement for this additional
     data use if it was not covered. If declined, ask for a user-chosen TMI
     assumption instead and label it as an assumption. With approval, fetch
     that tool's schema and call the impot-revenu tool twice with
     `revenuNetImposable` = other income + the gross salary of that structure
     (see 6 and 7), the family situation, `jointDeclaration` true when
     married, `partnerIncome` 0 and the children; use each `marginalRate`
     × 100 as `sasuMarginalTaxRate` / `eurlMarginalTaxRate`, and the higher
     of the two as `marginalTaxRate`.
5. « Fiscalité des dividendes » (gate) → `preferPFU`: « PFU (Flat Tax
   31,4 %) » = true, « Barème progressif (abattement 40%) » = false.
6. « SASU : Rémunération brute du dirigeant » → `sasuSalaryAmount`, between
   0 € (« 100% dividendes ») and the maximum 55 % × (CA − charges). Simulator
   helper: « Les cotisations sociales sont calculées sur la base (CA -
   charges). Vous choisissez ensuite le montant de rémunération brute à vous
   verser. Le reste sera disponible en dividendes. » Omit the field to take
   the maximum (all in salary, no dividends), as the simulator does by
   default.
7. « EURL : Rémunération brute du dirigeant » → `eurlSalaryAmount`, between
   0 € and the maximum (CA − charges) / 1,45. Helper: « Les cotisations
   sociales (45%) sont calculées sur la rémunération brute et déduites comme
   charge de la société. Le reste du bénéfice est distribué en dividendes. »
   Omit to take the maximum.

When the user wants "the best split", run several salary levels (the
simulator has sliders) and compare `netIncome`; do not guess an optimum.

## Rules and rates as coded in the simulator (2026)

- Base = CA − charges déductibles (floored at 0).
- SASU: cotisations = 45 % of the base, whatever the salary; maximum gross
  salary = base − cotisations = 55 % of the base; the rest after salary is
  taxed at IS and fully distributed. Lowering the salary therefore does not
  lower the SASU cotisations in this model.
- EURL: cotisations TNS = 45 % of the gross rémunération (a company expense);
  maximum rémunération = base / 1,45; résultat avant IS = base − cotisations
  − rémunération, fully distributed after IS.
- IS: 15 % up to 42 500 € of profit, then 25 %.
- Impôt sur le revenu on the rémunération: 2026 barème for one part, applied
  to the gross amount without the 10 % abattement — 0 % to 11 600 €, 11 % to
  29 579 €, 30 % to 84 577 €, 41 % to 181 917 €, 45 % above.
- Dividends: IR 12,8 % (PFU) or 60 % of the dividend × TMI (barème, 40 %
  abattement); prélèvements sociaux 18,6 %. EURL only: the slice of
  dividends above 10 % of the capital social bears 45 % TNS instead of the
  18,6 % PS (IR unchanged).
- Alerts (SASU only): `salaryBelowSmic` when 0 < gross salary < 22 404,24 €
  (SMIC annuel brut, 1 867,02 €/month since June 2026); `highDividendRatio`
  when net dividends exceed 50 % of the director's net income.
- Recommendation: `sasu` if its net income is strictly higher, otherwise
  `eurl` (ties go to EURL); `annualSavings` is the absolute gap. The
  simulator gives no textual reason beyond the amount.
- Warning the simulator shows whenever dividends are distributed:
  « Les dividendes ne sont distribuables qu'à partir du 2ème exercice
  comptable et nécessitent une trésorerie suffisante. Ils ne génèrent pas de
  droits à la retraite ni de protection sociale. »

## How to call the API

Always fetch the canonical input schema first (fields, bounds, defaults):

```
GET https://www.vestafolio.com/api/tools/v1/sasu-vs-eurl
```

Then POST the user's parameters (all amounts annual, in euros; rates in percent):

```bash
curl --fail-with-body --silent --show-error --max-time 30 -X POST https://www.vestafolio.com/api/tools/v1/sasu-vs-eurl \
  -H 'Content-Type: application/json' \
  -d '{
    "targetRevenue": 100000,
    "chargesDeductibles": 10000,
    "capitalSocial": 10000,
    "marginalTaxRate": 30,
    "sasuMarginalTaxRate": 30,
    "eurlMarginalTaxRate": 30,
    "sasuSalaryAmount": 30000,
    "eurlSalaryAmount": 30000,
    "preferPFU": true
  }'
```

Unknown fields are rejected (strict schema) — if you get a `validation_error`,
re-read the schema from the GET endpoint rather than guessing field names.
Salary amounts above the maximum are capped silently: check
`maxSalaryAvailable` in the response.

## Interpreting the output

- `recommendation` — "sasu" or "eurl"; `annualSavings` — the net-income gap
- Per-structure blocks (`sasu`, `eurl`): `netIncome`, `totalTax`,
  `effectiveRate`, `companyView` (CA → charges → rémunération → cotisations →
  résultat avant IS → IS → dividendes) and `directorView` (rémunération
  brute, IR, rémunération nette, dividendes perçus, impôt dividendes, total)
- `maxSalaryAvailable` — tell the user when their requested salary was capped
- `alerts.salaryBelowSmic` / `alerts.highDividendRatio` — relay the
  simulator's warnings: « Le salaire brut est inférieur au SMIC annuel. Cela
  peut limiter vos droits sociaux. » and « Les dividendes représentent plus
  de 50% de vos revenus. Votre protection sociale sera réduite. »
- `details.dividendIR`, `details.dividendPS`, `details.tnsContributions` —
  the EURL TNS on dividends is `dividendTax` minus IR and PS
- `breakdownComparison` — SASU vs EURL table (charges sociales, IS,
  fiscalité des dividendes, total prélèvements, revenu net)

## Caveats

- Simplified 45 % cotisation rates on both sides; real assimilé-salarié
  charges (employer + employee) and TNS scales differ. Estimates, not tax or
  legal advice — say so.
- Assumes the full post-remuneration profit is distributed as dividends and
  taxes the rémunération as a single-part household without the 10 %
  abattement.
- Interactive simulator, if useful to the user:
  https://www.vestafolio.com/simulateurs/sasu-vs-eurl
