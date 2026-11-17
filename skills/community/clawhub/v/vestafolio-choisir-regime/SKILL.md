---
name: vestafolio-choisir-regime
version: 1.2.1
description: Determine which French business legal forms (micro-entreprise, EI, EURL, SASU, SARL, SAS, SELARL, SELAS) an entrepreneur is eligible for and get a recommendation using Vestafolio's simulator API, after asking the simulator's questions (activity category, projected turnover, existing business, liability, partners, unemployment insurance). Use when a user asks "quel statut juridique", which legal structure to start a business in France, micro-entreprise eligibility, or whether to create a company for liability or assurance chômage reasons.
---

# Choisir son régime d'entreprise (Vestafolio)

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

Determines the eligible French legal forms for an entrepreneur's profile
(activity, projected turnover, partners, liability and unemployment-insurance
wishes) and recommends the most suitable one, with advantages, disadvantages
and reasoning. This is a qualitative orientation tool: it computes no
cotisations and no taxes.

## When to use

- "Quel statut juridique choisir ?" / "Should I start as micro-entreprise or
  create a company?"
- Checking micro-entreprise eligibility (turnover thresholds, existing
  business, regulated professions)
- Orienting a profile with partners, limited-liability needs, or a wish for
  assurance chômage toward the right family of structures

## When NOT to use

- Quantitative net-income comparisons — follow up with
  vestafolio-sasu-vs-eurl or vestafolio-micro-entreprise instead
- Tax or cotisation amounts (this tool returns none by design)
- Non-French business structures

## Questions to ask before calling the API

The simulator is a three-step wizard. Ask the questions of step 1, then
step 2, in French, before presenting any result; do not assume a default for
a question marked (gate).

Step 1 — « Votre activité » (« Décrivez votre projet pour identifier les
régimes adaptés »)

1. « Type d'activité » (gate) → `activityCategory` : « Vente de
   marchandises » = `vente` (E-commerce, boutique, vente en ligne) ;
   « Prestations de services (BIC) » = `services_bic` (Restauration,
   transport, hébergement) ; « Prestations de services (BNC) » =
   `services_bnc` (Consultant, développeur, designer) ; « Profession libérale
   réglementée » = `liberal` (Médecin, avocat, architecte) ; « Artisanat » =
   `artisan` (Plombier, électricien, menuisier) ; « Commerce de détail » =
   `commerce` (Épicerie, librairie, magasin).
2. « Chiffre d'affaires prévisionnel (annuel) » → `projectedTurnover`.
   Simulator helper: « Seuil micro-entreprise : 203 100 € » for vente and
   commerce, « 83 600 € » for the other categories (not shown for a
   regulated profession, which is never micro-eligible).
3. « Avez-vous déjà une entreprise ? » (gate) → `hasExistingBusiness`
   (« Impacts sur l'éligibilité au statut micro » — Oui removes the
   micro-entreprise).

Step 2 — « Vos besoins » (« Précisez vos critères pour affiner la
recommandation »)

4. « Protection du patrimoine personnel » (gate) → `needsLimitedLiability`
   (« Limiter votre responsabilité aux apports dans la société »).
5. « Projet avec associé(s) » (gate) → `hasPartners` (« Ouvre les formes
   pluripersonnelles (SARL/SAS et SEL pour professions réglementées) »).
6. « Accès à l'assurance chômage » (gate) → `wantsUnemploymentInsurance`
   (« Possibilité de toucher le chômage en cas d'arrêt d'activité »).

The web form also shows optional household fields: `maritalStatus`,
`numberOfChildren`, and `otherIncome`. They do not affect this tool's
eligibility or recommendation. Do not ask for them or include them in the
POST body, even if already known. The API accepts their omission; its internal
defaults are not claims about the user's household.

## Rules as coded in the simulator (2026)

- Micro thresholds: 203 100 € (vente, commerce), 83 600 € (services_bic,
  artisan, services_bnc, liberal).
- Micro-entreprise eligible only if the activity is not `liberal`, the
  turnover is ≤ threshold and there is no existing business. It is
  recommended when neither limited liability nor unemployment insurance is
  wanted (« Idéal pour démarrer avec un faible CA et une gestion
  simplifiée »).
- Entreprise individuelle is always eligible (non-liberal) and recommended
  when the turnover exceeds the threshold without a liability need (« Adapté
  pour un CA élevé avec déduction des charges réelles »).
- `liberal`: only SELARL (recommended with liability need and no chômage
  wish) and SELAS (liability need and chômage wish) are proposed; the
  explanations recall that a SEL needs a majority of practising
  professionals in capital and votes.
- `hasPartners`: SARL (liability, no chômage) and SAS (liability and chômage)
  replace EURL and SASU.
- Solo, non-liberal: SASU is proposed (recommended with liability need and
  either a chômage wish or a `services_bnc` activity); EURL is proposed too
  except for `services_bnc` — the simulator explains « En prestations de
  services (BNC), l'EURL n'est pas proposée : la SASU est l'option sociétaire
  en solo. »
- `recommendedRegime` = the first regime flagged recommended, otherwise the
  first eligible one (its generic description is then shown as the reason).
- Each regime carries `nextSimulatorLink`: /simulateurs/micro-entreprise for
  micro-entreprise and EI, /simulateurs/sasu-vs-eurl for company forms.

## How to call the API

Always fetch the canonical input schema first (fields, bounds, defaults):

```
GET https://www.vestafolio.com/api/tools/v1/choisir-regime
```

Then POST the user's profile (amounts in euros):

```bash
curl --fail-with-body --silent --show-error --max-time 30 -X POST https://www.vestafolio.com/api/tools/v1/choisir-regime \
  -H 'Content-Type: application/json' \
  -d '{
    "activityCategory": "services_bnc",
    "projectedTurnover": 50000,
    "hasExistingBusiness": false,
    "needsLimitedLiability": true,
    "hasPartners": false,
    "wantsUnemploymentInsurance": true
  }'
```

Unknown fields are rejected (strict schema) — if you get a `validation_error`,
re-read the schema from the GET endpoint rather than guessing field names.

## Interpreting the output

- `recommendedRegime` — the suggested structure with `recommendationReason`
  (or its `description` when no criterion matched — say so)
- `eligibleRegimes` — every eligible form with French `advantages` and
  `disadvantages` lists you can relay directly (the simulator shows the first
  three of each)
- `microEntrepriseEligible`, `microEntrepriseThreshold`,
  `turnoverExceedsThreshold` — explain micro eligibility explicitly,
  including the existing-business exclusion, which the explanations do not
  spell out
- `explanations` — the reasoning trail in French, useful to justify the answer
- `nextSimulatorLink` on a regime — hand the user the matching Vestafolio
  simulator (and the matching skill) for the quantitative follow-up

## Caveats

- Qualitative orientation only: no cotisation or tax math — for numbers,
  chain into vestafolio-sasu-vs-eurl or vestafolio-micro-entreprise.
- Eligibility rules as coded for 2026; legal thresholds evolve. Estimates,
  not legal advice — say so.
- Interactive simulator, if useful to the user:
  https://www.vestafolio.com/simulateurs/choisir-regime
