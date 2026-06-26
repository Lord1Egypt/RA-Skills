# Prompt · Citation generation

**The API is open — no API key.**

## Purpose

Produce a correct, consistent World Bank citation for every figure reported,
including the indicator name, code, country, year, and URL.

## Reusable template

```
For each figure you report from World Bank data, emit a citation in EXACTLY this format:

World Bank, {{indicator_name}} ({{indicator_code}}), {{country}}, {{year}}.
https://data.worldbank.org/indicator/{{indicator_code}}

Rules:
- Use indicator.value for {{indicator_name}} and indicator.id for {{indicator_code}}.
- Use country.value for {{country}} (or list multiple countries separated by " / ").
- Use the record's date for {{year}} (or a range "{{start}}–{{end}}").
- If a value was null, do NOT cite a number; state "data not available" for that year.
```

## Variables

| Variable | Source | Example |
|----------|--------|---------|
| `{{indicator_name}}` | `indicator.value` | GDP (current US$) |
| `{{indicator_code}}` | `indicator.id` | NY.GDP.MKTP.CD |
| `{{country}}` | `country.value` | United States |
| `{{year}}` | record `date` | 2023 |

## Example (filled)

```
World Bank, GDP (current US$) (NY.GDP.MKTP.CD), United States, 2023.
https://data.worldbank.org/indicator/NY.GDP.MKTP.CD
```

## Bad

> "US GDP is about 27 trillion dollars." (no source, no code, no year, no URL)

## Good

> "US GDP was ~27.36 trillion (current US$) in 2023.
> Source: World Bank, GDP (current US$) (NY.GDP.MKTP.CD), United States, 2023.
> https://data.worldbank.org/indicator/NY.GDP.MKTP.CD"

> Verification needed: confirm with https://datahelpdesk.worldbank.org/knowledgebase/articles/889392
