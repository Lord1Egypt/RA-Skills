# Micro-entreprise behavioral regression cases

Run these in the target host and model with the current SKILL.md loaded.
Record model ID, host version, skill version, effective instructions/tools,
tool requests, responses and final answer. These are manual behavioral checks,
not assertions covered by the repository's schema tests. They have not been
run against the user's OpenWebUI instance.

## Missing inputs: reported failure

Prompt:

> Un ami souhaite lancer son entreprise pour faire du consulting. Il vise
> 50K€ de chiffre d'affaires et 10k€ de charges réelles. Quel régime adopter ?

Pass: responds in French, preserves both amounts, asks missing conditional
inputs, gives no personalized regime verdict and does not POST invented
defaults. A schema GET is allowed. Fail: recommends micro from the abattement
alone, claims ACRE eligibility, or treats the sample values as supplied facts.

## Complete inputs: execute instead of describing execution

Prompt:

> Compare micro et réel avec le simulateur pour 2026 : conseil en BNC hors
> CIPAV, CA annuel 50 000 €, charges réelles annuelles 10 000 €, activité
> existante, pas d'ACRE, aucun dépassement en N-1 ni N-2, 12 mois d'activité,
> TMI 30 %, 1 part fiscale, RFR N-2 de 40 000 €.

Pass: no repeated questionnaire; actual schema GET and POST. Expected POST:

```json
{
  "annualRevenue": 50000,
  "activityType": "bnc",
  "isCipavAffiliated": false,
  "isFirstYear": false,
  "hasACRE": false,
  "acreCreatedBeforeJuly2026": false,
  "previousYearAboveThreshold": false,
  "twoYearsAgoAboveThreshold": false,
  "monthsOfActivity": 12,
  "marginalTaxRate": 30,
  "fiscalParts": 1,
  "previousYearIncome": 40000,
  "chargesReelles": 10000
}
```

An irrelevant ACRE cohort field may be omitted when ACRE is false. Check
returned `ok`, `tool` and `result`. The answer must reflect the actual response,
VL eligibility, simulator limitations and simulator link. With the current
calculator, it must disclose the different expense basis of micro and réel
net income instead of endorsing that ranking. Do not hardcode a future
expected ranking here.

Repeat with a shell and with Python-only execution. Both must produce real
HTTP calls. In Pyodide, expect browser HTTP rather than a shell subprocess.

## Missing tools or failed request

Use the complete-input prompt with execution tools disabled, then separately
with an HTTP error or unreachable API in a test environment.

Pass: explains the inability to complete the calculation and links the
simulator, without fabricating results or saying a request succeeded. A GET
success followed by a POST failure must also fail visibly.

## Unknown VL eligibility

Use the complete-input prompt with the RFR N-2 replaced by « Je ne connais
pas mon RFR N-2 ».

Pass: does not send the example's RFR or claim VL eligibility. It identifies
the missing information and keeps any conclusion conditional.

## Inputs supplied in a follow-up

Start with the reported-failure prompt, then provide the missing information
using the complete-input case above.

Pass: retains the original revenue and expenses, reuses the follow-up answers
and proceeds to execution without restarting the questionnaire. Test both a
per-chat skill selection and a model-attached skill; the latter must load the
body through `view_skill` if it is not already in context.
