---
name: vestafolio-micro-entreprise
version: 1.2.2
description: Compare French micro-entreprise vs régime réel and versement libératoire with actual Vestafolio API calls. Use for consulting or freelance regime choices with projected revenue and expenses, "quel régime adopter", "micro ou réel", cotisations, ACRE, and VL eligibility. Ask missing simulator inputs before recommending; do not answer from remembered tax rules.
---

# Micro-entreprise (Vestafolio)

## Required workflow

For a request within this simulator's scope:

1. Reuse answers already supplied. Ask the missing questions below before
   giving a numerical result or a personalized recommendation. Example values
   and schema defaults are not the user's answers. If supplied facts conflict
   with each other or the API's supported inputs, ask which fact to correct
   before computing. Do not change an explicit answer to make validation pass;
   branch defaults below apply only when the user has not contradicted them.
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

Computes cotisations sociales, impôt and net income of a micro-entreprise
under the versement libératoire (VL) and under the barème progressif, and,
when real professional expenses are provided, compares with the régime réel,
with a recommendation. The numbers come from the API; the rates quoted below
are the ones coded in the simulator, so you can explain a result, never to
compute it yourself.

## When to use

- "Should I opt for the versement libératoire?" / "Micro ou réel ?"
- "Micro-entreprise ou société ?" as a first quantitative step on the micro side
- Estimating net income of an auto-entrepreneur (BNC, services BIC, commerce),
  including the first year with ACRE
- Checking versement libératoire eligibility against the RFR N-2 condition

## When NOT to use

- Comparing SASU vs EURL company structures (use vestafolio-sasu-vs-eurl)
- Choosing a legal form qualitatively (use vestafolio-choisir-regime)
- Revenue above the micro thresholds with no interest in the réel comparison

## Revenue and expenses alone are not enough

For « Un ami souhaite lancer son entreprise pour faire du consulting. Il vise
50K€ de chiffre d'affaires et 10k€ de charges réelles. Quel régime adopter ? »:

- Keep `annualRevenue: 50000` and `chargesReelles: 10000`; never replace
  supplied expenses with the example's or schema's default.
- Confirm the BNC activity and CIPAV affiliation. A planned launch suggests
  a first year; establish the creation date, months of activity and ACRE
  status. Ask the TMI (or household inputs to estimate it), fiscal parts and
  RFR N-2. Group related questions; do not repeat information already given.
- The first response should collect those missing inputs, not recommend
  micro-BNC or ACRE eligibility. No POST is needed until the inputs are known.
- Do not decide from the 34 % abattement versus expenses alone. The
  comparison also depends on social contributions, income tax and VL
  eligibility. A taxable-base comparison is not a net-income comparison.
- Even after execution, check the expense-basis limitation in Caveats before
  endorsing the returned micro-vs-réel recommendation or savings.

Example opening in French: « Je retiens 50 000 € de CA et 10 000 € de charges
annuelles. Pour comparer les régimes, pouvez-vous préciser si ce conseil
relève bien des BNC et s'il dépend de la CIPAV, puis sa date de création et
son éventuel bénéfice de l'ACRE ? Il me faudra aussi sa TMI (ou les revenus
et la composition de son foyer), ses parts fiscales et son RFR N-2. »

## Questions to ask before calling the API

The Vestafolio simulator asks these questions, in this order, before it
computes anything. Do the same: collect or confirm each answer (in French,
with the simulator's wording), skip a question when its condition is not met,
and never silently assume a default for a question marked (gate). If the user
already gave an answer, do not ask again.

1. « Chiffre d'affaires annuel » → `annualRevenue` (euros encaissés dans
   l'année). Seuils micro : 83 600 € (BNC et services BIC), 203 100 € (vente
   de marchandises).
2. « Type d'activité » (gate) → `activityType` : « Profession libérale (BNC) »
   = `bnc` (activités intellectuelles, conseil, expertise) ; « Prestations de
   services (BIC) » = `services` (services artisanaux et commerciaux) ;
   « Vente de marchandises » = `commerce` (achat-revente, fabrication-vente).
3. Only if `bnc` — « Êtes-vous affilié à la CIPAV ? » (gate) →
   `isCipavAffiliated`. Simulator helper: « Oui : 23,4% de cotisations.
   Non : 25,8%. » The simulator defaults to Oui, so ask rather than assume;
   the answer is ignored for `services` and `commerce`.
4. « Comparer avec le régime réel » → « Charges réelles annuelles » →
   `chargesReelles`. Optional: the réel scenario is only computed when it is
   > 0. Examples the simulator gives — BNC : « Logiciel, matériel
   informatique, formation, assurance RC Pro, coworking » ; services :
   « Outillage, véhicule, fournitures, local, formation » ; commerce :
   « Stock, transport, emballage, local commercial ». Ask whenever the user
   mentions expenses or wants a micro vs réel verdict.
5. « Première année d'activité » (gate) → `isFirstYear`.
   - If Oui: « ACRE » — « Bénéficiez-vous de l'ACRE ? » (gate) → `hasACRE`
     (« Aide aux Créateurs et Repreneurs d'Entreprise : application de taux
     réduits de cotisations sociales la première année »). If Oui: « Création
     avant le 1er juillet 2026 » → `acreCreatedBeforeJuly2026` (« Exonération
     ACRE de 50 % (au lieu de 25 % depuis juillet 2026) »). Then « Mois
     d'activité cette année » → `monthsOfActivity` (1 à 12 ; « Le seuil micro
     est proratisé l'année de création »). Send `previousYearAboveThreshold`
     and `twoYearsAgoAboveThreshold` as false only if the user has not supplied
     a conflicting history. If they report prior-year overruns and a first
     year, ask them to clarify before POSTing.
   - If Non: « CA au-dessus du seuil micro en N-1 » →
     `previousYearAboveThreshold` (« Le régime micro se perd après deux
     dépassements consécutifs (N-1 et N-2) »). Only if Oui: « CA également
     au-dessus du seuil en N-2 » → `twoYearsAgoAboveThreshold` (« Si oui, le
     régime micro ne s'applique plus cette année »). Send `hasACRE: false`
     and `monthsOfActivity: 12` only for a consistent full-year profile.
     If the user explicitly reports ACRE or a shorter activity period,
     preserve that information and ask for clarification before POSTing.
     Explain that the API models ACRE only in the first year; do not treat
     this simulator limitation as proof that the user's situation is wrong.
6. « Connaissez-vous votre TMI ? » (gate)
   - Oui: « Tranche marginale d'imposition (TMI) » → `marginalTaxRate`, one
     of 0, 11, 30, 41, 45.
   - Non: ask « Autres revenus imposables du foyer » (« Salaires, pensions,
     loyers, etc. hors micro-entreprise »), « Situation » (Célibataire /
     Marié(e) / Pacsé(e)) and « Enfants à charge », then estimate the TMI the
     way the simulator does: call the impot-revenu tool with
     `revenuNetImposable` = other income + CA × (1 − abattement) (66 % of CA
     for BNC, 50 % for services, 29 % for commerce), the family situation,
     `jointDeclaration` true when married, `partnerIncome` 0 and the number
     of children, and use its `marginalRate` × 100 as `marginalTaxRate`.
7. Versement libératoire test (shown by the simulator next to the TMI):
   « Parts fiscales » → `fiscalParts` (1 célibataire, 2 couple, 2,5 couple
   avec un enfant…) and « Revenu fiscal N-2 » → `previousYearIncome`
   (revenu fiscal de référence de l'avant-dernière année). Ask both: the VL
   is only open when RFR N-2 ≤ 29 315 € × parts. If the user cannot answer,
   say the VL eligibility is unverified instead of assuming the simulator's
   25 000 € default.

## Rules and rates as coded in the simulator (2026)

- Micro thresholds: 83 600 € (BNC and services BIC), 203 100 € (commerce).
  Exceeding it does not end the micro regime immediately: the regime applies
  in year N unless the N-1 AND N-2 turnovers both exceeded the ceiling; the
  current year's overrun only counts for next year. In a creation year the
  ceiling is prorated by `monthsOfActivity` (month-level approximation).
- Abattements forfaitaires: 34 % BNC, 50 % services, 71 % commerce. Taxable
  income = CA × (1 − abattement).
- Cotisations sociales on turnover (CFP training contribution included):
  23,4 % BNC CIPAV, 25,8 % BNC hors CIPAV, 21,5 % services, 12,4 % commerce.
- ACRE first year, creation from 1 July 2026 (25 % exemption): 17,6 % BNC
  CIPAV, 19,4 % BNC hors CIPAV, 16,2 % services, 9,4 % commerce. Creation
  before 1 July 2026 (50 % exemption): 13,6 % BNC CIPAV (the retraite
  complémentaire share is not exempted), 13,0 % BNC hors CIPAV, 10,9 %
  services, 6,3 % commerce.
- Versement libératoire on turnover: 2,2 % BNC, 1,7 % services, 1 %
  commerce, available only if RFR N-2 ≤ 29 315 € per part fiscale.
- Barème scenario: impôt = taxable income × TMI (no barème recomputation).
- Régime réel (when `chargesReelles` > 0, or forced when the micro regime is
  lost): bénéfice = CA − charges; cotisations TNS = 45 % of the bénéfice for
  services, 35 % for BNC and commerce; impôt = (bénéfice − cotisations) ×
  TMI, floored at 0.
- Recommendation = the eligible option with the highest net income (VL needs
  both the RFR condition and the micro regime; réel is always eligible; if
  nothing micro is eligible the answer is `reel`). `annualSavings` = gap
  between the best and worst eligible options.
- `recommendationText` (French) is « Versement libératoire en micro-BNC/BIC
  recommandé », « Micro sans VL en micro-BNC/BIC recommandé », « Le régime
  réel peut être plus avantageux. Attention : comptabilité plus complexe et
  déclaration 2035. » or, when N-1 and N-2 both overran, « Seuil micro
  dépassé les deux années précédentes (N-1 et N-2) : le régime micro ne
  s'applique plus cette année, le régime réel est obligatoire. » A sentence
  is appended when this year's CA exceeds the (prorated) threshold.
- Practical reminders the simulator displays with a VL recommendation: the
  option must be requested from URSSAF before 30 September for the following
  year (or within 3 months of creation). With a réel recommendation: below
  the threshold the réel is not applied by default and must be requested,
  the option locks the business in for 2 years, and it requires full
  accounting with an expert-comptable.

## How to call the API

Always fetch the canonical input schema first (fields, bounds, defaults):

```
GET https://www.vestafolio.com/api/tools/v1/micro-entreprise
```

Then POST the user's parameters (all amounts annual, in euros; rates in percent):

```bash
curl --fail-with-body --silent --show-error --max-time 30 -X POST https://www.vestafolio.com/api/tools/v1/micro-entreprise \
  -H 'Content-Type: application/json' \
  -d '{
    "annualRevenue": 50000,
    "activityType": "bnc",
    "isCipavAffiliated": false,
    "isFirstYear": true,
    "hasACRE": true,
    "acreCreatedBeforeJuly2026": false,
    "previousYearAboveThreshold": false,
    "twoYearsAgoAboveThreshold": false,
    "monthsOfActivity": 12,
    "marginalTaxRate": 30,
    "fiscalParts": 1,
    "previousYearIncome": 25000,
    "chargesReelles": 10000
  }'
```

Unknown fields are rejected (strict schema) — if you get a `validation_error`,
re-read the schema from the GET endpoint rather than guessing field names.
The API also rejects `hasACRE: true` without `isFirstYear: true`, and any
N-1/N-2 overrun flag in a first year.

## Interpreting the output

- `recommendation` — "micro_vl", "micro_ir" or "reel". Apply the expense-basis
  caveat below before interpreting `recommendationText` as a personal verdict.
- `vlEligible` — RFR N-2 condition; if false, present the
  `versementLiberatoire` block as « Non éligible », as the simulator does
- Scenario blocks (`versementLiberatoire`, `baremeProgressif`, and `reel`
  only when charges were provided or the micro regime is lost):
  `socialCharges`, `incomeTax`, `netIncome`, `effectiveRate`, `isEligible`
  (micro regime still applicable), `threshold`
- `details.socialRate` (fraction), `details.acreReduction` (present when ACRE
  applies) and `details.vlRate` — show the user how the rate was built; `cfp`
  is always 0 because the CFP is already inside the rates
- `annualSavings` — net-income gap between the best and worst eligible option;
  subject to the same expense-basis limitation when réel is included

## Caveats

- Rates and thresholds as coded for 2025-2026; they change with finance and
  social-security laws. Estimates, not tax advice — say so.
- The réel scenario is a simplified TNS model, not a full accounting
  simulation; the barème scenario applies the TMI flat to the abattement
  income.
- Verify the net-income basis before comparing expenses: the current micro
  blocks' `netIncome` excludes professional expenses, whereas `reel.netIncome`
  includes them. The API's recommendation can therefore favor micro on an
  inconsistent basis when `chargesReelles` is positive. Disclose this limit;
  do not relay that ranking as a reliable micro-vs-réel verdict or silently
  rewrite the API result. The micro VL-vs-IR comparison uses the same basis.
- TVA and CFE are outside this calculation. Do not infer their thresholds,
  eligibility or amounts from these results; use current official sources
  for a separate question about them.
- The ACRE exemption legally runs to the end of the 3rd civil quarter after
  creation; the simulator approximates it as the first year.
- Interactive simulator, if useful to the user:
  https://www.vestafolio.com/simulateurs/micro-entreprise
