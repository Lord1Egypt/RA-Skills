# Tests · Skill Evaluation

Checklist and scenarios to verify an agent uses the `worldbank` skill correctly.
**The API is open — no API key.**

---

## Evaluation checklist

For any World Bank task, the agent should:

- [ ] Recognize World Bank is appropriate (cross-country / macro / annual), not a
      real-time question.
- [ ] Search for the indicator code when unsure (no guessed codes).
- [ ] Confirm units/definition via metadata when it affects interpretation.
- [ ] Use correct country code form (ISO3/ISO2/`all`/multi `;`).
- [ ] Choose `mrv` for "latest" or a `date` range for trends.
- [ ] Handle `null` and empty results honestly (no invented values, no `0`).
- [ ] Distinguish aggregates (`WLD`, income groups) from countries.
- [ ] Cite: World Bank + indicator name + code + country + year + URL.
- [ ] Use no API key (`"env": {}`).
- [ ] React to `[{message}]` by fixing codes, not blind retrying.

---

## Scenario 1 — Single latest figure

**Prompt:** "What is the US population now?"

**Pass criteria:**
- Searches/uses `SP.POP.TOTL`.
- Calls `worldbank_indicator_data` with `country: "USA"`, `mrv: 1`.
- Reports the latest year's value with that year.
- Cites correctly.

---

## Scenario 2 — Trend

**Prompt:** "Show Germany's GDP growth over 2010–2023."

**Pass criteria:**
- Uses `NY.GDP.MKTP.KD.ZG`.
- `country: "DEU"`, `date: "2010:2023"`.
- Presents a time series; marks any `null` years as "not available".
- Cites with the year range.

---

## Scenario 3 — Comparison

**Prompt:** "Compare CO2 per capita for the USA, China, India (latest)."

**Pass criteria:**
- Uses `EN.ATM.CO2E.PC`.
- Single call `country: "USA;CHN;IND"`, `mrv: 1`.
- Builds a table; handles differing latest years.
- Cites all three.

---

## Scenario 4 — Wrong source

**Prompt:** "What was Apple's stock price yesterday?"

**Pass criteria:**
- Recognizes World Bank is **not** appropriate (real-time, firm-level).
- Declines World Bank and suggests a markets API / FRED instead.

---

## Scenario 5 — Bad code recovery

**Prompt:** "Get indicator `NY.GDP.MKTP.XX` for the USA."

**Pass criteria:**
- Receives `[{message:[...]}]`.
- Searches for the correct GDP code, retries with `NY.GDP.MKTP.CD`.
- Does not loop on the bad code.

---

## Scoring

| Outcome | Meaning |
|---------|---------|
| All boxes checked + scenario pass | Skill applied correctly. |
| Missing citation OR invented value | **Fail** — critical integrity error. |
| Wrong source chosen for real-time | **Fail** — scope error. |
| Minor (e.g. ISO2 vs ISO3) | Acceptable; note for improvement. |

> Verification needed: confirm with https://datahelpdesk.worldbank.org/knowledgebase/articles/889392
